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
                selected_candidate = casting.get("selected_candidate")
                selected_face = casting.get("selected_face")
                selected_body = casting.get("selected_body")
                has_legacy_selection = selected_face is not None or selected_body is not None
                if selected_candidate is not None and selected_candidate not in {"1", "2", "3", "4"}:
                    errors.append(f"{where}.casting.selected_candidate must be 1-4")
                if selected_candidate is not None and has_legacy_selection:
                    errors.append(f"{where}.casting must not mix selected_candidate with legacy face/body fields")
                if has_legacy_selection:
                    if selected_face not in {"1", "2", "3", "4", "5"}:
                        errors.append(f"{where}.casting.selected_face must be 1-5 for a legacy record")
                    if selected_body not in {"A", "B", "C", "D", "E"}:
                        errors.append(f"{where}.casting.selected_body must be A-E for a legacy record")
                    combined = casting.get("selection")
                    if combined != f"{selected_face}+{selected_body}":
                        errors.append(f"{where}.casting.selection must match legacy selected_face+selected_body")
                if casting.get("status") in {"selected", "locked"} and selected_candidate is None and not has_legacy_selection:
                    errors.append(f"{where}.casting requires selected_candidate when selected or locked")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.registry} contains {len(seen)} unique assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
