def is_identifier(char):
    return not (" " <= char <= "@" or "[" <= char <= "`" or "{" <= char <= "~")

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
