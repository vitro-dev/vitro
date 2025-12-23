"""Palco core plugin."""

import logging
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from collections import ChainMap
from collections.abc import Generator
from typing import Any

from pluggy import PluginManager

from palco import hookimpl
from palco.devices.base_devices import PalcoDevice
from palco.exceptions import EnvConfigError
from palco.lib.device_manager import DeviceManager
from palco.lib.palco_config import PalcoConfig, parse_palco_config
from palco.plugins.hookspecs import devices as device_spec

_LOGGER = logging.getLogger(__name__)


def _non_empty_str(arg: str) -> str:
    """Type to check palco/pytest command line arguments empty value.

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
def palco_add_hookspecs(plugin_manager: PluginManager) -> None:
    """Add palco core plugin hookspecs.

    :param plugin_manager: plugin manager
    :type plugin_manager: PluginManager
    """
    plugin_manager.add_hookspecs(device_spec)


@hookimpl
def palco_add_cmdline_args(argparser: ArgumentParser) -> None:
    """Add palco command line arguments.

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
def palco_cmdline_parse(
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
def palco_parse_config(
    # pylint: disable=W0613
    cmdline_args: Namespace,  # noqa: ARG001
    inventory_config: dict[str, Any],
    env_config: dict[str, Any],
) -> PalcoConfig:
    """Parse the configs.

    This hook allows for the modification (if needed) of the configuration files.

    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param inventory_config: inventory json
    :type inventory_config: dict[str, Any]
    :param env_config: environment json
    :type env_config: dict[str, Any]
    :return: the palcom config
    :rtype: PalcoConfig
    """
    return parse_palco_config(inventory_config, env_config)


@hookimpl
def palco_add_devices() -> dict[str, type[PalcoDevice]]:
    """Add devices to known devices for deployment.

    :returns: devices dictionary
    """
    return {}


@hookimpl
def palco_register_devices(
    config: PalcoConfig,
    cmdline_args: Namespace,
    plugin_manager: PluginManager,
) -> DeviceManager:
    """Register devices as plugin with palco.

    :param config: palco config
    :type config: PalcoConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param plugin_manager: plugin manager
    :type plugin_manager: PluginManager
    :raises EnvConfigError: when a device in inventory is unknown to palco
    :return: device manager with all registered devices
    :rtype: DeviceManager
    """
    device_manager = DeviceManager(plugin_manager)
    known_devices_list = ChainMap(*plugin_manager.hook.palco_add_devices())
    to_be_ignored = cmdline_args.ignore_devices.split(",")
    for device_config in config.get_devices_config():
        if device_config.get("name") in to_be_ignored:
            _LOGGER.warning("Ignoring '%s'", device_config.get("name"))
            continue
        device_type = device_config.get("type")
        if device_type in known_devices_list:
            device_obj = known_devices_list.get(device_type)(
                device_config,
                cmdline_args,
            )
            device_manager.register_device(device_obj)
        else:
            msg = (
                f"{device_type} - Unknown palco device, please register "
                f"{device_type} device using palco_add_devices hook"
            )
            raise EnvConfigError(msg)

    return device_manager


@hookimpl(hookwrapper=True)
def palco_release_devices(
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
    plugin_manager.hook.palco_shutdown_device(device_manager=device_manager)
    yield
