"""Battery status skill — check battery level and charging status."""

from .registry import Skill, SkillResult


class BatteryStatusSkill(Skill):
    name = "battery_status"
    description = "Check battery level and charging status"
    triggers = ["battery", "battery status", "battery level", "how much battery", "power status", "charge level"]

    def execute(self, query: str, context: dict) -> SkillResult:
        try:
            import psutil
        except ImportError:
            return SkillResult(
                success=False,
                message="Battery monitoring requires psutil. Install with: pip install psutil"
            )

        battery = psutil.sensors_battery()

        if battery is None:
            return SkillResult(success=True, message="No battery detected. This device may be a desktop or server.")

        percent = battery.percent
        plugged = battery.power_plugged

        # Estimate time remaining
        secs_left = battery.secsleft
        if secs_left == psutil.POWER_TIME_UNLIMITED:
            time_str = "unlimited"
        elif secs_left == psutil.POWER_TIME_UNKNOWN:
            time_str = "unknown"
        else:
            hours, remainder = divmod(secs_left, 3600)
            minutes, _ = divmod(remainder, 60)
            time_str = f"{hours}h {minutes}m"

        status = "charging" if plugged else "on battery power"

        # Build a visual bar
        bar_length = 20
        filled = int(bar_length * percent / 100)
        bar = "[" + "#" * filled + "-" * (bar_length - filled) + "]"

        message = f"Battery: {percent}% {bar}\nStatus: {status}\nTime remaining: {time_str}"

        # Add a warning for low battery
        if percent < 20 and not plugged:
            message += "\nWarning: Low battery! Please connect your charger."

        return SkillResult(success=True, message=message)
