from token import Token

STRING_ESCAPES = {
    "`": "`",
    "n": "\n",
    "t": "\t",
    "\\": "\\",
    "r": "\r",
    "b": "\b",
    "f": "\f"
}

def lex(code):
    index = 0
    while index < len(code):
        if code[index:index + 3] == "---":
            while index < len(code) and code[index] != "\n":
                index += 1
        elif code[index:index + 3] == "...":
            while index < len(code) and code[index] != "\n":
                index += 1
            index += 1
        elif code[index] == "\n":
            yield Token("linebreak", None, index, index + 1)
            index += 1
        elif code[index].isspace():
            index += 1
        elif code[index] in "0123456789_.":
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
                elif code[index] in "ij" and allow_complex:
                    allow_complex = False
                else:
                    break
                state += code[index]
                index += 1

            yield Token("number", state, start, index)
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
                            if index < len(code) and "0" <= code[index] <= "7":
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
                    start, min(index, len(code))))
        elif "a" <= code[index] <= "z" or "A" <= code[index] <= "Z":
            state = code[index]
            start = index
            index += 1

            while index < len(code) and "a" <= code[index] <= "z" \
                    or "A" <= code[index] <= "Z" or code[index] == "_" \
                    and index + 1 < len(code) and ("a" <= code[index + 1] <= z \
                    or "A" <= code[index + 1] <= "Z"):
                state += code[index]
                index += 1

            yield Token("identifier", state, start, index)
        else:
            yield Token("unknown", code[index], index, index + 1)
            index += 1
