# Architecture diagram → PyTorch — storyboard (DRAFT, pre-VO)

**One idea:** every mark on the figure is a line of PyTorch. Boxes are
modules built in `__init__`; arrows are the order of calls in `forward`;
the bypass is the `x` that keeps getting reassigned; N× is a `for` loop.

Source: the "In code" column of `ZK Home/OpenAugi/Notes/2026-09-28 - How to
Read an AI Architecture Diagram - Is There a Standard.md`, plus Raschka's
"working code doesn't lie". VO ~125 words. Sequel to `006-diagram-grammar`:
opens on 006's last frame so the pair plays as one.

## Preflight (content-preflight, passed 2026-10-01)

- READER'S PAIN: "I can follow the diagram now but I still can't write it."
  Evidence: the channel's own data (PyTorch Neural Networks Made Simple,
  84K) says this audience wants the code; "how do I implement the
  transformer from the paper" is the standing r/learnmachinelearning
  question; Raschka's whole workflow post exists because paper → code is
  the hard step.
- AUDIENCE QUESTIONS: Which part of the diagram is which part of the code?
  Where do the arrows go in code? What is the residual in code? How do I
  write N×? Why do people say to read the code instead of the paper?
- PITCH (no I/my): the diagram and the `nn.Module` are the same object in
  two notations, and the mapping is five rules.
- HERO: the learner who wants to implement what they read. GUIDE: the
  five mark → line rules, each shown on the real diagram and the real code.
- VALUE WORDS: `nn.Module`, `forward`, `__init__`, residual, `for` loop,
  reference implementation, "from scratch".
- SHARE MOTIVATION: "this is the Rosetta stone, send it to whoever is
  reading the paper".
- EMOTION: excitement/empowerment ("I can write this tonight"). High.
- CURIOSITY GAP opener: "Every mark on this diagram is a line of PyTorch."
- STRUCTURE: problem/destabilise (beat 1) → framework (2–6) → proof +
  application (7: the whole model is ~20 lines, and the workflow).

## Layout decision

Labels at phone size leave no room beside the diagram for a code panel, so
the code card lives in the **caption band** (`self.band`) for beats 2–6:
1–3 lines of `transformer.GPT_SOURCE` at `S.SHORT_CODE_FONT_SIZE`, the
magenta bar on the line that matches the magenta mark above. Those beats
have no word captions (one caption source per beat); beats 1 and 7 use the
burned-in VO captions as usual (`captions.json` holds only those spans).
Beat 7 ghosts the diagram and fills the stage with the full `GPT_SOURCE`.
`transformer.MARK_LINES` is the mark → line contract; a test guards it.

## Beats

| # | Beat | ~s | Visual (9:16) | VO (author's sentences) |
|---|------|---:|---|---|
| 1 | Hook | 5 | 006's final frame: full diagram, dim. On "line of PyTorch" a code card slides up into the band showing `x = x + self.attn(x)`, no bar yet. | Every mark on this diagram is a line of PyTorch. |
| 2 | Box → `__init__` | 9 | Boxes magenta on "box". Card shows lines 3–4 (`self.attn = Attention(d)`, `self.ffn = FeedForward(d)`), bar on both. | A box is one nn.Module, built in init. Linear, attention, feed-forward: each one is an object you construct once. |
| 3 | Arrow → `forward` | 9 | Main-line arrows magenta. Card shows lines 7–9; the bar steps down one line per arrow as the token dot climbs the column. | An arrow is a tensor moving to the next op. In code it's the order of calls in forward. Top to bottom of forward is bottom to top of the diagram. |
| 4 | Skip + (+) → `x = x + …` | 10 | Skips and adds magenta. Card shows line 7 alone, big; the bar sits on `x + self.attn(x)` and the `x` on the left of `=` pulses on "reassigned". | The arrow that bypasses a box is the x that keeps getting reassigned. Add and norm is x equals x plus sublayer of x. |
| 5 | N× → `for` | 8 | Bracket magenta. Card shows lines 19–20; bar on the loop; two ghost blocks stamp upward in time with the bar pulsing twice. | A bracket with N× is a for loop. For block in blocks, x equals block of x. |
| 6 | Inset → class | 7 | The repeated block (attn, (+), ffn, (+), skips) magenta as one group; the card shows `class Block(nn.Module):` with the bar on it. | A zoomed-in box is a submodule's own forward. The block is its own class. |
| 7 | Close | 9 | Diagram fades to OP_GHOST; the full `GPT_SOURCE` fills the stage (`code_block`, no bar). Three small tags stack in the band on the three words: paper · config · code. Last frame still. | Raschka's workflow goes paper, then the model's config file, then the reference implementation, because working code doesn't lie. If you can read the diagram, you can read the code. |

Total ≈ 57 s before tightening. Hero per beat: 1 none, 2 boxes, 3 arrows,
4 skips + adds, 5 bracket, 6 the block, 7 none (code is the frame).

## Next

1. Chris: edit the VO column into your own phrasing where it isn't, then
   record `vo_raw.m4a` (one pass, ~1 s pause between beats). Recording 006
   and 007 in the same sitting keeps the voice matched.
2. Claude: clean → transcribe → cut list → scenes with real timings →
   assemble with partial `captions.json` → contact sheets.

## Final beats (VO recorded 2026-10-01, Descript Studio Sound; loudnorm only)

`vo_raw.m4a` 69.2 s → `vo_final.wav` 42.67 s with no phrase cuts: pauses
capped (0.25 s / 0.4 s at boundaries), a stray blip at 44.9–45.3 and the
tail after "code" removed. Known flaw: the "X" after "a sublayer of"
(~27.1–27.7 final) was spoken very softly and does not transcribe even
boosted; the code card shows it, so the eye gets what the ear misses.
Chris: listen there; if it bothers you, re-record that one sentence.

| # | Beat | Start | Length | Scene | VO |
|---|------|------:|-------:|-------|----|
| 1 | Hook | 0.00 | 3.13 | `01_hook.py` `Hook` | Every mark on this diagram is a line of PyTorch. |
| 2 | Box | 3.13 | 5.83 | `02_box.py` `Box` | A box is one nn.Module. Linear, attention, feed forward: each one of these is an object you construct once. |
| 3 | Arrow | 8.96 | 10.00 | `03_arrow.py` `Arrow` | An arrow represents a tensor moving to the next operation. In code, it's the order of calls in the forward function. Top to bottom of forward is bottom to top of this diagram. |
| 4 | Skip | 18.96 | 9.95 | `04_skip.py` `Skip` | The arrow that bypasses a box is the x that keeps getting reassigned. Add and norm is x equals x plus a sublayer of x. |
| 5 | Repeat | 28.91 | 5.91 | `05_repeat.py` `Repeat` | A bracket with N× is a for loop. For block in blocks, x equals block of x. |
| 6 | Inset | 34.82 | 5.07 | `06_inset.py` `Inset` | A zoomed-in box is a submodule's own forward function. The block is its own class. |
| 7 | Close | 39.89 | 2.78 | `07_close.py` `Close` | If you can read the diagram, you're understanding the code. |

Captions: `captions.json` holds beats 1 and 7 only; beats 2–6 draw a code
card in the band via `_code.py`.
