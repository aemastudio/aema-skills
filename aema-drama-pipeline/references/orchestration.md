# AEMA Pipeline Orchestration

## Stage routing

| Stage | Leaf skill | Minimum prerequisite | Successful handoff |
|---|---|---|---|
| Writing | `aema-scriptwriter` | idea, brief, or source draft | approved script, canon, scene and entity IDs |
| References | `aema-asset-builder` | approved script or explicit asset brief | locked registry and selected reference paths/IDs |
| 3D branch | `aema-blender` | scene need plus asset/context manifests | validated plan, scene/preview/render records |
| Element registration branch | `aema-asset-builder` in `register-existing` mode | approved local reference or Blender render | verified Element ID or manual-registration block |
| Video | `aema-seedance25-video` | approved scenes and locked references | selected, archived clips with request metadata |
| Subtitles | `aema-korean-srt` | actual final audio/video | validated UTF-8 SRT, transcript, QC report |

The pipeline may dry-plan a later stage using provisional inputs, but it must mark the result provisional and cannot satisfy that stage's prerequisite.

## Checkpoints

Use explicit review checkpoints for:

1. story/canon approval;
2. reference lock and selected images;
3. external image generation scope;
4. upload/Elements registration scope;
5. video generation scope and retake budget;
6. Blender preview versus final render;
7. final clip selection and subtitle QC.

The user's approval of one checkpoint does not approve later costs or mutations.

## Resume and invalidation

At the start of a run, compare current input hashes with the last approved stage inputs.

- Dialogue-only changes normally stale affected video/audio/subtitle items, not unrelated visual references.
- Identity, wardrobe, location, or hero-prop changes stale dependent references, Blender renders, and video shots.
- A selected-take change stales downstream assembly/subtitle timing but not source generation.
- Subtitle text corrections do not stale video unless captions are later burned in.

Record dependencies by stable ID so invalidation can be selective. Preserve stale artifacts for provenance.

## Failure handling

Stop a stage when a required tool, reference, right/consent check, media input, or authorization is unavailable. Return `blocked` with the exact missing prerequisite and keep independent stages usable. Never substitute a provider or increase scope without a new reviewed plan.
