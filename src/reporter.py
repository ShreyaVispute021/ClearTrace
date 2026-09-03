class Reporter:

    def report(self, diagnostics):

        print()
        print("╔══════════════════════════════════════════╗")
        print("║             CLEARTRACE                   ║")
        print("║   Universal Diagnostic Analyzer          ║")
        print("╚══════════════════════════════════════════╝")

        if not diagnostics:

            print()
            print("✓ No errors found.")
            print("  Compilation / validation successful.")
            print()

            return

        print()
        print(f"Detected {len(diagnostics)} error(s).")

        for index, diagnostic in enumerate(
            diagnostics,
            start=1
        ):

            print()
            print("──────────────────────────────────────────")
            print(f"Error #{index}")
            print(f"Language: {diagnostic.language}")
            print(f"Severity: {diagnostic.severity}")
            print(f"Category: {diagnostic.category}")
            print(f"Code:     {diagnostic.code}")
            print()

            print(
                f"  {diagnostic.line} │ "
                f"{diagnostic.source_line}"
            )

            spaces = max(
                0,
                diagnostic.column - 1
            )

            print(
                f"    │ "
                f"{' ' * spaces}^"
            )

            print()
            print("What happened?")
            print(f"  {diagnostic.message}")

            print()
            print("Why did this happen?")
            print(f"  {diagnostic.explanation}")

            print()
            print("Suggested fix:")
            print(f"  {diagnostic.suggestion}")

            print()
            print(
                f"Confidence: "
                f"{diagnostic.confidence}%"
            )

        print()
        print("──────────────────────────────────────────")

        if len(diagnostics) > 1:

            print()
            print("ROOT-CAUSE ANALYSIS")

            first = min(
                diagnostics,
                key=lambda d: (
                    d.line,
                    d.column
                )
            )

            print(
                f"  Earliest detected issue: "
                f"{first.code}"
            )

            print(
                f"  Line {first.line}: "
                f"{first.message}"
            )

            print()
            print(
                "  Recommendation:"
            )

            print(
                "  Fix the earliest error first, "
                "then re-run ClearTrace."
            )

        print()