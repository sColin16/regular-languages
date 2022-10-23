from .regex_ast import ClosureNode, ConcatNode, EmptyLangNode, EmptyStrNode, RegexAST, SymbolNode, UnionNode

def regex_ast_to_DNF(ast: RegexAST):
    '''
    Places a regular expression in disjunctive normal form: the union of
    collection of concatenations and closures
    '''

    match ast:
        # Base case: basis nodes of a regex are in DNF
        case SymbolNode(_) | EmptyLangNode() | EmptyStrNode() as node:
            return node

        # Simple case: union of expressions in DNF is still in DNF
        case UnionNode(left, right):
            left_in_DNF = regex_ast_to_DNF(left)
            right_in_DNF = regex_ast_to_DNF(right)

            return UnionNode(left_in_DNF, right_in_DNF)

        # Closure case: apply algebraic rule: (a|b)* == (a*b*)*
        case ClosureNode(child):
            child_in_DNF = regex_ast_to_DNF(child)

            match ClosureNode(child_in_DNF):
                case ClosureNode(UnionNode(a, b)):
                    return ClosureNode(ConcatNode(ClosureNode(a), ClosureNode(b)))

            return ClosureNode(child_in_DNF)

        # Concat case: apply distributive law: (a|b)(c|d) == (ac|ad|bc|bd)
        case ConcatNode(left, right):
            left_in_DNF = regex_ast_to_DNF(left)
            right_in_DNF = regex_ast_to_DNF(right)

            match ConcatNode(left_in_DNF, right_in_DNF):
                case ConcatNode(UnionNode(a, b), UnionNode(c, d)):
                    return UnionNode(UnionNode(ConcatNode(a, c), ConcatNode(a, d)), UnionNode(ConcatNode(b, c), ConcatNode(b, d)))

                case ConcatNode(a, UnionNode(b, c)):
                    return UnionNode(ConcatNode(a, b), UnionNode(a, c))

                case ConcatNode(UnionNode(a, b), c):
                    return UnionNode(ConcatNode(a, c), UnionNode(b, c))

            return ConcatNode(left_in_DNF, right_in_DNF)
