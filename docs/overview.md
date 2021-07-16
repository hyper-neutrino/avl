# overview

The first stage of each program is lexing or tokenizing, The lexer is responsible for taking a list of characters and producing a list of tokens. It should ideally be a generator.

The second stage is parsing. The parser is responsible for taking a line of list of tokens and producing a parse tree.

The third stage is translation. The translator is responsible for taking a parse tree and producing a single Python file that does the same thing.
