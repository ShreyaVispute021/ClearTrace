from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int


class Lexer:
    KEYWORDS = {
        "let": "LET"
    }

    SINGLE_CHAR_TOKENS = {
        "=": "ASSIGN",
        "+": "PLUS",
        "-": "MINUS",
        "*": "STAR",
        "/": "SLASH",
        ";": "SEMICOLON",
        "(": "LPAREN",
        ")": "RPAREN",
    }

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def advance(self):
        char = self.source[self.position]
        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def peek(self):
        if self.position >= len(self.source):
            return "\0"

        return self.source[self.position]

    def tokenize(self):
        tokens = []

        while self.position < len(self.source):
            char = self.peek()

            # Ignore spaces and tabs
            if char in " \t\r":
                self.advance()
                continue

            # New line
            if char == "\n":
                self.advance()
                continue

            # Identifier / keyword
            if char.isalpha() or char == "_":
                tokens.append(self.read_identifier())
                continue

            # Number
            if char.isdigit():
                tokens.append(self.read_number())
                continue

            # String
            if char == '"':
                tokens.append(self.read_string())
                continue

            # Single-character tokens
            if char in self.SINGLE_CHAR_TOKENS:
                line = self.line
                column = self.column
                token_type = self.SINGLE_CHAR_TOKENS[char]

                self.advance()

                tokens.append(
                    Token(token_type, char, line, column)
                )
                continue

            # Unknown character
            line = self.line
            column = self.column

            raise Exception(
                f"Unexpected character '{char}' "
                f"at line {line}, column {column}"
            )

        tokens.append(
            Token("EOF", "", self.line, self.column)
        )

        return tokens

    def read_identifier(self):
        line = self.line
        column = self.column

        value = ""

        while self.peek().isalnum() or self.peek() == "_":
            value += self.advance()

        token_type = self.KEYWORDS.get(value, "IDENTIFIER")

        return Token(token_type, value, line, column)

    def read_number(self):
        line = self.line
        column = self.column

        value = ""

        while self.peek().isdigit():
            value += self.advance()

        return Token("NUMBER", value, line, column)

    def read_string(self):
        line = self.line
        column = self.column

        self.advance()  # Opening quote

        value = ""

        while self.peek() != '"' and self.peek() != "\0":
            value += self.advance()

        if self.peek() == "\0":
            raise Exception(
                f"Unterminated string at "
                f"line {line}, column {column}"
            )

        self.advance()  # Closing quote

        return Token("STRING", value, line, column)