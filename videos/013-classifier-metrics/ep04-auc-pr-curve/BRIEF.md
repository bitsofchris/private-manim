# Beat brief: 013 ep04, ROC AUC vs PR AUC

**Name:** classifier-ep04-beat-brief
**Description:** The contract for the seven HyperFrames beats (beat 2 was cut; beat 3 opens on `SEAM[2]`, which equals `SEAM[1]`) of
"Precision recall curve explained (PR AUC vs ROC AUC)" (50.4 s). Every
beat draws with the episode kit `_kit/score.js` through one call,
`K.draw(g, S)`, where `S` is a state object; each beat opens on
`SC.SEAM[n-1]` and ends on `SC.SEAM[n]`, so cuts are exact by
construction.
**When to use:** you were handed this path plus one to three beat numbers.
**How it works:** your beat folder is already made (with `kit` and
`vendor` symlinks); write its `index.html` from the template, check,
render to `media/hf/`, review your own contact sheet, report.

## Read first

1. `agents/beat-brief-hyperframes.md` (repo root): the technical rules
   (pure function of time, no network, no `Math.random`, palette, safe
   area, text floor, review loop, report format). All of it applies. One
   exception: the stage runs to **y 1330** (captions are anchored bottom).
2. `_kit/score.js`: the kit. Read all of it, especially `mount` (the S
   fields listed above it), `REST` and `SEAM`.
3. `storyboard.md`: the ledger and the beats table (the visual brief).
4. `00_layout/index.html` (the approved look) and `00_layout/layout.png`
   (frame 0, beat 4, mid-morph, beat 7, last frame).

Never edit `_kit/`, `00_layout/`, another beat's folder, `videos/_shared/`
or anything outside this episode folder. Need something from the kit (a
new state field, a part)? Write a local helper in your `index.html` and
name it in the report. **Never type a number:** every number on screen is
already in the kit (`SC.LEDGER`, the notes, the code card), or comes from
`SC.counts(t)`.

## Template (`NN_beat/index.html`)

Copy `00_layout/index.html` and replace its script body with:

```js
(() => {
  const BEAT_SECONDS = 0.0;            // from the table
  const CUE = { /* word: beat-local seconds, from the table below / words.json */ };
  const root = document.getElementById("root"), g = document.getElementById("scene").getContext("2d");
  const { seg, lerp, pulse, SEAM, LEDGER } = SC, E = SC.E();
  const K = SC.mount(root);
  function S(t) { /* the state; S(0) equals SEAM[n-1], S(end) equals SEAM[n] */ }
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

and set `data-duration` on `#root` to `BEAT_SECONDS` (and fix the
comment at the top). Build `S(t)` by interpolating between the seam
states' fields with `seg` + an ease. Fields a seam leaves out take their
`REST` default (inside `draw`), so write every field you animate
explicitly at both ends. Text in `notes.sub` swaps only while its opacity
is 0: fade the old line out, change the string, fade the new one in.

Render from the beat folder:

```
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
```

Contact sheet from the episode folder:
`../../../tools/review_frames.sh media/hf/NN_beat.mp4 4`. Look at your
first and last frames side by side with `00_layout/layout.png`.
**Never two renders at once in one folder;** each agent renders only in
its own beat folder.

Motion rules: frame 0 is `SEAM[n-1]` exactly; something starts moving by
the first cue; a move the viewer tracks takes ≥ 0.6 s; the last ~0.3 s is
still and equals `SEAM[n]`. One magenta thing at a time (the hero column):
hand it over by fading the old hero's `hero` / `dim` field as the new one
rises, over the same ~0.4 s. Land each change on its word.

## The beats

Cue times are beat-local seconds (master − start), word starts from
`words.json`; check the ones that matter on the envelope of `vo_final.wav`.

| # | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on | Hero |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 6.50 | `SEAM[0]` (first frame of the Short) | `SEAM[1]` | the ROC area, then the threshold |
| 3 | `03_what_auc` | 6.50 | 9.20 | `SEAM[2]` | `SEAM[3]` | the ROC area |
| 4 | `04_the_point` | 15.70 | 8.30 | `SEAM[3]` | `SEAM[4]` | the threshold and its point |
| 5 | `05_swap` | 24.00 | 10.60 | `SEAM[4]` | `SEAM[5]` | the curve |
| 6 | `06_baseline` | 34.60 | 4.70 | `SEAM[5]` | `SEAM[6]` | the baseline |
| 7 | `07_pr_auc` | 39.30 | 6.30 | `SEAM[6]` | `SEAM[7]` | the PR area |
| 8 | `08_takeaway` | 45.60 | 4.85 | `SEAM[7]` | `SEAM[8]` (last frame, still) | the code card's lit line |

**1 Hook** (6.50 s) — "This model's ROC area under the curve is 0.985,
nearly perfect, but most of what it flags is wrong." Cues: ROC 1.06,
area 1.48, curve 2.19, 0.985 2.61, nearly 3.72, perfect 4.00, most 4.90,
flags 5.60, wrong 5.98. Frame 0 is already the finished picture (the
hook rule); give it motion from frame 1: a slow breath on the area
(`rocArea.o` 1 → ~0.8 → 1 around "area under the curve", or the value's
`roc.hero` pulse on "0.985"). Keep it subtle. On "nearly perfect":
`corner` 0→~0.6→0 (the good corner, top left, glows once). On "most of what it flags": hero
hand-off: `rocArea.hero` 1→0 while `thr.dim` 1→0 (the threshold turns
magenta), then `fpLit` 0→1 (the 60 flagged users brighten, ≥ 0.6 s), and
`notes.sub` lines "60 of 100 flags" / "are real users" fade in by
"wrong". Hold the last ~0.3 s on `SEAM[1]`.

**2 Context** — cut after the first watch (Chris, 10/17).

**3 What AUC is** (9.20 s) — "AUC is for comparing models. A coin flip
is 0.5. You pick a random attack and a random user, and 98.5% of the time
the attack scores higher." Cues: AUC 0.22, comparing 0.83, coin 2.38,
0.5 2.94, random 4.46, attack 4.72, random 5.20, user 5.40, 98.5% 5.82,
attack 7.68, higher 8.62. First (by ~0.8): hero back to the area —
`thr.dim` 0→1, `fpLit` 1→0, `rocArea.hero` 0→1; the two sub lines fade
out. "comparing models": `roc.hero` pulse on the value (0→~0.6→0). "coin
flip": `diag` 0→1 (≥ 0.8 s), and `notes.sub[1]` "coin flip 0.5" fades in
by "0.5". "random attack": `pair` 0→1 (the attack ring and the user ring;
the kit draws both together, so bring it up across "attack … user").
"98.5%": `notes.sub[0]` "98.5% of pairs" fades in. "scores higher":
hold. Ends `SEAM[3]`.

**4 The point** (8.30 s) — "Now look at this point. False positive rate
2.3 percent. Sounds small. It's 233 real users blocked just to catch 44
attacks." Cues: Now 0.22, this 0.54, point 0.76, False 1.48, 2.3% 2.36,
Sounds 3.38, 233 4.56, real 5.40, users 5.70, blocked 6.04, catch 6.88,
44 7.12, attacks 7.54. First (by ~0.5): `pair` 1→0, `diag` 1→0, the
subs out, `roc.o` 1→0 (the ROC readout leaves), `rocArea.hero` 1→0 and
`rocArea.o` 1→0.5. "this point": hero hand-off to the threshold
(`thr.dim` 1→0) and `point.o` 0→1 with `point.hero` 1, then `t`
0.70→0.55 (≥ 1.2 s, ease in-out) so the point runs down the curve with
the line; `point.ring` 0→1 as it lands. "2.3%": `ptLab.o` 0→1. "233":
`fpLit` 0→1 (the 233 users right of 0.55 brighten) and `sub[0]` "233
users blocked" in, by "blocked". "44": `sub[1]` "44 attacks caught"
(gold; the third element of the sub entry) in, and `flag` pulses the
attack rings (`attackRing` 0→~0.6→0) on "attacks". Ends `SEAM[4]`.

**5 Swap the axis** (10.60 s) — "So swap the false positive rate for
precision. Precision doesn't use true negatives. Recall goes across,
precision goes up, and the same model's curve drops. Now the good corner
is top right." Cues: swap 0.36, false 0.88, precision 1.72, Precision
2.70, true 3.53, negatives 3.66, Recall 4.76, across 5.16, precision
5.85, up 6.54, curve 7.92, drops 8.08, good 9.42, corner 9.63, top
9.97, right 10.17. First (by ~0.6): the readout notes out (`ptLab`,
subs), `point.ring` 1→0, `rocArea.o` 0.5→0. "false positive rate":
`names.bLit` 0→1. "precision" (1.72): `names.bText` 0→1 (the x name
becomes "precision" in place), `bLit` back to 0 by ~2.4. "true
negatives": `tnDim` 0→1 (the unflagged pile mutes, ≥ 0.6 s). "Recall"
(4.76): `names.aText` 0→1 ("true positive rate" → "recall"). "across …
up" (5.0 → 6.5): **both names move together**, `aMove` and `bMove` 0→1
over the same ~1.4 s (they pass on opposite arcs; never move one while
the other sits in its target slot). Then the morph: hero hand-off from
the threshold and point to the curve (`thr.dim` 0→1, `point.hero` 1→0,
`curve.hero` 0→1) at ~6.5, and `m` 0→1 from ~6.6 to ~8.3 (ease
in-out) so it lands on "drops". "good corner … top right": `corner`
0→1 by "right". Ends `SEAM[5]`.

**6 The baseline** (4.70 s) — "And the coin flip here isn't 0.5. It's
0.005, the attack rate." Cues: coin 0.44, isn't 1.06, 0.5 1.36, 0.005
2.76, attack 4.04, rate 4.36. First: `corner` 1→0 and `curve.hero` 1→0
(by ~0.6). "coin flip": `base.o` 0→1 at `v` 0.5, `base.hero` 1 (the
label "0.5" comes with it). "0.005": `v` 0.5→0.005 (≥ 0.8 s, ease out),
the label swaps to "0.005 · attack rate" on its own as it drops. "attack
rate": hold. Ends `SEAM[6]`.

**7 PR AUC** (6.30 s) — "This model's precision-recall area under the
curve is 0.56. It's low looking, but over a hundred times better than
chance." Cues: precision 0.72, area 1.38, curve 1.89, 0.56 2.16, low
3.77, hundred 4.54, times 4.92, chance 5.64. "area under the curve":
hand-off from the baseline (`base.hero` 1→0) to the PR area: `prArea`
`{o: 1, hero: 1, reveal: 0→1}` (≥ 1 s, the steps fill left to right).
"0.56": `notes.pr.o` 0→1 (the readout reads 0.556, the ledger value).
"hundred times": `notes.prSub` 0→1 ("111× a coin flip"). Hold from ~5.8.
Ends `SEAM[7]`.

**8 Takeaway** (4.80 s) — "When positives are rare, we want to compare
models on the precision-recall curve." Cues: positives 0.32, rare 0.94,
compare 1.65, models 1.96, precision 2.88, curve 3.62. "rare":
`attackRing` one pulse (0→1→0 over ~0.6 s). "compare models": the score
line gives way to the code card: `line` 1→0 (≥ 0.5 s), then `code.o`
0→1 with `out` both 1 (fade the line out before the card is ~30 % in),
and hero hand-off: `prArea.hero` 1→0 as `code.lit[1]` 0→1 by
"precision". Still from ~4.4 s. Ends `SEAM[8]`.

## Report

As in the HyperFrames brief: per beat, the cue constants with their word,
the mp4 path and measured duration, `check` errors / warnings, anything
changed from this brief and why, what you wished existed. Do not commit.
