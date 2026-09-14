# AEMA Character CANON Contract

Use this contract for every recurring character. The CANON ledger must be detailed enough that a later writer can preserve the character and `aema-asset-builder` can prepare casting without inventing missing fundamentals.

## Required character dossier

### Identity and story function

- stable ID, canonical name, aliases, pronouns where relevant, age or credible age range;
- occupation, education or skill background, economic and social context when story-relevant;
- dramatic role, public goal, private need, fear, secret, contradiction, stakes, and character arc;
- formative history and the specific past event that shapes present behavior;
- relationships to other recurring characters, including what each person knows, wants, hides, and misunderstands.

### Personality and performance

- dominant traits plus at least one counter-trait that prevents a flat stereotype;
- values, boundaries, habits, stress response, conflict style, affection style, and decision pattern;
- speech rhythm, vocabulary level, sentence length, honorific use, verbal tics, humor, lies, and silence behavior;
- default facial affect, gesture vocabulary, posture, walking energy, personal-space behavior, and emotional tells;
- how the character behaves differently in public, in private, and with each key relationship.

### Detailed appearance

Describe visible traits concretely enough for continuity. Cover:

- overall impression and apparent age;
- face shape, forehead, cheekbones, jawline, chin, and facial proportions;
- eye shape, size, spacing, eyelids, brows, gaze quality, and any stable asymmetry;
- nose bridge, tip and width; lips and mouth shape; smile characteristics;
- skin tone/undertone, texture, freckles, moles, scars, facial hair, or other distinguishing markers;
- hair color, length, texture, density, parting, hairline, and baseline styling;
- height impression, build, shoulder line, torso/hip relationship, limb proportions, hands, posture, and silhouette;
- movement quality and the way physique affects blocking or gesture;
- baseline wardrobe silhouette, palette, fit, fabrics, footwear, accessories, grooming, and condition;
- continuity-critical details visible in close-up, medium shot, and full-body framing.

Avoid vague shorthand such as “handsome,” “pretty,” “ordinary,” or “model-like” without observable features. Do not compare the character to a living celebrity or require imitation of a real person's likeness unless the user supplies an authorized reference and explicitly requests it.

## Lock levels for casting

Separate the appearance dossier into three classes:

- `story-locked`: cannot change without affecting plot, identity, representation, continuity, or user intent;
- `casting-flexible`: should vary across the four full-body candidates `1–4` so the user has meaningful whole-character choices;
- `scene-variant`: wardrobe, grooming, injury, fatigue, weather, age-state, or other changes tied to named scenes.

Detailed description does not mean every feature is already selected. When the user has not fixed a feature, describe the intended range and label it `casting-flexible`. The asset builder must preserve story-locked traits while varying only flexible traits.

## Output template

```text
CHAR-001 — [이름]

[기본 신원]
나이/성별 표현/직업/생활 배경:
극중 역할:

[내면과 서사]
외적 목표 / 내적 욕구 / 두려움 / 비밀 / 모순:
과거와 형성 사건:
시작 상태 → 변화 → 도착 상태:

[성격과 연기]
핵심 성격 / 반대 성향:
말투·어휘·존댓말·버릇:
표정·제스처·자세·걸음:
공적 행동 / 사적 행동 / 관계별 차이:

[외모 상세]
전체 인상과 나이감:
얼굴형·윤곽·비율:
눈·눈썹·시선:
코·입·미소:
피부·수염·점·흉터·비대칭:
머리색·길이·질감·가르마·스타일:
키 인상·체형·어깨·상하체·팔다리·손:
자세·실루엣·움직임:
기본 의상·색상·핏·소재·신발·액세서리:
클로즈업/미디엄/전신에서 반드시 보일 특징:

[캐스팅 전달]
story-locked:
casting-flexible:
scene-variant:

[관계]
CHAR-...에 대해 원하는 것 / 아는 것 / 숨기는 것 / 오해하는 것:

[연속성]
첫 등장 상태:
장면별 의상·부상·소품·감정 변화:
미해결 항목:
```

Do not fill gaps with arbitrary precision. Mark consequential unknowns as unresolved, but make reasonable, clearly labeled choices when the production can proceed without user input.
