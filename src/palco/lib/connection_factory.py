"""Connection decider module."""

from typing import Any

from palco.exceptions import EnvConfigError
from palco.lib.connections.ldap_authenticated_serial import LdapAuthenticatedSerial
from palco.lib.connections.local_cmd import LocalCmd
from palco.lib.connections.ser2net_connection import Ser2NetConnection
from palco.lib.connections.serial_connection import SerialConnection
from palco.lib.connections.ssh_connection import SSHConnection
from palco.lib.connections.telnet import TelnetConnection
from palco.lib.palco_pexpect import PalcoPexpect


def connection_factory(
    connection_type: str,
    connection_name: str,
    **kwargs: Any,  # noqa: ANN401
) -> PalcoPexpect:
    """Return connection of given type.

    :param connection_type: type of the connection
    :param connection_name: name of the connection
    :param kwargs: arguments to the connection
    :returns: PalcoPexpect: connection of given type
    :raises EnvConfigError: when given connection type is not supported
    """
    connection_dispatcher = {
        "ssh_connection": SSHConnection,
        "authenticated_ssh": SSHConnection,
        "ldap_authenticated_serial": LdapAuthenticatedSerial,
        "local_cmd": LocalCmd,
        "serial": SerialConnection,
        "ser2net": _ser2net_param_parser,
        "telnet": _telnet_param_parser,
    }
    connection_obj = connection_dispatcher.get(connection_type)
    if connection_obj is not None and callable(connection_obj):
        if connection_type == "ssh_connection":
            kwargs.pop("password")
        return connection_obj(connection_name, **kwargs)
    # Handle unsupported connection types
    msg = f"Unsupported connection type: {connection_type}"
    raise EnvConfigError(msg)


def _telnet_param_parser(
    connection_name: str,
    **kwargs: Any,  # noqa: ANN401
) -> TelnetConnection:
    return TelnetConnection(
        session_name=connection_name,
        command="telnet",
        save_console_logs=kwargs.pop("save_console_logs"),
        args=[
            kwargs["ip_addr"],
            kwargs["port"],
            kwargs["shell_prompt"],
        ],
    )


def _ser2net_param_parser(
    connection_name: str,
    **kwargs: Any,  # noqa: ANN401
) -> Ser2NetConnection:
    return Ser2NetConnection(
        connection_name,
        "telnet",
        kwargs.get("save_console_logs"),
        [
            kwargs["ip_addr"],
            kwargs["port"],
            kwargs["shell_prompt"],
        ],
    )
