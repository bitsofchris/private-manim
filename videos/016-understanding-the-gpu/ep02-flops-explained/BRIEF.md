# Beat brief for ep02-flops-explained (what every beat agent reads)

Read, in order: `agents/beat-brief-hyperframes.md` (the contract),
`storyboard.md` here (the Final beats table is the contract, the Beats
table the visual brief, the seam-states table your first and last frames),
`_kit/seam.js` (this episode's `SC.SEAM`), `_kit/flops.js` (ep 2's top card
and float panel: the header is the API), the headers of `../_kit/chip.js`
and `../_kit/code.js` (the series kit: the header comments are the API),
and `00_layout/index.html` (the starter). `00_layout/takes.png` and
`states.png` show every seam state as rendered.

Paths below are from this folder (`videos/016-understanding-the-gpu/ep02-flops-explained`).
The repo root is `$(git rev-parse --show-toplevel)`.

No 016 beat has shipped yet. For typing and pulse code, look at
`../../014-pytorch-dataloading/ep02-dataloader-explained/04_dataset` … `09_out`
(same HyperFrames idiom, a different kit); their cues and seam numbers are
not yours.

## Your folder is ready

`NN_beat/index.html` is a copy of `00_layout/index.html`; `vendor`, `kit`
and `ep` are linked. Keep the six `<script src>` lines, the `@font-face`
and the `#root` styles exactly as they are. Write only `NN_beat/index.html`
(set its `data-duration` and `BEAT_SECONDS` to your Length, and replace the
header comment with your beat's). Do not edit `_kit/`, `../_kit/`,
`00_layout/`, `storyboard.md`, `beats.json` or anything outside your beat
folders. A helper only your beat needs lives inside your `index.html`. Do
not commit.

## The state model

One state object S per frame, drawn by `kit.draw(S)` where
`const kit = EP.mount(root)` (once). Set `SC.clock = START + t` before each
draw (master seconds: the lit-cell shimmer runs on across cuts). Build as
`00_layout` does: `function render(t)`, then
`window.__timelines["main"] = SC.start(BEAT_SECONDS, render);` (that literal
line stays in `index.html`).

- Every S is `SC.SEAM[n]`-shaped: `cpu 0, queueO 0, strip 0, shimmer 1`
  always (the CPU, its queue and the time strip are off all episode). At
  t ≤ 0 return `SC.SEAM[N−1]` itself; through your closing still hold,
  return `SC.SEAM[N]` itself.
- Top card: `card = {o: 1, A, B, mix}`. To change content, put the old
  content in A, the new in B, and run `mix` 0 → 1 over ~0.3 s; once done,
  move to `{A: new, B: null, mix: 0}` (identical pixels). Fields of each
  kind are in the flops.js header.
- Float panel: `float = {o, grow, row1, row2, glide1, glide2, anat, anatO, lab}`.
  `grow` 0 → 1 grows it out of cell (row 5, col 5) over the chip and
  memory; while it is fully grown the kit hides memory itself. `glide1/2`
  0..1 move each row's point; `anat` 1|2 picks the anatomy numbers
  (`+ 1.0 −7` | `+ 3.0 6`), `anatO` their opacity, `lab [s, d, e]` the
  three labels' opacities. Hero names `sign`, `digits`, `exp`, `point`.
- Code card (beats 06–08): `code = {o, lines: SC.D.code.flops, typed, lit, cursor, blink, cy: 1245}`.
  Only line 1 (`flops = 6 * 8e9 * 15_000  # 7.2e14`) is used: pass
  `lines: SC.D.code.flops` and cap `typed` at `SC.D.code.flops[0].t.length`
  (line 2 never shows). `typed = Math.min(L1, SC_typedAt(lines, t − typeFrom, cps))`;
  pick cps so line 1 lands by "720" (30.10). `cy: 1245` always (the card
  bottom must stay at or above y 1330: captions sit under it).
- Core view (v2): `core = {o, grow, mode, ...}`, the same panel and grow as
  the float panel. `mode "op"` (beat 01): `mul`, `carry`, `add` 0..1 and
  the counter `n`, `lit` "mul"|"add"|null. `mode "dot"` (beat 08): `step`
  0..3, the counter and y follow from it. Hero "count" is the counter,
  "expr" the dot's running line. While a panel is fully grown the kit hides
  memory itself.
- Acronym: `acro = {o, u}`; u 0 is `FLOP`, u 1 FLOATING-POINT / OPERATION
  (the letters glide in u 0–0.6, the rest types in 0.45–1). Hero "acronym".
  While `acro` is on, `card.A` is null (the card background only).
- Stream: `stream = {o, phase}`; phase is seconds (pass beat time). Off at
  every seam.
- Count card: `{kind: "count", o2, v}`; while `v < 1` row 2 is the rolling
  count, at v 1 (or no v) `720 trillion = 7.2 × 10¹⁴`.
- Rate card: `{kind: "rate", clock, clockO}`; the 1 s clock at the card's
  right, hero "clock".
- Chip: `lit` 0.32 at rest, 1 from beat 08's "thousands"; `title` stays
  "GPU" (no B200 any more); `hero` one name at a time.
- Helpers on `SC`: `seg(t,a,b)`, `lerp`, `clamp01`, `pulse(t, at, w)` if
  present, `E()` (eases; call once) if present — check chip.js before you
  use one; write a 2-line ease inline otherwise.
- One magenta hero at a time: the thing the VO names. Teal is working,
  grey idle. A sequence of heroes is one after another, never two at once.
- Text floor 60 px, weight 800. Mono spans come from the kit
  (`fontFamily: monospace`); any code text you add yourself must set it too.
- No numbers outside the ledger (storyboard.md "Ledger"). "FLOPs" is the
  count, "FLOPS" the rate.

## Cues (master seconds, from words.json; beat-local = master − Start; `|` = a cut)

The VO lost "A B200 peaks near 2,250 teraFLOPS in bf16. Tera is a trillion."
(cut 35.50–41.98); everything from beat 08 on moved 6.48 s earlier.

A@0.40 FLOP@0.48 is@0.89 one@1.02 multiply or@1.32 one@2.10 add,@2.24 and@3.04 it's@3.10 the@3.25 unit@3.34 that@3.64 all@3.84 AI@4.08 compute@4.36 is@4.74 measured@4.90 in.@5.18 |
FLOP@5.92 stands@6.18 for@6.40 floating@6.62 point@7.08 operation.@7.36 |
Computers@8.66 store@9.04 decimals@9.28 as@9.72 a@9.92 floating@10.06 point,@10.36 scientific@11.04 notation@11.38 in@11.86 binary,@12.06 a@12.66 sign,@12.84 digits,@13.28 and@13.68 an@13.76 exponent.@13.86 |
The@14.85 point@14.92 floats,@15.31 so@16.18 one@16.28 format@16.56 holds@16.94 a@17.36 ten-millionth@17.96 and@18.74 three@19.32 million.@19.54 |
Every@20.40 weight,@20.54 activation,@20.92 and@21.50 gradient@21.58 is@21.78 one@22.08 of@22.26 these@22.38 numbers.@22.50 |
FLOPs@23.52 with@23.82 a@23.98 small@24.10 s@24.36 is@24.54 a@24.68 count.@24.80 Training@25.94 an@26.08 8@26.26 billion@26.48 parameter@26.68 model@27.12 on@27.50 15,000@27.70 tokens@28.50 costs@28.96 about@29.64 720@30.10 trillion@30.92 FLOPs.@31.52 |
FLOPS@32.62 with@32.86 a@33.02 capital@33.12 S@33.46 is@33.70 per@33.84 second.@34.06 This@34.60 is@34.72 a@34.82 rate.@34.98 |
A@35.73 transformer's@35.84 compute@36.54 is@36.88 nearly@37.00 all@37.24 matrix@37.62 multiplies@37.98 and@38.62 a@38.94 matmul@39.02 is@39.40 only@39.54 multiplies@39.86 and@40.48 adds.@40.58 GPUs@41.40 are@42.12 built@42.20 to@42.44 do@42.64 exactly@42.74 that,@43.22 thousands@44.00 at@44.42 once.@44.60 |
Divide a@45.51 run's@45.84 FLOPs@46.06 by@46.76 the@46.94 FLOPS you@47.14 get,@48.04 and@48.34 you@48.58 have@48.70 GPU-hours.@49.12 This@50.50 is@50.66 the@50.74 bill.@50.88

Some words.json starts sit 0.06–0.2 s early (the end of the word before);
v1's agents checked onsets on vo_final.wav's envelope, and so may you.

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
must show 0 errors; a lint waiver (`data-layout-allow-occlusion`,
`-overlap`, `-overflow`) only where the overlap is the design, said in
your report. Look at your own contact sheet with the Read tool and fix
what it shows. Once a neighbour's mp4 exists,
`uv run --no-sync --project "$(git rev-parse --show-toplevel)" python "$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json --beat NN_beat`
from this folder. Never run two renders at once in one folder (your own
beats: one after the other). Scratch files go in `<scratchpad>/<your agent name>/`.

Report per beat: cue constants with their word, mp4 path and measured
duration, the check summary, anything changed from the brief and why,
anything you wished the kit had.
