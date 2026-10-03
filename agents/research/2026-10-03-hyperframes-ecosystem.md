# HyperFrames ecosystem: what's there and what's worth using

**Name:** hyperframes-ecosystem
**Description:** A map of the HyperFrames repo, CLI, docs and catalog as of
`hyperframes@0.8.115` (2026-10-03), sorted by usefulness to this repo's
voice-first Shorts pipeline. From the repo README, the docs index
(`hyperframes.heygen.com/llms.txt`) and `hyperframes --help`.
**When to use:** before building a HyperFrames beat, to know which
built-in commands and docs to reach for and which to leave alone.
**How it works:** we use HyperFrames as a renderer only. Our voice,
captions, assembly, style and process stay ours (`AGENTS.md`).

## Use these

| What | Command or link | Why it helps us |
|---|---|---|
| Layout gate | `hyperframes check` (lint + runtime + layout + contrast) | the geometry check our Manim side lacks; already in the brief |
| Layout across time | `hyperframes inspect` | reports overlaps and off-frame elements along the timeline, not just one frame |
| Key frames as PNG | `hyperframes snapshot` | review a beat without rendering the mp4; faster than a contact sheet |
| Variant sheet | `hyperframes compare` | renders variants of a composition into one labelled sheet: A/B two openings for Chris in one image |
| Keyframe diagnostics | `hyperframes keyframes` | onion-skin view of motion paths when a move reads wrong |
| Word-level timestamps | `hyperframes transcribe` (local Parakeet model via `hyperframes models`) | the "word-level timestamps" backlog item: cue times per word instead of RMS guessing; test against MacWhisper before adopting (it downloads a model) |
| Transparent output | `render` to WebM with alpha (see rendering docs) | a HyperFrames character or overlay on top of a Manim beat |
| Variables | docs: `concepts/variables` | one composition, many beats: pass `BEAT_SECONDS`, the example text, the ledger values in as data |
| Environment check | `hyperframes doctor`, `hyperframes clean` | diagnose Chrome/ffmpeg; remove caches it left on disk |
| Local docs | `hyperframes docs <topic>` (data-attributes, gsap, compositions, rendering, examples, troubleshooting) | offline reference for agents |
| Studio | `hyperframes preview` | Chris can scrub a composition and nudge timing by hand |

## Read these (docs worth an agent's time)

- Determinism: https://hyperframes.heygen.com/concepts/determinism.md
- HTML schema and data attributes: https://hyperframes.heygen.com/reference/html-schema.md , https://hyperframes.heygen.com/concepts/data-attributes.md
- GSAP in compositions: https://hyperframes.heygen.com/guides/gsap-animation.md
- Rules and anti-patterns: https://hyperframes.heygen.com/prompting/rules-and-anti-patterns.md
- Explainers and storyboards: https://hyperframes.heygen.com/prompting/explainers.md , https://hyperframes.heygen.com/prompting/storyboards.md
- Motion that reads well: https://hyperframes.heygen.com/prompting/motion.md
- Code animations, data and maps: https://hyperframes.heygen.com/prompting/code-blocks.md , https://hyperframes.heygen.com/prompting/data-and-maps.md
- Caption styles (ideas only; ours are burned by `assemble.py`): https://hyperframes.heygen.com/prompting/captions-catalog.md
- Rendering options: https://hyperframes.heygen.com/guides/rendering.md
- Other runtimes (Lottie, Three.js, CSS keyframes, WAAPI): https://hyperframes.heygen.com/prompting/runtimes-and-3d.md , https://hyperframes.heygen.com/concepts/frame-adapters.md
- The whole index: https://hyperframes.heygen.com/llms.txt

## Browse for ideas, adopt with care

- **Catalog** (~388 blocks: transitions, overlays, charts, captions,
  maps, effects): https://hyperframes.heygen.com/catalog . `hyperframes
  add <block>` copies code from their registry into the project, so each
  block is a new dependency: read it, vendor it, and keep it offline like
  GSAP. Good for seeing how something is built.
- **Shader transitions** (`@hyperframes/shader-transitions`): beat-to-beat
  transitions inside one composition. We cut between beats in
  `assemble.py`, so only relevant if a Short becomes one composition.
- **Player** (`@hyperframes/player`, a `<hyperframes-player>` web
  component): embed a live composition on a web page instead of a GIF.
  Substack won't run it; a personal site would.
- **Showcase and "30 Days of HyperFrames"**: reference for what the engine
  can look like. https://hyperframes.heygen.com/showcase

## Leave alone

- **Skills and plugins** (`skills`, `npx skills add`, the Claude plugin,
  the 21 workflow skills): they rewrite agent config and bring their own
  process. Ours is `agents/beat-brief-hyperframes.md`. Their skill text is
  fine to read as reference.
- **`publish`, `cloud`, `auth`, `lambda`, `cloudrun`**: upload the project
  or render on someone else's machines. Nothing leaves this machine
  without Chris asking.
- **`tts`, avatar presenter, `capture`**: synthetic voice, a talking
  avatar, website capture. Chris records his own voice; none of these fit.
- **Telemetry** is on by default. We set `HYPERFRAMES_NO_TELEMETRY=1` and
  `HYPERFRAMES_NO_UPDATE_CHECK=1` in every command.
- **Their captions, audio mixing, music beat detection**: our assembler
  owns audio and captions.
