#!/usr/bin/env python3
"""Validate the structural invariants of an AEMA asset registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PREFIXES = {"characters": "CHAR-", "locations": "LOC-", "props": "PROP-"}
VALID_STATUS = {"draft", "review", "locked", "retired"}
VALID_CASTING_STATUS = {"planned", "generated", "selected", "locked"}


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
            if group == "characters" and "casting" in entry:
                casting = entry["casting"]
                if not isinstance(casting, dict):
                    errors.append(f"{where}.casting must be an object")
                    continue
                if casting.get("status") not in VALID_CASTING_STATUS:
                    errors.append(f"{where}.casting.status must be one of {sorted(VALID_CASTING_STATUS)}")
                selected_face = casting.get("selected_face")
                selected_body = casting.get("selected_body")
                if selected_face is not None and selected_face not in {"1", "2", "3", "4", "5"}:
                    errors.append(f"{where}.casting.selected_face must be 1-5")
                if selected_body is not None and selected_body not in {"A", "B", "C", "D", "E"}:
                    errors.append(f"{where}.casting.selected_body must be A-E")
                combined = casting.get("selection")
                if selected_face is not None and selected_body is not None and combined != f"{selected_face}+{selected_body}":
                    errors.append(f"{where}.casting.selection must match selected_face+selected_body")
                if casting.get("status") in {"selected", "locked"} and (selected_face is None or selected_body is None):
                    errors.append(f"{where}.casting requires both selections when selected or locked")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.registry} contains {len(seen)} unique assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
