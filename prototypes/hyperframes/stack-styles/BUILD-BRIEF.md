# Stack-styles exploration: builder brief

**Name:** stack-styles-builder-brief
**Description:** The shared contract for the 2026-10-04 style exploration: ten
visual styles for one five-second beat (beat 6 "Stack" of
`videos/005-transformer-short`), each built as one HyperFrames `index.html`.
**When to use:** you were handed this path plus one or two style specs.
**How it works:** copy `_scaffold/`, keep its contract, replace everything
visual with your style, check, render, review your own contact sheet, report.

## The beat

VO: "Now each block receives the previous block's output and continues to
refine it further." On screen: the L x d matrix for the tokens `my name is`
(3 columns, 3 values each) goes through a stack of 3 transformer blocks; each
block takes the previous block's output and changes the numbers a little. The
shape never changes. The Manim original: `videos/005-transformer-short/06_stack.py`.

## This is a style experiment

The house palette, the "background is always #0B0B14" rule and the
one-magenta-hero rule from `agents/beat-brief-hyperframes.md` do NOT apply
here: your style spec sets the palette, type and motion. Push the style hard;
a timid version tells Chris nothing. Everything technical in that brief still
applies (read it): pure function of time, one paused GSAP timeline registered
on `window.__timelines["main"]`, no network, no `Math.random`, no CSS
animations or transitions, transforms only in tweens (HyperFrames' `check`
rejects tweens on `top` / `left` / `width` / `height`; use `x` / `y` / `scale`
/ `opacity`, or set layout values inside a `render(t)` function).

## Fixed for every style (so the ten are comparable)

- 1080 x 1920, 30 fps, `data-duration="5"`.
- The `DATA` and `CUE` constants in `_scaffold/index.html`, unchanged:
  the matrix goes from `DATA.before` to `DATA.after`; show it as three visible
  refinements, one per block (interpolate in thirds, one decimal, e.g. the
  scaffold's `lerp`). Blocks are established by `CUE.blocks` (1.1 s); the
  matrix passes through them from `CUE.refine` (2.6 s); nothing moves after
  `CUE.still` (4.4 s), including grain, boil, drift and glow pulses.
- Frame 0 already shows the matrix and at least one block, with something
  moving. The last 0.6 s is a still, finished composition.
- The words `my`, `name`, `is` and the nine values are legible at phone size:
  digits and labels at least 60 px tall type. Blocks are identifiable as
  block 1, 2, 3 (numerals are enough).
- Content inside the safe area x 65-950, y 230-1536; the main visual in the
  stage y 230-1100. The band y 1100-1536 gets no content (captions are burned
  in there later) but the background and texture should run to the frame edge.
- Fonts: Inter ExtraBold via the local `@font-face` in the scaffold, plus the
  CSS generic families. If your spec wants `serif` or `monospace`, try it: if
  `check` complains or the render falls back oddly, use Inter and say so.
- No images, no new files besides `index.html`, no npm installs, no GSAP
  plugins. Everything is drawn with HTML / CSS / SVG / canvas 2D.

## Setup and commands

```
cd /Users/chris/repos/private-manim/prototypes/hyperframes/stack-styles
mkdir NN_slug && cp _scaffold/index.html NN_slug/index.html
ln -s ../../../../videos/_shared/web/vendor NN_slug/vendor
cd NN_slug && mkdir -p out
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o out/NN_slug.mp4
../../../../tools/review_frames.sh out/NN_slug.mp4 4 8 out/sheet.png
```

Open `out/sheet.png` with the Read tool and look at it critically: is the
style unmistakable in frame 0, are the digits readable at that tile size, is
anything clipped or in a dead zone, is the last tile still and finished? Up to
three render-and-review rounds per style. `check` must end "Check passed"
(contrast warnings on decorative text are acceptable; say which).

Never run: `hyperframes init`, `add`, `catalog`, `skills`, `publish`, `cloud`,
`lambda`, `tts`, `transcribe`, `models`, `npx skills add`, or any `npm
install`. Do not edit anything outside your own `NN_slug/` folders. Do not
commit.

## Report (short)

Per style: the folder, the mp4 path and measured duration, the `check`
result, what you changed from the spec and why, what was hard or impossible
in HyperFrames, and one honest sentence on whether this style could carry a
full 60 s technical Short.
