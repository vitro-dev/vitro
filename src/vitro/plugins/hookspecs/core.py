# mypy: disable-error-code="empty-body"
"""Vitro main hook specifications."""

from argparse import ArgumentParser, Namespace
from typing import Any

from pluggy import PluginManager

from vitro import hookspec
from vitro.devices.base_devices import VitroDevice
from vitro.libraries.device_manager import DeviceManager
from vitro.libraries.vitro_config import VitroConfig

# pylint: disable=unused-argument


@hookspec
def vitro_add_hookspecs(plugin_manager: PluginManager) -> None:
    """Add new hookspecs to extend and/or update the framework.

    :param plugin_manager: plugin manager
    :type plugin_manager: PluginManager
    """


@hookspec
def vitro_add_cmdline_args(argparser: ArgumentParser) -> None:
    """Add new command line argument(s).

    :param argparser: argument parser
    :type argparser: ArgumentParser
    """


@hookspec(firstresult=True)
def vitro_parse_config(
    cmdline_args: Namespace,
    inventory_config: dict[str, Any],
    env_config: dict[str, Any],
) -> VitroConfig:
    """Parse the config.

    This hook allows for the modification (if needed) of the configuration files,
    like inventory and environment, by using cmd line overrides.

    # noqa: DAR202

    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param inventory_config: inventory json
    :type inventory_config: dict[str, Any]
    :param env_config: environment json
    :type env_config: dict[str, Any]
    :return: a VitroConfig object
    :rtype: VitroConfig
    """


@hookspec(firstresult=True)
def vitro_cmdline_parse(
    argparser: ArgumentParser,
    cmdline_args: list[str],
) -> Namespace:
    """Parse command line arguments.

    # noqa: DAR202

    :param argparser: argument parser
    :type argparser: ArgumentParser
    :param cmdline_args: command line arguments
    :type cmdline_args: list[str]
    :return: command line arguments
    :rtype: Namespace
    """


@hookspec
def vitro_configure(cmdline_args: Namespace, plugin_manager: PluginManager) -> None:
    """Configure vitro based on command line arguments or environment config.

    This hook allows to register/deregister vitro plugins when you pass a
    command line argument. This way a plugin will be registered to vitro only
    when required.

    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param plugin_manager: plugin manager
    :type plugin_manager: PluginManager
    """


@hookspec(firstresult=True)
def vitro_reserve_devices(
    cmdline_args: Namespace,
    plugin_manager: PluginManager,
) -> dict[str, Any]:
    """Reserve devices before starting the deployment.

    This hook is used to reserve devices before deployment.

    # noqa: DAR202
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param plugin_manager: plugin manager instance
    :type plugin_manager: PluginManager
    :return: inventory configuration
    :rtype: dict[str, Any]
    """


@hookspec(firstresult=True)
def vitro_setup_env(
    config: VitroConfig,
    cmdline_args: Namespace,
    plugin_manager: PluginManager,
    device_manager: DeviceManager,
) -> DeviceManager:
    """Vitro environment setup for all the devices.

    This hook is used to deploy vitro devices.

    # noqa: DAR202
    :param config: vitro config
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param plugin_manager: plugin manager instance
    :type plugin_manager: PluginManager
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    :return: device manager with all devices in the environment
    :rtype: DeviceManager
    """


@hookspec
def vitro_post_setup_env(
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Call after the environment setup is completed for all the devices.

    This hook is used to perform required operations after the board is deployed.

    # noqa: DAR202
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_release_devices(
    config: VitroConfig,
    cmdline_args: Namespace,
    plugin_manager: PluginManager,
    deployment_status: dict[str, Any],
    device_manager: DeviceManager,
) -> None:
    """Release reserved devices after use.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param plugin_manager: plugin manager instance
    :type plugin_manager: PluginManager
    :param deployment_status: deployment status data
    :type deployment_status: Dict[str, Any]
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec(firstresult=True)
def vitro_register_devices(
    config: VitroConfig,
    cmdline_args: Namespace,
    plugin_manager: PluginManager,
) -> DeviceManager:
    """Register device to plugin manager.

    This hook is responsible to register devices to the device manager after
    initialization based on the given inventory and environment config.

    # noqa: DAR202
    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param plugin_manager: plugin manager instance
    :type plugin_manager: PluginManager
    :return: device manager with all registered devices
    :rtype: DeviceManager
    """


@hookspec
def vitro_add_devices() -> dict[str, type[VitroDevice]]:
    """Add devices to known devices list.

    This hook is used to let vitro know the devices which are configured
    in the inventory config.
    Each repo with a vitro device should implement this hook to add each
    devices to the list of known devices.

    # noqa: DAR202
    :return: dictionary with device name and class
    :rtype: dict[str, type[VitroDevice]]
    """


@hookspec
def vitro_shutdown_device(device_manager: DeviceManager) -> None:
    """Shutdown vitro device after use.

    This hook should be used by a device to perform a clean shutdown of a device
    after releasing all the resources (e.g. close all of the open ssh connections)
    before the shutdown of the framework.

    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """
