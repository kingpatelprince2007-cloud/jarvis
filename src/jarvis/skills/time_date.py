"""Time and date skill."""

from datetime import datetime
from .registry import Skill, SkillResult


class TimeDateSkill(Skill):
    name = "time_date"
    description = "Get the current time and date"
    triggers = ["what time", "what's the time", "what day", "what's today", "what date", "what's the date", "current time", "current date"]

    def execute(self, query: str, context: dict) -> SkillResult:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")

        if "time" in query.lower():
            message = f"The current time is {time_str}."
        elif "day" in query.lower() or "date" in query.lower() or "today" in query.lower():
            message = f"Today is {date_str}."
        else:
            message = f"The current time is {time_str} on {date_str}."

        return SkillResult(success=True, message=message)
