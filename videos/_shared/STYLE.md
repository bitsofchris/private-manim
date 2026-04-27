# Bits of Chris — Manim House Style

The palette tells a story: **teal is what you can see, magenta is what you reach in for.** Data is teal. The discovered structure (PC1, manifold axis, steering vector, gender axis) is magenta. Don't break this — it is the visual signature.

## When you want X, use Y

| Want | Use | Notes |
|---|---|---|
| Background | `S.BG_DEEP` | always; never plain black |
| A data point (2D) | `data_dot(p)` | teal, opacity 0.85 |
| A data point (3D) | `data_dot_3d(p)` | teal, opacity 0.85 |
| The hero direction | `hero_arrow(a, b)` / `hero_arrow_3d` | magenta, thick |
| A projection / residual | `residual(a, b)` | dashed, muted indigo |
| Axes (2D) | `BocAxes(...)` | dim, recedes |
| Grid plane | `BocNumberPlane(...)` | barely-there grid |
| Axes (3D) | `BocThreeDAxes(...)` | dim, recedes |
| Caption | `self.show_caption("...")` then `self.hide_caption(t)` | top-center, fades in/out |
| Math label | `MathTex(...)` | LaTeX defaults, set_color(S.FG) if needed |
| Wait beat | `self.beat("QUICK"/"BEAT"/"HOLD")` | 0.3 / 0.6 / 1.2s |
| Camera (3D) | already set in `Boc3DScene.setup()` | phi=70°, theta=-45° |

## Two-hero rule

Exactly **one** mobject (or one tightly-related VGroup) is magenta per beat. If everything is hero, nothing is. The rest is teal (data), muted (construction), or FG_DIM (labels).

`ACCENT_CYAN` and `ACCENT_PINK` are for transient pulses only — a sweep trail, a one-frame highlight. Never for static elements.

## Motion

- Three durations only: `QUICK` (0.3), `BEAT` (0.6), `HOLD` (1.2).
- Standard reveal: axes → data → caption fades in → hero appears with `Create` → caption fades out → `HOLD`.
- 3D ambient rotation rate: `S.CAM_AMBIENT_RATE` (0.12). Slower than default — the magenta hero needs time to land.

## Typography

- `Text(font=S.FONT, ...)` — Inter if installed, Pango falls back otherwise.
- Three sizes only: `CAPTION_SIZE`, `LABEL_SIZE`, `MATH_SM/LG`. Or use `.scale(S.CAPTION_SCALE)` etc. on `Text`.
- Math = LaTeX. Don't fight it.

## File layout

- `videos/<NNN>-<slug>/<scene>.py` — one Scene class per file.
- `videos/_shared/` — all reusable style/mobjects/scenes. Never duplicate constants.

## Render

```
uv run manim -pql videos/001-pca-best-shadow/shadow_3d.py BestShadow
```
