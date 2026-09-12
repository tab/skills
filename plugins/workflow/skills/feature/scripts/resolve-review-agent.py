#!/usr/bin/env python3
"""Resolve review-only model settings from bundled and project config."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


GATES = {"plan", "code", "pr", "follow-up"}
OVERRIDE_PATHS = {
    "codex": Path(".codex/feature-review.json"),
    "claude": Path(".claude/feature-review.json"),
}
DEFAULTS = Path(__file__).resolve().parents[1] / "references" / "review-agents.json"


class ConfigError(ValueError):
    """Report one invalid review config value."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ConfigError(f"missing file: {path}") from error
    except json.JSONDecodeError as error:
        raise ConfigError(f"invalid JSON in {path}: {error}") from error

    if not isinstance(value, dict):
        raise ConfigError(f"expected a JSON object in {path}")
    return value


def require_keys(value: dict[str, Any], allowed: set[str], path: Path, label: str) -> None:
    unknown = set(value) - allowed
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ConfigError(f"unknown {label} key in {path}: {names}")


def require_text(value: Any, path: Path, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{field} in {path} must be a non-empty string")
    return value


def validate_gate(
    value: Any,
    path: Path,
    label: str,
    *,
    require_both: bool,
) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ConfigError(f"{label} in {path} must be an object")
    require_keys(value, {"model", "effort"}, path, label)
    if require_both and set(value) != {"model", "effort"}:
        raise ConfigError(f"{label} in {path} must set model and effort")
    if not value:
        raise ConfigError(f"{label} in {path} must set model, effort or both")
    return {field: require_text(raw, path, f"{label}.{field}") for field, raw in value.items()}


def merged_bundled_gate(config: dict[str, Any], reviewer: str, gate: str) -> dict[str, str]:
    selected = dict(config["default"]["gates"][gate])
    reviewer_config = config["reviewers"].get(reviewer)
    if reviewer_config:
        selected.update(reviewer_config["gates"].get(gate, {}))
    return selected


def load_defaults(path: Path) -> dict[str, Any]:
    config = load_object(path)
    require_keys(config, {"version", "default", "reviewers"}, path, "top-level")
    if type(config.get("version")) is not int or config["version"] != 1:
        raise ConfigError(f"version in {path} must be 1")

    default = config.get("default")
    if not isinstance(default, dict):
        raise ConfigError(f"default in {path} must be an object")
    require_keys(default, {"reviewer", "gates"}, path, "default")
    if set(default) != {"reviewer", "gates"}:
        raise ConfigError(f"default in {path} must set reviewer and gates")
    default_reviewer = require_text(default.get("reviewer"), path, "default.reviewer")

    default_gates = default.get("gates")
    if not isinstance(default_gates, dict) or set(default_gates) != GATES:
        raise ConfigError(f"default.gates in {path} must configure every review gate")
    for gate, gate_config in default_gates.items():
        default_gates[gate] = validate_gate(
            gate_config,
            path,
            f"default gate {gate}",
            require_both=True,
        )

    reviewers = config.get("reviewers")
    if not isinstance(reviewers, dict):
        raise ConfigError(f"reviewers in {path} must be an object")
    if default_reviewer in reviewers:
        raise ConfigError(f"default.reviewer in {path} must not be repeated in reviewers")

    for reviewer, reviewer_config in reviewers.items():
        require_text(reviewer, path, "reviewer name")
        if not isinstance(reviewer_config, dict):
            raise ConfigError(f"reviewer {reviewer} in {path} must be an object")
        require_keys(reviewer_config, {"gates"}, path, f"reviewer {reviewer}")
        gates = reviewer_config.get("gates")
        if not isinstance(gates, dict) or not gates:
            raise ConfigError(f"reviewer {reviewer} gates in {path} must be a non-empty object")
        unknown_gates = set(gates) - GATES
        if unknown_gates:
            names = ", ".join(sorted(unknown_gates))
            raise ConfigError(f"unknown reviewer {reviewer} gate in {path}: {names}")
        for gate, gate_config in gates.items():
            gates[gate] = validate_gate(
                gate_config,
                path,
                f"reviewer {reviewer} gate {gate}",
                require_both=False,
            )
        for gate in GATES:
            if set(merged_bundled_gate(config, reviewer, gate)) != {"model", "effort"}:
                raise ConfigError(f"reviewer {reviewer} gate {gate} in {path} must resolve model and effort")

    return config


def load_override(path: Path) -> dict[str, dict[str, str]]:
    config = load_object(path)
    require_keys(config, {"version", "gates"}, path, "top-level")
    if type(config.get("version")) is not int or config["version"] != 1:
        raise ConfigError(f"version in {path} must be 1")

    gates = config.get("gates")
    if not isinstance(gates, dict) or not gates:
        raise ConfigError(f"gates in {path} must be a non-empty object")

    unknown_gates = set(gates) - GATES
    if unknown_gates:
        names = ", ".join(sorted(unknown_gates))
        raise ConfigError(f"unknown gate in {path}: {names}")

    return {
        gate: validate_gate(value, path, f"gate {gate}", require_both=False)
        for gate, value in gates.items()
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--gate", required=True)
    parser.add_argument("--reviewer")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        project_root = args.project_root.resolve(strict=True)
        if not project_root.is_dir():
            raise ConfigError(f"project root is not a directory: {project_root}")
        if args.gate not in GATES:
            raise ConfigError(f"unknown gate: {args.gate}")

        defaults = load_defaults(DEFAULTS)
        reviewer = args.reviewer or defaults["default"]["reviewer"]
        reviewers = defaults["reviewers"]
        if reviewer != defaults["default"]["reviewer"] and reviewer not in reviewers:
            raise ConfigError(f"reviewer is not configured: {reviewer}")
        if reviewer not in OVERRIDE_PATHS:
            raise ConfigError(f"project override path is not configured for reviewer: {reviewer}")

        selected = merged_bundled_gate(defaults, reviewer, args.gate)
        sources = ["default"]
        if reviewer in reviewers:
            sources.append(f"reviewers.{reviewer}")
        override_path = project_root / OVERRIDE_PATHS[reviewer]
        if override_path.exists() or override_path.is_symlink():
            resolved_override = override_path.resolve(strict=True)
            if not resolved_override.is_relative_to(project_root):
                raise ConfigError(f"project override leaves the project root: {override_path}")
            if not resolved_override.is_file():
                raise ConfigError(f"project override is not a file: {override_path}")
            override = load_override(override_path)
            selected.update(override.get(args.gate, {}))
            sources.append(OVERRIDE_PATHS[reviewer].as_posix())

        result = {
            "reviewer": reviewer,
            "gate": args.gate,
            "model": selected["model"],
            "effort": selected["effort"],
            "sources": sources,
        }
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ConfigError, OSError) as error:
        print(f"review config error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
