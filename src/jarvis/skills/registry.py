"""Skill registry — base classes and automatic registration system."""

from __future__ import annotations
import importlib
import pkgutil
from dataclasses import dataclass, field
from typing import Any

from jarvis.config import Config


@dataclass
class SkillResult:
    """Result of a skill execution."""
    success: bool = True
    message: str = ""
    data: dict = field(default_factory=dict)
    should_speak: bool = True  # Whether to speak the message via TTS


class Skill:
    """Base class for all Jarvis skills.

    Subclasses must define:
        name: short identifier
        description: what the skill does
        triggers: list of phrases that activate this skill (lowercase)
    """
    name: str = ""
    description: str = ""
    triggers: list[str] = []

    def __init__(self, config: Config):
        self.config = config

    def matches(self, query: str) -> bool:
        """Check if this skill should handle the given query."""
        query_lower = query.lower().strip()
        return any(trigger in query_lower for trigger in self.triggers)

    def execute(self, query: str, context: dict) -> SkillResult:
        """Execute the skill. Override in subclasses."""
        raise NotImplementedError

    def __repr__(self):
        return f"<Skill: {self.name}>"


class SkillRegistry:
    """Manages skill registration and routing."""

    def __init__(self, config: Config):
        self.config = config
        self._skills: list[Skill] = []

    def register(self, skill: Skill):
        """Register a skill instance."""
        self._skills.append(skill)

    def auto_discover(self):
        """Automatically discover and register all skills in the skills package."""
        from jarvis.skills import skill_modules
        for module_name in skill_modules:
            try:
                module = importlib.import_module(f"jarvis.skills.{module_name}")
                # Look for Skill subclasses defined in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type)
                            and issubclass(attr, Skill)
                            and attr is not Skill
                            and attr.__module__ == module.__name__):
                        self.register(attr(self.config))
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(
                    f"Failed to load skill module '{module_name}': {e}"
                )

    def find_skill(self, query: str) -> Skill | None:
        """Find the first skill that matches the query."""
        for skill in self._skills:
            if skill.matches(query):
                return skill
        return None

    def execute(self, query: str, context: dict | None = None) -> SkillResult | None:
        """Find and execute a matching skill. Returns None if no match."""
        skill = self.find_skill(query)
        if skill is None:
            return None

        try:
            return skill.execute(query, context or {})
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Skill '{skill.name}' encountered an error: {e}",
            )

    def list_skills(self) -> list[dict]:
        """List all registered skills for display."""
        return [
            {"name": s.name, "description": s.description, "triggers": s.triggers}
            for s in self._skills
        ]
