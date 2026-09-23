"""Open applications and websites skill."""

import subprocess
import sys
import webbrowser
from .registry import Skill, SkillResult


class OpenAppSkill(Skill):
    name = "open_app"
    description = "Open applications or websites"
    triggers = ["open ", "launch ", "start "]

    def execute(self, query: str, context: dict) -> SkillResult:
        # Extract what to open
        lower = query.lower()
        target = ""
        for trigger in self.triggers:
            if lower.startswith(trigger):
                target = query[len(trigger):].strip()
                break

        if not target:
            return SkillResult(success=False, message="What would you like me to open?")

        # Check if it's a website
        if self._is_website(target):
            url = target if target.startswith("http") else f"https://{target}"
            webbrowser.open(url)
            return SkillResult(success=True, message=f"Opening {target} in your browser.")

        # Try to open as an application
        result = self._open_application(target)
        return result

    def _is_website(self, target: str) -> bool:
        web_indicators = [".com", ".org", ".net", ".io", ".dev", "www."]
        return any(indicator in target.lower() for indicator in web_indicators)

    def _open_application(self, app_name: str) -> SkillResult:
        """Open an application based on the OS."""
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", "-a", app_name])
            elif sys.platform == "win32":
                subprocess.Popen(["start", app_name], shell=True)
            elif sys.platform.startswith("linux"):
                subprocess.Popen([app_name])
            else:
                return SkillResult(success=False, message=f"I can't open applications on this platform.")

            return SkillResult(success=True, message=f"Opening {app_name}.")
        except FileNotFoundError:
            return SkillResult(success=False, message=f"I couldn't find an application called '{app_name}'.")
        except Exception as e:
            return SkillResult(success=False, message=f"I couldn't open {app_name}: {e}")
