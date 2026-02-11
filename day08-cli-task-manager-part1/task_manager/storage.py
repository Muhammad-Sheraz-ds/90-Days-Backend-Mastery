"""
JSON Storage Layer

Handles saving and loading data to/from a JSON file.
"""

import json
from pathlib import Path
from typing import Any


class JSONStorage:
    """
    Handles JSON file persistence.
    
    Provides a simple interface for loading and saving
    dictionary data to a JSON file.
    """
    
    def __init__(self, filepath: str = "tasks.json"):
        """
        Initialize storage with file path.
        
        Args:
            filepath: Path to the JSON file
        """
        self.filepath = Path(filepath)
    
    def load(self) -> dict[str, Any]:
        """
        Load data from JSON file.
        
        Returns:
            Dictionary with tasks and metadata.
            Returns empty structure if file doesn't exist.
        """
        if not self.filepath.exists():
            return self._empty_data()
        
        try:
            content = self.filepath.read_text(encoding="utf-8")
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {self.filepath}: {e}")
            return self._empty_data()
        except IOError as e:
            print(f"Warning: Cannot read {self.filepath}: {e}")
            return self._empty_data()
    
    def save(self, data: dict[str, Any]) -> None:
        """
        Save data to JSON file.
        
        Args:
            data: Dictionary to save
        
        Raises:
            IOError: If file cannot be written
        """
        try:
            content = json.dumps(data, indent=2, ensure_ascii=False)
            self.filepath.write_text(content, encoding="utf-8")
        except IOError as e:
            print(f"Error: Cannot write to {self.filepath}: {e}")
            raise
    
    def _empty_data(self) -> dict[str, Any]:
        """Return empty data structure."""
        return {"tasks": [], "next_id": 1}
    
    def exists(self) -> bool:
        """Check if storage file exists."""
        return self.filepath.exists()
    
    def clear(self) -> None:
        """Delete storage file if it exists."""
        if self.filepath.exists():
            self.filepath.unlink()
