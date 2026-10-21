import difflib
import re


class SuggestionEngine:
    """Suggest close identifier names without changing source code."""

    def suggest(self, unknown_name, known_names):
        if not unknown_name or not known_names:
            return None
        matches = difflib.get_close_matches(
            unknown_name, sorted(set(known_names)), n=1, cutoff=0.55
        )
        return matches[0] if matches else None

    def declared_names(self, source, language):
        # This deliberately recognises common declarations only. It is a
        # lightweight suggestion aid, not a replacement for a language parser.
        patterns = {
            "C++": r"\b(?:int|long|short|float|double|char|bool|string|auto)\s+([A-Za-z_]\w*)",
            "Java": r"\b(?:byte|short|int|long|float|double|char|boolean|String|var)\s+([A-Za-z_]\w*)",
            "JavaScript": r"\b(?:let|const|var|function|class)\s+([A-Za-z_$][\w$]*)",
        }
        pattern = patterns.get(language)
        return re.findall(pattern, source) if pattern else []

    def suggestion_for_source(self, unknown_name, source, language):
        candidate = self.suggest(unknown_name, self.declared_names(source, language))
        return f"Did you mean '{candidate}'?" if candidate else None
