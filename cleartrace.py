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
        if not auto_fix:
            print("\nTip: Use --fix to attempt only explicitly supported high-confidence fixes.")
            return

        eligible = [d for d in diagnostics if d.confidence >= 95]
        if not eligible:
            print("\nNo diagnostics meet the automatic-fix confidence threshold.")
            return

        print("\nAUTOMATIC FIX MODE")
        # One backup protects the original file if the repair does not verify.
        fixer.create_backup(filename)
        applied = 0
        try:
            for diagnostic in eligible:
                print(f"\nProposing fix for {diagnostic.code} at line {diagnostic.line}...")
                if fixer.apply_fix(filename, diagnostic):
                    applied += 1
                    print("  Supported edit applied.")
                else:
                    print("  No safe, supported edit matched; skipped.")

            if applied == 0:
                fixer.restore_backup(filename)
                print("\nNo changes applied; original file preserved.")
                return

            print("\nRechecking source with the native toolchain...")
            remaining = analyzer.analyze(filename)
            if not remaining:
                fixer.discard_backup(filename)
                print("\n✓ VERIFIED: the native validation check passed.")
                print("  Note: this verifies the compiler/interpreter check, not runtime behavior.")
            else:
                fixer.restore_backup(filename)
                print(f"\n✗ Verification failed ({len(remaining)} diagnostic(s) remain).")
                print("  Original source restored from backup.")
                reporter.report(remaining)
        except Exception:
            fixer.restore_backup(filename)
            raise
    except FileNotFoundError:
        print(f"✗ File not found: {filename}")
    except Exception as error:
        print(f"✗ ClearTrace error: {error}")


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