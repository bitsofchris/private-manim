
# Repo

Make a folder per video in videos/. Number them with leading 0s 001





# Prompt

You are building a 3blue1brown-style explainer scene using Manim Community
(`from manim import *`). Target a ~30–60s clip at 1080p.

CONTEXT
- I'm teaching a specific PCA / manifold intuition. The scene name and goal
  are at the top of the file as a docstring — that is the single source of
  truth for what the animation must show.
- Audience: someone who knows basic linear algebra but hasn't internalized
  PCA. Prefer one clear visual beat over many.

CODING RULES
- One Scene class per file. Subclass `Scene` for 2D, `ThreeDScene` for 3D.
- Data first: synthesize small (<1000 pt) numpy arrays with a fixed seed.
  Use `sklearn.decomposition.PCA` for PCs — do not hand-roll eigen.
- Use `axes.c2p(...)` for every coordinate. Never hardcode scene coords.
- Animate with `self.play(...)` in clean beats separated by `self.wait(0.5)`.
- Group related mobjects into `VGroup`s so later scenes can transform them.
- Use `always_redraw` + `ValueTracker` for anything that sweeps a parameter.
- Keep the file under ~120 lines. Refactor shared helpers into `utils.py`.

VISUAL STYLE
- Dark background (default). Accent color for the "hero" object only.
- Label axes with `MathTex`, not `Text`. Captions top-center.
- For 3D: `set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)` as a
  default, and `begin_ambient_camera_rotation(rate=0.15)` for reveals.
- For linear transforms: show the grid first, then `ApplyMatrix(M, grid)`,
  then annotate what M was (e.g., rotation to PC1 basis).
- When showing text like for a definition - show it, then fade it out so it's not distracting the viewer

API I EXPECT YOU TO USE
Axes, ThreeDAxes, NumberPlane, Dot, Dot3D, VGroup, Arrow, Arrow3D, Line,
DashedLine, ParametricFunction, Surface, BarChart, ApplyMatrix,
ValueTracker, always_redraw, MathTex, Tex, LaggedStart, Transform,
ReplacementTransform, Rotate, FadeIn, FadeOut, Create, c2p,
set_camera_orientation, begin_ambient_camera_rotation, move_camera.

DELIVERABLE
1. A runnable `.py` file under `scenes/<scene_name>.py`.
2. A one-line `manim -pql scenes/<scene_name>.py <ClassName>` command.
3. A short comment block at top: what the viewer should understand after
   watching.

NOW BUILD: <paste the specific scene description from the list of 10>.