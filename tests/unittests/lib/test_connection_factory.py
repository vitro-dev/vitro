"""Unit tests for the Palco connection factory module."""

import pytest
from pytest_mock import MockerFixture

from palco.exceptions import EnvConfigError
from palco.lib.palco_pexpect import PalcoPexpect
from palco.lib.connection_factory import connection_factory
from palco.lib.connections.ssh_connection import SSHConnection


def test_connection_factory_invalid_connection_type() -> None:
    """Ensure an invalid connection type is handled."""
    with pytest.raises(
        EnvConfigError,
        match="Unsupported connection type: invalid_connection",
    ):
        connection_factory("invalid_connection", "ssh-connection")


def test_connection_factory_valid_connection_type(mocker: MockerFixture) -> None:
    """Ensure connection factory returns valid connection type.

    :param mocker: pytest mock object
    :type mocker: MockerFixture
    """
    mocker.patch.object(PalcoPexpect, attribute="__init__", return_value=None)
    mocker.patch.multiple(PalcoPexpect, __abstractmethods__=set())
    mocker.patch.object(SSHConnection, attribute="__init__", return_value=None)
    connection = connection_factory(
        "ssh_connection",
        "connection",
        username="root",
        password="",
    )
    assert isinstance(connection, SSHConnection)
