import sys
import json

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
        print("  python src/main.py <source-file> --json")
        print()
        return

    filename = sys.argv[1]
    auto_fix = "--fix" in sys.argv
    json_output = "--json" in sys.argv

    analyzer = ClearTraceAnalyzer()
    reporter = Reporter()
    fixer = FixEngine()

    try:

        diagnostics = analyzer.analyze(filename)

        if json_output:
            print(json.dumps({
                "diagnostics": [diagnostic.to_dict() for diagnostic in diagnostics],
                "summary": reporter.summary(diagnostics),
            }, indent=2))
            return

        reporter.report(diagnostics)

        if not diagnostics:
            return

        if auto_fix:
            eligible = [d for d in diagnostics if d.confidence >= 95]
            if not eligible:
                print("\\nNo diagnostics meet the automatic-fix confidence threshold.")
                return

            print()
            print("==========================================")
            print("           AUTOMATIC FIX MODE")
            print("==========================================")
            fixer.create_backup(filename)
            applied = 0
            try:
                for diagnostic in eligible:
                    print()
                    print(f"Proposing fix for {diagnostic.code} at line {diagnostic.line}...")
                    if fixer.apply_fix(filename, diagnostic):
                        applied += 1
                        print("✓ Supported edit applied.")
                    else:
                        print("⚠ No safe supported edit matched; skipped.")

                if not applied:
                    fixer.restore_backup(filename)
                    print("\\nNo changes applied; original file preserved.")
                    return

                print("\\nRechecking source with the native toolchain...")
                new_diagnostics = analyzer.analyze(filename)
                if not new_diagnostics:
                    fixer.discard_backup(filename)
                    print("✓ VERIFIED: native validation passed.")
                    print("  This verifies syntax/validation, not runtime behavior.")
                else:
                    fixer.restore_backup(filename)
                    print(f"✗ Verification failed ({len(new_diagnostics)} diagnostic(s) remain).")
                    print("  Original source restored from backup.")
                    reporter.report(new_diagnostics)
            except Exception:
                fixer.restore_backup(filename)
                raise

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