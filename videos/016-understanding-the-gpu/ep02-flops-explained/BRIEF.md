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
- Chip: `lit` 0.32 at rest, 1 from beat 08's "thousands"; `title` "GPU"
  until beat 07's "B200", then "B200"; `hero` one name at a time.
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

A@0.40 FLOP@0.48 is@0.89 one@1.02 multiply or@1.32 one@2.10 add,@2.24 and@3.04 it's@3.10 the@3.25 unit@3.34 that@3.64 all@3.84 AI@4.08 compute@4.36 is@4.74 measured@4.90 in.@5.18 |
FLOP@5.92 stands@6.18 for@6.40 floating@6.62 point@7.08 operation.@7.36 |
Computers@8.66 store@9.04 decimals@9.28 as@9.72 a@9.92 floating@10.06 point,@10.36 scientific@11.04 notation@11.38 in@11.86 binary,@12.06 a@12.66 sign,@12.84 digits,@13.28 and@13.68 an@13.76 exponent.@13.86 |
The@14.85 point@14.92 floats,@15.31 so@16.18 one@16.28 format@16.56 holds@16.94 a@17.36 ten-millionth@17.96 and@18.74 three@19.32 million.@19.54 |
Every@20.40 weight,@20.54 activation,@20.92 and@21.50 gradient@21.58 is@21.78 one@22.08 of@22.26 these@22.38 numbers.@22.50 |
FLOPs@23.52 with@23.82 a@23.98 small@24.10 s@24.36 is@24.54 a@24.68 count.@24.80 Training@25.94 an@26.08 8@26.26 billion@26.48 parameter@26.68 model@27.12 on@27.50 15,000@27.70 tokens@28.50 costs@28.96 about@29.64 720@30.10 trillion@30.92 FLOPs.@31.52 |
FLOPS@32.62 with@32.86 a@33.02 capital@33.12 S@33.46 is@33.70 per@33.84 second.@34.06 This@34.60 is@34.72 a@34.82 rate.@34.98 A@35.76 B200@35.94 peaks@36.48 near@36.94 2,250@37.26 teraFLOPS@38.66 in@39.34 bf16.@39.52 Tera@40.84 is@41.04 a@41.22 trillion.@41.36 |
A@42.21 transformer's@42.32 compute@43.02 is@43.36 nearly@43.48 all@43.72 matrix@44.10 multiplies@44.46 and@45.10 a@45.42 matmul@45.50 is@45.88 only@46.02 multiplies@46.34 and@46.96 adds.@47.06 GPUs@47.88 are@48.60 built@48.68 to@48.92 do@49.12 exactly@49.22 that,@49.70 thousands@50.48 at@50.90 once.@51.08 |
Divide a@51.99 run's@52.32 FLOPs@52.54 by@53.24 the@53.42 FLOPS you@53.62 get,@54.52 and@54.82 you@55.06 have@55.18 GPU-hours.@55.60 This@56.98 is@57.14 the@57.22 bill.@57.36

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
