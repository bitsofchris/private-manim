# Beat brief for ep02-dataloader-explained (what every beat agent reads)

Read, in order: `agents/beat-brief-hyperframes.md` (the contract),
`storyboard.md` here (the Final beats table is the contract, the beats
table the visual brief, the seam-states table your first and last frames),
`_kit/seam.js` (this episode's `SC.SEAM`), the headers of
`../_kit/machine.js` and `../_kit/code.js` (the shared kit: the header
comments are the API), and `00_layout/index.html` (the starter).

Paths below are from this folder (`videos/014-pytorch-dataloading/ep02-dataloader-explained`).
The repo root is `$(git rev-parse --show-toplevel)`.

## Worked examples (same kit, already shipped)

`../ep01-training-loop/`: `01_hook_batch` and `10_check_batch` (machine
at rest, batch card pulse through `kit.parts.batch`), `04_loss_code` and
`08_epoch_code` (flip to the card, `SC_typedAt` typing, the hero line),
`09_one_batch` (flip back from the card to the machine, hero handoff).
Copy their pulse, typing and flip code where it fits; their cues and
seam numbers are not yours.

## Your folder is ready

`NN_beat/index.html` is a copy of `00_layout/index.html`; `vendor`, `kit`
and `ep` are linked. Keep the five `<script>` lines, the `@font-face` and
the `#root` styles exactly as they are. Write only `NN_beat/index.html`
(set its `data-duration` and `BEAT_SECONDS` to your Length). Do not edit
`_kit/`, `../_kit/`, `00_layout/`, `storyboard.md`, `beats.json` or
anything outside your beat folder. An episode-local helper you need
(e.g. beat 9's riding batch copy) lives inside your `index.html`. Do not
commit.

## The state model

One state object S per frame, drawn by `kit.draw(null, S)` where
`const kit = SC.mount(root)` (once). Set `SC.clock = START + t` before
each draw (master seconds drive the sample hop, continuous across cuts).
Build as `00_layout` does: `function render(t)`, then
`window.__timelines["main"] = SC.start(BEAT_SECONDS, render);` (that
literal line stays in `index.html`).

- Machine S: `{hero, workers, flip: 0}` over `SC.REST` (`mode "map"`,
  no strike, no twins, shape `[32, 512]`). `hero` is one of `dataset,
  sampler, fetch, batching, collate, batch, model` or null. At t ≤ 0 and
  through your still hold, return `SC.SEAM[n]` itself.
- `workers` is 0 | 1 | 2 (integer in the kit: worker 0 is half-faint at
  0). To grow a worker in over ~0.3 s, after `kit.draw` set the opacity /
  scale of the worker `<g>` yourself (find them as children of
  `kit.stations.fetch.glyph`), and restore exactly when the grow ends;
  the S field changes on the cue word.
- Pulses ("pulses once"): after `kit.draw`, transform the part's SVG
  elements (`kit.parts.NAME.svg`, each has `data-tint`) about their
  centre and its DOM labels (`kit.parts.NAME.dom`, `style.transform`);
  restore exactly when the pulse ends (`SC.pulse(t, at, 0.6)` gives the
  0..1 bump). The indices `7 2 5 0 3 1` are a DOM label in
  `kit.parts.sampler.dom`; `×32` is in `kit.parts.batching.dom`; the
  shape `[32, 512]` is in `kit.parts.batch.dom`.
- `S.flip` 0 → 1 crossfades machine → code card over 0.4 s (and 1 → 0
  back). `S.code = {o: 1, lines: SC.D.code.loader, typed, lit, cursor,
  blink}`; `typed = SC_typedAt(SC.D.code.loader, t − typeFrom, 30)`
  (cps 30: the storyboard's number). `lit` is the `lit` of the line being
  typed (dataset, batching, sampler, fetch); the kit tints the line whose
  `lit` matches. Keep `hero: "dataset"` under the card (SEAM[3]) so the
  flip back lands on the Dataset card lit.
- Helpers on `SC`: `seg(t,a,b)`, `lerp`, `clamp01`, `pulse(t, at, w)`,
  `E()` (eases: `io`, `out`, `inn`, `back`, `sine`; call `SC.E()` once).
- One magenta hero at a time. A sequence of heroes (beat 2's ripple) is
  one after another, never two at once.

## Cues (master seconds, from words.json; beat-local = master − Start; `|` = a cut)

In@0.64 PyTorch,@0.74 the@1.32 dataset's@1.40 job@1.84 hand@2.24 back@2.52 one@2.78 sample,@3.00 and@3.78 data@4.06 loader's@4.28 job@4.82 call@5.40 it@5.78 n@6.31 number@6.46 of@6.70 times@6.86 and@7.18 hand@7.36 back@7.56 a@7.78 batch.@7.92 |
The@8.72 data@8.82 loader@9.02 machine@9.48 with@9.86 four@10.08 different@10.38 stations,@10.64 |
and@11.18 every@11.24 argument@11.44 you@11.76 pass@11.86 one@12.30 those@12.58 stations.@12.72 Your@13.63 dataset@13.74 sits@14.06 at@14.40 front.@14.62 |
All@15.20 knows@15.48 go@16.08 get@16.22 one@16.48 sample@16.82 wherever@17.26 data@18.02 lives.@18.22 |
The@18.96 first@19.08 station@19.30 sampler.@19.88 It@20.56 decides@20.64 order.@21.18 Shuffle@22.10 equals@22.28 true@22.56 random@23.14 sampler,@23.46 a@24.26 random@24.32 sequence@24.74 of@25.16 indices.@25.28 |
Second@26.20 up@26.52 fetch.@26.80 Workers@27.45 call@27.91 dataset@28.30 indices@28.94 in@29.26 parallel@29.80 if@30.20 ask@30.52 them.@30.88 |
Third@31.47 batching.@31.87 It@32.40 collects@32.48 batch-sized@32.94 samples.@34.01 |
And@35.18 fourth@35.24 collate.@35.68 This@36.06 packs@36.36 them@36.80 into@37.02 one@37.28 tensor@37.56 shaped@37.90 for@38.30 GPU.@38.58 |
Out@39.66 comes@39.74 the@39.98 batch@40.12 and@40.38 what@40.48 goes@40.67 into@40.82 forward@41.16 pass.@41.44

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
your cut numbers (beat N opens on SEAM[N−1], ends on SEAM[N]). Look at
your own contact sheet with the Read tool. Once a neighbour's mp4 exists,
`uv run --no-sync python "$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json --beat NN_beat`
from this folder. Never run two renders at once in one folder (your own
beats: one after the other). Scratch files go in `<scratchpad>/<your agent name>/`.

Report per beat: cue constants with their word, mp4 path and measured
duration, the check summary, anything changed from the brief and why,
anything you wished the kit had.
