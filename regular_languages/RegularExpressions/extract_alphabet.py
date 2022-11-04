
from typing import Set, TypeVar
from regular_languages.RegularExpressions.regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, RegexAST, SymbolNode, UnionNode

U = TypeVar('U')

def extract_alphabet(regex_ast: RegexAST[U]) -> Set:
    '''
    Extracts the alphabet implied by a regular expression ast
    '''

    match regex_ast:
        case UnionNode(left, right) | ConcatNode(left, right):
            return extract_alphabet(left).union(extract_alphabet(right))

        case ClosureNode(child):
            return extract_alphabet(child)

        case SymbolNode(symbol):
            return {symbol}

        case EmptyStrNode() | EmptyLangNode():
            return set()
