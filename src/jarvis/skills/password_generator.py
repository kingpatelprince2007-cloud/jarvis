"""Password generator skill — create secure random passwords."""

import secrets
import string
from .registry import Skill, SkillResult


class PasswordGeneratorSkill(Skill):
    name = "password_generator"
    description = "Generate secure random passwords"
    triggers = ["generate a password", "create a password", "password", "make a password", "new password"]

    def execute(self, query: str, context: dict) -> SkillResult:
        length = self._parse_length(query)

        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*-_=+?"

        # Ensure at least one of each type
        all_chars = lowercase + uppercase + digits + symbols

        password_chars = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(symbols),
        ]

        # Fill the rest randomly
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))

        # Shuffle the characters
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        # Calculate strength
        strength = self._estimate_strength(length)

        return SkillResult(
            success=True,
            message=f"Generated a {length}-character password: {password}\nStrength: {strength}",
            data={"password": password, "length": length, "strength": strength}
        )

    def _parse_length(self, query: str) -> int:
        """Extract password length from query, default to 16."""
        import re
        match = re.search(r'(\d+)', query)
        if match:
            length = int(match.group(1))
            # Clamp to reasonable range
            return max(8, min(64, length))
        return 16

    def _estimate_strength(self, length: int) -> str:
        """Estimate password strength based on length."""
        if length >= 20:
            return "Very Strong"
        elif length >= 16:
            return "Strong"
        elif length >= 12:
            return "Good"
        else:
            return "Fair"
