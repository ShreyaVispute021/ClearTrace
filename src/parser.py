from ast_nodes import (
    Program,
    LetDeclaration,
    NumberLiteral,
    StringLiteral,
    Identifier,
    BinaryExpression
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()

        if self.position < len(self.tokens) - 1:
            self.position += 1

        return token

    def match(self, token_type):

        if self.current().type == token_type:
            return self.advance()

        return None

    def expect(self, token_type):

        token = self.current()

        if token.type != token_type:

            raise SyntaxError({
                "type": "UNEXPECTED_TOKEN",
                "expected": token_type,
                "actual": token.value,
                "line": token.line,
                "column": token.column
            })

        return self.advance()

    # =========================
    # MAIN PARSER
    # =========================

    def parse(self):

        statements = []

        while self.current().type != "EOF":

            try:

                statement = self.parse_statement()

                if statement:
                    statements.append(statement)

            except SyntaxError as error:

                self.errors.append(error.args[0])

                self.synchronize()

        return Program(statements)

    # =========================
    # ERROR RECOVERY
    # =========================

    def synchronize(self):

        while self.current().type != "EOF":

            # Semicolon is a natural statement boundary
            if self.current().type == "SEMICOLON":
                self.advance()
                return

            # A new 'let' usually means a new statement
            if self.current().type == "LET":
                return

            self.advance()

    # =========================
    # STATEMENT
    # =========================

    def parse_statement(self):

        if self.current().type == "LET":
            return self.parse_declaration()

        token = self.current()

        raise SyntaxError({
            "type": "UNEXPECTED_TOKEN",
            "expected": "LET",
            "actual": token.value,
            "line": token.line,
            "column": token.column
        })

    # =========================
    # DECLARATION
    # =========================

    def parse_declaration(self):

        self.expect("LET")

        name_token = self.expect("IDENTIFIER")

        self.expect("ASSIGN")

        value = self.parse_expression()

        # --------------------------------
        # Check for semicolon
        # --------------------------------

        if self.current().type != "SEMICOLON":

            previous_token = self.tokens[self.position - 1]

            self.errors.append({
                "type": "MISSING_SEMICOLON",
                "line": previous_token.line,
                "column": previous_token.column
            })

            return LetDeclaration(
                name=name_token.value,
                value=value,
                line=name_token.line,
                column=name_token.column
            )

        # Normal case
        self.advance()

        return LetDeclaration(
            name=name_token.value,
            value=value,
            line=name_token.line,
            column=name_token.column
        )

    # =========================
    # EXPRESSIONS
    # =========================

    def parse_expression(self):

        left = self.parse_primary()

        while self.current().type in ("PLUS", "MINUS"):

            operator_token = self.advance()

            right = self.parse_primary()

            left = BinaryExpression(
                left=left,
                operator=operator_token.value,
                right=right,
                line=operator_token.line,
                column=operator_token.column
            )

        return left

    # =========================
    # PRIMARY EXPRESSIONS
    # =========================

    def parse_primary(self):

        token = self.current()

        if token.type == "NUMBER":

            self.advance()

            return NumberLiteral(
                value=int(token.value),
                line=token.line,
                column=token.column
            )

        if token.type == "STRING":

            self.advance()

            return StringLiteral(
                value=token.value,
                line=token.line,
                column=token.column
            )

        if token.type == "IDENTIFIER":

            self.advance()

            return Identifier(
                name=token.value,
                line=token.line,
                column=token.column
            )

        raise SyntaxError({
            "type": "UNEXPECTED_TOKEN",
            "expected": "expression",
            "actual": token.value,
            "line": token.line,
            "column": token.column
        })