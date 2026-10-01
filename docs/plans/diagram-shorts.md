# Plan: "How to read an AI architecture diagram" Shorts (006 + 007)

**Name:** diagram-shorts
**Description:** Two 9:16 Shorts from the note *How to Read an AI
Architecture Diagram: Is There a Standard?* (2026-09-28). 006 teaches the
implicit grammar of transformer figures, one mark per beat. 007 maps each
mark to a line of PyTorch. Both draw the same diagram from
`videos/_shared/transformer.py`, and 007 opens on 006's last frame.
**When to use:** the status page for this pair; move to `docs/archive/`
when both are published.
**How it works:** the shorts runbook (`docs/shorts-runbook.md`), audio
first. The shared diagram was built and reviewed before any VO exists so
the storyboards describe a visual that is known to fit the phone frame.

## Directions considered (2026-10-01)

| | Short | Status |
|---|---|---|
| A | The grammar: box, arrow, flow direction, skip + (+), N× | `videos/006-diagram-grammar/storyboard.md`, waiting on VO |
| B | Diagram → PyTorch: each mark to its line of the `nn.Module` | `videos/007-diagram-to-pytorch/storyboard.md`, waiting on VO |
| C | Follow the shape: `[batch, seq, d]` along every arrow | seeded as 006 beat 7; its own short if A/B perform |
| D | Long-form walk of the 2017 figure with code beside it | after the shorts |

Not pursued yet: cross-attention side arrows, dashed variant boxes, MoE
routing (note marks 7–9).

## Done

- `videos/_shared/transformer.py`: `build_block(stage)` → `BlockDiagram`
  with named parts (`boxes`, `adds`, `flow`, `skips`, `bracket`, `block`,
  `rows`); `stack_rows` pure layout; `GPT_SOURCE` + `MARK_LINES` as the
  diagram/code contract. Tests in `tests/test_transformer.py`.
- Layout finding: labels at `SHORT_LABEL_SCALE` are wide ("Feed Forward"
  is 5.1 of 7.4 units), so boxes say Embed / Attention / FFN / Linear and
  the add node is a bare (+). No room for a side-by-side code panel in
  007: the code card uses the caption band (see 007 storyboard).
- `videos/006-diagram-grammar/_preview.py` renders the diagram with guides
  for layout checks.

## Next

1. Chris records `vo_raw.m4a` for 006 and 007 (same sitting).
2. Runbook steps 3–8 per short.
3. Promote `_preview.py` into the first beat once timings exist; delete it.
