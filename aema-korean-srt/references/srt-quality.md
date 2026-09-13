# Korean SRT Quality Guide

Read this after transcription and before marking a subtitle package complete.

## Required format

- Save UTF-8 text with sequential cue numbers beginning at 1.
- Use `HH:MM:SS,mmm --> HH:MM:SS,mmm` timestamps.
- Every cue has positive duration, non-empty text, and a start time at or after the prior cue's start.
- Remove accidental overlaps unless the overlap represents genuinely simultaneous speech and the delivery system supports it.
- Keep cues inside the known media duration.

## Readability

- Split at phrase or sentence boundaries where possible; avoid separating a particle from its noun or an ending from its verb.
- Prefer one or two visually balanced lines. Treat character limits as configurable because font, safe area, platform, and speaking rate differ.
- Give short reactions enough screen time to read without stretching them far beyond the utterance.
- Preserve pauses that carry meaning. Merge fragments only when doing so improves reading without hiding a dramatic beat.
- Keep Korean, English names, numbers, honorifics, and intentional slang faithful to the audio.

## QC record

Record cue count, first/last timestamp, overlaps found/fixed, empty cues, unusually short/long cues, lines exceeding the chosen display limit, uncertain words, music/noise-only regions, and whether a human review occurred.

Whisper output is evidence, not ground truth. When a word is uncertain, flag it with timing in the QC report instead of confidently rewriting the dialogue.
