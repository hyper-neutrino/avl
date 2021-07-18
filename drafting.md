# drafting

- if statements: `[? statement]`, `[? condition :: statement]`,  `[? condition :: if :: else]`
- while statements:  `[! statement]`, `[! condition :: statement]`, `[! condition :: statement :: if-not-broken]`
- for-each statements: `[: statement]`, `[: variable :: statement]`, `[: variable :: statement :: if-not-broken]`
- switch statements: `[| niladic :: statement :: niladic :| niladic :: statement :: else-if-odd-statement-count]`
- match statements: `[# variadic :: statement :: variadic :| variadic :: statement :: else-if-idd-statement-count]`
- niladic blocks: `[ ... ]`
- monadic blocks: `( ... )`
- dyadic blocks: `{ ... }`

- statement separator: `::` or `\n`

- assignment: start a statement with `variable := statement` (niladic), `#variable := statement` (monadic), `@variable := statement` (dyadic)
  - the same variable cannot be assigned to different arities throughout the entire program
  - `:=` is invalid elsewhere to avoid confusion

- reference: just put the variable name; its arity is determinable at compile-time
