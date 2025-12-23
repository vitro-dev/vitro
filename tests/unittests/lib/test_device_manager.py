"""Unit tests for the Palco device manager module."""

import re

import pytest

from pytest_mock import MockerFixture

from palco.devices.base_devices import PalcoDevice

from palco.lib.device_manager import DeviceManager, get_device_manager
from palco.main import get_plugin_manager



class DummyDevice(PalcoDevice):
    """Dummy Palco Device class for testing."""


class InvalidDevice:
    """Invalid Device class for testing."""


@pytest.fixture(scope="function", name="device_manager")
def device_manager_fixture() -> DeviceManager:
    try:
        return DeviceManager(get_plugin_manager())
    except ValueError:
        return get_device_manager()


def test_device_manager_singleton(device_manager: DeviceManager) -> None:
    """Ensure exception raised when try to instantiate DeviceManager class again.

    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """
    assert device_manager
    with pytest.raises(
        ValueError, match=re.escape("DeviceManager is already initialized.")
    ):
        DeviceManager(get_plugin_manager())











def test_register_device_valid_palco_device(device_manager: DeviceManager) -> None:
    """Verify a new device is registered successfully.

    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """
    device_temp = DummyDevice({"name": "tmpdev", "type": "tmp"}, None)
    device_manager.register_device(device_temp)
    assert device_temp == get_plugin_manager().get_plugin("tmpdev")


def test_register_device_invalid_device_attribute_error(
    device_manager: DeviceManager,
) -> None:
    """Ensure error is raised when try to register a non PalcoDevice.

    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """
    invalid_device = InvalidDevice()
    with pytest.raises(
        AttributeError,
        match="'InvalidDevice' object has no attribute 'device_name'",
    ):
        device_manager.register_device(invalid_device)


def test_register_device_already_registered_error(
    device_manager: DeviceManager,
) -> None:
    """Ensure that a "ValueError" error is raised when try to register a device again.

    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """
    test_device = DummyDevice({"name": "test", "type": "test_device"}, None)
    device_manager.register_device(test_device)
    error_msg = "Plugin name already registered: .*"
    with pytest.raises(ValueError, match=error_msg):
        device_manager.register_device(test_device)


def test_unregister_device_registered_in_plugin(device_manager: DeviceManager) -> None:
    """Verify if a device can be un registered from plugins list.

    :param device_manager: device manager instance
    :type device_manager: DeviceManager
    """
    plugin_manager = get_plugin_manager()
    if not plugin_manager.has_plugin("dummy"):
        device_manager.register_device(
            DummyDevice({"name": "dummy", "type": "hello"}, None),
        )
    device_manager.unregister_device("dummy")
    assert not plugin_manager.has_plugin("dummy")
