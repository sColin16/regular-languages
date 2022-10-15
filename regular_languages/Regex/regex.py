from dataclasses import dataclass
from typing import Generic, Set, TypeVar

from .regex_ast import RegexAST

# TODO: can we somehow include convenience operators like question mark, dot,
# min/max/exact count, etc? Or would that make some of the normal form stuff
# more complicated?

U = TypeVar('U')

@dataclass
class Regex(Generic[U]):
    '''
    Represents a regular expression over an arbitrary alphabet
    '''

    alphabet: Set[U]
    ast: RegexAST[U]

    def __post_init__(self):
        # TODO: verify that the symbols in the ast are a subset of the alphabet
        # We should have pattern matching, so this should be easier!
        pass

    @classmethod
    def from_string(cls, regular_expression: str, alphabet: Set[U] | None = None):
        '''
        Compiles the given regular expression into an internal representation
        '''

        # TODO: automatically detect the alphabet if None is passed

        # TODO: I think we should call a compile function externally
        # Also, this is probably going to limit us to a character-based alphabet
        # which is fine. If you build your own AST with other symbols all this
        # should work
        pass


    def as_string(self) -> str:
        '''
        Converts the internal representation of the regex to a string (which
        could be used to construct a regex
        '''

        # TODO: consider how much flexibility I want to build into letting
        # arbitrary symbols stand for different elements of the parse tree. A
        # legitimate one is + vs | for union
        # TODO: probably just place parantheses around everything at first,
        # later I can look back at returning a regex that omits parantheses
        # where possible

        pass

    def as_DNF(self):
        '''
        Returns a new DNF that places the regex in disjunctive normal form: the
        union of regular expressions consisting only of concatenation and
        closures (and perhaps other operators like the question mark if I add them)
        '''

        # TODO: consider putting this in an operators file
        # I suppose that DFA minimize should possibly also be in there too
        # This should be possible to perform this recursively, bubbling up the
        # union operators to the top of the tree
        # The difficult part is handling the fact that the union operation is
        # binary, but DNF could be the union of an abritrary number of pieces.
        # Is that easy to handle?

        pass
