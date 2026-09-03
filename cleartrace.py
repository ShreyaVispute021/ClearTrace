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


def print_banner():

    print()
    print("╔════════════════════════════════════════════╗")
    print("║              CLEARTRACE                    ║")
    print("║     Universal Diagnostic Analyzer          ║")
    print("╚════════════════════════════════════════════╝")
    print()


def run_analysis(filename, auto_fix=False):

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
            print("╔════════════════════════════════════════════╗")
            print("║           AUTOMATIC FIX MODE               ║")
            print("╚════════════════════════════════════════════╝")

            for diagnostic in diagnostics:

                if diagnostic.confidence >= 95:

                    print()
                    print(
                        f"Applying {diagnostic.code}..."
                    )

                    fixed = fixer.apply_fix(
                        filename,
                        diagnostic
                    )

                    if fixed:
                        print("✓ Fix applied.")
                    else:
                        print("⚠ Fix could not be applied.")

                else:

                    print()
                    print(
                        f"⚠ Skipping {diagnostic.code}"
                    )
                    print(
                        f"  Confidence: "
                        f"{diagnostic.confidence}%"
                    )

            print()
            print("Rechecking source...")

            remaining = analyzer.analyze(filename)

            if not remaining:

                print()
                print("✓ VERIFIED")
                print("  All detected errors were resolved.")

            else:

                print()
                print(
                    f"⚠ {len(remaining)} "
                    f"error(s) remain."
                )

        else:

            print()
            print(
                "Tip: Use --fix for automatic "
                "high-confidence corrections."
            )

    except FileNotFoundError:

        print(
            f"✗ File not found: {filename}"
        )

    except Exception as error:

        print(
            f"✗ ClearTrace error: {error}"
        )


def interactive_mode():

    print_banner()

    filename = input(
        "Enter source file: "
    ).strip()

    if not filename:
        print("No file specified.")
        return

    if not os.path.exists(filename):

        print()
        print(
            f"✗ File not found: {filename}"
        )
        return

    print()

    analyzer = ClearTraceAnalyzer()

    try:

        language = analyzer.detector.detect(
            filename
        )

        print(
            f"Language detected: {language}"
        )

        print()
        print("Analyzing...")
        print()

        diagnostics = analyzer.analyze(
            filename
        )

        Reporter().report(diagnostics)

        if diagnostics:

            print()
            choice = input(
                "Apply high-confidence fixes? [y/N]: "
            ).strip().lower()

            if choice == "y":

                run_analysis(
                    filename,
                    auto_fix=True
                )

    except Exception as error:

        print(
            f"✗ ClearTrace error: {error}"
        )


def main():

    if len(sys.argv) == 1:

        interactive_mode()
        return

    if "--demo" in sys.argv:

        print_banner()

        demo_files = [
            "demo.py",
            "test.cpp",
            "Main.java",
            "test.js"
        ]

        analyzer = ClearTraceAnalyzer()
        reporter = Reporter()

        print("Running ClearTrace multi-language demonstration...")
        print()

        for filename in demo_files:

            print()
            print("════════════════════════════════════════════")
            print(f"Analyzing: {filename}")
            print("════════════════════════════════════════════")

            if not os.path.exists(filename):

                print(f"⚠ File not found: {filename}")
                continue

            try:

                language = analyzer.detector.detect(filename)

                print(f"Language detected: {language}")

                diagnostics = analyzer.analyze(filename)

                reporter.report(diagnostics)

            except Exception as error:

                print(f"✗ Analysis failed: {error}")

        print()
        print("════════════════════════════════════════════")
        print("        MULTI-LANGUAGE DEMO COMPLETE")
        print("════════════════════════════════════════════")
        print()

        return

    filename = sys.argv[1]
    auto_fix = "--fix" in sys.argv

    print_banner()

    run_analysis(
        filename,
        auto_fix
    )


if __name__ == "__main__":
    main()