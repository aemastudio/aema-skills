---
name: aema-blender
description: Plan and automate Blender scene layout, portrait cameras, lighting, objects, materials, animation, previews, and renders for AI short-drama production. Do not use for ordinary 2D image or video prompting.
---

# AEMA Blender

Create reproducible Blender plans and automation while preserving existing scenes and linked assets. Default to a validated scene plan; separate low-cost preview rendering from full rendering.

## Modes

- `plan`: scene breakdown, asset dependencies, scale, camera, lighting, materials, animation, render settings, and output paths.
- `script`: create or adapt a `bpy` automation script from the approved plan.
- `preview`: execute an approved local plan at reduced resolution or samples.
- `render`: execute the approved final scene/render scope.
- `register-reference-handoff`: return an approved Blender still to the pipeline; the pipeline may call `aema-asset-builder` in `register-existing` mode.

If the mode or execution scope is unclear, stop after `plan` or `script`.

## Workflow

1. Consume approved scene IDs and asset versions. Preserve AEMA IDs in Blender collection, object, material, camera, and output metadata.
2. Define units, origin, world axes, blocking, object ownership, camera target, frame range, fps, color management, render engine, resolution, samples, and required add-ons before execution.
3. Default production framing to 9:16. Use a lower-resolution exact-ratio preview rather than changing composition.
4. Distinguish real linked assets from placeholders. Never claim a stand-in is a finished asset.
5. Read [references/blender-plan.md](references/blender-plan.md) for the portable JSON contract. `scripts/aema_blender_scene.py` validates a plan outside Blender and can build a safe basic scene inside Blender.
6. For complex modeling, rigs, geometry nodes, simulation, compositing, or imports, generate a project-specific script in the archive instead of stretching the basic helper beyond its contract.
7. Follow [the canonical archive contract](../aema-drama-pipeline/references/archive-contract.md). Use relative asset paths in saved project metadata and version output `.blend` files and renders.

## Execution safety

The basic helper defaults to dry-run, refuses to overwrite its `.blend` output without `--force`, and manages only its own `AEMA_<scene-id>_ROOT` collection. Do not clear the user's scene, delete unrelated datablocks, install add-ons, download assets, or execute untrusted embedded scripts.

Before a preview or render, verify Blender version, required add-ons, linked files, fonts, textures, output path, frame range, device, samples, estimated frames, and missing dependencies. If a required dependency is unavailable, preserve the runnable plan/script and report `blocked`.

Preview execution requires an explicit request. Full-resolution or long rendering requires a separate confirmation after preview/QC. Never silently switch render engines, devices, denoisers, or color-management settings.

## Completion

Record `planned`, `scripted`, `previewed`, `rendered`, `archived`, `failed`, or `blocked`; include Blender version, scene/collection IDs, input/output hashes, frame range, render settings, logs, and warnings. Return a manifest fragment; do not edit the pipeline's global manifest or register remote Elements directly.
