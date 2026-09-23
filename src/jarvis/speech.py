"""Speech I/O — voice recognition and text-to-speech."""

import logging
from jarvis.config import Config

logger = logging.getLogger(__name__)


class SpeechEngine:
    """Handles text-to-speech and voice recognition with graceful fallbacks."""

    def __init__(self, config: Config):
        self.config = config
        self._tts = None
        self._recognizer = None

        if config.tts_enabled:
            self._init_tts()

        if config.voice_input_enabled:
            self._init_recognizer()

    def _init_tts(self):
        """Initialize the text-to-speech engine."""
        try:
            import pyttsx3
            self._tts = pyttsx3.init()
            # Set a slightly faster, clearer voice
            self._tts.setProperty("rate", 180)
            voices = self._tts.getProperty("voices")
            if voices:
                # Prefer a male voice if available
                for voice in voices:
                    if "male" in voice.name.lower() or "david" in voice.name.lower():
                        self._tts.setProperty("voice", voice.id)
                        break
            logger.info("Text-to-speech initialized.")
        except Exception as e:
            logger.warning(f"TTS initialization failed: {e}. Speech output disabled.")
            self._tts = None

    def _init_recognizer(self):
        """Initialize the speech recognizer."""
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._recognizer.energy_threshold = 4000
            logger.info("Voice recognition initialized.")
        except Exception as e:
            logger.warning(f"Voice recognition initialization failed: {e}. Voice input disabled.")
            self._recognizer = None

    def speak(self, text: str):
        """Speak text aloud. Falls back to printing if TTS is unavailable."""
        if self._tts:
            try:
                self._tts.say(text)
                self._tts.runAndWait()
                return
            except Exception as e:
                logger.warning(f"TTS error: {e}")
        print(f"\n[{self.config.name}]: {text}")

    def listen(self) -> str | None:
        """Listen for a voice command and return transcribed text.

        Returns None if voice input is unavailable or fails.
        """
        if not self._recognizer:
            return None

        try:
            import speech_recognition as sr
            with sr.Microphone() as source:
                print("Listening...")
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(source, timeout=10, phrase_time_limit=10)

            try:
                text = self._recognizer.recognize_google(audio)
                logger.info(f"Heard: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("(Sorry, I didn't catch that.)")
                return ""
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")
                return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None

    def get_input(self) -> str:
        """Get user input — tries voice first, falls back to typing."""
        if self.config.voice_input_enabled and self._recognizer:
            text = self.listen()
            if text:
                return text
            # If voice failed, prompt for typed input
            print("(Voice input unavailable. Please type your command.)")

        return input("\n> ").strip()
