import os
import sys
from pathlib import Path

# Add parent directory to path to import from lab3
sys.path.insert(0, str(Path(__file__).parent.parent / 'lab3'))

from lexer import Lexer, LexerError
from parser import Parser, ParseError, parse_source
from ast_nodes import print_ast


EXAMPLES = [
    ("Simple Assignment", "x = 10"),
    ("Arithmetic Expression", "result = 10 + 20 * 3"),
    ("Floating-Point", "x = 3.14159 / 2.0"),
    ("Trigonometric", "angle = sin(pi / 4) + cos(0)"),
    ("Complex Expression", "y = sqrt(x^2 + 1)"),
    ("Nested Functions", "result = sin(cos(tan(x)))"),
    ("Logical Expression", "valid = x >= 0 and x <= 100"),
    ("Multiple Operations", "a = b + c * d - e / f"),
    ("Unary Operators", "neg = -x + abs(y)"),
    ("Scientific Notation", "c = 2.998e8"),
    ("Compound Expression", "temp = (a + b) * (c - d) / (e + f)"),
    ("Exponentiation", "squared = x ^ 2 + y ^ 3"),
]

ERROR_CASES = [
    ("sin(x", "Unclosed parenthesis"),
    ("10 = x", "Cannot assign to literal"),
]


def print_section(title: str):
    """Print a formatted section header."""
    print(f"  {title}")
    print()


def main():
    print("       LABORATORY WORK 6 - Parser & Abstract Syntax Tree (AST)")
    
    # Part 1: Successful parses
    print_section("PART 1: SUCCESSFUL PARSING EXAMPLES")
    
    for i, (name, source) in enumerate(EXAMPLES, 1):
        print(f"\n[Example {i}] {name}")
        print(f"Input:  \"{source}\"")
        
        try:
            # Tokenize
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Display results
            print(f"\nTokens: {len(tokens) - 1} tokens (excluding EOF)")
            print("\nAST Structure:")
            print(print_ast(ast, indent=0), end="")
            
        except (LexerError, ParseError) as e:
            print(f"ERROR: {e}")

    # Part 2: Error handling
    print_section("PART 2: ERROR HANDLING")
    
    for source, desc in ERROR_CASES:
        print(f"\nTesting: \"{source}\"")
        print(f"Expected Error: {desc}")
        
        try:
            ast = parse_source(source)
            print("  [OK] No error detected (might be valid)")
        except (LexerError, ParseError) as e:
            print(f"  [OK] Error caught: {e}")
    
    # Part 3: Token types demonstration
    print_section("PART 3: TOKEN ANALYSIS")
    
    test_expr = "angle = sin(pi / 4) + cos(pi)"
    print(f"\nAnalyzing: \"{test_expr}\"")
    
    lexer = Lexer(test_expr)
    tokens = lexer.tokenize()
    
    print(f"\n{'Type':<20} {'Value':<20} {'Line':<6} {'Column':<6}")
    for token in tokens[:-1]:  # Exclude EOF
        val = repr(token.value) if isinstance(token.value, str) else str(token.value)
        print(f"{token.type.name:<20} {val[:18]:<20} {token.line:<6} {token.column:<6}")
    
    # Part 4: AST Visitor example
    print_section("PART 4: AST STRUCTURE DETAILS")
    
    complex_expr = "result = (x + y) * sin(x) - sqrt(z)"
    print(f"\nParsing: \"{complex_expr}\"")
    
    ast = parse_source(complex_expr)
    print("\nDetailed AST:")
    print(print_ast(ast, indent=0))
    
    # Part 5: Interactive mode
    print_section("PART 5: INTERACTIVE MODE")
    print("\nEnter expressions to parse, or 'quit' to exit.")
    print("Examples: 'x = 10 + 20', 'sin(pi)', 'sqrt(x^2 + 1)'")

    interactive_mode()


def _read_interactive_line(prompt: str) -> str:
    """Read a line from the console, falling back to the Windows console when needed."""
    if os.name == "nt":
        import msvcrt

        print(prompt, end="", flush=True)
        chars = []

        while True:
            ch = msvcrt.getwch()

            if ch in ("\r", "\n"):
                print()
                return "".join(chars)

            if ch == "\x03":
                raise KeyboardInterrupt

            if ch == "\b":
                if chars:
                    chars.pop()
                    print("\b \b", end="", flush=True)
                continue

            chars.append(ch)
            print(ch, end="", flush=True)

    raise EOFError("Interactive input is not available")


def interactive_mode():
    """Run an interactive parsing session."""
    while True:
        try:
            source = _read_interactive_line("\n>>> ").strip()
            
            if not source:
                continue
            
            if source.lower() in ['quit', 'exit', 'q']:
                print("Exiting interactive mode.")
                break
            
            # Tokenize and parse
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Display results
            print("\nAST Structure:")
            print(print_ast(ast, indent=0))
            
        except LexerError as e:
            print(f"Lexer Error: {e}")
        except ParseError as e:
            print(f"Parse Error: {e}")
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
