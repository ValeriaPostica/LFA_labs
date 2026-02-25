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
            productions = self.p.get(current_symbol, [])
            
            if not productions:
                break
            
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
    
    def generate_strings(self, count: int = 5) -> list:
        return [self.generate_string() for _ in range(count)]
    
    def classify_chomsky(self):
            # Classify the grammar according to the Chomsky hierarchy (Type 0–3).
            if self._check_type3():
                return "Type 3 — Regular Grammar"
            if self._check_type2():
                return "Type 2 — Context-Free Grammar"
            if self._check_type1():
                return "Type 1 — Context-Sensitive Grammar"
            return "Type 0 — Unrestricted Grammar"

        # Private helpers for each type check

    def _check_type3(self):
        # Regular grammar check.
        right_linear = False
        left_linear = False

        for lhs, rhs_options in self.p.items():
            if lhs not in self.vn:
                return False

            for rhs in rhs_options:
                if len(rhs) == 1:
                    if rhs in self.vt:
                        continue
                    return False
        
                if len(rhs) == 2:
                    if rhs[0] in self.vt and rhs[1] in self.vn:
                        right_linear = True
                    elif rhs[0] in self.vn and rhs[1] in self.vt:
                        left_linear = True
                    else:
                        return False
                    continue

        # ether right or left grammar
        if right_linear and left_linear:
            return False
        return True
    
    def _check_type2(self):
        for lhs in self.p:
            if lhs not in self.vn:
                return False
        return True

    def _check_type1(self):
        for lhs, rhs_options in self.p.items():
            for rhs in rhs_options:
                if rhs in ('', 'ε'):
                    return False
                if len(lhs) > len(rhs):
                    return False
        return True

    def to_finite_automaton(self):
        q_final = "X"
        states = self.vn.copy()
        states.add(q_final)
        
        alphabet = self.vt.copy()
        
        transitions = {}
        
        for non_terminal, productions in self.p.items():
            for production in productions:
                if len(production) == 1 and production in self.vt:
                    key = (non_terminal, production)
                    if key not in transitions:
                        transitions[key] = set()
                    transitions[key].add(q_final)
                    
                elif len(production) == 2:
                    terminal = production[0]
                    next_state = production[1]
                    key = (non_terminal, terminal)
                    if key not in transitions:
                        transitions[key] = set()
                    transitions[key].add(next_state)
        
        start_state = self.start_symbol
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
