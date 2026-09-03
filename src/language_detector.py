import os


class LanguageDetector:

    EXTENSIONS = {
        ".py": "Python",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".java": "Java",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".c": "C",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust"
    }

    def detect(self, filename):

        extension = os.path.splitext(
            filename
        )[1].lower()

        return self.EXTENSIONS.get(
            extension,
            "Unknown"
        )