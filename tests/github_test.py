"""Test cases for the github module."""
from unittest.mock import Mock

import click
import pytest

from github_release_fetcher import github
from github_release_fetcher.release import Release
from .test_data import dummy_asset_1


def test_latest_release_uses_given_repository(mock_requests_get: Mock) -> None:
    """It sends a request with the correct Owner and Repository in the URL."""
    github.latest_release(owner="foo", repository="bar")
    args, _ = mock_requests_get.call_args
    assert "repos/foo/bar/releases" in args[0]


def test_latest_release_returns_release(mock_requests_get: Mock) -> None:
    """It returns an instance of type Release."""
    release = github.latest_release()
    assert isinstance(release, Release)


def test_latest_release_handles_validation_errors(mock_requests_get: Mock) -> None:
    """It throws an ClickException if the json cannot be parsed."""
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        github.latest_release()


def test_latest_release_returns_assets(mock_requests_get: Mock) -> None:
    """It returns a list of assets."""
    release = github.latest_release()
    assert release.asset_size() == 2


def test_latest_release_returns_dl_url(mock_requests_get: Mock) -> None:
    """It returns the URL from the mock."""
    release = github.latest_release()
    assert release.assets[0] == dummy_asset_1
