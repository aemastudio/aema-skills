# AEMA Archive Contract

This is the only canonical archive contract for the six-skill suite. The pipeline owns the global manifest. Leaf skills receive a scoped context and return fragments; they do not redefine the layout or concurrently edit global state.

## Project tree

```text
PROJECT_ROOT/
|-- aema-project.json
|-- 01_script/
|   |-- brief/
|   |-- treatments/
|   |-- episodes/
|   `-- canon/
|-- 02_references/
|   |-- characters/
|   |-- locations/
|   |-- props/
|   `-- registries/
|-- 03_prompts/
|   |-- image/
|   |-- video/
|   `-- blender/
|-- 04_elements/
|   |-- registration-plans/
|   `-- records/
|-- 05_video/
|   |-- cuts/
|   |-- selected/
|   `-- qc/
|-- 06_blender/
|   |-- plans/
|   |-- scenes/
|   |-- scripts/
|   |-- previews/
|   `-- renders/
|-- 07_audio/
|   |-- source/
|   `-- extracted/
|-- 08_subtitles/
|   |-- transcripts/
|   |-- srt/
|   `-- qc/
|-- 09_exports/
`-- runs/
    `-- RUN-.../
        |-- plan.json
        |-- authorization.json
        |-- ledger.jsonl
        `-- stages/<skill-name>/manifest-fragment.json
```

Add subdirectories only for real project needs. Do not create a second archive root inside a leaf stage.

## Global manifest

`aema-project.json` uses `schema_version: "aema.archive/v1"` and contains:

- `project_id`, title, creation/update timestamps, default `aspect_ratio`, language, and optional episode metadata;
- stable entity/scene registries or relative links to their canonical files;
- stage state with current approved version, input hashes, output paths, and last `run_id`;
- remote provider IDs only when verified;
- no passwords, tokens, session cookies, private keys, or expiring signed URLs as the sole artifact location.

Paths stored in manifests are relative to `PROJECT_ROOT` and use `/`. Record SHA-256 for immutable source and generated artifacts.

## IDs and versions

- Project: `AEMA-YYYYMMDD-slug`
- Run: `RUN-YYYYMMDDTHHMMSSZ-shortid`
- Character/location/prop: `CHAR-001`, `LOC-001`, `PROP-001`
- Scene/clip/take: `E01-S001`, `E01-S001-C001`, `E01-S001-C001-T001`
- Immutable versions: `v001`, `v002`, and so on

Names are labels; IDs carry identity. An alias change does not create a new entity. A material identity redesign does create a new immutable version. Intentional scene-state changes refer back to the same version plus a named variant.

Never overwrite an approved, selected, registered, or delivered artifact. Write a new version and keep provenance to the prior one.

## Leaf `archive_context`

The pipeline passes:

```json
{
  "schema_version": "aema.archive-context/v1",
  "project_root": "absolute path used only at runtime",
  "run_id": "RUN-...",
  "stage_dir": "runs/RUN-.../stages/aema-...",
  "global_manifest": "aema-project.json",
  "input_versions": {},
  "mode": "dry-run"
}
```

The leaf writes inside `stage_dir` plus its declared project output directory, then returns a manifest fragment containing inputs/hashes, outputs/hashes, status, warnings, provider requests, and next prerequisites. The fragment uses relative paths. Only the pipeline merges it into the global manifest.

## Plans and authorization

Every external execution plan has a canonical `plan_hash`, itemized actions, provider/model, count, duration or dimensions, estimated cost or `unknown`, output locations, and retry ceiling. Approval is bound to that run and hash. Store a minimal approval record with approved scope and time; do not store credentials or unrelated conversation content.

If scope, provider, model, quality, reference set, count, or price ceiling changes, create a new plan. Separate generation from upload/registration so each remote mutation remains visible.

## State and recovery

Write global manifest changes atomically and append ledger events. Save remote request IDs before polling. A crash or timeout resumes from stored state; it does not resubmit blindly. If a remote result link is temporary, copy the result to durable local storage promptly and verify its checksum.

Use `planned`, `review`, `approved`, `submitted`, `running`, `complete`, `selected`, `archived`, `failed`, `blocked`, or `stale` only when evidence supports the state.
