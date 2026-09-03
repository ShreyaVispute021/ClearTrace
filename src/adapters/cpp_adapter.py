import subprocess
import re

from adapters.base import LanguageAdapter
from diagnostic_ir import Diagnostic


class CppAdapter(LanguageAdapter):

    def can_handle(self, filename):
        return filename.lower().endswith((".cpp", ".cc", ".cxx"))

    def analyze(self, filename):

        result = subprocess.run(
            ["g++", "-fsyntax-only", filename],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return []

        output = result.stderr

        match = re.search(
            r":(\d+):(\d+):\s*error:",
            output
        )

        line = int(match.group(1)) if match else 1
        column = int(match.group(2)) if match else 1

        source_line = ""

        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            if 1 <= line <= len(lines):
                source_line = lines[line - 1].rstrip()

        except Exception:
            pass

        # Classify common C++ errors

        if "expected ';'" in output:

            message = "Missing semicolon."

            explanation = (
                "C++ statements normally need to end with "
                "a semicolon ';'."
            )

            suggestion = (
                "Add ';' at the end of the statement."
            )

            confidence = 99

        elif "was not declared in this scope" in output:

            message = "Identifier is not declared."

            explanation = (
                "The program uses a variable or identifier "
                "that has not been declared in the current scope."
            )

            suggestion = (
                "Declare the identifier before using it."
            )

            confidence = 96

        elif "does not name a type" in output:

            message = "Unknown type."

            explanation = (
                "The compiler does not recognize the specified "
                "type name."
            )

            suggestion = (
                "Check the type name or include the required header."
            )

            confidence = 94

        elif "no match for" in output:

            message = "Invalid operation between types."

            explanation = (
                "The selected operator cannot be used with "
                "the provided operand types."
            )

            suggestion = (
                "Use compatible types or change the operator."
            )

            confidence = 92

        else:

            message = "C++ compilation error."

            explanation = (
                "The C++ compiler found an error while processing "
                "this source file."
            )

            suggestion = (
                "Check the compiler message and nearby code."
            )

            confidence = 75

        return [
            Diagnostic(
                language="C++",
                category="COMPILE_ERROR",
                severity="ERROR",
                code="CT-CPP-001",
                line=line,
                column=column,
                message=message,
                explanation=explanation,
                suggestion=suggestion,
                confidence=confidence,
                source_line=source_line
            )
        ]