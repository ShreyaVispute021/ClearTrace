from adapters.python_adapter import PythonAdapter
from adapters.cpp_adapter import CppAdapter
from adapters.java_adapter import JavaAdapter
from adapters.javascript_adapter import JavaScriptAdapter

from language_detector import LanguageDetector


class ClearTraceAnalyzer:

    def __init__(self):

        self.detector = LanguageDetector()

        self.adapters = [
            PythonAdapter(),
            CppAdapter(),
            JavaAdapter(),
            JavaScriptAdapter()
        ]

    def detect_adapter(self, filename):

        for adapter in self.adapters:

            if adapter.can_handle(filename):
                return adapter

        return None

    def analyze(self, filename):

        language = self.detector.detect(filename)

        adapter = self.detect_adapter(filename)

        if adapter is None:

            raise ValueError(
                f"Language '{language}' is not currently supported."
            )

        return adapter.analyze(filename)