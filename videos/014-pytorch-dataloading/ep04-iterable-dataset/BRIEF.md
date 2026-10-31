# Beat brief for ep04-iterable-dataset (what every beat agent reads)

Read, in order: `agents/beat-brief-hyperframes.md` (the contract),
`storyboard.md` here (the Final beats table is the contract, the beats
table the visual brief, the seam-states table your first and last frames),
`_kit/ep4.js` and `_kit/seam.js` (the episode kit; the header comments are
the API), `../_kit/machine.js` and `../_kit/code.js` headers (the shared
kit), and `00_layout/index.html`.

Paths below are from this folder (`videos/014-pytorch-dataloading/ep04-iterable-dataset`).
The repo root is `$(git rev-parse --show-toplevel)`.

## Your folder is ready

`NN_beat/index.html` is a starter: the right `BEAT_SECONDS`, `MASTER`
(master seconds at t = 0), the six `<script>` lines, `EP4.mount`, and a
`render(t)` that holds SEAM[N−1] then SEAM[N]. `vendor`, `kit` and `ep` are
linked. Keep the `<script>` lines, the `@font-face`, the `#root` styles and
the `window.__timelines["main"] = SC.start(BEAT_SECONDS, render);` line
exactly as they are; replace the head comment with your cue plan. Write
only `NN_beat/index.html`. Do not edit any `_kit/`, `00_layout/`,
`storyboard.md`, `beats.json` or anything outside your beat folder. Do not
commit.

## The state model

One state object S per frame, drawn by `ep.draw(S)` (`EP4.mount(root)`,
once; it calls the machine's `draw` and then the shards). Set `SC.clock =
MASTER + t` before each draw (the sample flow is continuous across cuts).
Return `SC.SEAM[N−1]` itself at t = 0 and `SC.SEAM[N]` itself for the last
~0.3 s (the state check compares both, and `end − 0.3`).

- Machine fields (`machine.js` header): `mode` (`"iterable"` everywhere
  except beat 10's opening, which is `"map"`), `strike` 0..1, `workers`
  0|1|2, `hero` (`dataset`, `len`, `getitem`, `iter`, `sampler`, `fetch`,
  `batching`, `collate`, `batch`, `model`, or null), opacities `dataset`,
  `loader`, `batch`, `model`, `flip`, `code`.
- `S.shards` (`_kit/ep4.js`): `o`, `order`, `pos` (fractional slots while
  cards move), `load` 0..1, `loadCard`, `hero` 0|1. One magenta hero: when
  `shards.hero` is 1, machine `hero` is null.
- `S.stream` (`_kit/stream.js`, header is the API; beats 3, 5–7): the
  third image. Fields `o`, `src`, `flow`, `nosampler`, `ask`, `order`,
  `pos`, `lift`, `load`, `read`, `lanes`, `hero` (shards, memory, iter,
  next, loader, sampler, split). Stream seam states set the machine's
  opacities to 0; `stream.o` 1 → 0 crossfades to the machine (beat 8).
- `S.flip` 0 → 1 crossfades machine → code card over 0.4 s (the machine is
  gone by flip 0.6). Never both. A beat that changes hidden machine fields
  (beat 9: workers 2 → 0, shards off; beat 10: mode iterable → map, strike
  1 → 0) does it only while flip ≥ 0.6.
- `S.code = {o: 1, lines, typed, lit, cursor, blink}`; `SC_typedAt(lines,
  seconds, cps)` for `typed` (pass cps ~30–36 where the window is short;
  `SC_typingSeconds(lines, cps)` plans it). `typedLines` (per-line counts)
  when some lines are already there (beat 4: `[Infinity×4, n]`). Cursor on
  while typing, `cursor: 0` in the final seam state. `lit` names a line's
  `lit` (`EP4.ITER`: dataset, iter, yield; `EP4.LEN`: + len;
  `EP4.CMP`: iter, getitem).
- A "pulse": a hero swap to null and back over ~0.3 s, or an opacity dip
  (`shards.o` 1 → 0.5 → 1, `dataset` likewise). Do not reach into the DOM.
- Helpers on `SC`: `seg(t,a,b)`, `lerp`, `clamp01`, `pulse(t, at, w)`,
  `E()` (eases `io`, `out`, `inn`, `back`, `sine`; the starter calls it).
- Make the change land on the word: start a move ~0.1–0.2 s before the cue,
  arrive on it. Moves the viewer tracks ≥ 0.6 s.

## Cues (master seconds, from words.json; beat-local = master − MASTER)

01 If@0.70 sample@1.38 cheap,@1.86 iterable@2.76 dataset.@3.08 |
02 Here,@4.08 one@4.60 function,@4.80 iter,@5.36 yields@6.16 samples.@6.56 |
03 I@7.61 bigger@9.00 models.@9.20 pack@9.80 data@10.24 shards@10.62 stream@11.46 through.@11.94 |
04 There's@12.69 length@13.00 no@13.38 get item.@13.50 Sample@14.02 exist@15.08 iterator@15.88 produces@16.24 it.@16.56 |
05 This@17.24 no@17.76 sampler.@17.92 loader@18.60 calls@19.06 dataset@19.50 over@19.70 over@20.08 yields@20.54 next@20.98 sample.@21.20 |
06 So@22.02 shuffling@22.08 problem.@22.94 pre-shuffle@23.74 shards,@24.74 load@25.42 shard@25.82 memory,@26.16 yield@26.62 it.@27.04 |
07 Splits@27.58 problem,@28.47 multiple@29.42 workers,@29.72 splitting@30.30 stream@30.60 determine.@31.98 |
08 The@32.84 data@32.96 loader@33.16 same@34.18 though.@34.38 batch@35.16 size,@35.42 collate,@35.82 batch@36.40 out.@36.64 |
09 The@37.24 changes@37.68 asking@38.90 next@39.50 sample,@39.78 not@40.46 index@41.22 i.@41.52 |
10 So@42.32 map@42.60 can't,@43.18 day@43.84 cheap,@44.92 swap@45.38 iterable@45.92 dataset.@46.16

## Worked examples

ep 1's beats are the nearest: `../ep01-training-loop/04_loss_code/index.html`
(flip to the card and type to a cue), `../ep01-training-loop/08_epoch_code/index.html`
(`typedLines`, lines out of order), `../ep01-training-loop/09_one_batch/index.html`
(flip back to the machine, hero passing). Copy their flip and typing code;
the cue times and seam numbers here are different.

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

`hf_state_check.js` must pass (0 failing) before you render. FROM/TO:
beat N opens on SEAM[N−1], ends on SEAM[N]. Look at your own contact sheet
with the Read tool (the `--at` times are beat-local). Once a neighbour's
mp4 exists, `uv run --no-sync python "$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json --beat NN_beat`
from the episode folder. Never run two renders at once in one folder.
Scratch files go in `<scratchpad>/<your agent name>/`.

Report per beat: cue constants with their word, mp4 path and measured
duration, the check summary, anything changed from the brief and why,
anything you wished the kit had.
