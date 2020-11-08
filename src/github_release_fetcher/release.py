"""Data package to represent the release information."""
from typing import Dict
from typing import List


class Release:
    """Data class to represent releases."""

    def __init__(self, data: Dict) -> None:
        """Release constructor."""
        self._tag_name: str = data["tag_name"]
        self._assets: List[str] = []

        for asset in data["assets"]:
            self._assets.append(asset["browser_download_url"])

    @property
    def tag_name(self) -> str:
        """Return tag_name attribute."""
        return self._tag_name

    @property
    def assets(self) -> List[str]:
        """Return list of download URLS."""
        return self._assets

    def asset_size(self) -> int:
        """Return number or assets."""
        return len(self._assets)
