# private-manim

3blue1brown-style explainer shorts in Manim Community 0.18.1. One folder per
video under `videos/<video-name>/`. Each video folder owns its own `media/`
subdirectory for rendered output.

## House style — hard rules

1. **Always import from `videos._shared`.** Never hardcode colors, fonts, beat
   durations, camera angles, or stroke widths in scene files. If a constant
   is missing from `videos/_shared/style.py`, add it there first, then use it.
2. **Two-hero rule.** Teal (`S.DATA`) is the data you can see. Magenta
   (`S.STRUCTURE`) is the discovered direction (PC1, manifold axis, steering
   vector). One magenta hero per beat. This is the visual signature.
3. **Subclass `BocScene` (2D) or `Boc3DScene` (3D)** from `videos._shared.base`.
4. **Use the preconfigured mobjects** (`data_dot`, `data_dot_3d`, `hero_arrow`,
   `hero_arrow_3d`, `residual`, `BocAxes`, `BocNumberPlane`, `BocThreeDAxes`)
   for those roles — never raw `Dot` / `Arrow` / `Axes`.
5. **Three motion durations only:** `S.QUICK` / `S.BEAT` / `S.HOLD`. Call
   `self.beat("QUICK"|"BEAT"|"HOLD")`, never `self.wait(0.45)`.
6. **Captions** via `self.show_caption(...)` and `self.hide_caption(t)`.

See `videos/_shared/STYLE.md` for the "when you want X, use Y" table.

## Scene template

```python
"""One-sentence viewer takeaway.

Render:
    cd videos/<dir> && uv run manim -pql <file>.py <SceneClass>
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import Boc3DScene
from videos._shared.mobjects import data_dot_3d, hero_arrow_3d, BocThreeDAxes

class MyScene(Boc3DScene):
    def construct(self):
        ...
```

The 3-line `sys.path` shim is required because we render from inside each
video folder (see below) — without it, `videos._shared` is not importable.

## Rendering

ALWAYS `cd videos/<video-name>/` before running `manim`. Manim writes output
to `./media/` relative to cwd; running from the repo root scatters renders
into a top-level `/media/` and breaks the one-folder-per-video rule.

Correct:
    cd videos/pickle-pirate-gemma
    uv run manim -pql blog07_composition.py BlogComposition

Wrong (creates /media/ at repo root):
    uv run manim -pql videos/pickle-pirate-gemma/blog07_composition.py ...

## Re-renders overwrite

Manim's output path is `media/videos/<source_file>/<quality>/<ClassName>.mp4`.
Re-rendering the same scene overwrites the previous file. To keep an old take,
rename the Python class (or copy the file out） before re-rendering.

## Top-level /media/ is not used

If you see `media/` at the repo root, it's from a render run with the wrong
cwd — move its contents into the matching `videos/<video-name>/media/` and
delete the root folder.

## Shorts (YouTube, 9:16)

Full process, research, and tools: `docs/shorts-runbook.md`.

Audio first: storyboard -> record VO -> time each beat -> one scene per beat
-> assemble. Full process in `docs/plans/shorts-pipeline.md`; layout table in
`videos/_shared/STYLE.md` ("Shorts (9:16)").

- Subclass `BocShortScene`. It forces 1080x1920 @ 30 fps (frame 9 x 16 units)
  whatever `-q` flag you pass, so output is always
  `media/videos/<file>/1920p30/<Scene>.mp4`.
- Safe area: YouTube's UI covers the top 12%, bottom 20%, right 12%. Text and
  the magenta hero stay in `self.safe`; the visual goes in `self.stage`;
  backgrounds may bleed to the frame edge. Fill the frame.
- Captions go in the lower third of the safe area (`self.show_caption`),
  2 to 4 words, never the top. Readable text >= 1/20 frame height.
- Frame 0 has content on screen and motion starts immediately.
- Each beat ends with `self.hold_until(BEAT_SECONDS)` so the render matches
  its VO line.

```
cd videos/004-backprop-short
uv run --no-sync manim -qh 01_hook.py Hook
../../tools/review_frames.sh media/videos/01_hook/1920p30/Hook.mp4 4   # contact sheet, look at it
cd ../.. && uv run --no-sync python tools/assemble.py videos/<slug>/beats.json \
    --vo videos/<slug>/vo.m4a --captions videos/<slug>/captions.json -o videos/<slug>/media/short.mp4
uv run --no-sync python -m unittest discover -s tests -v   # tests (no pytest installed)
```

## Other conventions

- Data first: synthesize with `np.random.default_rng(S.SEED)`. Use
  `sklearn.decomposition.PCA`, never hand-roll eigen.
- Use `axes.c2p(...)` for every coordinate. Never hardcode scene coords.
- Group related mobjects in `VGroup`s. Use `always_redraw` + `ValueTracker`
  for sweeping parameters.
- One Scene class per file. Keep files under ~120 lines.
