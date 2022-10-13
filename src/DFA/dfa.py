from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, Generic, List, Set, TypeAlias, TypeVar

T = TypeVar('T')
U = TypeVar('U')

TransitionFunction: TypeAlias = Callable[[T, U], T] 
TransitionMap: TypeAlias = Dict[T, Dict[U, T]]
TransitionList: TypeAlias = List[Dict[U, int]]

@dataclass
class DFA(Generic[T, U]):
    '''
    A generalized deterministic finite automata for states and symbols of any
    given type, based on the five components of a DFA
    '''

    states: Set[T]
    alphabet: Set[U]
    transition_map: TransitionMap
    start_state: T
    accept_states: Set[T]

    def __post_init__(self):
        '''
        Verifies that the constraints on the components of the DFA are met
        '''

        assert self.start_state in self.states
        assert self.accept_states.issubset(self.states)

        for state in self.states:
            if state not in self.transition_map:
                raise Exception(f'State {state} is missing from the domain of ' +
                                'the DFA\'s transition function')

            for symbol in self.alphabet:
                if symbol not in self.alphabet:
                    raise Exception(f'Symbol {symbol} is missing from the domain of ' +
                                    'the DFA\'s transition function')

                if self.transition_map[state][symbol] not in self.states:
                    raise Exception('DFA\'s transition function returned state '+
                                    f'{state}, which is not a valid state')

    @classmethod
    def from_transition_function(cls, states: Set[T], alphabet: Set[U],
                                 transition_function: TransitionFunction,
                                 start_state: T, accept_states: Set[T]):
        '''
        Constructs a DFA from an arbitrary transition function. Note that the
        states and alphabet passed will control what is considered valid by the
        DFA, even if the function accepts other states and/or symbols
        '''

        transition_map = defaultdict(dict)

        for state in states:
            for symbol in alphabet:
                next_state = transition_function(state, symbol)

                transition_map[state][symbol] = next_state

        return cls(states, alphabet, transition_map, start_state, accept_states)

    @classmethod
    def from_transition_map(cls, transition_map: TransitionMap, start_state: T,
                            accept_states: Set[T]):
        '''
        Construct a DFA from a transition map, which may be implicit. States
        that have no defined transitions are considered dead states, and
        symbols in the alphabet that are missing from a state's transitions are
        considered transitions to a dead state
        '''

        # TODO: handle a None state being passed, or document that
        # TODO: only create the None state if it's needed
        # TODO: try to consolidate the dead states if possible

        states = set([None])
        alphabet = set()
        final_transition_map = defaultdict(dict)

        # First, construct the pieces of the transition map we do have
        for state in transition_map:
            states.add(state)

            for symbol in transition_map[state]:
                alphabet.add(symbol)

                next_state = transition_map[state][symbol]

                final_transition_map[state][symbol] = next_state
                states.add(next_state)

        # Create a dead state for the DFA, which may not be necessary
        final_transition_map[None] = {symbol: None for symbol in alphabet}

        # Then, take another pass and fill in dead states and dead state transitions
        for state in states:
            # This is a dead state if the state had no defined transitions
            # So fill in all the transitions to loop back to this state
            if state not in final_transition_map:
                final_transition_map[state] = {symbol: state for symbol in alphabet}
                continue

            # Otherwise, direct all undefined transitions for the state to the dead state
            for symbol in alphabet:
                if symbol not in final_transition_map[state]:
                    final_transition_map[state][symbol] = None


        return cls(states, alphabet, final_transition_map, start_state, accept_states)

    @classmethod
    def from_transition_list(cls, transition_list: TransitionList,
                             accept_states: Set[int]):
        '''
        Constructs a DFA from a transition list, which is a transition map
        whose states are a subset of the natural numbers by the nature of being
        defined in an array, and start state is always 0 for convenience
        '''

        transition_map = {index: transitions for index, transitions in
                          enumerate(transition_list)}

        return cls.from_transition_map(transition_map, 0, accept_states)

    # @classmethod
    # def from_NFA(cls, nfa: NFA):
    #     '''
    #     Constructs a DFA that recognizes the same language as the provided NFA
    #     '''

    #     # Basically just modify the transition map to return sets

    #     pass

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

    def get_implicit_transition_map(self):
        '''
        This would return a simplified transition map that essentially undoes
        what the constructor helper for this does, and removes all references
        to the dead state. Good for printing out and understanding DFAs
        '''

        # TODO: I must detect all dead states
        pass

    def __post_init__(self):
        '''
        Verifies that the constraints on the components of the DFA are met
        '''

        assert self.start_state in self.states
        assert self.accept_states.issubset(self.states)

        # TODO: check the domain and range of the transition map match the
        # domain and range define by the state and alphabet
        # We want to do this to check the helper constructors and as 

    def transition_function(self, state: T, symbol: U) -> T:
        if state not in self.states:
            raise Exception(f'Error computing transition: {state} is not a valid state')

        if symbol not in self.alphabet:
            raise Exception(f'Error computing transition: {symbol} is not in the alphabet')

        return self.transition_map[state][symbol]

    def simulate(self, test_string: List[U], start_state=None) -> T:
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

    @classmethod
    def get_minimal(self):
        '''
        Returns the unique equivalent DFA with the minimal number of states
        '''

        # TODO: the states should probably frozen sets of original states
        # We can run a renaming function to get a tranisition list if desired
        pass

    def size(self) -> int:
        '''
        Returns the number of strings accepted by the DFA, or -1 if DFA has
        infinite size
        '''

        raise NotImplementedError

    def asJSON(self) -> str:
        '''
        Returns a JSON representation of the DFA
        '''

        raise NotImplementedError

