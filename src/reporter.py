class Reporter:

    def report(self, diagnostics):

        print()
        print("╔══════════════════════════════════════════╗")
        print("║             CLEARTRACE                   ║")
        print("║   Human-Readable Diagnostics             ║")
        print("╚══════════════════════════════════════════╝")

        if not diagnostics:

            print()
            print("✓ No errors found.")
            print("  Compilation / validation successful.")
            print()
            return

        for diagnostic in diagnostics:

            print()
            print("──────────────────────────────────────────")
            print(f"Language: {diagnostic.language}")
            print(f"Severity: {diagnostic.severity}")
            print(f"Category: {diagnostic.category}")
            print(f"Code:     {diagnostic.code}")
            print()

            print(
                f"  {diagnostic.line} │ "
                f"{diagnostic.source_line}"
            )

            print(
                f"    │ "
                f"{'^' * max(1, diagnostic.column)}"
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
            print(f"Confidence: {diagnostic.confidence}%")

        print()
        print("──────────────────────────────────────────")
        print(f"Total errors: {len(diagnostics)}")
        print()