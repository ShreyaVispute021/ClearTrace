import subprocess
import re

from adapters.base import LanguageAdapter
from diagnostic_ir import Diagnostic


class JavaScriptAdapter(LanguageAdapter):

    def can_handle(self, filename):
        return filename.lower().endswith(".js")

    def analyze(self, filename):

        result = subprocess.run(
            ["node", "--check", filename],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return []

        output = result.stderr

        match = re.search(
            r":(\d+)",
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

        if "Unexpected token" in output:

            message = "Unexpected token."

            explanation = (
                "JavaScript encountered a symbol or keyword "
                "that is not valid at this location."
            )

            suggestion = (
                "Check the syntax around the reported token."
            )

            confidence = 90

        else:

            message = "JavaScript syntax error."

            explanation = (
                "Node.js could not parse this JavaScript source file."
            )

            suggestion = "Check the syntax near this line."

            confidence = 75

        return [
            Diagnostic(
                language="JavaScript",
                category="SYNTAX_ERROR",
                severity="ERROR",
                code="CT-JS-001",
                line=line,
                column=1,
                message=message,
                explanation=explanation,
                suggestion=suggestion,
                confidence=confidence,
                source_line=source_line
            )
        ]