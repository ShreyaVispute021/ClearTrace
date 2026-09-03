import sys
import os

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)

from analyzer import ClearTraceAnalyzer
from reporter import Reporter
from fix_engine import FixEngine


def main():

    if len(sys.argv) < 2:

        print()
        print("========================================")
        print("          CLEARTRACE")
        print("   Universal Diagnostic Analyzer")
        print("========================================")
        print()
        print("Usage:")
        print("  python cleartrace.py <source-file>")
        print("  python cleartrace.py <source-file> --fix")
        print()
        print("Supported languages:")
        print("  Python (.py)")
        print("  C++    (.cpp, .cc, .cxx)")
        print("  Java   (.java)")
        print("  JavaScript (.js)")
        print()

        return

    filename = sys.argv[1]
    auto_fix = "--fix" in sys.argv

    if not os.path.exists(filename):

        print(f"Error: File '{filename}' not found.")
        return

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
            print("          AUTOMATIC FIX MODE")
            print("==========================================")

            for diagnostic in diagnostics:

                if diagnostic.confidence >= 95:

                    print()
                    print(
                        f"Applying fix for "
                        f"{diagnostic.code}..."
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

        else:

            print()
            print(
                "Tip: Use --fix to apply "
                "high-confidence fixes."
            )

    except Exception as error:

        print()
        print(f"ClearTrace error: {error}")


if __name__ == "__main__":
    main()