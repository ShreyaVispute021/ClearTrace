from dataclasses import dataclass


class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    statements: list


@dataclass
class LetDeclaration(ASTNode):
    name: str
    value: ASTNode
    line: int
    column: int


@dataclass
class NumberLiteral(ASTNode):
    value: int
    line: int
    column: int


@dataclass
class StringLiteral(ASTNode):
    value: str
    line: int
    column: int


@dataclass
class Identifier(ASTNode):
    name: str
    line: int
    column: int


@dataclass
class BinaryExpression(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    line: int
    column: int