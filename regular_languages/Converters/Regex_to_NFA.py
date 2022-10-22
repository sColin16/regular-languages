from typing import Tuple
from regular_languages import Regex
from regular_languages import NFA
from regular_languages.NFAs.nfa import SpecialSymbols, TransitionMap
from regular_languages.RegularExpressions.regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, RegexAST, SymbolNode, UnionNode

def Regex_to_NFA(regex: Regex) -> NFA:
    '''
    Constructs an NFA the recognizes the same langauge as the provided regex
    '''

    transition_map, accept_state = Regex_to_NFA_transition_map(regex.ast, 0)

    return NFA.from_transition_map(transition_map, 0, {accept_state}, states = set(range(accept_state + 1)), alphabet=regex.alphabet)

def Regex_to_NFA_transition_map(ast: RegexAST[str], start_id: int) -> Tuple[TransitionMap[int, str], int]:
    '''
    Recursive function to convert an ast for a regex to a transition map for an
    NFA. Returns the transition map and the final state id
    '''

    transition_map: TransitionMap[int, str]

    match ast:
        case EmptyStrNode():
            end_id = start_id + 1
            transition_map = {start_id: {SpecialSymbols.EMPTY: {end_id}}}

        case EmptyLangNode():
            end_id = start_id + 1
            transition_map = {}

        case SymbolNode(symbol):
            end_id = start_id + 1
            transition_map = {start_id: {symbol: {end_id}}}

        case ConcatNode(left_ast, right_ast):
            left_transition_map, left_id = Regex_to_NFA_transition_map(left_ast, start_id)
            right_transition_map, right_id = Regex_to_NFA_transition_map(right_ast, left_id + 1)

            transition_map = left_transition_map | right_transition_map | {
                left_id: {SpecialSymbols.EMPTY: {left_id + 1}}
            }
            end_id = right_id

        case UnionNode(left_ast, right_ast):
            left_transition_map, left_id = Regex_to_NFA_transition_map(left_ast, start_id + 1)
            right_transition_map, right_id = Regex_to_NFA_transition_map(right_ast, left_id + 1)

            end_id = right_id + 1
            transition_map = left_transition_map | right_transition_map | {
                start_id: {SpecialSymbols.EMPTY: {start_id + 1, left_id + 1}},
                left_id: {SpecialSymbols.EMPTY: {end_id}},
                right_id: {SpecialSymbols.EMPTY: {end_id}}
            }

        case ClosureNode(child_node):
            child_transition_map, child_end_id = Regex_to_NFA_transition_map(child_node, start_id + 1)

            if child_end_id in child_transition_map and SpecialSymbols.EMPTY in child_transition_map[child_end_id]:
                child_end_transitions = child_transition_map[child_end_id][SpecialSymbols.EMPTY]
            else:
                child_end_transitions = set()

            end_id = child_end_id + 1
            transition_map = child_transition_map | {
                start_id: {SpecialSymbols.EMPTY: {start_id + 1, end_id}},
                child_end_id: {SpecialSymbols.EMPTY: child_end_transitions.union({start_id + 1, end_id})}
            }

    return transition_map, end_id
