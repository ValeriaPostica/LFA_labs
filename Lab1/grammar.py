import random
from finite_automaton import FiniteAutomaton

class Grammar:
    
    def __init__(self, vn: set, vt: set, p: dict, start_symbol: str):
        self.vn = vn  # Non-terminal symbols
        self.vt = vt  # Terminal symbols
        self.p = p    # Production rules
        self.start_symbol = start_symbol
    
    def generate_string(self) -> str:
        result = ""
        current_symbol = self.start_symbol
        
        while current_symbol in self.vn:
            # Get all productions for the current non-terminal
            productions = self.p.get(current_symbol, [])
            
            if not productions:
                break
            
            # Randomly select one production
            production = random.choice(productions)
            
            # Process the production
            # Productions are in the form: terminal or terminal + non-terminal
            for char in production:
                if char in self.vt:
                    result += char
                elif char in self.vn:
                    current_symbol = char
                    break
            else:
                # No non-terminal found, we've reached a terminal production
                current_symbol = None
        
        return result
    
    def generate_strings(self, count: int = 5) -> list:
        return [self.generate_string() for _ in range(count)]
    
    def to_finite_automaton(self):
        # States are all non-terminals plus a final state
        q_final = "X"
        states = self.vn.copy()
        states.add(q_final)
        
        # Alphabet is the set of terminal symbols
        alphabet = self.vt.copy()
        
        # Build transition function
        # transitions = {(state, symbol): set of next states}
        transitions = {}
        
        for non_terminal, productions in self.p.items():
            for production in productions:
                # Because we work with a Regular Grammar(right) we can use
                # the fact that on the right side it is always either ->a or ->aB
                if len(production) == 1 and production in self.vt:
                    # Production of form A → a (terminal only)
                    key = (non_terminal, production)
                    if key not in transitions:
                        transitions[key] = set()
                    transitions[key].add(q_final)
                    
                elif len(production) == 2:
                    # Production of form A → aB (terminal + non-terminal)
                    terminal = production[0]
                    next_state = production[1]
                    key = (non_terminal, terminal)
                    if key not in transitions:
                        transitions[key] = set()
                    transitions[key].add(next_state)
        
        # Start state is the grammar's start symbol
        start_state = self.start_symbol
        
        # Final states
        final_states = {q_final}
        
        return FiniteAutomaton(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            start_state=start_state,
            final_states=final_states
        )
    
    def __str__(self) -> str:
        lines = ["Grammar:"]
        lines.append(f"  VN (Non-terminals): {self.vn}")
        lines.append(f"  VT (Terminals): {self.vt}")
        lines.append(f"  Start symbol: {self.start_symbol}")
        lines.append("  Productions P:")
        for non_terminal, productions in self.p.items():
            for prod in productions:
                lines.append(f"    {non_terminal} → {prod}")
        return "\n".join(lines)
