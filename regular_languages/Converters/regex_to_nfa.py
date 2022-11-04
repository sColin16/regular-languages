from regular_languages import Regex
from regular_languages import NFA
from regular_languages.NFAs.generated_states import BasisState
from regular_languages.NFAs.nfa import SpecialSymbols
from regular_languages.RegularExpressions.regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, RegexAST, SymbolNode, UnionNode
from regular_languages.operators import union_nfa, concat_nfa, closure_nfa

def regex_to_nfa(regex: Regex) -> NFA:
    '''
    Converts a regular expression to an NFA that recognizes the same language
    '''

    return regex_ast_to_nfa(regex.ast)

def regex_ast_to_nfa(ast: RegexAST) -> NFA:
    '''
    Helper function that recursively converts the regex ast to an NFA that
    recognizes the same language
    '''

    match ast:
        case EmptyStrNode():
            return empty_str_nfa()

        case EmptyLangNode():
            return empty_lang_nfa()

        case SymbolNode(symbol):
            return symbol_nfa(symbol)

        case UnionNode(left, right):
            left_nfa, right_nfa = regex_ast_to_nfa(left), regex_ast_to_nfa(right)

            return union_nfa(left_nfa, right_nfa)

        case ConcatNode(left, right):
            left_nfa, right_nfa = regex_ast_to_nfa(left), regex_ast_to_nfa(right)

            return concat_nfa(left_nfa, right_nfa)

        case ClosureNode(child):
            child_nfa = regex_ast_to_nfa(child)

            return closure_nfa(child_nfa)

# TODO: consider if I should try to reduce code duplication here
def empty_str_nfa():
    '''
    Produces the NFA that recognizes the language containing the empty string
    '''

    states = {BasisState.START, BasisState.ACCEPT}
    alphabet = set()

    def transition_function(state, symbol):
        match (state, symbol):
            case (BasisState.START, SpecialSymbols.EMPTY):
                return {BasisState.ACCEPT}

            case _:
                return set()

    start_state = BasisState.START
    accept_states = {BasisState.ACCEPT}

    return NFA.from_unsafe_transition_func(states, alphabet, transition_function, start_state, accept_states)

def empty_lang_nfa():
    '''
    Produces the NFA that recognizes the empty language containing
    '''

    states = {BasisState.START, BasisState.ACCEPT}
    alphabet = set()

    def transition_function(state, symbol):
        return set()

    start_state = BasisState.START
    accept_states = {BasisState.ACCEPT}

    return NFA.from_unsafe_transition_func(states, alphabet, transition_function, start_state, accept_states)

def symbol_nfa(input_symbol):
    '''
    Produces the NFA that recognizes the language containing a single string
    that consists of the input symbol
    '''
    states = {BasisState.START, BasisState.ACCEPT}
    alphabet = {input_symbol}

    def transition_function(state, transition_symbol):
        match (state, transition_symbol):
            case (BasisState.START, symbol) if symbol == input_symbol:
                return {BasisState.ACCEPT}

            case _:
                return set()

    start_state = BasisState.START
    accept_states = {BasisState.ACCEPT}

    return NFA.from_unsafe_transition_func(states, alphabet, transition_function, start_state, accept_states)
