from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

U = TypeVar('U')

@dataclass
class SymbolToken(Generic[U]):
    symbol: U

@dataclass
class EmptyStrToken:
    pass

@dataclass
class EmptyLangToken:
    pass

@dataclass
class UnionToken:
    pass

@dataclass
class ClosureToken:
    pass

@dataclass
class LParenToken:
    pass

@dataclass
class RParenToken:
    pass

UnitRegexToken = EmptyStrToken | EmptyLangToken | UnionToken | ClosureToken | LParenToken | RParenToken
RegexToken = SymbolToken[U] | UnitRegexToken
