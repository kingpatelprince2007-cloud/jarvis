# JARVIS - AI Assistant

> "Sometimes you gotta run before you can walk." — Tony Stark

A Python-based AI assistant inspired by Iron Man's JARVIS. Features voice input, text-to-speech, LLM-powered conversation, and a modular skill system.

## Features

- **Voice Recognition** — Listen to voice commands with a typed-input fallback
- **Text-to-Speech** — Jarvis speaks back to you
- **LLM Brain** — Powered by OpenAI-compatible APIs (OpenAI, Groq, Ollama, LM Studio, etc.)
- **Modular Skills** — Easily extensible plugin system for new capabilities
- **Built-in Skills:**
  - Weather lookups
  - Web search
  - System information (CPU, RAM, disk)
  - Notes & task management
  - Open applications and websites
  - Time and date
  - Jokes
  - AI conversation

## Quick Start

### Prerequisites

- Python 3.10+
- An OpenAI-compatible API key (OpenAI, Groq, Ollama, LM Studio, etc.)
- System dependencies for voice (see below)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/jarvis.git
cd jarvis

# Install the package
pip install -e .

# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env
```

### System Dependencies (Voice)

**macOS:**
```bash
brew install portaudio
```

**Ubuntu/Debian:**
```bash
sudo apt install portaudio19-dev python3-pyaudio flac
```

**Windows:**
PyAudio wheels are pre-built — no system dependencies needed.

### Running

```bash
# Start Jarvis
python -m jarvis

# Or after pip install
jarvis
```

## Configuration

All configuration is via environment variables in `.env`:

| Variable | Default | Description |
|---|---|---|
| `JARVIS_LLM_API_KEY` | — | Your API key for the LLM provider |
| `JARVIS_LLM_BASE_URL` | `https://api.openai.com/v1` | Base URL for OpenAI-compatible API |
| `JARVIS_LLM_MODEL` | `gpt-4o-mini` | Model name |
| `JARVIS_TTS_ENABLED` | `true` | Enable/disable text-to-speech |
| `JARVIS_VOICE_INPUT_ENABLED` | `true` | Enable/disable voice input |
| `JARVIS_NAME` | `Jarvis` | The assistant's name |
| `JARVIS_USER_NAME` | `Sir` | How Jarvis addresses you |
| `JARVIS_PERSONALITY` | (see .env.example) | System prompt personality |
| `JARVIS_LOG_LEVEL` | `INFO` | Logging level |

## Adding Skills

Create a new skill by adding a Python file in `src/jarvis/skills/`:

```python
from .registry import Skill, SkillResult

class MySkill(Skill):
    name = "my_skill"
    description = "Does something cool"
    triggers = ["do something cool", "my skill"]

    def execute(self, query: str, context: dict) -> SkillResult:
        # Your logic here
        return SkillResult(success=True, message="Done!", data={})
```

The skill is automatically registered when the module loads.

## Project Structure

```
jarvis/
├── src/jarvis/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── assistant.py          # Main assistant loop
│   ├── config.py             # Configuration loader
│   ├── llm.py                # LLM client
│   ├── speech.py             # Voice I/O
│   └── skills/
│       ├── registry.py       # Skill base classes & registry
│       ├── weather.py
│       ├── web_search.py
│       ├── system_info.py
│       ├── notes.py
│       ├── open_app.py
│       ├── jokes.py
│       └── time_date.py
├── tests/
├── docs/
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

## License

MIT — See [LICENSE](LICENSE) file.

## Disclaimer

Jarvis is a fan project inspired by the Marvel Cinematic Universe. Not affiliated with Marvel, Disney, or any related entity. "JARVIS" is a trademark of Marvel Entertainment.
