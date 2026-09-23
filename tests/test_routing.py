"""Tests for skill routing and the registry."""

import pytest
from jarvis.config import Config
from jarvis.skills.registry import SkillRegistry, Skill, SkillResult


@pytest.fixture
def config():
    return Config()


class DummySkill(Skill):
    """A test skill for routing tests."""
    name = "dummy"
    description = "A test skill"
    triggers = ["test", "dummy"]

    def execute(self, query: str, context: dict) -> SkillResult:
        return SkillResult(success=True, message="Test executed", data={"query": query})


class AnotherDummySkill(Skill):
    name = "another"
    description = "Another test skill"
    triggers = ["hello world"]

    def execute(self, query: str, context: dict) -> SkillResult:
        return SkillResult(success=True, message="Hello!")


def test_registry_register_and_find(config):
    """Test that skills can be registered and found."""
    registry = SkillRegistry(config)
    registry.register(DummySkill(config))
    registry.register(AnotherDummySkill(config))

    found = registry.find_skill("test this thing")
    assert found is not None
    assert found.name == "dummy"


def test_registry_no_match(config):
    """Test that registry returns None when no skill matches."""
    registry = SkillRegistry(config)
    registry.register(DummySkill(config))

    found = registry.find_skill("something completely unrelated")
    assert found is None


def test_registry_execute(config):
    """Test that registry executes the matched skill."""
    registry = SkillRegistry(config)
    registry.register(DummySkill(config))

    result = registry.execute("test please", {})
    assert result is not None
    assert result.success is True
    assert "Test executed" in result.message


def test_registry_execute_no_match(config):
    """Test that registry returns None when no skill matches."""
    registry = SkillRegistry(config)
    result = registry.execute("unrelated query", {})
    assert result is None


def test_registry_priority_order(config):
    """Test that first registered skill takes priority."""
    registry = SkillRegistry(config)
    registry.register(DummySkill(config))

    # If AnotherDummySkill also matched "test", DummySkill would win
    # since it was registered first
    found = registry.find_skill("test")
    assert found.name == "dummy"


def test_registry_auto_discover(config):
    """Test that auto_discover loads all skill modules."""
    registry = SkillRegistry(config)
    registry.auto_discover()

    # Should have loaded all skills from the skills package
    skill_names = [s.name for s in registry._skills]
    assert "time_date" in skill_names
    assert "jokes" in skill_names
    assert "weather" in skill_names
    assert "system_info" in skill_names


def test_registry_list_skills(config):
    """Test that list_skills returns skill info."""
    registry = SkillRegistry(config)
    registry.register(DummySkill(config))

    skills = registry.list_skills()
    assert len(skills) == 1
    assert skills[0]["name"] == "dummy"
    assert "test" in skills[0]["triggers"]
