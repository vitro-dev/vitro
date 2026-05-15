"""Unit tests for vitro pexpect module."""

import logging
from io import StringIO
from pathlib import Path

import pexpect
import pytest
from pytest_mock import MockerFixture

from vitro.libraries.vitro_pexpect import VitroPexpect, _LogWrapper


class TestVitroPexpect(VitroPexpect):
    r"""Quick class to provide an implementation for abstract methods."""

    def execute_command(self, command, timeout=-1):  # noqa: ANN001, D102
        return super().execute_command(command, timeout)


def test_start_interactive_session(mocker: MockerFixture):
    """Ensure that an interactive session is started successfully.

    :param mocker: pytest mock object
    :type mocker: MockerFixture
    """
    mocker.patch.object(pexpect.spawn, attribute="__init__", return_value=None)
    vitro_pexpect = TestVitroPexpect(
        "session",
        "pwd",
        save_console_logs="",
        args=["", ""],
    )
    interact_mock = mocker.patch.object(
        vitro_pexpect,
        "interact",
        return_value=None,
    )
    vitro_pexpect.start_interactive_session()
    logger = logging.getLogger("pexpect")
    assert len(logger.handlers) == 0
    interact_mock.assert_called_once()


def test_vitro_pexpect_with_save_console_logs(tmp_path: Path):
    """Ensure vitro pexpect saves console logs to the disk when enabled.

    :param mocker: pytest mock object
    :type mocker: MockerFixture
    :param tmp_path: pytest temporary directory fixture
    :type tmp_path: Path
    """
    bfp = TestVitroPexpect(
        "session", "pwd", save_console_logs=str(tmp_path), args=["", ""]
    )
    logger = logging.getLogger("pexpect.session")
    assert len(logger.handlers) > 0
    assert (tmp_path / "session.txt").is_file()
    assert isinstance(bfp.logfile_read, _LogWrapper)


def test_vitro_pexpect_without_save_console_logs(tmp_path: Path):
    """Ensure vitro pexpect doesn't save console logs to the disk when disabled."""
    bfp = TestVitroPexpect(
        "session_no_save",
        "pwd",
        save_console_logs="",
        args=["", ""],
    )
    logger = logging.getLogger("pexpect.session_no_save")
    assert len(logger.handlers) == 0
    assert not (tmp_path / "session_no_save.txt").is_file()
    assert isinstance(bfp.logfile_read, _LogWrapper)


def test_get_last_output(mocker: MockerFixture):
    """Ensure that the last output is retrieved successfully.

    :param mocker: pytest mock object
    :type mocker: MockerFixture
    """
    bfp = TestVitroPexpect("session", "pwd", save_console_logs="", args=["", ""])
    mocker.patch.object(bfp, "before", "/vitro_new_repo/vitro   ")
    assert bfp.get_last_output() == "/vitro_new_repo/vitro"


@pytest.mark.parametrize(
    ("input_line", "expected_output"),
    [
        ("Test line\n", "Test line\n"),
        (bytes("Test line\n", "utf-8"), "Test line\n"),
        ("Test line\n   ", "Test line\n"),
        ("abc \x08\x1b\x5b\x4bdef\n", "abcdef\n"),
        ("hello\x08\x20\x08world\n", "hellworld\n"),
        ("hello\tworld\n", "hello  world\n"),
        ("hello \x1b@00001 world\n", "hello 00001 world\n"),
        ("\x1b[1;31mHello\x1b[0m World\n", "Hello World\n"),
        ("\x1b[2J\x1b[HHello\n", "Hello\n"),
        ("\x1b[6nPosition\n", "Position\n"),
        ("Line 1\rLine 2\nLine 3\n", "Line 1\nLine 2\nLine 3\n"),
        ("Beep\x07Alert\n", "BeepAlert\n"),
        ("\x1b\x5b\x48\x1b\x5b\x4aContent\n", "Content\n"),
        ("Sample \x1b[32mText\x1b[0m\r\n", "Sample Text\n"),
    ],
)
def test_write_in_log_wrapper(input_line: str, expected_output: str):
    """Ensure that logs are formatted properly.

    :param input_line: input string
    :type input_line: str
    :param expected_output: expected output
    :type expected_output: str
    """
    logger = logging.getLogger("__name__")
    stream = StringIO()
    logger.addHandler(logging.StreamHandler(stream))
    logger.setLevel(logging.DEBUG)
    log_wrapper = _LogWrapper(logger)
    log_wrapper.write(input_line)
    stream.seek(0)
    captured_logs = stream.read()
    assert captured_logs == expected_output
