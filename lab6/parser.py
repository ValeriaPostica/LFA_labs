import sys
from typing import List, Optional
from pathlib import Path

# Add parent directory to path to import from lab3
sys.path.insert(0, str(Path(__file__).parent.parent / 'lab3'))

from lexer import Token, TokenType, Lexer, LexerError
from ast_nodes import (
    Program, Statement, Expression, ExpressionStatement, AssignmentStatement,
    IfStatement, WhileStatement, BinaryOp, UnaryOp, FunctionCall,
    Identifier, NumberLiteral, PiLiteral, EulerLiteral
)


class ParseError(Exception):
    """Exception raised when a parsing error occurs."""
    def __init__(self, message: str, token: Optional[Token] = None):
        if token:
            super().__init__(f"Parse Error at line {token.line}, column {token.column}: {message}")
        else:
            super().__init__(f"Parse Error: {message}")


class Parser:
    """Recursive descent parser for mathematical expressions."""
    
    # Token types that start an expression
    EXPRESSION_STARTERS = {
        TokenType.INTEGER, TokenType.FLOAT, TokenType.IDENTIFIER,
        TokenType.LPAREN, TokenType.MINUS, TokenType.NOT, TokenType.PLUS,
        TokenType.SIN, TokenType.COS, TokenType.TAN, TokenType.SQRT,
        TokenType.LOG, TokenType.EXP, TokenType.ABS, TokenType.PI, TokenType.E
    }
    
    # Mathematical functions
    FUNCTIONS = {
        TokenType.SIN, TokenType.COS, TokenType.TAN,
        TokenType.SQRT, TokenType.LOG, TokenType.EXP, TokenType.ABS
    }
    
    def __init__(self, tokens: List[Token]):
        """Initialize parser with a list of tokens."""
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else None
    
    def parse(self) -> Program:
        """Parse the token stream and return the AST."""
        statements = []
        
        while not self._check(TokenType.EOF):
            # Skip newlines at the statement level
            if self._check(TokenType.NEWLINE):
                self._advance()
                continue
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    def _parse_statement(self) -> Optional[Statement]:
        """Parse a single statement."""
        # If statement
        if self._check(TokenType.IF):
            return self._parse_if_statement()
        
        # While statement
        if self._check(TokenType.WHILE):
            return self._parse_while_statement()
        
        # For statement
        if self._check(TokenType.FOR):
            return self._parse_for_statement()
        
        # Expression statement (including assignments)
        if self._check_any(*self.EXPRESSION_STARTERS):
            expr = self._parse_expression()
            
            # Check for assignment
            if self._check(TokenType.ASSIGN):
                if not isinstance(expr, Identifier):
                    raise ParseError("Invalid assignment target", self.current)
                self._advance()  # consume '='
                value = self._parse_expression()
                stmt = AssignmentStatement(expr.name, value)
            else:
                stmt = ExpressionStatement(expr)
            
            # Consume optional semicolon or newline
            if self._check(TokenType.SEMICOLON) or self._check(TokenType.NEWLINE):
                self._advance()
            
            return stmt
        
        raise ParseError(f"Unexpected token: {self.current.type.name}", self.current)
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse an if statement."""
        self._consume(TokenType.IF, "Expected 'if'")
        
        condition = self._parse_expression()
        
        then_branch = self._parse_block()
        
        else_branch = None
        if self._check(TokenType.ELSE):
            self._advance()
            else_branch = self._parse_block()
        
        return IfStatement(condition, then_branch, else_branch)
    
    def _parse_while_statement(self) -> WhileStatement:
        """Parse a while statement."""
        self._consume(TokenType.WHILE, "Expected 'while'")
        
        condition = self._parse_expression()
        body = self._parse_block()
        
        return WhileStatement(condition, body)
    
    def _parse_for_statement(self) -> Statement:
        """Parse a for statement (simplified version)."""
        self._consume(TokenType.FOR, "Expected 'for'")
        
        var_name = self._consume(TokenType.IDENTIFIER, "Expected identifier in for loop").value
        
        # Simplified: assume "for x = 1 to 10" format
        self._consume(TokenType.ASSIGN, "Expected '=' in for loop")
        start = self._parse_expression()
        
        # Accept 'to' as an identifier for now
        if self._check(TokenType.IDENTIFIER) and self.current.value.lower() == 'to':
            self._advance()
        else:
            raise ParseError("Expected 'to' in for loop", self.current)
        
        end = self._parse_expression()
        body = self._parse_block()
        
        return ExpressionStatement(NumberLiteral(0))  # Placeholder
    
    def _parse_block(self) -> List[Statement]:
        """Parse a block of statements (between { and } or on the same line)."""
        statements = []
        
        # If followed by semicolon, parse until semicolon
        if self._check(TokenType.SEMICOLON):
            self._advance()
            if self._check_any(*self.EXPRESSION_STARTERS):
                stmt = self._parse_statement()
                if stmt:
                    statements.append(stmt)
        
        return statements if statements else [ExpressionStatement(NumberLiteral(0))]
    
    def _parse_expression(self) -> Expression:
        """Parse an expression (handles operator precedence)."""
        return self._parse_logical_or()
    
    def _parse_logical_or(self) -> Expression:
        """Parse logical OR expressions."""
        left = self._parse_logical_and()
        
        while self._check(TokenType.OR):
            op = self.current.value
            self._advance()
            right = self._parse_logical_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_logical_and(self) -> Expression:
        """Parse logical AND expressions."""
        left = self._parse_equality()
        
        while self._check(TokenType.AND):
            op = self.current.value
            self._advance()
            right = self._parse_equality()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_equality(self) -> Expression:
        """Parse equality operators (==, !=)."""
        left = self._parse_comparison()
        
        while self._check(TokenType.EQ) or self._check(TokenType.NEQ):
            op = self.current.value
            self._advance()
            right = self._parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_comparison(self) -> Expression:
        """Parse comparison operators (<, >, <=, >=)."""
        left = self._parse_addition()
        
        while self._check_any(TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.current.value
            self._advance()
            right = self._parse_addition()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_addition(self) -> Expression:
        """Parse addition and subtraction."""
        left = self._parse_multiplication()
        
        while self._check_any(TokenType.PLUS, TokenType.MINUS):
            op = self.current.value
            self._advance()
            right = self._parse_multiplication()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_multiplication(self) -> Expression:
        """Parse multiplication, division, and modulo."""
        left = self._parse_exponentiation()
        
        while self._check_any(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.current.value
            self._advance()
            right = self._parse_exponentiation()
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_exponentiation(self) -> Expression:
        """Parse exponentiation (right associative)."""
        left = self._parse_unary()
        
        if self._check(TokenType.POWER):
            op = self.current.value
            self._advance()
            right = self._parse_exponentiation()  # Right associative
            left = BinaryOp(left, op, right)
        
        return left
    
    def _parse_unary(self) -> Expression:
        """Parse unary operators (-, +, not)."""
        if self._check_any(TokenType.MINUS, TokenType.PLUS, TokenType.NOT):
            op = self.current.value
            self._advance()
            operand = self._parse_unary()
            return UnaryOp(op, operand)
        
        return self._parse_postfix()
    
    def _parse_postfix(self) -> Expression:
        """Parse postfix expressions (function calls)."""
        return self._parse_primary()
    
    def _parse_primary(self) -> Expression:
        """Parse primary expressions (literals, identifiers, function calls, parentheses)."""
        
        # Numbers
        if self._check(TokenType.INTEGER):
            value = self.current.value
            self._advance()
            return NumberLiteral(value)
        
        if self._check(TokenType.FLOAT):
            value = self.current.value
            self._advance()
            return NumberLiteral(value)
        
        # Constants
        if self._check(TokenType.PI):
            self._advance()
            return PiLiteral()
        
        if self._check(TokenType.E):
            self._advance()
            return EulerLiteral()
        
        # Identifiers (variables or function calls)
        if self._check(TokenType.IDENTIFIER):
            name = self.current.value
            self._advance()
            
            # Check for function call
            if self._check(TokenType.LPAREN):
                self._advance()
                args = self._parse_arguments()
                self._consume(TokenType.RPAREN, "Expected ')'")
                return FunctionCall(name, args)
            
            return Identifier(name)
        
        # Built-in function calls
        if self._check_any(*self.FUNCTIONS):
            func_name = self.current.value
            self._advance()
            
            self._consume(TokenType.LPAREN, f"Expected '(' after {func_name}")
            args = self._parse_arguments()
            self._consume(TokenType.RPAREN, f"Expected ')' after {func_name} arguments")
            
            return FunctionCall(func_name, args)
        
        # Parenthesized expression
        if self._check(TokenType.LPAREN):
            self._advance()
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "Expected ')'")
            return expr
        
        raise ParseError(f"Unexpected token in expression: {self.current.type.name}", self.current)
    
    def _parse_arguments(self) -> List[Expression]:
        """Parse function arguments."""
        args = []
        
        if not self._check(TokenType.RPAREN):
            args.append(self._parse_expression())
            
            while self._check(TokenType.COMMA):
                self._advance()
                args.append(self._parse_expression())
        
        return args
    
    # Helper methods
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type."""
        return self.current and self.current.type == token_type
    
    def _check_any(self, *token_types: TokenType) -> bool:
        """Check if current token is any of the given types."""
        return self.current and self.current.type in token_types
    
    def _advance(self) -> Token:
        """Consume and return the current token."""
        token = self.current
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None
        return token
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """Consume a token of the expected type or raise an error."""
        if not self._check(token_type):
            raise ParseError(message, self.current)
        return self._advance()


def parse_source(source: str) -> Program:
    """Convenience function to tokenize and parse source code."""
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    except LexerError as e:
        raise ParseError(f"Lexer error: {e}")
