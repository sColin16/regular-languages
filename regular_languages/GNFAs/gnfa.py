from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Dict, Generic, Literal, Set, TypeVar

from regular_languages import DFA
from regular_languages.DFAs.dfa import DFASpecialStates
from regular_languages.RegularExpressions.regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, RegexAST, SymbolNode, UnionNode, extract_alphabet
from regular_languages.RegularExpressions.simplify_regex_ast import simplify_regex_ast

class GNFASpecialStates(Enum):
    '''
    Helper enum to represent special states for GNFAs
    '''

    SOURCE = auto()
    SINK = auto()

T = TypeVar('T')
U = TypeVar('U')

AdjList = Dict[T | Literal[GNFASpecialStates.SOURCE], Dict[T | Literal[GNFASpecialStates.SINK], RegexAST[U]]]

@dataclass
class GNFA(Generic[T, U]):
    states: Set[T | DFASpecialStates]
    alphabet: Set[U]
    adj_list: AdjList

    def __post_init__(self):
        for source_state in self.states.union({GNFASpecialStates.SOURCE}):
            for dest_state in self.states.union({GNFASpecialStates.SINK}):
                try:
                    implied_sub_alphabet = extract_alphabet(self.adj_list[source_state][dest_state])
                except KeyError:
                    raise Exception(f'({source_state}, {dest_state}) is missing from the adjacency list')

                if not implied_sub_alphabet.issubset(self.alphabet):
                    raise Exception('The implied alphabet in an ast is not a subset of the defined alphabet')

    # TODO: should this be a converter? Or is it ok since GNFAs aren't really
    # meant to be an external class?
    @classmethod
    def from_DFA(cls, dfa: DFA[T, U]):
        states = set(dfa.states)
        alphabet = set(dfa.alphabet)
        adj_list: AdjList = defaultdict(lambda: defaultdict(EmptyLangNode))

        # Add the connection from the new source to the start state
        adj_list[GNFASpecialStates.SOURCE][dfa.start_state] = EmptyStrNode()

        # Add the connections from the accept states to the new sink state
        for accept_state in dfa.accept_states:
            adj_list[accept_state][GNFASpecialStates.SINK] = EmptyStrNode()

        # Add the rest of the connections as defined by the DFA
        for source_state in dfa.states:
            for symbol in dfa.alphabet:
                dest_state = dfa.transition_function(source_state, symbol)

                match adj_list[source_state][dest_state]:
                    case EmptyLangNode():
                        adj_list[source_state][dest_state] = SymbolNode(symbol)

                    case node:
                        adj_list[source_state][dest_state] = UnionNode(node, SymbolNode(symbol))

        return cls(states, alphabet, adj_list)

    def to_regexAST(self, simplify: Callable[[RegexAST], RegexAST]=simplify_regex_ast):
        orig_states = set(self.states)

        for state in orig_states:
            self.rip_state(state, simplify)

        final_ast = self.adj_list[GNFASpecialStates.SOURCE][GNFASpecialStates.SINK]

        return simplify(final_ast)

    def rip_state(self, rip_state: T | DFASpecialStates, simplify):
        # Update the adj list to account for the state being removed
        for source_state in self.states.union({GNFASpecialStates.SOURCE}).difference({rip_state}):
            for dest_state in self.states.union({GNFASpecialStates.SINK}).difference({rip_state}):
                orig_ast = self.adj_list[source_state][dest_state]
                r1 = self.adj_list[source_state][rip_state]
                r2 = self.adj_list[rip_state][rip_state]
                r3 = self.adj_list[rip_state][dest_state]

                new_ast = UnionNode(orig_ast, ConcatNode(ConcatNode(r1, ClosureNode(r2)), r3))
                self.adj_list[source_state][dest_state] = new_ast

        # Remove the state from the list of states
        self.states.remove(rip_state)

        # Remove the state from the adj list
        del self.adj_list[rip_state]
