"""Vitro exceptions for all plugins and modules used by framework."""

from typing import Any


class VitroError(Exception):
    """Base exception all vitro exceptions inherit from."""


class ShellPromptUndefinedError(VitroError):
    """Raise this when shell prompt is not defined."""


class DeviceConnectionError(VitroError):
    """Raise this on device connection error."""


class SSHConnectionError(DeviceConnectionError):
    """Raise this on SSH connection failure."""


class SCPConnectionError(DeviceConnectionError):
    """Raise this on SCP connection failure."""


class EnvConfigError(VitroError):
    """Raise this on environment configuration error."""


class DeviceRequirementError(VitroError):
    """Raise this on device requirement error."""


class DeviceNotFoundError(VitroError):
    """Raise this on device is not available."""


class FileLockTimeoutError(VitroError):
    """Raise this on file lock timeout."""


class ConfigurationFailureError(VitroError):
    """Raise this on device configuration failure."""


class DeviceBootFailureError(VitroError):
    """Raise this on device boot failure."""


class TR069ResponseErrorError(VitroError):
    """Raise this on TR069 response error."""


class TR069FaultCodeError(VitroError):
    """Raise this on TR069 response error."""

    faultdict: dict[str, Any]


class UseCaseFailureError(VitroError):
    """Raise this on failures in use cases."""


class NotSupportedError(VitroError):
    """Raise this on feature not supported."""


class SNMPError(VitroError):
    """Raise this on any SNMP related error."""


class VoiceError(VitroError):
    """Raise this on any voice related errors."""


# TODO: maybe move to testsuite
class TeardownError(VitroError):
    """Raise this on any test teardown failure."""


class ContingencyCheckError(VitroError):
    """Raise this on any contingency check failure."""


class WifiError(VitroError):
    """Raise this on any wifi related errors."""


class MulticastError(VitroError):
    """Raise this on any multicast related errors."""


class CodeError(VitroError):
    """Raise this if an code assert fails.

    This exception is only meant for custom assert
    clause used inside libraries.
    """
