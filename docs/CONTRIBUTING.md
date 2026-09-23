# Contributing to Jarvis

Thank you for your interest in contributing to Jarvis! Here's how to get started.

## Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/YOUR_USERNAME/jarvis.git
cd jarvis
pip install -e ".[dev]"

# Copy the example env
cp .env.example .env
# Add your API key to .env
```

## Running Tests

```bash
pytest -v
```

## Adding a New Skill

1. Create a new file in `src/jarvis/skills/` (e.g., `my_skill.py`)
2. Define a class inheriting from `Skill` with `name`, `description`, and `triggers`
3. Implement the `execute` method
4. Add the module name to `skill_modules` in `src/jarvis/skills/__init__.py`
5. Add tests in `tests/`

### Example

```python
from .registry import Skill, SkillResult

class CalculatorSkill(Skill):
    name = "calculator"
    description = "Perform calculations"
    triggers = ["calculate", "what is", "compute"]

    def execute(self, query: str, context: dict) -> SkillResult:
        # Parse and compute...
        return SkillResult(success=True, message="The answer is 42.")
```

## Code Style

- Use type hints
- Add docstrings to classes and functions
- Keep skills focused — one responsibility per skill
- Handle errors gracefully with `SkillResult(success=False, message=...)`

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-new-skill`)
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

## Reporting Issues

Please include:
- Your OS and Python version
- Steps to reproduce
- Expected vs actual behavior
- Any error messages
