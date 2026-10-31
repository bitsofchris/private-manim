# Parts: what exists to reuse

**Name:** parts inventory
**Description:** Every reusable visual in this repo, shared or still local
to one video, with where it lives and which videos used it. Read before
storyboarding a beat so the visual brief says "reuse X" instead of
describing X from scratch.
**When to use:** storyboarding (step 1), briefing beat agents (step 6),
the update pass (step 11, update the use counts).
**How it works:** shared parts live in `videos/_shared/*.py` and are
imported by any video. Local parts live in a video's `_parts.py` (or
`_<thing>.py`) and are imported only by that video's scenes. A local part
is promoted to `_shared` the second time another video wants it: move it,
add a test under `tests/`, update this table. Retired parts go to
`videos/_graveyard/`.

## Finding things

- Shared code: `grep -n "^def \|^class " videos/_shared/*.py`
- Local parts: `ls videos/*/_*.py`, and each file's docstring says what it
  holds and how to call it.
- Scene docstrings start with the beat's one-line takeaway and the VO, so
  `grep -l "residual" videos/*/0*.py` finds the beat that animated it.

## Shared (`videos/_shared/`)

| Part | Where | What | Used by |
|---|---|---|---|
| `BocShortScene` | `base.py` | 9:16 scene with `safe` / `stage` / `band`, `hold_until`, `show_guides` | every Short |
| `BocScene`, `Boc3DScene` | `base.py` | 16:9 scenes, captions, `beat()` | 001–003, pickle-pirate |
| `short_caption` | `base.py` | bold caption on a dark pill in the band; used by `assemble.py` | all Shorts |
| `data_dot`, `data_dot_3d` | `mobjects.py` | teal data point | everywhere |
| `hero_arrow`, `hero_arrow_3d`, `residual` | `mobjects.py` | magenta direction, dashed projection | 001–003 |
| `BocAxes`, `BocNumberPlane`, `BocThreeDAxes` | `mobjects.py` | dim axes and grid | 001–003 |
| `code_block`, `highlight_lines` | `mobjects.py` | code card with a sliding magenta bar | 003, 007 |
| `build_block` (transformer diagram) | `transformer.py` | Embed → [Attention → ⊕ → FFN → ⊕] N× → Linear, named parts; `GPT_SOURCE` + `MARK_LINES` | 006, 007, 008 |
| `label`, `op_box`, `flow_arrow`, `add_node` | `transformer.py` | phone-size label, diagram box, teal arrow, ⊕ node | 006–008 |
| 2D number plane kit (HyperFrames) | `web/vec/vec.js`, linked as `vec/` | camera `view(A, B, u)`; `floor`, `axes` (ticks from the view's extents), `guides`, `arrow` (thin), `line`, `puck`, `spot` (landing ring), `lattice` (a matrix's grid); row-vector `map` / `basisTo` / `comb`; DOM `label` / `place`, `vecCard`, `grid` + `brackets` (matrix notation), `cell`, `hbox`, `codeCard`, `code`. Starter: `prototypes/hyperframes/vec-plane/`. Tests: `tests/test_vec_kit.py` | ep01, ep03, ep04 (each shipped with its own copy) |
| Agent and knowledge-base cast (HyperFrames) | `web/cast/cast.js`, linked as `cast/` | SVG `layer`; figures `human`, `agent` (1 and 0 eyes), `janitor` (agent + broom) with `pose` / `hand` / `face` / `blink`; props `page` (agent notes), `board` (human layer), `vitrine` (curated case: `items.rules / map / goal`), `mapCard`, `blob` (the model + four `PIPES`); `hero(part, on)`, `place`, `show`. Starter: `prototypes/hyperframes/cast/`. Tests: `tests/test_cast_kit.py` | 012 (built for the series, 2026-10-17) |

## Local, candidates for promotion (second use promotes)

Paths in this table are relative to `videos/`.

| Part | Where | What | Used by | Uses |
|---|---|---|---|---|
| `ProbBars`, `text_card`, `chip_text`, `mono` | `008-jev-decision-models/_parts.py` | probability bars that refill in place, mono card, option chip | 008 | 1 |
| `net_glyph`, `counter_text`, token stream | `008-jev-decision-models/03_onepass.py` | tiny 3-box network, pass counter, glyph-by-glyph typing | 008 | 1 |
| `code_card` | `007-diagram-to-pytorch/_code.py` | lines of `GPT_SOURCE` as a card in the band | 007 | 1 |
| `ghostify` | `007-diagram-to-pytorch/_ghost.py` | fade a group without the stroke-only fill trap | 007 (006 has its own copy) | 2 → promote |
| `restroke`, `outline` | `007-diagram-to-pytorch/_marks.py` | recolor box outlines without hiding labels | 007 | 1 |
| neuron, tiny net | `004-backprop-short/02_neuron.py`, `01_hook.py` | the single neuron and the small layered net | 004 | 1 |
| loss bowl | `004-backprop-short/_bowl.py` | the loss surface bowl with a rolling ball | 004 | 1 |
| computational graph | `004-backprop-short/_graph.py` | micrograd-style value nodes with data/grad | 003, 004 | 2 → promote |
| token matrix | `005-transformer-short/_tokens.py` | L×d token columns, attention arcs | 005 | 1 |
| decision loop + diamonds | `008-jev-decision-models/04_agents.py` | agent loop ring with labelled decision diamonds | 008 | 1 |
| paper-figure cross-fade + zoom | `006-diagram-grammar/02_grammar.py` | real figure in, zoom to a region, our diagram over it | 006 | 1 |
| plane-kit wishes not yet in `web/vec/` | ep01–ep04 beats | `compass()`; a card slot `swell`; a card that grows and wraps (ep01 `listCard`); fit-to-width text (ep01 `fitSize`); label offsets per view that avoid the band and the left dead zone; a recipe drawer with hop ticks (ep03 `tick`, `hops`); a ring of vectors (ep03 beats 7–8) | ep01, ep03 | 1 each |
| 3D basis kit (HyperFrames) | `002-linear-algebra-basics/ep02-change-of-basis/_kit/basis.js` | floor-and-route world (`BK.world`, `route`, `floorGrid`, `coordsAt`), the address readout `makeReadout` (ticking numbers, one colour per basis vector), `makeBasisLabels` | ep02 | 1 |
| Score line + confusion box (HyperFrames) | `013-classifier-metrics/ep01-accuracy-trap/_kit/score.js` (+ `make_dots.py` → `dots.js` from seeded scores) | 10,000 requests as a dot plot on a 0 → 1 axis (users above, attacks below, soft-capped pile), the magenta threshold, flagged rings; the 2×2 box whose dots fly from the line into their cells and whose cells swell (`split`); counter; `SC.mount(root)` → `draw(g, S)` from one state object, `SC.SEAM` | 013 eps 1–5 (each its own copy). The plot is ep04's `ep04-auc-pr-curve/_kit/score.js`: real 0–1 ROC / PR axes, one point list carrying both positions so `m` morphs ROC → PR point by point, area fill (polygon / AP steps), dashed baselines, the threshold's point, axis names that trade places | 5 → promote to `web/` when a new series reuses it |
| Agent wearing its harness (HyperFrames, on the cast kit) | `012-harness-engineering/ep01-what-is-a-harness/_kit/rig.js` | `RIG.make` (agent whose head is the model, drawn dim; context pages above, terminal in the right hand, drawer in the left, loop arrow round the feet; `missing` parts dashed), `part(rig, i, u, pop)` teal→magenta with its label, `place`, `follow` (held parts track `CAST.pose`), `partAt` / `headAt` / `loopAt`, verdicts `check` / `circling` + `spin` | 012 ep01 | 1 |
| Dataloader machine (HyperFrames) | `014-pytorch-dataloading/_kit/machine.js` (+ `data.js`, the ledger) | the Dataset card, samples hopping as bracketed rows on the master clock (`SC.clock`), the DataLoader's four stations (sampler indices, fetch workers, batching `×N` read from `S.shape`, collate), the `[32, 512]` batch card, the model chip, map / iterable modes, twins (hero `"twins"` lights both cards); `SC.mount(root)` → `draw(null, S)`, `parts`, `SC.REST`, each episode's `SC.SEAM`. No `pulse` or label handles yet (`parts.sampler.dom[1]` is the indices); the `__getitem__` label touches the Dataset card's right border, so swell it from its right centre | 014 eps 1–5 (one shared copy) | 5 |
| Code card with a typist (HyperFrames) | `014-pytorch-dataloading/_kit/code.js` | VS Code Dark+ tokens, the hero line's gutter bar, `SC_typedAt` / `SC_typingSeconds` (human-paced typing), `S.flip` crossfade from the machine; a line over 28 characters sets every row smaller to fit (48 × 28 / length) | 014 eps 1–5; 016's `_kit/code.js` is an adapted copy (docked card, shrink-to-fit) | 2 → promote to `web/code/` |

## HyperFrames prototypes (copy, do not import)

An agent copies a piece from a prototype into its beat's `index.html`.
Nothing here becomes a template until a real video needs it twice (the same
promotion rule as Manim parts). The one shared script so far is 009's
isometric kit, `videos/_shared/web/iso/iso.js` (3 uses: 009, 010, 011): the
projection `ISO.P`, `box`, `ground`, `shadow`, the `tray` of tiles coloured
by token, ring slabs in two halves (`slabBack` / `slabFront`), the readout
`makeCard`, `label`, `guides`, `start`. It was promoted to `videos/_shared/web/iso/`
at its second use, with the transformer figure `diagram.js` beside it; the
helpers beats wrote locally and that could join it are listed in the
changelog (2026-10-04).
Paths below are under `prototypes/hyperframes/`.

| Piece | Where | What |
|---|---|---|
| stick figure, pose by tweens | `quiz/index.html`: `#fig` group, `arms()`, `face()` | standing figure; arm rotations about the shoulder, mouth/eye swaps, hops |
| stick figure, pose by function of `t` | `ironies/index.html`: `#fig`, `ik()`, the pose block in `render(t)` | seated figure; two-bone arm IK to any hand target, lean, slump, gaze |
| sketch / boil filter | `quiz`: filters `#w0`–`#w2` cycled by `tl.set` at 4 fps; `ironies`: one `#sketch` filter whose seed `render(t)` steps | hand-drawn wobble on everything inside the filtered group |
| caption pill | `.caption` CSS + the `.clip caption` divs in either file | VO-less clips only; with VO the band stays empty |
| `?guides` safe-area overlay | `ironies`: `#guides` (four shaded dead zones); `quiz`: `#guides` (dashed safe rectangle) | preview with `?guides` to check layout |
| `render(t)` driver | `ironies/index.html`: `driver` object + `hash()` | procedural drawing as a pure function of time, re-run on every seek; deterministic noise |
| vendored GSAP + Inter | `videos/_shared/web/vendor/`, linked as `vendor/` | the offline `<script>` and `@font-face`; see its README |
| house-style matrix + block panels | `stack-styles/00_house/index.html` | the Manim stack beat rebuilt as DOM: bracketed matrix, teal cells, panels, magenta flow line |
| a starting file that passes `check` | `stack-styles/_scaffold/index.html` | root attributes, `DATA` / `CUE`, `render(t)`, guides, timeline registration |
| ten other looks for one beat | `stack-styles/NN_slug/index.html` | riso, blueprint, oscilloscope, editorial, Swiss, isometric, paper collage, terminal, transit map, pixel art; see its README |

## Naming

- Local helper modules: `_parts.py` for a video's general parts, `_<thing>.py`
  for one big thing (`_graph.py`, `_bowl.py`). Leading underscore = not a scene.
- Scene files: `NN_<beat>.py` with one class named for the beat (`03_onepass.py`
  → `OnePass`). The docstring opens with the takeaway and the VO.
- Functions return the mobject; `*_anim` or a method on the part returns an
  animation (`bars.fill_to(probs)`), so the identity rule is kept by construction.
