"""Tests for the device hook specifications."""

from __future__ import annotations

import inspect

import pytest
from pluggy import PluginManager

from vitro import PROJECT_NAME, hookimpl
from vitro.plugins.hookspecs import devices as device_hookspecs

_LIFECYCLE_HOOKS = [
    name
    for name, _ in inspect.getmembers(device_hookspecs, inspect.isfunction)
    if name.startswith(("vitro_", "validate_")) and not name.endswith("_async")
]


@pytest.mark.parametrize("hook_name", _LIFECYCLE_HOOKS)
def test_every_lifecycle_hook_declares_an_async_twin(hook_name: str) -> None:
    """Declare a twin for every lifecycle hook, since setup_environment calls them.

    `_run_hook_async` reaches a twin by name, and `_is_async_hook_supported`
    decides whether to, so an undeclared twin is called through a hook caller
    that has no spec: no argument validation, and `check_pending()` would reject
    every plugin implementing it.

    Given each blocking lifecycle hook the module declares
    When its `_async` counterpart is looked for
    Then the counterpart is declared too
    """
    assert hasattr(device_hookspecs, f"{hook_name}_async")


def test_an_implementation_of_every_hook_leaves_nothing_pending() -> None:
    """Let a plugin implement every hook and still pass check_pending.

    Given a plugin implementing both variants of every lifecycle hook
    When it is registered and the plugin manager is asked for pending hooks
    Then none are pending, so a framework free to validate at startup can
    """
    plugin_manager = PluginManager(PROJECT_NAME)
    plugin_manager.add_hookspecs(device_hookspecs)

    class EveryHook:
        """A device implementing both variants of every lifecycle hook."""

    for name in _LIFECYCLE_HOOKS:
        setattr(EveryHook, name, hookimpl(lambda _self: None))
        setattr(EveryHook, f"{name}_async", hookimpl(_a_coroutine))

    plugin_manager.register(EveryHook(), "every-hook")

    plugin_manager.check_pending()


async def _a_coroutine(self: object) -> None:
    """Stand in for an async hook implementation.

    :param self: the device the hook is called on
    :type self: object
    """
