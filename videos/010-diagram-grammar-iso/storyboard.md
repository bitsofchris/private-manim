ENGINE: hyperframes

# How to read an AI architecture diagram, isometric — storyboard

**What this is:** `videos/006-diagram-grammar` rebuilt beat for beat in the
isometric HyperFrames house style (the look of 009), over the same
voice-over, cut and captions. The idea, preflight and VO are 006's and live
in `../006-diagram-grammar/storyboard.md`; nothing was re-recorded.

**Audio and captions (not copied):** `../006-diagram-grammar/vo_final.wav`
and `../006-diagram-grammar/captions.json`.

## The look, and the accuracy rule

The transformer block figure stands in the isometric world as an extruded
object: each box is a slab with its label on the front face; arrows, (+)
nodes, skip paths and the N× bracket are drawn on the plane of the front
faces. It is the same figure as `videos/_shared/transformer.py`, mark for
mark, read bottom to top: the Short teaches the figure's symbols and
direction, so they are never restyled or reversed. The figure lives in
`_diagram/diagram.js`; the kit is 009's `_iso/iso.js`; `00_layout/` is the
canonical frame; `BRIEF.md` is the contract the beat agents built to.

## Final beats

| # | Beat | Master start | Length | Folder | VO (author's words) |
|---|------|-------------:|-------:|--------|---------------------|
| 1 | Hook | 0.00 | 3.99 | `01_hook` | Here's how you can understand AI architecture diagrams like a pro. |
| 2 | Grammar | 3.99 | 8.27 | `02_grammar` | Now there's no formal standard, but there is a de facto visual grammar. Almost every paper figure inherits it from Figure 1 in Attention Is All You Need. |
| 3 | Box | 12.26 | 5.53 | `03_box` | A box is an operation or a layer. Linear, attention, feed forward, et cetera. |
| 4 | Arrow | 17.79 | 9.02 | `04_arrow` | An arrow is a tensor moving to the next operation. Flow is always bottom to top, where input tokens are at the bottom and logits are at the top. |
| 5 | Residual | 26.81 | 16.84 | `05_residual` | An arrow that bypasses a box is the residual path. The circle with the plus is where it adds its new updated vector back in. That vertical highway is the residual stream, and everything reads from it, adding information back to it as we refine our representation through the layers. |
| 6 | Repeat | 43.65 | 4.70 | `06_repeat` | A bracket with N× means this block repeats N times. (then 1.0 s held) |

Total 48.35 s.

## Render and assemble

```
cd videos/010-diagram-grammar-iso
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_grammar 03_box 04_arrow 05_residual 06_repeat; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../tools/assemble.py beats.json \
    --vo ../006-diagram-grammar/vo_final.wav \
    --captions ../006-diagram-grammar/captions.json \
    -o media/diagram_grammar_hyperframe.mp4
```
