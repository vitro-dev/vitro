"""Palco exceptions for all plugins and modules used by framework."""

from typing import Any


class PalcoError(Exception):
    """Base exception all palco exceptions inherit from."""


class DeviceConnectionError(PalcoError):
    """Raise this on device connection error."""


class SSHConnectionError(DeviceConnectionError):
    """Raise this on SSH connection failure."""


class SCPConnectionError(DeviceConnectionError):
    """Raise this on SCP connection failure."""


class EnvConfigError(PalcoError):
    """Raise this on environment configuration error."""


class DeviceRequirementError(PalcoError):
    """Raise this on device requirement error."""


class DeviceNotFoundError(PalcoError):
    """Raise this on device is not available."""


class FileLockTimeoutError(PalcoError):
    """Raise this on file lock timeout."""


class ConfigurationFailureError(PalcoError):
    """Raise this on device configuration failure."""


class DeviceBootFailureError(PalcoError):
    """Raise this on device boot failure."""


class TR069ResponseErrorError(PalcoError):
    """Raise this on TR069 response error."""


class TR069FaultCodeError(PalcoError):
    """Raise this on TR069 response error."""

    faultdict: dict[str, Any]


class UseCaseFailureError(PalcoError):
    """Raise this on failures in use cases."""


class NotSupportedError(PalcoError):
    """Raise this on feature not supported."""


class SNMPError(PalcoError):
    """Raise this on any SNMP related error."""


class VoiceError(PalcoError):
    """Raise this on any voice related errors."""


# TODO: maybe move to testsuite
class TeardownError(PalcoError):
    """Raise this on any test teardown failure."""


class ContingencyCheckError(PalcoError):
    """Raise this on any contingency check failure."""


class WifiError(PalcoError):
    """Raise this on any wifi related errors."""


class MulticastError(PalcoError):
    """Raise this on any multicast related errors."""


class CodeError(PalcoError):
    """Raise this if an code assert fails.

    This exception is only meant for custom assert
    clause used inside libraries.
    """
