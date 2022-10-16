from collections import defaultdict
from itertools import combinations
from regular_languages import DFA
from regular_languages import NFA
from regular_languages.DFAs.dfa import TransitionMap

def NFA_to_DFA(nfa: NFA) -> DFA:
    '''
    Converts an NFA to a DFA that recognizes the same language
    '''

    start_state = frozenset(nfa.epsilon_closure({nfa.start_state}))

    # Perform flood fill to precompute the transitions
    # We have to find all the states anyways, so might as well precompute the transitions
    # for performance gains when the DFA is simulated (as opposed to function
    # composition which would essentially simulate the NFA during DFA operation)
    states = {start_state}
    queue = [start_state]
    transition_map: TransitionMap = defaultdict(lambda: defaultdict(set))

    while len(queue) > 0:
        state = queue.pop()

        for symbol in nfa.alphabet:
            next_state = nfa.simulate([symbol], state)
            frozen_state = frozenset(next_state)

            transition_map[state][symbol] = frozen_state

            if frozen_state not in states:
                states.add(frozen_state)
                queue.append(frozen_state)

    accept_states = {state for state in states if len(state.intersection(nfa.accept_states)) > 0}

    # TODO: consider either dropping disconnected states here or creating it
    # from a thin transition function. The function will be a little more performant
    return DFA.from_transition_map(transition_map, start_state, accept_states)

def NFA_to_DFA_complete(nfa: NFA) -> DFA:
    '''
    Converts an NFA to a DFA using true subset construction: the powerset of the
    DFA's states are the set of states for the NFA. Useful if you wish to
    simulate the NFA from a set of states not reachable from the start state
    '''

    def powerset(input_set):
        return set().union(*((frozenset(c) for c in combinations(input_set, r)) for r in range(len(input_set))))

    states = powerset(nfa.states)
    transition_map = {
        state: {
            symbol: frozenset(nfa.simulate([symbol], state)) for symbol in nfa.alphabet
        } for state in states
    }
    start_state = frozenset(nfa.epsilon_closure({nfa.start_state}))
    accept_states = {state for state in states if len(state.intersection(nfa.accept_states)) > 0}

    return DFA.from_transition_map(transition_map, start_state, accept_states)
