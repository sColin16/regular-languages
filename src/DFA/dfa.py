from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, auto
from itertools import product
from typing import Callable, Dict, Generic, List, Set, TypeAlias, TypeVar

T = TypeVar('T')
U = TypeVar('U')

TransitionFunction: TypeAlias = Callable[[T, U], T] 
TransitionMap: TypeAlias = Dict[T, Dict[U, T]]
TransitionList: TypeAlias = List[Dict[U, int]]

class SpecialStates(Enum):
    '''
    An helper enum to internally define dead states. This should be treated as
    internal and should not be used to define DFA states externally
    '''

    DEAD = auto()

@dataclass
class DFA(Generic[T, U]):
    '''
    A generalized deterministic finite automata for states and symbols of any
    given type, based on the five components of a DFA
    '''

    states: Set[T | SpecialStates]
    alphabet: Set[U]
    transition_function: TransitionFunction
    start_state: T
    accept_states: Set[T]

    def __post_init__(self):
        '''
        Verifies that the constraints on the components of the DFA are met.

        Note that this function cannot verify that the transition function is
        "safe" (i.e. that it is only defined for the set of valid state/symbol
        combinations). Use the unsafe constructor helper to guarantee that
        '''

        if self.start_state not in self.states:
            raise Exception(f'Start state {self.start_state} is not in the set of states')

        if not self.accept_states.issubset(self.states):
            raise Exception('The accept states are not a subset of the valid states')

        for state, symbol in product(self.states, self.alphabet):
            if self.transition_function(state, symbol) not in self.states:
                raise Exception(f'Transition function returned state {state}, ' +
                                'which is not a valid state')

    @classmethod
    def from_unsafe_transition_func(cls, states: Set[T | SpecialStates], alphabet: Set[U],
                                    unsafe_transition_func: TransitionFunction,
                                    start_state: T, accept_states: Set[T]):
        '''
        Constructs a DFA from an unsafe transition function, a transition
        function that may be defined for state/symbol combinations that are not
        considered valid for the DFA, by wrapping the function in checks that
        the arguments are in the true domain. Provides an "upper bound" on the
        transition function type
        '''

        def safe_transition_func(state: T, symbol: U) -> T:
            if state not in states:
                raise Exception(f'{state} is not a valid state')

            if symbol not in alphabet:
                raise Exception(f'{symbol} is not in the alphabet')

            return unsafe_transition_func(state, symbol)

        return cls(states, alphabet, safe_transition_func, start_state, accept_states)

    @classmethod
    def from_transition_map(cls, transition_map: TransitionMap, start_state: T,
                            accept_states: Set[T]):
        '''
        Constructs a DFA from a transition map, a nested dictionary that
        implictly defines the alphabet and set of states, and need not
        explicitly define the transition for every state symbol combination.
        Non-explicit transitions are considred transitions to a "dead state"
        '''

        # Unpack the states and alphabet implied in the transition map
        states = set(transition_map.keys())\
                    .union(*(transitions.values() for transitions in transition_map.values()))\
                    .union({SpecialStates.DEAD})
        alphabet = set().union(*(transitions.keys() for transitions in transition_map.values()))

        def unsafe_transition_func(state: T, symbol: U) -> T | SpecialStates:
            if state is SpecialStates.DEAD or state not in transition_map:
                return SpecialStates.DEAD

            if symbol not in transition_map[state]:
                return SpecialStates.DEAD

            return transition_map[state][symbol]

        return cls.from_unsafe_transition_func(states, alphabet, unsafe_transition_func,
                                               start_state, accept_states)

    @staticmethod
    def from_transition_list(transition_list: TransitionList,
                             accept_states: Set[int]):
        '''
        Constructs a DFA from a transition list, which is a transition map
        whose states are a subset of the natural numbers by the nature of being
        defined in an array, and start state is always 0 for convenience
        '''

        transition_map = {index: transitions for index, transitions in
                          enumerate(transition_list)}

        # We can't use classmethod because subclasses could restrict non-int states
        return DFA.from_transition_map(transition_map, 0, accept_states)

    # @classmethod
    # def from_NFA(cls, nfa: NFA):
    #     '''
    #     Constructs a DFA that recognizes the same language as the provided NFA
    #     '''

    #     # Use subset construction to do this, possibly creating an intermediate
    #     # NFA that removes the epsilon transitions

    #     pass

    def simulate(self, test_string: Iterable[U], start_state=None) -> T:
        '''
        Simulates the DFA, returning the resulting state. This is the extended
        transition function that accepts a string instead of a single symbol
        '''

        curr_state = self.start_state if start_state is None else start_state

        for symbol in test_string:
            curr_state = self.transition_function(curr_state, symbol)

        return curr_state

    def test(self, test_string: List[U]) -> bool:
        '''
        Tests if the given string is accepted by the DFA
        '''

        return self.simulate(test_string) in self.accept_states

    def get_transition_map(self):
        '''
        Returns a dictionary that explcitly maps out the transition function for the DFA
        '''

        pass

    def get_implicit_transition_map(self):
        '''
        This would return a simplified transition map that essentially undoes
        what the constructor helper for this does, and removes all references
        to the dead state. Good for printing out and understanding DFAs
        '''

        # TODO: I must detect all dead states
        # I feel like maybe this isn't super useful, visualizing is probably better
        pass

    def visualize(self):
        '''
        Can we get graphviz or something to display the DFA?
        '''

        pass


    def get_transition_list(self):
        '''
        This would be an interesting function to rename the states so that we
        could get a super interopable DFA, even for strange states. This would
        be applicable for some of the conversions between DFA types!
        '''

        # TODO: should this be implicit or not? A flag you can pass? Two
        # separate functions?
        # TODO: ideally we would rename states so that state 1 has a transition
        # from state 0, and build out using BFS to get interpretable state ids

        pass

    @classmethod
    def get_minimal(self):
        '''
        Returns the unique equivalent DFA with the minimal number of states.
        '''

        # TODO: the states should probably frozen sets of original states
        # We can run a renaming function to get a tranisition list if desired
        # TODO: can this remove states not connected to the start state? (e.g.
        # the dead state generated) That would be ideal
        pass

    def size(self) -> int:
        '''
        Returns the number of strings accepted by the DFA, or a special enum
        value if the DFA has infinite size
        '''

        raise NotImplementedError

    def asJSON(self) -> str:
        '''
        Returns a JSON representation of the DFA
        '''

        raise NotImplementedError

