# Beat brief: 009-transformer-short-iso

**Name:** transformer-short-iso-beat-brief
**Description:** The contract for rebuilding `videos/005-transformer-short`
(the 59.27 s transformer Short) in the isometric HyperFrames style, house
palette, over the same voice-over, cut and captions. One `index.html` per
beat, all drawing with the shared kit `videos/_shared/web/iso/iso.js`.
**When to use:** you were handed this path plus one or two beat numbers.
**How it works:** copy `00_layout/` (the canonical frame), build your beat as
a pure `render(t)` function on the canvas plus flat DOM labels, check, render
to `media/hf/`, review your own contact sheet against the VO, report.

## Read first

1. `agents/beat-brief-hyperframes.md` — the technical rules (pure function of
   time, no network, no `Math.random`, no CSS animations, palette table, safe
   area, text floor, review loop). All of it applies.
2. `videos/_shared/web/iso/iso.js` — the kit. Read all of it.
3. `videos/009-transformer-short-iso/00_layout/index.html` — the starting
   file: it draws the canonical frame.
4. `videos/005-transformer-short/BRIEF.md` — the original Manim brief: your
   beat's VO phrases with beat-local times and what each phrase must show.
   The *ideas* carry over; the drawing is re-imagined in the isometric world.
5. `prototypes/hyperframes/stack-styles/13_iso_house/index.html` — the
   five-second prototype Chris liked (a tray dropping through ring slabs).

## The look (what Chris asked for)

An isometric world on the house navy with a faint floor grid. The matrix is a
physical tray of 3 x 3 extruded tiles coloured by token column
(`ISO.COL.tokens`: my teal, name blue, is gold; tall = large, a darker shade
= negative), and a flat readout card above it carries the words `my name is`
and the nine numbers in the same colours. Blocks and layers are solid slabs and rings the tray
passes through. Flat text only for things that must be read. One magenta hero
per beat (`ISO.COL.hero`): whatever is doing the work right now; when the beat
moves on it returns to teal, dim or slab colour.

Direction of flow is **down**: data falls through the model (input at the
top, output at the bottom), the opposite of the Manim diagram. Keep that in
every beat.

## The canonical frame (continuity)

`CANON(vals)` is exactly:

```js
ISO.ground(g); ISO.shadow(g, ISO.P2); ISO.tray(g, vals); card.set(vals);
```

with the card from `ISO.makeCard(root)` and nothing else on screen. The tray
never leaves its canonical spot (`ISO.TRAY_Y`) except where a beat below says
so, and it is the same object from beat 2 to the end: never fade-swap it.

| Beat | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on |
|---|---|---:|---:|---|---|
| 1 Hook | `01_hook` | 0.00 | 6.20 | (first frame of the Short) | the bird's-eye tower with the output tray below it |
| 2 Matrix | `02_matrix` | 6.20 | 9.08 | beat 1's last frame | `CANON(ISO.VALUES.embed)` |
| 3 Attention | `03_attention` | 15.28 | 13.82 | `CANON(embed)` | `CANON(embed)` + the magenta update column for "is" |
| 4 Residual | `04_residual` | 29.10 | 5.40 | beat 3's last frame | `CANON(ISO.VALUES.afterAttn)` |
| 5 Feed-forward | `05_ffn` | 34.50 | 11.45 | `CANON(afterAttn)` | `CANON(ISO.VALUES.afterFfn)` |
| 6 Stack | `06_stack` | 45.95 | 4.49 | `CANON(afterFfn)` | `CANON(ISO.VALUES.afterStack)` |
| 7 Head | `07_head` | 50.44 | 8.83 | `CANON(afterStack)` | free (last beat): still and finished |

A beat's first frame must be pixel-identical in layout to the previous beat's
last frame (the assembler hard-cuts between them), with something starting to
move by frame 1. A beat's last ~0.3 s is still.

## Beats (isometric re-imagining; VO times are in 005's BRIEF.md)

**1 Hook.** Bird's-eye view of the whole model as a tower, top to bottom: an
`Embed` slab, the block (an `Attention` ring and an `FFN` ring inside a frame
or bracket marked `N×`), and a dim `Linear` slab at the bottom. Flat labels
beside the parts. No card, no words `my name is` in this beat. "takes a
sequence of tokens": a small tray (digit-less, `VALUES.embed`) with a teal
`X` drops into Embed and a highlight travels down through Attention and FFN.
"updated representations": the tray comes out below the block, visibly
changed, labelled `X′`. "of those tokens": still. Nothing magenta.

**2 Matrix.** The zoom: the tower fades and the small output tray grows into
the canonical tray while the card with words and digits arrives (the values
may settle to `VALUES.embed` during the zoom). "vector of D numbers": one
token's line of three tiles is the hero (magenta) with a `d` tag. "L tokens":
the three token lines are marked with an `L` tag. "L by D matrix": the tray's
outline is drawn or pulses. "keeps that shape": tags go, outline pulses once.

**3 Attention.** Arcs rise over the tray from the `my` and `name` token lines
into the `is` line (width = `ISO.ATTN_WEIGHTS`, plus a small self loop).
"query": a `query?` tag on `is` (hero). "key": `key` tags on the other two
(dim or teal). "weighted sum": a flash runs along the arcs into `is` and a
magenta update column (three tiles, `ISO.VALUES.update`) builds in the lower
region. "match the key and query": arcs settle, tags fade. Ends with the
update column parked in the lower region below the `is` line.

**4 Residual.** "adds": a magenta `+`, and the update column rises onto the
`is` line: it is *added on top of* the existing tiles, not swapped in.
"existing representation": the `is` tiles and card digits tick to
`VALUES.afterAttn` as the update merges into them. "instead of replacing":
one brief ghost of the alternative (the old column sliding away, or a
struck-through `replace`) that does not happen.

**5 Feed-forward.** "works on each token alone": three separate small
machines, one per token line, with nothing joining them. Inside one, "which
combinations of features matter": a few connections light magenta;
"amplifying": one unit grows; "non-linearity": a ReLU kink glyph.
"depend on the input": the results feed back and every tile and digit ticks
to `VALUES.afterFfn`; the machines go.

**6 Stack.** The prototype, adapted: the tray stays canonical and three ring
slabs (`ISO.slabBack` / `ISO.slabFront`), numbered 1 2 3, travel *up* past it
(the same relative motion as the tray falling through three floors). The
slab the tray is inside glows magenta and the values tick one third of the
way from `afterFfn` to `afterStack` in each. Ends with the slabs gone.

**7 Head.** "final representations": the whole tray pulses. "not necessarily
predictions": hold. "output layer": a magenta `head` slab rises under the
tray. "turn these representations": the whole tray sinks into the head.
"whatever the training objective is asking for": the head lifts and `Chris`
comes out the other side, the one output, with a dim `next token` tag.

## Rules specific to this video

- **Do not edit `videos/_shared/web/iso/iso.js` or `00_layout/`.** Need something the kit lacks:
  write it as a local function in your beat and name it in your report.
- Set up a beat folder from the video folder:
  `mkdir NN_name && cp 00_layout/index.html NN_name/index.html && ln -s ../../_shared/web/vendor NN_name/vendor && ln -s ../../_shared/web/iso NN_name/iso`.
  Keep the two `<script src>` lines and the literal
  `window.__timelines["main"] = ISO.start(BEAT_SECONDS, render);` (the static
  lint needs it). Set `data-duration` to your `BEAT_SECONDS`.
- Everything visual is drawn in `render(t)`; flat text is DOM (`ISO.label`,
  `ISO.makeCard`) styled inside `render(t)` (opacity, transform, colour).
  Labels at least 60 px. Painter's order matters on the canvas: draw back to
  front.
- Stage for the visual: y 230-1100 (text and the hero inside x 65-950). The
  band y 1100-1536 stays empty: `tools/assemble.py` burns the captions there.
  The floor grid and background fill the frame.
- Cues come from the audio: `videos/005-transformer-short/vo_final.wav`, your
  window is master start to start + `BEAT_SECONDS` (silencedetect or an RMS
  envelope, as in `agents/beat-brief.md`); `videos/005-transformer-short/captions.json`
  has word-group times on the master timeline. Cues are named constants with
  the word in a comment.
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
duration, the `check` result, the exact end state (what is drawn, where),
anything changed from this brief and why, and local helpers that should move
into the kit.
