from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple
import random

DEFAULT_MAX_UNBOUNDED_REPEAT = 5

@dataclass
class Node:
    # Base class for all nodes
    def generate(self, rng: random.Random, trace: Optional[List[str]] = None, depth: int = 0) -> str:
        raise NotImplementedError

@dataclass
class Literal(Node):
    # Single character
    value: str
    def generate(self, rng: random.Random, trace: Optional[List[str]] = None, depth: int = 0) -> str:
        if trace:
            trace.append(f"{'  ' * depth}Literal: '{self.value}'")
        return self.value

@dataclass
class Concat(Node):
    # Concatenate multiple parts
    parts: List[Node]
    def generate(self, rng: random.Random, trace: Optional[List[str]] = None, depth: int = 0) -> str:
        if trace:
            trace.append(f"{'  ' * depth}Concat: {len(self.parts)} parts")
        return "".join(part.generate(rng, trace, depth + 1) for part in self.parts)

@dataclass
class Alternate(Node):
    # Choose between alternatives (|)
    choices: List[Node]
    def generate(self, rng: random.Random, trace: Optional[List[str]] = None, depth: int = 0) -> str:
        index = rng.randrange(len(self.choices))
        if trace:
            trace.append(f"{'  ' * depth}Alternate: chose option {index + 1}/{len(self.choices)}")
        return self.choices[index].generate(rng, trace, depth + 1)

@dataclass
class Repeat(Node):
    # Repeat with min/max bounds (*, +, ?, {n}, ^n)
    child: Node
    min_count: int
    max_count: int
    def generate(self, rng: random.Random, trace: Optional[List[str]] = None, depth: int = 0) -> str:
        count = rng.randint(self.min_count, self.max_count)
        if trace:
            trace.append(f"{'  ' * depth}Repeat: [{self.min_count},{self.max_count}] → {count} times")
        return "".join(self.child.generate(rng, trace, depth + 1) for _ in range(count))

class RegexParser:
    # Parse regex patterns into AST
    def __init__(self, pattern: str, max_unbounded_repeat: int = DEFAULT_MAX_UNBOUNDED_REPEAT):
        self.pattern = "".join(pattern.split())
        self.pos = 0
        self.max_unbounded_repeat = max_unbounded_repeat
    
    def parse(self) -> Node:
        # Parse entire pattern
        if not self.pattern:
            raise ValueError("Pattern cannot be empty")
        root = self._parse_alternation()
        if not self._is_end():
            raise ValueError(f"Unexpected '{self._current()}' at position {self.pos}")
        return root
    
    def _parse_alternation(self) -> Node:
        # Handle | (lowest precedence)
        branches = [self._parse_sequence()]
        while self._match("|"):
            branches.append(self._parse_sequence())
        return branches[0] if len(branches) == 1 else Alternate(branches)
    
    def _parse_sequence(self) -> Node:
        # Handle concatenation
        parts = []
        while not self._is_end() and self._current() not in "|)":
            parts.append(self._parse_quantified())
        return Concat(parts) if len(parts) > 1 else (parts[0] if parts else Literal(""))
    
    def _parse_quantified(self) -> Node:
        # Handle quantifiers: *, +, ?, {n}, ^n
        atom = self._parse_atom()
        
        while True:
            if self._match("*"):
                atom = Repeat(atom, 0, self.max_unbounded_repeat)
            elif self._match("+"):
                atom = Repeat(atom, 1, self.max_unbounded_repeat)
            elif self._match("?"):
                atom = Repeat(atom, 0, 1)
            elif self._match("^"):
                n = self._read_number()
                atom = Repeat(atom, n, n)
            elif self._match("{"):
                n = self._read_number()
                if not self._match("}"):
                    raise ValueError(f"Expected '}}' at position {self.pos}")
                atom = Repeat(atom, n, n)
            else:
                break
        return atom
    
    def _parse_atom(self) -> Node:
        # Handle single char or (expression)
        if self._match("("):
            result = self._parse_alternation()
            if not self._match(")"):
                raise ValueError(f"Expected ')' at position {self.pos}")
            return result
        ch = self._current()
        if ch in "|)*+?^{}":
            raise ValueError(f"Unexpected '{ch}' at position {self.pos}")
        
        self._advance()
        return Literal(ch)
    
    # Helper methods
    def _current(self) -> Optional[str]:
        return self.pattern[self.pos] if self.pos < len(self.pattern) else None
    
    def _is_end(self) -> bool:
        return self.pos >= len(self.pattern)
    
    def _advance(self) -> str:
        ch = self.pattern[self.pos]
        self.pos += 1
        return ch
    
    def _match(self, ch: str) -> bool:
        # If current char matches, advance and return True
        if self._current() == ch:
            self._advance()
            return True
        return False
    
    def _read_number(self) -> int:
        # Read digits as integer
        start = self.pos
        while self._current() and self._current().isdigit():
            self._advance()
        if self.pos == start:
            raise ValueError(f"Expected number at position {self.pos}")
        return int(self.pattern[start:self.pos])
    
class RegexWordGenerator:
    def __init__(self, max_unbounded_repeat: int = DEFAULT_MAX_UNBOUNDED_REPEAT, seed: Optional[int] = None):
        self.max_unbounded_repeat = max_unbounded_repeat
        self.rng = random.Random(seed)
    
    def parse(self, regex: str) -> Node:
        # Parse regex into AST
        return RegexParser(regex, self.max_unbounded_repeat).parse()
    
    def generate_word(self, regex: str) -> str:
        # Generate single random word
        ast = self.parse(regex)
        return ast.generate(self.rng)
    
    def generate_words(self, regex: str, count: int = 10, unique: bool = True, max_attempts: int = 5000) -> List[str]:
        # Generate multiple words, optionally unique
        if count <= 0:
            return []
        ast = self.parse(regex)
        if not unique:
            return [ast.generate(self.rng) for _ in range(count)]
        
        # Generate unique words with retry limit
        words = set()
        for _ in range(max_attempts):
            if len(words) >= count:
                break
            words.add(ast.generate(self.rng))
        return sorted(words)
    
    def generate_with_trace(self, regex: str) -> Tuple[str, List[str]]:
        # Generate word and show generation steps
        ast = self.parse(regex)
        trace = [f"Pattern: {regex}", "Process:"]
        result = ast.generate(self.rng, trace=trace, depth=0)
        trace.append(f"Result: {result}")
        return result, trace