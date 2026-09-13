# AEMA Character Casting Board

Use this contract before producing final references for a new recurring character.

## Board 1: face candidates

Create one contact sheet with five equal, clearly separated cells labeled `1`, `2`, `3`, `4`, `5`. Each cell shows a different facial identity under the same neutral conditions:

- head-and-shoulders or tight portrait, straight-on;
- neutral expression, unobstructed face, consistent focal length and lighting;
- same stated age range, presentation, role-compatible styling, hair treatment, and realism/style family;
- no hats, sunglasses, dramatic makeup, extreme expressions, or pose changes that prevent fair comparison.

Vary facial structure and distinctive identity traits enough to make the five choices meaningfully different. The label must be outside the face and remain readable. Do not generate five separate deliverables when the requested review artifact is one board.

## Board 2: body candidates

Create one contact sheet with five equal, clearly separated cells labeled `A`, `B`, `C`, `D`, `E`. Each cell shows a different full-body build and silhouette under comparable conditions:

- front-facing neutral stance, head-to-toe visible, no cropping;
- simple fitted neutral clothing that reveals silhouette without sexualization;
- same camera height, distance, lighting, background, and approximate scale guide;
- vary height impression, shoulder/hip relationship, build, limb proportions, posture, and overall silhouette.

The body board is for physique selection, not a second face audition. Use a neutral/de-emphasized provisional face and do not treat it as identity. Preserve role, age range, accessibility needs, and user-specified physical constraints.

## Generation plan

The dry-run plan lists exactly two image outputs per character:

1. `CHAR-...__casting-face-1-5__v...`
2. `CHAR-...__casting-body-A-E__v...`

Record provider/model, board dimensions, layout, labels, estimated cost or `unknown`, output paths, and retry limit. Both boards are candidates, not locked references. A failed label or cropped body requires a proposed retake and new approval; do not pay for an automatic retry.

## Selection and lock

Present both boards together and ask for one face number plus one body letter. Accept compact forms such as `1E`, `1+E`, or `얼굴 1 / 몸 E`, normalize the stored value to `1+E`, and echo it back before producing final references.

After selection:

- crop or derive the chosen candidates only when the generation plan permits it;
- create a unified identity brief that binds the exact chosen face to the exact chosen physique;
- generate the required three-panel master character sheet defined in [character-reference-sheet.md](character-reference-sheet.md) as a new immutable version before optional expression or pose variants;
- check that the final full-body face matches the selected face and the silhouette matches the selected body;
- keep both original casting boards and the selection record for provenance.

Do not infer a choice from praise, cursor position, or an ambiguous statement. If only one axis is selected, keep the other axis pending.
