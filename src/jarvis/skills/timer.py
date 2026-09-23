"""Timer skill — set countdown timers."""

import threading
import time
from datetime import datetime, timedelta
from .registry import Skill, SkillResult


class TimerSkill(Skill):
    name = "timer"
    description = "Set countdown timers"
    triggers = ["set a timer", "set timer", "start a timer", "countdown", "timer for"]

    # Active timers stored at class level so they persist across skill calls
    _timers: dict = {}
    _lock = threading.Lock()

    def execute(self, query: str, context: dict) -> SkillResult:
        seconds = self._parse_duration(query)

        if seconds is None:
            return SkillResult(success=False, message="For how long? Try 'set a timer for 5 minutes' or 'timer for 2 minutes 30 seconds'.")

        timer_id = f"timer_{len(self._timers) + 1}"
        end_time = datetime.now() + timedelta(seconds=seconds)

        with self._lock:
            self._timers[timer_id] = {
                "end_time": end_time,
                "duration": seconds,
                "active": True,
            }

        # Start the timer in a background thread
        def _timer_callback():
            time.sleep(seconds)
            with self._lock:
                if timer_id in self._timers:
                    self._timers[timer_id]["active"] = False
            mins, secs = divmod(seconds, 60)
            duration_str = f"{mins} minute{'s' if mins != 1 else ''} and {secs} second{'s' if secs != 1 else ''}"
            print(f"\n[TIMER] {duration_str} timer has finished!\n")

        thread = threading.Thread(target=_timer_callback, daemon=True)
        thread.start()

        mins, secs = divmod(seconds, 60)
        if mins > 0 and secs > 0:
            duration_str = f"{mins} minute{'s' if mins != 1 else ''} and {secs} second{'s' if secs != 1 else ''}"
        elif mins > 0:
            duration_str = f"{mins} minute{'s' if mins != 1 else ''}"
        else:
            duration_str = f"{secs} second{'s' if secs != 1 else ''}"

        return SkillResult(success=True, message=f"Timer set for {duration_str}.")

    def _parse_duration(self, query: str) -> int | None:
        """Parse a duration string into seconds."""
        import re
        lower = query.lower()

        total_seconds = 0
        found = False

        # Match patterns like "5 minutes", "30 seconds", "1 hour", "2 hours 30 minutes"
        patterns = [
            (r'(\d+)\s*hours?\b', 3600),
            (r'(\d+)\s*hrs?\b', 3600),
            (r'(\d+)\s*minutes?\b', 60),
            (r'(\d+)\s*mins?\b', 60),
            (r'(\d+)\s*seconds?\b', 1),
            (r'(\d+)\s*secs?\b', 1),
        ]

        for pattern, multiplier in patterns:
            match = re.search(pattern, lower)
            if match:
                total_seconds += int(match.group(1)) * multiplier
                found = True

        if not found:
            # Try just a bare number (assume seconds)
            match = re.search(r'(\d+)', lower)
            if match:
                total_seconds = int(match.group(1))
                found = True

        return total_seconds if found else None
