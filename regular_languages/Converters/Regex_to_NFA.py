from regular_languages import Regex
from regular_languages import NFA

def Regex_to_NFA(regex: Regex) -> NFA:
    '''
    Constructs an NFA the recognizes the same langauge as the provided regex
    '''

    # THis may be possible to do recursively here, or might require a
    # recursive helper function to more efficiently build the transition
    # map (at least to build starting at a certain numeric id)

    raise NotImplementedError
