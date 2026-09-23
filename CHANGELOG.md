# Changelog

All notable changes to the Jarvis AI Assistant project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.2.0] - 2026-09-23

### Added
- **World Clock skill** — Get the time in 30+ cities worldwide
- **Stopwatch skill** — Start, stop, and check elapsed time
- **Battery Status skill** — Check battery level, charging status, and time remaining
- **File Search skill** — Search for files by name across common directories
- **QR Code Generator skill** — Generate QR codes as PNG files for text, URLs, or data
- **Reminders skill** — Set, list, and delete persistent reminders
- **Calculator functions** — Now supports `sqrt`, `abs`, `round`, `min`, `max`, `sin`, `cos`, `tan`, `log`, `factorial`, and more
- **GitHub Actions CI** — Automated testing across Python 3.10, 3.11, and 3.12 with code coverage
- **Docker support** — Dockerfile and docker-compose.yml for containerized text-mode usage
- **CHANGELOG.md** — This file
- 24 new tests (77 total, all passing)

### Changed
- Password generator no longer speaks the password aloud (prints only for security)
- News skill description updated to reflect tech news from Hacker News
- Calculator now properly supports function calls via safe AST evaluation
- Skill priority reordered for better routing accuracy

### Fixed
- Calculator function aliases (`sqrt`, `round`, etc.) now actually work with safe AST evaluation
- Password generator `should_speak` set to False for security

## [1.1.0] - 2026-09-23

### Added
- **Calculator skill** — Safe math expression evaluation with AST parsing
- **Timer skill** — Countdown timers with background threads
- **News skill** — Tech headlines via Hacker News API
- **Translator skill** — 20+ languages via Google Translate
- **Unit Converter skill** — Length, weight, and temperature conversions
- **Password Generator skill** — Secure random passwords with strength rating
- **IP Address skill** — Local and public IP address lookup
- **Random Facts skill** — Trivia and math facts via Numbers API
- **Currency Converter skill** — Live exchange rates with caching
- Smart routing: calculator only matches queries with numbers
- Currency converter matches by currency code detection
- Unit converter handles plural forms
- 35 new tests (53 total, all passing)

## [1.0.0] - 2026-09-23

### Added
- Initial release
- Voice input with speech recognition + typed fallback
- Text-to-speech output
- LLM-powered conversation (OpenAI-compatible APIs)
- Modular skill system with auto-discovery
- 7 built-in skills: Time & Date, System Info, Weather, Web Search, Notes, Open Apps, Jokes
- Configuration via `.env` file
- 18 unit tests (all passing)
- MIT license
- README, CONTRIBUTING guide, .gitignore, .env.example
