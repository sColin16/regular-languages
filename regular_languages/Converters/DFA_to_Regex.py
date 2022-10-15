from regular_languages import DFA
from regular_languages import Regex

def DFA_to_Regex(dfa: DFA) -> Regex:
    '''
    Constructs a regular expression that matches the same language as the
    given DFA
    '''

    # TODO: consider passing a callback that can be used to simplify the
    # regex at each step, or at the very end, following regex algebra
    # I think we should just call the GNFA support function:
    # gnfa = GNFA.from_DFA(dfa)
    # return gnfa.as_regex_ast() <- This rips itself to 2-states, then extracts the AST