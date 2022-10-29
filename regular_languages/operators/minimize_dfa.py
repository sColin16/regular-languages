from typing import Set, TypeVar
from regular_languages.DFAs.dfa import DFA
from regular_languages.operators.helpers import partition_dfa_states

def minimize_dfa(dfa: DFA):
    pr = partition_dfa_states(dfa)

    new_states = set(pr.sets)
    alphabet = dfa.alphabet

    # Maps each new state to an element in that state
    new_state_representative = {}
    for state in new_states:
        repr, *_ = state

        new_state_representative[state] = repr

    def transition_function(state, symbol):
        source_state_repr = new_state_representative[state]
        dest_state_repr = dfa.transition_function(source_state_repr, symbol)

        return pr.get_partition(dest_state_repr)

    start_state = pr.get_partition(dfa.start_state)
    accept_states = {pr.get_partition(accept_state) for accept_state in dfa.accept_states}

    return DFA.from_unsafe_transition_func(new_states, alphabet, transition_function, start_state, accept_states)
