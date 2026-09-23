"""QR code generator skill — generate QR codes as PNG files."""

from .registry import Skill, SkillResult


class QRCodeSkill(Skill):
    name = "qr_code"
    description = "Generate QR codes for text, URLs, or data"
    triggers = ["generate qr", "create qr", "qr code", "make qr", "qr for"]

    def execute(self, query: str, context: dict) -> SkillResult:
        data = self._extract_data(query)

        if not data:
            return SkillResult(success=False, message="What data should I encode? Try 'generate qr code for https://example.com'.")

        try:
            import qrcode
        except ImportError:
            return SkillResult(
                success=False,
                message="QR code generation requires the 'qrcode' package. Install with: pip install qrcode[pil]"
            )

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save to file
        self.config.ensure_data_dir()
        filename = self._sanitize_filename(data)
        filepath = self.config.data_dir / f"qr_{filename}.png"
        img.save(str(filepath))

        return SkillResult(
            success=True,
            message=f"QR code generated for '{data}'. Saved to {filepath}",
            data={"data": data, "filepath": str(filepath)},
            should_speak=False  # Don't speak the file path
        )

    def _extract_data(self, query: str) -> str:
        """Extract the data to encode from the query."""
        lower = query.lower()
        for trigger in self.triggers:
            if trigger in lower:
                idx = lower.index(trigger) + len(trigger)
                # Skip 'code' if present
                remaining = query[idx:].strip()
                if remaining.lower().startswith("code"):
                    remaining = remaining[4:].strip()
                if remaining.lower().startswith("for"):
                    remaining = remaining[3:].strip()
                return remaining
        return ""

    def _sanitize_filename(self, data: str) -> str:
        """Create a safe filename from the data."""
        import re
        # Take first 20 chars, replace non-alphanumeric
        safe = re.sub(r'[^a-zA-Z0-9]', '_', data[:20])
        return safe.strip("_") or "data"
