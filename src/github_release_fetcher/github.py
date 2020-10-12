import click
import requests


API_URL = "https://api.github.com/repos/{owner}/{repository}/releases/latest"


def latest_release(owner="", repository=""):
    url = API_URL.format(owner=owner, repository=repository)
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
