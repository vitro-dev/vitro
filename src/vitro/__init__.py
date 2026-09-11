"""Automated testing of network devices."""

from __future__ import annotations

__version__ = "2025.12.17a0"

from pluggy import HookimplMarker, HookspecMarker

PROJECT_NAME = "vitro"

hookspec = HookspecMarker(PROJECT_NAME)
hookimpl = HookimplMarker(PROJECT_NAME)


__all__ = ["hookimpl", "hookspec"]
