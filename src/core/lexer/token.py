class Token:
    def __init__(self, tokentype, value, start, end):
        self.type = tokentype
        self.value = value
        self.start = start
        self.end = end
    def __str__(self):
        return f"<'{self.type}' token, ({self.start}, {self.end}): {self.value}>"
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        elif isinstance(other, tuple):
            if len(other) == 2:
                tokentype, value = other
                return self.type == tokentype and self.value == value
            else:
                return False
        else:
            return self.value == other
