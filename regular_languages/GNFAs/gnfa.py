from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Generic, Literal, Set, TypeVar

from regular_languages import DFA
from regular_languages.RegularExpressions.regex_ast import ClosureNode, ConcatNode, RegexAST, UnionNode, extract_alphabet

class SpecialStates(Enum):
    '''
    Helper enum to represent special states for GNFAs
    '''

    SOURCE = auto()
    SINK = auto()

T = TypeVar('T')
U = TypeVar('U')

@dataclass
class GNFA(Generic[T, U]):
    states: Set[T]
    alphabet: Set[U]
    adj_list: Dict[T | Literal[SpecialStates.SOURCE], Dict[T | Literal[SpecialStates.SINK], RegexAST[U]]]

    def __post_init__(self):
        for source_state in self.states.union({SpecialStates.SOURCE}):
            if source_state not in self.adj_list:
                raise Exception(f'{source_state} is missing as a source state from the adjacency list')

            for dest_state in self.states.union({SpecialStates.SINK}):
                if dest_state not in self.adj_list[source_state]:
                    raise Exception(f'{dest_state} is missing as a destination state from the adjacency list')

                implied_sub_alphabet = extract_alphabet(self.adj_list[source_state][dest_state])

                if not implied_sub_alphabet.issubset(self.alphabet):
                    raise Exception('The implied alphabet in an ast is not a subset of the defined alphabet')

    @classmethod
    def from_DFA(cls, dfa: DFA):
        pass

    def to_regexAST(self):
        orig_states = set(self.states)

        for state in orig_states:
            self.rip_state(state)

        return self.adj_list[SpecialStates.SOURCE][SpecialStates.SINK]

    def rip_state(self, rip_state: T):
        # Update the adj list to account for the state being removed
        for source_state in self.states.union({SpecialStates.SOURCE}).difference({rip_state}):
            for dest_state in self.states.union({SpecialStates.SINK}).difference({rip_state}):
                orig_ast = self.adj_list[source_state][dest_state]
                r1 = self.adj_list[source_state][rip_state]
                r2 = self.adj_list[rip_state][rip_state]
                r3 = self.adj_list[rip_state][dest_state]

                self.adj_list[source_state][dest_state] = UnionNode(orig_ast, ConcatNode(ConcatNode(r1, ClosureNode(r2)), r3))

        # Remove the state from the list of states
        self.states.remove(rip_state)

        # Remove the state from the adj list
        del self.adj_list[rip_state]
