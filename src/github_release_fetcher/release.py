"""Data package to represent the release information."""
from typing import Dict


class Release:
    """Data class to represent releases."""

    def __init__(self, data: Dict) -> None:
        """Release constructor."""
        self._tag_name: str = data["tag_name"]

    @property
    def tag_name(self) -> str:
        """Return tag_name attribute."""
        return self._tag_name
