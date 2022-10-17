from typing import List, TypeVar, get_args
from regular_languages.RegularExpressions.regex_tokens import ClosureToken, EmptyLangToken, EmptyStrToken, LParenToken, RParenToken, RegexToken, SymbolToken, UnionToken
from regular_languages.RegularExpressions.regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, RegexAST, SymbolNode, UnionNode
from regular_languages.helpers import Stream

U = TypeVar('U')

# TODO: split this up, and consider if there are better ways to resolve
# ambiguiity, because this function is a mess

def parse_regular_expression(token_stream: Stream[RegexToken[U]]) -> RegexAST[U]:
    '''
    Uses shift-reduce parsing to parse a regex token stream

    Check out the sweet pattern matching here!
    '''

    print(token_stream)

    stack: List[RegexAST[U] | RegexToken[U]] = []

    # Continue pushing or reducing until there is one node in the stack, and no
    # tokens in the stream
    while not token_stream.is_empty() or len(stack) > 1:
        # NOTE: I am kinda unhappy with needing to union six different literal
        # objects here, but I don't believe I can use the type alias for the
        # union type, or create any sort of alias for the union
        match stack:
            # Always reduce paranthesized expressions first
            case [
                *rest,
                LParenToken(),
                ClosureNode() | ConcatNode() | EmptyLangNode() | EmptyStrNode() | SymbolNode() | UnionNode() as enclosed,
                RParenToken()
            ]:
                for _ in range(3): stack.pop()
                stack.append(enclosed)

            # Closure has highest precedence, so reduce that next
            case [
                *rest,
                ClosureNode() | ConcatNode() | EmptyLangNode() | EmptyStrNode() | SymbolNode() | UnionNode() as child,
                ClosureToken()
            ]:
                for _ in range(2): stack.pop()
                stack.append(ClosureNode(child))

            # Reduce concatenation if next token in stream is not a closure token
            case [
                *rest,
                ClosureNode() | ConcatNode() | EmptyLangNode() | EmptyStrNode() | SymbolNode() | UnionNode() as left,
                ClosureNode() | ConcatNode() | EmptyLangNode() | EmptyStrNode() | SymbolNode() | UnionNode() as right
            ] if not isinstance(token_stream.peek(), ClosureToken):
                for _ in range(2): stack.pop()
                stack.append(ConcatNode(left, right))

            # Reduce union if next token would not cause a closure or concat
            # reduction
            case [
                *rest,
                ClosureNode() | ConcatNode() | EmptyLangNode() | EmptyStrNode() | SymbolNode() | UnionNode() as left,
                UnionToken(),
                ClosureNode() | ConcatNode() | EmptyLangNode() | EmptyStrNode() | SymbolNode() | UnionNode() as right
            ] if not isinstance(token_stream.peek(), ClosureToken) and\
                    not isinstance(token_stream.peek(), SymbolToken):
                for _ in range(3): stack.pop()
                stack.append(UnionNode(left, right))

            # Perform a shift if none of these patterns matched
            case _ if not token_stream.is_empty():
                next_token = token_stream.consume()

                match next_token:
                    case SymbolToken(symbol):
                        stack.append(SymbolNode(symbol))

                    case EmptyStrToken():
                        stack.append(EmptyStrNode())

                    case EmptyLangToken():
                        stack.append(EmptyLangNode())

                    case token:
                        stack.append(token)

            case _:
                raise Exception('Invalid syntax')

    match stack[0]:
        case ClosureNode() | ConcatNode() | EmptyLangNode() | EmptyStrNode() | SymbolNode() | UnionNode():
            return stack[0]

        case _:
            raise Exception('Invalid syntax')
