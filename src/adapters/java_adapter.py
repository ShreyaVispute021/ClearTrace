import subprocess
import re
import os

from adapters.base import LanguageAdapter
from diagnostic_ir import Diagnostic
from suggestion_engine import SuggestionEngine


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
        try:
            with open(filename, "r", encoding="utf-8") as file:
                source = file.read()
        except OSError:
            source = ""

        match = re.search(
            r":(\d+): error:",
            output
        )

        line = int(match.group(1)) if match else 1

        source_line = ""

        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # javac may place a missing-semicolon diagnostic on the next
            # statement (commonly `return`). Prefer the preceding unterminated
            # statement when the compiler explicitly says `';' expected`.
            if "';' expected" in output and 1 < line <= len(lines):
                previous = lines[line - 2].rstrip("\r\n")
                current = lines[line - 1].strip()
                previous_stripped = previous.strip()
                if (
                    previous_stripped
                    and not previous_stripped.endswith((";", "{", "}", ":"))
                    and not previous_stripped.startswith(("//", "/*", "*", "*", "@"))
                    and current
                ):
                    line -= 1

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

        elif "incompatible types:" in output:
            message = "Type mismatch."
            explanation = (
                "The value's type is not compatible with the type "
                "required by this assignment or expression."
            )
            suggestion = (
                "Check the declared types and use a compatible value "
                "or an appropriate conversion."
            )
            confidence = 90

        elif "cannot find symbol" in output:

            message = "Unknown identifier or symbol."

            explanation = (
                "Java could not find the variable, method, "
                "or class being referenced."
            )

            unknown_match = re.search(r"symbol:\s+variable\s+([A-Za-z_]\w*)", output)
            unknown_name = unknown_match.group(1) if unknown_match else None
            close_hint = SuggestionEngine().suggestion_for_source(unknown_name, source, "Java") if unknown_name else None
            suggestion = close_hint or (
                "Check the spelling and make sure it is declared or imported."
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