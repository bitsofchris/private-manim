# Beat-agent brief: HyperFrames

**Name:** beat-agent-brief-hyperframes
**Description:** The contract a subagent gets when it builds one or two
beats of a Short in HyperFrames (HTML/CSS/SVG + GSAP, rendered to MP4 by
headless Chrome via `npx hyperframes@0.8.115`). The orchestrator pastes
this file's path plus the beat-specific brief (beat number, folder name,
`BEAT_SECONDS`, VO with master times, the visual brief, the hero).
Manim beats get `agents/beat-brief.md` instead.
**When to use:** runbook step 6, for every beat whose storyboard row says
`hyperframes` (the default engine; `AGENTS.md` "Which engine").
**How it works:** one folder per beat holding one `index.html`; build it
from a prototype, check, render to the path `beats.json` lists, review
your own contact sheet, report. You never edit `videos/_shared/` (that
includes `videos/_shared/web/vendor/`).

## Read first, in this order

1. `AGENTS.md` (two heroes, captions rule 6; the Manim-only rules do not
   apply), `agents/animation-rules.md`, the Shorts rules in
   `agents/style.md` (they hold for both engines).
2. The worked examples: `prototypes/hyperframes/quiz/` and
   `prototypes/hyperframes/ironies/` (`concept.md`, then `index.html`).
   `agents/parts.md` ("HyperFrames prototypes") says which piece of which
   file to copy. Copy, do not rewrite.
3. The video's `storyboard.md`: the "Final beats" table is the contract
   (start, length, folder, VO), and its seam-states row for each of your
   cuts is what your first and last frames show; the beats table and the
   ledger above it are the visual brief. Names, example values and choices come from the
   ledger, never invented in the beat.

## Where a beat lives

```
videos/NNN-slug/
  NN_beat/                    one HyperFrames beat (name as in the storyboard)
    index.html                the composition: the only file you write
    vendor -> ../../_shared/web/vendor     symlink: GSAP + Inter, offline
  media/hf/NN_beat.mp4        the render (gitignored); beats.json points here
```

Set it up from the video folder:

```
cd videos/NNN-slug
mkdir NN_beat && ln -s ../../_shared/web/vendor NN_beat/vendor
cp ../../prototypes/hyperframes/ironies/index.html NN_beat/index.html   # or quiz/
```

In a series episode (`videos/NNN-series/epNN-slug/`) every link is one
`../` deeper: `ln -s ../../../_shared/web/vendor NN_beat/vendor`. The
episode prompt lists the links the series needs.

`index.html` plus `vendor/` is a complete HyperFrames project; no
`package.json`, `hyperframes.json` or `node_modules`. Do **not** run
`hyperframes init`. If one ever has to run, use `HYPERFRAMES_SKIP_SKILLS=1`,
delete the `CLAUDE.md` / `AGENTS.md` it writes, and replace its jsDelivr
`<script>` with `vendor/gsap.min.js`.

Never: `npx skills add`, `hyperframes skills`, `add` / `catalog` (registry
downloads), `publish` / `cloud` / `lambda` (uploads), `tts` / `transcribe`
/ `models` (model downloads), `snapshot` without `--describe false` (it
sends frames to Gemini whenever `GEMINI_API_KEY` is set), or installing
any npm package. HyperFrames
lints `../` paths above the project root as errors, which is why vendored
files come in through the `vendor` symlink, not a relative path.

## Commands (from the beat folder)

```
cd videos/NNN-slug/NN_beat
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
cd .. && "$(git rev-parse --show-toplevel)"/tools/review_frames.sh --at CUE1,CUE2 media/hf/NN_beat.mp4 4
ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 media/hf/NN_beat.mp4
```

`--prefer-offline` stops npx from asking the registry every run (without
it, an offline run stalls ~70 s). The env vars turn off HyperFrames'
telemetry and update check. Renders take 10–20 s, so render freely. While
iterating,
`npx --yes --prefer-offline hyperframes@0.8.115 preview` and add `?guides`
to the URL for the safe-area overlay (both prototypes have one).

The `beats.json` row for the beat: `{"clip": "media/hf/NN_beat.mp4", "end": BEAT_SECONDS}`.

## Rules of the beat

**Composition.**
- Root `<div id="root" data-composition-id="main" data-start="0"
  data-duration="BEAT_SECONDS" data-fps="30" data-width="1080"
  data-height="1920">`; `html, body, #root` are 1080 × 1920 with
  `overflow: hidden` and the house background.
- Elements that appear and disappear on a schedule are `class="clip"` with
  `data-start` / `data-duration` (and a `data-track-index`); everything
  else is always present and animated by the timeline.
- One paused GSAP timeline, built inline in a `<script>` at the end of
  `<body>`, registered as `window.__timelines["main"] = tl`, padded to the
  full length with `tl.set({}, {}, BEAT_SECONDS)`. The renderer seeks it
  per frame.
- Every frame is a pure function of time: a tween, a `tl.set`, or a
  function of `t` driven by a tween (the `render(t)` driver in `ironies`).
  No `Date.now`, `performance.now`, `Math.random` (use a hash of an index,
  as `ironies` does), `requestAnimationFrame`, `setTimeout`, CSS
  animations or transitions, `fetch`, or any network load. No remote
  `<script>`, `<link>`, `url()` or `@import`:
  `tests/test_hyperframes_offline.py` fails on them.
- GSAP comes from `<script src="vendor/gsap.min.js"></script>` (3.14.2).
  Inter comes from a local `@font-face`, and the stack names no other font
  family, only the generic `sans-serif`: HyperFrames tries Google Fonts
  for any named family without a local face (`-apple-system`,
  `"Helvetica Neue"`, ...):
  ```
  @font-face { font-family: "Inter"; font-style: normal; font-weight: 800;
    font-display: block; src: url("vendor/Inter-ExtraBold.woff2") format("woff2"); }
  #root { font-family: "Inter", sans-serif; }
  ```
  Only weight 800 is vendored. Need another weight: say so in the report.

**Format and time.**
- 1080 × 1920 at 30 fps. `data-duration` is `BEAT_SECONDS` to the
  millisecond; the render rounds up to whole frames (4.37 s → 132 frames
  = 4.40 s) and `assemble.py` trims to `end`.
- Frame 0 has the beat's content on screen. In the hook beat something is
  already moving; a later beat moves only what its VO names
  (`agents/animation-rules.md` rule 1) and may hold still until its first
  cue (012 ep03). Whatever moves at a cut is something from the previous
  beat's last frame carrying on,
  or a new element growing in from nothing over ~0.2 s, never a new
  element at full size: 012 ep01's loop dot appeared whole at frame 0 and
  broke the cut (222/255) until it grew in.
  The last frame is still: every motion, including the line boil and any
  drift, stops before the end (both prototypes freeze at a `HOLD_FROM` /
  `T.still` constant).
- Land each change on the word that names it. Cue times come from the
  audio, not the brief: start from the video's `words.json` (master times,
  runbook step 5), and check a cue that matters on a 10–50 ms RMS envelope
  of your window from `vo_final.wav`. Transcribe a sub-clip only for a
  word that is missing or misheard.
  Beat-local = master − start. Cues are named constants at the top of the
  script with the word in a comment: `const CUE = { auto: 1.30 /* "automate" */ };`.
- A move the viewer must track gets ≥ 0.6 s (`S.BEAT`); pops and
  colour swaps may be quicker.

**Palette.** Copied into CSS variables at the top of `<style>`.
`videos/_shared/style.py` is the source of truth for these hex values;
if it changes, so does every beat.

| CSS variable | `style.py` | Hex | Role |
|---|---|---|---|
| `--bg` | `BG_DEEP` | `#0B0B14` | background, always |
| `--panel` | `BG_PANEL` | `#14142B` | cards, panels, screens |
| `--text` | `FG` | `#ECEBE4` | ink, labels |
| `--dim` | `FG_DIM` | `#8A8FB0` | secondary labels |
| `--data` | `DATA` (`HERO_TEAL`) | `#2DD4BF` | what you can see / keep |
| `--hero` | `STRUCTURE` (`HERO_MAGENTA`) | `#C084FC` | the one hero on screen |
| `--muted` | `MUTED` | `#4A5070` | construction lines, retired heroes |

One magenta hero at a time (`AGENTS.md` rule 2), the one the brief names;
when the VO moves on, the old hero goes teal, `--dim` or `--muted`. `ACCENT_CYAN` /
`ACCENT_PINK` only for one-frame pulses.

**Layout, in pixels** (from the `SHORT_SAFE_*` fractions in `style.py`).
- Safe area: x 65–950, y 230–1536 (dead zones: top 230, bottom 384,
  right 130, left 65). Text and the hero stay inside; backgrounds and
  floor lines may bleed to the frame edge.
- Stage (the visual): y 230–1100. Caption band: y 1100–1536. With
  captions anchored bottom the stage runs to y 1330 (`agents/style.md`,
  "Share the band"); the video's brief says which.
- With VO: the band stays empty. `tools/assemble.py` burns the word
  captions there; a beat draws no captions.
- Without VO (a silent clip): one caption at a time, 2–4 words, in the
  band, ≥ 64 px, weight 800, on a dark pill (`rgba(11,11,20,0.85)`, the
  `CAPTION_PILL_OPACITY` of `--bg`). Copy the `.caption` clip from a
  prototype.
- Text floor: every label ≥ 60 px `font-size`, weight 800. Count widths
  before building: at 64 px, Inter ExtraBold runs ~38 px a character, so
  the safe width holds ~23 characters.

## What `check` and the renderer trip on

Trigger, then the fix. All found building `prototypes/hyperframes/stack-styles/`
and `videos/009-transformer-short-iso/`.

- **A tween on `top` / `left` / `width` / `height`** is a lint error
  (`gsap_non_transform_motion`). Tween `x` / `y` / `scale` / `opacity`, or
  set the value inside `render(t)`.
- **`window.__timelines` registered inside a shared script** fails the
  static lint (`missing_timeline_registry`). The literal
  `window.__timelines["main"] = ...` must be in the beat's own `index.html`.
- **A beat drawn only on a canvas, or one where only SVG colours change,**
  fails with `sweep_static` ("Timeline did not advance under seek"): the
  audit fingerprints DOM geometry and opacity, not pixels or colours (012
  ep03 beat 6). Give it one honest DOM change (a label that swells
  when its part is named).
- **Canvas text is invisible to `check`** (contrast reports 0/0). Text that
  must be read is DOM text; if it has to be canvas, judge it on the sheet.
- **A full-frame overlay** (scanlines, vignette, grain) makes every label
  "occluded". Put it under the text, or mark it `data-layout-allow-occlusion`.
- **Text clipped on purpose** (`overflow: hidden` masks, scrollback, an
  odometer) is reported as overflow / occlusion / overlap. Waive only those
  elements: `data-layout-allow-overflow`, `-occlusion`, `-overlap`. A
  full-bleed canvas takes `data-layout-allow-overflow`.
- **Text line boxes that touch** are `content_overlap` errors even when the
  glyphs do not: keep the row pitch at or above the line height.
- **`mix-blend-mode` text** is scored on its declared colour, not the
  blended pixel; `data-layout-ignore` on that text is the only way through.
  A GSAP transform isolates the blend group, so the blend mode goes on the
  tweened wrapper, not its children.
- **CSS applies `filter` before `clip-path`** on one element: clip a child,
  filter its parent.
- **Generic `serif`** renders as Inter with a synthesised italic. Generic
  `monospace` works. Any other face has to be vendored first.
- **Stepped full-frame grain** makes huge files (37 MB for 5 s): freeze or
  slow it.
- **Monospace set in the HTML rendered in Inter**, both by a CSS class
  (ep01) and by an inline `style="font-family: monospace"` attribute
  (ep03). Set it from the script, on the element and every span inside it:
  `el.style.fontFamily = "monospace"` (ep01 beats 5–6, ep03 beats 6–7;
  cause not confirmed).
- **Layout budget:** Inter ExtraBold at 60 px is about 140 px per `+0.4`.
  Count rows and widths before drawing; nine numbers plus three words is
  already a 546 x 258 px card. Monospace at 60 px fits about 22 characters
  across the safe width (012 ep04 shortened `loader = DataLoader(ds)`).

## One driver, and a shared kit when a video has one look

Draw the whole beat in one `render(t)` and let the timeline be the clock
(`ISO.start` in 009, the `driver` in `ironies`). It is a pure function of
time by construction, seeks cleanly, and keeps cues as plain numbers.

When every beat of a video shares a world, put the drawing code in one
script in the video folder and link it into each beat as `vendor` is linked
(`ln -s ../../_shared/web/iso NN_beat/iso`, then `<script src="iso/iso.js">`): 009's
`videos/_shared/web/iso/iso.js`. The kit also defines the canonical frame each beat opens and
ends on, which is what lets beats be built in parallel and still cut
cleanly. Beat agents do not edit the kit; they write local helpers and name
them in the report.

Put the storyboard's seam-states table in the kit as data (`SEAM`, plus
`START` for the first frame), and have each beat draw its first and last
frame from it, so a cut matches by construction: 013's `SC.SEAM`, 012
ep02's world kit and ep04's `DESK.SEAM`. A beat that only reads the table
in prose rebuilds its neighbour's state by hand and drifts.

What the kit owes its beats (013 ep04):
- `mount(root)` returns `draw` and every part a beat may animate (the
  readout, the axis names), so a beat never searches the DOM for them.
- Its `00_layout` cycles through every seam state, so every string the
  kit can show is on screen once before beats are built. ep04's baseline
  label was wired to a field `draw` never passed and showed nowhere.

Before rendering, check your beat's states against the table:
`node "$(git rev-parse --show-toplevel)"/tools/hf_state_check.js NN_beat FROM TO`
(from the video folder; FROM and TO are the seam numbers of your cuts). It
runs the page in Node, compares S(0), S(end) and the last 0.3 s with
`SEAM[FROM]` / `SEAM[TO]`, and names every field that differs. A field
under a part at opacity 0 isn't compared.

## Review

`check` must report 0 errors (the "file too large" warning and
`container_overflow` infos on a full-frame filtered SVG are expected).
Then open the contact sheet with the Read tool and look: text legible at
phone size, nothing in the dead zones, the band empty when there is VO,
one magenta hero, frame 0 populated, last frame still, duration within
1/30 s above `BEAT_SECONDS`, and the text in Inter (a fallback sans looks
narrower and lighter).

Frame 0 must be the previous beat's last frame. If its render exists
(`media/hf/<previous>.mp4`), grab the last frame and compare it with yours
side by side; if it does not exist yet, build from the brief and say in the
report which end state you assumed. Once a neighbour's render exists, run
`"$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json` from
the video folder and report every cut it flags, yours or not (012 ep01's
beat 3–4 agent caught the 4 → 5 cut this way); `--beat NN_beat` checks only
your own cuts. It compares
`hyperframes snapshot` PNGs, not mp4 frames: h264 noise around text reads as
a difference of up to ~60/255 where there is none, ep03).

Fix the smallest thing first: the attribute, then the element, then the
beat. Two review rounds. If the same kind of problem is still there after
the second, stop and report it with the element id and the line; do not
keep nudging.

## Report (the orchestrator reads only this)

Per beat: the cue constants with their VO word, the mp4 path and its
measured duration, the `check` summary (errors / warnings), anything
changed from the brief and why, and anything you wished existed (a part
to copy, a rule, a vendored weight). Do not commit. Temporary files go in
`<scratchpad>/<your agent name>/`: agents share one scratchpad, and 013
ep04's overwrote each other's check scripts.

## More of the toolbox

`agents/research/2026-10-03-hyperframes-ecosystem.md` lists the built-in
commands worth using (`inspect`, `snapshot`, `compare`, `keyframes`,
transparent WebM output, variables), the docs worth reading, and what to
leave alone (skills, publish, cloud, tts).
