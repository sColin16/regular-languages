from regular_languages import Regex, NFA
from regular_languages.NFAs.generated_states import BasisState, InternalState
from regular_languages.NFAs.nfa import SpecialSymbols
from regular_languages.RegularExpressions.regex_ast import ClosureNode

def closure_regex(regex: Regex):
    return Regex(set(regex.alphabet), ClosureNode(regex.ast))

def closure_nfa(nfa: NFA):
    states = {BasisState.START}.union({InternalState(state) for state in nfa.states})
    alphabet = set(nfa.alphabet)

    def transition_function(state, symbol):
        match state:
            case InternalState(child) if child not in nfa.accept_states:
                return InternalState.wrap(nfa.transition_function(child, symbol))

            case InternalState(child) if child in nfa.accept_states and symbol is not SpecialSymbols.EMPTY:
                return InternalState.wrap(nfa.transition_function(child, symbol))

            case InternalState(child) if child in nfa.accept_states and symbol is SpecialSymbols.EMPTY:
                return InternalState.wrap(nfa.transition_function(child, symbol).union({nfa.start_state}))

            case BasisState.START if symbol is SpecialSymbols.EMPTY:
                return {InternalState(nfa.start_state)}

            case _:
                return set()

    start_state = BasisState.START
    accept_states = {BasisState.START}.union({InternalState(state) for state in nfa.accept_states})

    return NFA.from_unsafe_transition_func(states, alphabet, transition_function, start_state, accept_states)
