"""Notes skill — save and retrieve notes."""

import json
from .registry import Skill, SkillResult


class NotesSkill(Skill):
    name = "notes"
    description = "Take notes, list notes, and save reminders"
    triggers = ["take a note", "save a note", "write down", "note this", "my notes", "show notes", "list notes"]

    def execute(self, query: str, context: dict) -> SkillResult:
        self.config.ensure_data_dir()

        lower = query.lower()

        if "show" in lower or "list" in lower or "my notes" in lower:
            return self._list_notes()
        else:
            return self._add_note(query)

    def _add_note(self, query: str) -> SkillResult:
        # Extract note content
        lower = query.lower()
        note_content = query
        for trigger in self.triggers:
            if trigger in lower:
                idx = lower.index(trigger) + len(trigger)
                note_content = query[idx:].strip()
                break

        if not note_content:
            return SkillResult(success=False, message="What would you like me to note?")

        notes = self._load_notes()
        from datetime import datetime
        notes.append({
            "content": note_content,
            "timestamp": datetime.now().isoformat()
        })
        self._save_notes(notes)

        return SkillResult(success=True, message=f"Note saved: '{note_content}'")

    def _list_notes(self) -> SkillResult:
        notes = self._load_notes()
        if not notes:
            return SkillResult(success=True, message="You have no saved notes.")

        from datetime import datetime
        lines = [f"You have {len(notes)} note(s):"]
        for i, note in enumerate(notes, 1):
            lines.append(f"{i}. {note['content']}")

        return SkillResult(success=True, message=" ".join(lines))

    def _load_notes(self) -> list:
        try:
            with open(self.config.notes_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_notes(self, notes: list):
        with open(self.config.notes_path, "w") as f:
            json.dump(notes, f, indent=2)
