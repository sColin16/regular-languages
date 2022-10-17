from typing import TypeVar

from regular_languages.RegularExpressions.regex_ast import RegexAST
from regular_languages.RegularExpressions.regex_lexer import lex_regular_expression
from regular_languages.RegularExpressions.regex_parser import parse_regular_expression

U = TypeVar('U')

def compile_regular_expression(regular_expression: str) -> RegexAST[str]:
    '''
    Compiles a regular expression defined as a string to an AST for the regex
    '''

    token_stream = lex_regular_expression(regular_expression)
    ast = parse_regular_expression(token_stream)

    return ast
