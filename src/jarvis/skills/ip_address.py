"""IP address skill — show local and public IP addresses."""

import socket
import requests
from .registry import Skill, SkillResult


class IPAddressSkill(Skill):
    name = "ip_address"
    description = "Get local and public IP addresses"
    triggers = ["ip address", "what's my ip", "my ip", "what is my ip", "ip info", "public ip"]

    def execute(self, query: str, context: dict) -> SkillResult:
        parts = []

        # Get local IP
        local_ip = self._get_local_ip()
        if local_ip:
            parts.append(f"Local IP: {local_ip}")

        # Get public IP
        public_ip = self._get_public_ip()
        if public_ip:
            parts.append(f"Public IP: {public_ip}")

        if not parts:
            return SkillResult(success=False, message="I couldn't determine your IP address.")

        return SkillResult(success=True, message=". ".join(parts) + ".")

    def _get_local_ip(self) -> str | None:
        """Get the local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return None

    def _get_public_ip(self) -> str | None:
        """Get the public IP address."""
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("ip")
        except Exception:
            return None
