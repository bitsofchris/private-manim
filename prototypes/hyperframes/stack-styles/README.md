# Stack styles: one beat, ten looks

**Name:** hyperframes-stack-styles
**Description:** A style exploration from 2026-10-04: beat 6 "Stack" of
`videos/005-transformer-short` ("Now each block receives the previous
block's output and continues to refine it further") built eleven times in
HyperFrames, five seconds each, with the same matrix values and cue times,
to see which visual styles the engine can carry. `00_house` is the control:
the current house style rebuilt in HyperFrames.
**When to use:** when choosing a look for a Short, or when you need a
worked example of a technique (canvas glow, blend modes, stepped motion,
clip masks, path following, a character grid).
**How it works:** one folder per style, each a complete beat (`index.html`
plus the `vendor` symlink). `_scaffold/` is the starting file that passes
`check`; `BUILD-BRIEF.md` is the contract the five builder agents got. The
styles break the house palette on purpose, so none is a shippable beat as
it stands.

```
cd prototypes/hyperframes/stack-styles/NN_slug
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o out/NN_slug.mp4   # out/ is gitignored
```

| Folder | Style | How the stack is drawn | Technique worth copying | Could carry 60 s? |
|---|---|---|---|---|
| `00_house` | house style (control) | bracketed matrix, panels, magenta flow line | DOM matrix with value-tinted cells | it is the current look |
| `01_riso` | two-ink risograph | three print passes; misregistration tightens | `mix-blend-mode: multiply`, stepped grain | yes, with the grain slowed |
| `02_blueprint` | blueprint | exploded assembly, rev A/B/C stamps | `pathLength="1"` draw-on, crosshair on `getPointAtLength` | yes, for structure beats |
| `03_scope` | oscilloscope | three gates denoise each token's trace | canvas `lighter` + `shadowBlur`, hashed noise | yes; one hue for a minute is the risk |
| `04_editorial` | FT / Distill light mode | heat-map cells and a layer slider | diverging colour scale in `render(t)`, inset ghosts | yes |
| `05_swiss` | Swiss typographic | giant numerals, one red bar, odometer digits | clip masks with the layout waivers | for "one number, one idea" beats |
| `06_iso` | isometric tower (lilac) | a tray of tiles falls through three ring slabs | painter's-order isometric on canvas | became 009 |
| `07_paper` | paper collage on twos | index card under three stencil windows | `steps()` eases, torn edges by displacement | yes, but every prop is hand-tuned |
| `08_terminal` | REPL session | three calls; the stack is the scrollback | fixed character grid, typed text by slicing | paired with a diagram style |
| `09_transit` | transit map | token lines through three stations, split-flap board | dots along paths, concentric bends | yes, with few labels per frame |
| `12_pixel` | pixel art | a sprite hops down three levels | 5x7 glyph table, Bayer dither, 12 fps tick | only for a game-themed video |
| `13_iso_house` | isometric, house palette | `06_iso` recoloured | the house palette on slabs and tiles | became 009 |

## What it showed

- The control matches the Manim beat closely, so the engine does not limit
  the house look. Renders took 5 to 10 seconds; each builder reached a
  passing beat in two or three rounds.
- The binding constraint is the 60 px text floor with one heavy font: nine
  numbers and three words drove every layout. A lighter weight or a
  condensed face would loosen all of them.
- Chris picked the isometric one, asked for it in the house colours
  (`13_iso_house`), and 009 rebuilt the whole transformer Short in it.
- Two passes rest on audit waivers: `01_riso` (blended text is skipped by
  the contrast audit) and `05_swiss` (clipped numerals).
- The traps found here are in `agents/beat-brief-hyperframes.md` ("What
  `check` and the renderer trip on"); the research behind the ten styles is
  `agents/research/2026-10-04-hyperframes-styles.md`.
