# Beat brief for ep03-six-flops-per-parameter (what every beat agent reads)

Read, in order: `agents/beat-brief-hyperframes.md` (the contract),
`storyboard.md` here (the Final beats table is the contract, the Beats
table the visual brief, the seam-states table your first and last frames),
`_kit/seam.js` (this episode's `SC.SEAM`), `_kit/layer.js` (ep 3's tiny
layer, matrix, FLOP bar and readout: the header is the API), `_kit/ep.js`
(every episode string), the headers of `../_kit/chip.js` and
`../_kit/code.js` (the series kit), and `00_layout/index.html` (the
starter). `00_layout/layout.png` shows frame 0 and every seam state as
rendered.

Paths below are from this folder (`videos/016-understanding-the-gpu/ep03-six-flops-per-parameter`).
The repo root is `$(git rev-parse --show-toplevel)`.

Worked examples on the same series kit: `../ep02-flops-explained/06_count`
… `09_bill` (code-card typing, chip title change, hero hand-off) and
`../ep01-why-gpus-for-ai/06_code`. Copy their idioms; their cues and seam
numbers are not yours.

## Your folder is ready

`NN_beat/index.html` is a copy of `00_layout/index.html`; `vendor`, `kit`
and `ep` are linked. Keep the seven `<script src>` lines, the `@font-face`
and the `#root` styles exactly as they are. Write only `NN_beat/index.html`
(set its `data-duration` and `BEAT_SECONDS` to your Length, and replace the
header comment with your beat's). Do not edit `_kit/`, `../_kit/`,
`00_layout/`, `storyboard.md`, `beats.json` or anything outside your beat
folders. A helper only your beat needs lives inside your `index.html`. Do
not commit.

## The state model

One state object S per frame, drawn by `kit.draw(S)` where
`const kit = SC.mount(root)` (once; `SC.mount` is ep 3's wrapper from
`_kit/layer.js`, which draws the chip and the layer). Set
`SC.clock = START + t` before each draw (master seconds: the run pulses
and the chip shimmer carry on across cuts). Build as `00_layout` does:
`function render(t)`, then
`window.__timelines["main"] = SC.start(BEAT_SECONDS, render);` (that
literal line stays in `index.html`).

- S = chip fields + `S.ly` (layer fields, all in the layer.js header).
  Build each frame's S from `SC.SEAM[n]` with `Object.assign` (00_layout's
  `ly(n, extra)` helper shows how). At t ≤ 0 return `SC.SEAM[N−1]` itself;
  through your closing still hold (≥ 0.3 s), return `SC.SEAM[N]` itself.
- The layer's moves are fields, not DOM tweens: `pass` + `prog` (0..6)
  runs a pass over the six lines in order w11 w12 w13 w21 w22 w23, with a
  rider glyph `×` for the first half of each line and `+` for the second;
  `bar.f` fills segments; `rd.text` is the readout (`EP.count(n)`);
  `flash k` draws line k and its cell as the hero; `bumpIn` / `bumpOut`
  swell the dots; `mat.fill` fills dW cells; `shrink` 0..1 shrinks the
  whole layer group into one chip cell (beat 07). Label changes
  (`inLab`, `outLab`, `eq.text`, `mat.name`) are hard swaps in the state:
  cross-fade them yourself after `kit.draw` (each part is in
  `kit.parts`, layer.js's `mountLayer` return) if a swap looks abrupt,
  and restore exactly when the fade ends.
- Chip fields (beats 07–08): see `SC.SEAM[7]` / `[8]`. Code card:
  `code = {o: 1, lines: SC.D.code.sixN, typed, lit, cursor, cy: 1246}`;
  `typed = SC_typedAt(lines, t − typeFrom, cps)`. `cy: 1246` always (the
  card's bottom stays at y 1330: captions sit under it).
- Helpers on `SC`: `seg(t,a,b)`, `lerp`, `clamp01`, `hash`. No ease
  helper: write a two-line ease inline.
- One magenta hero at a time: the thing the VO names (storyboard's hero
  per beat). Teal is working, grey idle. A sequence of heroes is one after
  another, never two at once.
- Text floor 60 px, weight 800. Code text is the kit's (monospace set
  from the script); any code text you add yourself must set
  `el.style.fontFamily = "monospace"` on it and every span inside.
- No numbers outside the ledger (storyboard.md "Ledger"). "FLOPs" is the
  count, "FLOPS" the rate. No strings outside `_kit/ep.js` / `../_kit/data.js`;
  if you need one, say so in the report and inline it for now.

## Cues (master seconds, from words.json; beat-local = master − Start; `|` = a cut)

Training@0.41 an@0.70 LLM@0.82 costs@1.28 about@1.68 6@1.88 FLOPs@2.30 per@2.64 parameter@2.92 per@3.44 token.@3.70 You@4.57 spend@4.60 2@4.92 FLOPs@5.24 on@5.68 the@5.94 forward@6.06 pass@6.28 and@6.58 about@6.68 4@6.88 on@7.26 the@7.46 backward@7.58 pass.@7.93 |
Almost@9.14 every@9.26 parameter@9.50 sits@9.84 in@10.18 a@10.28 weight@10.38 matrix.@10.58 Here's@11.58 a@11.66 tiny@11.78 one,@12.00 3@12.35 inputs,@12.48 2@12.87 outputs,@12.98 6@13.40 weights.@13.62 |
Going@14.40 forward,@14.66 each@15.16 weight@15.36 does@15.68 one@15.84 multiply@16.16 and@16.68 one@16.86 add.@17.04 So@17.92 you@17.98 have@18.00 2@18.15 FLOPs@18.30 per@18.64 weight,@18.78 12@19.22 for@19.38 this@19.52 entire@19.68 layer.@20.00 |
Coming@20.73 backwards@20.90 now,@21.24 the@21.50 error@21.60 has@21.94 to@22.16 reach@22.32 the@22.54 layer@22.70 before.@22.84 So@23.74 the@23.80 same@23.96 weights@24.16 in@24.38 reverse,@24.48 another@25.00 multiply@25.18 and@25.94 add@26.00 each.@26.22 |
Then@27.02 each@27.14 weight@27.32 needs@27.54 its@27.74 own@27.92 gradient@28.12 for@28.50 the@28.84 optimizer.@29.00 Error@29.96 times@30.20 input@30.50 added@30.80 to@31.30 a@31.48 running@31.56 total@31.72 is@32.08 2@32.42 more.@32.60 |
That's@33.28 6@33.50 per@33.72 weight@33.88 per@34.17 token.@34.24 |
So@35.14 training@35.30 compute@35.66 is@36.38 6@36.56 times@36.94 parameters@37.44 times@38.04 tokens.@38.28 |
An@39.14 8@39.30 billion@39.51 parameter@39.74 model@40.22 at@40.56 15,000@40.81 tokens@41.38 per@41.68 second@41.84 per@42.14 GPU@42.34 is@42.68 doing@42.97 720@43.14 teraflops.@43.96

Beat starts: 01 0.000 · 02 8.660 · 03 14.160 · 04 20.485 · 05 26.740 ·
06 33.040 · 07 34.890 · 08 38.960.

## Check, render, review (from your beat folder)

```
cd NN_beat
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
node "$(git rev-parse --show-toplevel)"/tools/hf_state_check.js . FROM TO
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
cd .. && "$(git rev-parse --show-toplevel)"/tools/review_frames.sh --at CUE1,CUE2 media/hf/NN_beat.mp4 4
ffprobe -v error -show_entries format=duration -of csv=p=0 media/hf/NN_beat.mp4
```

`hf_state_check.js` must pass (0 failing) before you render. FROM/TO are
your cut numbers (beat N opens on SEAM[N−1], ends on SEAM[N]). `check`
must show 0 errors; a lint waiver only where the overlap is the design,
said in your report. Look at your own contact sheet with the Read tool and
fix what it shows. Once a neighbour's mp4 exists,
`uv run --no-sync --project "$(git rev-parse --show-toplevel)" python "$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json --beat NN_beat`
from this folder. Never run two renders at once in one folder (your own
beats: one after the other). Scratch files go in `<scratchpad>/<your agent name>/`.

Report per beat: cue constants with their word, mp4 path and measured
duration, the check summary, anything changed from the brief and why,
anything you wished the kit had.
