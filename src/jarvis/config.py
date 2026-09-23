"""Configuration loader — reads from environment variables and .env file."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

DEFAULT_PERSONALITY = (
    "You are Jarvis, a sophisticated AI assistant inspired by the one from "
    "Iron Man. You are polite, witty, and efficient. Address the user as "
    "\"Sir\" unless told otherwise. Keep responses concise and helpful. "
    "You have a dry sense of humor but always prioritize being useful."
)


@dataclass
class Config:
    """Central configuration for Jarvis."""

    # LLM
    llm_api_key: str = field(default_factory=lambda: os.getenv("JARVIS_LLM_API_KEY", ""))
    llm_base_url: str = field(default_factory=lambda: os.getenv("JARVIS_LLM_BASE_URL", "https://api.openai.com/v1"))
    llm_model: str = field(default_factory=lambda: os.getenv("JARVIS_LLM_MODEL", "gpt-4o-mini"))

    # Voice
    tts_enabled: bool = field(default_factory=lambda: os.getenv("JARVIS_TTS_ENABLED", "true").lower() == "true")
    voice_input_enabled: bool = field(default_factory=lambda: os.getenv("JARVIS_VOICE_INPUT_ENABLED", "true").lower() == "true")

    # Personality
    name: str = field(default_factory=lambda: os.getenv("JARVIS_NAME", "Jarvis"))
    user_name: str = field(default_factory=lambda: os.getenv("JARVIS_USER_NAME", "Sir"))
    personality: str = field(default_factory=lambda: os.getenv("JARVIS_PERSONALITY", DEFAULT_PERSONALITY))

    # System
    log_level: str = field(default_factory=lambda: os.getenv("JARVIS_LOG_LEVEL", "INFO"))

    # Paths
    data_dir: Path = field(default_factory=lambda: Path(os.getenv("JARVIS_DATA_DIR", "data")))

    @property
    def notes_path(self) -> Path:
        return self.data_dir / "notes.json"

    @property
    def tasks_path(self) -> Path:
        return self.data_dir / "tasks.json"

    def ensure_data_dir(self):
        """Create the data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def has_llm_key(self) -> bool:
        """Check if an API key is configured."""
        return bool(self.llm_api_key and self.llm_api_key != "your-api-key-here")
