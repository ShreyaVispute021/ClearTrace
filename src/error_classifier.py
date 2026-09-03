class ErrorClassifier:

    def classify(self, diagnostic):

        message = diagnostic.message.lower()

        if (
            "missing" in message
            or "unexpected" in message
            or "syntax" in message
            or "indentation" in message
        ):
            return "SYNTAX"

        if (
            "not declared" in message
            or "unknown" in message
            or "type" in message
        ):
            return "SEMANTIC"

        return "GENERAL"