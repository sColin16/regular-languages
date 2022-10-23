from dataclasses import dataclass
from typing import Callable, Generic, Optional, Set, TypeVar

from regular_languages.RegularExpressions.regex_compiler import compile_regular_expression
from regular_languages.RegularExpressions.simplify_regex_ast import simplify_regex_ast

from .regex_ast import RegexAST, extract_alphabet

# TODO: provide an augmented provider than can compile other operators to the
# operators defined here (question mark, plus, min/max/exact count)
# TODO: consider creating an augmented ast that cnopiles more advanced operators
# to an NFA directly

U = TypeVar('U')

DEFAULT_REGEX_COMPILER = compile_regular_expression

@dataclass
class Regex(Generic[U]):
    '''
    Represents a regular expression over an arbitrary alphabet
    '''

    alphabet: Set[U]
    ast: RegexAST[U]

    def __post_init__(self):
        implicit_alphabet = extract_alphabet(self.ast)

        if not implicit_alphabet.issubset(self.alphabet):
            raise Exception('The defined alphabet for the regex is not a ' +
                            'subset of the alphabet implied by the regex')

    @classmethod
    def from_string(cls, regular_expression: str, alphabet: Optional[Set[U]] = None,
                    compiler: Callable[[str], RegexAST] = DEFAULT_REGEX_COMPILER):
        '''
        Compiles the given regular expression into an internal representation
        '''

        ast = compiler(regular_expression)
        implicit_alphabet = extract_alphabet(ast)

        final_alphabet = implicit_alphabet if alphabet is None else alphabet

        return cls(final_alphabet, ast)

    def simplified(self):
        '''
        Converts the regex to an equivalent regex, with a possibly more compact representation
        '''

        simplified_ast = simplify_regex_ast(self.ast)

        return Regex(self.alphabet, simplified_ast)

    def to_string(self) -> str:
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

    def to_DNF(self):
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
