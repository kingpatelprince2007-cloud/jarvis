"""Translator skill — translate text using the free Google Translate web API."""

import requests
from .registry import Skill, SkillResult

# Common language codes
LANGUAGES = {
    "english": "en", "spanish": "es", "french": "fr", "german": "de",
    "italian": "it", "portuguese": "pt", "russian": "ru", "japanese": "ja",
    "chinese": "zh", "korean": "ko", "arabic": "ar", "hindi": "hi",
    "dutch": "nl", "polish": "pl", "turkish": "tr", "swedish": "sv",
    "hebrew": "he", "thai": "th", "vietnamese": "vi", "indonesian": "id",
}


class TranslatorSkill(Skill):
    name = "translator"
    description = "Translate text between languages"
    triggers = ["translate", "how do you say", "say in"]

    def execute(self, query: str, context: dict) -> SkillResult:
        target_lang, text = self._parse_query(query)

        if not text:
            return SkillResult(success=False, message="What would you like me to translate? Try 'translate hello to Spanish'.")

        if not target_lang:
            return SkillResult(success=False, message="Which language should I translate to? Try 'translate hello to Spanish'.")

        try:
            # Use Google Translate's free web endpoint (no API key needed)
            response = requests.get(
                "https://translate.googleapis.com/translate_a/single",
                params={
                    "client": "gtx",
                    "sl": "auto",
                    "tl": target_lang,
                    "dt": "t",
                    "q": text,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            # Response format: [[[translated, original, ...], ...], ...]
            translated_parts = [part[0] for part in data[0] if part[0]]
            translated_text = "".join(translated_parts)

            lang_name = self._get_lang_name(target_lang)
            return SkillResult(
                success=True,
                message=f"In {lang_name}: {translated_text}",
                data={"original": text, "translated": translated_text, "lang": target_lang}
            )
        except requests.RequestException as e:
            return SkillResult(success=False, message=f"I couldn't translate that: {e}")

    def _parse_query(self, query: str) -> tuple[str | None, str]:
        """Parse the query to extract target language and text to translate."""
        lower = query.lower()

        # Pattern: "translate <text> to <language>"
        if " to " in lower:
            # Find the language after "to"
            idx = lower.rfind(" to ")
            lang_part = lower[idx + 4:].strip()
            text = query[len("translate "):idx].strip() if lower.startswith("translate") else query[:idx].strip()

            # Clean up text if it starts with "how do you say"
            for trigger in self.triggers:
                if text.lower().startswith(trigger):
                    text = text[len(trigger):].strip()

            target_lang = self._get_lang_code(lang_part)
            return target_lang, text

        # Pattern: "how do you say <text> in <language>"
        if " in " in lower:
            idx = lower.rfind(" in ")
            lang_part = lower[idx + 4:].strip()
            text = query[:idx].strip()
            for trigger in self.triggers:
                if text.lower().startswith(trigger):
                    text = text[len(trigger):].strip()

            target_lang = self._get_lang_code(lang_part)
            return target_lang, text

        return None, ""

    def _get_lang_code(self, name: str) -> str | None:
        """Get the language code from a language name."""
        name = name.lower().strip()
        if name in LANGUAGES:
            return LANGUAGES[name]
        # Check if it's already a code
        if len(name) == 2:
            return name
        # Try partial match
        for lang_name, code in LANGUAGES.items():
            if name in lang_name or lang_name in name:
                return code
        return None

    def _get_lang_name(self, code: str) -> str:
        """Get the language name from a code."""
        for name, lang_code in LANGUAGES.items():
            if lang_code == code:
                return name.capitalize()
        return code
