"""Unit tests for the Vitro connection factory module."""

import pytest
from pytest_mock import MockerFixture

from vitro.exceptions import EnvConfigError
from vitro.libraries.connection_factory import connection_factory
from vitro.libraries.connections.ssh_connection import SSHConnection
from vitro.libraries.vitro_pexpect import VitroPexpect


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
    mocker.patch.object(VitroPexpect, attribute="__init__", return_value=None)
    mocker.patch.multiple(VitroPexpect, __abstractmethods__=set())
    mocker.patch.object(SSHConnection, attribute="__init__", return_value=None)
    connection = connection_factory(
        "ssh_connection",
        "connection",
        username="root",
        password="",
    )
    assert isinstance(connection, SSHConnection)
