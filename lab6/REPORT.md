# Laboratory Work 6 - Parser & Abstract Syntax Tree (AST)

### Topic: Parser & Building an Abstract Syntax Tree  
### Course: Formal Languages & Finite Automata
### Author: Postica Valeria FAF-243

---

## 1. Overview

This laboratory work focuses on implementing a **parser** and building an **Abstract Syntax Tree (AST)** for a mathematical expression language. The parser extends the lexer from Laboratory Work 3 by extracting syntactic structure and meaning from the token stream.

### Key Concepts

- **Parsing**: The process of analyzing a sequence of tokens to extract syntactic structure
- **Abstract Syntax Tree (AST)**: A hierarchical representation of the syntactic structure of the source code
- **Recursive Descent Parsing**: A top-down parsing technique where each grammar rule is implemented as a function
- **Operator Precedence**: Handling the correct order of operations in expressions

---

## 2. Objectives

1. Extend the lexical analyzer from Lab 3 with a parser
2. Implement a comprehensive `TokenType` enum using the existing lexer
3. Design and implement AST data structures to represent program constructs
4. Implement a recursive descent parser that builds AST from tokens
5. Demonstrate parsing of complex expressions with multiple operators
6. Handle error reporting and recovery

---

## 3. Implementation Details

### 3.1 Architecture

The implementation has three coordinated components: the lexer (from Lab 3) that tokenizes the source text into a stream of tokens; the parser (this lab) that consumes those tokens and constructs an Abstract Syntax Tree (AST); and the AST, which represents the program's syntactic structure for later analysis, evaluation, or code generation.

### 3.2 TokenType Enum

The lexer from Lab 3 already provides a comprehensive `TokenType` enum:

```python
class TokenType(Enum):
		# Literals
		INTEGER, FLOAT, IDENTIFIER, PI, E
    
		# Functions
		SIN, COS, TAN, SQRT, LOG, EXP, ABS
    
		# Operators
		PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, POWER
		EQ, NEQ, LT, GT, LTE, GTE, ASSIGN
		AND, OR, NOT
    
		# Delimiters
		LPAREN, RPAREN, COMMA, SEMICOLON, NEWLINE
    
		# Keywords
		IF, ELSE, WHILE, FOR
    
		# Special
		EOF
```

### 3.3 AST Node Hierarchy

The AST is composed of different node types representing different language constructs:

#### **Expression Nodes**

- `NumberLiteral(value)` - Integer or floating-point numbers
- `Identifier(name)` - Variable names
- `PiLiteral()` - Mathematical constant π
- `EulerLiteral()` - Mathematical constant e
- `BinaryOp(left, operator, right)` - Binary operations (+, -, *, /, ^, etc.)
- `UnaryOp(operator, operand)` - Unary operations (-, +, not)
- `FunctionCall(name, args)` - Function calls (sin, cos, sqrt, etc.)

#### **Statement Nodes**

- `ExpressionStatement(expression)` - A standalone expression
- `AssignmentStatement(identifier, value)` - Variable assignment
- `IfStatement(condition, then_branch, else_branch)` - Conditional branching
- `WhileStatement(condition, body)` - Loop constructs
- `ForStatement(variable, start, end, body)` - For loop (simplified)

#### **Program Node**

- `Program(statements)` - Root node containing all statements

### 3.4 Parser Implementation

The parser uses **recursive descent parsing** with proper **operator precedence**:

```
Expression Hierarchy (from lowest to highest precedence):
┌─ Logical OR (||)
│  ├─ Logical AND (&&)
│  │  ├─ Equality (==, !=)
│  │  │  ├─ Comparison (<, >, <=, >=)
│  │  │  │  ├─ Addition/Subtraction (+, -)
│  │  │  │  │  ├─ Multiplication/Division (*, /, %)
│  │  │  │  │  │  ├─ Exponentiation (^) [right-associative]
│  │  │  │  │  │  │  ├─ Unary (-, +, not)
│  │  │  │  │  │  │  │  └─ Primary (literals, identifiers, function calls, parentheses)
```

**Key parsing methods:**

- `parse()` - Main entry point, parses the entire program
- `_parse_statement()` - Parses assignments, control flow, expressions
- `_parse_expression()` - Parses expressions with proper precedence
- `_parse_binary_op_*()` - Handle different operator precedence levels
- `_parse_unary()` - Handles unary operators
- `_parse_primary()` - Parses literals, identifiers, function calls

### 3.5 Code Files

#### **ast_nodes.py**
Defines all AST node classes with proper inheritance hierarchy:
- Base classes: `ASTNode`, `Statement`, `Expression`
- Concrete node types for all language constructs
- Helper function `print_ast()` for pretty-printing ASTs

#### **parser.py**
Implements the recursive descent parser:
- `Parser` class with all parsing methods
- `ParseError` exception for error reporting
- `parse_source()` convenience function

#### **main.py**
Demonstration program showing:
- 12 example expressions of increasing complexity
- Error handling demonstrations
- Token analysis
- Interactive parsing session

---

## 4. Examples

### Example 1: Simple Assignment
```
Input:  x = 10
Output: Program(
					statements=[
						AssignmentStatement(x = NumberLiteral(10))
					]
				)
```

### Example 2: Arithmetic Expression
```
Input:  result = 10 + 20 * 3
Output: Program(
					statements=[
						AssignmentStatement(result = 
							BinaryOp(
								NumberLiteral(10),
								+,
								BinaryOp(NumberLiteral(20), *, NumberLiteral(3))
							)
						)
					]
				)
```

### Example 3: Function Calls
```
Input:  angle = sin(pi / 4) + cos(0)
Output: Program(
					statements=[
						AssignmentStatement(angle =
							BinaryOp(
								FunctionCall(sin, [BinaryOp(PiLiteral(), /, NumberLiteral(4))]),
								+,
								FunctionCall(cos, [NumberLiteral(0)])
							)
						)
					]
				)
```

### Example 4: Complex Nested Expression
```
Input:  y = sqrt(x^2 + 1)
Output: Program(
					statements=[
						AssignmentStatement(y =
							FunctionCall(sqrt, [
								BinaryOp(
									BinaryOp(Identifier(x), ^, NumberLiteral(2)),
									+,
									NumberLiteral(1)
								)
							])
						)
					]
				)
```

---

## 5. Testing & Results

### Test Categories

1. **Basic Literals and Identifiers**
	 - Numbers (int, float, scientific notation)
	 - Variables
	 - Mathematical constants (π, e)

2. **Arithmetic Expressions**
	 - Binary operations with multiple operators
	 - Operator precedence (multiplication before addition, etc.)
	 - Exponentiation with right-associativity

3. **Function Calls**
	 - Built-in functions (sin, cos, tan, sqrt, log, exp, abs)
	 - Multiple arguments
	 - Nested function calls

4. **Logical and Comparison**
	 - Comparison operators (<, >, <=, >=, ==, !=)
	 - Logical operators (&&, ||, !)
	 - Proper precedence handling

5. **Error Detection**
	 - Mismatched parentheses
	 - Invalid assignments (to literals)
	 - Unexpected tokens

### Sample Output

When running `main.py`, the program demonstrates:

1. **12 successful parsing examples** showing increasing complexity
2. **Error handling** demonstrating graceful error reporting
3. **Token analysis** showing lexical structure
4. **Interactive mode** for manual testing

---

## 6. Key Implementation Decisions

### 6.1 Recursive Descent Parsing

**Why chosen:** 
- Direct correspondence between grammar rules and code
- Easy to understand and modify
- Excellent error reporting capabilities
- Suitable for the expression grammar

### 6.2 Operator Precedence via Recursive Methods

**Approach:** Each precedence level is a separate parsing method that calls the next higher precedence level. This ensures correct operator precedence without explicit parse tables.

### 6.3 Right-Associative Exponentiation

**Implementation:** The exponentiation parsing method calls itself recursively on the right operand, ensuring that `2^3^2` parses as `2^(3^2)` rather than `(2^3)^2`.

### 6.4 AST-Only Representation

**Design:** The AST is pure data structures without evaluation. This allows for:
- Easy visualization
- Separate evaluation phase
- Static analysis possibilities

---

## 7. Error Handling

The parser provides comprehensive error handling:

```python
class ParseError(Exception):
		"""Reports parse errors with line and column information"""
    
# Examples:
# Parse Error at line 1, column 5: Expected ')'
# Parse Error at line 2, column 3: Cannot assign to literal
```

Error information includes:
- Line number where error occurred
- Column number in source
- Descriptive message about what went wrong

---

## 8. Operator Precedence Summary

| Precedence | Operators | Associativity |
|:----------:|:----------|:-------------:|
| 1 (lowest) | `\|\|` (OR) | Left |
| 2 | `&&` (AND) | Left |
| 3 | `==`, `!=` (Equality) | Left |
| 4 | `<`, `>`, `<=`, `>=` (Comparison) | Left |
| 5 | `+`, `-` (Addition) | Left |
| 6 | `*`, `/`, `%` (Multiplication) | Left |
| 7 | `^` (Exponentiation) | **Right** |
| 8 | `-`, `+`, `!` (Unary) | Right |
| 9 (highest) | Literals, Identifiers, Function Calls, Parentheses | - |

---

## 9. Conclusion

This laboratory successfully implements a complete parser for a mathematical expression language, demonstrating:

 **Lexical Analysis Integration** - Seamless use of Lab 3's lexer  
 **AST Construction** - Proper hierarchical representation  
 **Operator Precedence** - Correct parsing of complex expressions  
 **Error Handling** - Meaningful error messages  
 **Comprehensive Testing** - Multiple examples and edge cases  

The parser can be extended for:
- Actual evaluation of expressions
- Semantic analysis
- Code generation
- Optimization passes

---

## 10. References

- [Wikipedia - Parsing](https://en.wikipedia.org/wiki/Parsing)
- [Wikipedia - Abstract Syntax Tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
- [Recursive Descent Parsing](https://en.wikipedia.org/wiki/Recursive_descent_parser)
- [Operator Precedence](https://en.wikipedia.org/wiki/Operator_precedence)

---

**Files Included:**
- `ast_nodes.py` - AST node definitions
- `parser.py` - Parser implementation
- `main.py` - Demonstration and testing
- `REPORT.md` - This document