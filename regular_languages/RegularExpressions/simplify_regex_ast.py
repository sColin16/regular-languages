from .regex_ast import RegexAST
from regular_languages.RegularExpressions.regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, SymbolNode, UnionNode

def simplify_regex_ast(ast: RegexAST):
    '''
    Simplifies a regex ast using the algebraic properties of ASTs
    Useful for simplifying an AST generated using a GNFA
    '''

    match ast:
        # Base case: the basis elements of an AST cannot be simplified
        case SymbolNode(_) | EmptyLangNode() | EmptyStrNode() as node:
            return node

        # Recursive cases: simplify the children then detect any patterns
        # This strategy makes simplification linear w/r/t the nodes in the AST
        case ClosureNode(child):
            simplified_child = simplify_regex_ast(child)

            # Match high-level patterns for the closure node
            match ClosureNode(simplified_child):
                # Closure of the empty language is the empty string
                case ClosureNode(EmptyLangNode()):
                    return EmptyStrNode()

                # Closure of the empty string is the empty string
                case ClosureNode(EmptyStrNode()):
                    return EmptyStrNode()

                # Closure of a closure eliminates the redundant closure
                case ClosureNode(ClosureNode(a)):
                    return ClosureNode(a)

                # No simplification identified
                case node:
                    return node

        case UnionNode(left, right):
            left_simplified = simplify_regex_ast(left)
            right_simplified = simplify_regex_ast(right)

            # Match high-level patterns for union nodes
            match UnionNode(left_simplified, right_simplified):
                # Idempotent law
                case UnionNode(left, right) if left == right:
                    return left

                # TODO: generalized idempotent law (e.g. \e|1*) Can we detect this generally in an easy way?
                # (e.g. ((1|2)*)|((12)*) is harder to detect)

                # Union of a language with the empty language is that language
                case UnionNode(EmptyLangNode(), a) | UnionNode(a, EmptyLangNode()):
                    return a

                # Union of the empty string with aa* is a*
                case UnionNode(EmptyStrNode(), ConcatNode(a, ClosureNode(b)))\
                        | UnionNode(EmptyStrNode(), ConcatNode(ClosureNode(a), b))\
                        | UnionNode(ConcatNode(a, ClosureNode(b)), EmptyStrNode())\
                        | UnionNode(ConcatNode(ClosureNode(a), b), EmptyStrNode())\
                        if a == b:
                    return ClosureNode(a)

                # No simplifications identified
                case node:
                    return node

        case ConcatNode(left, right):
            left_simplified = simplify_regex_ast(left)
            right_simplified = simplify_regex_ast(right)

            match ConcatNode(left_simplified, right_simplified):
                # Concat with empty string eliminates the empty string
                case ConcatNode(EmptyStrNode(), a) | ConcatNode(a, EmptyStrNode()):
                    return a

                # Concat anything with the empty language is the empty language
                case ConcatNode(EmptyLangNode(), a) | ConcatNode(a, EmptyLangNode()):
                    return EmptyLangNode()


                # Concatenation of identical closures is redundant
                case ConcatNode(ClosureNode(a), ClosureNode(b)) if a == b:
                    return ConcatNode(ClosureNode(a))

                # No simplifications identified
                case node:
                    return node
