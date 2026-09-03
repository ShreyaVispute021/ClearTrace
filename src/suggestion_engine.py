import difflib


class SuggestionEngine:

    def suggest(self, unknown_name, known_names):

        if not known_names:
            return None

        matches = difflib.get_close_matches(
            unknown_name,
            known_names,
            n=1,
            cutoff=0.55
        )

        if matches:
            return matches[0]

        return None