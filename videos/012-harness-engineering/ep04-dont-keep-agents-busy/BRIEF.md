# Beat brief: Harness ep 4, Stop Keeping Agents Busy

**Name:** harness-ep04-beat-brief
**Description:** The contract for the nine HyperFrames beats of "Is AI
Making Us Dumber? Stop Keeping Agents Busy" (47.49 s). Every beat draws
the one scene with the episode kit `_kit/desk.js` through one call,
`scene.draw(S, T)`, where `S` is a state object and `T` is MASTER time;
each beat opens on `DESK.SEAM[n-1]` and ends on `DESK.SEAM[n]`, so cuts
are exact by construction.
**When to use:** you were handed this path plus one or two beat numbers.
**How it works:** set up the folder, copy the template below, write `S(t)`
from the cues, check, render to `media/hf/`, review your own contact
sheet, report.

## Read first

1. `agents/beat-brief-hyperframes.md` (repo root): the technical rules
   (pure function of time, no network, no `Math.random`, palette, safe
   area, text floor, review loop, report format). All of it applies.
2. `_kit/desk.js`: the kit. Read all of it, especially the state fields at
   the top, `draw`, and `SEAM` / `START`.
3. `videos/_shared/web/cast/cast.js`: the figures (`CAST.pose`, `face`,
   `blink`, `hand`).
4. `storyboard.md`: the ledger and the beats table (your visual brief).
5. `00_layout/index.html` (the approved look) and `00_layout/layout.png`.

Never edit `_kit/`, `00_layout/`, another beat's folder, `videos/_shared/`,
`agents/`, or anything outside this episode folder. Need something the kit
lacks (a pose, a part)? Write a local helper in your `index.html` and name
it in the report. Do not commit.

## Set up (from the episode folder)

```
cd videos/012-harness-engineering/ep04-dont-keep-agents-busy
mkdir NN_beat && cd NN_beat
ln -s ../../../_shared/web/vendor vendor && ln -s ../../../_shared/web/iso iso
ln -s ../../../_shared/web/cast cast && ln -s ../_kit kit
```

Render from inside the beat folder, never two renders at once in one folder:

```
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
cd .. && ../../../tools/review_frames.sh media/hf/NN_beat.mp4 4
```

## Template (`NN_beat/index.html`)

Copy `00_layout/index.html` for the head and style (load order:
`vendor/gsap.min.js`, `iso/iso.js`, `cast/cast.js`, `kit/desk.js`), set
`data-duration` to `BEAT_SECONDS`, and make the script:

```js
(() => {
  const BEAT = 5, BEAT_SECONDS = 5.75;               // your beat number and length
  const T0 = DESK.START[BEAT];                       // master start
  const { seg, lerp, E, SEAM } = DESK;
  const A = SEAM[BEAT - 1], B = SEAM[BEAT];          // open on A, end on B
  const CUE = { plumb: 22.14 - T0 /* "writes" */ };  // beat-local, from words.json
  const HOLD_FROM = BEAT_SECONDS - 0.4;              // still from here (last beat: longer)
  const root = document.getElementById("root");
  const scene = DESK.mount(root);
  ISO.guides(root);
  function render(t) {
    const S = { /* build from A, B and the cues; every field at t=0 equals A, at HOLD_FROM equals B */ };
    scene.draw(S, T0 + t);                           // master time
  }
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = ISO.start(BEAT_SECONDS, render);
})();
```

## Rules for this episode

- **Seams.** At t = 0, `S` must equal `SEAM[n-1]` field for field; from
  `HOLD_FROM` on, it must equal `SEAM[n]`. Write a small `mix(A, B, u)` or
  set fields explicitly; any field present in one and missing in the other
  takes the kit default (`pile0` 6 — always pass 4; `ink` 1; `hero`/`dim`
  0; human pose `DESK.HUMAN_REST`).
- **Writing** is two fields: `write` (arm on the sheet, pencil shown) and
  `wiggle` (the pencil moving, reads the master time). Every seam has
  `wiggle` 0, so ramp it up (≥ 0.2 s) after t = 0 while the human writes
  and back to 0 before `HOLD_FROM`. Frame 0 still counts as moving when
  the wiggle starts within the first ~0.2 s.
- **flow** is the global page counter; keep it continuous: `flow` at t = 0
  is `A.flow`, at the end `B.flow`; in between drive it at whatever rate
  the VO wants (faster in beat 2–3). Page j lands `TRAVEL` (1.6) flow
  units after it leaves. When `stream` drops to 0, the pages in the air
  fade with it.
- **The agents** (`S.agents.rest` 1 = arms down, no tossing) and
  `S.agents.blink = [0|1, 0|1]` for a blink on a cue (a few frames).
- **One magenta hero at a time:** the hero column of the storyboard. The
  old hero goes back to its rest colour by a colour mix, ≥ 0.3 s.
- **Cues from the audio:** `words.json` (master times; subtract `T0`).
  A change lands on the word that names it. Moves ≥ 0.6 s.
- **No text** besides what the kit draws (code card, "today"). Captions
  carry the words; the band (y 1100–1536) stays empty.
- Every move stops before `HOLD_FROM`. Frame 0 has something moving
  (beat 1: the page stream; later beats: carry over the motion of the
  previous beat's end, e.g. the pencil).
- If the kit's drawing is wrong for your beat (a pose looks broken, a
  part overlaps), say so in the report with the element and the line;
  don't patch around it silently.

## Worked examples

- `00_layout/index.html`: the kit in three states.
- `videos/013-classifier-metrics/ep01-accuracy-trap/03_model_a/index.html`
  and its `_kit/score.js` `SEAM`: the same state-object / seam pattern on a
  different kit.
- `prototypes/hyperframes/cast/index.html`: figure poses driven by
  `seg` + easing in `render(t)`.
