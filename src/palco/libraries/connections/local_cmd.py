"""Connect to a device with a local command."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pexpect

from palco.exceptions import (
    DeviceConnectionError,
    PalcoError,
    ShellPromptUndefinedError,
)
from palco.libraries.palco_pexpect import PalcoPexpect

if TYPE_CHECKING:
    from pexpect.spawnbase import _InputRePattern

_CONNECTION_ERROR_THRESHOLD = 2
_CONNECTION_FAILED_STR: str = "Connection failed with Local Command"


class LocalCmd(PalcoPexpect):
    """Connect to a device with a local command."""

    def __init__(  # pylint: disable=too-many-arguments  # noqa: PLR0913
        self,  # pylint: disable=unused-argument
        name: str,
        conn_command: str,
        save_console_logs: str,
        shell_prompt: list[_InputRePattern] | None = None,
        args: list[str] | None = None,
        *,
        username: str = "root",
        password: str | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Initialize local command connection.

        :param name: connection name
        :type name: str
        :param conn_command: command to start the session
        :type conn_command: str
        :param save_console_logs: save console logs to disk
        :type save_console_logs: str
        :param shell_prompt: shell prompt pattern, defaults to None
        :type shell_prompt: list[str]
        :param args: arguments to the command, defaults to None
        :type args: list[str], optional
        :param username: effective user inside the local command session.
            Defaults to ``"root"``, matching the default ``docker exec``
            behaviour.  Set when the local command launches as a
            non-root user (e.g. ``docker exec --user alice ...``) so
            :meth:`sudo_sendline` knows whether escalation is required.
        :type username: str
        :param password: password used for sudo escalation when
            ``username != "root"``.  Required only when the sudoers
            policy prompts for one; may be ``None`` for NOPASSWD
            configurations.
        :type password: str | None
        :param kwargs: additional keyword args
        """
        self._shell_prompt = shell_prompt
        self._username = username
        self._password = password
        if args is None:
            args = []
        super().__init__(
            name,
            conn_command,
            save_console_logs,
            args,
            **kwargs,
        )

    # pylint: disable=duplicate-code
    def login_to_server(self, password: str | None = None) -> None:
        """Login.

        :param password: ssh password
        :raises DeviceConnectionError: connection failed via local command
        :raises ValueError: if shell prompt is unavailable
        """
        if password is not None:
            if self.expect(
                ["password:", pexpect.EOF, pexpect.TIMEOUT],
            ):
                raise DeviceConnectionError(_CONNECTION_FAILED_STR)
            self.sendline(password)
        # TODO: temp fix for now. To be decided if shell prompt to be used.
        if not self._shell_prompt:
            raise ShellPromptUndefinedError
        if (
            self.expect(
                [
                    pexpect.EOF,
                    pexpect.TIMEOUT,
                    *self._shell_prompt,
                ],
            )
            < _CONNECTION_ERROR_THRESHOLD
        ):
            raise DeviceConnectionError(_CONNECTION_FAILED_STR)

    def execute_command(self, command: str, timeout: int = -1) -> str:
        """Execute a command in the local command session.

        :param command: command to execute
        :param timeout: timeout in seconds. defaults to -1
        :returns: command output
        :raises ValueError: if shell prompt is unavailable
        """
        if not self._shell_prompt:
            raise ShellPromptUndefinedError
        self.sendline(command)
        self.expect_exact(command)
        self.expect(self.linesep)
        # TODO: is this needed? is the shell prompt of Local(Jenkins or any user)?
        self.expect(self._shell_prompt, timeout=timeout)
        return self.get_last_output()

    def sudo_sendline(self, cmd: str) -> None:
        """Add sudo in the sendline if username is not root.

        Mirrors :meth:`SSHConnection.sudo_sendline`: when ``_username``
        is not ``"root"``, prime sudo with ``sudo true``, supply
        ``_password`` if sudo prompts for one, then send the command
        prefixed with ``sudo``.  For ``_username == "root"`` the method
        collapses to a plain :meth:`sendline` — identical to the root
        branch of :class:`SSHConnection`.

        :param cmd: command to send
        :raises PalcoError: if sudo prompts for a password but none was
            configured on the connection.
        :raises ShellPromptUndefinedError: if no shell prompt was
            configured on the connection.
        """
        if not self._shell_prompt:
            raise ShellPromptUndefinedError
        if self._username != "root":
            self.sendline("sudo true")
            password_requested = self.expect(
                [*self._shell_prompt, "password for .*:", "Password:"],
            )
            if password_requested:
                if self._password is None:
                    msg = (
                        "sudo prompted for a password but none was configured "
                        f"for LocalCmd (username={self._username!r}). "
                        "Supply a password at construction time or use a "
                        "NOPASSWD sudoers entry for this user."
                    )
                    raise PalcoError(msg)
                self.sendline(self._password)
                self.expect(self._shell_prompt)
            cmd = "sudo " + cmd
        self.sendline(cmd)

    # pylint: enable=duplicate-code
