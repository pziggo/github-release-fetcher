"""Interface package to interact with the Github REST API."""
from dataclasses import dataclass

import click
import desert
import marshmallow
import requests


API_URL: str = "https://api.github.com/repos/{owner}/{repository}/releases/latest"


@dataclass
class Release:
    """Release resource.

    Attributes:
        tag_name: The version string.
    """

    tag_name: str


schema = desert.schema(Release, meta={"unknown": marshmallow.EXCLUDE})


def latest_release(owner: str = "", repository: str = "") -> Release:
    """Return the latest release version.

    Invokes a request to the /release/latest endpoint.

    Args:
        owner: The Github organisation name or user.
        repository: The Github repository.

    Returns:
        An instance of type Release.

    Raises:
        ClickException: The request failed or the response is invalid.

    Example:
        >>> from github_release_fetcher import github
        >>> release = github.latest_release(owner="pziggo", repository=
        ... "github-release-fetcher")  #doctest: +ELLIPSIS
        >>> bool(release.tag_name)
        True
    """
    url = API_URL.format(owner=owner, repository=repository)
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
