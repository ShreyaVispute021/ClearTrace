from collections import Counter
from error_classifier import ErrorClassifier


class Reporter:

    @staticmethod
    def summary(diagnostics):
        """Return stable counts for text and machine-readable reports."""
        by_code = Counter(d.code for d in diagnostics)
        by_category = Counter(d.category for d in diagnostics)
        return {
            "total": len(diagnostics),
            "errors": sum(1 for d in diagnostics if d.severity.upper() == "ERROR"),
            "warnings": sum(1 for d in diagnostics if d.severity.upper() == "WARNING"),
            "by_code": dict(sorted(by_code.items())),
            "by_category": dict(sorted(by_category.items())),
        }


    def report(self, diagnostics):
        classifier = ErrorClassifier()
        
        if not diagnostics:

            print()
            print("✓ No errors found.")
            print("  Compilation / validation successful.")
            self.print_summary(diagnostics)
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
            classification = classifier.classify(diagnostic)
            print(f"Category: {diagnostic.category}")
            print(f"Classification: {classification}")
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
            if diagnostic.confidence >= 95:
                confidence_level = "HIGH"
            elif diagnostic.confidence >= 80:
                confidence_level = "MEDIUM"
            else:
                confidence_level = "LOW"
            print(
                f"Confidence: "
                f"{diagnostic.confidence}% "
                f"({confidence_level})"
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

        self.print_summary(diagnostics)
        print()

    def print_summary(self, diagnostics):
        summary = self.summary(diagnostics)
        print("DIAGNOSTIC SUMMARY")
        print(f"  Errors: {summary['errors']}")
        print(f"  Warnings: {summary['warnings']}")
        if summary["by_code"]:
            print("  By code:")
            for code, count in summary["by_code"].items():
                print(f"    {code}: {count}")
        if summary["by_category"]:
            print("  By category:")
            for category, count in summary["by_category"].items():
                print(f"    {category}: {count}")