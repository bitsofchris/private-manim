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
| Share the band with a scene element | element at the band top (bottom edge ≤ y 1330), `assemble.py --captions-anchor bottom` | burned captions sit just above the safe bottom (007, ep03 code cards). While the element is up every caption must fit one line: a two-line caption grows upward into it (ep03 split "the input direction"). `captions_from_transcript.py` keeps every caption to 15 characters, one line (013) |
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

- The Short's frame 0 (the hook beat): something is on screen and something is moving by frame 1. No title card, no empty dark opener. Later beats follow `agents/animation-rules.md` rule 1: only what the VO names moves, and a beat may hold still until its first cue (012 ep03).
- Readable text has one floor per engine, both passed on a phone: Manim, nothing smaller than `SHORT_LABEL_SCALE` (~1/20 of frame height, ~96 px line height); HyperFrames, 60 px font-size, weight 800 (`agents/beat-brief-hyperframes.md`, "Layout, in pixels").
- One caption at a time, on one line, always in the band (VO captions: `captions_from_transcript.py`, ≤ 15 characters; a scene's own captions: 2 to 4 words). Burned-in VO captions from `tools/assemble.py` use the same band, so a beat uses scene captions or VO captions, not both.
- **The scene changes about every 5 s.** The message comes first, but a
  Short that holds one image for 20 s loses the scroller (Chris, 014
  ep01: the loop image held for 26 s, "we should be changing between the
  scenes a little bit quicker"). A video may have only two or three
  images, and they may come back as often as the VO returns to them;
  what matters is that something new is on screen every ~5 s: a flip to
  the code card and back, the machine, the loop. Plan it in the
  storyboard's beats table: no run of beats on one image longer than
  ~6 s unless that image is itself moving through distinct states. The
  seam-state kit makes a return to an image cheap (the state is data),
  so reuse images rather than inventing more.
- **A part arrives when the VO names it.** Frame 0 shows what line 1
  talks about, not every part the Short will use. A part the VO first
  names later (016 ep01's CPU, named at 14 s) is off screen until then
  and fades in on its word, even when the series image has a slot for it.
  Chris, 016 ep01: the CPU box parked in the top slot from frame 0 "we
  don't need sitting there".
- **An equation sits next to the picture it describes.** When the VO
  ties a formula to a drawing (`y = x @ W` and the network layer it
  is), stack them, the formula directly under the drawing, and let the
  shared image (the chip) shrink for those beats; light the matching
  parts together (an output node with its y column and its incoming
  edges with W's column). A beat that hands the stage back moves the
  formula to its usual slot on the next named change. Chris, 016 ep01:
  the network in the top slot and the formula in the bottom slot read as
  two things; stacked, with the GPU at 0.8×, they read as one.

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
| the hero | one magenta mark at a time (`AGENTS.md` rule 2); it returns to its resting colour when the VO moves on |

What it keeps from the Manim look, because that is where the clarity came
from: one thing changes at a time, exact values are upright and large, and
the subject has empty space around it. What to leave alone: do not extrude
something only to make it isometric, and do not put a number on a slanted
surface.

## Linear algebra (HyperFrames Shorts)

From the Linear Algebra for AI Engineers series (`videos/002-linear-algebra-basics/`).
Vectors, bases and coordinates read on a **flat 2D number plane, not the
isometric floor** (Chris, ep01: "the ISO view doesn't work for these linear
algebra ones"). East is right, north is up, one grid square is one step.
The code is `videos/_shared/web/vec/vec.js` (linked into a beat as `vec/`); start a beat from `prototypes/hyperframes/vec-plane/index.html`.

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
| numbers that don't fit one scale (e1 at 1 step and x @ W at 4) | a few named camera views, each beat moving between them on the words that call for it and starting in the view the last one ended in (`VEC.view(A, B, u)`; ep03: NEAR 300 px per step under the card, FAR 160 px for the recipe, MID centred) |

### Vectors and matrices as numbers

The default for every video that shows a tensor's numbers (Chris, ep04: the
first layout boxed every number and "looks kind of like a table, and it
loses that sort of matrix notation"). One notation, close to what PyTorch
prints, so a frame reads like a tensor from a notebook. Deviate when it
clearly helps that video, and say why in its storyboard. The code is
`videos/_shared/web/vec/vec.js` (`VEC.grid`, `VEC.brackets`, `VEC.vecCard`,
`VEC.codeCard`, `VEC.hbox`).

| When you want | Use |
|---|---|
| a vector (1-D) | one horizontal row in square brackets with commas: `[ 1, 2, −1 ]`; the row-vector (PyTorch) convention |
| a matrix (2-D) | bare numbers in a tight grid inside one tall pair of square brackets; no commas, no box per number (009's readout card, ep01's brackets) |
| its name and shape | the name above in `--dim` (`W`), the shape beside or under it as PyTorch prints `.shape`: `(3, 2)`, never "3×2" |
| code | monospace, only for literal code (`x @ W`, `nn.Linear(3, 2)`, `.T`); the math stays in Inter. How to set it so it renders: the monospace trap in `agents/beat-brief-hyperframes.md` |
| a number | a true minus sign (−1); decimals only where the value has them (0.5, 4.1), never `2.0` |
| colour | digits carry the meaning: one categorical colour per row when rows matter (rows of `W`, rows of a batch `X`); brackets `--dim`; the one hero gets magenta digits and brackets |
| to point at an entry, row or column | its digits turn magenta (a highlight box behind them if colour alone is not enough), then back; at rest it is notation, not a table |
| a matrix acting on the plane | the matrix is on screen whenever the VO says "this matrix" or the plane moves because of it, and the row doing the work lights while its direction moves (Chris, ep03: "show a matrix for the transformation we're about to show"; "emphasize the row as you move e1 and e2") |
| a vector used as a column | only as a visible move ("turn x sideways") and only for that step; the row is the default |
| a big tensor (a batch, an embedding) | at most about 4 × 4 numbers, then `⋯`, with the shape saying the size |
| a batch as an icon (a card, a glyph on a track) | still digits: two or three rows of the ledger's readout in brackets, or in the card's own rounded outline when there is no room for brackets (014's `_kit/machine.js` `readout`); never a stack of squiggles, which reads as decoration, not data (Chris, 014 ep 1) |
| a row and its geometry | the row's colour on its arrow from the origin on the plane, so "rows are where input directions land" is visible |

## Agents and knowledge bases (HyperFrames Shorts)

From the Harness Engineering series (`videos/012-harness-engineering/`,
look locked by Chris 2026-10-17). Line-drawn people and flat outlined
props on the house background. The code is `videos/_shared/web/cast/cast.js`
(linked into a beat as `cast/`, after `iso/`); start a beat from
`prototypes/hyperframes/cast/index.html`.

| When you want | Use |
|---|---|
| a person | `CAST.human`: the quiz stick figure, round head, dot eyes, a face (`smile` / `flat` / `frown`) |
| an agent | `CAST.agent`: the same body with a rectangle head and `1` and `0` for eyes, the only teal on it; never a robot icon or a new body |
| cleanup, the janitor | `CAST.janitor`: an agent with a broom, not a new character |
| what agents write | `CAST.page`: a teal page, a hash on top, dense lines; it reads as "not for you" |
| what the human reads | `CAST.board`: one ink board of cards (the human layer) |
| rules, the map, goals | `CAST.vitrine`: the glass case; make one item the hero with `CAST.hero(part.items.map, true)` |
| an index that points | `CAST.mapCard`: a short card with arrows to teal files; dashed muted files are the ones it does not point to |
| the model and its harness | `CAST.blob`: the model (dim at rest) with four teal pipes in `CAST.PIPES` order (context, tools, memory, loop); light one pipe, or the body, at a time. Or the agent wearing its harness (head = model, the four parts carried): ep01's `_kit/rig.js` |
| motion | poses as numbers in `render(t)` (`CAST.pose`: arm angles from straight down, `lean`, `tilt`); every move lands on its word and stops before the hold |

Colour jobs stay the house ones: teal is what agents write and data,
magenta is the one thing the beat points at, ink is people and structure.

## Two-hero rule

The rule is `AGENTS.md` hard rule 2: one magenta hero on screen at a time. If everything is hero, nothing is. The rest is teal (data), muted (construction), or FG_DIM (labels).

A shared part is never magenta at rest: the beat makes one thing the hero, so a kit that draws a part magenta by default leaves a second magenta on screen whenever a sub-part is named. 012 ep01 had to redraw `CAST.blob`'s magenta model dim before a pipe could be the hero; the kit's blob now rests dim.

`ACCENT_CYAN` and `ACCENT_PINK` are for transient pulses only — a sweep trail, a one-frame highlight. Never for static elements.

## Motion

- Three durations only: `QUICK` (0.3), `BEAT` (0.6), `HOLD` (1.2).
- Standard reveal: axes → data → caption fades in → hero appears with `Create` → caption fades out → `HOLD`.
- 3D ambient rotation rate: `S.CAM_AMBIENT_RATE` (0.12). Slower than default — the magenta hero needs time to land.

## Typography

- `Text(font=S.FONT, ...)` — Inter if installed, Pango falls back otherwise.
- Three sizes only: `CAPTION_SIZE`, `LABEL_SIZE`, `MATH_SM/LG`. Or use `.scale(S.CAPTION_SCALE)` etc. on `Text`.

### Code on screen (every engine)

Chris, 014 ep01 (2026-10-28): "have it follow like a VS Code style
coloring, so it's not just purple", and "simulate the typing like a human
when it makes sense". In HyperFrames, use the shared code card,
`videos/_shared/web/code/code.js` (`CODE.make` with `look: "dark+"`,
`CODE.typedAt`, `CODE.typingSeconds`; `agents/parts.md`); link it, don't
copy it. In Manim, match its colours and rhythm.

| When you want | Use |
|---|---|
| code that reads as code | VS Code Dark+ colours on the panel: keywords `#569CD6`, calls `#DCDCAA`, names `#9CDCFE`, numbers `#B5CEA8`, strings `#CE9178`, comments `#6A9955`, punctuation `#D4D4D4`, classes `#4EC9B0`; never one block of ink, never magenta text for the whole line |
| the hero line | a magenta bar in the gutter and a lighter row (`rgba(192,132,252,0.12)`); the text keeps its colours, so the one-magenta-hero rule still holds |
| code appearing while the VO talks about it | type it like a person: uneven per-character pace (0.45–1.55× the mean at ~22 cps), spaces quick, a 2.5× pause at each line break, a blinking block cursor until the last line lands, then cursor off and still. Plan the cue with `SC_typingSeconds` so the last line lands before the VO moves on. If the typing outruns the line that names the code, raise the pace to ~30 cps at most, then hold the card through the next line and flip back on the line that returns to the other image (014 ep02: four lines took 2.6 s at 30 cps, so the card held through "Your dataset sits at the front" and flipped back on "All it knows") |
| code that is already there when the beat starts, or a card shown as a reference | no typing; the card is fully typed from frame 0 and the hero bar moves with the VO |

## File layout

- `videos/<NNN>-<slug>/<scene>.py` — one Scene class per file.
- `videos/_shared/` — all reusable style/mobjects/scenes. Never duplicate constants.

## Render

Always from inside the video folder, one scene at a time (see `AGENTS.md`):

```
cd videos/001-pca-best-shadow && uv run --no-sync manim -qh --disable_caching shadow_3d.py BestShadow
```
