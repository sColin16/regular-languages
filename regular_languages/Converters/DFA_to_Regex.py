from typing import TypeVar
from regular_languages import DFA
from regular_languages import Regex
from regular_languages.GNFAs.gnfa import GNFA

T = TypeVar('T')
U = TypeVar('U')

def DFA_to_Regex(dfa: DFA[T, U]) -> Regex[U]:
    '''
    Constructs a regular expression that matches the same language as the
    given DFA
    '''

    # TODO: consider passing a callback that can be used to simplify the
    # regex at each step, or at the very end, following regex algebra
    # I think we should just call the GNFA support function:

    gnfa = GNFA.from_DFA(dfa)
    regex_ast = gnfa.to_regexAST()

    return Regex(dfa.alphabet, regex_ast)
