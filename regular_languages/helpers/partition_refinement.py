from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Generic, List, Set, TypeVar

U = TypeVar('U')

@dataclass
class PartitionRefinement(Generic[U]):
    '''
    Implementation of the partition refinement data structure, effectively the
    inverse of the union find data structure.

    Implementation is based loosely on:
    https://www.ics.uci.edu/~eppstein/PADS/PartitionRefinement.py
    '''

    # Maps from partition id to the set of elements in the partitiono
    sets: List[Set[U]]

    # Maps from an element to to the partition id of the element
    partitions: Dict[U, int]

    def __post_init__(self):
        '''
        Verifies the integrity of the data structure
        '''

        # TODO: consider implementing this
        pass

    @classmethod
    def from_set(cls, s: Set[U]):
        '''
        Constructs a new partition refinement instance with a single partition
        '''

        sets = [s]
        partitions = {x: 0 for x in s}

        return cls(sets, partitions)

    def refine(self, s: Set[U]):
        '''
        Performs the refinement operation, splitting elements in the input set
        and all elements not in the input set into separate partitions
        '''

        split_sets = defaultdict(set)

        # Iterate over all elements in refinement set and create the split sets
        # for each partition
        for x in s:
            partition = self.partitions[x]
            split_sets[partition].add(x)

        out = []
        for partition, split_set in split_sets.items():
            # Skip if set difference is the empty set
            # Note that skip for set intersection being empty is implicit since
            # it will not appear in the split_sets dictionary
            if len(self.sets[partition]) != len(split_set):
                for x in split_set:
                    # Assign the element to a new partition
                    self.partitions[x] = len(self.sets)

                    # Remove the element from the original set
                    self.sets[partition].remove(x)

                self.sets.append(split_set)
                out.append((split_set, self.sets[partition]))

        return out

    def freeze(self):
        '''
        Converts all the sets to frozen sets
        '''

        self.sets = [frozenset(x) for x in self.sets]

    def get_partition(self, item: U):
        '''
        Retrieves the partition that the item is contained in
        '''

        if item not in self.partitions:
            raise Exception('Item is not in the partitions')

        return self.sets[self.partitions[item]]
