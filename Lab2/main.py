from grammar import Grammar
from finite_automaton import FiniteAutomaton

def main():
    print("LABORATORY WORK 2")
    print("Topic: Determinism in Finite Automata. Conversion from NDFA to DFA. Chomsky Hierarchy.")

    print("\nTASK 3: Finite Automaton Operations (Variant 22)")
    
    # Create the FA from Variant 22
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    final_states = {'q2'}
    start_state = 'q0'
    
    # Build transitions - note that δ(q1, b) has two targets: q1 and q2
    transitions = {
        ('q0', 'a'): {'q0'},
        ('q0', 'b'): {'q1'},
        ('q1', 'a'): {'q0'},
        ('q1', 'b'): {'q1', 'q2'},  # Non-deterministic transition!
        ('q2', 'b'): {'q1'}
    }
    
    nfa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
    print(f"\n{nfa}")
    
    print("\nTASK 3b: Check if Automaton is Deterministic")
    
    is_dfa = nfa.is_deterministic()
    print(f"\nIs the automaton deterministic? {is_dfa}")
    
    reasons = []
    for (state, symbol), next_states in transitions.items():
        if len(next_states) > 1:
            reasons.append(f"δ({state}, {symbol}) = {next_states} (multiple transitions)")
    
    if reasons:
        print("Non-deterministic because:\n  " + "\n  ".join(reasons))
    else: 
        print("The automaton is deterministic.")
    
    print("\nTASK 3a: Convert Finite Automaton to Regular Grammar")
    
    regular_grammar_from_fa = nfa.to_regular_grammar()
    print("\nConverted Regular Grammar:")
    print(regular_grammar_from_fa)
    print(f"\nClassification: {regular_grammar_from_fa.classify_chomsky()}")
    
    print("\nTASK 3c: Convert NFA to DFA (Subset Construction)")
    
    print("\nApplying subset construction algorithm...")
    dfa = nfa.to_dfa()
    
    print("\nResulting DFA:")
    print(dfa)
    
    print(f"\nIs the converted automaton deterministic? {dfa.is_deterministic()}")
    
    print("\nVERIFICATION: Test String Acceptance (NFA vs DFA)")
    
    test_strings = [
        "ab",           # q0 ->a q0 ->b q1 (not accepted, q1 not final)
        "abb",          # q0 ->a q0 ->b q1 ->b {q1,q2} (accepted, q2 is final)
        "bb",           # q0 ->b q1 ->b {q1,q2} (accepted)
        "abbb",         # accepted (can reach q2)
        "aabb",         # q0 ->a q0 ->a q0 ->b q1 ->b {q1,q2} (accepted)
        "b",            # q0 ->b q1 (not accepted)
        "bbb",          # accepted (q0 -> q1 -> {q1,q2} -> q1 at some point hits q2)
        "a",            # q0 ->a q0 (not accepted)
        "ba",           # q0 ->b q1 ->a q0 (not accepted)
        "bba",          # q0 ->b q1 ->b {q1,q2} ->a ? (q2 has no 'a' transition)
        "",             # empty string (not accepted, q0 is not final)
    ]
    
    print("\n{:<15} {:<15} {:<15} {:<10}".format("String", "NFA Result", "DFA Result", "Match?"))
    
    for test_string in test_strings:
        nfa_result = nfa.string_belongs_to_language(test_string)
        dfa_result = dfa.string_belongs_to_language(test_string)
        match = "✓" if nfa_result == dfa_result else "✗"
        
        display_string = test_string if test_string else "(empty)"
        nfa_status = "ACCEPTED" if nfa_result else "REJECTED"
        dfa_status = "ACCEPTED" if dfa_result else "REJECTED"
        
        print(f"{display_string:<15} {nfa_status:<15} {dfa_status:<15} {match}")
    
    print("\nTASK 3d (BONUS): Graphical Representation")
    
    try:
        print("\nGenerating NFA visualization...")
        nfa_path = nfa.visualize("variant22_nfa")
        print(f"NFA diagram saved to: {nfa_path}")
        
        print("\nGenerating DFA visualization...")
        dfa_path = dfa.visualize("variant22_dfa")
        print(f"DFA diagram saved to: {dfa_path}")
    except Exception as e:
        print(f"\nNote: Could not generate visualizations.")
        print(f"To enable visualizations, install graphviz:")
        print(f"  1. pip install graphviz")
        print(f"  2. Install Graphviz system package from https://graphviz.org/download/")
        print(f"\nError details: {e}")

if __name__ == "__main__":
    main()
