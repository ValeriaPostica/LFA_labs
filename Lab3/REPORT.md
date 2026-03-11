# Laboratory Work Nr. 3
## Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Postica Valeria FAF-243

---

## Overview

This laboratory work focuses on understanding and implementing a lexer (also known as a scanner or tokenizer). A lexer performs lexical analysis, which is the process of converting a sequence of characters into a sequence of tokens. This is typically the first phase of a compiler or interpreter.

## Objectives

1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Theoretical Background

### What is a Lexer?

A **lexer** (lexical analyzer) is a program that takes an input string and breaks it down into meaningful units called **tokens**. Each token represents a category of lexemes (actual text values) in the source code.

### Key Concepts

| Term | Definition |
|------|------------|
| **Lexeme** | The actual character sequence in the source (e.g., `42`, `sin`, `+`) |
| **Token** | A pair of (token-type, lexeme) that categorizes the lexeme |
| **Token Type** | The category a lexeme belongs to (e.g., INTEGER, IDENTIFIER, PLUS) |
| **Pattern** | The rule describing which lexemes belong to a token type |

### Lexer vs. Tokenizer vs. Scanner

These terms are often used interchangeably, but there are subtle differences:

- **Scanner**: Reads characters and groups them into lexemes
- **Tokenizer**: Converts lexemes into tokens
- **Lexer**: Typically combines both functions

In practice, all three terms refer to the same component in a compiler.

### Role in Compilation

```
Source Code → [LEXER] → Tokens → [PARSER] → AST → [Code Generator] → Output
```

The lexer is the first stage that:
1. Removes whitespace and comments
2. Identifies keywords, identifiers, literals, and operators
3. Reports lexical errors (invalid characters)
4. Provides tokens to the parser

## Implementation

### Token Types

My lexer recognizes the following token categories:

#### Literals
```python
INTEGER = auto()    # Integer numbers: 42, 0, -17
FLOAT = auto()      # Floating-point: 3.14, 2.0, 1e-5
```

#### Mathematical Functions
```python
SIN = auto()        # Sine function
COS = auto()        # Cosine function
TAN = auto()        # Tangent function
SQRT = auto()       # Square root
LOG = auto()        # Natural logarithm
EXP = auto()        # Exponential (e^x)
ABS = auto()        # Absolute value
```

#### Operators
```python
# Arithmetic
PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, POWER

# Comparison
(==), (!=), (<), (>), (<=), (>=)

# Logical
AND, OR, NOT
```

#### Keywords
```python
IF, ELSE, WHILE, FOR    # Control flow
PI, E                    # Mathematical constants
```

### Token Class

```python
@dataclass
class Token:
    type: TokenType     # Category of the token
    value: Any          # The actual lexeme value
    line: int           # Line number (1-indexed)
    column: int         # Column number (1-indexed)
```

The `Token` class stores not just the type and value, but also position information for error reporting.

### Lexer Algorithm

The lexer uses a character-by-character scanning approach:

```
Algorithm: Tokenize(source)
Input: source string
Output: list of tokens

1. Initialize position to 0, line to 1, column to 1
2. While not at end of source:
   a. Mark start of current lexeme
   b. Read next character
   c. Match against patterns:
      - If whitespace: skip
      - If newline: create NEWLINE token, increment line
      - If digit: scan_number()
      - If letter/underscore: scan_identifier()
      - If operator character: create operator token
      - If '#': skip_comment()
      - Otherwise: raise LexerError
   d. Add matched token to list
3. Add EOF token
4. Return token list
```

### Number Scanning

Numbers can be integers or floats, with optional scientific notation:

```python
def _scan_number(self) -> None:
    # Consume integer part
    while self._peek().isdigit():
        self._advance()
    
    # Check for decimal point
    is_float = False
    if self._peek() == '.' and self._peek_next().isdigit():
        is_float = True
        self._advance()  # Consume '.'
        while self._peek().isdigit():
            self._advance()
    
    # Check for scientific notation (e.g., 1e10, 2.5e-3)
    if self._peek().lower() == 'e':
        is_float = True
        self._advance()
        if self._peek() in '+-':
            self._advance()
        while self._peek().isdigit():
            self._advance()
```

This allows recognition of:
- Integers: `42`, `0`, `123`
- Floats: `3.14`, `0.5`, `2.0`
- Scientific notation: `1e10`, `2.5e-3`, `6.022e23`

### Identifier and Keyword Scanning

Identifiers start with a letter or underscore, followed by alphanumerics:

```python
def _scan_identifier(self) -> None:
    while self._peek().isalnum() or self._peek() == '_':
        self._advance()
    
    lexeme = self.source[self.start:self.current]
    
    # Check if it's a keyword
    if lexeme.lower() in self.KEYWORDS:
        token_type = self.KEYWORDS[lexeme.lower()]
    else:
        token_type = TokenType.IDENTIFIER
```

Keywords are case-insensitive, so `SIN`, `Sin`, and `sin` all map to `TokenType.SIN`.

### Two-Character Operators

Some operators require looking ahead:

```python
if char == '=':
    if self._match('='):
        # It's '==' (equality)
        self.tokens.append(Token(TokenType.EQ, '==', ...))
    else:
        # It's '=' (assignment)
        self.tokens.append(Token(TokenType.ASSIGN, '=', ...))
```

## Examples and Results

### Example 1: Basic Arithmetic
```
Input: "result = 10 + 20 * 3"

Tokens:
  IDENTIFIER      result      line=1  col=1
  ASSIGN          =           line=1  col=8
  INTEGER         10          line=1  col=10
  PLUS            +           line=1  col=13
  INTEGER         20          line=1  col=15
  MULTIPLY        *           line=1  col=18
  INTEGER         3           line=1  col=20
  EOF                         line=1  col=21
```

### Example 2: Trigonometric Functions
```
Input: "angle = sin(pi / 4) + cos(0)"

Tokens:
  IDENTIFIER      angle       line=1  col=1
  ASSIGN          =           line=1  col=7
  SIN             sin         line=1  col=9
  LPAREN          (           line=1  col=12
  PI              pi          line=1  col=13
  DIVIDE          /           line=1  col=16
  INTEGER         4           line=1  col=18
  RPAREN          )           line=1  col=19
  PLUS            +           line=1  col=21
  COS             cos         line=1  col=23
  LPAREN          (           line=1  col=26
  INTEGER         0           line=1  col=27
  RPAREN          )           line=1  col=28
  EOF                         line=1  col=29
```

### Example 3: Complex Expression
```
Input: "y = sqrt(x^2 + 1) * exp(-x)"

Tokens:
  IDENTIFIER      y           line=1  col=1
  ASSIGN          =           line=1  col=3
  SQRT            sqrt        line=1  col=5
  LPAREN          (           line=1  col=9
  IDENTIFIER      x           line=1  col=10
  POWER           ^           line=1  col=11
  INTEGER         2           line=1  col=12
  PLUS            +           line=1  col=14
  INTEGER         1           line=1  col=16
  RPAREN          )           line=1  col=17
  MULTIPLY        *           line=1  col=19
  EXP             exp         line=1  col=21
  LPAREN          (           line=1  col=24
  MINUS           -           line=1  col=25
  IDENTIFIER      x           line=1  col=26
  RPAREN          )           line=1  col=27
  EOF                         line=1  col=28
```

### Example 4: Scientific Notation
```
Input: "speed_of_light = 2.998e8"

Tokens:
  IDENTIFIER      speed_of_light   line=1  col=1
  ASSIGN          =                line=1  col=16
  FLOAT           299800000.0      line=1  col=18
  EOF                              line=1  col=26
```

### Example 5: Multi-line with Comments
```
Input:
  # Calculate circle area
  radius = 5.0
  area = pi * radius ^ 2

Tokens:
  NEWLINE         \n          line=1
  IDENTIFIER      radius      line=2
  ASSIGN          =           line=2
  FLOAT           5.0         line=2
  NEWLINE         \n          line=2
  IDENTIFIER      area        line=3
  ASSIGN          =           line=3
  PI              pi          line=3
  MULTIPLY        *           line=3
  IDENTIFIER      radius      line=3
  POWER           ^           line=3
  INTEGER         2           line=3
  EOF                         line=3
```

## Error Handling

The lexer raises `LexerError` for invalid input:

```python
class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")
```

Examples of errors:
- `@invalid` → "Unexpected character: '@'" at line 1, column 1
- `$price` → "Unexpected character: '$'" at line 1, column 1
- `1e` → "Invalid number: expected exponent" at line 1, column 3

## Features Summary

| Feature | Supported |
|---------|-----------|
| Integer literals | ✓ |
| Floating-point literals | ✓ |
| Scientific notation | ✓ |
| Arithmetic operators | ✓ (+, -, *, /, %, ^) |
| Comparison operators | ✓ (==, !=, <, >, <=, >=) |
| Logical operators | ✓ (and, or, not, &&, \|\|) |
| Trigonometric functions | ✓ (sin, cos, tan) |
| Math functions | ✓ (sqrt, log, exp, abs) |
| Mathematical constants | ✓ (pi, e) |
| Identifiers | ✓ |
| Keywords | ✓ (if, else, while, for) |
| Comments | ✓ (# single-line) |
| Position tracking | ✓ (line and column) |
| Error reporting | ✓ |


## Conclusions

In this laboratory work, I successfully implemented a lexer (scanner/tokenizer) for a mathematical expression language, gaining practical understanding of lexical analysis — the first and fundamental stage of any compiler or interpreter.

### What Was Implemented

The lexer supports a comprehensive set of features:

1. **Multiple numeric formats** - integers, floats, and scientific notation (e.g., `2.998e8`)
2. **Trigonometric and mathematical functions** - as required by the task (sin, cos, tan, sqrt, log, exp, abs)
3. **Rich operator set** - arithmetic (`+`, `-`, `*`, `/`, `%`, `^`), comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), and logical (`and`, `or`, `not`)
4. **Keywords and control flow** - if, else, while, for
5. **Mathematical constants** - pi and e
6. **Error handling** - with precise position information (line and column)
7. **Comments** - single-line comments with `#`

### How the Lexer Works

The implementation follows a character-by-character scanning approach with lookahead capabilities:

1. **Character consumption**: The `_advance()` method reads characters one at a time while tracking position
2. **Pattern matching**: Each character triggers specific scanning logic based on its type
3. **Lookahead**: Methods like `_peek()` and `_peek_next()` allow examining upcoming characters without consuming them, essential for distinguishing `=` from `==` or recognizing decimal points in floats
4. **Keyword recognition**: Identifiers are first scanned completely, then checked against a keyword table — this approach is simpler and more maintainable than trying to recognize keywords during scanning

### Key Insights Learned

- **Lexical analysis is pattern matching**: The lexer's job is to recognize patterns (digits for numbers, letters for identifiers, specific symbols for operators) and categorize them appropriately
- **Position tracking matters**: Storing line and column information with each token is essential for meaningful error messages that help users locate problems in their source code
- **Separation of concerns**: The lexer only breaks input into tokens — it doesn't validate syntax (that's the parser's job) or evaluate expressions (that's the interpreter's job)
- **Lookahead enables complex tokens**: Without the ability to peek ahead, it would be impossible to correctly tokenize multi-character operators or distinguish floats from integers followed by dots
- **Error recovery is important**: A good lexer should provide clear error messages with exact locations, making debugging easier for users

### Practical Applications

The skills learned in implementing this lexer are directly applicable to:

- Building compilers and interpreters for programming languages
- Creating domain-specific languages (DSLs)
- Implementing configuration file parsers
- Text processing and data extraction tools
- Syntax highlighting in code editors

The lexer correctly identifies and categorizes tokens, providing a solid foundation for building a parser or interpreter in future work.

## References

1. [LLVM Tutorial - Implementing a Lexer](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)
2. [Lexical Analysis - Wikipedia](https://en.wikipedia.org/wiki/Lexical_analysis)
