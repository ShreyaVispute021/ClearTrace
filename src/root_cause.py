"""Explainable, heuristic diagnostic triage.

This module prioritizes likely primary diagnostics; it does not claim to prove
causality between compiler errors.
"""
from collections import OrderedDict


class RootCauseAnalyzer:
    @staticmethod
    def _key(d):
        return (str(d.language).lower(), str(d.code), int(d.line), int(d.column),
                str(d.message).strip().casefold())

    def deduplicate(self, diagnostics):
        """Remove exact normalized duplicates while preserving first occurrence."""
        unique = OrderedDict()
        for diagnostic in diagnostics:
            unique.setdefault(self._key(diagnostic), diagnostic)
        return list(unique.values())

    @staticmethod
    def _rank_key(d):
        # Earlier locations are useful evidence, but not proof of causality.
        # Prefer errors over warnings and higher-confidence normalized rules.
        severity = str(getattr(d, "severity", "ERROR")).upper()
        severity_rank = 0 if severity == "ERROR" else 1 if severity == "WARNING" else 2
        try:
            confidence = int(getattr(d, "confidence", 0))
        except (TypeError, ValueError):
            confidence = 0
        return (severity_rank, int(getattr(d, "line", 1) or 1),
                int(getattr(d, "column", 1) or 1), -confidence)

    def find_root_cause(self, diagnostics):
        ordered = self.deduplicate(diagnostics)
        return min(ordered, key=self._rank_key) if ordered else None

    def find_related_errors(self, diagnostics):
        ordered = self.deduplicate(diagnostics)
        root = self.find_root_cause(ordered)
        if root is None:
            return []
        return [d for d in sorted(ordered, key=self._rank_key) if d is not root]

    def analyze(self, diagnostics):
        unique = self.deduplicate(diagnostics)
        root = self.find_root_cause(unique)
        return {"diagnostics": unique, "root_cause": root,
                "related_errors": self.find_related_errors(unique),
                "method": "heuristic severity/source-order/confidence ranking",
                "causality_proven": False}
