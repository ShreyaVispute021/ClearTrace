from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from diagnostics import DiagnosticEngine


def read_source_code():

    print()
    print("========================================")
    print("          CLEARTRACE COMPILER")
    print("     Human-Readable Diagnostics v0.1")
    print("========================================")
    print()
    print("Enter your code.")
    print("Type END on a new line when finished.")
    print()

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    return "\n".join(lines)


def compile_source(source):

    # =========================
    # LEXICAL ANALYSIS
    # =========================

    try:

        lexer = Lexer(source)
        tokens = lexer.tokenize()

    except Exception as error:

        print()
        print("Lexer error:")
        print(error)
        return


    # =========================
    # SYNTAX ANALYSIS
    # =========================

    parser = Parser(tokens)
    ast = parser.parse()

    syntax_errors = parser.errors


    # =========================
    # SEMANTIC ANALYSIS
    # =========================

    analyzer = SemanticAnalyzer()
    semantic_errors = analyzer.analyze(ast)


    # =========================
    # COMBINE ERRORS
    # =========================

    errors = syntax_errors + semantic_errors


    # =========================
    # DIAGNOSTICS
    # =========================

    diagnostics = DiagnosticEngine(source)


    print()
    print("----------------------------------------")

    if not errors:

        print("✓ Compilation successful")
        print("  No errors found.")

    else:

        print(f"✗ Found {len(errors)} error(s)")
        print()

        for error in errors:
            print(diagnostics.report(error))


def main():

    source = read_source_code()

    if not source.strip():

        print()
        print("No source code entered.")
        return

    compile_source(source)


if __name__ == "__main__":
    main()