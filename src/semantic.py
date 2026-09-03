from ast_nodes import (
    LetDeclaration,
    NumberLiteral,
    StringLiteral,
    Identifier,
    BinaryExpression
)


class SemanticAnalyzer:

    def __init__(self):
        self.symbols = {}
        self.errors = []

    def analyze(self, program):
        for statement in program.statements:
            self.analyze_statement(statement)

        return self.errors

    def analyze_statement(self, statement):

        if not isinstance(statement, LetDeclaration):
            return

        # Check duplicate declaration

        if statement.name in self.symbols:

            self.errors.append({
                "type": "DUPLICATE_DECLARATION",
                "name": statement.name,
                "line": statement.line,
                "column": statement.column
            })

            self.get_type(statement.value)

            return

        # Analyze the value

        value_type = self.get_type(statement.value)

        # Add variable to symbol table

        self.symbols[statement.name] = value_type

    def get_type(self, node):

        # Integer

        if isinstance(node, NumberLiteral):
            return "integer"

        # String

        if isinstance(node, StringLiteral):
            return "string"

        # Identifier

        if isinstance(node, Identifier):

            if node.name not in self.symbols:

                self.errors.append({
                    "type": "UNDECLARED_VARIABLE",
                    "name": node.name,
                    "line": node.line,
                    "column": node.column
                })

                return "unknown"

            return self.symbols[node.name]

        # Binary expression

        if isinstance(node, BinaryExpression):

            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)

            if left_type == "unknown" or right_type == "unknown":
                return "unknown"

            # Types must match
            if left_type != right_type:

                self.errors.append({
                    "type": "TYPE_MISMATCH",
                    "left_type": left_type,
                    "right_type": right_type,
                    "operator": node.operator,
                    "line": node.right.line,
                    "column": node.right.column
                })

                return "unknown"

            return left_type

        return "unknown"