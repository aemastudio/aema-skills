---
name: aema-asset-builder
description: Cast recurring characters, then turn an approved script into consistent character, environment, and prop reference packages with controlled image generation and Higgsfield Elements registration. Do not use for video-shot generation.
---

# AEMA Asset Builder

Build the locked visual references that downstream shots reuse. Begin with a dry run. Script analysis or prompt writing never implies permission to spend credits, upload files, or register remote Elements.

## Modes

- `cast-plan`: prepare face board `1–5` and full-body board `A–E` for each new recurring character.
- `cast-generate`: generate only the two approved casting boards from a reviewed plan.
- `cast-select`: lock the user's chosen face/body pair, such as `1+E`, before character reference production.
- `analyze`: extract and normalize visual entities from an approved script.
- `plan`: create reference briefs, prompts, contact-sheet requirements, and a versioned generation plan.
- `generate`: generate only the exact image items authorized from a reviewed plan.
- `register-existing`: register selected, already-created artifacts as Higgsfield Elements.
- `generate-and-register`: execute both approved scopes, recording each as a separate remote action.

If the requested mode is unclear, stop after `plan`.

## Casting gate for new characters

For every new recurring character without an already locked identity, casting is the first visual step. Read [references/casting-board.md](references/casting-board.md) and follow this sequence:

1. Analyze the approved character brief without locking appearance details that the user has not chosen.
2. Plan one face contact sheet containing exactly five clearly separated candidates labeled `1`, `2`, `3`, `4`, `5`.
3. Plan one full-body contact sheet containing exactly five clearly separated body/silhouette candidates labeled `A`, `B`, `C`, `D`, `E`.
4. Keep age range, presentation, ethnicity where specified, role, genre, and overall styling compatible across both boards. Vary facial identity only on the face board; vary body build, height impression, proportions, and silhouette only on the body board.
5. Generate the two boards only after approval of their dry-run plan. Present both boards together and stop for a user selection such as `1+E`.
6. Record the selected pair. Only then create the character's unified reference package using the chosen face and chosen body. The first locked deliverable is the mandatory `16:9` three-panel master sheet in [references/character-reference-sheet.md](references/character-reference-sheet.md). Do not average candidates or silently change either selection.

Do not continue to final character sheets, Elements registration, or video references while casting is unselected. If the user supplies an existing locked face and body reference or explicitly asks to retain a known character, record that provenance and skip candidate generation rather than recasting them.

## Reference workflow

1. Resolve duplicate names and aliases. Preserve script IDs; never merge ambiguous entities silently.
2. Separate immutable identity anchors from wardrobe, expression, damage, weather, and other scene variants.
3. For recurring characters, consume the locked casting pair before building the reference lock. Generate the three-panel master sheet first; derive any additional expression/pose coverage only after that sheet is selected. Include scale, color/material notes, and negative constraints only where they prevent known drift.
4. Keep prompts provider-neutral at the canonical layer. Put provider-specific payloads in the reviewed run plan.
5. Read [references/asset-registry.md](references/asset-registry.md) when creating or validating a registry. Use `scripts/validate_asset_registry.py` for a deterministic structural check.
6. Follow [the canonical archive contract](../aema-drama-pipeline/references/archive-contract.md) whenever an AEMA project context is supplied.

## Environment adapters

Choose an adapter only after checking the tools actually available.

### Codex

Use the available native image-generation capability for approved image items. Save a durable local artifact and generation metadata before considering it archived. Use an available Higgsfield connector or MCP only for a separately approved upload/Elements registration step.

### Claude

Use the configured Higgsfield MCP for approved image generation and Elements registration. Save or export the result into the local archive, then verify the artifact and returned remote ID. If the MCP cannot provide a durable artifact, mark archiving as blocked rather than claiming success.

Before either adapter registers an Element, inspect the live tool capabilities. The ability to use an existing Element does not prove that programmatic Element creation is available. If create/register is absent, write a manual registration manifest and mark remote registration `blocked` until a person completes and verifies it.

Do not silently substitute another provider when a required adapter is unavailable. Produce a handoff-ready manifest instead.

## External-action gate

The dry-run plan must name its `run_id` and `plan_hash` and list exact asset IDs, versions, provider/model, image count, dimensions/aspect ratio, estimated cost or `unknown`, destination, planned uploads/registrations, and retry limit.

Execute only after the user approves that exact plan and scope. Re-plan and re-authorize if the provider, model, count, resolution, selected references, cost ceiling, or remote mutations change. Never make an automatic paid retry. For an ambiguous timeout, query the stored job or idempotency key before proposing a retry.

## Completion

Record truthful per-item states: `planned`, `generated`, `selected`, `registered`, `archived`, `failed`, or `blocked`. Store provider job IDs and Element IDs but never credentials. Preserve all earlier versions and never overwrite a selected reference.
