from regular_languages import Regex, NFA
from regular_languages.NFAs.generated_states import LeftInternalState, RightInternalState
from regular_languages.NFAs.nfa import SpecialSymbols
from regular_languages.RegularExpressions.regex_ast import ConcatNode

def concat_regex(regex1: Regex, regex2: Regex):
    new_alphabet = regex1.alphabet.union(regex2.alphabet)
    new_ast = ConcatNode(regex1.ast, regex2.ast)

    return Regex(new_alphabet, new_ast)

def concat_nfa(nfa1: NFA, nfa2: NFA):
    states = LeftInternalState.wrap(nfa1.states).union(RightInternalState.wrap(nfa2.states))
    alphabet = nfa1.alphabet.union(nfa2.alphabet)

    def transition_function(state, symbol):
        match state:
            # State is a non-accept state in NFA1
            case LeftInternalState(child) if child not in nfa1.accept_states and (symbol in nfa1.alphabet or symbol is SpecialSymbols.EMPTY):
                return LeftInternalState.wrap(nfa1.transition_function(child, symbol))

            # State is in an accept state in NFA1 and the symbol is not the empty string
            # (yes, the check for not being the empty symbol is redundant, but is more clear)
            case LeftInternalState(child) if child in nfa1.accept_states and symbol is not SpecialSymbols.EMPTY and symbol in nfa1.alphabet:
                return LeftInternalState.wrap(nfa1.transition_function(child, symbol))

            # State is an accept state in NFA1 and the symbol is the empty string
            case LeftInternalState(child) if child in nfa1.accept_states and symbol is SpecialSymbols.EMPTY:
                return LeftInternalState.wrap(nfa1.transition_function(child, symbol)).union({RightInternalState(nfa2.start_state)})

            case RightInternalState(child) if symbol in nfa2.alphabet or symbol is SpecialSymbols.EMPTY:
                return RightInternalState.wrap(nfa2.transition_function(child, symbol))

            # Catch cases where the symbol wasn't valid in the alphabet of one of the component NFAs
            case _:
                return set()

    start_state = LeftInternalState(nfa1.start_state)
    accept_states = {RightInternalState(state) for state in nfa2.accept_states}

    return NFA.from_unsafe_transition_func(states, alphabet, transition_function, start_state, accept_states)
