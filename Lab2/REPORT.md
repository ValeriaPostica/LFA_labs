# Laboratory Work Nr. 2
## Determinism in Finite Automata. Conversion from NDFA to DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata
### Author: Postica Valeria FAF-243

---

## Overview

This laboratory work focuses on understanding determinism in finite automata, implementing conversions between different automaton types, and classifying grammars according to the Chomsky hierarchy.

## Objectives

1. Understand what an automaton is and what it can be used for.
2. Add grammar classification based on Chomsky hierarchy.
3. Implement finite automaton operations:
   - Convert FA to regular grammar
   - Determine if FA is deterministic (DFA) or non-deterministic (NFA)
   - Convert NFA to DFA using subset construction
   - Visualize finite automata (bonus)

## Variant 22 Definition

```
Q = {q0, q1, q2}
Σ = {a, b}
F = {q2}
δ(q0, a) = q0
δ(q1, b) = q1
δ(q1, b) = q2
δ(q0, b) = q1
δ(q1, a) = q0
δ(q2, b) = q1
```

**Note:** The transition `δ(q1, b)` has two possible destinations: `q1` and `q2`. This makes the automaton **non-deterministic**.

## Implementation

### 1. Chomsky Hierarchy Classification

The Chomsky hierarchy classifies grammars into four types:

| Type | Name | Rules |
|------|------|-------|
| 0 | Unrestricted | No restrictions |
| 1 | Context-Sensitive | \|α\| ≤ \|β\| |
| 2 | Context-Free | A → γ (single non-terminal on LHS) |
| 3 | Regular | A → aB or A → a (right-linear) or A → Ba or A → a (left-linear) |

**Implementation in `grammar.py`:**

```python
def classify_chomsky(self):
    # Classify the grammar according to the Chomsky hierarchy (Type 0–3).
    if self._check_type3():
        return "Type 3 — Regular Grammar"
    if self._check_type2():
        return "Type 2 — Context-Free Grammar"
    if self._check_type1():
        return "Type 1 — Context-Sensitive Grammar"
    return "Type 0 — Unrestricted Grammar"

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

    # Either right or left grammar (not both)
    if right_linear and left_linear:
        return False
    return True

def _check_type2(self):
    # Context-free grammar: LHS must be a single non-terminal
    for lhs in self.p:
        if lhs not in self.vn:
            return False
    return True

def _check_type1(self):
    # Context-sensitive grammar: |LHS| <= |RHS| and no epsilon productions
    for lhs, rhs_options in self.p.items():
        for rhs in rhs_options:
            if rhs in ('', 'ε'):
                return False
            if len(lhs) > len(rhs):
                return False
    return True
```

### 2. FA to Regular Grammar Conversion

The algorithm converts each transition to a production rule:
- For `δ(A, a) = B`: Create production `A → aB`
- If `B` is a final state: Also create `A → a`

**Implementation in `finite_automaton.py`:**

```python
def to_regular_grammar(self):
    productions = {}
    
    for (state, symbol), next_states in self.transitions.items():
        for next_state in next_states:
            # If next state is final, add A → a
            if next_state in self.final_states:
                productions[state].append(symbol)
            
            # Add A → aB (continues to next state)
            production = symbol + next_state
            productions[state].append(production)
    
    return Grammar(vn, vt, productions, self.start_state)
```

### 3. Determinism Check

A finite automaton is **deterministic** if and only if:
1. For each state and input symbol, there is **at most one** transition
2. No epsilon (ε) transitions exist

**Implementation:**

```python
def is_deterministic(self) -> bool:
    for (state, symbol), next_states in self.transitions.items():
        if len(next_states) > 1:
            return False
    return True
```

For Variant 22, the automaton is **non-deterministic** because:
- `δ(q1, b) = {q1, q2}` — multiple transitions from the same state on the same input symbol

### 4. NFA to DFA Conversion (Subset Construction)

The subset construction algorithm creates a DFA where:
- Each DFA state represents a **set** of NFA states
- Initial DFA state = {initial NFA state}
- For each DFA state and symbol, compute the union of all reachable NFA states
- A DFA state is final if it contains any NFA final state

**Algorithm:**

```
1. Start with initial_state = {q0}
2. While there are unmarked DFA states:
   a. For each unmarked state S and symbol a:
      - Compute T = ∪{δ(s, a) | s ∈ S}
      - If T is new, add to DFA states
      - Add transition (S, a) → T
   b. Mark S as processed
3. Final DFA states = states containing any NFA final state
```

**Implementation:**

```python
def to_dfa(self) -> 'FiniteAutomaton':
    initial_dfa_state = frozenset([self.start_state])
    unmarked_states = [initial_dfa_state]
    dfa_states = {initial_dfa_state}
    dfa_transitions = {}
    
    while unmarked_states:
        current = unmarked_states.pop(0)
        
        for symbol in self.alphabet:
            next_set = set()
            for state in current:
                if (state, symbol) in self.transitions:
                    next_set.update(self.transitions[(state, symbol)])
            
            if next_set:
                next_frozen = frozenset(next_set)
                dfa_transitions[(current, symbol)] = {next_frozen}
                
                if next_frozen not in dfa_states:
                    dfa_states.add(next_frozen)
                    unmarked_states.append(next_frozen)
    
    # Build final DFA with proper state naming...
```

### 5. Visualization (Bonus)

Using the Graphviz library to create visual representations:

```python
def visualize(self, filename: str = "automaton"):
    from graphviz import Digraph
    
    dot = Digraph()
    dot.attr(rankdir='LR')
    
    # Add states (double circle for final states)
    for state in self.states:
        shape = 'doublecircle' if state in self.final_states else 'circle'
        dot.node(state, state, shape=shape)
    
    # Add transitions
    for (state, symbol), next_states in self.transitions.items():
        for next_state in next_states:
            dot.edge(state, next_state, label=symbol)
    
    dot.render(filename, format='png', cleanup=True)
```

## Results

### Variant 22 NFA Analysis

**Original NFA:**
```
States Q: {q0, q1, q2}
Alphabet Σ: {a, b}
Start state: q0
Final states F: {q2}
Transitions:
  δ(q0, a) = {q0}
  δ(q0, b) = {q1}
  δ(q1, a) = {q0}
  δ(q1, b) = {q1, q2}  ← Non-deterministic!
  δ(q2, b) = {q1}
```

**Is Deterministic?** NO
- Reason: `δ(q1, b) = {q1, q2}` has multiple transitions

### Converted DFA

After applying subset construction:

```
States Q: {q0, q1, {q1,q2}}
Alphabet Σ: {a, b}
Start state: q0
Final states F: {{q1,q2}}
Transitions:
  δ(q0, a) = {q0}
  δ(q0, b) = {q1}
  δ(q1, a) = {q0}
  δ(q1, b) = {{q1,q2}}
  δ({q1,q2}, a) = {q0}
  δ({q1,q2}, b) = {{q1,q2}}
```

**Is Deterministic?** YES

### Converted Regular Grammar

```
Grammar:
  VN (Non-terminals): {q0, q1, q2}
  VT (Terminals): {a, b}
  Start symbol: q0
  Productions P:
    q0 → aq0
    q0 → bq1
    q1 → aq0
    q1 → b      (because q2 is final)
    q1 → bq2
    q1 → bq1
    q2 → bq1
```

**Classification:** Type 3 — Regular Grammar

### String Acceptance Verification

| String | NFA Result | DFA Result | Match |
|--------|------------|------------|-------|
| ab     | REJECTED   | REJECTED   | ✓     |
| abb    | ACCEPTED   | ACCEPTED   | ✓     |
| bb     | ACCEPTED   | ACCEPTED   | ✓     |
| abbb   | ACCEPTED   | ACCEPTED   | ✓     |
| aabb   | ACCEPTED   | ACCEPTED   | ✓     |
| b      | REJECTED   | REJECTED   | ✓     |
| bbb    | ACCEPTED   | ACCEPTED   | ✓     |
| a      | REJECTED   | REJECTED   | ✓     |
| ba     | REJECTED   | REJECTED   | ✓     |
| bba    | REJECTED   | REJECTED   | ✓     |
| (empty)| REJECTED   | REJECTED   | ✓     |

The NFA and DFA accept the **same language**, confirming correct conversion.

## Conclusions

1. **Chomsky Hierarchy Classification**: Implemented a method to classify grammars into Types 0-3 based on their production rules. The grammar from Variant 22 converts to a Type 3 (Regular Grammar).

2. **Determinism Analysis**: The Variant 22 automaton is **non-deterministic** because the transition `δ(q1, b)` leads to multiple states `{q1, q2}`.

3. **NFA to DFA Conversion**: Successfully implemented the subset construction algorithm. The resulting DFA has a composite state `{q1, q2}` that represents being in either state of the original NFA.

4. **Equivalence Verification**: Both the NFA and DFA accept exactly the same language, as verified by testing multiple strings.

5. **Visualization**: Implemented graphical representation using Graphviz (optional feature).

## References

1. Formal Languages & Finite Automata, Technical University of Moldova
2. Graphviz documentation - https://graphviz.org/download/
