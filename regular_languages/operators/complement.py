from regular_languages import DFA

def complement_dfa(dfa: DFA):
    '''
    Constructs a DFA that recognizes the complement of the language recognized
    by the original DFA
    '''

    # Just invert the accept states!
    return DFA(set(dfa.states), set(dfa.alphabet), dfa.transition_function, dfa.start_state, dfa.states.difference(dfa.accept_states))
