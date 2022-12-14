from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, auto
from itertools import product
from typing import Callable, Dict, Generic, Iterable, List, Set, TypeVar

class SpecialSymbols(Enum):
    '''
    A helper enum to represent the empty string as a symbol for transitions
    '''

    EMPTY = auto()

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

TransitionFunction = Callable[[T, U | SpecialSymbols], Set[T]]
TransitionMap = Dict[T, Dict[U | SpecialSymbols, Set[T]]]
TransitionList = List[Dict[U | SpecialSymbols, Set[int]]]

@dataclass
class NFA(Generic[T, U]):
    '''
    A generalized non-deterministic finite automata for states and symbols of
    any given type, based on the five components of an NFA
    '''

    states: Set[T]
    alphabet: Set[U]
    transition_function: TransitionFunction
    start_state: T
    accept_states: Set[T]

    def __post_init__(self):
        '''
        Verifies that the constraints of the NFA have been met
        '''

        if self.start_state not in self.states:
            raise Exception(f'Start state {self.start_state} is not in the set of states')

        if not self.accept_states.issubset(self.states):
            raise Exception('The accept states are not a subset of the valid states')

        for state, symbol in product(self.states, self.alphabet.union({SpecialSymbols.EMPTY})):
            states = self.transition_function(state, symbol)
            if not states.issubset(self.states):
                raise Exception('NFA\'s transition function returned a set of states '+
                                'that are not a subset of the valid states: '+
                                f'States returned: {states}. Valid States: {self.states}')

    @classmethod
    def from_unsafe_transition_func(cls, states: Set[T], alphabet: Set[U],
                                 unsafe_transition_func: TransitionFunction,
                                 start_state: T, accept_states: Set[T]):
        '''
        Constructs an NFA from an unsafe transition function, a transition
        function that may be defined for a state/symbol combination that are
        not considered valid for the NFA, by wrapping the function in checks
        that the arguments are in the true domain
        '''

        def safe_transition_func(state: T, symbol: U | SpecialSymbols) -> Set[T]:
            if state not in states:
                raise Exception(f'{state} is not a valid state')

            if symbol not in alphabet.union({SpecialSymbols.EMPTY}):
                raise Exception(f'{symbol} is not in the alphabet or the empty string')

            return unsafe_transition_func(state, symbol)

        return cls(states, alphabet, safe_transition_func, start_state, accept_states)

    @classmethod
    def from_transition_map(cls, transition_map: TransitionMap[T, U], start_state: T,
                            accept_states: Set[T], states: Set[T] = None, alphabet: Set[U] = None):
        '''
        Constructs an NFA from a transition map, a nested dictionary that
        impliclty defines the alphabet and set of staes, and need not
        explicitly define the transition for every state/symbol combination.
        Non-explicit transitions are considered the empty set
        '''

        # Unpack the states and alpjabet implied in the transition map
        implied_states = set(transition_map.keys())\
                    .union(*(set().union(*(transitions.values())) for transitions
                             in transition_map.values()))

        # The empty string should not be part of the alphabet
        # Ignore the type b/c difference removes empty symbols
        implicit_alphabet: Set[U] = set().union(*(transitions.keys() for transitions
                                 in transition_map.values()))\
                                         .difference({SpecialSymbols.EMPTY}) # type: ignore 

        final_states = implied_states if states is None else states
        final_alphabet = implicit_alphabet if alphabet is None else alphabet

        def unsafe_transition_func(state: T, symbol: U | SpecialSymbols) -> Set[T]:
            if state not in transition_map:
                return set()

            if symbol not in transition_map[state]:
                return set()

            return transition_map[state][symbol]

        return cls.from_unsafe_transition_func(final_states, final_alphabet, unsafe_transition_func,
                                               start_state, accept_states)

    @classmethod
    def from_transition_list(cls, transition_list: TransitionList,
                             accept_states: Set[int]):
        '''
        Constructs an NFA from a transition list, which is a transition list
        whose states are a subset of the natural numbers by the nature of being
        defined in an array, and start state is always 0 for convenience
        '''

        transition_map = {index: transitions for index, transitions in
                          enumerate(transition_list)}

        return NFA.from_transition_map(transition_map, 0, accept_states)

    def epsilon_closure(self, states: Set[T]) -> Set[T]:
        '''
        Computes the epsilon closure of a set of states. That is, the set of
        all states reachable from some set of states, using only epsilon
        transitions (empty strings)
        '''

        # Perform flood fill with epsilon transitions considered as neighbors
        visited = set(states)
        queue = list(states)

        while len(queue) > 0:
            state = queue.pop()

            for next_state in self.transition_function(state, SpecialSymbols.EMPTY):
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append(next_state)

        return visited

    def simulate(self, test_string: Iterable[U], start_states=None) -> Set[T]:
        '''
        Simulates the NFA, returning the resulting set of states. This is
        effectively the extended transition function that handles a string
        instead of a single symbol
        '''

        curr_states = {self.start_state} if start_states is None else start_states
        curr_states = self.epsilon_closure(curr_states)

        for symbol in test_string:
            next_states = set().union(*(self.transition_function(state, symbol)
                                     for state in curr_states))

            curr_states = self.epsilon_closure(next_states)

        return curr_states

    def test(self, test_string: List[U]) -> bool:
        # TODO: consider having this function return false if a symbol is missing from the alphabet
        final_states = self.simulate(test_string)

        return any(final_state in self.accept_states for final_state in final_states)

    def rename_states(self, name_map: Dict[T, V]):
        inv_name_map = {
            value: key for key, value in name_map.items()
        }

        if len(inv_name_map) != len(name_map):
            raise Exception('Invalid name map: the provided map had non-unique mappings')

        states = set(name_map.values())
        alphabet = self.alphabet

        def transition_function(state, symbol):
            orig_state = inv_name_map[state]
            orig_result = self.transition_function(orig_state, symbol)

            return {name_map[state] for state in orig_result}

        start_state = name_map[self.start_state]
        accept_states = {name_map[accept_state] for accept_state in self.accept_states}

        return NFA.from_unsafe_transition_func(states, alphabet, transition_function, start_state, accept_states)

    def rename_states_numeric(self):
        name_map = {
            state: i for state, i in zip(self.states, range(len(self.states)))
        }

        return self.rename_states(name_map)
