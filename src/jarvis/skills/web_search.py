"""Web search skill — opens a browser search for the query."""

import webbrowser
from .registry import Skill, SkillResult


class WebSearchSkill(Skill):
    name = "web_search"
    description = "Search the web for information"
    triggers = ["search for", "google", "look up", "search the web", "find online"]

    def execute(self, query: str, context: dict) -> SkillResult:
        # Extract the search query
        search_term = self._extract_search_term(query)

        if not search_term:
            return SkillResult(
                success=False,
                message="What would you like me to search for?"
            )

        url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
        webbrowser.open(url)

        return SkillResult(
            success=True,
            message=f"Searching the web for '{search_term}'."
        )

    def _extract_search_term(self, query: str) -> str:
        """Extract the search term from the query."""
        lower = query.lower()
        for trigger in self.triggers:
            if trigger in lower:
                idx = lower.index(trigger) + len(trigger)
                return query[idx:].strip()
        return ""
