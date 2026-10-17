# Beat brief: 013 ep05, F1 and the threshold

**Name:** classifier-ep05-beat-brief
**Description:** The contract for the seven HyperFrames beats of "F1 score
explained" (44.35 s). Every beat draws with the episode kit
`_kit/score.js` through one call, `K.draw(g, S)`, where `S` is a state
object; each beat opens on `SC.SEAM[n-1]` and ends on `SC.SEAM[n]`, so
cuts are exact by construction.
**When to use:** you were handed this path plus one or two beat numbers.
**How it works:** copy the template below into your beat folder, write
`S(t)` from the cues, check, render to `media/hf/`, review your own
contact sheet, report.

## Read first

1. `agents/beat-brief-hyperframes.md` (repo root): the technical rules
   (pure function of time, no network, no `Math.random`, palette, safe
   area, text floor, review loop, report format). All of it applies. One
   exception, below: the stage runs to y 1330.
2. `_kit/score.js`: the kit. Read all of it, especially `mount`, the
   state fields above it, and `SEAM`.
3. `storyboard.md`: the ledger and the beats table (the visual brief).
4. `00_layout/index.html` (the approved look) and its `layout.png`.
5. The worked examples: ep 1's finished beats, same kit pattern:
   `../ep01-accuracy-trap/03_model_a/index.html` (threshold drop-in,
   ticking numbers) and `../ep01-accuracy-trap/04_box_flags/index.html`
   (one part fading out, another in, a lit cell).

Never edit `_kit/`, `00_layout/`, another beat's folder,
`videos/_shared/`, or anything outside this episode folder. Need something
from the kit? Write a local helper in your `index.html` and name it in the
report.

## Layout facts

- Captions are burned with `assemble.py --captions-anchor bottom`, so the
  stage runs to **y 1330**. Nothing of yours goes below 1330.
- Numbers come from the kit (`SC.LEDGER`, `SC.BARS_EX`, `SC.BARS_A`, and
  the readout, which counts the dots for the current `thrS`). Never type a
  new number. A bar's value text is "0.9" / "0.1" for the example and
  "40%" / "80%" for Model A (the VO says them that way); switch the text
  when that bar starts to move.
- One magenta hero per moment, as listed per beat below. When the hero
  passes on, the old one goes to rest in the same ~0.3 s.

## Template (copy to `NN_beat/index.html`)

Start from `00_layout/index.html` (keep its `<head>`, font face and
`#root`) and replace its script body with:

```js
(() => {
  const BEAT_SECONDS = 0.0;            // from the table
  const MASTER = 0.0;                  // master start, from the table
  const CUE = { /* word: master − MASTER, from words.json */ };
  const root = document.getElementById("root"), g = document.getElementById("scene").getContext("2d");
  const { seg, lerp, pulse, SEAM } = SC, E = SC.E();
  const K = SC.mount(root);
  function S(t) { /* build the state; S(0) deep-equals SEAM[n-1] (plus beat 1's motion), S(end) deep-equals SEAM[n] */ }
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

and set `data-duration` on `#root` to `BEAT_SECONDS`. The folders and
their `kit` / `vendor` symlinks already exist. Render from the beat
folder (env vars from the HyperFrames brief):
`npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4`.
Contact sheet from the episode folder:
`../../../tools/review_frames.sh media/hf/NN_beat.mp4 4`.
Never two renders at once in one folder; each agent renders only its own
beat folders.

Fades: when one part leaves and another arrives in the same area (bars →
cards, cards → target), fade the old one out before the new one is more
than ~30 % in, or `check` flags overlapping text. Frame 0 must be
`SEAM[n-1]` exactly; something moves by frame 1 or soon after the first
cue; the last ~0.3 s is still and equals `SEAM[n]`.

## The beats

Master times from `words.json` (spellings fixed). Cue = master − start.

| # | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on | Hero |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 7.40 | first frame of the Short = `SEAM[1]` plus motion | `SEAM[1]` | the F1 line |
| 2 | `02_harmonic` | 7.40 | 7.30 | `SEAM[1]` | `SEAM[2]` | the F1 line |
| 3 | `03_model_a` | 14.70 | 4.20 | `SEAM[2]` | `SEAM[3]` | the F1 line |
| 4 | `04_costs` | 18.90 | 9.60 | `SEAM[3]` | `SEAM[4]` | the card being named |
| 5 | `05_target` | 28.50 | 6.20 | `SEAM[4]` | `SEAM[5]` | "at least 1 flag in 3" (+ its outline) |
| 6 | `06_move_line` | 34.70 | 4.00 | `SEAM[5]` | `SEAM[6]` | the threshold |
| 7 | `07_takeaway` | 38.70 | 5.65 | `SEAM[6]` | `SEAM[7]` (last frame of the Short, still) | the threshold |

**1 Hook** (0.00) — "The F1 score is precision and recall in one number,
and it punishes whichever is worse. It's a prompt injection detector."
Frame 0 is the finished picture (the hook rule), so `S(0)` is `SEAM[1]`
with motion on top: the F1 line's `f1Pulse` already rising (a gentle
swell over the first ~0.6 s). "one number" (2.32): `f1Pulse` once.
"whichever is worse" (4.04–4.75): `pulseR` once (the 0.1 bar). "prompt
injection detector" (5.78–6.56): `tagBright` up then down, with one
`userPulse` and one `attackRing` across it. Still from ~7.0.

**2 Why harmonic** (7.40) — "Average 0.9 and 0.1 and you get 0.5. F1 will
give you 0.18. It's a harmonic mean." "0.9" (8.06 → 0.66): `pulseP`
small. "0.1" (8.96 → 1.56): `pulseR` small. "0.5" (9.74 → 2.34): `mean`
0 → 1 (≥ 0.6 s; the dashed line draws left to right). "0.18" (12.06 →
4.66): `f1Pulse`. "harmonic" (13.72 → 6.32): `pulseR` and a smaller
`f1Pulse` together (the F1 line hugs the weak bar). Ends `SEAM[2]`.

**3 Model A** (14.70) — "Our model, 40 percent precision, 80 percent
recall, scores 0.53." "Our model" (14.94 → 0.24): `thr` 0 → 1 (≥ 0.6 s;
it stays dim, `thrHero` 0), `flag` 0 → 1 with it, `mean` 1 → 0. "40"
(15.57 → 0.87): `p` 0.9 → 0.40 (≥ 0.6 s), `pText` "40%". "80" (16.54 →
1.84): `r` 0.1 → 0.80, `rText` "80%". "0.53" (17.58 → 2.88): `f1` 0.18 →
0.53, landing by ~3.5, `f1Text` "F1 0.53" as it moves. Ends `SEAM[3]`.

**4 Costs** (18.90) — "But F1 treats both mistakes the same, and here
they aren't. A false positive blocks a real user who can try again. A
false negative would let an attack hijack your agent and leak your data."
"But F1" (19.16 → 0.26): `bars.opacity` 1 → 0 by ~0.9, then
`cards.opacity` 0 → 1 (the two cards, same size, nothing lit). "false
positive" (22.23 → 3.33): `lit.fp` 0 → 1 and one `fpRing` pulse on the
score line (≥ 0.8 s). "false negative" (25.11 → 6.21): `lit.fp` → 0,
`lit.fn` → 1, one `fnRing` pulse. Ends `SEAM[4]`.

**5 The target** (28.50) — "So say we'll accept two blocked users for
every attack we stop. That means at least one flag in three has to be a
real attack." "So say" (28.72 → 0.22): `cards.opacity` → 0. "two blocked
users" (29.56 → 1.06): `target.tokens` 0 → 1 and `target.rate` 0 → 1
(`target.opacity` 1 throughout). "one flag in three" (32.10 → 3.60):
`rule` 0 → 1 with `ruleHero` 1. "real attack" (33.98 → 5.48): `readout`
0 → 1 (Model A's line: "caught 40 / 50", "100 flags, 40 real"). Ends
`SEAM[5]`.

**6 Move the line** (34.70) — "Now move the line down as far as that
allows, 41 of 50 attacks caught." "move" (35.02 → 0.32): `ruleHero` 1 →
0 and `thrHero` 0 → 1 together (~0.3 s), then `thrS` from `SC.T_A` to
`SC.T_END` (ease in-out, ≥ 1.5 s, landing by "allows" + ~0.3, before
"41" at 37.14 → 2.44). The readout and the flagged dots follow `thrS` on
their own. "41 of 50" (2.44): `caughtPulse` once. Ends `SEAM[6]`.

**7 Takeaway** (38.70) — "You don't ship an F1 score, you ship a
threshold. Decide what a mistake costs and then put the line there."
"threshold" (40.28 → 1.58): `thrPulse` once. "costs" (42.21 → 3.51):
`rulePulse` once (the rule stays white; no magenta). "put the line
there" (42.74–43.26): hold. Still from ~4.9 to the end. Ends `SEAM[7]`.

## Report

As in the HyperFrames brief: per beat, the cue constants with their word,
the mp4 path and measured duration, `check` errors / warnings, anything
changed from this brief and why, what you wished existed. Do not commit.
