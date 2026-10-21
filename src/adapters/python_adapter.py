import subprocess
import sys
import re
import difflib

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

        # Missing colon

        if "expected ':'" in output:

            return [
                Diagnostic(
                    language="Python",
                    category="SYNTAX_ERROR",
                    severity="ERROR",
                    code="CT-PY-001",
                    line=line,
                    column=max(1, len(source_line)),
                    message="Missing ':' after statement.",
                    explanation=(
                        "Python requires a colon after statements "
                        "such as if, for, while, and function definitions."
                    ),
                    suggestion="Add ':' at the end of the statement.",
                    confidence=99,
                    source_line=source_line
                )
            ]

        # Indentation error

        if "IndentationError" in output:

            return [
                Diagnostic(
                    language="Python",
                    category="SYNTAX_ERROR",
                    severity="ERROR",
                    code="CT-PY-002",
                    line=line,
                    column=1,
                    message="Incorrect indentation.",
                    explanation=(
                        "Python uses indentation to define blocks of code. "
                        "This line does not match the expected indentation."
                    ),
                    suggestion=(
                        "Check the indentation and align this line "
                        "with the surrounding block."
                    ),
                    confidence=94,
                    source_line=source_line
                )
            ]

        # Generic error

        return [
            Diagnostic(
                language="Python",
                category="SYNTAX_ERROR",
                severity="ERROR",
                code="CT-PY-999",
                line=line,
                column=1,
                message="Python syntax error.",
                explanation=(
                    "The Python interpreter could not parse "
                    "this part of the program."
                ),
                suggestion=(
                    "Check the syntax near the reported line."
                ),
                confidence=75,
                source_line=source_line
            )
        ]