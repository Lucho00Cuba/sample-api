"""LocalStore module."""

import json
import os
from typing import Dict, Any

from .interface import DBInterface


class LocalStore(DBInterface):
    """Concrete implementation of DBInterface using a JSON file as storage."""

    def __init__(self, filename: str):
        """Initializes the store with a specific file."""
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the JSON file exists."""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_data(self) -> Dict[str, Dict[str, Any]]:
        """Loads data from the JSON file."""
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_data(self, data: Dict[str, Dict[str, Any]]) -> None:
        """Saves data to the JSON file."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def create(self, key: str, data: Dict[str, Any]) -> None:
        """Creates a new record in the database."""
        data_store = self._load_data()
        if key in data_store:
            raise KeyError(f"Record with key {key} already exists.")
        data_store[key] = data
        self._save_data(data_store)

    def read(self, key: str) -> Dict[str, Any]:
        """Reads a record from the database."""
        data_store = self._load_data()
        if key not in data_store:
            raise KeyError(f"Record with key {key} not found.")
        return data_store[key]

    def update(self, key: str, data: Dict[str, Any]) -> None:
        """Updates an existing record in the database."""
        data_store = self._load_data()
        if key not in data_store:
            raise KeyError(f"Record with key {key} not found.")
        data_store[key] = data
        self._save_data(data_store)

    def delete(self, key: str) -> None:
        """Deletes a record from the database."""
        data_store = self._load_data()
        if key not in data_store:
            raise KeyError(f"Record with key {key} not found.")
        del data_store[key]
        self._save_data(data_store)

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        """Lists all records in the database."""
        return self._load_data()
