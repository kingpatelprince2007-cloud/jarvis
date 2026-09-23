# JARVIS - AI Assistant

> "Sometimes you gotta run before you can walk." — Tony Stark

A Python-based AI assistant inspired by Iron Man's JARVIS. Features voice input, text-to-speech, LLM-powered conversation, and a modular skill system with 22 built-in skills.

## Features

- **Voice Recognition** — Listen to voice commands with a typed-input fallback
- **Text-to-Speech** — Jarvis speaks back to you
- **LLM Brain** — Powered by OpenAI-compatible APIs (OpenAI, Groq, Ollama, LM Studio, etc.)
- **Modular Skills** — Easily extensible plugin system for new capabilities
- **22 Built-in Skills** — See the full list below
- **Docker Support** — Run Jarvis in a container (text mode)
- **CI/CD** — Automated testing via GitHub Actions

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
pip install -e ".[dev]"

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

### Docker

```bash
# Build and run in text mode
docker-compose up -d
docker exec -it jarvis python -m jarvis

# Or build manually
docker build -t jarvis .
docker run -it -e JARVIS_LLM_API_KEY=your-key jarvis
```

> Note: Voice features (TTS, speech recognition) are disabled in Docker. Use text mode only.

## Skills (22 total)

| # | Skill | Example Command | Description |
|---|---|---|---|
| 1 | Time & Date | "what time is it" | Current time and date |
| 2 | World Clock | "time in tokyo" | Time in 30+ cities worldwide |
| 3 | Stopwatch | "start stopwatch" | Track elapsed time |
| 4 | Timer | "set a timer for 5 minutes" | Countdown timer |
| 5 | Battery Status | "battery status" | Battery level and charging info |
| 6 | IP Address | "what's my ip" | Local and public IP |
| 7 | Currency Converter | "convert 100 usd to eur" | Live exchange rates |
| 8 | Unit Converter | "convert 10 feet to meters" | Length, weight, temperature |
| 9 | Calculator | "calculate 15 * 23" | Safe math evaluation with functions |
| 10 | System Info | "system info" | CPU, RAM, disk usage |
| 11 | File Search | "find file readme" | Search for files by name |
| 12 | Weather | "weather in Chicago" | Current conditions via wttr.in |
| 13 | News | "tech news" | Top headlines via Hacker News |
| 14 | Web Search | "search for python" | Opens browser search |
| 15 | Translator | "translate hello to spanish" | 20+ languages |
| 16 | Reminders | "remind me to call mom" | Persistent reminders |
| 17 | Notes | "take a note" | Save and list notes |
| 18 | Password Generator | "generate a password" | Secure random passwords |
| 19 | QR Code | "generate qr for example.com" | QR code PNG files |
| 20 | Random Facts | "random fact" | Trivia via Numbers API |
| 21 | Open Apps | "open youtube.com" | Launch apps and websites |
| 22 | Jokes | "tell a joke" | Programming humor |

### Calculator Functions

The calculator supports basic operators (+, -, *, /, **, %, //) plus:

| Function | Example |
|---|---|
| `sqrt(x)` | "calculate sqrt(16)" → 4 |
| `abs(x)` | "calculate abs(-5)" → 5 |
| `round(x)` | "calculate round(3.7)" → 4 |
| `min(a, b, ...)` | "calculate max(5, 3, 8)" → 8 |
| `math.factorial(x)` | "calculate math.factorial(5)" → 120 |
| `math.sin(x)` | "calculate math.sin(0)" → 0 |
| `math.cos(x)` | "calculate math.cos(0)" → 1 |
| `math.log(x)` | "calculate math.log(10)" → 2.303 |
| `math.log10(x)` | "calculate math.log10(100)" → 2 |

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
| `JARVIS_DATA_DIR` | `data` | Directory for notes, reminders, etc. |

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

Add the module name to `skill_modules` in `src/jarvis/skills/__init__.py`. The skill is automatically registered when the module loads. See `docs/CONTRIBUTING.md` for full instructions.

## Project Structure

```
jarvis/
├── .github/workflows/
│   └── ci.yml                # GitHub Actions CI pipeline
├── src/jarvis/
│   ├── __init__.py
│   ├── __main__.py            # Entry point
│   ├── assistant.py           # Main assistant loop
│   ├── config.py              # Configuration loader
│   ├── llm.py                 # LLM client
│   ├── speech.py              # Voice I/O
│   └── skills/
│       ├── registry.py        # Skill base classes & registry
│       ├── time_date.py
│       ├── world_clock.py
│       ├── stopwatch.py
│       ├── timer.py
│       ├── battery_status.py
│       ├── calculator.py
│       ├── currency_converter.py
│       ├── unit_converter.py
│       ├── system_info.py
│       ├── ip_address.py
│       ├── file_search.py
│       ├── weather.py
│       ├── news.py
│       ├── web_search.py
│       ├── translator.py
│       ├── reminders.py
│       ├── notes.py
│       ├── password_generator.py
│       ├── qr_code.py
│       ├── random_fact.py
│       ├── open_app.py
│       └── jokes.py
├── tests/                     # 77 unit tests
├── docs/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── pyproject.toml
├── requirements.txt
├── CHANGELOG.md
└── README.md
```

## Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=jarvis --cov-report=term-missing
```

## License

MIT — See [LICENSE](LICENSE) file.

## Disclaimer

Jarvis is a fan project inspired by the Marvel Cinematic Universe. Not affiliated with Marvel, Disney, or any related entity. "JARVIS" is a trademark of Marvel Entertainment.
