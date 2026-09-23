"""Weather skill — fetches current weather via wttr.in (no API key needed)."""

import requests
from .registry import Skill, SkillResult


class WeatherSkill(Skill):
    name = "weather"
    description = "Get current weather for a location"
    triggers = ["weather", "temperature outside", "how's the weather", "what's it like outside"]

    def execute(self, query: str, context: dict) -> SkillResult:
        # Try to extract a location from the query
        location = self._extract_location(query)

        try:
            response = requests.get(
                f"https://wttr.in/{location}?format=%C+%t+%h+%w",
                timeout=10,
                headers={"User-Agent": "Jarvis/1.0"}
            )
            response.raise_for_status()
            weather_data = response.text.strip()

            # Format: "Partly cloudy +72°F +45% ↓5mph"
            parts = weather_data.replace("+", "").replace("↓", "Wind: ").replace("↑", "Wind: ")
            location_label = location if location != "" else "your location"

            return SkillResult(
                success=True,
                message=f"Current weather for {location_label}: {parts}"
            )
        except requests.RequestException as e:
            return SkillResult(
                success=False,
                message=f"I couldn't fetch the weather. {str(e)}"
            )

    def _extract_location(self, query: str) -> str:
        """Extract a location from the query string."""
        lower = query.lower()
        # Remove trigger words
        for trigger in self.triggers:
            lower = lower.replace(trigger, "")
        # Remove common filler words
        for word in ["in", "for", "at", "the", "like", "outside"]:
            lower = lower.replace(f" {word} ", " ")
        location = lower.strip()
        return location if location else ""
