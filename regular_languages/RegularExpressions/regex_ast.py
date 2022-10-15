from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

U = TypeVar('U')

class SymbolNode(Generic[U]):
    symbol: U

class ConcatNode:
    left: RegexAST
    right: RegexAST

class UnionNode:
    left: RegexAST
    right: RegexAST

RegexAST = SymbolNode[U] | ConcatNode | UnionNode
