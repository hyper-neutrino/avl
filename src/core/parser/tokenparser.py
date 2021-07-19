def divide_statements(tokens):
    statements = []
    block = []
    bal = 0
    arity = None
    for token in tokens:
        if statements == []:
            statements.append([])
        if bal:
            if bracket_arity(token) == arity:
                bal += bracket_class(token)
            if bal == 0:
                statements[-1].append(divide_statements(block))
                statements[-1].append(token)
                block = []
                arity = None
            else:
                block.append(token)
        else:
            if bracket_class(token) == -1:
                this_block = statements.pop()
                sublist = divide_statements(this_block)
                statements.append([sublist])
                statements[-1].append(token)
            elif token == ("primitive", "::"):
                statements.append([])
            else:
                bal += bracket_class(token)
                arity = bracket_arity(token)
                statements[-1].append(token)
    if block:
        statements[-1].append(divide_statements(block))
    return statements

def bracket_class(token):
    if token.type != "primitive":
        return 0
    if token.value in ["[", "(", "{"]:
        return 1
    if token.value in ["]", ")", "}"]:
        return -1
    if len(token.value) == 2 and token.value[0] in ["[", "(", "{"]:
        return 1
    return 0

def bracket_arity(token):
    if token.type != "primitive":
        return
    if "[" in token.value or "]" in token.value:
        return 0
    if "(" in token.value or ")" in token.value:
        return 1
    if "{" in token.value or "}" in token.value:
        return 2
