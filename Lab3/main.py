from lexer import Lexer, LexerError

EXAMPLES = [
    ("Basic Arithmetic", "result = 10 + 20 * 3"),
    ("Floating-Point Numbers", "x = 3.14159 / 2.0 + 0.5"),
    ("Trigonometric Functions", "angle = sin(pi / 4) + cos(0)"),
    ("Complex Expression", "y = sqrt(x^2 + 1) * exp(-x) + log(abs(x))"),
    ("Comparison & Logical", "if x >= 0 and x <= 100"),
    ("Scientific Notation", "speed_of_light = 2.998e8"),
    ("Multi-line with Comments", "# Circle area\nradius = 5.0\narea = pi * radius ^ 2"),
    ("All Operators", "a + b - c * d / e % f ^ g"),
    ("Nested Functions", "result = sin(cos(tan(x)))"),
    ("Control Flow", "while x < 10; x = x + 1"),
]

ERROR_CASES = [
    ("@invalid", "Invalid character '@'"),
    ("$price", "Invalid character '$'"),
    ("1e", "Invalid scientific notation"),
]

def main():
    print("LABORATORY WORK 3 - Lexer & Scanner\n")
    
    for i, (name, source) in enumerate(EXAMPLES, 1):
        print(f"EXAMPLE {i}: {name}")
        print(f"Input: \"{source}\"")
        try:
            lexer = Lexer(source)
            lexer.tokenize()
            print(lexer.get_tokens_table())
        except LexerError as e:
            print(f"Error: {e}")
        print()
    
    print("ERROR HANDLING DEMONSTRATION")
    for source, desc in ERROR_CASES:
        print(f"Testing: \"{source}\" ({desc})")
        try:
            Lexer(source).tokenize()
            print("  Tokenized successfully")
        except LexerError as e:
            print(f"  Error: {e}")

def interactive_mode():
    print("\nINTERACTIVE LEXER MODE")
    print("Type expressions to tokenize, or 'quit' to exit.")
    
    while True:
        try:
            source = input("\n>>> ")
            if source.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            if not source.strip():
                continue
            lexer = Lexer(source)
            lexer.tokenize()
            print(lexer.get_tokens_table())
        except LexerError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
    interactive_mode()