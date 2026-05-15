"""Unit tests for docker-compose generator module."""

from __future__ import annotations

from json import loads
from pathlib import Path

import pytest
from vitro.libraries.vitro_config import get_json, parse_vitro_config

from vitro.libraries.docker_factory.docker_compose_generator import (
    DockerComposeGenerator,
)

_TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture(name="template_manager")
def fixture_template_manager() -> DockerComposeGenerator:
    """Return a DockerComposeGenerator instance."""
    ams_path = _TEST_DATA_DIR / "ams.json"
    environment_json_path = _TEST_DATA_DIR / "test_environment.json"
    inventory_json = loads(ams_path.read_text())
    vitro_config = parse_vitro_config(
        inventory_json["F5685LGE-1-1"],
        get_json(environment_json_path.as_posix()),
    )
    return DockerComposeGenerator(vitro_config)


def test_docker_compose_generator(template_manager: DockerComposeGenerator) -> None:
    """Verify docker-compose generation produces expected output."""
    expected_compose_path = _TEST_DATA_DIR / "expected_compose.json"
    expected_compose = loads(expected_compose_path.read_text())
    assert dict(sorted(template_manager.generate_docker_compose().items())) == dict(
        sorted(expected_compose.items()),
    )


@pytest.mark.parametrize(
    (
        "data",
        "val_from",
        "val_to",
        "expected",
    ),
    [
        ([1, 2, 3], 2, "a", [1, "a", 3]),
        ({"a": 1, "b": 2}, 2, "x", {"a": 1, "b": "x"}),
    ],
)
def test_replace_basic(
    template_manager: DockerComposeGenerator,
    data: list[int],
    val_from: int,
    val_to: str,
    expected: list[int | str],
) -> None:
    """Verify basic value replacement in lists and dicts."""
    actual = template_manager._replace(data, val_from, val_to)
    assert actual == expected


@pytest.mark.parametrize(
    ("data", "val_from", "val_to"),
    [([[1, 2], [3, 4]], 2, "a"), ({"a": {"b": 2}}, 2, "x")],
)
def test_replace_nested(
    template_manager: DockerComposeGenerator,
    data: list[list[int]] | dict[str, int],
    val_from: int,
    val_to: str,
) -> None:
    """Verify value replacement in nested structures."""
    actual = template_manager._replace(data, val_from, val_to)
    expected = template_manager._replace(data, val_from, val_to)
    assert actual == expected


def test_replace_no_match(template_manager: DockerComposeGenerator) -> None:
    """Verify data remains unchanged when value is not found."""
    data = [1, 2, 3]
    val_from = 4
    val_to = "x"
    actual = template_manager._replace(data, val_from, val_to)
    assert actual == data
