from adapters.python_adapter import PythonAdapter
from adapters.cpp_adapter import CppAdapter
from adapters.java_adapter import JavaAdapter
from adapters.javascript_adapter import JavaScriptAdapter


class ClearTraceAnalyzer:

    def __init__(self):

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

        adapter = self.detect_adapter(filename)

        if adapter is None:

            raise ValueError(
                "Unsupported language. "
                "Supported languages: Python, C++, Java, JavaScript."
            )

        return adapter.analyze(filename)