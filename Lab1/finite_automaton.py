class FiniteAutomaton:
    def __init__(self, states: set, alphabet: set, transitions: dict, 
                 start_state: str, final_states: set):
        """
        Args:
            states: Set of all states (Q)
            alphabet: Set of input symbols (Σ)
            transitions: Transition function as dict {(state, symbol): set of next states}
            start_state: Initial state (q0)
            final_states: Set of accepting states (F)
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
    
    def string_belongs_to_language(self, input_string: str) -> bool:

        # Start from the initial state
        current_states = {self.start_state}
        
        # Process each symbol in the input string
        for symbol in input_string:
            # Check if the symbol is in the alphabet
            if symbol not in self.alphabet:
                return False
            
            # Compute the next set of states
            next_states = set()
            for state in current_states:
                key = (state, symbol)
                if key in self.transitions:
                    next_states.update(self.transitions[key])
            
            # If no transitions are possible, the string is not accepted
            if not next_states:
                return False
            
            current_states = next_states
        
        # Check if any current state is a final state ("X" = "X")
        return bool(current_states.intersection(self.final_states))
    
    def __str__(self) -> str:
        lines = ["Finite Automaton:"]
        lines.append(f"  States Q: {self.states}")
        lines.append(f"  Alphabet Σ: {self.alphabet}")
        lines.append(f"  Start state q0: {self.start_state}")
        lines.append(f"  Final states F: {self.final_states}")
        lines.append("  Transitions δ:")
        for (state, symbol), next_states in sorted(self.transitions.items()):
            lines.append(f"    δ({state}, {symbol}) = {next_states}")
        return "\n".join(lines)
