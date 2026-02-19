# Intro to Formal Languages. Regular Grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Postica Valeria

----

## Theory

A formal language is a set of strings built from an alphabet according to specific rules. It consists of terminal symbols (VT), non-terminal symbols (VN), production rules (P), and a start symbol (S). Regular grammars are a type of formal grammar where productions are either right-linear (A → aB or A → a) or left-linear. Finite automata are mathematical models that recognize regular languages through states and transitions. Regular grammars and finite automata are equivalent - any regular grammar can be converted to an FA and vice versa.


## Objectives:

* Understand what a formal language is and its components.
* Implement a type/class for the grammar (Variant 22).
* Add a function that generates 5 valid strings from the language.
* Implement functionality to convert a Grammar to a Finite Automaton.
* Add a method to check if an input string can be obtained via state transitions.


## Implementation description

### Grammar Initialization

The Grammar class stores the four components of a formal grammar. The constructor takes non-terminals (VN), terminals (VT), production rules as a dictionary, and the start symbol.

```python
class Grammar:
    def __init__(self, vn: set, vt: set, p: dict, start_symbol: str):
        self.vn = vn  # Non-terminal symbols
        self.vt = vt  # Terminal symbols
        self.p = p    # Production rules
        self.start_symbol = start_symbol
```

### String Generation

The `generate_string` method creates valid strings by starting from S and randomly selecting productions. It continues until reaching a terminal-only production, building the result string along the way.

```python
def generate_string(self) -> str:
    result = ""
    current_symbol = self.start_symbol
    
    while current_symbol in self.vn:
        productions = self.p.get(current_symbol, [])
        production = random.choice(productions)
        
        for char in production:
            if char in self.vt:
                result += char
            elif char in self.vn:
                current_symbol = char
                break
        else:
            current_symbol = None
    
    return result
```

### Grammar to Finite Automaton Conversion

The `to_finite_automaton` method converts the grammar to an FA. For productions like A → aB, it creates transition δ(A, a) = B. For terminal productions like A → a, it creates δ(A, a) = q_final.

```python
def to_finite_automaton(self):
    q_final = "X"
    states = self.vn.copy()
    states.add(q_final)
    
    transitions = {}
    for non_terminal, productions in self.p.items():
        for production in productions:
            if len(production) == 1 and production in self.vt:
                key = (non_terminal, production)
                transitions.setdefault(key, set()).add(q_final)
            elif len(production) == 2:
                terminal, next_state = production[0], production[1]
                key = (non_terminal, terminal)
                transitions.setdefault(key, set()).add(next_state)
    
    return FiniteAutomaton(states, self.vt, transitions, self.start_symbol, {q_final})
```

### String Validation in Finite Automaton

The `string_belongs_to_language` method simulates the automaton. It starts at the initial state, follows transitions for each input symbol, and checks if the final state is accepting.

```python
def string_belongs_to_language(self, input_string: str) -> bool:
    current_states = {self.start_state}
    
    for symbol in input_string:
        if symbol not in self.alphabet:
            return False
        
        next_states = set()
        for state in current_states:
            key = (state, symbol)
            if key in self.transitions:
                next_states.update(self.transitions[key])
        
        if not next_states:
            return False
        current_states = next_states
    
    return bool(current_states.intersection(self.final_states))
```


## Conclusions / Screenshots / Results

This laboratory work successfully demonstrated the fundamental relationship between formal grammars and finite automata by implementing both computational models for Variant 22 and establishing their equivalence.

### Implementation Process

The development process began with analyzing the theoretical foundations of formal languages and understanding the four core components: the set of non-terminal symbols (VN), terminal symbols (VT), production rules (P), and the start symbol (S). For Variant 22, the grammar was defined with three non-terminals {S, D, F}, four terminals {a, b, c, d}, and a set of production rules that define how strings can be derived.

The first step involved creating the `Grammar` class in Python, which encapsulates all components of a formal grammar. The class constructor was designed to accept the sets of terminals and non-terminals, a dictionary structure for production rules, and the designated start symbol. This object-oriented approach ensures clean separation of concerns and makes the code reusable for different grammar variants.

Next, the string generation algorithm was implemented using a recursive derivation approach. Starting from the initial symbol S, the algorithm randomly selects applicable production rules and continues the derivation process until only terminal symbols remain. The use of Python's `random.choice()` function ensures variety in the generated strings, demonstrating that the grammar can produce multiple valid outputs. Edge cases were considered, such as handling productions that lead directly to terminals versus those that include both a terminal and a non-terminal.

The most challenging aspect was implementing the grammar-to-finite-automaton conversion. This required understanding the correspondence between right-linear grammar productions and FA transitions. For each production of the form A → aB (where A, B are non-terminals and a is a terminal), a transition δ(A, a) = B was created. For productions of the form A → a (terminal-only), a special final state X was introduced, with the transition δ(A, a) = X. This systematic mapping preserves the language recognized by both representations.

The `FiniteAutomaton` class was then developed to store states, alphabet, transitions (as a dictionary), the initial state, and the set of final states. The string validation method implements the standard FA simulation algorithm: starting from the initial state, it processes each input symbol by following the corresponding transitions, and accepts the string if and only if the final reached state is in the set of accepting states.

### Testing and Validation

The implementation was thoroughly tested by generating multiple strings from the grammar and verifying that each one was correctly accepted by the converted finite automaton. Additionally, invalid strings (those not derivable from the grammar) were tested to confirm proper rejection. This bidirectional testing confirmed the correctness of both the generation and validation mechanisms.

### Key Learnings

Through the development of a Grammar class that generates valid strings using production rules and a FiniteAutomaton class that validates strings through state transitions, the practical implementation confirmed the theoretical principle that regular grammars and finite automata are interchangeable representations of the same formal language. The conversion algorithm effectively mapped grammar productions to automaton transitions, showing that every string derivable from the grammar (such as "ca", "abcda", and "cba") was correctly recognized by the corresponding finite automaton, while invalid strings were properly rejected.

This hands-on experience solidified the understanding of how formal language theory provides the mathematical foundation for pattern recognition and language processing in computer science. The project reinforced important programming concepts including object-oriented design, dictionary-based data structures for representing transitions, set operations for state management, and algorithm design for language recognition. Understanding the equivalence between grammars and automata is fundamental for more advanced topics such as compiler design, regular expression engines, and lexical analysis.

**Grammar Definition (Variant 22):**
```
VN = {S, D, F}
VT = {a, b, c, d}
P = { S → aS | bS | cD,  D → dD | bF | a,  F → bS | a }
```

**Example Generated Strings:**
- "ca" (S → cD → ca)
- "abcda" (S → aS → abS → abcD → abcdD → abcda)
- "cba" (S → cD → cbF → cba)

**Finite Automaton Transitions:**

| State | Symbol | Next State |
|-------|--------|------------|
| S | a | S |
| S | b | S |
| S | c | D |
| D | d | D |
| D | b | F |
| D | a | X |
| F | b | S |
| F | a | X |

The implementation demonstrates that regular grammars and finite automata are equivalent - all strings generated by the grammar are correctly accepted by the automaton.


## References

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). Introduction to Automata Theory, Languages, and Computation
2. Technical University of Moldova, Formal Languages and Finite Automata: Guide for practical lessons, Chișinău, 2022.
