from collections import defaultdict
import itertools
from typing import Dict, FrozenSet, Set, TypeVar

from regular_languages.DFAs.dfa import DFA, DFASpecialStates
from regular_languages.helpers import PartitionRefinement

T = TypeVar('T')
U = TypeVar('U')

def partition_dfa_states(dfa: DFA[T, U]) -> PartitionRefinement[T | DFASpecialStates]:
    '''
    Creates a disjoint parition of states for the dfa, where states are in the
    same partition are considered non-distinguishable, and states in different
    partitions are considered distingusable

    Based loosely on Hopcroft's algorithm outlined here:
    https://en.wikipedia.org/wiki/DFA_minimization
    '''

    # Build the reverse transition map: for every symbol in the alphabet,
    # compute the set of states that can reach each state via that symbol
    reverse_transitions: Dict[U, Dict[T | DFASpecialStates, Set[T | DFASpecialStates]]] = defaultdict(lambda: defaultdict(set))

    for state, symbol in itertools.product(dfa.states, dfa.alphabet):
        dest_state = dfa.transition_function(state, symbol)

        reverse_transitions[symbol][dest_state].add(state)

    # The initial partition splits accept and non accept states
    pr = PartitionRefinement.from_set(set(dfa.states))
    pr.refine(dfa.accept_states)

    # Queue containing partitions to analyze: use the inital partitions
    q: Set[Set[T | DFASpecialStates] | FrozenSet[T | DFASpecialStates]] = set(frozenset(x) for x in pr.sets)

    while len(q) > 0:
        partition = q.pop()

        for symbol in dfa.alphabet:
            # Collect all the states for which a transition along the symbol
            # leads to one of the states in the current partition
            source_states = set()
            for state in partition:
                source_states.update(reverse_transitions[symbol][state])

            # Iterate through each of the new partitions created by refining the
            # partition with the source states
            # x and y are the two disjoint sets that together form a partition
            # that existed before the refinement
            for x, y in pr.refine(source_states):
                # Split the set in the queue if it exists in the queue
                if source_states in q:
                    q.remove(source_states)
                    q.add(frozenset(x))
                    q.add(frozenset(y))

                # Otherwise, add the smaller of the sets to the queue, to
                # achieve log n time complexity
                elif len(x) < len(y):
                    q.add(frozenset(x))
                else:
                    q.add(frozenset(y))

    pr.freeze()
    return pr
