"""DBDriverFactory module."""

from .interface import DBInterface
from .local import LocalStore


class DBDriverFactory:  # pylint: disable=too-few-public-methods
    """Factory to select the appropriate DB driver."""

    @staticmethod
    def get_driver(driver_type: str, *args, **kwargs) -> DBInterface:
        """Returns the appropriate DB driver based on the driver type."""
        driver_type = driver_type.lower()
        if driver_type == "local":
            return LocalStore(*args, **kwargs)
        raise ValueError(f"Unsupported driver type: {driver_type}")
