from typing import List
from unittest.mock import Mock

import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from github_release_fetcher import console

FAKE_CONSOLE_OPTIONS: List[str] = ["--owner=foo", "--repository=bar"]


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


@pytest.fixture
def mock_github_latest_release(mocker: MockFixture) -> Mock:
    return mocker.patch("github_release_fetcher.github.latest_release")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert result.exit_code == 0


def test_main_fails_missing_option(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert "Usage" in result.output


def test_main_prints_version(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert "0.1.0" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert mock_requests_get.called


def test_main_uses_api_github_com(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    args, _ = mock_requests_get.call_args
    assert "api.github.com" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert "Error" in result.output


def test_main_uses_specified_repository(
    runner: CliRunner, mock_github_latest_release: Mock
) -> None:
    runner.invoke(console.main, ["--owner=foo", "--repository=bar"])
    mock_github_latest_release.assert_called_with(owner="foo", repository="bar")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    result = runner.invoke(
        console.main, ["--owner=pziggo", "--repository=github-release-fetcher"]
    )
    assert result.exit_code == 0
