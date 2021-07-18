import sys

from collections import deque

def parse(code, tokens):
    arities = preparse_arities(code, tokens)
    return parse_tokens(tokens, arities)

def preparse_arities(code, tokens):
    arities = {}
    offenders = []

    statement_start = True

    index = 0
    while index < len(tokens):
        if statement_start and index + 1 < len(tokens) \
                and tokens[index].type == "identifier" \
                and tokens[index + 1] == ("primitive", ":="):
            register_arity(arities, tokens[index], 0)
            index += 2
            statement_start = False
        elif statement_start and index + 2 < len(tokens) \
                and tokens[index].type == "primitive" \
                and tokens[index].value in ["#", "@"] \
                and tokens[index + 1].type == "identifier" \
                and tokens[index + 2] == ("primitive", ":="):
            register_arity(arities, tokens[index + 1], \
                    1 if tokens[index].value == "#" else 1)
            index += 3
            statement_start = False
        elif tokens[index] == ("primitive", ":="):
            offenders.append(tokens[index])
            index += 1
            statement_start = False
        elif tokens[index].type == "linebreak" \
                or tokens[index] == ("primitive", "::"):
            index += 1
            statement_start = True
        else:
            index += 1
            statement_start = False

    failed = False

    for key in sorted(arities):
        if sum(map(bool, arities[key])) > 1:
            failed = True
            print(f"Preparser Error: multiple arities detected for `{key}`:", \
                    file = sys.stderr, end = "\n\n")
            for arity, instances in enumerate(arities[key]):
                if instances:
                    print(["Niladic", "Monadic", "Dyadic"][arity] + \
                            " definitions:", file = sys.stderr)
                for token in sorted(instances, \
                        key = lambda token: token.start):
                    print_context(code, token, sys.stderr)
                    print(file = sys.stderr)

    if offenders:
        failed = True
        print("Preparser Error: `:=` found without being part of a valid " \
                "variable declaration:", file = sys.stderr, end = "\n\n")
        for token in offenders:
            print_context(code, token, sys.stderr)
            print(file = sys.stderr)

    if failed:
        raise SystemExit

    result = {}

    for key in arities:
        for arity, instances in enumerate(arities[key]):
            if instances:
                result[key] = arity

    return result

def register_arity(arities, token, arity):
    if token.value not in arities:
        arities[token.value] = [[], [], []]
    arities[token.value][arity].append(token)

def print_context(code, token, file = sys.stdout):
    row = code.split("\n")[token.start[0] - 1]
    left = min(10, token.start[1])
    context = row[token.start[1] - left:token.end[1] + 10]
    print(f"    Line {token.start[0]} Column {token.start[1]}")
    print("    " + context, file = file)
    print(" " * (3 + left) + "^" * (token.end[1] - token.start[1]), file = file)

def parse_tokens(tokens, arities):
    return divide_statements(tokens)

def divide_statements(tokens):
    statements = []
    for token in tokens:
        if statements == []:
            statements = [[]]
        if token.type == "linebreak" or token == ("primitive", "::"):
            statements.append([])
        else:
            statements[-1].append(token)
    return statements
