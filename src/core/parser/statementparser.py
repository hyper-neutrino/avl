from ..lexer import Token

def parse_statements(statements, arities, arity):
    results = []
    for statement in statements:
        results.append(parse_statement(statement, arities, arity))
        if arity == 0:
            arity = 1
    return ("statement-list", results)

def parse_statement(statement, arities, arity):
    results = []
    for section in divide_substatements(statement):
        results.append(parse_line(section, arities, arity))
        if arity == 0:
            arity = 1
    return results

def divide_substatements(statement):
    sections = []
    for component in statement:
        if sections == []:
            sections.append([])
        if isinstance(component, Token) and component.type == "linebreak":
            sections.append([])
        else:
            sections[-1].append(component)
    return sections

def parse_line(statement, arities, arity):
    return statement
