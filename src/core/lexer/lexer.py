from .token import Token
from .symbols import is_identifier, PRIMITIVES

STRING_ESCAPES = {
    "`": "`",
    "n": "\n",
    "t": "\t",
    "\\": "\\",
    "r": "\r",
    "b": "\b",
    "f": "\f"
}

def compute_positions(code):
    row = 1
    col = 1
    positions = [0] * len(code)
    for index, char in enumerate(code):
        positions[index] = (row, col)
        if char == "\n":
            row += 1
            col = 1
        else:
            col += 1
    positions.append((row, col))
    return positions

def lex(code):
    index = 0
    positions = compute_positions(code)
    while index < len(code):
        if code[index:index + 3] == "---":
            while index < len(code) and code[index] != "\n":
                index += 1
        elif code[index:index + 3] == "...":
            while index < len(code) and code[index] != "\n":
                index += 1
            index += 1
        elif code[index] == "\n":
            yield Token("linebreak", None, \
                    positions[index], positions[index + 1])
            index += 1
        elif code[index].isspace():
            index += 1
        else:
            for primitive in PRIMITIVES:
                if code[index:].startswith(primitive):
                    yield Token("primitive", primitive, \
                            positions[index], positions[index + len(primitive)])
                    index += len(primitive)
                    break
            else:
                if code[index] in "0123456789_.":
                    allow_negative = False
                    allow_decimal = code[index] != "."
                    allow_base = True
                    allow_complex = True

                    state = code[index]
                    start = index
                    index += 1

                    while index < len(code):
                        if code[index].isdigit():
                            pass
                        elif code[index] == "_" and allow_negative:
                            allow_negative = False
                        elif code[index] == "." and allow_decimal:
                            allow_decimal = False
                        elif code[index] in "eboxEBOX" and allow_base:
                            allow_base = False
                            allow_decimal = True
                        elif code[index] in "ij" and allow_complex:
                            allow_complex = False
                            allow_negative = True
                            allow_decimal = True
                            allow_base = True
                        else:
                            break
                        state += code[index]
                        index += 1

                    yield Token("number", state, \
                            positions[start], positions[index])
                elif index + 1 < len(code) and code[index + 1] == "`" \
                        and code[index] in "bcl" \
                        or code[index] == "`":
                    state = ""
                    postprocess = code[index]
                    start = index
                    index += 1 + (code[index] != "`")

                    while index < len(code):
                        if code[index] == "\\":
                            index += 1
                            if index >= len(code):
                                state += "\\"
                                break
                            elif code[index] in STRING_ESCAPES:
                                state += STRING_ESCAPES[code[index]]
                            elif code[index] == "x":
                                index += 1
                                state += chr(int(code[index:index + 2], 16))
                                index += 2
                            elif code[index] == "u":
                                index += 1
                                state += chr(int(code[index:index + 4], 16))
                                index += 4
                            elif "0" <= code[index] <= "7":
                                octal = code[index]
                                for _ in range(2):
                                    index += 1
                                    if index < len(code) \
                                            and "0" <= code[index] <= "7":
                                        octal += code[index]
                                index += 1
                                state += chr(int(octal, 8))
                            else:
                                state += "\\"
                                state += code[index]
                        elif code[index] == "`":
                            index += 1
                            break
                        else:
                            state += code[index]
                        index += 1

                    yield Token("string", (postprocess, state), \
                            positions[start], positions[min(index, len(code))])
                elif is_identifier(code[index]):
                    state = code[index]
                    start = index
                    index += 1

                    while index < len(code) and (is_identifier(code[index]) \
                            or code[index].isdigit() \
                            or code[index] == "_" and index + 1 < len(code) \
                            and is_identifier(code[index + 1])):
                        state += code[index]
                        index += 1

                    yield Token("identifier", state, \
                            positions[start], positions[index])
                else:
                    printf("Tokenization Error: unrecognized symbol: " \
                            + code[index], file = sys.stderr)
                    exit(1)
