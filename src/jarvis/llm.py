"""LLM client — communicates with OpenAI-compatible APIs."""

from openai import OpenAI
from jarvis.config import Config


class LLMClient:
    """Wrapper around OpenAI-compatible chat completions."""

    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url,
        )
        self._messages: list[dict] = [
            {"role": "system", "content": config.personality}
        ]

    def chat(self, user_message: str) -> str:
        """Send a message to the LLM and return the response text.

        Maintains conversation history for context.
        """
        self._messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=self._messages,
            temperature=0.7,
            max_tokens=500,
        )

        assistant_message = response.choices[0].message.content
        self._messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def reset(self):
        """Clear conversation history."""
        self._messages = [
            {"role": "system", "content": self.config.personality}
        ]
