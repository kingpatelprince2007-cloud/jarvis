"""Unit converter skill — convert between common units."""

from .registry import Skill, SkillResult

# Conversion factors to base unit
LENGTH_FACTORS = {
    "millimeter": ("mm", 0.001), "millimeter": ("mm", 0.001), "mm": ("mm", 0.001),
    "centimeter": ("cm", 0.01), "cm": ("cm", 0.01),
    "meter": ("m", 1.0), "m": ("m", 1.0),
    "kilometer": ("km", 1000.0), "km": ("km", 1000.0),
    "inch": ("in", 0.0254), "in": ("in", 0.0254),
    "foot": ("ft", 0.3048), "ft": ("ft", 0.3048), "feet": ("ft", 0.3048),
    "yard": ("yd", 0.9144), "yd": ("yd", 0.9144),
    "mile": ("mi", 1609.344), "mi": ("mi", 1609.344),
}

WEIGHT_FACTORS = {
    "milligram": ("mg", 0.001), "mg": ("mg", 0.001),
    "gram": ("g", 1.0), "g": ("g", 1.0),
    "kilogram": ("kg", 1000.0), "kg": ("kg", 1000.0),
    "ounce": ("oz", 28.3495), "oz": ("oz", 28.3495),
    "pound": ("lb", 453.592), "lb": ("lb", 453.592), "lbs": ("lb", 453.592),
    "ton": ("ton", 907185.0), "tonnes": ("tonne", 1000000.0), "tonne": ("tonne", 1000000.0),
}

TEMP_UNITS = {"celsius", "c", "fahrenheit", "f", "kelvin", "k"}

ALL_FACTORS = {**LENGTH_FACTORS, **WEIGHT_FACTORS}


class UnitConverterSkill(Skill):
    name = "unit_converter"
    description = "Convert between units (length, weight, temperature)"
    triggers = ["convert", "how many", "conversion"]

    def _normalize_unit(self, unit: str) -> str:
        """Normalize a unit name by handling plurals and aliases."""
        lower = unit.lower().strip()
        if lower in ALL_FACTORS:
            return lower
        # Try removing trailing 's' for plurals
        if lower.endswith('s') and lower[:-1] in ALL_FACTORS:
            return lower[:-1]
        # Try adding 's'
        if lower + 's' in ALL_FACTORS:
            return lower + 's'
        return lower

    def execute(self, query: str, context: dict) -> SkillResult:
        value, from_unit, to_unit = self._parse_query(query)

        if value is None or not from_unit or not to_unit:
            return SkillResult(
                success=False,
                message="Try a format like 'convert 5 feet to meters' or 'convert 100 fahrenheit to celsius'."
            )

        # Normalize units (handle plurals)
        from_unit = self._normalize_unit(from_unit)
        to_unit = self._normalize_unit(to_unit)

        # Temperature needs special handling
        if from_unit in TEMP_UNITS or to_unit in TEMP_UNITS:
            result = self._convert_temperature(value, from_unit, to_unit)
            if result is not None:
                return SkillResult(
                    success=True,
                    message=f"{value} {from_unit} is {result:.2f} {to_unit}.",
                    data={"from": from_unit, "to": to_unit, "value": value, "result": result}
                )
            return SkillResult(success=False, message=f"I can't convert between {from_unit} and {to_unit}.")

        # Length and weight conversions
        from_factor = ALL_FACTORS.get(from_unit.lower())
        to_factor = ALL_FACTORS.get(to_unit.lower())

        if not from_factor or not to_factor:
            return SkillResult(success=False, message=f"I don't recognize the units '{from_unit}' or '{to_unit}'.")

        # Convert to base then to target
        base_value = value * from_factor[1]
        result = base_value / to_factor[1]

        return SkillResult(
            success=True,
            message=f"{value} {from_unit} is {result:.4f} {to_unit}.",
            data={"from": from_unit, "to": to_unit, "value": value, "result": result}
        )

    def _parse_query(self, query: str) -> tuple:
        """Parse 'convert 5 feet to meters' style queries."""
        import re
        lower = query.lower()

        # Remove trigger words
        for trigger in self.triggers:
            lower = lower.replace(trigger, "")

        lower = lower.strip()

        # Pattern: <number> <unit> to <unit>
        match = re.match(r'(\d+\.?\d*)\s+(\w+)\s+to\s+(\w+)', lower)
        if match:
            value = float(match.group(1))
            from_unit = match.group(2)
            to_unit = match.group(3)
            return value, from_unit, to_unit

        # Pattern: how many <unit> in <number> <unit>
        match = re.match(r'(\w+)\s+in\s+(\d+\.?\d*)\s+(\w+)', lower)
        if match:
            to_unit = match.group(1)
            value = float(match.group(2))
            from_unit = match.group(3)
            return value, from_unit, to_unit

        return None, None, None

    def _convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float | None:
        """Convert between temperature units."""
        from_unit = from_unit.lower()[0]
        to_unit = to_unit.lower()[0]

        # Convert to Celsius first
        if from_unit == "c":
            celsius = value
        elif from_unit == "f":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "k":
            celsius = value - 273.15
        else:
            return None

        # Convert from Celsius to target
        if to_unit == "c":
            return celsius
        elif to_unit == "f":
            return celsius * 9 / 5 + 32
        elif to_unit == "k":
            return celsius + 273.15

        return None
