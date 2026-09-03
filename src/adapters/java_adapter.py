import subprocess
import re
import os

from adapters.base import LanguageAdapter
from diagnostic_ir import Diagnostic


class JavaAdapter(LanguageAdapter):

    def can_handle(self, filename):
        return filename.lower().endswith(".java")

    def analyze(self, filename):

        result = subprocess.run(
            ["javac", filename],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return []

        output = result.stderr

        match = re.search(
            r":(\d+): error:",
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

        if "';' expected" in output:

            message = "Missing semicolon."

            explanation = (
                "Java statements must normally end with "
                "a semicolon ';'."
            )

            suggestion = "Add ';' at the end of the statement."

            confidence = 99

        elif "cannot find symbol" in output:

            message = "Unknown identifier or symbol."

            explanation = (
                "Java could not find the variable, method, "
                "or class being referenced."
            )

            suggestion = (
                "Check the spelling and make sure it is "
                "declared or imported."
            )

            confidence = 94

        else:

            message = "Java compilation error."

            explanation = (
                "The Java compiler found an error in the "
                "source program."
            )

            suggestion = "Check the compiler message and nearby code."

            confidence = 75

        return [
            Diagnostic(
                language="Java",
                category="COMPILE_ERROR",
                severity="ERROR",
                code="CT-JAVA-001",
                line=line,
                column=1,
                message=message,
                explanation=explanation,
                suggestion=suggestion,
                confidence=confidence,
                source_line=source_line
            )
        ]