class FixEngine:

    def apply_fix(self, filename, diagnostic):

        if diagnostic.code == "CT-PY-001":
            return self.fix_python_colon(filename, diagnostic)

        if diagnostic.code == "CT-CPP-001":
            return self.fix_cpp_semicolon(filename, diagnostic)

        if diagnostic.code == "CT-JAVA-001":
            return self.fix_java_semicolon(filename, diagnostic)

        return False

    def fix_python_colon(self, filename, diagnostic):

        return self.insert_at_end(
            filename,
            diagnostic.line,
            ":"
        )

    def fix_cpp_semicolon(self, filename, diagnostic):

        return self.insert_at_end(
            filename,
            diagnostic.line,
            ";"
        )

    def fix_java_semicolon(self, filename, diagnostic):

        return self.insert_at_end(
            filename,
            diagnostic.line,
            ";"
        )

    def insert_at_end(self, filename, line_number, character):

        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if not (1 <= line_number <= len(lines)):
            return False

        line = lines[line_number - 1].rstrip("\n")

        if line.rstrip().endswith(character):
            return False

        lines[line_number - 1] = (
            line.rstrip() + character + "\n"
        )

        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(lines)

        return True