import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from diagnostic_ir import Diagnostic
from reporter import Reporter
from suggestion_engine import SuggestionEngine


class DiagnosticFeatureTests(unittest.TestCase):
    def setUp(self):
        self.diagnostics = [
            Diagnostic("C++", "COMPILE_ERROR", "ERROR", "CT-CPP-001", 2, 8,
                       "Identifier is not declared.", "Not declared.",
                       "Did you mean 'total'?", 96, "print(totl);"),
            Diagnostic("Java", "SYNTAX_ERROR", "WARNING", "CT-JAVA-002", 4, 1,
                       "Example warning.", "Explanation.", "Suggestion.", 80, ""),
        ]

    def test_diagnostic_serializes_to_dict(self):
        data = self.diagnostics[0].to_dict()
        self.assertEqual(data["code"], "CT-CPP-001")
        self.assertEqual(data["line"], 2)
        self.assertEqual(data["column"], 8)
        self.assertEqual(data["source_line"], "print(totl);")

    def test_summary_counts_errors_warnings_and_codes(self):
        summary = Reporter.summary(self.diagnostics)
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["warnings"], 1)
        self.assertEqual(summary["by_code"]["CT-CPP-001"], 1)

    def test_similar_identifier_suggestion(self):
        engine = SuggestionEngine()
        self.assertEqual(engine.suggest("totl", ["total", "count"]), "total")

    def test_declaration_names_for_cpp(self):
        engine = SuggestionEngine()
        self.assertIn("total", engine.declared_names("int total = 4;", "C++"))

    def test_similar_name_message(self):
        engine = SuggestionEngine()
        self.assertEqual(
            engine.suggestion_for_source("totl", "int total = 4;", "C++"),
            "Did you mean 'total'?",
        )


if __name__ == "__main__":
    unittest.main()
