import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from diagnostic_ir import Diagnostic
from root_cause import RootCauseAnalyzer
from fix_engine import FixEngine


def diagnostic(code="CT-PY-001", line=1, column=1, message="Example", severity="ERROR", confidence=99):
    return Diagnostic("Python", "SYNTAX_ERROR", severity, code, line, column,
                      message, "Explanation", "Suggestion", confidence, "")


class RootCauseUpgradeTests(unittest.TestCase):
    def test_deduplicates_same_normalized_diagnostic(self):
        a = diagnostic(line=2, message="missing colon")
        b = diagnostic(line=2, message="missing colon")
        self.assertEqual(len(RootCauseAnalyzer().deduplicate([a, b])), 1)

    def test_empty_input_has_no_root(self):
        self.assertIsNone(RootCauseAnalyzer().find_root_cause([]))

    def test_root_is_explainable_priority_not_claimed_causality(self):
        later = diagnostic(line=5, message="later")
        earlier = diagnostic(line=2, message="earlier")
        result = RootCauseAnalyzer().analyze([later, earlier])
        self.assertIs(result["root_cause"], earlier)
        self.assertFalse(result["causality_proven"])


class SafeFixTests(unittest.TestCase):
    def test_python_colon_fix_only_for_block_header(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.py"
            path.write_text("if x == 1\n    print(x)\n", encoding="utf-8")
            self.assertTrue(FixEngine().apply_fix(str(path), diagnostic()))
            self.assertEqual(path.read_text(encoding="utf-8"), "if x == 1:\n    print(x)\n")

    def test_python_colon_fix_refuses_arbitrary_expression(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.py"
            path.write_text("value = 4\n", encoding="utf-8")
            self.assertFalse(FixEngine().apply_fix(str(path), diagnostic()))
            self.assertEqual(path.read_text(encoding="utf-8"), "value = 4\n")

    def test_restore_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.py"
            path.write_text("before\n", encoding="utf-8")
            engine = FixEngine()
            engine.create_backup(str(path))
            path.write_text("after\n", encoding="utf-8")
            self.assertTrue(engine.restore_backup(str(path)))
            self.assertEqual(path.read_text(encoding="utf-8"), "before\n")


if __name__ == "__main__":
    unittest.main()
