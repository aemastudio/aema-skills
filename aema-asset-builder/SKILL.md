---
name: aema-asset-builder
description: Analyze an approved script into consistent character, environment, and prop reference packages, then prepare or execute controlled image generation and Higgsfield Elements registration. Do not use for video-shot generation.
---

# AEMA Asset Builder

Build the locked visual references that downstream shots reuse. Begin with a dry run. Script analysis or prompt writing never implies permission to spend credits, upload files, or register remote Elements.

## Modes

- `analyze`: extract and normalize visual entities from an approved script.
- `plan`: create reference briefs, prompts, contact-sheet requirements, and a versioned generation plan.
- `generate`: generate only the exact image items authorized from a reviewed plan.
- `register-existing`: register selected, already-created artifacts as Higgsfield Elements.
- `generate-and-register`: execute both approved scopes, recording each as a separate remote action.

If the requested mode is unclear, stop after `plan`.

## Reference workflow

1. Resolve duplicate names and aliases. Preserve script IDs; never merge ambiguous entities silently.
2. Separate immutable identity anchors from wardrobe, expression, damage, weather, and other scene variants.
3. Build a reference lock before video generation. Include portrait-safe full body, neutral identity view, expression/pose coverage, scale, color/material notes, and negative constraints only where they prevent known drift.
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
