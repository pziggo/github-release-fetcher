from github_release_fetcher import github


def test_latest_release_uses_given_repository(mock_requests_get):
    github.latest_release(owner="foo", repository="bar")
    args, _ = mock_requests_get.call_args
    assert "repos/foo/bar/releases" in args[0]
