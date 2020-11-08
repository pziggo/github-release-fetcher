"""Common data and structures for tests."""

dummy_owner = "foo"
dummy_repository = "bar"
dummy_version: str = "0.1.0"
dummy_asset_1: str = "https://github.com/{}/{}/releases/download/{}/a".format(
    dummy_owner, dummy_repository, dummy_version
)
dummy_asset_2: str = "https://github.com/{}/{}/releases/download/{}/b".format(
    dummy_owner, dummy_repository, dummy_version
)

dummy_response_latest = {
    "tag_name": dummy_version,
    "assets": [
        {"browser_download_url": dummy_asset_1},
        {"browser_download_url": dummy_asset_2},
    ],
}
