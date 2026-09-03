import subprocess
import sys
import re

from adapters.base import LanguageAdapter
from diagnostic_ir import Diagnostic


class PythonAdapter(LanguageAdapter):

    def can_handle(self, filename):
        return filename.lower().endswith(".py")

    def analyze(self, filename):

        result = subprocess.run(
            [sys.executable, "-m", "py_compile", filename],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return []

        output = result.stderr

        match = re.search(
            r'File ".*?", line (\d+)',
            output
        )

        line = int(match.group(1)) if match else 1

        source_line = ""

        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            if 1 <= line <= len(lines):
                source_line = lines[line - 1].rstrip()

        except Exception:
            pass

        if "expected ':'" in output:

            message = "Missing ':' after statement."

            suggestion = "Add ':' at the end of the statement."

            explanation = (
                "Python requires a colon after statements such as "
                "if, for, while, and function definitions."
            )

            confidence = 99

        else:

            message = "Python syntax error."

            suggestion = "Check the syntax near this line."

            explanation = (
                "The Python interpreter could not parse this "
                "part of the program."
            )

            confidence = 75

        return [
            Diagnostic(
                language="Python",
                category="SYNTAX_ERROR",
                severity="ERROR",
                code="CT-PY-001",
                line=line,
                column=1,
                message=message,
                explanation=explanation,
                suggestion=suggestion,
                confidence=confidence,
                source_line=source_line
            )
        ]