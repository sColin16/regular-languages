import itertools
from typing import Set
from regular_languages import NFA, Regex, DFA
from regular_languages.DFAs.dfa import DFASpecialStates
from regular_languages.NFAs.generated_states import BasisState, LeftInternalState, RightInternalState
from regular_languages.NFAs.nfa import SpecialSymbols
from regular_languages.RegularExpressions.regex_ast import UnionNode

def union_regex(regexA: Regex, regexB: Regex):
    new_alphabet = regexA.alphabet.union(regexB.alphabet)
    new_ast = UnionNode(regexA.ast, regexB.ast)

    return Regex(new_alphabet, new_ast)

def union_dfa(dfa1: DFA, dfa2: DFA):
    alphabet = dfa1.alphabet.union(dfa2.alphabet)

    new_dfa1 = augment_dfa(dfa1, alphabet)
    new_dfa2 = augment_dfa(dfa2, alphabet)

    states = set(itertools.product(new_dfa1.states, new_dfa2.states))

    def transition_function(state, symbol):
        dest_state_1 = new_dfa1.transition_function(state[0], symbol)
        dest_state_2 = new_dfa2.transition_function(state[1], symbol)

        return (dest_state_1, dest_state_2)

    start_state = (dfa1.start_state, dfa2.start_state)
    accept_states = {(state1, state2) for state1, state2 in states if state1 in dfa1.accept_states or state2 in dfa2.accept_states}

    return DFA(states, alphabet, transition_function, start_state, accept_states)

def union_nfa(nfa1: NFA, nfa2: NFA):
    states = {BasisState.START}.union(LeftInternalState.wrap(nfa1.states)).union(RightInternalState.wrap(nfa2.states))
    alphabet = nfa1.alphabet.union(nfa2.alphabet)

    # These are WRONG because they don't consider the epsilon closure of the transition function!
    def transition_function(state, symbol):
        match state:
            case LeftInternalState(child) if symbol in nfa1.alphabet or symbol is SpecialSymbols.EMPTY:
                return LeftInternalState.wrap(nfa1.transition_function(child, symbol))

            case RightInternalState(child) if symbol in nfa2.alphabet or symbol is SpecialSymbols.EMPTY:
                return RightInternalState.wrap(nfa2.transition_function(child, symbol))

            case BasisState.START if symbol is SpecialSymbols.EMPTY:
                return {LeftInternalState(nfa1.start_state), RightInternalState(nfa2.start_state)}

            # Catches the cases where the symbol was not valid in the above transitions
            case _:
                return set()

    start_state = BasisState.START
    accept_states = {LeftInternalState(state) for state in nfa1.accept_states}\
                        .union({RightInternalState(state) for state in nfa2.accept_states})

    return NFA.from_unsafe_transition_func(states, alphabet, transition_function, start_state, accept_states)

# TODO: this should be in some other file, probably
def augment_dfa(dfa: DFA, new_alphabet: Set):
    '''
    Produces a DFA with an augmented alphabet, with the DFA entering the dead
    state for character that weren't in the original alphabet
    '''

    states = dfa.states.union({DFASpecialStates.DEAD})

    def transition_function(state, symbol):
        if state is DFASpecialStates.DEAD:
            return DFASpecialStates.DEAD

        elif symbol not in dfa.alphabet:
            return DFASpecialStates.DEAD

        else:
            return dfa.transition_function(state, symbol)

    start_state = dfa.start_state
    accept_states = set(dfa.accept_states)

    return DFA.from_unsafe_transition_func(states, new_alphabet, transition_function, start_state, accept_states)

