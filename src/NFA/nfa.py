from dataclasses import dataclass
from typing import Dict Generic, Set, TypeAlias, TypeVar

T = TypeVar('T')
U = TypeVar('U')

TransitionFunction: TypeAlias = Callable[[T, U], Set[T]]
TransitionMap: TypeAlias = Dict[T, Dict[U, Set[T]]]
TransitionList: TypeAlias = List[Dict[U, Set[int]]]

@dataclass
class NFA(Generic[T, U]):
    '''
    A generalized non-deterministic finite automata for states and symbols of
    any given type, based on the five components of an NFA
    '''

    # TODO: how to handle empty strings from a type standpoint? A literal empty
    # string? or a special type (which would work better with types, less well
    # with ease of use
    states: Set[T]
    alphabet: Set[U]
    transition_map: TransitionMap
    start_state: T
    accept_states: Set[T]

    # TODO: determine how to handle empty string transitions
    @classmethod
    def from_transition_function(cls, states: Set[T], alphabet: Set[U],
                                 transition_function: TransitionFunction,
                                 start_state:T, accept_states: Set[T]):
        '''
        Constructs an NFA from an arbitrary transition function. Note that the
        provided set of states and alphabet defines the domain of the NFAs
        transition function, even if the provided function accepts other
        symbols/states
        '''

        # Follow a similar procedure to NFAs, but will take more work to
        # identify invalid states contained within the sets
        raise NotImplementedError

    @classmethod
    def from_transition_map(cls, transition_map: TransitionMap, start_state: T,
                            accept_states: Set[T]):
        '''
        Constructs an NFA from a transition map, which may be implicit.
        Transitions that are missing for a state will be assumed to be the
        empty set
        '''

        # Similar process to DFAs, but there is no need to handle dead states,
        # you just direct to the empty set
        raise NotImplementedError

    @classmethod
    def from_transition_list(cls, transition_list: TransitionList,
                             accept_states: Set[int]):
        '''
        Constructs an NFA from a transition list, which is a transition list
        whose states are a subset of the natural numbers by the nature of being
        defined in an array, and start state is always 0 for convenience
        '''

        # Similar to the NFA, convert the list to a transition map, then call
        # the transition map constructor helper

        raise NotImplementedError

    def __post_init__(self):
        '''
        Verifies that the constraints of the NFA have been met
        '''

        assert self.start_state in self.states
        assert self.accept_states.issubset(self.states)

        # TODO: verify the domain and range of the transition map

    def transition_function(self, state: T, symbol: U) -> Set[T]:
        if state not in self.states:
            raise Exception(f'Error computing transition: {state} is not a valid state')

        if symbol not in self.alphabet:
            raise Exception(f'Error computing transition: {symbol} is not in the alphabet')

        return self.transition_map[state][symbol]

    def simulate(self, test_string: List[U], start_states=None) -> Set[T]:
        '''
        Simulates the NFA, returning the resulting set of states. This is
        effectively the extended transition function that handles a string
        instead of a single symbol
        '''

        curr_states = {self.start_state} if start_states is None else start_states

        for symbol in test_string:
            curr_states= set.union(*(self.tranisition_function(state, symbol)
                                     for state in curr_states))

        return curr_states

    def test(self, test_string: List[U]) -> bool:
        final_states = self.simulate(test_string)

        return any(state in self.accept_states for state in final_states)

