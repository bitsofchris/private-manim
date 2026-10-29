# Beat brief for ep05-num-workers (what every beat agent reads)

Read, in order: `agents/beat-brief-hyperframes.md` (the contract),
`storyboard.md` here (the Final beats table is the contract, the beats
table the visual brief, the seam-states table your first and last frames),
`_kit/ep5.js` and `_kit/seam.js` (the episode kit; header comments are the
API), `../_kit/machine.js` and `../_kit/code.js` headers (the shared kit),
and `00_layout/index.html` (the starter: your `index.html` is a copy of it).

Worked examples in the sibling episode (same kit, same moves):
`../ep01-training-loop/04_loss_code/index.html` (flip to the card, typing,
hero following the typed line), `../ep01-training-loop/09_one_batch/` and
`10_check_batch/` (machine beats with a hero pass and a pulse),
`../ep01-training-loop/08_epoch_code/` (typing timed to cues).

Paths below are from this folder
(`videos/014-pytorch-dataloading/ep05-num-workers`). The repo root is
`$(git rev-parse --show-toplevel)`.

## Your folder is ready

`NN_beat/index.html` is a copy of `00_layout/index.html`; `vendor`, `kit`
and `ep` are linked. Keep the six `<script>` lines, the `@font-face` and
the `#root` styles exactly as they are; change the comment, `data-duration`,
`BEAT_SECONDS` and the render body. Write only `NN_beat/index.html`. Do not
edit `_kit/`, `../_kit/`, `00_layout/`, `storyboard.md`, `beats.json` or
anything outside your beat folder(s). Do not commit.

## The state model

- Mount once: `const kit = EP5.mount(root);` Draw every frame:
  `EP5.draw(kit, S)` (never `kit.draw` directly: `EP5.draw` lights both
  twin cards for hero `"twins"` and fits the 30-character iterable card).
- Set `SC.clock = MASTER_START + t` before each draw (the sample flow runs
  on master seconds so it is continuous across cuts).
- Build `S` from the seam states: start from `SC.SEAM[FROM]`, end exactly
  on `SC.SEAM[TO]` (return the object itself at t ≤ 0 and through the last
  ≥ 0.3 s). Fields (machine.js header): `mode` "map"|"iterable", `strike`
  0..1 (sampler struck), `workers` 2, `twins` 0..1 (the twin card slides
  in/out; at 0 the model chip is back), `shape` (always `SC.D.series.smallShape`),
  `hero`, `flip` 0..1, `code {o, lines, typed, lit, cursor, blink}`,
  opacities `dataset`, `loader`, `batch`, `model`.
- Flips: `flip` 0 → 1 (or back) over 0.4 s, starting on the cue word. The
  machine fields stay as the seam table says under the card; where the
  storyboard changes the machine under the card (beat 8: trap → fixed, i.e.
  `twins` 0, hero fetch), switch it only while `flip ≥ 0.6` (machine
  invisible).
- Typing: `typed = SC_typedAt(lines, t - typeFrom, cps)`; pick `cps` so
  the line the VO names lands on its cue (`SC_typingSeconds(lines, cps)`
  is the total). The hero follows the line being typed: as in 00_layout,
  walk the lines and take the `lit` of the last line with characters
  typed (a line whose `lit` is null keeps the previous one). Cursor 1 while
  typing, 0 at the seam. Lines: `EP5.LINES.iterable | workers | shard`.
  Beat 8 types only the first three shard lines (`typed` ends at
  `EP5.SHARD3`); beat 9 types the fourth from there.
- Mode change map ↔ iterable (beats 4, 5): `mode` is discrete; dip
  `S.dataset` 1 → 0.25 → 1 over ~0.5 s and switch `mode` at the bottom.
  `strike` and `twins` tween (≥ 0.6 s, eased with `SC.E()`).
- Pulses: after `EP5.draw`, scale an element about its centre and restore
  it exactly when the pulse ends. The twin cards: `kit.parts.batch.svg` /
  `kit.parts.twins.svg` (each card's rect is 410 × 90 at y 1000; x from
  `S.twins`, see machine.js `bX/twX`) and their `.dom` labels
  (`style.transform`). The two worker photocopies: the two `<g>` children
  of `kit.stations.fetch.glyph`; the kit rewrites their `transform`
  (`translate(x y)`) every draw, so append ` scale(s)` about the card centre
  (150 × 56) after drawing: `translate(x y) translate(75 28) scale(s) translate(-75 -28)`.
  Or do it through S with a quick hero/opacity swap. A pulse is ~0.5 s,
  `SC.pulse(t, at, w)`.
- Helpers on `SC`: `seg`, `lerp`, `clamp01`, `pulse`, `E()` (call once:
  `io`, `out`, `inn`, `back`, `sine`).

## Cues (master seconds, from words.json; beat-local = master − Start)

```
01_hook_twins start 0.000: In@0.74 PyTorch,@0.82 num_workers@1.56 doesn't@2.10 split@2.42 your@2.70 data@2.84 across@3.12 the@3.52 workers.@3.70
02_full_copy start 4.390: Each@4.76 worker@4.84 is@5.20 a@5.38 full@5.48 copy@5.80 of@6.16 your@6.30 dataset@6.40 fetching@6.74 and@7.12 collating@7.26 on@7.56 its@7.74 own.@7.88
03_same_data start 8.360: So@8.62 when@8.72 you@8.86 run@8.96 an@9.22 iterable@9.42 dataset@9.76 with@10.14 multiple@10.36 workers,@10.68 every@11.66 worker@11.90 gets@12.14 the@12.36 same@12.54 dataset@12.98 object@13.66 and@13.72 unless@13.98 you@14.22 split@14.30 the@14.62 stream@14.70 yourself,@14.92 they@15.24 all@15.40 deliver@15.72 the@15.96 same@16.12 data.@16.30
04_map_fine start 16.810: With@17.08 a@17.16 map-style@17.30 dataset,@17.72 you're@18.16 fine.@18.24 The@19.14 sampler@19.28 stays@19.62 in@19.96 the@20.08 main@20.20 process@20.38 and@20.94 hands@21.34 each@21.94 worker@22.22 a@22.44 different@22.58 set@22.82 of@23.00 indices.@23.14 Every@24.12 sample@24.34 here@24.66 gets@24.88 fetched@25.08 once.@25.38
05_no_indices start 25.910: But@26.16 with@26.24 an@26.38 iterable@26.54 dataset,@26.84 there@27.38 are@27.46 no@27.64 indices.@27.80 Each worker@28.88 starts@29.24 the@29.60 stream@29.84 from@30.00 the@30.18 beginning.@30.32 So@31.16 if@31.22 you@31.28 have@31.38 the@31.50 same@31.62 seed,@31.82 you're@32.18 getting@32.24 the@32.54 same@32.64 data.@32.80
06_true_code start 33.320: Two@33.58 workers,@33.74 batch@34.32 size@34.52 4,@34.74 the@35.20 first@35.28 two@35.54 batches@35.68 will@36.11 be@36.18 identical.@36.32
07_iter_fix start 37.020: The@37.30 fix@37.42 lives@37.64 inside@37.82 your@38.10 iter@38.34 function.@38.52
08_worker_info start 39.130: Ask@39.42 for@39.72 the@39.78 worker@39.92 info@40.30 and@41.38 have@41.46 worker@41.60 k@41.92 take@42.26 every@42.72 nth@42.90 sample,@43.26 starting@43.96 at@44.14 k.@44.33
09_false_code start 44.855: Now@45.17 the@45.52 two@45.72 copies@45.86 can@46.10 walk@46.30 the@46.55 stream@46.62 in@46.86 step@46.96 and@47.27 nothing@47.38 is@47.78 delivered@47.90 twice.@48.12
10_closer start 48.690: So@49.08 before@49.18 you@49.46 increase@49.82 num_workers@50.36 on@50.84 an@51.04 iterable@51.14 dataset,@51.40 be@52.30 sure@52.42 you're@52.60 passing@52.66 that@53.02 worker@53.24 info@53.46 to@53.80 each@54.00 iter@54.23 function@54.38 so@54.88 you@55.46 can@55.62 split@55.78 the@55.98 stream@56.14 accordingly.@56.42
```

"Each worker@28.88" is one entry: "Each" was dropped by the recognizer and
put back; the word "Each" starts near 28.70 (check the envelope).

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
your cut numbers (beat N opens on SEAM[N−1], ends on SEAM[N]). Look at your
contact sheet with the Read tool. Once a neighbour's mp4 exists,
`uv run --no-sync python "$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json --beat NN_beat`
from the episode folder. Never run two renders at once in one folder (each
agent renders only in its own beat folders). Scratch files go in
`<scratchpad>/<your agent name>/`.

Report per beat: cue constants with their word, mp4 path and measured
duration, the check summary, anything changed from the brief and why,
anything you wished the kit had.
