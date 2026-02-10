"""Validation sessions."""

from __future__ import annotations

from typing import Literal

import nox

ResolutionType = Literal["highest", "lowest-direct", "lowest"]
_PYTHON_VERSIONS = (
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
    "3.14t",
)
_RESOLUTIONS: tuple[ResolutionType, ...] = (
    "highest",
    # "lowest-direct",
    "lowest",
)


# Fail nox session when run a program which is not installed in its virtualenv
nox.options.error_on_external_run = True

# use uv to speed up the dependencies installation
nox.options.default_venv_backend = "uv"


def _install_deps(session: nox.Session, resolution: ResolutionType) -> None:
    session.run_install(
        "uv",
        "sync",
        "-q",
        "--frozen",
        f"--python={session.virtualenv.location}",
        f"--resolution={resolution}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session(python=_PYTHON_VERSIONS)
@nox.parametrize("resolution", _RESOLUTIONS)
def lint(session: nox.Session, resolution: ResolutionType) -> None:
    """Perform style checks of the code."""
    _install_deps(session=session, resolution=resolution)
    session.run("ruff", "format", "--check", ".")
    session.run("ruff", "check", ".")
    session.run("mypy", "./src/", "./tests/")


@nox.session
def coverage_clean(session: nox.Session) -> None:
    """Clean coverage data."""
    _install_deps(session=session, resolution="highest")
    session.run("coverage", "erase")


@nox.session(python=_PYTHON_VERSIONS, requires=("coverage_clean",))
@nox.parametrize("resolution", _RESOLUTIONS)
def test(session: nox.Session, resolution: ResolutionType) -> None:
    """Execute the tests and measure code coverage."""
    # Speed up coverage by using sysmon, see
    # https://coverage.readthedocs.io/en/latest/cmd.html#execution-coverage-run
    # TODO: move to pyproject.toml once 3.12 is the min. supported version
    extra_env = {"COVERAGE_CORE": "sysmon"}
    _install_deps(session=session, resolution=resolution)
    session.run("coverage", "run", "-m", "pytest", "tests", env=extra_env)

    session.notify("coverage_collate")


@nox.session
def coverage_collate(session: nox.Session) -> None:
    """Combine test coverage results from all test executions."""
    _install_deps(session=session, resolution="highest")
    session.run("coverage", "combine")
    session.run("coverage", "html")
