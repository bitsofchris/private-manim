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

## Local, candidates for promotion (second use promotes)

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

## Naming

- Local helper modules: `_parts.py` for a video's general parts, `_<thing>.py`
  for one big thing (`_graph.py`, `_bowl.py`). Leading underscore = not a scene.
- Scene files: `NN_<beat>.py` with one class named for the beat (`03_onepass.py`
  → `OnePass`). The docstring opens with the takeaway and the VO.
- Functions return the mobject; `*_anim` or a method on the part returns an
  animation (`bars.fill_to(probs)`), so the identity rule is kept by construction.
