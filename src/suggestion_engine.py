import difflib


class SuggestionEngine:

    def find_similar(self, name, known_names):

        matches = difflib.get_close_matches(
            name,
            known_names,
            n=3,
            cutoff=0.6
        )

        return matches

    def suggest(self, name, known_names):

        matches = self.find_similar(
            name,
            known_names
        )

        if not matches:
            return None

        return matches[0]