from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Sequence, Set, TypeVar

U = TypeVar('U')

@dataclass
class ConcatNode:
    left: RegexAST
    right: RegexAST

@dataclass
class UnionNode:
    left: RegexAST
    right: RegexAST

@dataclass
class ClosureNode:
    child: RegexAST

@dataclass
class EmptyStrNode:
    pass

@dataclass
class EmptyLangNode:
    pass

@dataclass
class SymbolNode(Generic[U]):
    symbol: U

RegexAST = ConcatNode | UnionNode | ClosureNode | SymbolNode[U] | EmptyStrNode | EmptyLangNode
