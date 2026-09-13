#!/usr/bin/env python3
"""Preview or initialize a versioned AEMA project archive."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import sys
from pathlib import Path


DIRECTORIES = [
    "01_script/brief", "01_script/treatments", "01_script/episodes", "01_script/canon",
    "02_references/characters", "02_references/locations", "02_references/props", "02_references/registries",
    "03_prompts/image", "03_prompts/video", "03_prompts/blender",
    "04_elements/registration-plans", "04_elements/records",
    "05_video/cuts", "05_video/selected", "05_video/qc",
    "06_blender/plans", "06_blender/scenes", "06_blender/scripts", "06_blender/previews", "06_blender/renders",
    "07_audio/source", "07_audio/extracted",
    "08_subtitles/transcripts", "08_subtitles/srt", "08_subtitles/qc",
    "09_exports", "runs",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="New project archive root")
    parser.add_argument("--title", required=True)
    parser.add_argument("--project-id", help="Optional explicit AEMA project ID")
    parser.add_argument("--language", default="ko")
    parser.add_argument("--aspect-ratio", default="9:16")
    parser.add_argument("--execute", action="store_true", help="Create directories and manifest; default is dry-run")
    parser.add_argument("--allow-existing", action="store_true", help="Allow an existing non-empty root without an AEMA manifest")
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:32] or f"project-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:8]}"


def safe_root(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    home = Path.home().resolve()
    if resolved == Path(resolved.anchor) or resolved == home:
        raise ValueError("refusing to initialize a filesystem root or home directory")
    return resolved


def main() -> int:
    args = parse_args()
    try:
        root = safe_root(args.root)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    manifest_path = root / "aema-project.json"
    if manifest_path.exists():
        print(f"ERROR: project already initialized: {manifest_path}", file=sys.stderr)
        return 1
    if root.exists() and any(root.iterdir()) and not args.allow_existing:
        print("ERROR: root is non-empty; inspect it and pass --allow-existing only if it is the intended project", file=sys.stderr)
        return 1

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    date = now.strftime("%Y%m%d")
    project_id = args.project_id or f"AEMA-{date}-{slugify(args.title)}"
    run_id = f"RUN-{now.strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(3)}"
    manifest = {
        "schema_version": "aema.archive/v1",
        "project_id": project_id,
        "title": args.title,
        "created_at": now.isoformat().replace("+00:00", "Z"),
        "updated_at": now.isoformat().replace("+00:00", "Z"),
        "aspect_ratio": args.aspect_ratio,
        "language": args.language,
        "stages": {},
        "current_run_id": run_id,
    }
    preview = {
        "mode": "execute" if args.execute else "dry-run",
        "root": str(root),
        "project_id": project_id,
        "run_id": run_id,
        "manifest": str(manifest_path),
        "directories": DIRECTORIES,
    }
    if not args.execute:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    root.mkdir(parents=True, exist_ok=True)
    for relative in DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)
    run_root = root / "runs" / run_id
    (run_root / "stages").mkdir(parents=True, exist_ok=True)
    temp_path = manifest_path.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp_path, manifest_path)
    ledger = run_root / "ledger.jsonl"
    event = {"at": manifest["created_at"], "event": "project-initialized", "project_id": project_id, "run_id": run_id}
    ledger.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(preview, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
