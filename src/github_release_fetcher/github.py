"""Interface package to interact with the Github REST API."""
import click
import requests

from .release import Release


API_URL: str = "https://api.github.com/repos/{owner}/{repository}/releases/latest"


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
            return Release(response.json())
    except (requests.RequestException, TypeError) as error:
        message = str(error)
        raise click.ClickException(message) from error
