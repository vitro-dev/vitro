"""Vitro plugin to support parsing the config files passed as arguments."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vitro import hookimpl
from vitro.libraries.vitro_config import get_inventory_config

if TYPE_CHECKING:
    from argparse import Namespace


@hookimpl
def vitro_reserve_devices(cmdline_args: Namespace) -> dict[str, Any]:
    """Return inventory config after reservation check.

    In scenarios where board reservation is not needed,
    the devices can be accessed directly by using no_reservation plugin.

    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :return: inventory configuration
    :rtype: dict[str, Any]
    """
    return get_inventory_config(cmdline_args.board_name, cmdline_args.inventory_config)
