# Beat brief for ep01-training-loop (what every beat agent reads)

Read, in order: `agents/beat-brief-hyperframes.md` (the contract),
`storyboard.md` here (the Final beats table is the contract, the beats
table the visual brief, the seam-states table your first and last frames),
`_kit/loop.js` and `_kit/seam.js` (the episode kit; the header comments are
the API), `../_kit/machine.js` and `../_kit/code.js` headers (the shared
kit), and `00_layout/index.html` (the starter: copy its structure).

Paths below are from this folder (`videos/014-pytorch-dataloading/ep01-training-loop`).
The repo root is `$(git rev-parse --show-toplevel)`.

## Your folder is ready

`NN_beat/index.html` is a copy of `00_layout/index.html`; `vendor`, `kit`
and `ep` are linked. Keep the six `<script>` lines, the `@font-face` and
the `#root` styles exactly as they are. Write only `NN_beat/index.html`.
Do not edit any `_kit/`, `00_layout/`, `storyboard.md`, `beats.json`
or anything outside your beat folder. Do not commit.

## The state model

One state object S per frame, drawn by `kit.draw(null, S)` where
`const kit = SC.mount(root)` (once). Set `SC.clock = MASTER + t` before
each draw (master seconds drive the machine's sample flow; the loop
ignores it). Build your page as `00_layout` does: `function render(t)`,
then `window.__timelines["main"] = SC.start(BEAT_SECONDS, render);` (that
literal line must stay in `index.html`).

- `S.loop` fields (`_kit/loop.js`): `o`, `take` (always `"ring"`), `u`
  (position along the track, 0 = in the DataLoader's slot, wraps mod 1),
  `batch` (riding glyph opacity), `slot` (a waiting glyph in the slot),
  `lit` (`batch | loader | forward | loss | backward | update | step | track`).
  `LOOP.at("ring", NAME)` is the u where the glyph sits beside a box
  (`forward`, `loss`, `backward`, `update`) or in the slot (`loader`).
  The track runs slot → right gutter (past forward, loss, backward,
  update) → under update → left gutter back to the slot; u increases
  along it, so riding from forward to loss is u from `at("forward")` to
  `at("loss")`, and the return from update to the slot is u from
  `at("update")` to 1 (= 0).
- A loop beat spreads `SC.LOOP_ONLY` into S (machine off) and sets
  `loop: {o: 1, ...}`. Seam states are built with exactly that shape:
  read `_kit/seam.js` and return `SC.SEAM[n]` itself at t ≤ 0 / t ≥ HOLD.
- `S.flip` 0 → 1 crossfades machine (and loop) → code card over 0.4 s.
  `S.code = {o, lines: LOOP.CODE, typed, lit, cursor, blink}`;
  `SC_typedAt(LOOP.CODE, secondsSinceTypingStarted)` gives `typed`
  (human-paced; `SC_typingSeconds(LOOP.CODE)` is how long it takes). The
  line whose `lit` equals `S.code.lit` is the hero (a magenta gutter bar;
  `LOOP.CODE[i].lit` is outer/inner/forward/loss/backward/update).
- Machine beats (7, 8): S is `{hero, flip: 0, loop: {o: 0}}` over
  `SC.REST`; `hero` is `"model"` or `"batch"`. The machine has no scale
  field. A "pulse" of the batch card: after `kit.draw`, set a transform on
  the card's SVG elements through `kit.parts.batch.svg` (each has
  `data-tint`; the card's rect is at x 190, y 1000, w 410, h 90, so scale
  about its centre with `transform-origin`/`transform-box: fill-box` or a
  translate-scale-translate string) and on `kit.parts.batch.dom` (the
  label; use `style.transform`); restore them exactly when the pulse ends.
  "The four stations dim slightly then return": dip `S.loader` to ~0.7 and
  back over 0.6 s (the storyboard's own wording; the whole box dims, that
  is fine).
- Helpers on `SC`: `seg(t,a,b)` (0..1 clamp), `lerp`, `clamp01`,
  `pulse(t, at, w)` (a 0..1 sine bump), `E()` (eases: `io`, `out`, `inn`,
  `back`, `sine`; call `SC.E()` once after gsap loads).

Pulses the storyboard asks for ("the glyph pulses", "forward pulses
once", "the track pulses magenta once") are done through S: a short
`lit` swap (e.g. `lit: "track"` for 0.5 s then back to `"batch"`), or a
quick `batch` opacity dip-and-return. Do not reach into the DOM.

## Cues (master seconds, from words.json; beat-local = master − Start)

packed@2.26 tensor@3.00 parallelize.@4.18 | And@5.38 training@5.98 loop@6.26 one@7.24 batch.@7.38 |
The@8.26 yields@8.82 it,@9.18 forward@10.64 pass,@10.92 prediction.@12.18 |
We@12.96 compare@13.12 target,@14.30 loss.@15.12 |
The@15.94 backwards,@17.04 updated@18.34 descent.@19.58 |
That@20.32 one@20.76 training@21.12 step.@21.48 |
Then@22.28 go@22.42 back@22.54 next@23.64 batch.@23.88 |
An@24.66 epoch@24.80 dataset.@26.68 inner@27.97 loop@28.14 outer@30.12 loop@30.48 set.@32.22 |
The@33.0 model@33.08 one@35.82 batch@36.02 time.@36.46 |
check@38.22 batch@38.54 first.@38.74 |
Everything@39.64 four@41.38 lines@41.64 time.@42.14

## The code card, out of order

`S.code.typedLines = [n0, n1, ...]` (per-line character counts) replaces
`typed` when lines land out of order: beat 8 shows `LOOP.CODE` with
`typedLines = [h0, h1, Infinity, Infinity, Infinity, Infinity]` where
`h0`/`h1` come from `SC_typedAt(LOOP.CODE.slice(0, 2), seconds)` split
across the two headers; `cursorLine` says which row carries the cursor.
`S.code.lit` may be an array (`LOOP.STEP` lights the four body lines).
`LOOP.BODY` is the four-line card of beats 4 and 6.

## Crossfades between images

Machine ↔ card and loop ↔ card: `S.flip` (the kit's 0.4 s crossfade).
Machine ↔ loop (beat 2 only): no kit field; the beat lerps the machine's
four opacities (`dataset, loader, batch, model`) 1 → 0 and `loop.o`
0 → 1 over 0.4 s itself. A beat that flips to a card from the loop passes
the loop state through (as SEAM[n−1].loop) so the fade is the kit's.

The previous eight-beat build is in git at commit a343253
(`git show a343253:videos/014-pytorch-dataloading/ep01-training-loop/03_loss/index.html`
etc.: 01_hook, 02_forward, 03_loss, 04_backward, 05_next_batch,
06_epoch_code, 07_one_batch, 08_check_batch). Copy its ride, pulse and
flip code where it fits; the cues and seam numbers have all changed.

## Check, render, review (from your beat folder)

```
cd NN_beat
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
node "$(git rev-parse --show-toplevel)"/tools/hf_state_check.js . FROM TO   # from the episode folder: node .../hf_state_check.js NN_beat FROM TO
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
cd .. && "$(git rev-parse --show-toplevel)"/tools/review_frames.sh --at CUE1,CUE2 media/hf/NN_beat.mp4 4
ffprobe -v error -show_entries format=duration -of csv=p=0 media/hf/NN_beat.mp4
```

`hf_state_check.js` must pass (0 failing) before you render. FROM/TO are
your cut numbers (beat N opens on SEAM[N−1], ends on SEAM[N]). Look at
your own contact sheet with the Read tool. Once a neighbour's mp4 exists,
`uv run --no-sync python "$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json --beat NN_beat`
from the episode folder. Never run two renders at once in one folder.
Scratch files go in `<scratchpad>/<your agent name>/`.

Report per beat: cue constants with their word, mp4 path and measured
duration, the check summary, anything changed from the brief and why,
anything you wished the kit had.
