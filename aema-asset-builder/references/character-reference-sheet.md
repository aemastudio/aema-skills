# AEMA Three-Panel Character Reference Sheet

After the user selects a casting pair such as `1+E`, create exactly one `16:9` landscape master character-reference image with three fixed panels. This is the first locked character artifact and the source reference for later images, Elements, Blender, and video shots. The project's delivery video may remain `9:16`; the master reference sheet itself is always `16:9`.

## Fixed left-to-right layout

### Left — front full body with head bowed

- show the selected body and physique from head to toe;
- use a neutral front-facing standing pose with arms and legs clearly readable;
- bow the head deeply downward so the face is naturally obscured and difficult to identify;
- do not turn the head away, cover it with hands or props, add a mask, blur the face, or crop the face out;
- do not crop the head, hands, or feet; avoid props and gestures that obscure the body.

### Center — back view

- show the same character from directly behind, head to toe;
- preserve the exact selected physique, height impression, hair length, baseline wardrobe, footwear, and accessories;
- use the same neutral stance, camera height, scale, lighting, and background as the left panel;
- make the back silhouette, garment construction, hair back, and accessory placement clearly readable.

### Right — large face close-up

- show a large, straight-on close-up of the selected face;
- use neutral expression, unobstructed features, realistic skin texture, and even identity lighting;
- preserve face shape, eyes, brows, nose, mouth, skin markers, hairline, hairstyle, and stable asymmetry from the selected face candidate;
- fill most of the panel with the head and upper shoulders without cutting off identity-critical hair or jaw details.

## Cross-panel consistency

All three panels depict one character version. Keep body, hair, wardrobe, palette, grooming, accessories, age impression, and style identical. The right close-up owns facial identity; the left panel must not introduce a competing face. The center panel must not change body proportions or clothing.

Use a clean neutral background, consistent color management, no dramatic perspective, no environmental storytelling, no extra people, and no decorative collage elements. Separate panels cleanly. Do not put descriptive text over the character.

The canvas aspect ratio is `16:9`, with three vertical panels arranged left to right. Keep enough horizontal width for the right face close-up while preserving uncropped full-body views in the left and center panels.

## Output and QC

Use an immutable item ID such as `CHAR-001__master-reference-3panel__v001`. Store the casting selection (`1+E`), face-board hash, body-board hash, prompt/plan/run IDs, output hash, and selected status.

Reject or propose a new approved take when:

- the left panel does not show a deeply bowed head, or the face remains clearly identifiable;
- the left panel hides the face by turning away, masking, blurring, covering, or cropping instead of bowing the head;
- any head, hand, foot, hairstyle, garment, or accessory is cropped or missing;
- the center is not a true back view;
- the right close-up does not match the selected face;
- body proportions, hair, wardrobe, or accessories drift between panels;
- the image contains extra views, people, props, text overlays, or a non-neutral background.

Do not automatically pay for a retry. Present the QC failure and wait for approval of a revised generation plan.
