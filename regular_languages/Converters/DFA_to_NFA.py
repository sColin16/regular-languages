from typing import Set, TypeVar
from regular_languages import DFA
from regular_languages import NFA
from regular_languages.DFAs.dfa import SpecialStates
from regular_languages.NFAs.nfa import SpecialSymbols

T = TypeVar('T')
U = TypeVar('U')

def DFA_to_NFA(dfa: DFA[T | SpecialStates, U]) -> NFA[T | SpecialStates, U]:
    '''
    Constructs an NFA that recognizes the same language as the provided DFA
    '''

    # We ignore the type because this difference should make the type correct
    states = set(dfa.states)
    alphabet = set(dfa.alphabet)
    start_state = dfa.start_state
    accept_states = set(dfa.accept_states)

    # Just wrap in a set and handle the empty string as a symbol
    def transition_function(state: T, symbol: U | SpecialSymbols) -> Set[T]:
        if symbol == SpecialSymbols.EMPTY:
            return set()

        return {dfa.transition_function(state, symbol)}

    return NFA(states, alphabet, transition_function, start_state, accept_states)
