from regular_languages import DFA
from regular_languages import NFA

def NFA_to_DFA(nfa: NFA) -> DFA:
    '''
    Converts an NFA to a DFA that recognizes the same language
    '''

    # Use subset construction to do this, possibly creating an intermediate
    # NFA that removes the epsilon transitions

    raise NotImplementedError
