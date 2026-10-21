
import re
import subprocess

from adapters.base import LanguageAdapter
from diagnostic_ir import Diagnostic
from suggestion_engine import SuggestionEngine


class CppAdapter(LanguageAdapter):

    ERROR_PATTERN = re.compile(
        r"^(.+?):(\d+):(\d+):\s*(fatal error|error|warning|note):\s*(.*)$",
        re.MULTILINE
    )

    def can_handle(self, filename):
        return filename.lower().endswith((".cpp", ".cc", ".cxx"))

    def analyze(self, filename):
        result = subprocess.run(
            ["g++", "-fmax-errors=0", "-fsyntax-only", filename],
            capture_output=True,
            text=True,
            errors="replace"
        )

        if result.returncode == 0:
            return []

        output = result.stderr

        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except OSError:
            lines = []

        matches = list(self.ERROR_PATTERN.finditer(output))
        diagnostics = []
        suggestion_engine = SuggestionEngine()

        for index, match in enumerate(matches):
            severity_text = match.group(4)
            if severity_text not in ("error", "fatal error"):
                continue

            line = int(match.group(2))
            column = int(match.group(3))
            message_text = match.group(5)

            # Keep the context belonging to this compiler diagnostic.
            end = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(output)
            )
            block = output[match.start():end]
            details = message_text + "\n" + block

            source_line = ""
            if 1 <= line <= len(lines):
                source_line = lines[line - 1].rstrip("\r\n")

            message = "C++ compilation error."
            explanation = (
                "The C++ compiler found an error while processing "
                "this source file."
            )
            suggestion = "Check the compiler message and nearby code."
            confidence = 75

            if (
                "expected ';'" in details
                or "expected ',' or ';' before" in details
                or "expected ';' before" in details
                or "expected ‘;’" in details
            ):
                message = "Missing semicolon."
                explanation = (
                    "C++ statements normally need to end with "
                    "a semicolon ';'."
                )
                suggestion = "Add ';' at the end of the statement."
                confidence = 99

            elif "was not declared in this scope" in details:
                message = "Identifier is not declared."
                explanation = (
                    "The program uses a variable or identifier "
                    "that has not been declared in the current scope."
                )

                unknown_match = re.search(
                    r"['‘]([A-Za-z_]\w*)['’]?\s+was not declared in this scope",
                    details
                )
                unknown_name = (
                    unknown_match.group(1) if unknown_match else None
                )

                close_hint = (
                    suggestion_engine.suggestion_for_source(
                        unknown_name, "\n".join(lines), "C++"
                    )
                    if unknown_name else None
                )
                suggestion = (
                    close_hint
                    or "Declare the identifier before using it."
                )
                confidence = 96

            elif "does not name a type" in details:
                message = "Unknown type."
                explanation = (
                    "The compiler does not recognize the specified "
                    "type name."
                )
                suggestion = (
                    "Check the type name or include the required header."
                )
                confidence = 94

            elif "no match for" in details:
                message = "Invalid operation between types."
                explanation = (
                    "The selected operator cannot be used with "
                    "the provided operand types."
                )
                suggestion = (
                    "Use compatible types or change the operator."
                )
                confidence = 92

            diagnostics.append(
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
            )

        # Fallback for compiler output that doesn't match the pattern.
        if not diagnostics:
            diagnostics.append(
                Diagnostic(
                    language="C++",
                    category="COMPILE_ERROR",
                    severity="ERROR",
                    code="CT-CPP-001",
                    line=1,
                    column=1,
                    message="C++ compilation error.",
                    explanation=(
                        "The C++ compiler reported an error, but "
                        "ClearTrace could not parse its source location."
                    ),
                    suggestion=(
                        "Check the compiler output and nearby source code."
                    ),
                    confidence=75,
                    source_line=(
                        lines[0].rstrip("\r\n") if lines else ""
                    )
                )
            )

        return diagnostics
