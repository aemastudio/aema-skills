# Vertical AI Short-Drama Writing Guide

Read this reference when the requested script will be produced as a short-form vertical video.

## Story shape

- Put a legible curiosity, conflict, surprise, or emotional promise in the opening seconds.
- Give every scene one dominant dramatic job. Combine or remove beats that repeat the same information.
- Budget spoken lines against the intended runtime; allow space for looks, physical actions, reveals, and transitions.
- End episodes with a payoff, reversal, decision, or new question rather than an arbitrary stop.

## 9:16 staging

- Prefer staging that reads with one or two dominant subjects in a portrait frame.
- Specify important vertical relationships: foreground/background, top/bottom reveal, doorway, staircase, phone screen, full-body entrance, or close reaction.
- Avoid making essential story information depend on a very wide group tableau. If a wide location is essential, identify a portrait-safe crop or a sequence of details.
- Keep on-screen text within a central safe region and do not make tiny background text carry the plot.

## Consistency ledger

For each recurring entity, record the facts that production must preserve. Character rows are only an index; use [character-canon.md](character-canon.md) for the full recurring-character dossier.

```text
CHAR-001 | canonical name | aliases | age range | immutable facial markers |
body/silhouette | baseline hair | baseline wardrobe | permitted scene changes

LOC-001  | canonical name | time/weather variants | fixed geometry and landmarks |
palette | practical light sources | continuity-sensitive state

PROP-001 | canonical name | dimensions/shape | material | color | wear/damage |
story function | state by scene
```

Distinguish immutable identity anchors from scene-specific changes. A torn sleeve or cracked lens is a timeline event, not a redesign.

## Production-script scene fields

Each scene should expose enough structure for downstream tools without becoming a shot prompt:

```text
Scene ID and estimated duration
INT./EXT. - location ID - time
Characters, location, and prop IDs
Visible action and emotional turn
Dialogue and speaker
Sound or silence that affects the story
Entry state -> exit state
9:16 staging note
Continuity dependencies
```

Keep camera jargon optional at the writing stage. Describe the visual intention; the video skill owns shot design and provider prompts.
