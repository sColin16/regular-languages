from dataclasses import dataclass
from .regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, RegexAST, SymbolNode, UnionNode

# TODO: this file could probably use updates once I understand CFLs and yields better

@dataclass
class PrinterConfig():
    '''
    Defines how a regular expression is converted to a string. Basically the
    inverse of the LexerConfig
    '''

    union_symbol: str
    closure_symbol: str
    lparen_symbol: str
    rparen_symbol: str
    empty_str_symbol: str
    empty_lang_symbol: str

DEFAULT_PRINTER_CONFIG = PrinterConfig(
    union_symbol="|",
    closure_symbol="*",
    lparen_symbol="(",
    rparen_symbol=")",
    empty_str_symbol="\e",
    empty_lang_symbol="\o"
)

# TODO: avoid adding parnatheses to this string where possible
def regex_ast_to_string(ast: RegexAST, config=DEFAULT_PRINTER_CONFIG) -> str:
    match ast:
        case EmptyLangNode():
            return f'{config.empty_lang_symbol}'

        case EmptyStrNode():
            return f'{config.empty_str_symbol}'

        case SymbolNode(symbol):
            return f'{symbol}'

        case UnionNode(left, right):
            left_str = regex_ast_to_string(left)
            right_str = regex_ast_to_string(right)

            return f'{config.lparen_symbol}{left_str}{config.union_symbol}{right_str}{config.rparen_symbol}'

        case ConcatNode(left, right):
            left_str = regex_ast_to_string(left)
            right_str = regex_ast_to_string(right)

            return f'{config.lparen_symbol}{left_str}{right_str}{config.rparen_symbol}'

        case ClosureNode(child):
            child_str = regex_ast_to_string(child)

            return f'{child_str}{config.closure_symbol}'
