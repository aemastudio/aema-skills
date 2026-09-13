#!/usr/bin/env python3
"""Validate an AEMA Seedance generation plan and its canonical plan hash."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path


VALID_STATUS = {"planned", "approved", "submitted", "running", "generated", "selected", "archived", "failed", "blocked"}


def canonical_hash(data: dict) -> str:
    payload = copy.deepcopy(data)
    payload.pop("plan_hash", None)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to generation-plan JSON")
    parser.add_argument("--print-hash", action="store_true", help="Print the canonical hash even when validation fails")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("ERROR: plan root must be an object", file=sys.stderr)
        return 1

    computed = canonical_hash(data)
    errors: list[str] = []
    if data.get("schema_version") != "aema.video-plan/v1":
        errors.append("schema_version must be 'aema.video-plan/v1'")
    for key in ("run_id", "mode", "provider", "model", "cost_estimate", "external_actions", "authorization"):
        if key not in data:
            errors.append(f"missing top-level field: {key}")
    if data.get("aspect_ratio") != "9:16":
        errors.append("aspect_ratio must be '9:16' for this workflow")
    if data.get("plan_hash") != computed:
        errors.append(f"plan_hash mismatch; expected {computed}")
    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        errors.append("shots must be a non-empty array")
        shots = []

    seen_shots: set[str] = set()
    seen_takes: set[str] = set()
    for index, shot in enumerate(shots):
        where = f"shots[{index}]"
        if not isinstance(shot, dict):
            errors.append(f"{where} must be an object")
            continue
        for field in ("shot_id", "take_id", "duration_seconds", "asset_refs", "prompt", "output_path", "status"):
            if field not in shot:
                errors.append(f"{where} missing field: {field}")
        shot_id = shot.get("shot_id")
        take_id = shot.get("take_id")
        if shot_id in seen_shots:
            errors.append(f"duplicate shot_id: {shot_id}")
        elif isinstance(shot_id, str):
            seen_shots.add(shot_id)
        if take_id in seen_takes:
            errors.append(f"duplicate take_id: {take_id}")
        elif isinstance(take_id, str):
            seen_takes.add(take_id)
        duration = shot.get("duration_seconds")
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"{where}.duration_seconds must be positive")
        if not isinstance(shot.get("asset_refs"), list):
            errors.append(f"{where}.asset_refs must be an array")
        if shot.get("status") not in VALID_STATUS:
            errors.append(f"{where}.status must be one of {sorted(VALID_STATUS)}")

    if args.print_hash:
        print(computed)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {len(shots)} shots, plan_hash={computed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
