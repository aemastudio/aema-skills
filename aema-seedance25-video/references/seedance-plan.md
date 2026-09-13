# Seedance 2.5 Plan Contract

Read this reference when writing provider prompts or an executable generation plan.

## Capability preflight

Seedance 2.5 capabilities and identifiers differ by provider and plan. Verify them through the connected provider immediately before execution. Do not hardcode price, model ID, resolution, or reference limits.

Official starting points:

- [ByteDance Seedance 2.5 overview](https://seed.bytedance.com/en/seedance2_5)
- [BytePlus Seedance video generation](https://docs.byteplus.com/en/docs/Byteplus_LAS/video_gen_enhanced)
- [Higgsfield Seedance guide](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-seedance)

Official documentation describes 9:16 and native audiovisual generation, but an adapter may expose only a subset. Use only confirmed parameters. Check provider policy and the user's rights/consent before uploading any real-person reference.

## Prompt packet

Keep canonical intent separate from provider payload:

```text
SHOT: E01-S001-C001 / duration target
PURPOSE: the one dramatic or visual job of the clip
REFERENCES: CHAR-001@v001, LOC-001@v002, PROP-001@v001, remote IDs if verified
CONTINUITY IN: positions, wardrobe, damage, carried props, light and weather
TIMELINE: ordered beats with approximate time windows
CAMERA: portrait framing, height, lens character, motion, focus behavior
PERFORMANCE: action, gaze, expression, interaction and physical constraints
ENVIRONMENT: only motion and details relevant to the beat
AUDIO: spoken language and exact line, ambience, effects, music choice
CONTINUITY OUT: final pose, direction, object state and transition handle
AVOID: concrete drift risks, not a generic negative-prompt dump
```

Do not overload a short clip with more actions or dialogue than its duration can show. For a multi-beat clip, use explicit chronological wording or timestamps supported by the active adapter.

## Generation-plan JSON

Use `schema_version: "aema.video-plan/v1"`. Calculate `plan_hash` as lowercase SHA-256 of the canonical UTF-8 JSON after removing the top-level `plan_hash`, using sorted keys and compact separators.

Required top-level fields:

```json
{
  "schema_version": "aema.video-plan/v1",
  "run_id": "RUN-...",
  "plan_hash": "...",
  "mode": "dry-run",
  "provider": "unresolved",
  "model": "unresolved",
  "aspect_ratio": "9:16",
  "cost_estimate": {"amount": null, "currency_or_credits": "unknown", "checked_at": null},
  "external_actions": [],
  "authorization": {"required": true, "status": "not-approved"},
  "shots": []
}
```

Each shot requires `shot_id`, `take_id`, `duration_seconds`, `asset_refs`, `prompt`, `output_path`, and `status`. Keep provider payloads as children of the corresponding shot, not as the canonical prompt.

## Results

Store the request ID as soon as the provider returns it. Keep status responses, provider/model revision, submitted payload, cost charged if available, media checksum, and local relative path. Remote URLs may expire and are not the archive.
