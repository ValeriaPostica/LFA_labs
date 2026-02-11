from grammar import Grammar
from finite_automaton import FiniteAutomaton


def main():
    
    vn = {'S', 'D', 'F'}  # Non-terminal symbols
    vt = {'a', 'b', 'c', 'd'}  # Terminal symbols
    
    # Production rules as dictionary
    # Each non-terminal maps to a list of its possible productions
    productions = {
        'S': ['aS', 'bS', 'cD'],
        'D': ['dD', 'bF', 'a'],
        'F': ['bS', 'a']
    }
    
    start_symbol = 'S'
    
    # Create the grammar
    grammar = Grammar(vn, vt, productions, start_symbol)
    
    print("LABORATORY WORK 1 - VARIANT 22")
    
    # Task 3a: Display the grammar
    print("\nTask 3a: Grammar Definition")
    print(grammar)
    
    # Task 3b: Generate 5 valid strings
    print("\nTask 3b: Generate 5 Valid Strings")
    generated_strings = grammar.generate_strings()
    for i, string in enumerate(generated_strings, 1):
        print(f"  String {i}: {string}")
    
    # Task 3c: Convert Grammar to Finite Automaton
    print("\nTask 3c: Convert Grammar to Finite Automaton")
    fa = grammar.to_finite_automaton()
    print(fa)
    
    # Task 3d: Check if strings belong to the language
    print("\nTask 3d: String Validation using Finite Automaton")
    # Test with some manual test cases
    print("\nTesting strings:")
    test_strings = [
        "ca",            # S → cD → ca (valid)
        "abca",         # S → aS → abS → abcD → abca (valid)
        "cda",          # S → cD → cdD → cda (valid)
        "cbba",         # S → cD → cbF → cbbS → ... needs to end properly
        "cba",          # S → cD → cbF → cba (valid)
        "aabbcda",      # longer valid string
        "x",            # Invalid (x not in alphabet)
        "ac",           # Invalid path
        "",             # Empty string (invalid - no production leads to empty)
        "aaabbbcdddda", # S → aS → aaS → aaaS → aaabS → ... → cD → dD → ... → a
    ]
    
    for string in test_strings:
        result = fa.string_belongs_to_language(string)
        status = "ACCEPTED" if result else "REJECTED"
        print(f"  '{string}' -> {status}")

if __name__ == "__main__":
    main()
