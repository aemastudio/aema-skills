#!/usr/bin/env python3
"""Validate the structural invariants of an AEMA asset registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PREFIXES = {"characters": "CHAR-", "locations": "LOC-", "props": "PROP-"}
VALID_STATUS = {"draft", "review", "locked", "retired"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path, help="Path to asset-registry JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.registry.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    if data.get("schema_version") != "aema.assets/v1":
        errors.append("schema_version must be 'aema.assets/v1'")
    for key in ("project_id", "registry_version", "source_script"):
        if not data.get(key):
            errors.append(f"missing non-empty top-level field: {key}")

    seen: set[str] = set()
    for group, prefix in PREFIXES.items():
        entries = data.get(group)
        if not isinstance(entries, list):
            errors.append(f"{group} must be an array")
            continue
        for index, entry in enumerate(entries):
            where = f"{group}[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{where} must be an object")
                continue
            asset_id = entry.get("id", "")
            if not isinstance(asset_id, str) or not asset_id.startswith(prefix):
                errors.append(f"{where}.id must start with {prefix}")
            elif asset_id in seen:
                errors.append(f"duplicate asset id: {asset_id}")
            else:
                seen.add(asset_id)
            version = entry.get("version", "")
            if not isinstance(version, str) or len(version) != 4 or not version.startswith("v") or not version[1:].isdigit():
                errors.append(f"{where}.version must match vNNN")
            if entry.get("status") not in VALID_STATUS:
                errors.append(f"{where}.status must be one of {sorted(VALID_STATUS)}")
            for field in ("name", "source_scenes", "identity_anchors", "allowed_variants", "reference_artifacts", "provenance"):
                if field not in entry:
                    errors.append(f"{where} missing field: {field}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.registry} contains {len(seen)} unique assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
