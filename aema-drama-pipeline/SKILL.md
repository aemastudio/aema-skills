---
name: aema-drama-pipeline
description: Orchestrate a multi-stage AEMA AI short-drama project across the sibling aema skills, with resumable archive state and approval gates. Use for end-to-end production, not a standalone single-stage request.
---

# AEMA Drama Pipeline

Coordinate the suite without copying the leaf skills' writing, prompting, generation, Blender, or transcription logic. This skill owns project state, routing, approvals, checkpoints, and handoffs.

## Load the contracts

Always read:

- [references/archive-contract.md](references/archive-contract.md) for the one canonical project layout and manifest rules;
- [references/orchestration.md](references/orchestration.md) for stage prerequisites, call order, invalidation, and resume behavior.

Use `scripts/init_project.py` to preview or initialize a new archive. A project archive is a local deliverable, not permission to call external services.

## Orchestration graph

```text
aema-scriptwriter
        |
        v
aema-asset-builder ----------------------+
        |                                 |
        +--> aema-blender (when useful) --+
        |          |                      |
        |          +-- approved render ---+--> aema-asset-builder/register-existing
        v
aema-seedance25-video
        |
        v
aema-korean-srt (after actual audio/video exists)
```

Leaf skills do not call one another. This pipeline invokes one leaf at a time with a scoped `archive_context`, receives a manifest fragment, verifies it, and alone updates `aema-project.json`.

## Run behavior

1. Resolve the user's requested start and stop stages. Reuse already approved inputs instead of regenerating them.
2. Create a `run_id`, snapshot input paths and hashes, and provide each leaf only the inputs and stage directory it needs.
3. Require truthful stage results: `planned`, `review`, `approved`, `running`, `complete`, `failed`, `blocked`, or `stale`. Never infer completion from a prompt, submission, or missing tool output.
4. Pause downstream work when a prerequisite is missing. A dry-run may still prepare a clearly marked provisional later-stage plan, but it may not claim validated references, media, or subtitles.
5. Assess Blender for shots that benefit from controlled 3D geometry, camera, lighting, simulation, or repeatable renders. Do not force Blender into every production.
6. Merge only validated manifest fragments, write updates atomically, and append a run-ledger event. Preserve old versions.
7. On script or reference changes, compare hashes and mark only affected downstream artifacts `stale`; never delete them.
8. Summarize completed work, blocked stages, cost-bearing actions awaiting approval, and the exact next action.

## External and heavy-work gates

Analysis, local plans, prompts, and archive metadata are allowed in dry-run. Image/video generation, uploads, Elements registration, or any billable provider call require explicit approval bound to the reviewed `run_id`, `plan_hash`, exact item scope, provider/model, current estimate, and retry limit.

Treat registration/upload as a separately visible mutation. If the available Higgsfield tools can use existing Elements but cannot create one, prepare a manual registration manifest and mark the stage blocked; never fabricate a remote ID.

For Blender, prepare and validate the scene plan first. Run a low-cost preview only when requested; require confirmation before a long or full-resolution render. Do not install add-ons or execute untrusted embedded scripts automatically.

Do not retry a paid submission automatically. When provider state is ambiguous, query the stored request ID. Any scope or cost increase creates a new plan and approval checkpoint.

## Boundary

This skill may create an export or assembly manifest, but it does not invent missing footage, burn captions, or duplicate a video editor. Use a separate available editing capability only when the user requests an assembled deliverable. Never modify unrelated skills or configuration.
