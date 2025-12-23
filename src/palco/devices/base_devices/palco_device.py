"""Palco base device template."""

from argparse import Namespace

from palco.lib.palco_pexpect import PalcoPexpect
from palco.type_hints import DeviceConfigType


class PalcoDevice:
    """Palco base device which all devices inherit from."""

    def __init__(self, config: DeviceConfigType, cmdline_args: Namespace) -> None:
        """Initialize palco base device.

        :param config: device configuration
        :param cmdline_args: command line arguments
        """
        self._config: DeviceConfigType = config
        self._cmdline_args = cmdline_args

    def _extract_property_value(self, property_name: str) -> str:
        name = self._config.get(property_name)
        if name is None:
            msg = f"{property_name} is not set in the configuration: {self._config=}"
            raise RuntimeError(msg)
        return name

    @property
    def config(self) -> DeviceConfigType:
        """Get device configuration.

        :returns: device configuration
        """
        return self._config

    @property
    def device_name(self) -> str:
        """Get name of the device.

        :returns: device name
        """
        return self._extract_property_value("name")

    @property
    def device_type(self) -> str:
        """Get type of the device.

        :returns: device type
        """
        return self._extract_property_value("type")

    def get_interactive_consoles(self) -> dict[str, PalcoPexpect]:
        """Get interactive consoles from device.

        :returns: interactive consoles of the device
        """
        return {}
