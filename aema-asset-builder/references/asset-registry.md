# Asset Registry Contract

Read this reference when producing the reference lock or a provider execution plan.

Provider capabilities can change. Use the [Higgsfield MCP guide](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp) and [Elements workflow](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-cinema-studio) only as official starting points, then inspect the live tools before execution. Do not infer a create/register API from the ability to reference existing Elements.

## Canonical registry

Use JSON with `schema_version: "aema.assets/v1"`. The top-level object contains `project_id`, `registry_version`, `source_script`, and arrays named `characters`, `locations`, and `props`.

Every asset entry requires:

- `id`: stable type-prefixed ID such as `CHAR-001`, `LOC-001`, or `PROP-001`;
- `version`: immutable version such as `v001`;
- `name` and optional `aliases`;
- `status`: `draft`, `review`, `locked`, or `retired`;
- `source_scenes`: script scene IDs;
- `identity_anchors`: traits that must persist;
- `allowed_variants`: named, scene-bound changes;
- `reference_artifacts`: relative local paths, hashes, selection status, and optional remote IDs;
- `provenance`: prompt/plan/run IDs and provider metadata without secrets.

Character entries should distinguish face, hair, body/silhouette, baseline wardrobe, and scene wardrobe. Location entries should distinguish fixed geometry from time, weather, dressing, and damage variants. Prop entries should capture scale, shape, material, color, wear, and story-state changes.

## Prompt package

For each planned image, include:

```json
{
  "item_id": "CHAR-001__identity-front__v001",
  "asset_ref": "CHAR-001@v001",
  "purpose": "identity reference",
  "aspect_ratio": "9:16",
  "composition": "portrait-safe framing",
  "positive_prompt": "...",
  "negative_constraints": ["..."],
  "input_reference_ids": [],
  "output_path": "02_references/characters/CHAR-001/v001/generated/...",
  "status": "planned"
}
```

Use reference IDs rather than re-describing a locked identity differently in every prompt. Generated images are candidates until explicitly selected.

## Registration record

Registration is separate from generation. Record the local artifact path and hash, remote provider, remote Element ID, registration time, response metadata path, and the authorizing `run_id`/`plan_hash`. Detect duplicates by artifact hash and existing remote ID before registering.
