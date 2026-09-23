"""World clock skill — get the time in multiple timezones."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from .registry import Skill, SkillResult

# Common timezones
TIMEZONES = {
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "denver": "America/Denver",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "madrid": "Europe/Madrid",
    "rome": "Europe/Rome",
    "moscow": "Europe/Moscow",
    "dubai": "Asia/Dubai",
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "bangkok": "Asia/Bangkok",
    "singapore": "Asia/Singapore",
    "hong kong": "Asia/Hong_Kong",
    "tokyo": "Asia/Tokyo",
    "seoul": "Asia/Seoul",
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "auckland": "Pacific/Auckland",
    "sao paulo": "America/Sao_Paulo",
    "mexico city": "America/Mexico_City",
    "toronto": "America/Toronto",
    "vancouver": "America/Vancouver",
    "amsterdam": "Europe/Amsterdam",
    "stockholm": "Europe/Stockholm",
    "istanbul": "Europe/Istanbul",
    "cairo": "Africa/Cairo",
    "johannesburg": "Africa/Johannesburg",
    "utc": "UTC",
    "gmt": "GMT",
}


class WorldClockSkill(Skill):
    name = "world_clock"
    description = "Get the time in cities around the world"
    triggers = ["time in", "what time is it in", "world clock", "timezone", "time zone"]

    def execute(self, query: str, context: dict) -> SkillResult:
        city = self._extract_city(query)

        if not city:
            # Show a few major cities
            return self._show_major_cities()

        tz_name = self._get_timezone(city)
        if not tz_name:
            return SkillResult(
                success=False,
                message=f"I don't have timezone information for '{city}'. Try cities like London, Tokyo, New York, Sydney, etc."
            )

        try:
            tz = ZoneInfo(tz_name)
            now = datetime.now(tz)
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d")

            city_display = city.title()
            return SkillResult(
                success=True,
                message=f"The time in {city_display} is {time_str} on {date_str}."
            )
        except Exception as e:
            return SkillResult(success=False, message=f"I couldn't get the time for {city}: {e}")

    def _extract_city(self, query: str) -> str:
        """Extract the city name from the query."""
        lower = query.lower()
        for trigger in self.triggers:
            if trigger in lower:
                idx = lower.index(trigger) + len(trigger)
                city = query[idx:].strip().rstrip("?").strip()
                return city.lower()
        return ""

    def _get_timezone(self, city: str) -> str | None:
        """Get the timezone name for a city."""
        city = city.lower().strip()
        if city in TIMEZONES:
            return TIMEZONES[city]
        # Try partial match
        for known_city, tz in TIMEZONES.items():
            if city in known_city or known_city in city:
                return tz
        return None

    def _show_major_cities(self) -> SkillResult:
        """Show the time in major cities around the world."""
        major = ["new york", "london", "paris", "tokyo", "sydney"]
        lines = ["Here's the time in major cities:"]

        for city in major:
            tz_name = TIMEZONES[city]
            try:
                tz = ZoneInfo(tz_name)
                now = datetime.now(tz)
                time_str = now.strftime("%I:%M %p")
                lines.append(f"  {city.title()}: {time_str}")
            except Exception:
                pass

        return SkillResult(success=True, message="\n".join(lines))
