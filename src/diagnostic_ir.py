from dataclasses import dataclass


@dataclass
class Diagnostic:
    language: str
    category: str
    severity: str
    code: str
    line: int
    column: int
    message: str
    explanation: str
    suggestion: str
    confidence: int
    source_line: str = ""

    def to_dict(self):
        return {
            "language": self.language,
            "category": self.category,
            "severity": self.severity,
            "code": self.code,
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "explanation": self.explanation,
            "suggestion": self.suggestion,
            "confidence": self.confidence,
            "source_line": self.source_line,
        }