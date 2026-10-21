class RootCauseAnalyzer:

    def find_root_cause(self, diagnostics):

        if not diagnostics:
            return None

        ordered = sorted(
            diagnostics,
            key=lambda d: (d.line, d.column)
        )

        return ordered[0]

    def find_related_errors(self, diagnostics):

        if len(diagnostics) <= 1:
            return []

        ordered = sorted(
            diagnostics,
            key=lambda d: (d.line, d.column)
        )

        return ordered[1:]