"""Random facts skill — fetch interesting facts from the Numbers API."""

import requests
from .registry import Skill, SkillResult


class RandomFactSkill(Skill):
    name = "random_fact"
    description = "Get a random interesting fact"
    triggers = ["random fact", "tell me a fact", "interesting fact", "did you know", "fact of the day", "fun fact"]

    def execute(self, query: str, context: dict) -> SkillResult:
        lower = query.lower()

        # Check if asking for a fact about a specific number
        import re
        number_match = re.search(r'about\s+(?:the\s+)?number\s+(\d+)', lower)
        if number_match:
            number = number_match.group(1)
            return self._get_number_fact(number)

        # Check for "math fact"
        if "math" in lower:
            return self._get_math_fact()

        # Default: random trivia fact
        return self._get_random_fact()

    def _get_random_fact(self) -> SkillResult:
        """Get a random trivia fact."""
        try:
            response = requests.get(
                "https://numbersapi.com/random/trivia",
                timeout=10,
            )
            response.raise_for_status()
            fact = response.text.strip()
            return SkillResult(success=True, message=f"Did you know? {fact}")
        except requests.RequestException as e:
            return SkillResult(success=False, message=f"I couldn't fetch a fact: {e}")

    def _get_number_fact(self, number: str) -> SkillResult:
        """Get a fact about a specific number."""
        try:
            response = requests.get(
                f"https://numbersapi.com/{number}",
                timeout=10,
            )
            response.raise_for_status()
            fact = response.text.strip()
            return SkillResult(success=True, message=fact)
        except requests.RequestException as e:
            return SkillResult(success=False, message=f"I couldn't fetch that fact: {e}")

    def _get_math_fact(self) -> SkillResult:
        """Get a random math fact."""
        try:
            response = requests.get(
                "https://numbersapi.com/random/math",
                timeout=10,
            )
            response.raise_for_status()
            fact = response.text.strip()
            return SkillResult(success=True, message=f"Math fact: {fact}")
        except requests.RequestException as e:
            return SkillResult(success=False, message=f"I couldn't fetch a math fact: {e}")
