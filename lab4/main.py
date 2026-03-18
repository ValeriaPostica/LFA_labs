from typing import List
from regex_generator import RegexWordGenerator

VARIANT_2_REGEXES: List[str] = [
    "M?N^2(O|P)^3Q*R+",
    "(X|Y|Z){3}8+(9|0)",
    "(H|I)(J|K)L*N?",
]

def print_header() -> None:
    print("LABORATORY WORK 4")
    print("Assigned Variant: 2\n")

def print_variant_2_definition() -> None:
    print("Variant 2 regex set:")
    for index, regex in enumerate(VARIANT_2_REGEXES, 1):
        print(f"  {index}. {regex}")
    print()

def run_for_regexes(generator: RegexWordGenerator, regexes: List[str], words_per_regex: int = 12) -> None:
    for index, regex in enumerate(regexes, 1):
        print(f"Regex {index}: {regex}")

        words = generator.generate_words(regex, count=words_per_regex, unique=True)
        print("Generated valid words:")
        print("{" + ", ".join(words) + "}")

        _, trace = generator.generate_with_trace(regex)
        print("Processing sequence example:")
        for step in trace:
            print(f"  {step}")
        print()

def interactive_mode(generator: RegexWordGenerator) -> None:
    print("INTERACTIVE SINGLE-REGEX MODE")
    print("Type any regex using (), |, *, +, ?, ^n, {n}")
    print("Type 'quit' to exit")
    while True:
        raw = input("\nregex> ").strip()
        if raw.lower() in {"quit", "q", "exit"}:
            print("Goodbye!")
            break
        if not raw:
            continue
        try:
            words = generator.generate_words(raw, count=10, unique=True)
            print("Generated valid words:")
            print("{" + ", ".join(words) + "}")

            _, trace = generator.generate_with_trace(raw)
            print("Processing sequence:")
            for step in trace:
                print(f"  {step}")
        except ValueError as exc:
            print(f"Error: {exc}")

def main() -> None:
    print_header()
    print_variant_2_definition()
    generator = RegexWordGenerator(max_unbounded_repeat=5, seed=42)
    run_for_regexes(generator, VARIANT_2_REGEXES, words_per_regex=12)
    interactive_mode(generator)

if __name__ == "__main__":
    main()