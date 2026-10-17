# Beat brief: 013 ep03, the threshold and the ROC curve

**Name:** classifier-ep03-beat-brief
**Description:** The contract for the nine HyperFrames beats of "ROC curve
explained" (42.10 s). Every beat draws with the episode kit
`_kit/score.js` through one call, `K.draw(g, S)`, where `S` is a state
object; each beat opens on `SC.SEAM[n-1]` and ends on `SC.SEAM[n]`, so
cuts are exact by construction.
**When to use:** you were handed this path plus one or more beat numbers.
**How it works:** copy the template below into your beat folder, write
`S(t)` from the cues, check, render to `media/hf/`, review your own
contact sheet, report.

## Read first

1. `agents/beat-brief-hyperframes.md` (repo root): the technical rules
   (pure function of time, no network, no `Math.random`, palette, safe
   area, text floor, review loop, report format). All of it applies. One
   exception, below: the stage runs to y 1330.
2. `_kit/score.js`: the kit. Read all of it, especially the `S` fields
   above `mount`, `box(t)`, `roc`, and `SEAM`.
3. `storyboard.md`: the ledger and the beats table (the visual brief).
4. `00_layout/index.html` (the approved look) and `00_layout/frame.png`.
5. A worked example of this kit's family: `../ep01-accuracy-trap/BRIEF.md`
   and any finished `../ep01-accuracy-trap/0N_*/index.html` (same driver,
   same state-object pattern). Read only; never edit ep01.

Never edit `_kit/`, `00_layout/`, another beat's folder, `videos/_shared/`
or anything outside this episode folder. Need something from the kit (a
new state field, a part)? Write a local helper in your `index.html` (for
example draw an extra canvas layer after `K.draw`), and name it in the
report.

## Layout facts

- Captions are burned with `assemble.py --captions-anchor bottom`, so the
  stage runs to **y 1330**. Nothing of yours goes below 1330.
- Every count on screen comes from `SC.box(t)` (the dots' own scores; it
  reproduces the ledger stops exactly). Never type a number. Threshold
  values you move to are the ledger stops `SC.STOPS` = 0.20, 0.40, 0.55,
  0.70, 0.85 (and the score of the tagged dot in beat 4).
- **Hero:** the threshold line and its ROC dot are one magenta group (move
  one, the other moves). The stop points in beat 7 belong to that group.
  The curve is magenta only in beat 3 (`curve.hero`), the corner only in
  beat 8. While something else is the hero, the line and dot rest
  (`thr.dim`, `dot.dim`). A box cell being named uses `boxHi` (white, not
  magenta).
- The code line's number is always `t` (2 dp). `code.hero` lights `> t`
  magenta; while it's lit, `thr.dim` the line (one hero).
- A move the viewer tracks: ≥ 0.6 s, `E.io` easing. When the line slides
  between stops, ease the *score* `t` (counts tick with it for free).

## Template (copy to `NN_beat/index.html`)

Start from `00_layout/index.html` and replace its script body with:

```js
(() => {
  const BEAT_SECONDS = 0.0;            // from the table
  const MASTER = 0.0;                  // master start, from the table
  const CUE = { /* word: master − MASTER, from words.json */ };
  const root = document.getElementById("root"), g = document.getElementById("scene").getContext("2d");
  const { seg, lerp, pulse, SEAM } = SC, E = SC.E();
  const K = SC.mount(root);
  function S(t) { /* build the state; S(0) deep-equals SEAM[n-1], S(end) deep-equals SEAM[n] */ }
  function render(t) { K.draw(g, S(t)); }
  const tl = gsap.timeline({ paused: true, onUpdate: () => render(tl.time()) });
  tl.to({ p: 0 }, { p: 1, duration: BEAT_SECONDS, ease: "none" }, 0);
  tl.set({}, {}, BEAT_SECONDS);
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = tl;
  tl.seek(0); render(0);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => render(tl.time()));
})();
```

and set `data-duration` on `#root` to `BEAT_SECONDS`. "Deep-equals" means
the drawn frame is identical: a field at its default (0, or absent) is the
same as absent. The folder already has its two symlinks (`kit`,
`vendor`). Render from the beat folder:

```
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
```

Contact sheet from the episode folder:
`../../../tools/review_frames.sh media/hf/NN_beat.mp4 4`.

Canvas-only motion fails `check`'s `sweep_static`: give each beat one
honest DOM change (a label that swells when named; the code number
ticking; a box count changing). Frame 0 must be `SEAM[n-1]` exactly;
something moves by frame 1 or soon after the first cue; the last ~0.3 s
is still and equals `SEAM[n]`.

## The beats

Master times in `vo_final.wav`. Word starts (master s) from `words.json`;
check the ones that matter on the envelope of your window.

| # | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on | Hero |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 3.00 | (first frame of the Short) | `SEAM[1]` | line + dot |
| 2 | `02_context` | 3.00 | 3.50 | `SEAM[1]` | `SEAM[2]` | line + dot |
| 3 | `03_every_place` | 6.50 | 3.15 | `SEAM[2]` | `SEAM[3]` | the curve |
| 4 | `04_score` | 9.65 | 5.95 | `SEAM[3]` | `SEAM[4]` | line, then `> 0.70` |
| 5 | `05_slide_left` | 15.60 | 4.55 | `SEAM[4]` | `SEAM[5]` | line + dot |
| 6 | `06_slide_right` | 20.15 | 4.20 | `SEAM[5]` | `SEAM[6]` | line + dot |
| 7 | `07_each_point` | 24.35 | 7.50 | `SEAM[6]` | `SEAM[7]` | the stop points (with the line) |
| 8 | `08_sweet_spot` | 31.85 | 1.90 | `SEAM[7]` | `SEAM[8]` | the corner |
| 9 | `09_takeaway` | 33.75 | 8.35 | `SEAM[8]` | `SEAM[9]` (last frame of the Short, still) | line + dot |

**1 Hook** — "You can change what your classifier does without retraining
it." (You 0.45, change 0.66, classifier 1.22, retraining 2.18, it 2.62.)
Frame 0 is the finished picture already moving (the hook rule): the line
mid-slide. `t` starts at 0.55 and eases to 0.70 by ~"retraining" (≥ 1.2 s;
counts tick, the ROC dot rides the curve). Still from ~2.7 s at
`SEAM[1]`. Optional: one `dot.pulse` as it lands.

**2 Context** — "It's a prompt injection detector. You just move this
line." (It's 3.18, prompt 3.38, detector 4.16, move 5.35, this 5.62, line
5.90.) "prompt injection detector": `tagBright` 0→1→0 (back by ~4.9).
"move this line": `t` 0.70 → 0.62 → 0.70, each leg ≥ 0.6 s, eased; a
`thr.pulse` on "line" is fine. Ends `SEAM[2]`.

**3 Every place** — "An ROC curve shows every place that you could put
it." (ROC 6.82, curve 7.20, shows 7.46, every 8.12, place 8.48, put 9.12.)
"ROC curve": `curve.hero` 0→1 (the curve takes the hero; `thr.dim` and
`dot.dim` → ~0.6 meanwhile). "every place": `t` sweeps 0.70 → ~0.95 → 0.20
→ 0.70 (or a simpler right→left→back you judge better; ≥ 0.6 s a leg, the
dot tracing the curve; the dot may come back to full while it traces). By
the end: `curve.hero` 0, dims 0, `t` 0.70, still. Ends `SEAM[3]`.

**4 Score** — "The model doesn't say yes or no. It gives every request a
score. And this threshold is what turns that score into a yes." (model
9.92, yes 10.46, no 10.78, gives 11.00, score 11.92, threshold 13.26,
turns 14.02, score 14.54, yes 15.12.) `t` stays 0.70 the whole beat.
"yes or no": nothing moves, or a gentle `userPulse` on "request" (11.38).
"a score": `scoreTag {i: SC.TAG_I, a: 0→1}` (its real score, "0.84"); while
it's up, its ring is the flagged ring already drawn. "this threshold":
`thr.pulse` one pulse. "into a yes": `code.opacity` 0→1 (from ~14.0) with
`code.hero` 1 and `thr.dim` ~0.6 while lit, landing on "yes"; then
`code.hero` → 0, `thr.dim` → 0, `scoreTag.a` → 0 by ~5.6 s. Ends `SEAM[4]`.

**5 Slide left** — "You slide it to the left and we can catch every
attack. But we end up blocking most of our users." (slide 15.98, left
16.50, catch 17.00, every 17.22, attack 17.42, blocking 18.71, most 19.04,
users 19.58.) "slide it to the left": `t` 0.70 → 0.20, ≥ 1.2 s, eased,
landing by ~"every". "every attack": `boxHi.tp` pulse (TP 50) and
`attackRing` one pulse. "most of our users": `boxHi.fp` pulse (FP 5,055),
`userPulse`. Ends `SEAM[5]`.

**6 Slide right** — "If you slide it to the right, almost nobody gets
blocked, but half of the attacks get through." (slide 20.62, right 21.20,
nobody 21.74, blocked 22.34, half 22.82, attacks 23.34, through 23.94.)
"slide it to the right": `t` 0.20 → 0.85, ≥ 1.2 s. "nobody gets blocked":
`boxHi.fp` pulse (FP 28). "half of the attacks": `boxHi.fn` pulse (FN 29)
and `missRing` 0→1→0 (the 29 unflagged gold dots). Ends `SEAM[6]`.

**7 Each one is a point** — "Every threshold gives a new confusion matrix,
and each one is a point. The true positive rate up, false positive rate
across." (Every 24.60, threshold 24.80, new 25.84, confusion 26.05,
matrix 26.44, each 27.00, point 27.82, true 28.70, positive 29.00, up
29.66, false 30.34, across 31.16.) First ~0.5 s: `curve.dim` 0→0.7.
"Every threshold … matrix": `t` steps 0.85 → 0.20 → 0.40 → 0.55 (eased
legs, ≥ 0.6 s, a short hold at each so the box reads). "each one is a
point": the points arrive — at the current stop a point pops
(`points[k].a` 0→1, `dot.pulse`), then the line continues 0.70, 0.85 and
the points for the stops already passed (0.20, 0.40) pop on "point"
(27.82); order them so all five are on by ~30.5. "true positive rate up":
`rocLabels.tpr` 0→1→0 and `guide` 0→1 (from the current dot). "false
positive rate across": `rocLabels.fpr` 0→1→0, `guide` → 0 by the end.
Last ~0.6 s: `curve.dim` → 0, `t` at 0.85. Ends `SEAM[7]` (points
array: all five, `a` 1, in `SC.STOPS` order).

**8 Sweet spot** — "Top left is the sweet spot." (Top 32.30, left 32.38,
sweet 32.84, spot 33.10.) On "Top left": `corner` 0→1 (≥ 0.6 s), while
`thr.dim`, `dot.dim` and each point's `dim` → 1. Still from ~1.5 s. Ends
`SEAM[8]`.

**9 Takeaway** — "Now ROC is for picking thresholds. You decide whether
you'd rather avoid false positives or get all the positives depending on
the problem you're solving." (ROC 34.24, picking 35.00, thresholds 35.24,
decide 36.12, avoid 37.54 (check: the word after "rather" at 37.41 on the
envelope), false 38.10, positives 38.36, get 38.98, all 39.16, positives
39.62, depending 39.78, problem 40.47, solving 40.98.) "picking
thresholds": `corner` → 0, points `a` → 0, `thr.dim` and `dot.dim` → 0
(the line takes the hero back). "avoid false positives": the line is already
at the right-hand stop (0.85), so it holds there and `boxHi.fp` pulses
(FP 28). "get all the
positives": `t` 0.85 → 0.20 (≥ 1 s), `boxHi.tp` pulse (TP 50).
"problem you're solving": `t` 0.20 → 0.70 (≥ 1 s), one `dot.pulse` as it
lands. Still for the last ~1 s. Ends `SEAM[9]`.

## Report

As in the HyperFrames brief: per beat, the cue constants with their word,
the mp4 path and measured duration, `check` errors / warnings, anything
changed from this brief and why, what you wished existed. Do not commit.
