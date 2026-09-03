class RootCauseAnalyzer:

    def analyze(self, diagnostics):

        if not diagnostics:
            return None

        if len(diagnostics) == 1:
            return diagnostics[0]

        # The earliest syntax error is often
        # a possible root cause.

        sorted_errors = sorted(
            diagnostics,
            key=lambda error: (
                error.line,
                error.column
            )
        )

        first = sorted_errors[0]

        return {
            "root_cause": first,
            "related_errors": sorted_errors[1:]
        }