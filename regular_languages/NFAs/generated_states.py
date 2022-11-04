from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Set

class BasisState(Enum):
    START = auto()
    ACCEPT = auto()

@dataclass(eq=True, frozen=True)
class InternalState:
    child: GeneratedNFAState

    @staticmethod
    def wrap(states: Set):
        return {InternalState(state) for state in states}

@dataclass(eq=True, frozen=True)
class LeftInternalState:
    child: GeneratedNFAState

    @staticmethod
    def wrap(states: Set):
        return {LeftInternalState(state) for state in states}

@dataclass(eq=True, frozen=True)
class RightInternalState:
    child: GeneratedNFAState

    @staticmethod
    def wrap(states: Set):
        return {RightInternalState(state) for state in states}

GeneratedNFAState = BasisState | InternalState | LeftInternalState | RightInternalState
