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

def extract_alphabet(regex_ast: RegexAST[U]) -> Set:
    match regex_ast:
        case UnionNode(left, right) | ConcatNode(left, right):
            return extract_alphabet(left).union(extract_alphabet(right))

        case ClosureNode(child):
            return extract_alphabet(child)

        case SymbolNode(symbol):
            return {symbol}

        case EmptyStrNode() | EmptyLangNode():
            return set()
