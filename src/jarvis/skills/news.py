"""News skill — fetch top headlines via a free news API."""

import requests
from .registry import Skill, SkillResult


class NewsSkill(Skill):
    name = "news"
    description = "Get the latest news headlines"
    triggers = ["news", "headlines", "what's happening", "what's going on in the world", "today's news"]

    def execute(self, query: str, context: dict) -> SkillResult:
        try:
            # Use the free Hacker News API as a fallback (no key needed)
            response = requests.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json",
                timeout=10,
            )
            response.raise_for_status()
            story_ids = response.json()[:5]

            headlines = []
            for story_id in story_ids:
                story_resp = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=10,
                )
                story_resp.raise_for_status()
                story = story_resp.json()
                if story and "title" in story:
                    title = story["title"]
                    url = story.get("url", "")
                    headlines.append(f"- {title}" + (f" ({url})" if url else ""))

            if not headlines:
                return SkillResult(success=False, message="I couldn't find any news headlines right now.")

            message = "Here are today's top headlines:\n" + "\n".join(headlines)
            return SkillResult(success=True, message=message)
        except requests.RequestException as e:
            return SkillResult(success=False, message=f"I couldn't fetch the news: {e}")
