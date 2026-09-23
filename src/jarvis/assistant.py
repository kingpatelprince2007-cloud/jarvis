"""Main Jarvis assistant — orchestrates skills, LLM, and speech."""

import logging
import sys

from jarvis.config import Config
from jarvis.llm import LLMClient
from jarvis.speech import SpeechEngine
from jarvis.skills.registry import SkillRegistry

logger = logging.getLogger(__name__)


class Jarvis:
    """The main assistant class that ties everything together."""

    # Commands that control Jarvis itself (not routed to skills or LLM)
    EXIT_COMMANDS = ["exit", "quit", "shutdown", "goodbye", "bye", "stop"]
    HELP_COMMANDS = ["help", "what can you do", "list skills", "commands"]
    RESET_COMMANDS = ["reset", "clear memory", "forget", "new conversation"]

    def __init__(self):
        self.config = Config()
        self._setup_logging()
        self.speech = SpeechEngine(self.config)
        self.skills = SkillRegistry(self.config)
        self.skills.auto_discover()
        self.llm = None  # Lazy-init when first needed

        self._running = False

    def _setup_logging(self):
        level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )

    def _get_llm(self) -> LLMClient | None:
        """Lazy-initialize the LLM client."""
        if self.llm is None:
            if not self.config.has_llm_key():
                logger.warning("No LLM API key configured. LLM features disabled.")
                return None
            try:
                self.llm = LLMClient(self.config)
            except Exception as e:
                logger.error(f"Failed to initialize LLM: {e}")
                return None
        return self.llm

    def _is_exit(self, query: str) -> bool:
        return any(query == cmd or query.startswith(cmd) for cmd in self.EXIT_COMMANDS)

    def _is_help(self, query: str) -> bool:
        return any(cmd in query for cmd in self.HELP_COMMANDS)

    def _is_reset(self, query: str) -> bool:
        return any(cmd in query for cmd in self.RESET_COMMANDS)

    def _handle_help(self):
        """Display available skills."""
        skills = self.skills.list_skills()
        lines = [f"Here's what I can do, {self.config.user_name}:"]
        for skill in skills:
            lines.append(f"  - {skill['description']} (try: \"{skill['triggers'][0]}...\")")
        lines.append("  - General conversation (just talk to me)")
        lines.append(f"  - Type 'exit' to shut me down.")
        message = "\n".join(lines)
        print(message)
        self.speech.speak(f"I can help with time, weather, web search, notes, system info, and general conversation. What do you need, {self.config.user_name}?")

    def _handle_reset(self):
        """Reset the LLM conversation."""
        if self.llm:
            self.llm.reset()
        message = "Conversation cleared. Starting fresh."
        self.speech.speak(message)

    def _process_command(self, query: str) -> bool:
        """Process a single command. Returns False if should exit."""
        query = query.strip()
        if not query:
            return True

        # Check for exit
        if self._is_exit(query):
            farewell = f"Goodbye, {self.config.user_name}."
            self.speech.speak(farewell)
            return False

        # Check for help
        if self._is_help(query):
            self._handle_help()
            return True

        # Check for reset
        if self._is_reset(query):
            self._handle_reset()
            return True

        # Try to match a skill
        result = self.skills.execute(query, {"config": self.config})
        if result is not None:
            if result.should_speak:
                self.speech.speak(result.message)
            else:
                print(result.message)
            return True

        # Fall back to LLM conversation
        llm = self._get_llm()
        if llm:
            response = llm.chat(query)
            self.speech.speak(response)
        else:
            no_llm_msg = (
                f"I don't have a specific skill for that, {self.config.user_name}, "
                "and no LLM API key is configured. Please set JARVIS_LLM_API_KEY in your .env file "
                "to enable general conversation."
            )
            self.speech.speak(no_llm_msg)

        return True

    def run(self):
        """Main loop — listen for commands and respond."""
        self._running = True

        from jarvis import __version__
        banner = f"""
╔══════════════════════════════════════════════════╗
║          JARVIS AI ASSISTANT v{__version__:<10}          ║
╚══════════════════════════════════════════════════╝

  Online and ready, {self.config.user_name}.
  Type 'help' for available commands.
  Type 'exit' to shut down.

{'─' * 50}
"""
        print(banner)

        greeting = f"Good day, {self.config.user_name}. How may I assist you?"
        self.speech.speak(greeting)

        while self._running:
            try:
                query = self.speech.get_input()
                if not query:
                    continue
                if not self._process_command(query):
                    self._running = False
            except KeyboardInterrupt:
                print()
                self.speech.speak(f"Shutting down. Goodbye, {self.config.user_name}.")
                self._running = False
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                self.speech.speak(f"I encountered an error. {str(e)}")

        sys.exit(0)
