from dataclasses import dataclass

import click
import desert
import marshmallow
import requests


API_URL: str = "https://api.github.com/repos/{owner}/{repository}/releases/latest"


@dataclass
class Release:
    tag_name: str


schema = desert.schema(Release, meta={"unknown": marshmallow.EXCLUDE})


def latest_release(owner: str = "", repository: str = "") -> Release:
    url = API_URL.format(owner=owner, repository=repository)
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
