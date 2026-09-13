---
name: aema-korean-srt
description: Create and quality-check timed Korean SRT subtitles from video or audio, preferring an already-installed local Whisper model. Do not use for general translation, caption burn-in, or video editing.
---

# AEMA Korean SRT

Produce a truthful UTF-8 Korean subtitle package while preserving the source media. Prefer local transcription and never fall back to a network or paid service without a separate, explicit plan and approval.

## Workflow

1. Resolve the source media, intended language, output path, and whether the user wants verbatim speech or light readability editing.
2. Inspect local capabilities. Prefer `faster-whisper`, then `openai-whisper`, only when the package, media decoder, and model files are already present locally.
3. Run `scripts/transcribe_korean.py` without `--execute` to preview the operation and verify the offline prerequisites. The helper refuses to download a model.
4. Execute locally only when a real media input and local model path are available. If not, return `blocked` with the missing prerequisite; do not create placeholder SRT text.
5. Apply minimal Korean spacing and punctuation cleanup without changing meaning, speaker intent, proper nouns, or code-switching. Do not invent unheard dialogue.
6. Read [references/srt-quality.md](references/srt-quality.md), then validate numbering, timestamps, non-empty cues, overlaps, media bounds where available, and readability.
7. Save the SRT, machine-readable transcript metadata, and QC report. Follow [the canonical archive contract](../aema-drama-pipeline/references/archive-contract.md) when an AEMA context is supplied.

## Output contract

Record source path and hash, detected duration, backend, local model identifier/path, language, transcription options, generated paths, warnings, and `status`. Do not store private credentials.

Use `planned`, `running`, `complete`, `failed`, or `blocked` only when supported by evidence. A transcript plan is not a completed SRT. Return a manifest fragment to the pipeline and do not edit its global manifest.

## Boundaries

- Preserve the source media and do not overwrite an existing SRT unless the user explicitly requests replacement; versioning is preferred.
- Do not identify speakers unless diarization evidence exists. Labels such as `화자 1` are not identity claims.
- Do not translate other languages into Korean unless the user separately asks for translation.
- Burning captions into pixels belongs to a video-editing workflow, not this skill.
- If a remote fallback is requested, create a dry-run plan with provider, media scope, privacy implications, estimate, output, and retry ceiling, then wait for approval.
