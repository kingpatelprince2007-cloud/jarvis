"""Reminders skill — set and manage persistent reminders."""

import json
from datetime import datetime
from .registry import Skill, SkillResult


class RemindersSkill(Skill):
    name = "reminders"
    description = "Set, list, and remove reminders"
    triggers = ["remind me", "set a reminder", "create a reminder", "list reminders", "show reminders", "my reminders", "delete reminder", "remove reminder"]

    def execute(self, query: str, context: dict) -> SkillResult:
        self.config.ensure_data_dir()
        lower = query.lower()

        if "list" in lower or "show" in lower or "my reminders" in lower:
            return self._list_reminders()
        elif "delete" in lower or "remove" in lower:
            return self._delete_reminder(query)
        else:
            return self._add_reminder(query)

    def _add_reminder(self, query: str) -> SkillResult:
        """Add a new reminder."""
        lower = query.lower()
        reminder_text = query

        for trigger in self.triggers:
            if lower.startswith(trigger):
                reminder_text = query[len(trigger):].strip()
                break

        if not reminder_text:
            return SkillResult(success=False, message="What would you like me to remind you about?")

        reminders = self._load_reminders()
        reminder = {
            "text": reminder_text,
            "created": datetime.now().isoformat(),
            "completed": False,
        }
        reminders.append(reminder)
        self._save_reminders(reminders)

        return SkillResult(success=True, message=f"Reminder set: '{reminder_text}'")

    def _list_reminders(self) -> SkillResult:
        """List all active reminders."""
        reminders = self._load_reminders()
        active = [r for r in reminders if not r.get("completed", False)]

        if not active:
            return SkillResult(success=True, message="You have no active reminders.")

        lines = [f"You have {len(active)} reminder(s):"]
        for i, reminder in enumerate(active, 1):
            lines.append(f"  {i}. {reminder['text']}")

        return SkillResult(success=True, message="\n".join(lines))

    def _delete_reminder(self, query: str) -> SkillResult:
        """Delete a reminder by number."""
        import re
        match = re.search(r'(\d+)', query)
        if not match:
            return SkillResult(success=False, message="Which reminder number would you like to remove?")

        idx = int(match.group(1)) - 1
        reminders = self._load_reminders()
        active = [r for r in reminders if not r.get("completed", False)]

        if idx < 0 or idx >= len(active):
            return SkillResult(success=False, message=f"Invalid reminder number. You have {len(active)} reminder(s).")

        # Mark as completed
        reminder_text = active[idx]["text"]
        for r in reminders:
            if r["text"] == reminder_text and not r.get("completed", False):
                r["completed"] = True
                break

        self._save_reminders(reminders)
        return SkillResult(success=True, message=f"Reminder removed: '{reminder_text}'")

    def _load_reminders(self) -> list:
        """Load reminders from the data file."""
        filepath = self.config.data_dir / "reminders.json"
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_reminders(self, reminders: list):
        """Save reminders to the data file."""
        filepath = self.config.data_dir / "reminders.json"
        with open(filepath, "w") as f:
            json.dump(reminders, f, indent=2)
