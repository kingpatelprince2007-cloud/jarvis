"""Stopwatch skill — start, stop, and check elapsed time."""

import time
from .registry import Skill, SkillResult


class StopwatchSkill(Skill):
    name = "stopwatch"
    description = "Start, stop, and check a stopwatch"
    triggers = ["start stopwatch", "stop stopwatch", "stopwatch time", "check stopwatch", "elapsed time", "start the stopwatch", "stop the stopwatch"]

    _start_time: float | None = None
    _running: bool = False

    def execute(self, query: str, context: dict) -> SkillResult:
        lower = query.lower()

        if "start" in lower:
            return self._start()
        elif "stop" in lower:
            return self._stop()
        elif "check" in lower or "elapsed" in lower or "time" in lower:
            return self._check()
        else:
            return SkillResult(success=False, message="Try 'start stopwatch', 'stop stopwatch', or 'check stopwatch'.")

    def _start(self) -> SkillResult:
        if self._running:
            elapsed = time.time() - self._start_time
            mins, secs = divmod(int(elapsed), 60)
            return SkillResult(success=True, message=f"Stopwatch is already running. Elapsed: {mins}m {secs}s.")

        self._start_time = time.time()
        self._running = True
        return SkillResult(success=True, message="Stopwatch started.")

    def _stop(self) -> SkillResult:
        if not self._running:
            return SkillResult(success=False, message="The stopwatch isn't running.")

        elapsed = time.time() - self._start_time
        self._running = False
        self._start_time = None

        mins, secs = divmod(int(elapsed), 60)
        hours, mins = divmod(mins, 60)

        if hours > 0:
            time_str = f"{hours}h {mins}m {secs}s"
        elif mins > 0:
            time_str = f"{mins}m {secs}s"
        else:
            time_str = f"{secs}s"

        return SkillResult(success=True, message=f"Stopwatch stopped. Elapsed time: {time_str}.")

    def _check(self) -> SkillResult:
        if not self._running or self._start_time is None:
            return SkillResult(success=False, message="The stopwatch isn't running.")

        elapsed = time.time() - self._start_time
        mins, secs = divmod(int(elapsed), 60)
        hours, mins = divmod(mins, 60)

        if hours > 0:
            time_str = f"{hours}h {mins}m {secs}s"
        elif mins > 0:
            time_str = f"{mins}m {secs}s"
        else:
            time_str = f"{secs}s"

        return SkillResult(success=True, message=f"Stopwatch running. Elapsed: {time_str}.")
