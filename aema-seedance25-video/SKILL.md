---
name: aema-seedance25-video
description: Turn approved scenes and locked references into 9:16 Seedance 2.5 shot prompts and versioned generation plans, then submit only explicitly approved batches. Do not use for reference-image design or final editing.
---

# AEMA Seedance 2.5 Video

Design coherent, producible Seedance 2.5 clips for an AI short drama. Prompt preparation is local; video submission is a separate, potentially billable phase.

## Required inputs

- approved scene text or scene IDs;
- target duration and delivery framing, defaulting to 9:16 for this workflow;
- locked character, location, and prop versions;
- selected local references and/or remote Element IDs;
- any dialogue, ambient sound, or music requirements;
- an AEMA `archive_context` when called by the pipeline.

If a required recurring reference is missing, mark the affected shot `blocked` or explicitly describe the continuity risk. Do not invent an Element ID or claim a reference is locked.

## Plan the shots

1. Break each scene into the smallest useful set of clips. Keep one dominant visual intention per clip while preserving the dramatic beat.
2. Give each shot a stable ID such as `E01-S001-C001` and each attempt a take ID such as `...-T001`.
3. Write a time-ordered prompt with framing, camera behavior, subject action, expression, environment motion, dialogue/audio, and end state. Bind recurring entities by exact asset version or Element ID.
4. Check portrait composition, screen direction, eyelines, prop hands, costume state, entry/exit state, and neighboring-shot continuity.
5. Create a provider-neutral plan first. At execution time, discover the connected provider's current model ID, input limits, duration, resolution, audio, reference, price, and policy capabilities. Never silently switch models.
6. Read [references/seedance-plan.md](references/seedance-plan.md) for the manifest and prompt contract. Validate a plan with `scripts/validate_generation_plan.py`.
7. Follow [the canonical archive contract](../aema-drama-pipeline/references/archive-contract.md) and write only within the supplied stage directory.

## Dry-run and execution gate

Default to dry-run. It may create local shot lists, prompts, estimates, and manifests, but it must not submit jobs or consume credits.

Before execution, show the exact `run_id` and `plan_hash`, shot/take IDs, provider/model, duration, resolution, reference inputs, native-audio choice, number of jobs, current cost estimate or `unknown`, output paths, remote actions, and maximum attempts. Submit only when the user approves that reviewed scope. A changed provider, model, count, duration, resolution, reference set, or cost ceiling requires a new plan and approval.

Submit each approved job once. Persist the request ID immediately. For ambiguous timeouts, query by that ID before any new submission; do not automatically repeat a paid POST. Poll asynchronous status with bounded backoff, then archive successful media and response metadata promptly. Never claim success based only on submission.

No paid retake is automatic. Preserve every take, identify the reason for a proposed retake, and wait for an explicit retry budget.

## Output states

Use truthful states: `planned`, `approved`, `submitted`, `running`, `generated`, `selected`, `archived`, `failed`, or `blocked`. A selected take is never overwritten. Return a manifest fragment to the pipeline; do not edit its global manifest.
