"""DBInterface module."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class DBInterface(ABC):
    """Interface for the database operations (CRUD)."""

    @abstractmethod
    def create(self, key: str, data: Dict[str, Any]) -> None:
        """Creates a new record in the database."""

    @abstractmethod
    def read(self, key: str) -> Dict[str, Any]:
        """Reads a record from the database."""

    @abstractmethod
    def update(self, key: str, data: Dict[str, Any]) -> None:
        """Updates an existing record in the database."""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Deletes a record from the database."""

    @abstractmethod
    def list_all(self) -> Dict[str, Dict[str, Any]]:
        """Lists all records in the database."""
