# Harness ep 2: the beat contract

**Name:** harness-ep02-beat-brief
**Description:** What every beat agent of "Give Your Agent a Map" gets on
top of `agents/beat-brief-hyperframes.md`.
**When to use:** runbook step 6 for this episode; the orchestrator's
spawn prompt names your beats and points here.
**How it works:** one world, drawn by `_kit/ep02.js`; each beat is a
`render(t)` that computes a state and calls `W.set(state)`. Seams are
fixed states in the kit, so parallel beats cut cleanly.

## Read, in order

1. `agents/beat-brief-hyperframes.md` (the general contract; it wins on
   anything not said here).
2. `storyboard.md` in this folder: the ledger, the beats table (the
   visual brief), and "Final beats" (start, length, VO). Your beat's
   length is `BEAT_SECONDS`, to the millisecond.
3. `_kit/ep02.js`: the parts, `EP2.EMPTY` (every state key and its
   default), `EP2.MAP`, `EP2.PILE` / `EP2.SPILL`, `EP2.SEAM`.
4. `00_layout/index.html`: the worked example of a beat on this kit.

## Set up a beat (from this folder)

```
mkdir NN_name && cd NN_name
ln -s ../../../_shared/web/vendor vendor && ln -s ../../../_shared/web/iso iso
ln -s ../../../_shared/web/cast cast && ln -s ../_kit kit
cp ../00_layout/index.html index.html     # then set data-duration, BEAT_SECONDS, render(t)
```

Scripts load in this order: `vendor/gsap.min.js`, `iso/iso.js`,
`cast/cast.js`, `kit/ep02.js`. The literal
`window.__timelines["main"] = ISO.start(BEAT_SECONDS, render)` stays in
your `index.html`.

## Rules of this episode

- **Seams.** Frame 0 is exactly `W.set(EP2.SEAM[n-1])` (beat 1: `EP2.MAP`
  with `arrows: [0.15, 0.15, 0.15]` and moving). Your last ≥ 0.3 s is
  exactly `W.set(EP2.SEAM[n])`, still. Beat 8 ends on the state in its
  brief. Interpolate between states yourself (numbers with `EP2.lerp`,
  colours by the 0..1 hero/rot keys); `fileXY` arrays may be tweened per
  file.
- **Cues** come from `words.json` (master seconds; beat-local = master −
  your start). Name them at the top of the script with the word in a
  comment. Check the ones that land a hero on a 10–50 ms RMS envelope of
  your window of `vo_final.wav`.
- **One magenta hero at a time**, the one the storyboard names for your
  beat; it may pass on a named word, the old one returns to rest.
- **The kit is the orchestrator's.** Do not edit `_kit/`, `00_layout/`,
  another beat's folder, or anything outside this episode folder. A part
  the kit lacks: draw it in your own `index.html` (into `W.svg`, or DOM
  text into `root`) and name it in your report.
- Text is DOM, ≥ 60 px, weight 800; monospace is set from the script
  (`el.style.fontFamily = "monospace"`). Nothing in the caption band
  (y > 1100). No LaTeX.
- Render only from your own beat folder, one render at a time:
  `npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_name.mp4`
  (with `HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1`), after
  `check` reports 0 errors.
- Review your own contact sheet (`../../../tools/review_frames.sh
  media/hf/NN_name.mp4 4` from this folder) and compare your frame 0 with
  the previous beat's last frame if its mp4 exists.
- Do not commit. Report as the general brief says.
