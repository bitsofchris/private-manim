# Beat brief: 013 ep01, the accuracy trap

**Name:** classifier-ep01-beat-brief
**Description:** The contract for the seven HyperFrames beats of
"Confusion matrix explained: the accuracy trap" (48.80 s as briefed; 41.96 s after
Chris's second cut, see storyboard.md "Final beats" for the current starts). Every beat draws
with the episode kit `_kit/score.js` through one call, `K.draw(g, S)`,
where `S` is a state object; each beat opens on `SC.SEAM[n-1]` and ends on
`SC.SEAM[n]`, so cuts are exact by construction.
**When to use:** you were handed this path plus one or two beat numbers.
**How it works:** copy the template below into your beat folder, write
`S(t)` from the cues, check, render to `media/hf/`, review your own
contact sheet, report.

## Read first

1. `agents/beat-brief-hyperframes.md`: the technical rules (pure function
   of time, no network, no `Math.random`, palette, safe area, text floor,
   review loop, report format). All of it applies. One exception, below:
   the stage runs to y 1330.
2. `_kit/score.js`: the kit. Read all of it, especially `mount`, the state
   fields above it, and `SEAM`.
3. `storyboard.md`: the ledger and the beats table (the visual brief).
4. `00_layout/index.html` (the approved look) and its `layout.png`.

Never edit `_kit/`, `00_layout/`, another beat's folder, `videos/_shared/`
or anything outside this episode folder. Need something from the kit (a
new state field, a part)? Write a local helper in your `index.html` and
name it in the report.

## Layout facts

- Captions are burned with `assemble.py --captions-anchor bottom`, so the
  stage runs to **y 1330** (agents/style.md "Share the band with a scene
  element"). Nothing of yours goes below 1330.
- Numbers come from the ledger (`SC.LEDGER`, `storyboard.md`). Never type a
  new number. The code card's text is `SC.CODE` / `SC.CODE_OUT`.
- Hero: the one magenta thing per moment is listed per beat below. The
  code card's highlight bar is magenta, so while it's lit nothing else is.
- The code card is 52 px monospace (the ledger's 26-character lines don't
  fit the safe width at 60). Known; don't change it.

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

and set `data-duration` on `#root` to `BEAT_SECONDS`. The folder needs
two symlinks (from the episode folder):

```
ln -s ../_kit NN_beat/kit && ln -s ../../../_shared/web/vendor NN_beat/vendor
```

(Already made for you.) Render from the beat folder:
`npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4`
(with the env vars from the HyperFrames brief). Contact sheet from the
episode folder: `../../../tools/review_frames.sh media/hf/NN_beat.mp4 4`.

Fades: when one part leaves and another arrives in the same area (counter
→ code, counter → box), fade the old one out before the new one is more
than ~30 % in, or `check` flags overlapping text. Frame 0 must be
`SEAM[n-1]` exactly; something starts moving by frame 1 or soon after the
first cue; the last ~0.3 s is still and equals `SEAM[n]`.

## The beats

Master times; cue times come from `words.json` (master seconds, spellings
fixed) and are checked on the envelope of `vo_final.wav` where they matter.

| # | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on | Hero |
|---|---|---:|---:|---|---|---|
| 1 | `01_hook` | 0.00 | 5.20 | (first frame of the Short) = `SEAM[1]` plus motion | `SEAM[1]` | the counter (white; no magenta) |
| 2 | `02_never_flag` | 5.20 | 8.10 | `SEAM[1]` | `SEAM[2]` | the code card's lit line, then its output |
| 3 | `03_model_a` | 13.30 | 7.50 | `SEAM[2]` | `SEAM[3]` | the threshold |
| 4 | `04_box_flags` | 20.80 | 10.40 | `SEAM[3]` | `SEAM[4]` | the cell being named |
| 5 | `05_box_misses` | 31.20 | 6.50 | `SEAM[4]` | `SEAM[5]` | the cell being named |
| 6 | `06_where_accuracy` | 37.70 | 4.85 | `SEAM[5]` | `SEAM[6]` | the TN cell |
| 7 | `07_takeaway` | 42.55 | 6.25 | `SEAM[6]` | `SEAM[7]` (last frame of the Short, still) | none |

**1 Hook** — "This model is 99.5% accurate, but it's never caught a single
attack." Frame 0 is already the finished picture (the hook rule), so
`S(0)` is `SEAM[1]` with motion on top: the counter's value ticks up from
~99.0% to 99.5% over the first ~0.6 s (strings formatted `99.x%`, landing
exactly on `SC.LEDGER.accNever`), or the pile breathes with `userPulse`.
Pick one, and keep it subtle. On "99.5%": the value lands. On "never
caught": `pulseCaught` on 0 / 50. Still from ~4.9 s.

**2 Never flag** — "It's a prompt injection detector. 10,000 requests come
in, but only 50 are attacks. It never flags anything, and you're still
right 99.5% of the time." "prompt injection detector": `tagBright` up
then back down. "10,000 requests": `userPulse`. "only 50": `attackRing`.
"never flags": the counter goes compact (≥ 0.6 s), and once its label and
caught line are out, the code card fades in with line 3 (`pred =
torch.zeros…`) lit. "right": line 4 lit (line 3 off). "99.5%":
`out` 0→1 with `outHero` pulsing magenta on the output (line 4 off by then),
then back to teal. Ends `SEAM[2]`: nothing lit, output shown. Lines 1–2
are context and are never lit: they're on screen from the card's fade-in.

**3 Model A** — "Now, here's a real model. It flags 100 requests and
catches 40 of the 50 attacks, but its accuracy goes down to 99.3%." Card
out and counter back to full size first (by "real model"). "real model":
`thr` 0→1 (≥ 0.6 s). "flags 100": `flag` 0→1. "catches 40": caught ticks
0→40 (integers) by the end of "50 attacks". "goes down": value ticks
99.5% → 99.3% (one decimal, down through 99.4%), landing on "99.3%".

**4 The box, flags** — "So we look at the confusion matrix instead. A
true positive is I said there was an attack, and it was genuinely an
attack. A false positive is the model predicted attack, but it was a real
user." "confusion matrix": the counter fades out, then the box fades in
(`box.opacity`, empty cells, headers and row labels), and `thrDim` 0→1 as
the box takes the hero. "true positive": `lit.tp` 1 and `show.tp` 0→1 as
`fly.tp` 0→1 (≥ 1 s; the 40 gold dots travel). "false positive": `lit.tp`
→0, `lit.fp` 1, `fly.fp` 0→1, `show.fp` 0→1. Ends `SEAM[4]`.

**5 The box, misses** — "A false negative, I said user, but it was an
attack. And a true negative, I said user, and it was a user." "false
negative": lit fn, `fly.fn`, `show.fn`. "true negative": lit tn, `fly.tn`
(the teal pile streams in; ≥ 1.2 s), `show.tn`. Ends `SEAM[5]`.

**6 Where accuracy comes from** — "Now look where the accuracy comes from.
Almost all of it is true negatives. These are the easy ones." "accuracy":
hold on `SEAM[5]` (the move belongs to the next phrase). "true negatives": `split` 0.5 → 0.22 (both, ≥ 1 s, ease),
`show` of tp/fp/fn → 0 and `rowOpacity` → 0 in the first ~0.3 s of that
move (their text doesn't fit the slim cells), then `sub.tn` ["of 9,930",
0→1]. "easy ones": hold. Ends `SEAM[6]`.

**7 Takeaway** — "When positives are rare, we don't want to read the
accuracy. We want to look at the confusion matrix." "rare": `attackRing`
one pulse (the gold dots, in their cells). "read the accuracy": `sub.tn`
out, `split` back to 0.5 (≥ 1 s), then `show` of all four and `rowOpacity`
back to 1, `lit.tn` → 0. "confusion matrix": hold. Still for the last
~1 s. Ends `SEAM[7]`.

## Report

As in the HyperFrames brief: per beat, the cue constants with their word,
the mp4 path and measured duration, `check` errors / warnings, anything
changed from this brief and why, what you wished existed. Do not commit.
