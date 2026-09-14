# AEMA Character Casting Board

Use this contract before producing final references for a new recurring character.

## Single four-candidate board

Create exactly one `16:9` landscape casting board containing four equal, clearly separated cells labeled `1`, `2`, `3`, `4`. Each cell shows one different candidate as a photorealistic front-facing full-body studio photograph:

- head, hands, legs, and shoes fully visible with no cropping;
- neutral standing pose, arms relaxed, no crossed limbs or props;
- same camera height, distance, focal-length family, lighting, background, and approximate scale;
- a genuinely different facial identity in every cell, not one face with changed hair or makeup;
- age range, presentation, ethnicity where specified, role, genre, and overall realism compatible with the same canon description;
- meaningful variation in face shape, features, hairstyle, physique, height impression, proportions, posture, and silhouette;
- role-appropriate wardrobe that does not hide the physique or create an unfairly more attractive candidate;
- labels placed outside the body and kept readable.

The board is for choosing a whole actor—face and body together. Do not split face and body into separate boards. Do not show close-ups, back views, side views, multiple poses per candidate, or more or fewer than four people.


## Character description before generation

Always present the canon character description with the dry-run plan before generating candidates. It must explain the character's age, dramatic function, temperament, family resemblance requirements, physique, distinctive visual traits, and wardrobe context. Design all four faces to fit this description while remaining visibly different from one another and from already selected cast members.

If a reference image is supplied, state whether it is an identity anchor or only directional inspiration. A directional reference must not cause four near-duplicate faces. An identity anchor means casting is already locked and candidate generation should be skipped unless the user explicitly asks to recast.

## Generation plan

The dry-run plan lists exactly one image output per character:

`CHAR-...__casting-candidates-1-4__v...`

Record provider/model, `16:9` dimensions, four-cell layout, labels, reference roles, estimated cost or `unknown`, output path, and retry limit. The board remains a candidate artifact. A missing person, duplicated face, unreadable label, cropped body, inconsistent framing, or extra view requires a proposed retake and new approval; do not pay for an automatic retry.

## Selection and lock

Present the board and ask for one number. Accept forms such as `3`, `3번`, or `후보 3`, normalize the stored selection to `3`, and echo it back before producing final references.

After selection:

- crop or derive the chosen candidate only when the approved plan permits it;
- create a unified identity brief binding that exact face and physique;
- generate the required three-panel master character sheet defined in [character-reference-sheet.md](character-reference-sheet.md) as a new immutable version;
- verify that the master sheet matches both the selected face and selected silhouette;
- retain the original four-candidate board and selection record for provenance.

Do not infer a choice from praise, cursor position, or an ambiguous statement.
