# Bits of Chris — Manim House Style

The palette tells a story: **teal is what you can see, magenta is what you reach in for.** Data is teal. The discovered structure (PC1, manifold axis, steering vector, gender axis) is magenta. Don't break this — it is the visual signature.

For *when and how* things should move (story, motion, frame, VO sync), see [`animation-rules.md`](animation-rules.md).

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
| Caption (16:9 or VO-less clip) | `self.show_caption("...")` then `self.hide_caption(t)` | top-center, fades in/out. Shorts with VO: captions are burned in by `tools/assemble.py`, scenes draw none |
| Math / symbols | `Text(..., font=S.FONT)` | no LaTeX on this machine: never `MathTex` / `Tex` / `DecimalNumber` |
| Wait beat | `self.beat("QUICK"/"BEAT"/"HOLD")` | 0.3 / 0.6 / 1.2s |
| Camera (3D) | already set in `Boc3DScene.setup()` | phi=70°, theta=-45° |

## Shorts (9:16) — when you want X, use Y

Subclass `BocShortScene` (1080x1920 @ 30 fps, frame 9 x 16 units, 1 unit = 120 px). Any `-q` flag renders at that size; output lands in `media/videos/<file>/1920p30/`.

| Want | Use | Notes |
|---|---|---|
| Where text / the hero may go | `self.safe` | YouTube UI covers top 12%, bottom 20%, right 12%; 4% left gutter |
| Where the visual goes | `self.stage` | upper two thirds of `safe`; `.move_to(self.stage)`, `scale_to_fit_width(self.stage.width)` |
| Caption (Short without VO) | `self.show_caption("2-4 words")`; with VO, captions are burned in by `tools/assemble.py` and scenes draw none | lower third of `safe` (`self.band`), `S.SHORT_CAPTION_SCALE`, bold on a dark pill (`S.CAPTION_PILL_*`) so it never reads as a diagram label; too wide -> two lines |
| Share the band with a scene element | element at the band top, `assemble.py --captions-anchor bottom` | burned captions sit just above the safe bottom (007 code cards) |
| Label next to a thing | `Text(...).scale(S.SHORT_LABEL_SCALE)` | the floor: ~98 px line height |
| Data dot | `data_dot(p, radius=S.DOT_SHORT)` | ~50 px across |
| Code on screen | `code_block(src, highlight=None)` | Menlo on BG_PANEL, literals teal, ~27 columns fit the safe width |
| Point at a line of code | `self.play(highlight_lines(code, 3), run_time=S.BEAT)` | magenta bar behind the line(s); same bar slides on later calls |
| A transformer block diagram | `transformer.build_block(self.stage)` | Embed → [Attention → (+) → FFN → (+)] N× → Linear; teal flow, marks FG_DIM; recolor `d.boxes` / `d.flow` / `d.skips` / `d.adds` / `d.bracket` for the hero. `GPT_SOURCE` + `MARK_LINES` is the matching code |
| Match the VO line length | `self.hold_until(BEAT_SECONDS)` at the end; `hold_until(t)` to land a change on a word | warns if the scene overran |
| A token's vector | `TokenColumn(values, digits=True)` | teal cells (+) / indigo (−), opacity = magnitude, `⋮` row; `col.animate.set_values(v)` ticks it in place |
| An L × d token matrix | `TokenMatrix(values)` | 3 signed one-decimal columns fit the safe width; one shared bracket pair |
| An update to a token | `TokenColumn(values, color=S.STRUCTURE, dots=False)` | the magenta thing that gets added |
| Attention between tokens | `attention_arcs(sources, target, weights)` | magenta arcs into one target, width = weight |
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
- Wrapping already-added mobjects in a new `VGroup(...)` and calling `.animate` on it re-adds that group at the top of the scene, so an opaque box panel covers its own label for the rest of the beat. Animate the existing parts in place (`*[b.box.animate... for b in d.boxes]`) or a group that is already in the scene family.
- The partial-movie cache can round a re-render one frame short of `hold_until`. Final renders use `--disable_caching`.
- Parallel `manim` runs in the same video folder race on `media/texts/` (half-written SVG -> `ParseError`) and the partial-movie cache. Render one scene at a time per folder.
- `FadeOut(VGroup(a, b))` on a *fresh* VGroup re-adds it on top of the scene, so a fading opaque panel dims whatever it covered. Fade already-added mobjects one `FadeOut` each.
- `mobject.become(other)` copies points, not attributes: a `Text` keeps its old `.text`. Set it yourself if code reads it (see `TokenColumn.set_values`).

## The isometric house look (HyperFrames Shorts)

The default look for a HyperFrames Short since 2026-10-04, from 009, 010 and
011, except linear algebra on a plane, which uses the flat 2D plane below. The code is `videos/_shared/web/iso/iso.js` (the world),
`videos/_shared/web/iso/diagram.js` (the transformer figure)
and `videos/011-jev-decision-models-iso/_jev/jev.js` (pillars, slabs, cards).

**The one question per element: is the viewer meant to see a thing, or read
a value?** See: an isometric object. Read: a flat, upright card. One beat may
hold both; the same information is never shown twice.

| When you want | Use |
|---|---|
| the ground every frame stands on | the navy floor grid (`ISO.ground`), in every beat, so the Short is one place |
| a model, a layer, a block, a head | a slab or ring with its name on the front face (`JV.slab`, `ISO.slabBack` / `slabFront`) |
| data passing through an operation | the object moves through the slab or ring; the one at work glows magenta |
| a quantity compared at a glance | height: a pillar or a tile (`JV.pillars`, `ISO.tray`) |
| numbers someone will read (a matrix, probabilities with values) | flat, upright digits on a card standing in the world (`ISO.makeCard`); not tiles alone |
| code, JSON, a token stream, a ticket, a chip, a counter | a flat card (`JV.card`, `mono` for code); never sheared |
| a label for an object | flat and upright beside it; lay text on a front face only for the object's own name |
| which column or choice something belongs to | one colour per token or choice, on the tile, the word and the digits alike (`ISO.COL.tokens`) |
| a figure from a paper, when the beat is about reading it | the figure with its own marks and direction, unchanged (`DG.draw`); objects may come out of it afterwards |
| the hero | one magenta mark per beat; it returns to its resting colour when the VO moves on |

What it keeps from the Manim look, because that is where the clarity came
from: one thing changes at a time, exact values are upright and large, and
the subject has empty space around it. What to leave alone: do not extrude
something only to make it isometric, and do not put a number on a slanted
surface.

## Linear algebra (HyperFrames Shorts)

From the Linear Algebra for Engineers series (`videos/002-linear-algebra-basics/`).
Vectors, bases and coordinates read on a **flat 2D number plane, not the
isometric floor** (Chris, ep01: "the ISO view doesn't work for these linear
algebra ones"). East is right, north is up, one grid square is one step.
The code is `videos/002-linear-algebra-basics/ep01-what-is-a-vector/_vec/vec.js`.

| When you want | Use |
|---|---|
| the space | the plane: grid one line per step, origin at the safe area's centre, at least ±2 steps in every direction, about 165 px per step (`VEC.floor`); a cramped plane was the first complaint |
| a vector the viewer should read as its numbers | the arrow from the origin plus the axes with a tick per step (`VEC.axes`) and dashed guides from the tip to its coordinates (`VEC.guides`); an arrow alone on a grid does not say "−2, 2" |
| an arrow | thin: `VEC.arrow` scales every width by `VEC.THIN` (0.6), so the hero is about a 31 px shaft at 165 px per step; at full weight Chris called them "a little too thick" |
| the hero arrow | colour alone; no halo or glow behind it (translucent rectangles along a diagonal read as "a fuzzy box") |
| more dimensions | more axes through the origin (lines, no arrowheads) for the one vector, never more arrows: a fan of arrows says "many vectors" (ep01 beat 7) |
| a 3D vector and a change of basis | a solid floor carrying one 2D grid (the first two basis vectors), a dashed stalk for height, the address as a route of legs tip to tail (`ep02-change-of-basis/_kit/basis.js`); never a full 3D lattice through the volume, which read as a mesh (ep02's first build, "way too confusing") |
| the old grid under a sheared new one | ghost alpha about 0.14; at 0.3 the two grids read as a triangle mesh |
| a 3D change-of-basis example | a basis whose third vector stays fixed, so the change is a floor shear (ep02: v1 = (0, −1, 0), v2 = (1, 1, 0), v3 = z) |
| camera motion across beats | none: a drift frozen at each beat's hold jumps 0.1–0.8° at every cut; move inside a beat and return to the canonical view before the hold |

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

## File layout

- `videos/<NNN>-<slug>/<scene>.py` — one Scene class per file.
- `videos/_shared/` — all reusable style/mobjects/scenes. Never duplicate constants.

## Render

Always from inside the video folder, one scene at a time (see `AGENTS.md`):

```
cd videos/001-pca-best-shadow && uv run --no-sync manim -qh --disable_caching shadow_3d.py BestShadow
```
