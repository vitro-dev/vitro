"""Vitro device hook specifications.

A Vitro device should belong to one of the following categories:

    1. server, i.e. DHCP, ACS...
    2. device, i.e. a connectivity CPE
    3. attached device, i.e. a LAN client


Every device should fulfill the following responsibilities at
different stages of the deployment.

Hook responsibilities:

    1. skip boot
        - device can be interacted with as it is without making
          any changes to it

    2. boot
        - device is running with required software
        - device can be interacted with, e.g. via console
        - device has a management IP address or direct console access
          if the device has a console

    3. configure
        - all of the points from boot
        - user driven configurations are applied to the device
        - device has a service IP address if applicable
            Eg: A CPE device has access network IP address,
                eRouter IP, except in disabled mode, eMTA IP
        - for Wi-Fi clients, no connection to the Wi-Fi network
          is made and no IP address on service interface is assigned
"""

from argparse import Namespace
from typing import Any

from vitro import hookspec
from vitro.libraries.device_manager import DeviceManager
from vitro.libraries.vitro_config import VitroConfig

# pylint: disable=unused-argument


@hookspec
def vitro_server_boot(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Boot vitro server device.

    This hook should be used to boot a device which is not dependent on other
    devices in the environment. E.g. WAN and CMTS.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
async def vitro_server_boot_async(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Boot vitro server device.

    This hook should be used to boot a device which is not dependent on other
    devices in the environment. E.g. WAN and CMTS.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_skip_boot(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Skips the booting for the device connected.

    This hook skip the booting process on those
    devices that implement the boot_device hook

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
async def vitro_skip_boot_async(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Skips the booting for the device connected.

    This hook skip the booting process on those
    devices that implement the boot_device hook

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_server_configure(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Configure vitro server device.

    This hook should be used to configure a device, after having it booted,
    which is not dependent on other devices in the environment. E.g. WAN and CMTS

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_server_configure_async(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Configure vitro server device leveraging the asyncio library.

    This hook should be used to configure a device, after having it booted,
    which is not dependent on other devices in the environment. E.g. WAN and CMTS
    To be used for the asynchronous implementation.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_device_boot(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Boot vitro device.

    This hook should be used to boot a device which is dependent on one or more
    servers in the environment. E.g. CPE.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_device_configure(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Configure vitro device.

    This hook should be used to configure a device, after having it booted,
    which is dependent on one or more servers in the environment. E.g. CPE.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
async def vitro_device_configure_async(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Configure vitro device.

    This hook should be used to configure a device, after having it booted,
    which is dependent on one or more servers in the environment. E.g. CPE.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_attached_device_boot(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Boot vitro attached device.

    This hook should be used to boot a device which is attached to a device
    in the environment. E.g. LAN.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
async def vitro_attached_device_boot_async(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Boot vitro attached device leveraging the asyncio library.

    This hook should be used to boot a device which is attached to a device
    in the environment. E.g. LAN.
    To be used for the asynchronous implementation.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def vitro_attached_device_configure(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Configure vitro attached device.

    This hook should be used to configure a device, after having it booted,
    which is attached to a device in the environment. E.g. LAN.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
async def vitro_attached_device_configure_async(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Configure vitro attached device.

    This hook should be used to configure a device, after having it booted,
    which is attached to a device in the environment. E.g. LAN.
    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def contingency_check(env_req: dict[str, Any], device_manager: DeviceManager) -> None:
    """Perform contingency check to make sure the device is working fine before use.

    This hook could be used by any device.
    It is used by the pytest-vitro plugin to make sure the device is in
    good condition before running each test.

    :param env_req: environment request dictionary
    :type env_req: dict[str, Any]
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
def validate_device_requirements(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Validate device requirements.

    This hook is responsible to validate the requirements of a device before
    deploying devices to the environment.
    This allows us to fail the deployment early.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """


@hookspec
async def validate_device_requirements_async(
    config: VitroConfig,
    cmdline_args: Namespace,
    device_manager: DeviceManager,
) -> None:
    """Validate device requirements.

    This hook is responsible to validate the requirements of a device before
    deploying devices to the environment.
    This allows us to fail the deployment early.

    :param config: vitro config instance
    :type config: VitroConfig
    :param cmdline_args: command line arguments
    :type cmdline_args: Namespace
    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """
