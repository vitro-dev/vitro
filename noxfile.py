"""Validation sessions."""

import nox

_PYTHON_VERSIONS = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
]

# Fail nox session when run a program which is not installed in its virtualenv
nox.options.error_on_external_run = True

# use uv to speed up the dependencies installation
nox.options.default_venv_backend = "uv"


def _install_deps(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "-q",
        "--frozen",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session(python=_PYTHON_VERSIONS)
def lint(session: nox.Session) -> None:
    """Perform style checks of the code."""
    _install_deps(session)
    session.run("ruff", "format", "--check", ".")
    session.run("ruff", "check", ".")
    session.run("mypy", "./src/", "./tests/")


@nox.session
def coverage_clean(session: nox.Session) -> None:
    """Clean coverage data."""
    _install_deps(session)
    session.run("coverage", "erase")


@nox.session(python=_PYTHON_VERSIONS, requires=("coverage_clean",))
def tests(session: nox.Session) -> None:
    """Execute the tests and measure code coverage."""
    # Speed up coverage by using sysmon, see
    # https://coverage.readthedocs.io/en/latest/cmd.html#execution-coverage-run
    # TODO: move to pyproject.toml once 3.12 is the min. supported version

    py_ver = tuple(map(int, session.python.split(".")))  # type: ignore[union-attr]
    extra_env = {"COVERAGE_CORE": "sysmon"} if py_ver >= (3, 12) else None
    _install_deps(session)
    session.run("coverage", "run", "-m", "pytest", "tests", env=extra_env)

    session.notify("collate_coverage")


@nox.session
def collate_coverage(session: nox.Session) -> None:
    """Combine test coverage results from all test executions."""
    _install_deps(session)
    session.run("coverage", "combine")
    session.run("coverage", "html")
