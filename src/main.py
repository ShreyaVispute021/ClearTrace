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

        print()
        print(f"✗ Found {len(errors)} error(s)")
        print()

        # Display detailed diagnostics
        for error in errors:
            print(diagnostics.report(error))

        # --------------------------------
        # Diagnostic Summary
        # --------------------------------

        print("========================================")
        print("           DIAGNOSTIC SUMMARY")
        print("========================================")
        print()

        print(f"Errors: {len(errors)}")
        print()

        counts = {}

        for error in errors:

            error_type = error["type"]

            if error_type not in counts:
                counts[error_type] = 0

            counts[error_type] += 1

        names = {
            "MISSING_SEMICOLON": "Missing semicolon",
            "UNDECLARED_VARIABLE": "Undeclared variable",
            "DUPLICATE_DECLARATION": "Duplicate declaration",
            "TYPE_MISMATCH": "Type mismatch",
            "UNEXPECTED_TOKEN": "Unexpected token"
        }

        codes = {
            "MISSING_SEMICOLON": "E001",
            "UNDECLARED_VARIABLE": "E002",
            "DUPLICATE_DECLARATION": "E003",
            "TYPE_MISMATCH": "E004",
            "UNEXPECTED_TOKEN": "E005"
        }

        for error_type, count in counts.items():

            print(
                f"{codes.get(error_type, 'E???')}  "
                f"{names.get(error_type, error_type)}"
                f"  {count}"
            )


def main():

    source = read_source_code()

    if not source.strip():

        print()
        print("No source code entered.")
        return

    compile_source(source)


if __name__ == "__main__":
    main()