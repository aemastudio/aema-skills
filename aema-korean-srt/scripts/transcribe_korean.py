#!/usr/bin/env python3
"""Preview or run offline Korean transcription with a local Whisper model."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Local video or audio file")
    parser.add_argument("--output", required=True, type=Path, help="Destination .srt path")
    parser.add_argument("--backend", choices=("auto", "faster-whisper", "openai-whisper"), default="auto")
    parser.add_argument("--model-path", type=Path, help="Existing local model directory or checkpoint; required for execution")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--initial-prompt")
    parser.add_argument("--execute", action="store_true", help="Run transcription; default is dry-run")
    parser.add_argument("--force", action="store_true", help="Replace existing output files")
    return parser.parse_args()


def available_backends() -> dict[str, bool]:
    return {
        "faster-whisper": importlib.util.find_spec("faster_whisper") is not None,
        "openai-whisper": importlib.util.find_spec("whisper") is not None,
    }


def select_backend(requested: str, available: dict[str, bool]) -> str | None:
    if requested != "auto":
        return requested if available.get(requested) else None
    for name in ("faster-whisper", "openai-whisper"):
        if available[name]:
            return name
    return None


def srt_timestamp(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def normalize_segments(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    last_end = 0.0
    for item in raw:
        text = " ".join(str(item.get("text", "")).strip().split())
        start = max(0.0, float(item.get("start", 0.0)))
        end = max(start + 0.001, float(item.get("end", start)))
        if not text:
            continue
        if start < last_end:
            start = last_end
            end = max(end, start + 0.001)
        cues.append({"index": len(cues) + 1, "start": start, "end": end, "text": text})
        last_end = end
    return cues


def transcribe_faster(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    from faster_whisper import WhisperModel  # type: ignore

    model = WhisperModel(str(args.model_path), device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(
        str(args.input), language="ko", task="transcribe", vad_filter=True,
        initial_prompt=args.initial_prompt,
    )
    raw = [{"start": part.start, "end": part.end, "text": part.text} for part in segments]
    metadata = {"language": getattr(info, "language", "ko"), "duration": getattr(info, "duration", None)}
    return raw, metadata


def transcribe_openai(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    import whisper  # type: ignore

    model = whisper.load_model(str(args.model_path), device=None if args.device == "auto" else args.device)
    result = model.transcribe(
        str(args.input), language="ko", task="transcribe", verbose=False,
        initial_prompt=args.initial_prompt,
    )
    raw = [{"start": part["start"], "end": part["end"], "text": part["text"]} for part in result.get("segments", [])]
    metadata = {"language": result.get("language", "ko"), "duration": raw[-1]["end"] if raw else 0.0}
    return raw, metadata


def atomic_write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(content, encoding="utf-8")
    os.replace(temp, path)


def main() -> int:
    args = parse_args()
    available = available_backends()
    backend = select_backend(args.backend, available)
    companions = {
        "transcript": args.output.with_suffix(".transcript.json"),
        "qc": args.output.with_suffix(".qc.json"),
    }
    preview = {
        "mode": "execute" if args.execute else "dry-run",
        "input": str(args.input.resolve()),
        "output": str(args.output.resolve()),
        "backend_requested": args.backend,
        "backend_selected": backend,
        "available_backends": available,
        "ffmpeg": shutil.which("ffmpeg"),
        "model_path": str(args.model_path.resolve()) if args.model_path else None,
        "network_fallback": False,
        "companion_outputs": {key: str(value.resolve()) for key, value in companions.items()},
    }
    if not args.execute:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    if not args.input.is_file():
        print(f"ERROR: input media does not exist: {args.input}", file=sys.stderr)
        return 2
    if args.output.suffix.lower() != ".srt":
        print("ERROR: --output must end in .srt", file=sys.stderr)
        return 2
    if backend is None:
        print("ERROR: no requested local Whisper backend is installed", file=sys.stderr)
        return 3
    if args.model_path is None or not args.model_path.exists():
        print("ERROR: --model-path must point to an existing local model; downloads are not automatic", file=sys.stderr)
        return 3
    if not args.force and any(path.exists() for path in (args.output, *companions.values())):
        print("ERROR: one or more output files already exist; use a new version or --force", file=sys.stderr)
        return 1

    try:
        raw, engine_metadata = (transcribe_faster(args) if backend == "faster-whisper" else transcribe_openai(args))
        cues = normalize_segments(raw)
        if not cues:
            raise RuntimeError("transcription returned no spoken cues")
        srt = "\n\n".join(
            f"{cue['index']}\n{srt_timestamp(cue['start'])} --> {srt_timestamp(cue['end'])}\n{cue['text']}"
            for cue in cues
        ) + "\n"
        transcript = {"schema_version": "aema.transcript/v1", "backend": backend, "language": "ko", "engine": engine_metadata, "cues": cues}
        qc = {
            "schema_version": "aema.subtitle-qc/v1",
            "status": "complete",
            "cue_count": len(cues),
            "first_start": cues[0]["start"],
            "last_end": cues[-1]["end"],
            "empty_cues": 0,
            "overlaps": 0,
            "human_reviewed": False,
        }
        atomic_write(args.output, srt, args.force)
        atomic_write(companions["transcript"], json.dumps(transcript, ensure_ascii=False, indent=2) + "\n", args.force)
        atomic_write(companions["qc"], json.dumps(qc, ensure_ascii=False, indent=2) + "\n", args.force)
    except Exception as exc:
        print(f"ERROR: transcription failed: {exc}", file=sys.stderr)
        return 4

    print(json.dumps({**preview, "status": "complete", "cue_count": len(cues)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
