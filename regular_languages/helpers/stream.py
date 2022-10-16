from dataclasses import dataclass
from typing import Generic, Iterable, List, TypeVar

U = TypeVar('U')

@dataclass
class Stream(Generic[U]):
    '''
    A data structure that represents a consumable stream of some objects
    '''

    data: List[U]
    index: int

    @classmethod
    def from_iterable(cls, data: Iterable[U]):
        return cls(list(data), 0)

    def peek(self, offset: int = 0) -> U:
        '''
        Peek at a token in the stream with the given offset
        '''

        effective_index = self.index + offset

        if not 0 <= effective_index < len(self.data):
            raise Exception('Stream access out of bounds')

        return self.data[effective_index]

    def consume(self, number: int = 1) -> U:
        '''
        Consumes the given number of tokens, returning the last token consumed
        '''

        effective_index = self.index + number

        if number <= 0:
            raise Exception('Must consume 1 or more tokens')

        # We can consume all tokens, make effective index the length
        if effective_index > len(self.data):
            raise Exception('Too many tokens consumed')

        data = self.data[effective_index - 1]
        self.index = effective_index

        return data

    def is_empty(self) -> bool:
        return self.index >= len(self.data)
