def is_identifier(char):
    if char in "\r\f\n":
        return False
    if " " <= char <= "@":
        return False
    if "[" <= char <= "`":
        return False
    if "{" <= char <= "~":
        return False
    return True

syms = """!"#$%&'()*+,-/:;<=>?@[\]^`{|}~"""

PRIMITIVES = list(syms)

for char in "?!:|#":
    PRIMITIVES.append("[" + char)
    PRIMITIVES.append("(" + char)
    PRIMITIVES.append("{" + char)

for char in syms + "_.":
    if char not in "[({})]":
        PRIMITIVES.append(":" + char)
        PRIMITIVES.append("$" + char)

PRIMITIVES.append("**")
PRIMITIVES.append("||")
PRIMITIVES.append("&&")
PRIMITIVES.append("..")

PRIMITIVES.sort(key = len, reverse = True)
