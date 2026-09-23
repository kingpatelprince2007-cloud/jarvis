"""Tests for v1.2.0 skills."""

import pytest
from jarvis.config import Config
from jarvis.skills.world_clock import WorldClockSkill
from jarvis.skills.stopwatch import StopwatchSkill
from jarvis.skills.battery_status import BatteryStatusSkill
from jarvis.skills.file_search import FileSearchSkill
from jarvis.skills.qr_code import QRCodeSkill
from jarvis.skills.reminders import RemindersSkill
from jarvis.skills.calculator import CalculatorSkill, _safe_eval
import ast


@pytest.fixture
def config():
    return Config()


# === World Clock ===

class TestWorldClockSkill:
    def test_matches(self, config):
        skill = WorldClockSkill(config)
        assert skill.matches("time in tokyo")
        assert skill.matches("what time is it in london")
        assert skill.matches("world clock")
        assert not skill.matches("tell a joke")

    def test_get_timezone(self, config):
        skill = WorldClockSkill(config)
        assert skill._get_timezone("london") == "Europe/London"
        assert skill._get_timezone("tokyo") == "Asia/Tokyo"
        assert skill._get_timezone("new york") == "America/New_York"
        assert skill._get_timezone("sydney") == "Australia/Sydney"

    def test_get_timezone_partial(self, config):
        skill = WorldClockSkill(config)
        # "new" should partially match "new york"
        assert skill._get_timezone("new") is not None
        # "tok" should partially match "tokyo"
        assert skill._get_timezone("tok") is not None

    def test_extract_city(self, config):
        skill = WorldClockSkill(config)
        city = skill._extract_city("time in tokyo")
        assert city == "tokyo"
        city = skill._extract_city("what time is it in london")
        assert city == "london"

    def test_execute_known_city(self, config):
        skill = WorldClockSkill(config)
        result = skill.execute("time in london", {})
        assert result.success is True
        assert "london" in result.message.lower()

    def test_execute_unknown_city(self, config):
        skill = WorldClockSkill(config)
        result = skill.execute("time in mars", {})
        assert result.success is False


# === Stopwatch ===

class TestStopwatchSkill:
    def test_matches(self, config):
        skill = StopwatchSkill(config)
        assert skill.matches("start stopwatch")
        assert skill.matches("stop stopwatch")
        assert skill.matches("check stopwatch")
        assert not skill.matches("tell a joke")

    def test_start(self, config):
        skill = StopwatchSkill(config)
        # Reset state
        StopwatchSkill._running = False
        StopwatchSkill._start_time = None
        result = skill.execute("start stopwatch", {})
        assert result.success is True
        assert "started" in result.message.lower()

    def test_stop_without_start(self, config):
        skill = StopwatchSkill(config)
        StopwatchSkill._running = False
        StopwatchSkill._start_time = None
        result = skill.execute("stop stopwatch", {})
        assert result.success is False

    def test_check_without_running(self, config):
        skill = StopwatchSkill(config)
        StopwatchSkill._running = False
        StopwatchSkill._start_time = None
        result = skill.execute("check stopwatch", {})
        assert result.success is False


# === Battery Status ===

class TestBatteryStatusSkill:
    def test_matches(self, config):
        skill = BatteryStatusSkill(config)
        assert skill.matches("battery status")
        assert skill.matches("battery level")
        assert skill.matches("how much battery")
        assert not skill.matches("tell a joke")

    def test_execute(self, config):
        skill = BatteryStatusSkill(config)
        result = skill.execute("battery status", {})
        # Should succeed (either with battery info or "no battery" message)
        assert result.success is True


# === File Search ===

class TestFileSearchSkill:
    def test_matches(self, config):
        skill = FileSearchSkill(config)
        assert skill.matches("find file readme")
        assert skill.matches("search for file test")
        assert not skill.matches("tell a joke")

    def test_extract_search_term(self, config):
        skill = FileSearchSkill(config)
        term = skill._extract_search_term("find file readme")
        assert term == "readme"

    def test_format_size(self, config):
        skill = FileSearchSkill(config)
        assert "B" in skill._format_size(500)
        assert "KB" in skill._format_size(2048)
        assert "MB" in skill._format_size(2 * 1024 * 1024)


# === QR Code ===

class TestQRCodeSkill:
    def test_matches(self, config):
        skill = QRCodeSkill(config)
        assert skill.matches("generate qr code for hello")
        assert skill.matches("create qr code")
        assert not skill.matches("tell a joke")

    def test_extract_data(self, config):
        skill = QRCodeSkill(config)
        data = skill._extract_data("generate qr code for https://example.com")
        assert data == "https://example.com"

    def test_sanitize_filename(self, config):
        skill = QRCodeSkill(config)
        assert skill._sanitize_filename("hello world") == "hello_world"
        assert skill._sanitize_filename("https://example.com") == "https___example_com"


# === Reminders ===

class TestRemindersSkill:
    def test_matches(self, config):
        skill = RemindersSkill(config)
        assert skill.matches("remind me to call mom")
        assert skill.matches("set a reminder")
        assert skill.matches("list reminders")
        assert skill.matches("delete reminder 1")
        assert not skill.matches("tell a joke")

    def test_add_and_list(self, config, tmp_path, monkeypatch):
        monkeypatch.setenv("JARVIS_DATA_DIR", str(tmp_path))
        cfg = Config()
        skill = RemindersSkill(cfg)

        # Add a reminder
        result = skill.execute("remind me to buy groceries", {})
        assert result.success is True
        assert "buy groceries" in result.message

        # List reminders
        result = skill.execute("list reminders", {})
        assert result.success is True
        assert "buy groceries" in result.message

    def test_delete_reminder(self, config, tmp_path, monkeypatch):
        monkeypatch.setenv("JARVIS_DATA_DIR", str(tmp_path))
        cfg = Config()
        skill = RemindersSkill(cfg)

        # Add two reminders
        skill.execute("remind me to buy groceries", {})
        skill.execute("remind me to call mom", {})

        # Delete the first one
        result = skill.execute("delete reminder 1", {})
        assert result.success is True
        assert "groceries" in result.message

        # List should show only one
        result = skill.execute("list reminders", {})
        assert "call mom" in result.message
        assert "groceries" not in result.message


# === Calculator function calls ===

class TestCalculatorFunctions:
    def test_sqrt(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate sqrt(16)", {})
        assert result.success is True
        assert "4" in result.message

    def test_abs(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate abs(-5)", {})
        assert result.success is True
        assert "5" in result.message

    def test_round(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate round(3.7)", {})
        assert result.success is True
        assert "4" in result.message

    def test_min_max(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate max(5, 3, 8)", {})
        assert result.success is True
        assert "8" in result.message

    def test_factorial(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate math.factorial(5)", {})
        assert result.success is True
        assert "120" in result.message

    def test_sin(self, config):
        import math
        skill = CalculatorSkill(config)
        result = skill.execute("calculate math.sin(0)", {})
        assert result.success is True
        assert "0" in result.message

    def test_disallowed_function(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate eval('print(1)')", {})
        assert result.success is False

    def test_nested_expression(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate sqrt(abs(-16))", {})
        assert result.success is True
        assert "4" in result.message
