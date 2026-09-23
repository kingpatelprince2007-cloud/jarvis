"""Tests for the new skills added in v2."""

import pytest
from jarvis.config import Config
from jarvis.skills.calculator import CalculatorSkill
from jarvis.skills.timer import TimerSkill
from jarvis.skills.unit_converter import UnitConverterSkill
from jarvis.skills.password_generator import PasswordGeneratorSkill
from jarvis.skills.currency_converter import CurrencyConverterSkill
from jarvis.skills.translator import TranslatorSkill
from jarvis.skills.news import NewsSkill
from jarvis.skills.random_fact import RandomFactSkill
from jarvis.skills.ip_address import IPAddressSkill


@pytest.fixture
def config():
    return Config()


# === Calculator ===

class TestCalculatorSkill:
    def test_matches(self, config):
        skill = CalculatorSkill(config)
        assert skill.matches("calculate 5 + 3")
        assert skill.matches("what is 2 plus 2")
        assert skill.matches("compute 10 * 5")
        assert not skill.matches("tell a joke")

    def test_addition(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate 5 + 3", {})
        assert result.success is True
        assert "8" in result.message

    def test_multiplication(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate 12 * 7", {})
        assert result.success is True
        assert "84" in result.message

    def test_division(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate 100 / 4", {})
        assert result.success is True
        assert "25" in result.message

    def test_power(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate 2 ** 10", {})
        assert result.success is True
        assert "1024" in result.message

    def test_division_by_zero(self, config):
        skill = CalculatorSkill(config)
        result = skill.execute("calculate 5 / 0", {})
        assert result.success is False
        assert "zero" in result.message.lower()

    def test_extract_expression(self, config):
        skill = CalculatorSkill(config)
        expr = skill._extract_expression("calculate 5 + 3")
        assert expr == "5 + 3"


# === Timer ===

class TestTimerSkill:
    def test_matches(self, config):
        skill = TimerSkill(config)
        assert skill.matches("set a timer for 5 minutes")
        assert skill.matches("timer for 30 seconds")
        assert not skill.matches("what time is it")

    def test_parse_minutes(self, config):
        skill = TimerSkill(config)
        seconds = skill._parse_duration("set a timer for 5 minutes")
        assert seconds == 300

    def test_parse_seconds(self, config):
        skill = TimerSkill(config)
        seconds = skill._parse_duration("timer for 30 seconds")
        assert seconds == 30

    def test_parse_combined(self, config):
        skill = TimerSkill(config)
        seconds = skill._parse_duration("timer for 2 minutes 30 seconds")
        assert seconds == 150

    def test_parse_hours(self, config):
        skill = TimerSkill(config)
        seconds = skill._parse_duration("timer for 1 hour")
        assert seconds == 3600

    def test_parse_invalid(self, config):
        skill = TimerSkill(config)
        seconds = skill._parse_duration("set a timer")
        assert seconds is None

    def test_execute_success(self, config):
        skill = TimerSkill(config)
        result = skill.execute("set a timer for 5 seconds", {})
        assert result.success is True
        assert "5 second" in result.message


# === Unit Converter ===

class TestUnitConverterSkill:
    def test_matches(self, config):
        skill = UnitConverterSkill(config)
        assert skill.matches("convert 5 feet to meters")
        assert skill.matches("how many inches in 1 foot")
        assert not skill.matches("tell a joke")

    def test_length_conversion(self, config):
        skill = UnitConverterSkill(config)
        result = skill.execute("convert 1 foot to meters", {})
        assert result.success is True
        assert "0.3048" in result.message

    def test_weight_conversion(self, config):
        skill = UnitConverterSkill(config)
        result = skill.execute("convert 1 kilogram to pounds", {})
        assert result.success is True

    def test_temperature_celsius_to_fahrenheit(self, config):
        skill = UnitConverterSkill(config)
        result = skill.execute("convert 100 celsius to fahrenheit", {})
        assert result.success is True
        assert "212" in result.message

    def test_temperature_fahrenheit_to_celsius(self, config):
        skill = UnitConverterSkill(config)
        result = skill.execute("convert 32 fahrenheit to celsius", {})
        assert result.success is True
        assert "0" in result.message

    def test_parse_query(self, config):
        skill = UnitConverterSkill(config)
        value, from_unit, to_unit = skill._parse_query("convert 5 feet to meters")
        assert value == 5
        assert from_unit == "feet"
        assert to_unit == "meters"


# === Password Generator ===

class TestPasswordGeneratorSkill:
    def test_matches(self, config):
        skill = PasswordGeneratorSkill(config)
        assert skill.matches("generate a password")
        assert skill.matches("create a password")
        assert not skill.matches("what time is it")

    def test_default_length(self, config):
        skill = PasswordGeneratorSkill(config)
        result = skill.execute("generate a password", {})
        assert result.success is True
        # Password is 16 chars + we can check the data
        assert result.data["length"] == 16

    def test_custom_length(self, config):
        skill = PasswordGeneratorSkill(config)
        result = skill.execute("generate a 24 character password", {})
        assert result.success is True
        assert result.data["length"] == 24

    def test_min_length_clamped(self, config):
        skill = PasswordGeneratorSkill(config)
        result = skill.execute("generate a 4 character password", {})
        assert result.data["length"] == 8

    def test_password_has_variety(self, config):
        skill = PasswordGeneratorSkill(config)
        result = skill.execute("generate a password", {})
        password = result.data["password"]
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)

    def test_strength_estimation(self, config):
        skill = PasswordGeneratorSkill(config)
        assert skill._estimate_strength(24) == "Very Strong"
        assert skill._estimate_strength(16) == "Strong"
        assert skill._estimate_strength(12) == "Good"
        assert skill._estimate_strength(8) == "Fair"


# === Currency Converter ===

class TestCurrencyConverterSkill:
    def test_matches(self, config):
        skill = CurrencyConverterSkill(config)
        assert skill.matches("convert 100 usd to eur")
        assert skill.matches("how much is 50 euros in dollars")
        assert not skill.matches("tell a joke")

    def test_normalize_currency(self, config):
        skill = CurrencyConverterSkill(config)
        assert skill._normalize_currency("dollar") == "usd"
        assert skill._normalize_currency("euros") == "eur"
        assert skill._normalize_currency("pounds") == "gbp"
        assert skill._normalize_currency("yen") == "jpy"

    def test_parse_query(self, config):
        skill = CurrencyConverterSkill(config)
        amount, from_curr, to_curr = skill._parse_query("convert 100 USD to EUR")
        assert amount == 100
        assert from_curr == "usd"
        assert to_curr == "eur"


# === Translator ===

class TestTranslatorSkill:
    def test_matches(self, config):
        skill = TranslatorSkill(config)
        assert skill.matches("translate hello to spanish")
        assert skill.matches("how do you say hello in french")
        assert not skill.matches("tell a joke")

    def test_get_lang_code(self, config):
        skill = TranslatorSkill(config)
        assert skill._get_lang_code("spanish") == "es"
        assert skill._get_lang_code("french") == "fr"
        assert skill._get_lang_code("en") == "en"

    def test_parse_query(self, config):
        skill = TranslatorSkill(config)
        lang, text = skill._parse_query("translate hello to spanish")
        assert lang == "es"
        assert text == "hello"


# === News ===

class TestNewsSkill:
    def test_matches(self, config):
        skill = NewsSkill(config)
        assert skill.matches("news")
        assert skill.matches("headlines")
        assert skill.matches("what's happening")
        assert not skill.matches("tell a joke")


# === Random Fact ===

class TestRandomFactSkill:
    def test_matches(self, config):
        skill = RandomFactSkill(config)
        assert skill.matches("random fact")
        assert skill.matches("tell me a fact")
        assert skill.matches("fun fact")
        assert not skill.matches("tell a joke")


# === IP Address ===

class TestIPAddressSkill:
    def test_matches(self, config):
        skill = IPAddressSkill(config)
        assert skill.matches("what's my ip")
        assert skill.matches("ip address")
        assert skill.matches("my ip")
        assert not skill.matches("tell a joke")
