import click.testing
import pytest
import requests

from github_release_fetcher import console

FAKE_CONSOLE_OPTIONS = ["--owner=foo", "--repository=bar"]


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_github_latest_release(mocker):
    return mocker.patch("github_release_fetcher.github.latest_release")


def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert result.exit_code == 0


def test_main_fails_missing_option(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Usage" in result.output


def test_main_prints_version(runner, mock_requests_get):
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert "0.1.0" in result.output


def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert mock_requests_get.called


def test_main_uses_api_github_com(runner, mock_requests_get):
    runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    args, _ = mock_requests_get.call_args
    assert "api.github.com" in args[0]


def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main, FAKE_CONSOLE_OPTIONS)
    assert "Error" in result.output


def test_main_uses_specified_repository(runner, mock_github_latest_release):
    runner.invoke(console.main, ["--owner=foo", "--repository=bar"])
    mock_github_latest_release.assert_called_with(owner="foo", repository="bar")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    result = runner.invoke(
        console.main, ["--owner=pziggo", "--repository=github-release-fetcher"]
    )
    assert result.exit_code == 0
