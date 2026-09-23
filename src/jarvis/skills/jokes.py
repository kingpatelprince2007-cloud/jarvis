"""Jokes skill — because even Jarvis needs to be entertaining."""

import random
from .registry import Skill, SkillResult

JOKES = [
    "Why did the AI cross the road? To optimize the chicken's path.",
    "I would tell you a UDP joke, but you might not get it.",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break. It said 'No problem, I'll go to sleep.'",
    "Why did the Python developer go broke? Because he used up all his cache.",
    "A SQL query walks into a bar, goes up to two tables and asks: 'Can I join you?'",
    "Why don't scientists trust atoms? Because they make up everything. Unlike me — I only make up jokes.",
    "I'm not saying I'm the best AI, but I did debug a program by staring at it once.",
    "How many programmers does it take to change a light bulb? None — that's a hardware problem.",
    "I would make a joke about artificial intelligence, but I'm afraid you wouldn't find it... natural.",
    "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
]


class JokesSkill(Skill):
    name = "jokes"
    description = "Tell a joke"
    triggers = ["tell a joke", "make me laugh", "say something funny", "joke", "funny"]

    def execute(self, query: str, context: dict) -> SkillResult:
        joke = random.choice(JOKES)
        return SkillResult(success=True, message=joke)
