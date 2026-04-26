from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Set, Tuple


Symbol = str
RHS = Tuple[Symbol, ...]
Productions = Dict[Symbol, Set[RHS]]


@dataclass
class Grammar:
    vn: Set[Symbol]
    vt: Set[Symbol]
    productions: Productions
    start_symbol: Symbol

    def clone(self) -> "Grammar":
        return Grammar(
            vn=set(self.vn),
            vt=set(self.vt),
            productions={lhs: set(rhs_set) for lhs, rhs_set in self.productions.items()},
            start_symbol=self.start_symbol,
        )

    @staticmethod
    def from_rules(
        vn: Iterable[Symbol],
        vt: Iterable[Symbol],
        rules: Dict[Symbol, Iterable[str]],
        start_symbol: Symbol,
    ) -> "Grammar":
        parsed: Productions = {}
        for lhs, rhs_list in rules.items():
            parsed[lhs] = set()
            for rhs in rhs_list:
                cleaned = rhs.strip()
                if cleaned in {"", "epsilon", "eps", "e", "ε"}:
                    parsed[lhs].add(tuple())
                else:
                    parsed[lhs].add(tuple(cleaned))

        grammar = Grammar(set(vn), set(vt), parsed, start_symbol)
        grammar._ensure_all_nonterminals_present()
        return grammar

    def _ensure_all_nonterminals_present(self) -> None:
        for nt in self.vn:
            self.productions.setdefault(nt, set())

    def _fresh_nonterminal(self, prefix: str) -> Symbol:
        i = 1
        candidate = f"{prefix}{i}"
        while candidate in self.vn or candidate in self.vt:
            i += 1
            candidate = f"{prefix}{i}"
        return candidate

    def format(self) -> str:
        lines: List[str] = []
        lines.append(f"V_N = {{{', '.join(sorted(self.vn))}}}")
        lines.append(f"V_T = {{{', '.join(sorted(self.vt))}}}")
        lines.append(f"Start symbol: {self.start_symbol}")
        lines.append("Productions:")

        for lhs in sorted(self.productions):
            rhs_variants = sorted(self.productions[lhs], key=self._rhs_sort_key)
            formatted_rhs = [self._rhs_to_str(rhs) for rhs in rhs_variants]
            if formatted_rhs:
                lines.append(f"  {lhs} -> {' | '.join(formatted_rhs)}")
            else:
                lines.append(f"  {lhs} -> <none>")
        return "\n".join(lines)

    @staticmethod
    def _rhs_sort_key(rhs: RHS) -> Tuple[int, str]:
        return (len(rhs), "".join(rhs))

    @staticmethod
    def _rhs_to_str(rhs: RHS) -> str:
        return "ε" if len(rhs) == 0 else "".join(rhs)

    def with_new_start_symbol(self) -> "Grammar":
        grammar = self.clone()

        if all(not lhs == grammar.start_symbol or rhs != (grammar.start_symbol,) for lhs, rhs_set in grammar.productions.items() for rhs in rhs_set):
            if all(grammar.start_symbol not in rhs for rhs_set in grammar.productions.values() for rhs in rhs_set):
                return grammar

        new_start = grammar._fresh_nonterminal("S")
        grammar.vn.add(new_start)
        grammar.productions.setdefault(new_start, set()).add((grammar.start_symbol,))
        grammar.start_symbol = new_start
        grammar._ensure_all_nonterminals_present()
        return grammar

    def nullable_nonterminals(self) -> Set[Symbol]:
        nullable: Set[Symbol] = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhs_set in self.productions.items():
                for rhs in rhs_set:
                    if len(rhs) == 0:
                        if lhs not in nullable:
                            nullable.add(lhs)
                            changed = True
                    elif all(symbol in nullable for symbol in rhs):
                        if lhs not in nullable:
                            nullable.add(lhs)
                            changed = True
        return nullable

    def eliminate_epsilon_productions(self) -> "Grammar":
        grammar = self.clone()
        nullable = grammar.nullable_nonterminals()
        start_is_nullable = grammar.start_symbol in nullable

        new_productions: Productions = {nt: set() for nt in grammar.vn}

        for lhs, rhs_set in grammar.productions.items():
            for rhs in rhs_set:
                if len(rhs) == 0:
                    continue

                nullable_positions = [i for i, symbol in enumerate(rhs) if symbol in nullable]

                all_generated = {rhs}
                for size in range(1, len(nullable_positions) + 1):
                    for selected in combinations(nullable_positions, size):
                        selected_set = set(selected)
                        candidate = tuple(
                            symbol
                            for idx, symbol in enumerate(rhs)
                            if idx not in selected_set
                        )
                        all_generated.add(candidate)

                for candidate in all_generated:
                    if len(candidate) > 0:
                        new_productions[lhs].add(candidate)
                    elif lhs == grammar.start_symbol and start_is_nullable:
                        new_productions[lhs].add(tuple())

        if start_is_nullable:
            new_productions[grammar.start_symbol].add(tuple())

        grammar.productions = new_productions
        grammar._ensure_all_nonterminals_present()
        return grammar

    def eliminate_unit_productions(self) -> "Grammar":
        grammar = self.clone()

        unit_graph: Dict[Symbol, Set[Symbol]] = {nt: set() for nt in grammar.vn}
        for lhs, rhs_set in grammar.productions.items():
            for rhs in rhs_set:
                if len(rhs) == 1 and rhs[0] in grammar.vn:
                    unit_graph[lhs].add(rhs[0])

        unit_closure: Dict[Symbol, Set[Symbol]] = {nt: {nt} for nt in grammar.vn}

        for nt in grammar.vn:
            stack = [nt]
            seen = {nt}
            while stack:
                current = stack.pop()
                for nxt in unit_graph[current]:
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            unit_closure[nt] = seen

        new_productions: Productions = {nt: set() for nt in grammar.vn}
        for lhs in grammar.vn:
            for target in unit_closure[lhs]:
                for rhs in grammar.productions.get(target, set()):
                    if len(rhs) == 1 and rhs[0] in grammar.vn:
                        continue
                    new_productions[lhs].add(rhs)

        grammar.productions = new_productions
        grammar._ensure_all_nonterminals_present()
        return grammar

    def eliminate_non_productive_symbols(self) -> "Grammar":
        grammar = self.clone()

        productive: Set[Symbol] = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhs_set in grammar.productions.items():
                if lhs in productive:
                    continue
                for rhs in rhs_set:
                    if all(sym in grammar.vt or sym in productive for sym in rhs):
                        productive.add(lhs)
                        changed = True
                        break

        new_vn = {nt for nt in grammar.vn if nt in productive}
        new_productions: Productions = {nt: set() for nt in new_vn}

        for lhs in new_vn:
            for rhs in grammar.productions.get(lhs, set()):
                if all(sym in grammar.vt or sym in new_vn for sym in rhs):
                    new_productions[lhs].add(rhs)

        grammar.vn = new_vn
        grammar.productions = new_productions

        if grammar.start_symbol not in grammar.vn:
            raise ValueError("Start symbol became non-productive. Grammar generates no terminal strings.")

        grammar._ensure_all_nonterminals_present()
        return grammar

    def eliminate_inaccessible_symbols(self) -> "Grammar":
        grammar = self.clone()

        reachable: Set[Symbol] = {grammar.start_symbol}
        changed = True

        while changed:
            changed = False
            for lhs in list(reachable):
                for rhs in grammar.productions.get(lhs, set()):
                    for sym in rhs:
                        if sym in grammar.vn and sym not in reachable:
                            reachable.add(sym)
                            changed = True

        new_vn = {nt for nt in grammar.vn if nt in reachable}
        new_productions: Productions = {nt: set() for nt in new_vn}

        for lhs in new_vn:
            for rhs in grammar.productions.get(lhs, set()):
                if all(sym in grammar.vt or sym in new_vn for sym in rhs):
                    new_productions[lhs].add(rhs)

        grammar.vn = new_vn
        grammar.productions = new_productions
        grammar._ensure_all_nonterminals_present()
        return grammar

    def convert_to_cnf(self) -> "Grammar":
        grammar = self.with_new_start_symbol()

        terminal_replacements: Dict[Symbol, Symbol] = {}
        binary_replacements: Dict[Tuple[Symbol, Symbol], Symbol] = {}

        def get_terminal_nonterminal(terminal: Symbol) -> Symbol:
            if terminal in terminal_replacements:
                return terminal_replacements[terminal]
            new_nt = grammar._fresh_nonterminal(f"T{terminal.upper()}")
            grammar.vn.add(new_nt)
            grammar.productions.setdefault(new_nt, set()).add((terminal,))
            updated.setdefault(new_nt, set()).add((terminal,))
            terminal_replacements[terminal] = new_nt
            return new_nt

        def get_binary_nonterminal(left: Symbol, right: Symbol) -> Symbol:
            pair = (left, right)
            if pair in binary_replacements:
                return binary_replacements[pair]

            new_nt = grammar._fresh_nonterminal("X")
            grammar.vn.add(new_nt)
            grammar.productions.setdefault(new_nt, set()).add(pair)
            updated.setdefault(new_nt, set()).add(pair)
            binary_replacements[pair] = new_nt
            return new_nt

        updated: Productions = {nt: set() for nt in grammar.vn}

        for lhs, rhs_set in list(grammar.productions.items()):
            for rhs in rhs_set:
                if len(rhs) == 0:
                    if lhs == grammar.start_symbol:
                        updated[lhs].add(rhs)
                    continue

                if len(rhs) == 1:
                    symbol = rhs[0]
                    if symbol in grammar.vt:
                        updated[lhs].add(rhs)
                    else:
                        updated[lhs].add(rhs)
                    continue

                replaced_rhs: List[Symbol] = []
                for symbol in rhs:
                    if symbol in grammar.vt:
                        replaced_rhs.append(get_terminal_nonterminal(symbol))
                    else:
                        replaced_rhs.append(symbol)

                if len(replaced_rhs) == 2:
                    updated[lhs].add(tuple(replaced_rhs))
                else:
                    symbols = replaced_rhs
                    while len(symbols) > 2:
                        helper = get_binary_nonterminal(symbols[-2], symbols[-1])
                        symbols = symbols[:-2] + [helper]

                    updated.setdefault(lhs, set()).add(tuple(symbols))

        for nt in grammar.vn:
            updated.setdefault(nt, set())

        grammar.productions = updated
        grammar._ensure_all_nonterminals_present()
        return grammar

    def to_cnf(self) -> "Grammar":
        grammar = self.with_new_start_symbol()
        grammar = grammar.eliminate_epsilon_productions()
        grammar = grammar.eliminate_unit_productions()
        grammar = grammar.eliminate_non_productive_symbols()
        grammar = grammar.eliminate_inaccessible_symbols()
        grammar = grammar.convert_to_cnf()
        return grammar

    def is_cnf(self) -> bool:
        for lhs, rhs_set in self.productions.items():
            if lhs not in self.vn:
                return False
            for rhs in rhs_set:
                if len(rhs) == 0:
                    if lhs != self.start_symbol:
                        return False
                    continue
                if len(rhs) == 1:
                    if rhs[0] not in self.vt:
                        return False
                    continue
                if len(rhs) == 2:
                    if rhs[0] not in self.vn or rhs[1] not in self.vn:
                        return False
                    continue
                return False
        return True
