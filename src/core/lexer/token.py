class Token:
    def __init__(self, tokentype, value, start, end):
        self.type = tokentype
        self.value = value
        self.start = start
        self.end = end
