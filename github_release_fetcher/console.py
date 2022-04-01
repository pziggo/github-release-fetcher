"""Command-line interface for github_release_fetcher."""
import click

from . import __version__, github


@click.command()
@click.option(
    "--owner",
    help="Organisation of the Github repository",
    required=True,
)
@click.option(
    "--repository",
    help="Github repository",
    required=True,
)
@click.version_option(version=__version__)
def main(owner: str, repository: str) -> None:
    """The Github releases fetcher tool."""
    data = github.latest_release(owner=owner, repository=repository)

    version = data.tag_name

    click.echo("Version: {}".format(version))
    click.echo("Assets:")
    for asset in data.assets:
        click.echo(asset)
