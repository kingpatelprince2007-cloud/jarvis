"""File search skill — search for files by name (read-only, safe)."""

import os
from pathlib import Path
from .registry import Skill, SkillResult


class FileSearchSkill(Skill):
    name = "file_search"
    description = "Search for files by name"
    triggers = ["find file", "search for file", "find files", "search files", "look for file", "where is file"]

    def execute(self, query: str, context: dict) -> SkillResult:
        search_term = self._extract_search_term(query)

        if not search_term:
            return SkillResult(success=False, message="What file are you looking for? Try 'find file readme'.")

        # Search in common directories
        home = Path.home()
        search_dirs = [
            home,
            home / "Documents",
            home / "Downloads",
            home / "Desktop",
            home / "workspace",
        ]

        results = []
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            try:
                for root, dirs, files in os.walk(search_dir):
                    # Limit depth to avoid scanning entire filesystem
                    depth = len(Path(root).parts) - len(search_dir.parts)
                    if depth > 3:
                        dirs.clear()
                        continue
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith(".")]
                    for filename in files:
                        if search_term.lower() in filename.lower():
                            filepath = os.path.join(root, filename)
                            size = os.path.getsize(filepath)
                            results.append({"path": filepath, "name": filename, "size": size})
                            if len(results) >= 10:
                                break
                    if len(results) >= 10:
                        break
            except PermissionError:
                continue
            if len(results) >= 10:
                break

        if not results:
            return SkillResult(success=True, message=f"No files matching '{search_term}' were found.")

        lines = [f"Found {len(results)} file(s) matching '{search_term}':"]
        for i, result in enumerate(results, 1):
            size_str = self._format_size(result["size"])
            lines.append(f"  {i}. {result['name']} ({size_str})")
            lines.append(f"     {result['path']}")

        return SkillResult(success=True, message="\n".join(lines))

    def _extract_search_term(self, query: str) -> str:
        """Extract the search term from the query."""
        lower = query.lower()
        for trigger in self.triggers:
            if trigger in lower:
                idx = lower.index(trigger) + len(trigger)
                return query[idx:].strip()
        return ""

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable form."""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
