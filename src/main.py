from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from diagnostics import DiagnosticEngine


source = """
let x = 10
let y = unknown + 5;
let x = 20;
let z = "hello" + 10;
"""


# =========================
# LEXICAL ANALYSIS
# =========================

lexer = Lexer(source)
tokens = lexer.tokenize()


# =========================
# SYNTAX ANALYSIS
# =========================

parser = Parser(tokens)
ast = parser.parse()

syntax_errors = parser.errors


# =========================
# SEMANTIC ANALYSIS
# =========================

analyzer = SemanticAnalyzer()
semantic_errors = analyzer.analyze(ast)


# =========================
# COMBINE ERRORS
# =========================

errors = syntax_errors + semantic_errors


# =========================
# DIAGNOSTICS
# =========================

diagnostics = DiagnosticEngine(source)

if not errors:

    print()
    print("✓ Compilation successful")
    print("  No errors found.")

else:

    print()
    print(f"Found {len(errors)} error(s):")
    print()

    for error in errors:

        print(diagnostics.report(error))