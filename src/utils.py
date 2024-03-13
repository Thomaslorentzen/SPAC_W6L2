"""Utilities to be used thoughout the code."""

import json
from typing import Any


class ConfigManager:
    """Class to handle the config file."""

    def __init__(self, filepath: str) -> None:
        """Initialize the class.

        Args:
            filepath (str): Path to config file.
        """
        self.filepath: str = filepath
        self.config: dict[str, str] = self.load_file()

    def load_file(self) -> Any:
        """Load the config file in as a dict.

        Returns:
            Any: Configurations.
        """
        with open(self.filepath, "r") as file:
            return json.load(file)

    def username(self) -> Any:
        """Fetch the username from the config.

        Returns:
            Any: Username.
        """
        return self.config["username"]

    def password(self) -> Any:
        """Return the password from the config.

        Returns:
            Any: Password.
        """
        return self.config["password"]
