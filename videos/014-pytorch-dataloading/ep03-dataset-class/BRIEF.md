# Beat brief for ep03-dataset-class (what every beat agent reads)

Read, in order: `agents/beat-brief-hyperframes.md` (the contract),
`storyboard.md` here (the Final beats table is the contract, the Beats
table the visual brief, the seam-states table your first and last frames,
the Cues line your cue times), `_kit/ep.js` and `_kit/seam.js` (the
episode kit; header comments are the API), `../_kit/machine.js` and
`../_kit/code.js` headers (the shared kit), and `00_layout/index.html`
(the starter: copy its structure).

Paths below are from this folder (`videos/014-pytorch-dataloading/ep03-dataset-class`).
The repo root is `$(git rev-parse --show-toplevel)`.

## Your folder is ready

`NN_beat/index.html` is a copy of `00_layout/index.html`; `vendor`, `kit`
and `ep` are linked. Keep the six `<script src>` lines, the `@font-face`
and the `#root` styles exactly as they are; set `data-duration` and
`BEAT_SECONDS` to your beat's Length. Write only `NN_beat/index.html`.
Do not edit `_kit/`, `../_kit/`, `00_layout/`, `storyboard.md`,
`beats.json` or anything outside your beat folder. Do not commit.

## The state model

One state object S per frame, drawn by `kit.draw(null, S)` where
`const kit = SC.mount(root)` (once). Set `SC.clock = START + t` before
each draw (START = your beat's master start; it keeps the machine's
sample flow continuous across cuts). Build as `00_layout` does:
`function render(t)`, then
`window.__timelines["main"] = SC.start(BEAT_SECONDS, render);` (that
literal line stays in `index.html`).

- At t = 0 your S must equal `SC.SEAM[N-1]`, and from `BEAT_SECONDS − 0.3`
  to the end it must equal `SC.SEAM[N]` exactly (build both from the
  SEAM objects themselves: `Object.assign({}, SC.SEAM[k], ...)`).
- Machine states: `{hero, flip: 0, code: {o: 0}}` over `SC.REST`. `hero`
  is one of `len, getitem, sampler, fetch, batching, collate, dataset` or
  null. Swapping `hero` on a cue word is the pulse/hand-off.
- Card states: `{flip: 1, hero: null, code: {o: 1, lines, typed, lit,
  cursor, blink}}`. `lines` is `EP.MAP` or `EP.HAND`; `lit` a name from
  those lines (`dataset, len, getitem, slice` / `sampler, batching,
  collate`), `EP.TWO` (both methods), or null. `typed: Infinity` = fully
  typed. Typing: `typed = SC_typedAt(lines, secondsSinceStart, cps)`;
  `SC_typingSeconds(lines, cps)` is how long it takes; `EP.litAt(lines,
  typed)` is the lit of the line being typed (the hero while typing).
  `blink: t` drives the cursor blink; at a seam the cursor is 0 except
  SEAM[0].
- The flip: `S.flip` 0 → 1 (machine → card) or 1 → 0 over 0.4 s, eased
  (`SC.E().io`). During a flip pass both the machine fields and the full
  `code` object, so the crossfade is the kit's. A beat that opens on a
  card and flips to the machine (5, 8) keeps `code` = the SEAM card's
  code during the flip, then `code: {o: 0}` once flip is 0. Set `hero`
  to the machine hero only once flip < 1 (at flip 1 the machine is
  hidden anyway, but S(0) must equal the SEAM card state with hero null).
- A DOM emphasis (beat 3's getitem swell, beat 6's index pulse): after
  `kit.draw`, set `style.transform = "scale(…)"` with
  `transformOrigin: "left center"` on `kit.parts.getitem.dom[0]` (the
  `__getitem__` label on the Dataset card) or the `7 2 5 0 3 1` index
  label, `kit.parts.sampler.dom.find(el => el.textContent ===
  SC.D.indices.join(" "))` (`dom[0]` is the station's name), via `SC.pulse(t, at, 0.6)`; set
  `transform` back to `""` when the pulse is 0, so the seam frame is the
  kit's own. ≤ 1.15× so nothing overlaps.
- Helpers on `SC`: `seg(t,a,b)`, `lerp`, `clamp01`, `pulse(t, at, w)`,
  `E()` (eases `io`, `out`, `inn`, `back`, `sine`; call once after gsap).

Cue times are master seconds in the storyboard's Cues line; beat-local =
master − START. Name them at the top: `const CUE = { slice: 18.16 - START /* "slice" */ };`.
Land each hero change on its word's start (or ~0.05 s before).
Monospace: the code card and kit labels already set it from script; if
you add any code text yourself, set `el.style.fontFamily = "monospace"`
from the script, on the element and every span.

## Check, render, review (from the episode folder unless noted)

```
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
node "$(git rev-parse --show-toplevel)"/tools/hf_state_check.js NN_beat FROM TO   # FROM = N-1, TO = N; must print 0 failing
cd NN_beat && npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4 && cd ..
"$(git rev-parse --show-toplevel)"/tools/review_frames.sh --at CUE1,CUE2 media/hf/NN_beat.mp4 4
ffprobe -v error -show_entries format=duration -of csv=p=0 media/hf/NN_beat.mp4
```

Look at your own contact sheet with the Read tool. Never run two renders
at once in one beat folder; if you own two beats, render them one after
the other. Once a neighbour's mp4 exists,
`uv run --no-sync --project "$(git rev-parse --show-toplevel)" python "$(git rev-parse --show-toplevel)"/tools/seam_check.py beats.json --beat NN_beat`
(note `--project`: plain `uv run --no-sync` from this folder lacks numpy).
Scratch files go in
`/private/tmp/claude-501/-Users-chris-repos-private-manim/6a55daac-414d-49ea-bfbe-9a0a314709c8/scratchpad/<your agent name>/`.

Report per beat: cue constants with their word, mp4 path and measured
duration, the check summary, the state-check result, anything changed
from the brief and why, anything you wished the kit had.
