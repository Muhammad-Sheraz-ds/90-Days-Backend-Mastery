"""
JSON Storage Layer (v2) — Same as Day 8
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JSONStorage:
    """Handles JSON file persistence."""
    
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = Path(filepath)
    
    def load(self) -> dict[str, Any]:
        if not self.filepath.exists():
            return {"tasks": [], "next_id": 1}
        try:
            return json.loads(self.filepath.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {self.filepath}: {e}")
            return {"tasks": [], "next_id": 1}
    
    def save(self, data: dict[str, Any]) -> None:
        self.filepath.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    
    def exists(self) -> bool:
        return self.filepath.exists()
