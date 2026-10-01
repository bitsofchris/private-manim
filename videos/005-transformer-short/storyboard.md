# Transformer block in 60 seconds — storyboard 

**One idea:** a transformer never replaces a token's vector. It keeps the same
L×d matrix and *adds* refinements to it, block after block. Attention adds
what other tokens know; the feed-forward net adds what the token can work
out on its own; the residual connection is the "+". The stack's output is a
refined representation, not a prediction. A task head turns it into whatever
the loss asks for.

**Hook (visual + spoken):** a sentence becomes columns of numbers, and the
columns never go away; they just keep getting edited.

Source: `ZK Home/_private/0-Fleeting-Inbox/2026-10-01 - Transformer basics.md`.
VO lines below are the note's own sentences, lightly cut. ~135 words.

## Preflight (content-preflight)

- READER'S PAIN: "I get attention, but what does the *rest* of the block do,
  and what does the stack actually output?" Evidence: this exact question
  came up while writing the note ("is the output the representation at the
  next step or whatever the loss targets?"); it is the standard confusion
  under every attention explainer. **Confirm with 2–3 real comments before
  recording** (3b1b transformer video comments, r/learnmachinelearning).
- AUDIENCE QUESTIONS: What goes in / what comes out? What is attention
  *for* vs the feed-forward net? Why "residual"? Do all the blocks do the
  same thing? Where does the next-word prediction come from?
- PITCH (no I/my): A transformer never throws a token away; it refines the
  same matrix over and over, and the prediction is a separate last step.
- HERO: the learner who has watched attention videos and still can't draw
  the block. GUIDE: one diagram you can redraw from memory.
- VALUE WORDS: residual stream, representation, L×d, tokens, head, logits.
- EMOTION: awe/relief ("oh, it's *just* X + update, repeated"). High arousal.
- CURIOSITY GAP opener: "Attention is the famous part. It is one line of
  four, and the other three are where the picture gets simple."

## Beats (final, from `transcript_final.txt`)

VO recorded in Descript (Studio Sound on), one take with alternates, 164 s.
Loudness-normalized only (`vo_clean.wav`), cut to 59.27 s with
`tools/tighten_vo.py` (+3.5 % tempo, cut list below), re-transcribed to verify.
Beat boundaries sit at the end of a 0.4 s pause so each beat cuts on its first word.

| # | Beat | Master start | Length | Scene | VO (author's words) |
|---|------|-------------:|-------:|-------|---------------------|
| 1 | Hook | 0.00 | 6.20 | `01_hook.py` `Hook` | A transformer takes a sequence of tokens and produces updated representations of those tokens. (v2: the shared block diagram fills the frame, "my name is" is absorbed by Embed, a pulse climbs the N× block, a tiny matrix pops out above it) |
| 2 | Matrix | 6.20 | 9.08 | `02_matrix.py` `Matrix` | (v2 opens by zooming the tiny matrix into the canonical one) Each token is a vector of D numbers, and a sequence of L tokens is then an L by D matrix. Every block in the transformer stack keeps that shape. |
| 3 | Attention | 15.28 | 13.82 | `03_attention.py` `Attention` | Attention is what combines information across the tokens. Each token asks a query, which is what am I looking for. Every token then offers a key, saying what do I have? So each token collects a weighted sum of these values that match the key and query. |
| 4 | Residual | 29.10 | 5.40 | `04_residual.py` `Residual` | Now a residual connection just adds the update to the existing representation instead of replacing it. |
| 5 | Feed-forward | 34.50 | 11.45 | `05_ffn.py` `FeedForward` | A feed forward network then works on each token alone. It learns which combinations of features matter, amplifying the ones that do, and then adds a non-linearity on top that lets the choice depend on the input. |
| 6 | Stack | 45.95 | 4.49 | `06_stack.py` `Stack` | Now each block receives the previous block's output and continues to refine it further. |
| 7 | Head | 50.44 | 8.83 | `07_head.py` `Head` | Now the final representations are not necessarily predictions, but a task specific output layer will turn these representations into whatever the training objective is asking for. |

Total 59.27 s. Per-phrase word times and the opening/closing state of every
beat are in `BRIEF.md` (the contract the scene agents built to).

## Cuts made to the raw take (whole phrases; nothing re-recorded)

- "And when those match up, we then weight the value of that attention higher." (misstates the mechanism; attention was 3 s over)
- "Key, query and value are learnable matrices in part of each attention block." (afterthought take)
- "You can think of residuals as constantly refining the existing representation." (beat 6 says it with the stack on screen)
- Feed-forward takes 2 and 3 (take 1 is shortest; take 2 opens on a flub)
- Head take 1 (take 2 is shorter and cleaner)
- Pauses capped at 0.25 s inside beats, 0.4 s at beat boundaries; tempo +3.5 %; 0.3 s trimmed from the tail.

## Visual design

v2 opens on the bird's-eye view: the shared block diagram from
`videos/_shared/transformer.py` (the one 006 teaches), then zooms into the
tokens. From there the matrix never leaves its spot. Words above three teal
columns (`my name is`), one shared bracket. The head predicts `Chris`.
v1 (`the cat sat`, sentence-first opener) is kept as `01_hook_v1.py` /
`02_matrix_v1.py` and `media/transformer_short_v1_catsat.mp4`. The lower third of the stage is where updates
arrive: the magenta attention update column (beat 3) slides up onto its token
(beat 4); the per-token feed-forward nets sit there (beat 5); the block slabs
and the output head's bars use it (beats 6, 7). Shared mobjects:
`TokenColumn`, `TokenMatrix`, `attention_arcs` in `videos/_shared/mobjects.py`;
sentence, seeded value stages and canonical placement in `_tokens.py`.

## Assemble

```
cd videos/005-transformer-short
for f in 0*_*.py; do uv run --no-sync manim -qh $f; done
uv run --no-sync python ../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json -o media/transformer_short.mp4
```
