"""Tests for individual skills."""

import pytest
from jarvis.config import Config
from jarvis.skills.time_date import TimeDateSkill
from jarvis.skills.jokes import JokesSkill
from jarvis.skills.system_info import SystemInfoSkill
from jarvis.skills.web_search import WebSearchSkill


@pytest.fixture
def config():
    return Config()


def test_time_date_skill_matches(config):
    """Test that time/date skill matches appropriate triggers."""
    skill = TimeDateSkill(config)
    assert skill.matches("what time is it")
    assert skill.matches("what's the date")
    assert skill.matches("what day is today")
    assert not skill.matches("what's the weather")


def test_time_date_skill_execute(config):
    """Test that time/date skill returns a valid result."""
    skill = TimeDateSkill(config)
    result = skill.execute("what time is it", {})
    assert result.success is True
    assert "time" in result.message.lower()


def test_jokes_skill_matches(config):
    """Test that jokes skill matches triggers."""
    skill = JokesSkill(config)
    assert skill.matches("tell a joke")
    assert skill.matches("make me laugh")
    assert not skill.matches("what time is it")


def test_jokes_skill_execute(config):
    """Test that jokes skill returns a joke."""
    skill = JokesSkill(config)
    result = skill.execute("tell a joke", {})
    assert result.success is True
    assert len(result.message) > 0


def test_web_search_skill_extract(config):
    """Test that web search extracts the search term."""
    skill = WebSearchSkill(config)
    term = skill._extract_search_term("search for python tutorials")
    assert term == "python tutorials"


def test_system_info_skill_matches(config):
    """Test that system info skill matches triggers."""
    skill = SystemInfoSkill(config)
    assert skill.matches("system info")
    assert skill.matches("cpu usage")
    assert skill.matches("ram usage")
    assert not skill.matches("tell a joke")
