"""Tests for configuration loading."""

import os
import pytest
from jarvis.config import Config


def test_default_config():
    """Test that default config values are sensible."""
    # Clear env vars for a clean test
    config = Config()
    assert config.name == "Jarvis"
    assert config.user_name == "Sir"
    assert config.tts_enabled is True or config.tts_enabled is False
    assert config.log_level == "INFO"


def test_config_from_env(monkeypatch):
    """Test that config reads from environment variables."""
    monkeypatch.setenv("JARVIS_NAME", "Friday")
    monkeypatch.setenv("JARVIS_USER_NAME", "Boss")
    monkeypatch.setenv("JARVIS_TTS_ENABLED", "false")
    monkeypatch.setenv("JARVIS_LLM_API_KEY", "test-key")

    config = Config()
    assert config.name == "Friday"
    assert config.user_name == "Boss"
    assert config.tts_enabled is False
    assert config.llm_api_key == "test-key"


def test_has_llm_key_false_for_placeholder(monkeypatch):
    """Test that placeholder key returns False for has_llm_key."""
    monkeypatch.setenv("JARVIS_LLM_API_KEY", "your-api-key-here")
    config = Config()
    assert config.has_llm_key() is False


def test_has_llm_key_true_for_real_key(monkeypatch):
    """Test that a real key returns True for has_llm_key."""
    monkeypatch.setenv("JARVIS_LLM_API_KEY", "sk-real-key-12345")
    config = Config()
    assert config.has_llm_key() is True


def test_ensure_data_dir(tmp_path, monkeypatch):
    """Test that data directory is created."""
    monkeypatch.setenv("JARVIS_DATA_DIR", str(tmp_path / "test_data"))
    config = Config()
    config.ensure_data_dir()
    assert (tmp_path / "test_data").exists()
