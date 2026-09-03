import sys

from analyzer import ClearTraceAnalyzer
from reporter import Reporter
from fix_engine import FixEngine


def main():

    if len(sys.argv) < 2:

        print()
        print("ClearTrace - Human-Readable Compiler Diagnostics")
        print()
        print("Usage:")
        print("  python src/main.py <source-file>")
        print("  python src/main.py <source-file> --fix")
        print()
        return

    filename = sys.argv[1]
    auto_fix = "--fix" in sys.argv

    analyzer = ClearTraceAnalyzer()
    reporter = Reporter()
    fixer = FixEngine()

    try:

        diagnostics = analyzer.analyze(filename)

        reporter.report(diagnostics)

        if not diagnostics:
            return

        if auto_fix:

            print()
            print("==========================================")
            print("           AUTOMATIC FIX MODE")
            print("==========================================")

            for diagnostic in diagnostics:

                if diagnostic.confidence >= 95:

                    print()
                    print(
                        f"Applying fix for {diagnostic.code}..."
                    )

                    fixed = fixer.apply_fix(
                        filename,
                        diagnostic
                    )

                    if fixed:

                        print("✓ Fix applied.")

                    else:

                        print("⚠ Fix could not be applied.")

            print()
            print("Rechecking source...")

            new_diagnostics = analyzer.analyze(filename)

            if not new_diagnostics:

                print("✓ All detected errors resolved.")

            else:

                print(
                    f"⚠ {len(new_diagnostics)} "
                    f"error(s) remain."
                )

                reporter.report(new_diagnostics)

        else:

            print()
            print(
                "Tip: Run with --fix to apply "
                "high-confidence fixes."
            )

    except FileNotFoundError:

        print(
            f"Error: File '{filename}' not found."
        )

    except Exception as error:

        print(
            f"ClearTrace error: {error}"
        )


if __name__ == "__main__":
    main()