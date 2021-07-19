import sys

from collections import deque

from .preparser import preparse_arities
from .tokenparser import divide_statements
from .statementparser import parse_statements

def parse(code, tokens, arity):
    arities = preparse_arities(code, tokens)
    statements = divide_statements(tokens)
    parse_tree = parse_statements(statements, arities, arity)
    return parse_tree
