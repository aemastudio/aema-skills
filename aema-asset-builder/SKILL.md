---
name: aema-asset-builder
description: Cast recurring characters, then turn an approved script into consistent character, environment, and prop reference packages with controlled image generation and Higgsfield Elements registration. Do not use for video-shot generation.
---

# AEMA Asset Builder

Build the locked visual references that downstream shots reuse. Begin with a dry run. Script analysis or prompt writing never implies permission to spend credits, upload files, or register remote Elements.

## Modes

- `cast-plan`: prepare one `16:9` casting board with four full-body candidates `1–4` for each new recurring character.
- `cast-generate`: generate only the approved four-candidate casting board from a reviewed plan.
- `cast-select`: lock the user's chosen candidate number before character reference production.
- `cast-review`: assemble already selected recurring-character references into one self-contained HTML ensemble board for final cast review. This mode does not generate or alter images.
- `analyze`: extract and normalize visual entities from an approved script.
- `plan`: create reference briefs, prompts, contact-sheet requirements, and a versioned generation plan.
- `generate`: generate only the exact image items authorized from a reviewed plan.
- `register-existing`: register selected, already-created artifacts as Higgsfield Elements.
- `generate-and-register`: execute both approved scopes, recording each as a separate remote action.

If the requested mode is unclear, stop after `plan`.

## Casting gate for new characters

For every new recurring character without an already locked identity, casting is the first visual step. Read [references/casting-board.md](references/casting-board.md) and follow this sequence:

1. Analyze the approved character brief without locking appearance details that the user has not chosen.
2. Plan one `16:9` landscape contact sheet containing exactly four clearly separated candidates labeled `1`, `2`, `3`, `4`.
3. Show all four candidates as uncropped, front-facing, head-to-toe full-body photographs under comparable studio conditions. Each candidate must have a genuinely different face while all four satisfy the same canon description.
4. Vary face, build, height impression, proportions, posture, hairstyle, and role-compatible styling enough to support a real casting decision. Keep age range, presentation, ethnicity where specified, role, genre, and realism consistent.
5. Generate the single board only after approval of its dry-run plan. Present it with the canon character description and stop for a user selection such as `3번`.
6. Record the selected candidate. Only then create the character's unified reference package. The first locked deliverable is the mandatory `16:9` three-panel master sheet in [references/character-reference-sheet.md](references/character-reference-sheet.md). Do not blend candidates or silently change the selection.

Do not continue to final character sheets, Elements registration, or video references while casting is unselected. If the user supplies an existing locked face and body reference or explicitly asks to retain a known character, record that provenance and skip candidate generation rather than recasting them.

## Final ensemble cast review

When the user asks to review all final characters together, use `cast-review`; do not return to candidate generation. Read the **Final ensemble HTML board** section in [references/character-reference-sheet.md](references/character-reference-sheet.md), prepare its manifest from the current canon and selected reference records, and run `scripts/build_final_cast_review.py`. Use only the existing selected images. Never invoke image generation merely to fill this board.

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
