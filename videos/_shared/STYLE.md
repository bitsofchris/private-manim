# Bits of Chris — Manim House Style

The palette tells a story: **teal is what you can see, magenta is what you reach in for.** Data is teal. The discovered structure (PC1, manifold axis, steering vector, gender axis) is magenta. Don't break this — it is the visual signature.

For *when and how* things should move (story, motion, frame, VO sync), see [`ANIMATION_RULES.md`](ANIMATION_RULES.md).

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

## Shorts (9:16) — when you want X, use Y

Subclass `BocShortScene` (1080x1920 @ 30 fps, frame 9 x 16 units, 1 unit = 120 px). Any `-q` flag renders at that size; output lands in `media/videos/<file>/1920p30/`.

| Want | Use | Notes |
|---|---|---|
| Where text / the hero may go | `self.safe` | YouTube UI covers top 12%, bottom 20%, right 12%; 4% left gutter |
| Where the visual goes | `self.stage` | upper two thirds of `safe`; `.move_to(self.stage)`, `scale_to_fit_width(self.stage.width)` |
| Caption | `self.show_caption("2-4 words")` | lower third of `safe` (`self.band`), `S.SHORT_CAPTION_SCALE`; too wide -> two lines |
| Label next to a thing | `Text(...).scale(S.SHORT_LABEL_SCALE)` | the floor: ~98 px line height |
| Data dot | `data_dot(p, radius=S.DOT_SHORT)` | ~50 px across |
| Code on screen | `code_block(src, highlight=None)` | Menlo on BG_PANEL, literals teal, ~27 columns fit the safe width |
| Point at a line of code | `self.play(highlight_lines(code, 3), run_time=S.BEAT)` | magenta bar behind the line(s); same bar slides on later calls |
| Match the VO line length | `self.hold_until(BEAT_SECONDS)` at the end; `hold_until(t)` to land a change on a word | warns if the scene overran |
| Check layout | `self.show_guides()` while iterating, then `tools/review_frames.sh <mp4>` | delete the guides call before the final render |
| Fill the frame | backgrounds / panels may bleed past `safe` to the frame edge | text and the magenta hero never do |

Rules that are specific to Shorts:

- Something is on screen at frame 0 and something is moving by frame 1. No title card, no empty dark opener.
- Readable text is at least ~1/20 of frame height (96 px). Nothing smaller than `SHORT_LABEL_SCALE`.
- One caption at a time, 2 to 4 words, always in the band. Burned-in VO captions from `tools/assemble.py` use the same band, so a beat uses scene captions or VO captions, not both.

### Manim 0.18.1 gotchas found building the Short pipeline

- A negative `set_z_index` hides a mobject while it is being animated. Layer by `self.add()` order instead.
- `LaggedStart(*[Create(c) for c in group])` over the children of a VGroup that is already in the scene renders nothing. Use `Create(group, lag_ratio=...)` on the group.
- No LaTeX on this machine: `Text` only, never `MathTex` / `Tex` / `DecimalNumber`.

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
