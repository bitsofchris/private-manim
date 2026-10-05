# Visual styles for HyperFrames beats

**Name:** hyperframes-styles
**Description:** A digest of one research pass (2026-10-04) on which visual
styles a HyperFrames beat could take, what is known about visual treatment
and retention on Shorts, and which CSS / SVG / canvas techniques produce
each look under this repo's constraints (offline, deterministic, Inter
ExtraBold only, no assets).
**When to use:** when a Short wants a look other than the house style, or
when someone claims a style "retains better".
**How it works:** fourteen concepts were specified for one beat; ten were
built in `prototypes/hyperframes/stack-styles/` (see its README for what
each turned out like). This file keeps the evidence and the four concepts
that were not built.

## What the evidence says about style and retention

- **Measured, already in `2026-10-03-shorts-craft.md`:** the swipe-or-stay
  decision is made in 1 to 3 s; changes should land on the spoken word;
  staged transitions beat simultaneous ones; informal drawn visuals beat
  polished slides (MOOC video, not Shorts).
- **No evidence found that any one visual style retains better than
  another.** The case for a distinctive style is recognisability in the
  feed, which is practitioner opinion.
- **Vendor-blog numbers with no method shown** (treat as folklore): "80%
  held through 3 s", "on-screen text gives an 18% watch-time lift", "a
  pattern interrupt every 4 s held 58% vs 41%".
- **Practical consequence:** judge a look on frame-0 contrast against a
  feed of dark-navy, neon AI videos, and on the mute-and-squint test.
  Light and print-textured looks differ most from that feed.

## Techniques by look (all GSAP core, no plugins)

| Look | Technique |
|---|---|
| risograph overprint | `mix-blend-mode: multiply` ink layers on a paper div; grain from one-octave `feTurbulence` with the seed stepped by `render(t)` |
| blueprint draw-on | SVG paths with `pathLength="1"` and a `stroke-dashoffset` set from `render(t)`; grid from two `repeating-linear-gradient`s |
| phosphor glow | canvas 2D, `globalCompositeOperation = "lighter"`, `shadowBlur` 6 px or less with a sharp core on top; scanlines as a gradient overlay under the text |
| editorial heat map | plain DOM grid; `gsap.utils.interpolate` across three colour stops; `box-shadow: inset` ghosts |
| Swiss kinetic type | `overflow: hidden` masks, `scaleX` wipes from the left, two stacked spans per odometer cell; `expo.out` only |
| isometric solids | project by hand on a canvas and paint back to front; split a ring into a back and a front half to pass something through it |
| stop motion | `ease: "steps(n)"`; torn edges by `feDisplacementMap` on the shape, static seed |
| terminal | a fixed grid of inline-block character cells; type by slicing the string in `render(t)` |
| transit map | round-joined paths; dots placed with `getPointAtLength`; split-flap by `scaleY` |
| pixel art | full-resolution canvas with integer blocks (no CSS scaling); time quantised to 12 fps; Bayer 4x4 dither |
| halftone | `radial-gradient` dots with `background-size`, dot pitch 20 px or more to survive re-encoding |

## Not built

- **Halftone comic** (three panels, Ben-Day dots): moire risk after
  re-encoding; tone may be too jokey.
- **Focus pull** (blur and frosted glass sharpen at each block): frame 0 is
  unreadable by design, and it is the closest to the house navy.
- **Flat-glow factory** (Kurzgesagt-like machines): the most imitated
  explainer look on YouTube.
- **Bauhaus shapes** (value as shape size): loses the matrix of numbers.

## Sources

- Bartosz Ciechanowski, https://ciechanowski.com ; on interactive
  explainers, https://unsung.aresluna.org/three-good-interactive-explainers/
- Distill, https://distill.pub ; FT Visual Vocabulary,
  https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md
- Brendan Bycroft's LLM visualization, https://bbycroft.net/llm
- Riso technique, https://jonathanstephens.us/play/riso/ ; halftone in CSS,
  https://frontendmasters.com/blog/pure-css-halftone-effect-in-3-declarations/
- Vox motion style, https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/
- Kurzgesagt style,
  https://artsatmichigan.umich.edu/ink/2019/09/27/simple-bright-beautiful-the-work-of-kurzgesagt
- Vendor claims (unverified): https://www.gofaceless.ai/en/blog/high-retention-youtube-shorts-attributes ,
  https://www.opus.pro/blog/youtube-shorts-hook-formulas
