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
        #Check if a string is accepted by the automaton
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
    
    def is_deterministic(self) -> bool:
        """
         A FA is deterministic if:
        1. For each state and symbol, there is at most one transition
        2. No epsilon transitions (not checked here as we don't support them)
        Returns:
            bool: True if DFA, False if NFA
        """
        for (state, symbol), next_states in self.transitions.items():
            if len(next_states) > 1:
                return False
        
        return True
    
    def to_regular_grammar(self):
        """
        Algorithm:
        - Each state becomes a non-terminal
        - For transition δ(A, a) = B, create production A → aB
        - For transition δ(A, a) = F where F is a final state, create A → a
        - Start symbol is the start state
        Returns:
            Grammar: A regular grammar equivalent to this FA
        """
        from grammar import Grammar
        
        # Non-terminals are the states
        vn = set(self.states)
        
        # Terminals are the alphabet
        vt = set(self.alphabet)
        
        # Build productions
        productions = {}
        
        for (state, symbol), next_states in self.transitions.items():
            if state not in productions:
                productions[state] = []
            
            for next_state in next_states:
                # If next state is a final state, we can add both A → a and A → aB
                if next_state in self.final_states:
                    # Add A → a (terminates)
                    if symbol not in productions[state]:
                        productions[state].append(symbol)
                
                # Add A → aB (continues to next state)
                production = symbol + next_state
                if production not in productions[state]:
                    productions[state].append(production)
        
        return Grammar(vn, vt, productions, self.start_state)
    
    def to_dfa(self) -> 'FiniteAutomaton':
        """
        Algorithm:
        1. Start with the set containing only the initial state
        2. For each set of states and each symbol, compute the set of reachable states
        3. Repeat until no new sets are created
        4. Final states are any sets containing an original final state
        Returns:
            FiniteAutomaton: An equivalent DFA
        """
        if self.is_deterministic():
            return self
        
        # Initial state of DFA is the set containing the NFA's start state
        initial_dfa_state = frozenset([self.start_state])
        
        # Track unmarked and marked states
        unmarked_states = [initial_dfa_state]
        dfa_states = {initial_dfa_state}
        dfa_transitions = {}
        
        while unmarked_states:
            current_state_set = unmarked_states.pop(0)
            
            for symbol in self.alphabet:
                # Compute the set of states reachable from current_state_set on symbol
                next_state_set = set()
                for state in current_state_set:
                    key = (state, symbol)
                    if key in self.transitions:
                        next_state_set.update(self.transitions[key])
                
                if next_state_set:
                    next_state_frozen = frozenset(next_state_set)
                    
                    # Add transition
                    dfa_transitions[(current_state_set, symbol)] = {next_state_frozen}
                    
                    # If this is a new state, add it to unmarked
                    if next_state_frozen not in dfa_states:
                        dfa_states.add(next_state_frozen)
                        unmarked_states.append(next_state_frozen)
        
        # Convert frozensets to readable state names
        state_name_map = {}
        for i, state_set in enumerate(sorted(dfa_states, key=lambda x: (len(x), sorted(x)))):
            # Create a readable name from the set of states
            if len(state_set) == 1:
                state_name_map[state_set] = list(state_set)[0]
            else:
                state_name_map[state_set] = "{" + ",".join(sorted(state_set)) + "}"
        
        # Build final DFA
        new_states = set(state_name_map.values())
        new_transitions = {}
        
        for (state_set, symbol), next_sets in dfa_transitions.items():
            state_name = state_name_map[state_set]
            for next_set in next_sets:
                next_name = state_name_map[next_set]
                key = (state_name, symbol)
                if key not in new_transitions:
                    new_transitions[key] = set()
                new_transitions[key].add(next_name)
        
        # Final states are any states that contain an original final state
        new_final_states = set()
        for state_set in dfa_states:
            if state_set.intersection(self.final_states):
                new_final_states.add(state_name_map[state_set])
        
        # Start state
        new_start_state = state_name_map[initial_dfa_state]
        
        return FiniteAutomaton(
            states=new_states,
            alphabet=self.alphabet.copy(),
            transitions=new_transitions,
            start_state=new_start_state,
            final_states=new_final_states
        )
    
    def visualize(self, filename: str = "automaton", format: str = "png") -> str:
        """
        Generate a graphical representation of the automaton using Graphviz.
        Args:
            filename: Name of the output file (without extension)
            format: Output format (png, pdf, svg, etc.)
        Returns:
            str: Path to the generated image file
        """
        try:
            from graphviz import Digraph
        except ImportError:
            return "Error: graphviz library not installed. Run: pip install graphviz"
        
        dot = Digraph(comment='Finite Automaton')
        dot.attr(rankdir='LR')  # Left to right layout
        
        # Add invisible start node with arrow pointing to start state
        dot.node('start', '', shape='none', width='0', height='0')
        dot.edge('start', self.start_state)
        
        # Add states
        for state in self.states:
            if state in self.final_states:
                # Double circle for final states
                dot.node(state, state, shape='doublecircle')
            else:
                dot.node(state, state, shape='circle')
        
        # Add transitions
        # Group transitions with the same source and destination
        edge_labels = {}
        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                key = (state, next_state)
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)
        
        for (src, dst), symbols in edge_labels.items():
            label = ",".join(sorted(symbols))
            dot.edge(src, dst, label=label)
        
        # Render the graph
        output_path = dot.render(filename, format=format, cleanup=True)
        return output_path
    
    def __str__(self) -> str:
        lines = ["Finite Automaton:"]
        lines.append(f"  States: {self.states}")
        lines.append(f"  Alphabet: {self.alphabet}")
        lines.append(f"  Start state: {self.start_state}")
        lines.append(f"  Final states: {self.final_states}")
        lines.append("  Transitions:")
        for (state, symbol), next_states in sorted(self.transitions.items()):
            lines.append(f"    δ({state}, {symbol}) = {next_states}")
        return "\n".join(lines)
