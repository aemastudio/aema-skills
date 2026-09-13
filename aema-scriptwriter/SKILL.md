---
name: aema-scriptwriter
description: Develop ideas, synopses, episode structures, scenarios, and dialogue scripts for AI short dramas. Use for story and screenplay work, not visual-asset or video generation.
---

# AEMA Scriptwriter

Turn a premise or partial draft into the requested level of production-ready writing. Match the user's language; when the request is in Korean, write natural Korean unless asked otherwise.

## Choose the deliverable

- For a raw idea, develop only as far as the user requests: premise, synopsis, treatment, episode map, scene outline, or full script.
- For revisions, preserve locked canon and stable IDs. Surface any requested change that conflicts with earlier facts before propagating it.
- For an AI short-drama production script, read [references/vertical-short-drama.md](references/vertical-short-drama.md).
- When invoked by `aema-drama-pipeline`, accept its `archive_context` and return a manifest fragment. Do not edit the global project manifest.

## Workflow

1. Establish or reasonably infer format, total duration, episode count, audience, genre, tone, platform, and content boundaries. State consequential assumptions rather than blocking on minor gaps.
2. Create a compact canon ledger before long-form writing. Give recurring entities stable IDs: `CHAR-*`, `LOC-*`, and `PROP-*`.
3. Develop the requested story layer. Keep cause and effect, character goals, reversals, setup/payoff, and episode hooks traceable.
4. For scripts, assign stable scene IDs such as `E01-S001`. Include location/time, participating entity IDs, visible action, dialogue, sound, continuity, and production notes.
5. Run a continuity and producibility pass. Check names, ages, relationships, costume/prop state, spatial logic, time, dialogue duration, and whether a 9:16 frame can communicate the beat.
6. If an AEMA archive is in use, follow [the canonical archive contract](../aema-drama-pipeline/references/archive-contract.md) and write only within the supplied stage directory.

## Handoff contract

Return the writing plus:

- locked and unresolved canon items;
- entity registry with stable IDs and aliases;
- scene index with estimated duration and required entities;
- intentional continuity changes, separated from errors;
- asset hints, without writing image prompts;
- `status` as `draft`, `review`, `approved`, or `blocked`.

Do not generate images or videos, register remote Elements, invent provider job IDs, or claim downstream production is complete. Approval of a script does not authorize media generation.
