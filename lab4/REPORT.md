# Laboratory Work Nr. 4
## Regular Expressions

### Course: Formal Languages & Finite Automata
### Author: Postica Valeria FAF-243

---

## Overview

This laboratory work focuses on understanding regular expressions and implementing a dynamic generator of valid words based on regex patterns. The implemented program parses regex expressions into an Abstract Syntax Tree (AST) and generates words by traversing this structure, without hardcoding each pattern.

For this submission, the assigned set is **Variant 2**.

## Objectives

1. Explain what regular expressions are and what they are used for.
2. Dynamically interpret and generate valid words from regex input.
3. Limit unbounded repetition operators to 5 occurrences.
4. Implement bonus functionality: show the sequence of regex processing steps.

## Theoretical Background

### What Is a Regular Expression?

A **regular expression (regex)** is a formal notation for describing sets of strings over an alphabet. Regex is used in compilers (lexical analysis), validators, search engines, and text processing tools.

### Operators Used

| Operator | Meaning | Example |
|------|------|------|
| Concatenation | Sequence of symbols | `ab` |
| `|` | Alternation (choice) | `(a|b)` |
| `*` | Zero or more repetitions | `a*` |
| `+` | One or more repetitions | `a+` |
| `?` | Optional (zero or one) | `a?` |
| `^n` | Exact repetition (custom notation from assignment) | `(ab)^3` |
| `{n}` | Exact repetition (also supported) | `(ab){3}` |

### Why Dynamic Interpretation?

The assignment explicitly requires interpreting regexes dynamically and not hardcoding generation logic for each individual expression. To satisfy this, I built a generic parser and generator that work for all provided variants and any custom regex using the supported operators.

## Implementation

### Project Structure

- `main.py` - CLI, variant selection, execution, interactive testing.
- `regex_generator.py` - parser, AST node definitions, generation logic, and processing trace.
- `task (3).md` - assignment statement.

### 1. AST Design

I implemented the following AST node classes:

- `Literal(value)` - stores one symbol.
- `Concat(parts)` - concatenates child nodes.
- `Alternate(choices)` - selects one branch from alternatives.
- `Repeat(child, min_count, max_count)` - repeats a child node in a specified range.

Each node has:

```python
def generate(self, rng, trace=None, depth=0) -> str
```

This method both produces output and optionally records processing steps.

### 2. Parser (Recursive Descent)

The parser supports:

- Grouping: `(...)`
- Alternation: `|`
- Concatenation: implicit
- Quantifiers: `*`, `+`, `?`, `^n`, `{n}`

Parsing hierarchy:

```text
expression -> concatenation ('|' concatenation)*
concatenation -> quantified_atom+
quantified_atom -> atom quantifier*
atom -> '(' expression ')' | literal
```

This hierarchy correctly models precedence:

1. Quantifiers
2. Concatenation
3. Alternation

### 3. Repetition Limit Rule

To avoid very long strings, unbounded operators are constrained:

- `*` becomes repeat interval `[0, 5]`
- `+` becomes repeat interval `[1, 5]`

This limit is controlled by `max_unbounded_repeat=5`.

### 4. Bonus Functionality: Processing Sequence

The method `generate_with_trace(regex)` returns:

1. A generated valid word.
2. Ordered trace steps (what was processed and in what order).

Typical trace entries:

- `Concat with 4 part(s)`
- `Alternate: pick branch 2/3`
- `Repeat in [1, 5] -> chosen 4`
- `Literal 'Q'`

This satisfies the bonus requirement of showing first, second, and subsequent processing steps.

## Variant 2 Definition

The implemented assignment variant is:

1. `M?N^2(O|P)^3Q*R+`
2. `(X|Y|Z){3}8+(9|0)` (equivalent to handwritten `(X|Y|Z)^3 8+(9|0)`)
3. `(H|I)(J|K)L*N?`

Program flow:

1. Show the assigned Variant 2 regex set.
2. Generate valid words for each Variant 2 regex.
3. Print one processing trace example for each regex.
4. Enter interactive single-regex mode.

## Results

For each regex, the output contains:

1. Regex text.
2. A generated set of valid words.
3. A detailed processing sequence.

Example output structure:

```text
Regex 1: O(P|Q|R)+2(3|4)
Generated valid words:
{OPP23, ORQ24, ...}
Processing sequence example:
  Pattern: O(P|Q|R)+2(3|4)
  Processing sequence:
  ...
  Result: OQQQ24
```

All generated words conform to the expression semantics and respect the repetition cap.

## Faced Difficulties and Solutions

1. **Potential infinite growth due to `*` and `+`.**
   - Solved by introducing the global cap (5 repetitions).

2. **Need for transparent generation logic (bonus).**
   - Solved by passing a `trace` collector through AST traversal.

3. **Correct precedence in regex parsing.**
   - Solved with recursive-descent layers: expression -> concatenation -> quantified atom -> atom.

## Conclusion

This laboratory work achieved both the theoretical and practical objectives of the assignment and resulted in a reusable regex-generation tool, not just a one-time script for a single variant.

From the theoretical side, I clarified what regular expressions represent in formal language theory and how they are applied in real systems such as lexical analyzers, text validators, and pattern matching utilities. This connection between theory and implementation was important because the goal was not only to generate strings, but to understand why such generation is possible through formal operators like concatenation, alternation, and repetition.

From the implementation side, the most important result is that the solution is fully dynamic at algorithm level. The program does not contain hardcoded generation rules for each of the three Variant 2 expressions. Instead, it parses input patterns with a recursive-descent parser, builds an AST, and generates valid words by traversing that structure. Because of this architecture, one generator is sufficient for all three required expressions.

The requirement to avoid extremely long outputs was addressed correctly by constraining unbounded quantifiers (`*` and `+`) to a maximum of 5 repetitions. This keeps generation finite and predictable while preserving operator semantics.

The bonus task was also completed through `generate_with_trace(...)`, which exposes the internal sequence of processing steps. This makes the program easier to explain during presentation and easier to debug, because one can see exactly which branches and repetition counts were chosen.

I also encountered and solved practical issues related to notation ambiguity from handwritten expressions (for example, constructs that mix exponent-style repetition with trailing literal digits). Supporting both `^n` and `{n}` gave a robust and explicit way to represent exact repetition in code.

Overall, the final solution is modular, scalable, and presentation-ready. It satisfies all mandatory requirements, implements the bonus functionality, and can be extended in future labs with additional regex features (for example ranges, escaped characters, or bounded intervals like `{m,n}`) without changing the fundamental design.
