# Beat-agent brief

**Name:** beat-agent-brief
**Description:** The contract a subagent gets when it builds one or two
beat scenes of a Short. The orchestrator pastes this file's path plus the
beat-specific brief (beat number, file and class name, `BEAT_SECONDS`, VO
with master times, the visual brief, the hero). Everything general lives
here so the per-beat brief stays short.
**When to use:** runbook step 6, every beat, every video.
**How it works:** read in the order below, build, render, review your own
contact sheet, report. You never edit `videos/_shared/`.

## Read first, in this order

1. `AGENTS.md` (hard rules), `videos/_shared/STYLE.md` (Shorts table, Manim
   traps), `videos/_shared/ANIMATION_RULES.md`.
2. `videos/_shared/PARTS.md`, then the parts the brief names (shared, or
   the video's local `_parts.py`). Reuse before building.
3. The latest finished beat in `videos/` as the worked example of shape:
   docstring with takeaway, VO and render line; cue constants with the VO
   word; `hold_until(BEAT_SECONDS)` at the end.
4. The video's `storyboard.md`: the "Final beats" table is the contract
   (start, length, file, class, VO); the beats table above it is the
   visual brief.

## Rules of the beat

- Subclass `BocShortScene`. One class per file, named as in `beats.json`.
  The 3-line `sys.path` shim at the top.
- `BEAT_SECONDS` is the beat's length to the millisecond. End with
  `self.hold_until(BEAT_SECONDS)`. Never overrun (the log warns).
- Frame 0 has the beat's content on screen and the first play starts
  motion. Last frame still and clean.
- One magenta hero, the one the brief names. Everything else teal, FG,
  FG_DIM, BG_PANEL.
- Land each change on the word that names it. Get cue times from the
  audio, not the brief: extract your window from `vo_final.wav` and run
  silencedetect or a 50 ms RMS envelope. Beat-local = master − start.
  Cues are named constants with the word in a comment.
- Only `S.QUICK` / `S.BEAT` / `S.HOLD` run times (multiples of HOLD for
  rides). A move the viewer tracks gets ≥ BEAT.
- `Text` via `transformer.label`, `_parts.mono`, or `Text(font=S.FONT)`;
  never LaTeX. All text ≥ `S.SHORT_LABEL_SCALE` (code text may use the
  code size) and inside `self.safe`. Nothing in `self.band` unless the
  brief says so.
- Layout budget: the stage is 7.38 × 7.25 units; a label at the floor is
  0.64 high and ~0.4 per character wide ("Feed Forward" is 5.1 wide).
  Count rows and widths before building; if it does not fit, say so in
  the report rather than shrinking text.
- Identity: `Transform` what stays the same thing; fade-swap what changes
  meaning. Parts with an `*_anim` or `fill_to` method keep identity for you.
- Manim 0.18.1 traps: negative `z_index` hides animating mobjects;
  `LaggedStart` over children of an already-added VGroup draws nothing;
  `set_opacity` on a stroke-only VMobject fills it; wrapping already-added
  mobjects in a new `VGroup` and animating it re-adds the group on top
  and hides labels (animate the parts in place); spaces are not glyphs.

## Render and review (from inside the video folder, one scene at a time)

```
cd videos/NNN-slug && uv run --no-sync manim -qh --disable_caching FILE.py Class
../../tools/review_frames.sh media/videos/FILE/1920p30/Class.mp4 4
ffprobe -v error -show_entries format=duration -of csv=p=0 media/videos/FILE/1920p30/Class.mp4
```

Open the contact sheet with the Read tool and look: text legible at phone
size, nothing in the dead zones or the band, one hero, frame 0 populated,
last frame still, duration within 1/30 s of `BEAT_SECONDS`. Fix and
re-render until it passes.

## Report (the orchestrator reads only this)

Per beat: cue constants with their VO word, the mp4 path and measured
duration, anything changed from the brief and why, anything you wished
existed in `_shared` (a part, a rule, a token). Do not commit.
