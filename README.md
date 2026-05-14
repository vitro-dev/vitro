# Palco

Palco is a Python framework for setting up and operating testbed
environments — deploying, configuring, and orchestrating the devices that
make up a system under test. It is the second-generation successor to
Boardfarm, distilling its lessons into a leaner, plugin-driven core.

## Background

The previous generation packaged the framework, a large built-in device
library, and test integrations together in a single project. Palco splits
those concerns: the core is a small orchestrator that knows nothing about
specific devices or test runners. Device drivers, environment helpers, and
reservation systems are contributed externally as plugins. A separate,
shared template/operations pool can be layered on top to keep multiple
plugins interoperable.

The result is a framework you can adopt for a single testbed without
pulling in code for every device anyone has ever supported, while still
allowing standardised test resources to be assembled across organisations.

## What Palco gives you

- **Two-file environment model.** A standardised `environment.json`
  (devices and their roles) merged with a testbed-specific
  `inventory.json` (connection details) via `jsonmerge`.
- **Pluggable device registry.** Plugins contribute device classes via the
  `palco_add_devices` hook; Palco wires them up by type string from the
  config.
- **Lifecycle hooks.** Boot and configure phases, distinct for *servers*,
  *devices*, and *attached devices*, with sync and async variants.
- **Plugin extension surface (pluggy).** Reservation, command-line args,
  config parsing, environment setup, and shutdown are all hookable.
- **Connection helpers.** Pexpect-based SSH, serial, and local-command
  connections in `palco.libraries.connections`.
- **`palco` CLI.** A standalone entry point that drives the full
  reserve → register → boot → configure cycle from a JSON config pair.

## Quick start

Install:

```bash
pip install palco
```

A minimal device plugin lives in your own package. The device class
subclasses `PalcoDevice` and implements lifecycle methods that Palco
discovers by name; a module-level `@hookimpl` registers the device type
string with the framework:

```python
# my_plugin/__init__.py
from palco import hookimpl
from palco.devices.base_devices import PalcoDevice


class MyBox(PalcoDevice):
    """Driver for the device type "my_box"."""

    def palco_device_boot(self, config, cmdline_args, device_manager):
        """Boot sequence — connect, verify required tools, etc."""
        ...

    def palco_device_configure(self, config, cmdline_args, device_manager):
        """Apply post-boot configuration."""
        ...


@hookimpl
def palco_add_devices() -> dict[str, type[PalcoDevice]]:
    """Tell Palco about our device type."""
    return {"my_box": MyBox}
```

Register the package as a Palco plugin via a setuptools entry point:

```toml
# pyproject.toml
[project.entry-points."palco"]
my_plugin = "my_plugin"
```

With an `environment.json` that references `"type": "my_box"` for one or
more devices, and an `inventory.json` providing their connection details,
run:

```bash
palco --board-name my-testbed \
      --env-config environment.json \
      --inventory-config inventory.json
```

Palco will reserve, register, boot, and configure the devices, then keep
them available for the next stage of your workflow — interactive
exploration, automated tests via `pytest-palco`, or any other consumer
of the live device manager.

## Where it fits

Palco is deliberately framework-agnostic. It does not assume a particular
test runner, a particular device library, or a particular reservation
system. Two companion projects layer on top when useful:

- A pytest bridge (`pytest-palco`) exposes the live device manager as
  fixtures so you can write tests against booted devices.
- A shared template/operations pool (`palco-commons`) can sit between Palco and your plugins, providing standardised contracts that multiple testbed plugins
  can conform to. This is the path for sharing tests across organisations.

Both are separate, optional packages — Palco can be used without either.

## Contributing

Contributions are welcome. Please open an issue describing the change you
have in mind before sending a substantial pull request.

## License

See [LICENSE](LICENSE).
