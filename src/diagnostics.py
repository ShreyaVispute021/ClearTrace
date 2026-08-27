class DiagnosticEngine:

    ERROR_CODES = {
        "MISSING_SEMICOLON": "E001",
        "UNDECLARED_VARIABLE": "E002",
        "DUPLICATE_DECLARATION": "E003",
        "TYPE_MISMATCH": "E004",
        "UNEXPECTED_TOKEN": "E005",
    }

    def __init__(self, source):
        self.source = source
        self.lines = source.splitlines()

    def report(self, error):
        error_type = error["type"]

        if error_type == "MISSING_SEMICOLON":
            return self.missing_semicolon(error)

        if error_type == "UNDECLARED_VARIABLE":
            return self.undeclared_variable(error)

        if error_type == "DUPLICATE_DECLARATION":
            return self.duplicate_declaration(error)

        if error_type == "TYPE_MISMATCH":
            return self.type_mismatch(error)

        if error_type == "UNEXPECTED_TOKEN":
            return self.unexpected_token(error)

        return "Unknown compiler error."

    def unexpected_token(self, error):

        code = self.ERROR_CODES["UNEXPECTED_TOKEN"]

        line = error["line"]
        column = error["column"]

        actual = error["actual"]
        expected = error["expected"]

        source_line = self.get_source_line(line)

        return f"""Error {code}: Unexpected token
  --> line {line}, column {column}

    {source_line}
    {self.make_caret(column)}

  Expected {expected}, but found '{actual}'.

  Suggestion: Check the syntax at this location.
"""

    def get_source_line(self, line):
        if 1 <= line <= len(self.lines):
            return self.lines[line - 1]

        return ""

    def make_caret(self, column):
        return " " * (column - 1) + "^"

    def undeclared_variable(self, error):

        code = self.ERROR_CODES["UNDECLARED_VARIABLE"]

        line = error["line"]
        column = error["column"]
        name = error["name"]

        source_line = self.get_source_line(line)

        return f"""Error {code}: Undeclared variable
  --> line {line}, column {column}

    {source_line}
    {self.make_caret(column)}

  The variable '{name}' has not been declared.

  Suggestion: Declare '{name}' before using it.
"""

    def duplicate_declaration(self, error):

        code = self.ERROR_CODES["DUPLICATE_DECLARATION"]

        line = error["line"]
        column = error["column"]
        name = error["name"]

        source_line = self.get_source_line(line)

        return f"""Error {code}: Duplicate declaration
  --> line {line}, column {column}

    {source_line}
    {self.make_caret(column)}

  The variable '{name}' has already been declared.

  Suggestion: Use a different variable name.
"""

    def type_mismatch(self, error):

        code = self.ERROR_CODES["TYPE_MISMATCH"]

        line = error["line"]
        column = error["column"]

        left_type = error["left_type"]
        right_type = error["right_type"]
        operator = error["operator"]

        source_line = self.get_source_line(line)

        return f"""Error {code}: Type mismatch
  --> line {line}, column {column}

    {source_line}
    {self.make_caret(column)}

  The '{operator}' operator cannot combine
  a {left_type} and a {right_type}.

  Suggestion: Use compatible types with the '{operator}' operator.
"""

    def missing_semicolon(self, error):

        code = self.ERROR_CODES["MISSING_SEMICOLON"]

        line = error["line"]
        column = error["column"]

        source_line = self.get_source_line(line)

        # Point to the end of the statement
        column = len(source_line) + 1

        return f"""Error {code}: Missing semicolon
  --> line {line}, column {column}

    {source_line}
    {self.make_caret(column)}

  This statement must end with a semicolon.

  Suggestion: Add ';' at the end of the statement.
"""