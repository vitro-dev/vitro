"""Vitro core plugin."""

import logging
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from collections import ChainMap
from collections.abc import Generator
from typing import Any

from pluggy import PluginManager

from vitro import hookimpl
from vitro.devices.base_devices import VitroDevice
from vitro.exceptions import EnvConfigError
from vitro.libraries.device_manager import DeviceManager
from vitro.libraries.vitro_config import VitroConfig, parse_vitro_config
from vitro.plugins.hookspecs import devices as device_spec

_LOGGER = logging.getLogger(__name__)


def _non_empty_str(arg: str) -> str:
    """Type to check vitro/pytest command line arguments empty value.

    :param arg: command line argument
    :type arg: str
    :raises ArgumentTypeError: raises argparse ArgumentTypeError
                    for empty argument values
    :return: arg if the argument is non empty
    :rtype: str
    """
    if arg:
        return arg
    message = "Argument value should not be empty"
    raise ArgumentTypeError(message)


@hookimpl
def vitro_add_hookspecs(plugin_manager: PluginManager) -> None:
    """Add vitro core plugin hookspecs.

    :param plugin_manager: plugin manager
    :type plugin_manager: PluginManager
    """
    plugin_manager.add_hookspecs(device_spec)


@hookimpl
def vitro_add_cmdline_args(argparser: ArgumentParser) -> None:
    """Add vitro command line arguments.

    :param argparser: argument parser
    :type argparser: ArgumentParser
    """
    argparser.add_argument(
        "--board-name",
        type=_non_empty_str,
        required=False,
        help="Board name",
    )
    argparser.add_argument(
        "--env-config",
        type=_non_empty_str,
        required=True,
        help="Environment JSON config file path",
    )
    argparser.add_argument(
        "--inventory-config",
        type=_non_empty_str,
        required=False,
        help="Inventory JSON config file path",
    )
    argparser.add_argument(
        "--legacy",
        action="store_true",
        help="allows for devices.<device> obj to be exposed (only for legacy use)",
    )
    argparser.add_argument(
        "--skip-boot",
        action="store_true",
        help="Skips the booting process, all devices will be used as they are",
    )
    argparser.add_argument(
        "--skip-contingency-checks",
        action="store_true",
        help="Skip contingency checks while running tests",
    )
    argparser.add_argument(
        "--save-console-logs",
        default="",  # does not save the logs by default
        help="Save the console logs at the give location",
    )
    argparser.add_argument(
        "--ignore-devices",
        default="",
        help=(
            "Ignore the given devices (names are comma separated)."
            " Useful when a device is incommunicado"
        ),
    )


@hookimpl
def vitro_cmdline_parse(
    argparser: ArgumentParser,
    cmdline_args: list[str],
) -> Namespace:
    """Parse command line arguments.

    :param argparser: argument parser instance
    :type argparser: ArgumentParser
    :param cmdline_args: command line arguments list
    :type cmdline_args: list[str]
    :return: command line arguments
    :rtype: Namespace
    """
    return argparser.parse_args(args=cmdline_args)


@hookimpl
def vitro_parse_config(
    # pylint: disable=W0613
    cmdline_args: Namespace,  # noqa: ARG001
    inventory_config: dict[str, Any],
    env_config: dict[str, Any],
) -> VitroConfig:
    """Parse the configs.

    This hook allows for the modification (if needed) of the configuration files.

    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param inventory_config: inventory json
    :type inventory_config: dict[str, Any]
    :param env_config: environment json
    :type env_config: dict[str, Any]
    :return: the vitrom config
    :rtype: VitroConfig
    """
    return parse_vitro_config(inventory_config, env_config)


@hookimpl
def vitro_add_devices() -> dict[str, type[VitroDevice]]:
    """Add devices to known devices for deployment.

    :returns: devices dictionary
    """
    return {}


@hookimpl
def vitro_register_devices(
    config: VitroConfig,
    cmdline_args: Namespace,
    plugin_manager: PluginManager,
) -> DeviceManager:
    """Register devices as plugin with vitro.

    :param config: vitro config
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param plugin_manager: plugin manager
    :type plugin_manager: PluginManager
    :raises EnvConfigError: when a device in inventory is unknown to vitro
    :return: device manager with all registered devices
    :rtype: DeviceManager
    """
    device_manager = DeviceManager(plugin_manager)
    known_devices_list = ChainMap(*plugin_manager.hook.vitro_add_devices())
    to_be_ignored = cmdline_args.ignore_devices.split(",")
    for device_config in config.get_devices_config():
        if device_config.get("name") in to_be_ignored:
            _LOGGER.warning("Ignoring '%s'", device_config.get("name"))
            continue
        device_type = device_config.get("type")
        if device_type in known_devices_list:
            device_class = known_devices_list.get(device_type)
            if device_class is None:
                continue
            device_obj = device_class(device_config, cmdline_args)
            device_manager.register_device(device_obj)
        else:
            msg = (
                f"{device_type} - Unknown vitro device, please register "
                f"{device_type} device using vitro_add_devices hook"
            )
            raise EnvConfigError(msg)

    return device_manager


@hookimpl(hookwrapper=True)
def vitro_release_devices(
    plugin_manager: PluginManager,
    device_manager: DeviceManager,
) -> Generator[None, None, None]:
    """Shutdown all the devices before releasing them.

    :param plugin_manager: plugin manager instance
    :type plugin_manager: PluginManager
    :param device_manager: device manager with all registered devices
    :type device_manager: DeviceManager
    :yield: None
    :rtype: Generator[None,None,None]
    """
    plugin_manager.hook.vitro_shutdown_device(device_manager=device_manager)
    yield
