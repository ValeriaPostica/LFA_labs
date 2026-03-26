from grammar import Grammar


def build_variant_22_grammar() -> Grammar:
    vn = {"S", "A", "B", "C", "E"}
    vt = {"a", "b"}

    rules = {
        "S": ["aB", "AC"],
        "A": ["a", "ACSC", "BC"],
        "B": ["b", "aA"],
        "C": ["ε", "BA"],
        "E": ["bB"],
    }

    return Grammar.from_rules(vn=vn, vt=vt, rules=rules, start_symbol="S")


def print_stage(title: str, grammar: Grammar) -> None:
    print(f"\nStage: {title}")
    print(grammar.format())


def run_normalization(grammar: Grammar, title: str) -> None:
    print(f"\nCNF NORMALIZATION - {title}\n")
    
    print_stage("Initial Grammar", grammar)

    g0 = grammar.with_new_start_symbol()
    print_stage("1) Added New Start Symbol", g0)

    g1 = g0.eliminate_epsilon_productions()
    print_stage("2) After Eliminating epsilon-productions", g1)

    g2 = g1.eliminate_unit_productions()
    print_stage("3) After Eliminating Unit Productions", g2)

    g3 = g2.eliminate_non_productive_symbols()
    print_stage("4) After Eliminating Non-Productive Symbols", g3)

    g4 = g3.eliminate_inaccessible_symbols()
    print_stage("5) After Eliminating Inaccessible Symbols", g4)

    g5 = g4.convert_to_cnf()
    print_stage("6) Final CNF Grammar", g5)

    print("\nCNF validation:", "PASSED ✓" if g5.is_cnf() else "FAILED ✗")


def main() -> None:
    grammar = build_variant_22_grammar()
    run_normalization(grammar, "Variant 22")


if __name__ == "__main__":
    main()
