"""Palco exceptions for all plugins and modules used by framework."""

from typing import Any


class PalcoException(Exception):
    """Base exception all palco exceptions inherit from."""


class DeviceConnectionError(PalcoException):
    """Raise this on device connection error."""


class SSHConnectionError(DeviceConnectionError):
    """Raise this on SSH connection failure."""


class SCPConnectionError(DeviceConnectionError):
    """Raise this on SCP connection failure."""


class EnvConfigError(PalcoException):
    """Raise this on environment configuration error."""


class DeviceRequirementError(PalcoException):
    """Raise this on device requirement error."""


class DeviceNotFound(PalcoException):
    """Raise this on device is not available."""


class FileLockTimeout(PalcoException):
    """Raise this on file lock timeout."""


class ConfigurationFailure(PalcoException):
    """Raise this on device configuration failure."""


class DeviceBootFailure(PalcoException):
    """Raise this on device boot failure."""


class TR069ResponseError(PalcoException):
    """Raise this on TR069 response error."""


class TR069FaultCode(PalcoException):
    """Raise this on TR069 response error."""

    faultdict: dict[str, Any]


class UseCaseFailure(PalcoException):
    """Raise this on failures in use cases."""


class NotSupportedError(PalcoException):
    """Raise this on feature not supported."""


class SNMPError(PalcoException):
    """Raise this on any SNMP related error."""


class VoiceError(PalcoException):
    """Raise this on any voice related errors."""


# TODO: maybe move to testsuite
class TeardownError(PalcoException):
    """Raise this on any test teardown failure."""


class ContingencyCheckError(PalcoException):
    """Raise this on any contingency check failure."""


class WifiError(PalcoException):
    """Raise this on any wifi related errors."""


class MulticastError(PalcoException):
    """Raise this on any multicast related errors."""


class CodeError(PalcoException):
    """Raise this if an code assert fails.

    This exception is only meant for custom assert
    clause used inside libraries.
    """
