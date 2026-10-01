# How to read an AI architecture diagram — storyboard (DRAFT, pre-VO)

**One idea:** the figure is not a picture, it is a program. Eight marks make
up a grammar nobody writes down. Once you have them, every architecture
diagram since 2017 reads the same way.

Source: `ZK Home/OpenAugi/Notes/2026-09-28 - How to Read an AI Architecture
Diagram - Is There a Standard.md`. VO lines are the note's own sentences, cut
and reordered. ~130 words. Pair with `007-diagram-to-pytorch` (same diagram,
same final frame, pays the grammar off in code).

## Preflight (content-preflight, passed 2026-10-01)

- READER'S PAIN: "I open the paper, see Figure 1, and skip it. I don't know
  what the arrows and boxes are *saying*." Evidence: every transformer
  explainer opens by apologising for the figure (Hivenet's guide: the
  diagrams "stack many ideas at once"); arXiv 2402.05424 (Neural Circuit
  Diagrams) exists because paper figures are ambiguous; "Tracing the
  Transformer in Diagrams" (TDS) is a whole post re-drawing it.
- AUDIENCE QUESTIONS: What is a box? What does an arrow carry? Which way do
  I read it? What is the line that goes around a box? What does N× mean?
  Is there a standard I'm supposed to already know?
- PITCH (no I/my): experts read an architecture figure as a program; here is
  the eight-mark grammar they use without noticing.
- HERO: the learner who skips Figure 1. GUIDE: the grammar, one mark at a
  time, on one real diagram.
- VALUE WORDS: layer, tensor, residual, skip connection, N×, forward pass,
  "read the paper".
- SHARE MOTIVATION: "this is the decoder ring for every paper figure".
- EMOTION: awe/relief ("there *is* a system and I now have it"). High.
- CURIOSITY GAP opener: "There is no standard like UML. There is a grammar.
  Nobody writes it down."
- STRUCTURE: problem (beat 1) → destabilise (beat 2) → framework (3–6) →
  application (7). No personal story needed; proof is the diagram itself.
- First 25 % (beats 1–2) already delivers: "the figure is a program, and
  the grammar comes from one 2017 paper".

## Beats

Visual: `videos/_shared/transformer.build_block(self.stage)` for every beat.
Teal arrows = tensors. One magenta hero per beat. Burned-in VO captions.

| # | Beat | ~s | Visual (9:16) | VO (author's sentences) |
|---|------|---:|---|---|
| 1 | Hook | 6 | The whole block is on screen at frame 0, FG_DIM, and draws in bottom to top (`Create`, lag). Nothing is magenta yet. | People look at the figure as a picture. Experts read it as a program. |
| 2 | No standard | 8 | A "2017" tag lands beside the diagram on "Attention Is All You Need". Behind it, three ghosted mini-copies of the same column fan out (OP_GHOST) and settle: every later figure inherits it. | There's no formal standard like UML. There *is* a de facto visual grammar. Almost every paper figure inherits it from Figure 1 of Attention Is All You Need. |
| 3 | Box | 7 | All four boxes turn magenta on "box"; the label inside each pulses once. | A box is an operation or a layer. Linear, attention, feed-forward. |
| 4 | Arrow | 9 | Boxes back to dim. The main-line arrows turn magenta on "arrow"; a single teal token dot rides the column bottom to top on "bottom", "top". | An arrow is a tensor moving to the next op. Flow is bottom to top: input tokens at the bottom, logits at the top. |
| 5 | Skip + (+) | 10 | The two bypass paths turn magenta on "bypasses"; the two (+) nodes join them on "add". The token dot splits: one copy goes through Attention, the other around, they merge at (+). | An arrow that bypasses a box is the residual path. The circle with a plus is where it adds back in. That vertical highway is the residual stream; everything reads from it and adds back into it. |
| 6 | N× | 8 | Bracket turns magenta on "N"; two ghost copies of the block stamp upward (OP_GHOST, `TransformFromCopy`) then collapse back into the bracket. | A bracket with N× means this block repeats N times. |
| 7 | Close | 8 | Everything returns to dim. A shape tag `[batch, seq, d]` (teal) rides the main line from Embed to Linear, unchanged at every arrow. Last frame still: diagram + tag. | Reading tip: trace the shape along the arrows. If you can say the shape at every arrow, you've understood the diagram. |

Total ≈ 56 s before tightening. Hero per beat: 1 none, 2 the year tag,
3 boxes, 4 arrows, 5 skips + adds, 6 bracket, 7 the shape tag.

## Not in this short (on purpose)

Side-entering arrows (cross-attention), dashed/coloured variant boxes, the
zoom-in inset, MoE routing. These are marks 7–9 of the note; a follow-up if
this one performs. Beat 7's shape-tracing is the seed of a third short
("follow the shape").

## Next

1. Chris: read the VO column aloud once for length, edit any sentence that
   isn't how you'd say it, then record `vo_raw.m4a` in one pass (pause ~1 s
   between beats).
2. Claude: clean → transcribe → cut list (Chris approves) → one scene per
   beat with the real timings → assemble → contact sheets.
