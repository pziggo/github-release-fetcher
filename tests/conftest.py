"""Common test fixtures for all packages under test."""
from typing import Any
from unittest.mock import Mock

import pytest
from pytest_mock import MockFixture

from .test_data import dummy_response_latest


def pytest_configure(config: Any) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    """Fixture for mocking requests.get()."""
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = dummy_response_latest
    return mock
