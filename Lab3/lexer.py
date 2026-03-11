from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Any

class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    IDENTIFIER = auto()
    SIN = auto()
    COS = auto()
    TAN = auto()
    SQRT = auto()
    LOG = auto()
    EXP = auto()
    ABS = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    SEMICOLON = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    EOF = auto()
    NEWLINE = auto()
    PI = auto()
    E = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")

class Lexer:
    KEYWORDS = {
        'sin': TokenType.SIN, 'cos': TokenType.COS, 'tan': TokenType.TAN,
        'sqrt': TokenType.SQRT, 'log': TokenType.LOG, 'exp': TokenType.EXP,
        'abs': TokenType.ABS, 'if': TokenType.IF, 'else': TokenType.ELSE,
        'while': TokenType.WHILE, 'for': TokenType.FOR, 'and': TokenType.AND,
        'or': TokenType.OR, 'not': TokenType.NOT, 'pi': TokenType.PI, 'e': TokenType.E,
    }
    
    SINGLE_CHAR = {
        '+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE, '%': TokenType.MODULO, '^': TokenType.POWER,
        '(': TokenType.LPAREN, ')': TokenType.RPAREN, ',': TokenType.COMMA,
        ';': TokenType.SEMICOLON,
    }
    
    TWO_CHAR = {'==': TokenType.EQ, '!=': TokenType.NEQ, '<=': TokenType.LTE,
                '>=': TokenType.GTE, '&&': TokenType.AND, '||': TokenType.OR}
    
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.pos = self.line = self.col = 0
        self.line = 1
        self.col = 1
    
    def tokenize(self) -> List[Token]:
        self.tokens = []
        while self.pos < len(self.source):
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.col))
        return self.tokens
    
    def _scan_token(self):
        start_col = self.col
        char = self._advance()
        
        if char in ' \t\r': return
        if char == '\n':
            self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, start_col))
            self.line += 1
            self.col = 1
            return
        if char == '#':
            while self._peek() != '\n' and self.pos < len(self.source): self._advance()
            return
        if char in self.SINGLE_CHAR:
            self.tokens.append(Token(self.SINGLE_CHAR[char], char, self.line, start_col))
            return
        
        two = char + self._peek()
        if two in self.TWO_CHAR:
            self._advance()
            self.tokens.append(Token(self.TWO_CHAR[two], two, self.line, start_col))
            return
        if char == '=':
            self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, start_col))
            return
        if char == '!':
            self.tokens.append(Token(TokenType.NOT, '!', self.line, start_col))
            return
        if char == '<':
            self.tokens.append(Token(TokenType.LT, '<', self.line, start_col))
            return
        if char == '>':
            self.tokens.append(Token(TokenType.GT, '>', self.line, start_col))
            return
        
        if char.isdigit():
            self._scan_number(start_col)
            return
        if char.isalpha() or char == '_':
            self._scan_identifier(start_col)
            return
        
        raise LexerError(f"Unexpected character: '{char}'", self.line, start_col)
    
    def _scan_number(self, start_col):
        start = self.pos - 1
        while self._peek().isdigit(): self._advance()
        
        is_float = False
        if self._peek() == '.' and self._peek_next().isdigit():
            is_float = True
            self._advance()
            while self._peek().isdigit(): self._advance()
        
        if self._peek().lower() == 'e':
            is_float = True
            self._advance()
            if self._peek() in '+-': self._advance()
            if not self._peek().isdigit():
                raise LexerError("Invalid number: expected exponent", self.line, self.col)
            while self._peek().isdigit(): self._advance()
        
        lexeme = self.source[start:self.pos]
        value = float(lexeme) if is_float else int(lexeme)
        self.tokens.append(Token(TokenType.FLOAT if is_float else TokenType.INTEGER, value, self.line, start_col))
    
    def _scan_identifier(self, start_col):
        start = self.pos - 1
        while self._peek().isalnum() or self._peek() == '_': self._advance()
        lexeme = self.source[start:self.pos]
        token_type = self.KEYWORDS.get(lexeme.lower(), TokenType.IDENTIFIER)
        self.tokens.append(Token(token_type, lexeme, self.line, start_col))
    
    def _advance(self) -> str:
        char = self.source[self.pos]
        self.pos += 1
        self.col += 1
        return char
    
    def _peek(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else '\0'
    
    def _peek_next(self) -> str:
        return self.source[self.pos + 1] if self.pos + 1 < len(self.source) else '\0'
    
    def get_tokens_table(self) -> str:
        lines = [f"{'Type':<20} {'Value':<20} {'Line':<6} {'Column':<6}"]
        for t in self.tokens:
            val = repr(t.value) if isinstance(t.value, str) else str(t.value)
            lines.append(f"{t.type.name:<20} {val[:18]:<20} {t.line:<6} {t.column:<6}")
        return "\n".join(lines)
