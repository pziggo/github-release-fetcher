"""Nox sessions."""
import tempfile
from typing import Any
from typing import List

import nox
from nox.sessions import Session

package: str = "github_release_fetcher"
python: List[str] = ["3.10", "3.9", "3.8", "3.7"]
locations = "github_release_fetcher", "tests", "noxfile.py"

nox.options.sessions = "lint", "mypy", "safety", "tests"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=constraints.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.10"])
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=["3.10"])
def coverage(session: Session) -> None:
    """Generate coverage data."""
    install_with_constraints(session, "coverage[toml]")
    session.run("coverage", "xml", "--fail-under=0")


@nox.session(python=python)
def lint(session: Session) -> None:
    """Run darglint and flake8 linters."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "darglint",
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "pep8-naming",
    )
    session.run("flake8", *args)


@nox.session(python=["3.10"])
def mypy(session: Session) -> None:
    """Run static type checks using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy", "types-requests", "types-click")
    session.run("mypy", *args)


@nox.session(python=["3.10"])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=constraints.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=python)
def tests(session: Session) -> None:
    """Run the test suite, per default without E2E tests."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--only", "main", external=True)
    install_with_constraints(session, "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)


@nox.session(python=["3.10"])
def typeguard(session: Session) -> None:
    """Run dynamic type checks with typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--only", "main", external=True)
    install_with_constraints(session, "pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python=["3.10"])
def xdoctest(session: Session) -> None:
    """Run examples from docstring with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--only", "main", external=True)
    install_with_constraints(session, "xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)
