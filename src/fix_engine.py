"""Conservative automatic fixes with backup and rollback support.

Only explicitly supported, narrowly matched repairs are applied. A compiler
re-check is still required before a fix can be described as verified.
"""
from pathlib import Path
import shutil


class FixEngine:
    BACKUP_SUFFIX = ".cleartrace.bak"

    def backup_path(self, filename):
        path = Path(filename)
        return path.with_name(path.name + self.BACKUP_SUFFIX)

    def create_backup(self, filename):
        path = Path(filename)
        backup = self.backup_path(filename)
        shutil.copy2(path, backup)
        return backup

    def restore_backup(self, filename):
        backup = self.backup_path(filename)
        if not backup.exists():
            return False
        shutil.copy2(backup, filename)
        backup.unlink()
        return True

    def discard_backup(self, filename):
        backup = self.backup_path(filename)
        if backup.exists():
            backup.unlink()

    def apply_fix(self, filename, diagnostic):
        """Apply a narrow supported fix; caller must re-analyze afterwards."""
        code = getattr(diagnostic, "code", "")
        if code == "CT-PY-001":
            return self._fix_python_colon(filename, diagnostic)
        if code == "CT-CPP-001":
            return self._fix_statement_terminator(filename, diagnostic, ";", "cpp")
        if code == "CT-JAVA-001":
            return self._fix_statement_terminator(filename, diagnostic, ";", "java")
        return False

    @staticmethod
    def _read_lines(filename):
        return Path(filename).read_text(encoding="utf-8").splitlines(keepends=True)

    def _replace_line(self, filename, line_number, replacement):
        lines = self._read_lines(filename)
        if not 1 <= int(line_number) <= len(lines):
            return False
        old = lines[int(line_number) - 1]
        newline = "\n" if old.endswith("\n") else ""
        lines[int(line_number) - 1] = replacement.rstrip("\r\n") + newline
        Path(filename).write_text("".join(lines), encoding="utf-8")
        return True

    def _fix_python_colon(self, filename, diagnostic):
        lines = self._read_lines(filename)
        line_no = int(diagnostic.line)
        if not 1 <= line_no <= len(lines):
            return False
        raw = lines[line_no - 1]
        content = raw.rstrip("\r\n")
        stripped = content.strip()
        # Only handle obvious block headers; never append a colon to arbitrary code.
        import re
        header = re.match(r"^(if\b.+|elif\b.+|else|for\b.+|while\b.+|def\b.+|class\b.+|try|except\b.*|finally|with\b.+)\s*$", stripped)
        if not header or stripped.endswith(":") or "#" in stripped:
            return False
        return self._replace_line(filename, line_no, content + ":")

    def _fix_statement_terminator(self, filename, diagnostic, terminator, language):
        lines = self._read_lines(filename)
        line_no = int(diagnostic.line)
        if not 1 <= line_no <= len(lines):
            return False
        raw = lines[line_no - 1]
        content = raw.rstrip("\r\n")
        stripped = content.strip()
        if not stripped or stripped.endswith((";", "{", "}", ":")):
            return False
        if stripped.startswith(("//", "/*", "*", "#")):
            return False
        # Do not mutate control headers, function/class declarations, or lines
        # where adding a terminator is likely to change structure incorrectly.
        import re
        if language == "cpp":
            if re.match(r"^(if|else|for|while|switch|case|class|struct|namespace|using\b|template\b)\b", stripped):
                return False
            if re.match(r"^(int|void|char|bool|float|double|auto|std::\w+)\s+\w+\s*\([^;]*\)\s*$", stripped):
                return False
        if language == "java":
            if re.match(r"^(if|else|for|while|switch|case|class|interface|enum|public|private|protected)\b", stripped):
                return False
            if re.match(r"^(public|private|protected|static|final|void|int|String|boolean|double|float)\b.*\([^;]*\)\s*$", stripped):
                return False
        return self._replace_line(filename, line_no, content.rstrip() + terminator)
