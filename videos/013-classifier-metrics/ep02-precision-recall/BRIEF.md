# Beat brief: 013 ep02, precision vs recall

**Name:** classifier-ep02-beat-brief
**Description:** The contract for the eight HyperFrames beats of
"Precision vs recall" (37.12 s). Every beat draws with the episode kit
`_kit/score.js` through one call, `K.draw(g, S)`, where `S` is a state
object; each beat opens on `SC.SEAM[n-1]` and ends on `SC.SEAM[n]`, so cuts
are exact by construction.
**When to use:** you were handed this path plus one or two beat numbers.
**How it works:** copy the template below into your beat folder, write
`S(t)` from the cues, check, render to `media/hf/`, review your own
contact sheet, report.

## Read first

1. `agents/beat-brief-hyperframes.md` (repo root): the technical rules
   (pure function of time, no network, no `Math.random`, palette, safe
   area, text floor, review loop, report format). All of it applies. One
   exception, below: the stage runs to y 1330.
2. `_kit/score.js`: the kit. Read all of it, especially `mount`, the state
   fields listed above it, and `SEAM`.
3. `storyboard.md`: the ledger and the beats table (the visual brief).
4. `00_layout/index.html` (the approved look, including a worked lift of
   the attack column into recall's denominator: copy its timing shape for
   beats 3 and 5) and `00_layout/layout_sheet.png`.
5. Worked examples from ep 1, same kit family:
   `../ep01-accuracy-trap/03_model_a/index.html` (cues, a hold, a local
   helper) and `../ep01-accuracy-trap/04_box_flags/index.html` (one cell lit
   at a time). Read only; never edit ep 1.

Never edit `_kit/`, `00_layout/`, another beat's folder, `videos/_shared/`
or anything outside this episode folder. Need something from the kit (a
new state field, a part)? Write a local helper in your `index.html` and
name it in the report.

## Layout facts

- Captions are burned with `assemble.py --captions-anchor bottom`, so the
  stage runs to **y 1330**. Nothing of yours goes below 1330.
- The dots never leave the score line in this episode. The box holds
  counts only. The fraction rows are under the box.
- Numbers come from the ledger (`SC.LEDGER`, `storyboard.md`). Never type
  a new number.
- **One magenta hero** at a time, named per beat below. The threshold
  rests dimmed (the kit draws it that way); don't light it.
- Rings on the score line (`ring`, `attackRing`) are white accents, not
  the hero; they go with the magenta box group they belong to.
- `check`'s `sweep_static` needs an honest DOM change (geometry or
  opacity, not just colour). The fraction rows, the `alt` tag swap and the
  `bright` scale do that; a beat that only changes colours and canvas
  rings needs a small DOM move too (e.g. `box.bright` on the named cell's
  count).

## Template (copy to `NN_beat/index.html`)

Start from `00_layout/index.html` (head, style, root) and replace its
script body with:

```js
(() => {
  const BEAT_SECONDS = 0.0;            // from the table
  const MASTER = 0.0;                  // master start, from the table
  const CUE = { /* word: master − MASTER, from words.json */ };
  const HOLD = 0.0;                    // still from here; S(t) === SEAM[n]
  const root = document.getElementById("root"), g = document.getElementById("scene").getContext("2d");
  const { seg, lerp, pulse, SEAM } = SC, E = SC.E();
  const K = SC.mount(root);
  function S(t) { /* S(0) deep-equals SEAM[n-1], S(t >= HOLD) is SEAM[n] */ }
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

and set `data-duration` on `#root` to `BEAT_SECONDS` and the comment at
the top to your beat. The `kit` and `vendor` symlinks are already in your
folder. Render from the beat folder:
`npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4`
(with the env vars from the HyperFrames brief). Contact sheet from the
episode folder: `../../../tools/review_frames.sh media/hf/NN_beat.mp4 4`.
**Never two renders at once in one folder;** your beat folder is yours.

Frame 0 must be `SEAM[n-1]` exactly; something starts moving by the first
cue; the last ≥ 0.3 s is still and equals `SEAM[n]`. A move the viewer
tracks gets ≥ 0.6 s; a fade or a colour change can be 0.3 s.

## The beats

Master times; cue times are from `words.json` (master seconds, spellings
fixed). Check the cues that matter on the envelope of `vo_final.wav`.
Beat-local = master − start.

| # | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on | Hero |
|---|---|---:|---:|---|---|---|
| 1 | `01_recall_q` | 0.00 | 4.30 | `SEAM[0]` (first frame of the Short) | `SEAM[1]` | the attack column (tp + fn frames) |
| 2 | `02_context` | 4.30 | 4.25 | `SEAM[1]` | `SEAM[2]` | none (the tag brightens white) |
| 3 | `03_recall_80` | 8.55 | 4.35 | `SEAM[2]` | `SEAM[3]` | the lift, then recall's 80% |
| 4 | `04_precision_q` | 12.90 | 6.40 | `SEAM[3]` | `SEAM[4]` | the flagged row (tp + fp frames) |
| 5 | `05_precision_40` | 19.30 | 3.65 | `SEAM[4]` | `SEAM[5]` | the lift, then precision's 40% |
| 6 | `06_no_tn` | 22.95 | 6.20 | `SEAM[5]` | `SEAM[6]` | the TN cell, then none |
| 7 | `07_missed` | 29.15 | 3.05 | `SEAM[6]` | `SEAM[7]` | the FN cell |
| 8 | `08_wasted` | 32.20 | 4.922 | `SEAM[7]` | `SEAM[8]` (last frame of the Short, still) | the FP cell, then none |

**1 Recall, the question** — "Recall is asking, of all the positives, how
many did I actually catch?" Words (master): Recall 0.38, positives 1.88,
how 2.84, actually 3.48, catch 3.78 (ends 4.16). Frame 0 is the finished
picture (the hook rule) with motion from frame 1: on "Recall" `bars.r.lit`
0→1 (0.3 s). On "positives": `box.lit` tp and fn 0→1 together (the
column) and `ring` tp and fn 0→1 (0.4 s). On "catch": `box.bright.tp`
one pulse (the 40 swells and settles). Still from ~4.0 s. Ends `SEAM[1]`.

**2 Context** — "It's a prompt injection detector. 10,000 requests come
in, but only 50 are attacks." Words (master): It's 4.48, prompt 4.70,
detector 5.46, 10,000 6.20, requests 6.58, only 7.36, 50 7.50, attacks
8.00 (ends 8.40). First ~0.4 s: everything from `SEAM[1]` back to rest
(column frames, rings and the recall label off). "prompt injection
detector": `tag.bright` 0→1, back to 0 by ~6.0. "10,000 requests":
`tag.bright2` up and down, with `userPulse` one pulse. "only 50":
`tag.atk` up and down, with `attackRing` one pulse. DOM motion for
`sweep_static`: a small local helper is fine (e.g. scale the tag line
being named 1 → 1.04 → 1 with `K.tag.l1.style.transform`; reset to none
by the end). Still from ~8.3 s. Ends `SEAM[2]` (= rest).

**3 Recall = 80%** — "If there were 50 attacks and we only caught 40,
recall is about 80%." Words (master): If 8.72, 50 9.04, attacks 9.42,
caught 10.28, 40 10.48, recall 11.34, 80% 11.94 (ends 12.54). On "50
attacks": `box.lit` tp+fn on (0.25 s), then the `lift` {kind "col"} u 0→1
(≥ 0.8 s) while the column frames go back to 0 as the lift leaves, and
`bars.r.den` 0→1 as it lands, then `lift.a` → 0. "caught 40": `bars.flyNum`
{row "r"} u 0→1 (≥ 0.7 s), then `bars.r.num` 0→1 as it lands. "recall":
`bars.r.lit` up. "80%": `bars.r.pct` 0→1 with `pctHero` 1 (the 80% lands
magenta), then `pctHero` and `r.lit` back to 0 in the last ~0.6 s. Still
from ~4.0 s. Ends `SEAM[3]`.

**4 Precision, the question** — "Now precision is saying, of the ones that
I did predict were positive, how many actually were positive?" Words
(master): Now 13.08, precision 13.24, ones 14.82, predict 15.62, positive
16.25, how 17.21, actually 17.64, positive 18.54 (ends 18.92). "precision":
`bars.p.lit` 0→1. "predict were positive": `box.lit` tp and fp 0→1 (the
row) and `ring` tp and fp 0→1 (the 100 dots right of the threshold:
40 gold rings, 60 teal grow). "actually were": `box.bright.tp` one pulse.
Still from ~19.0 master. Ends `SEAM[4]`.

**5 Precision = 40%** — "We flagged 100, 40 were attacks, precision is
40%." Words (master): We 19.48, flagged 19.54, 100 19.90, 40 20.41,
attacks 20.74, precision 21.31, 40% 22.01 (ends 22.16). Short beat, so
start at once: "flagged 100": the `lift` {kind "row"} u 0→1 (0.7 s) as
the row frames go to 0, `bars.p.den` 0→1 as it lands, `ring` tp/fp out
with it. "40 were attacks": `flyNum` {row "p"} (0.6 s), `bars.p.num` 0→1.
"40%": `bars.p.pct` with `pctHero` 1, then `pctHero` and `p.lit` to 0 by
~3.3 s local. Still from ~3.3 s. Ends `SEAM[5]`.

**6 Neither uses TN** — "Neither one uses the true negatives. In this
case, there's almost 10,000 of them. That's why they still work when the
attacks are rare." Words (master): Neither 23.15, true 23.92, negatives
24.10, 10,000 26.05, rare 28.62 (ends 28.92). "true negatives":
`box.lit.tn` 0→1 (the hero). "10,000": `box.bright.tn` one pulse (the
9,890 swells; the screen shows the ledger value). Then, by ~27.3 master:
`lit.tn` → 0 while `ghost.tn` 0→1 and `strike.tn` 0→1 (≥ 0.6 s): the cell
fades out of play, struck through. "rare": `attackRing` one pulse on the
score line. Still from ~28.9 master. Ends `SEAM[6]`.

**7 What you missed** — "Recall is all about what you missed. These are
the attacks that got through," Words (master): Recall 29.36, missed 30.38,
These 31.24, attacks 31.52, through 32.16. "Recall": `bars.r.lit` pulse up
and back down by "missed" (one hero at a time: it's down before the cell
lights). "missed": `box.lit.fn` 0→1 and `box.alt.fn` 0→1 (0.4 s): the tag
"FN" crossfades to "missed". "attacks that got through": `ring.fn` 0→1
(the 10 gold dots left of the threshold). Still from ~32.6 master (short
hold, 0.3 s minimum). Ends `SEAM[7]`.

**8 What you wasted** — "and precision is about what you wasted. These
are real users that you ended up blocking." Words (master): and 32.48,
precision 32.58, wasted 33.64, These 34.55, real 34.76, users 35.00,
blocking 35.95 (ends 36.28; the VO is silent from 36.35 to 37.12). First
~0.4 s: `lit.fn` and `ring.fn` → 0 (`alt.fn` stays 1). "precision":
`bars.p.lit` up and down, as in beat 7. "wasted": `box.lit.fp` 0→1 and
`box.alt.fp` 0→1: "FP" → "wasted". "real users": `ring.fp` 0→1 (the 60
teal dots right of the threshold grow). "blocking": hold, then `lit.fp`
and `ring.fp` → 0 by ~36.4 master. Still from ~36.4 master to the end:
the last frame of the Short, `SEAM[8]`.

## Report

As in the HyperFrames brief: per beat, the cue constants with their word,
the mp4 path and measured duration, `check` errors / warnings, anything
changed from this brief and why, what you wished existed. Do not commit.
