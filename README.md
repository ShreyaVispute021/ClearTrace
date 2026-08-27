# ClearTrace: Human-Readable Compiler Diagnostics

ClearTrace is an educational compiler front-end focused on **human-readable and actionable compiler diagnostics**.

Instead of simply detecting an error and displaying a generic message, ClearTrace attempts to explain **what went wrong, where it happened, why it happened, and how it can be fixed**.

The project is inspired by the diagnostic experience provided by modern compilers such as Rust, Clang, and other developer-focused toolchains.

---

## Problem Statement

Traditional educational compiler projects often focus primarily on lexical analysis, parsing, and semantic validation. While these components are essential, compiler errors are frequently presented as short and generic messages that provide limited guidance to the programmer.

ClearTrace focuses on the diagnostics layer.

The goal is to transform compiler errors into structured, human-readable diagnostics containing:

* Error classification
* Error code
* Exact source location
* Source-code context
* Caret-based highlighting
* Plain-English explanation
* Suggested correction

---

## Project Objectives

* Implement a small compiler front-end.
* Perform lexical analysis and tokenization.
* Track source-code line and column positions.
* Implement recursive-descent parsing.
* Generate an Abstract Syntax Tree (AST).
* Maintain a symbol table.
* Perform basic semantic analysis.
* Classify common compiler errors.
* Generate human-readable diagnostic messages.
* Provide suggestions for correcting errors.
* Support basic parser error recovery.
* Report multiple errors in a single compilation.

---

## Architecture

```text
                     Source Code
                          │
                          ▼
                   ┌─────────────┐
                   │    Lexer    │
                   └──────┬──────┘
                          │
                          ▼
                       Tokens
                          │
                          ▼
                   ┌─────────────┐
                   │    Parser   │
                   │ Recursive   │
                   │   Descent   │
                   └──────┬──────┘
                          │
                          ▼
                         AST
                          │
                          ▼
                ┌───────────────────┐
                │ Semantic Analyzer │
                └─────────┬─────────┘
                          │
                  ┌───────┴────────┐
                  ▼                ▼
            Symbol Table     Error Detection
                  │                │
                  └───────┬────────┘
                          ▼
                ┌───────────────────┐
                │ Diagnostic Engine │
                └─────────┬─────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Location   Explanation   Suggestion
             │            │            │
             └────────────┼────────────┘
                          ▼
                Human-readable output
```

---

## Current Language Features

The current prototype supports a small programming language containing:

* Variable declarations using `let`
* Integer literals
* String literals
* Identifiers
* Assignment
* Addition
* Subtraction
* Basic expressions

Example:

```text
let x = 10;
let y = x + 20;
let message = "hello";
```

---

## Diagnostic Categories

### E001 — Missing Semicolon

Input:

```text
let x = 10
```

ClearTrace reports:

```text
Error E001: Missing semicolon
  --> line 1, column 11

    let x = 10
              ^

  This statement must end with a semicolon.

  Suggestion: Add ';' at the end of the statement.
```

---

### E002 — Undeclared Variable

Input:

```text
let x = unknown + 5;
```

Output:

```text
Error E002: Undeclared variable
  --> line 1, column 9

    let x = unknown + 5;
            ^

  The variable 'unknown' has not been declared.

  Suggestion: Declare 'unknown' before using it.
```

---

### E003 — Duplicate Declaration

Input:

```text
let x = 10;
let x = 20;
```

Output:

```text
Error E003: Duplicate declaration
  --> line 2, column 5

    let x = 20;
        ^

  The variable 'x' has already been declared.

  Suggestion: Use a different variable name.
```

---

### E004 — Type Mismatch

Input:

```text
let x = "hello" + 10;
```

Output:

```text
Error E004: Type mismatch
  --> line 1, column 19

    let x = "hello" + 10;
                      ^

  The '+' operator cannot combine
  a string and an integer.

  Suggestion: Use compatible types with the '+' operator.
```

---

## Multiple Error Reporting

ClearTrace supports basic error recovery so that compilation does not necessarily stop at the first error.

For example:

```text
let x = 10
let y = unknown + 5;
let x = 20;
let z = "hello" + 10;
```

The compiler can identify multiple problems:

```text
E001  Missing semicolon
E002  Undeclared variable
E003  Duplicate declaration
E004  Type mismatch
```

This allows the programmer to understand several problems in one compilation rather than fixing errors one at a time.

---

## Project Structure

```text
ClearTrace/
│
├── src/
│   ├── main.py
│   ├── lexer.py
│   ├── parser.py
│   ├── ast_nodes.py
│   ├── semantic.py
│   └── diagnostics.py
│
├── tests/
│   └── test_cases.txt
│
└── README.md
```

### Components

**`lexer.py`**

Responsible for tokenizing source code and tracking line/column positions.

**`parser.py`**

Implements recursive-descent parsing and basic syntax error recovery.

**`ast_nodes.py`**

Contains the Abstract Syntax Tree node definitions.

**`semantic.py`**

Performs semantic checks using a symbol table and basic type information.

**`diagnostics.py`**

Converts structured compiler errors into human-readable explanations and suggestions.

**`main.py`**

Provides the command-line interface and connects the compiler pipeline.

---

## Running the Project

### Requirements

* Python 3.x
* Git (optional, for version control)

### Clone the repository

```bash
git clone <your-repository-url>
cd ClearTrace
```

### Run ClearTrace

```bash
python src/main.py
```

You will be prompted to enter source code.

Type:

```text
let x = 10;
let y = x + 20;
END
```

The compiler will analyze the program and report whether it contains errors.

---

## Example Session

```text
========================================
          CLEARTRACE COMPILER
     Human-Readable Diagnostics v0.1
========================================

Enter your code.
Type END on a new line when finished.

let x = 10
let y = unknown + 5;
let x = 5;
let z = "hello" + 10;
END

----------------------------------------
✗ Found 4 error(s)
```

ClearTrace then displays each diagnostic with its location, explanation, and suggestion.

---

## Design Philosophy

ClearTrace follows a simple principle:

> **Don't just tell the programmer that something is wrong. Explain what is wrong and help them fix it.**

The project separates compiler analysis from diagnostic presentation. The lexer, parser, and semantic analyzer identify problems, while the diagnostic engine transforms those problems into understandable messages.

This separation makes it possible to extend the compiler with additional diagnostics without tightly coupling error messages to the compiler implementation.

---

## Future Scope

Planned improvements include:

* Additional syntax and semantic error categories
* Improved parser error recovery
* Function declarations and calls
* Boolean and additional data types
* Function argument checking
* Unused-variable warnings
* Unreachable-code warnings
* More intelligent suggestions
* Improved source highlighting
* Automatic code fixes
* Web-based code editor
* IDE integration

---

## Academic Relevance

ClearTrace demonstrates concepts from:

* Compiler Design
* Lexical Analysis
* Syntax Analysis
* Recursive-Descent Parsing
* Abstract Syntax Trees
* Symbol Tables
* Semantic Analysis
* Error Detection
* Error Recovery
* Compiler Diagnostics

The project focuses particularly on the practical problem of making compiler diagnostics more understandable and useful to programmers.

---

## Status

**Current version: v0.1 — Working Prototype**

Implemented:

* Lexer
* Token position tracking
* Recursive-descent parser
* AST generation
* Symbol table
* Semantic analysis
* Four diagnostic categories
* Human-readable diagnostics
* Source-location highlighting
* Suggestions
* Basic error recovery
* Multiple-error reporting
* Interactive command-line interface

---

## License

This project is intended for educational and academic purposes.
