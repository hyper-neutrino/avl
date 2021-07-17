# lexer

The following characters are _symbols_ and are reserved for primitives and structures: ``!"#$%&'()*+,-/:;<=>?@[\\]^`{|}~``. `_.` are used for numeric literals and thus are excluded from this list.  
The following characters are _digits_ and can be used in identifiers but also serve as numeric literals: `0123456789`.  
Outside of strings, newlines and spaces just separate tokens.  
All other characters (letters, basically) are valid identifiers.
