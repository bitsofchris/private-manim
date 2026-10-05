# Beat brief: 010-diagram-grammar-iso

**Name:** diagram-grammar-iso-beat-brief
**Description:** The contract for rebuilding `videos/006-diagram-grammar`
("how to read an AI architecture diagram", 48.35 s) in the isometric
HyperFrames house style, over the same voice-over, cut and captions.
**When to use:** you were handed this path plus one or two beat numbers.
**How it works:** copy `00_layout/` (the canonical frame), build your beat as
a pure `render(t)` function with the two kits, check, render to `media/hf/`,
review your own contact sheet against the VO, report.

## Read first

1. `agents/beat-brief-hyperframes.md` — the technical rules, including "What
   `check` and the renderer trip on". All of it applies.
2. `videos/009-transformer-short-iso/_iso/iso.js` (linked into each beat as
   `iso/`) — the isometric kit: projection, palette, ground, `label`, `start`.
3. `videos/010-diagram-grammar-iso/_diagram/diagram.js` (linked as
   `diagram/`) — the figure: layout constants, `DG.draw(g, st)`, the path
   helpers, `DG.token`, `DG.makeLabels` / `DG.styleLabels`, `DG.canon`.
   Read all of it; its header comment states what the figure means.
4. `videos/010-diagram-grammar-iso/00_layout/index.html` — the starting file.
5. Your beat in `videos/006-diagram-grammar/` (`NN_name.py`): its docstring
   and cue constants say what each VO phrase must show. `storyboard.md` there
   has the "Final beats" table. The ideas carry over; the drawing is the
   isometric figure.
6. `videos/009-transformer-short-iso/` — a finished Short in this style, for
   how a beat file is organised (for example `06_stack/index.html`).

## Accuracy comes first (Chris's instruction)

This Short teaches how to read the figure, so the figure must stay correct
in every frame. In his words: "this should be factually accurate, so we're
still representing the symbols and direction used in the diagram."

- Flow is **bottom to top**: Embed at the bottom, Linear at the top; every
  main-line arrow points up; a token travels up. Never show anything flowing
  down the main line.
- The marks are the paper's marks: a **box** is an operation or layer; an
  **arrow** is a tensor moving to the next operation; a line that leaves the
  main line below a box and re-enters at the circle above it is the
  **residual (skip) path**; the **circle with a plus** is where it adds back
  in; the **bracket with N×** spans the repeated block (Attention, (+), FFN,
  (+)). Do not restyle a mark into something that no longer looks like the
  mark (no replacing the (+) with a different glyph, no arrowless lines for
  tensors, no bracket that spans other rows).
- Do not move, resize, re-order or relabel anything in `DG`: draw the figure
  with `DG.draw` and change only its state (`boxes`, `arrows`, `skips`,
  `adds`, `bracket`, `alpha`, `reveal`, `yOff`, `only`). Anything you add
  (a token, a tag, a band, a ghost copy) is an addition on top of a correct
  figure, positioned with `DG.pt` / the path helpers.
- Teal arrows are tensors. One magenta hero per beat: the mark the VO is
  naming. When the VO moves on, the mark returns to its resting colour.

## The canonical frame (continuity)

`CANON` is exactly `DG.canon(g, labels)` with `labels = DG.makeLabels(root)`
and nothing else on screen: the complete figure at rest.

| Beat | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on |
|---|---|---:|---:|---|---|
| 1 Hook | `01_hook` | 0.00 | 3.99 | (first frame of the Short) | `CANON` |
| 2 Grammar | `02_grammar` | 3.99 | 8.27 | `CANON` | `CANON` |
| 3 Box | `03_box` | 12.26 | 5.53 | `CANON` | `CANON` |
| 4 Arrow | `04_arrow` | 17.79 | 9.02 | `CANON` | `CANON` |
| 5 Residual | `05_residual` | 26.81 | 16.84 | `CANON` | `CANON` |
| 6 Repeat | `06_repeat` | 43.65 | 4.70 | `CANON` | free (last beat): still and finished |

The assembler hard-cuts between beats, so the first and last frames above
are binding. Something starts moving by frame 1 of every beat; the last
~0.3 s of every beat is still.

## Beats

**1 Hook** — "Here's how you can understand AI architecture diagrams like a
pro." Frame 0 already shows the whole figure (faint, e.g. `alpha` about
0.3) and it draws in bottom to top (`reveal`) at full strength, finishing
before the end. Nothing magenta. This is the first frame of the Short: it
has to read as a figure at a glance.

**2 Grammar** — "Now there's no formal standard, but there is a de facto
visual grammar. Almost every paper figure inherits it from Figure 1 in
Attention Is All You Need." Still through "no formal standard"; one pulse
of the whole figure on "visual grammar". On "almost every paper figure" the
real Figure 1 replaces ours: `videos/006-diagram-grammar/figure1_aiayn.png`
(1358 x 2000; copy it into your beat folder and load it as a DOM `<img>`,
styled in `render(t)`; laying it on the figure plane with the same shear as
the labels, `DG.SHEAR`, makes it a sheet of paper standing in the world). On
"Figure 1" it zooms to the decoder column (fractions of the image, x 0.52 to
0.90, y 0.06 to 0.88, as in 006's `02_grammar.py`). On "Attention Is All You
Need" our figure fades back in over it and the paper fades away. No hero.

**3 Box** — "A box is an operation or a layer. Linear, attention, feed
forward, et cetera." All four boxes are the hero on "box"; then each named
box pulses on its own word (Linear, Attention, FFN). Back to rest by the end.

**4 Arrow** — "An arrow is a tensor moving to the next operation. Flow is
always bottom to top, where input tokens are at the bottom and logits are at
the top." The five main-line arrows are the hero on "arrow". On "next
operation" a teal token (`DG.token`) hops one arrow, from one box into the
next. On "bottom to top" it rides the whole main line from the bottom of
Embed to the top of Linear (`DG.mainPoint`). "input tokens at the bottom" /
"logits at the top": mark the two ends (a pulse at each end is enough; a
flat tag only if it fits at 60 px without touching the figure).

**5 Residual** — "An arrow that bypasses a box is the residual path. The
circle with the plus is where it adds its new updated vector back in. That
vertical highway is the residual stream, and everything reads from it,
adding information back to it as we refine our representation through the
layers." The two skip paths are the hero on "bypasses"; the two (+) nodes
join them on "circle with the plus". A token splits below Attention: one
copy goes up through the box, the other goes around on the skip
(`DG.skipPath`, `DG.along`), and they merge at the (+) on "adds ... back
in". On "vertical highway" the hero hands off to a translucent magenta band
along the main line, bottom to top (the residual stream), and the skips and
(+) return to rest. "everything reads from it, adding information back": the
token rides up the stream, and at each box a copy dips through the box and
adds back at its (+). 16.84 s on one figure: land a visible change on every
phrase.

**6 Repeat** — "A bracket with N× means this block repeats N times." The
bracket and the `N×` label are the hero on "bracket". On "repeats", ghost
copies of the repeated block stamp out of it and stack back in depth
(`DG.draw(g, { only: "block", yOff: negative, alpha })`, drawn before the
main figure so they sit behind it; a negative `yOff` lands up and to the
right on screen, the skip side), like cards. The VO ends at about 3.7 s;
the last second is silence and the frame is held: ghosts stacked, bracket
magenta. This is the last frame of the Short.

## Rules specific to this video

- **Do not edit `_diagram/diagram.js`, `00_layout/`, or the kit in 009.**
  Need something they lack: write a local function and name it in the report.
- Set up a beat folder from the video folder:
  `mkdir NN_name && cp 00_layout/index.html NN_name/index.html && ln -s ../../_shared/web/vendor NN_name/vendor && ln -s ../../009-transformer-short-iso/_iso NN_name/iso && ln -s ../_diagram NN_name/diagram`.
  Keep the three `<script src>` lines and the literal
  `window.__timelines["main"] = ISO.start(BEAT_SECONDS, render);`. Set
  `data-duration` to your `BEAT_SECONDS`.
- Draw order each frame: `ISO.ground(g, DG.BASE_Y + 8)`, anything behind the
  figure, `DG.draw(g, st)`, anything in front (tokens), then
  `DG.styleLabels(labels, st)` with the same `st`.
- Stage y 230-1100, text and hero inside x 65-950; the band y 1100-1536
  stays empty (captions are burned in there). Flat text at least 60 px.
- Cues come from the audio: `videos/006-diagram-grammar/vo_final.wav`, your
  window is master start to start + `BEAT_SECONDS` (silencedetect or an RMS
  envelope); `videos/006-diagram-grammar/captions.json` has word-group
  times on the master timeline. Cues are named constants with the word in a
  comment.
- Commands, from your beat folder:
  ```
  export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
  npx --yes --prefer-offline hyperframes@0.8.115 check
  npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_name.mp4
  cd .. && ../../tools/review_frames.sh media/hf/NN_name.mp4 4 12 media/hf/NN_name_sheet.png
  ```
  Open the sheet with the Read tool. `check` must end "Check passed". Up to
  three render-and-review rounds per beat.
- Never run `hyperframes init / add / catalog / skills / publish / cloud /
  lambda / tts / transcribe / models` or any `npm install`. Do not commit.

## Report

Per beat: cue constants with their VO word, the mp4 path and measured
duration, the `check` result, the exact end state, anything changed from
this brief and why, any place the picture could be read as inaccurate about
the figure, and local helpers that should move into a kit.
