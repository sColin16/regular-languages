from dataclasses import dataclass
from typing import Dict, List, Optional, Generic, Sequence, Set, Type, TypeVar

from regular_languages.helpers.stream import Stream
from .regex_tokens import ClosureToken, EmptyLangToken, EmptyStrToken, LParenToken, RParenToken, RegexToken, SymbolToken, UnionToken, UnitRegexToken

U = TypeVar('U')

@dataclass
class LexerConfig(Generic[U]):
    '''
    Defines how the lexer converts symbols to tokens. This is the lexical
    grammar, but defined without regular expressions. Note that ambiguous
    configurations should be avoided, and have undefined behavior
    '''

    alphabet: Set[Sequence[U]]
    union_symbol: Sequence[U]
    closure_symbol: Sequence[U]
    lparen_symbol: Sequence[U]
    rparen_symbol: Sequence[U]
    empty_str_symbol: Sequence[U]
    empty_lang_symbol: Sequence[U]

ALPHANUMERIC = "abcdefghijklmnopqrstuvwxyzABCEDFGHIJKLMNOPQRSTUVWXYZ0123456789"
DEFAULT_LEXER_CONFIG: LexerConfig[str] = LexerConfig(
    alphabet=set(ALPHANUMERIC),
    union_symbol="|",
    closure_symbol="*",
    lparen_symbol="(",
    rparen_symbol=")",
    empty_str_symbol="\e",
    empty_lang_symbol="\o"
)

def lex_regular_expression_generic(regular_expression: Sequence[U],
        config: LexerConfig[U]) -> Stream[RegexToken]:
    '''
    Converts a regular expression defined as a list of arbitrary sequences of
    symbols, into a stream of tokens to be processed by a parser.
    '''

    token_symbol_map: Dict[Type[UnitRegexToken], Sequence[U]] = {
        UnionToken: config.union_symbol,
        ClosureToken: config.closure_symbol,
        LParenToken: config.lparen_symbol,
        RParenToken: config.rparen_symbol,
        EmptyStrToken: config.empty_str_symbol,
        EmptyLangToken: config.empty_lang_symbol
    }
    index = 0
    tokens: List[RegexToken[U]] = []

    while index < len(regular_expression):
        alpha_match = False
        for symbol in config.alphabet:
            if regular_expression[index:index+len(symbol)] == symbol:
                tokens.append(SymbolToken(symbol))
                index += len(symbol)
                alpha_match = True
                break

        if alpha_match:
            continue

        for token, symbol in token_symbol_map.items():
            if regular_expression[index:index + len(symbol)] == symbol:
                tokens.append(token())
                index += len(symbol)
                break

    return Stream.from_iterable(tokens)
