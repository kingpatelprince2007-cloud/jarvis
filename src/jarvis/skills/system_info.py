"""System information skill — CPU, RAM, disk usage."""

import platform
from .registry import Skill, SkillResult


class SystemInfoSkill(Skill):
    name = "system_info"
    description = "Get system information (CPU, RAM, disk)"
    triggers = ["system info", "system status", "cpu usage", "ram usage", "memory usage", "disk usage", "system resources"]

    def execute(self, query: str, context: dict) -> SkillResult:
        try:
            import psutil
        except ImportError:
            return SkillResult(
                success=False,
                message="System monitoring requires psutil. Install with: pip install psutil"
            )

        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        parts = []
        if "cpu" in query.lower() or "system" in query.lower():
            parts.append(f"CPU usage is at {cpu_percent}%")
        if "ram" in query.lower() or "memory" in query.lower() or "system" in query.lower():
            parts.append(f"Memory is at {memory.percent}% ({memory.used // (1024**3)}GB of {memory.total // (1024**3)}GB)")
        if "disk" in query.lower() or "system" in query.lower():
            parts.append(f"Disk usage is at {disk.percent}% ({disk.used // (1024**3)}GB of {disk.total // (1024**3)}GB)")

        if not parts:
            parts = [
                f"CPU: {cpu_percent}%",
                f"Memory: {memory.percent}%",
                f"Disk: {disk.percent}%",
            ]

        message = ". ".join(parts) + "."
        return SkillResult(success=True, message=message)
