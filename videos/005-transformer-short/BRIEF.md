# Beat brief: 005-transformer-short

Read first: `/Users/chris/repos/private-manim/CLAUDE.md`, `videos/_shared/STYLE.md`
("Shorts (9:16)" section and the 0.18.1 gotchas), `videos/_shared/ANIMATION_RULES.md`.
Model scenes: `videos/004-backprop-short/02_neuron.py` and `06_gradient.py`.

## Hard rules
- One file per beat, one `BocShortScene` subclass, file/class names exactly as in
  `beats.json` (the assembler looks for `media/videos/<file>/1920p30/<Class>.mp4`).
- `BEAT_SECONDS` = the beat length below; end with `self.hold_until(BEAT_SECONDS)`.
  `hold_until(t)` before each change so it lands on the word that names it.
- No scene captions: word captions are burned in later over `self.band`. Keep the
  band empty. Everything visual lives in `self.stage`; text and the magenta hero
  never leave `self.safe`.
- No LaTeX (`Text` only). Nothing smaller than `S.SHORT_LABEL_SCALE`. Use
  `label()` from `_tokens.py` for text.
- One magenta (`S.STRUCTURE`) hero per beat. Teal is the data (the matrix).
- Meaningful moves take `S.HOLD` (1.2 s) or `S.BEAT`; never `S.QUICK`.
- Each beat opens on the previous beat's final frame (states below) and ends on
  the state the next beat expects. Build the opening state and `self.add` it
  before the first `play`; something must be moving by frame 1.
- Do NOT edit `videos/_shared/*` or `_tokens.py`. If you need a change there,
  work around it locally in your file and say so in your report.
- Render: `cd videos/005-transformer-short && uv run --no-sync manim -qh <file>.py <Class>`
  then `../../tools/review_frames.sh media/videos/<file>/1920p30/<Class>.mp4 4` and
  LOOK at the contact sheet (Read the png). Fix overlaps, dead-zone intrusions,
  anything unreadable. Delete any `show_guides()` call before the final render.
- Report: what the scene does per VO phrase, the render path, any deviations.

## Shared API (`_tokens.py`, `videos/_shared/mobjects.py`)
```python
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens
from _tokens import (TOKENS, TARGET, ATTN_WEIGHTS, NEXT_TOKENS, VALUES,
                     VALUES_AFTER_ATTN, build_matrix, word_labels, tokens, label)
from videos._shared.mobjects import TokenMatrix, TokenColumn, attention_arcs, bracket, hero_arrow
```
- `TOKENS = ["my","name","is"]`, `TARGET = 2` (the "is" column attends). `NEXT_TOKENS = [("Chris",.58),("Sam",.27),("not",.09)]`.
- `VALUES[k]`: (3 x 3) arrays; 0 embeddings, 1 after attention, 2 after FFN, 3 after stack.
- `m = build_matrix(self.stage, values=VALUES[k], digits=True, bracketed=True)`:
  the L x d matrix in its canonical place (top of the stage, centred).
  `m.columns[i]` is a `TokenColumn` (`.cells`, `.nums`, `.dots`); `m.brackets`.
  `self.play(m.animate.set_values(VALUES[k+1]), run_time=S.HOLD)` ticks the
  numbers in place (same mobjects: never fade-swap the matrix).
  `col.animate.set_values(row)` does one column.
- `words = word_labels(m)` — the three words above their columns.
  `toks = tokens(m, words)` — [VGroup(word, column)] per token.
- `attention_arcs(toks, toks[TARGET], ATTN_WEIGHTS)` — magenta arcs from above
  each word into the target; width = weight; the target gets a self loop.
- `TokenMatrix(VALUES[1][TARGET:TARGET+1], bracketed=False, dots=False, color=S.STRUCTURE)`
  — a magenta "update" column (1 token). Place with `.align_to(self.stage, DOWN).set_x(col.get_x())`.
- `label("text", color=S.FG)` — Text at the Short label scale.
- Lower region of the stage (below the matrix, ~2.8 units tall) is free for
  updates, FFN fans, bars. Stage is 7.38 wide x 7.25 tall.

## Beats (lengths are exact; VO times are scene-local seconds, from the final transcript)

### 1 `01_hook.py` `Hook` — 6.20 s  (v2: bird's-eye opener)
VO: "A transformer takes a sequence of tokens" 0.3-2.8 ("tokens" ~2.3);
"and produces updated representations of those tokens" 2.8-6.2
("updated representations" ~3.9-5.2).
Uses the shared block diagram `videos/_shared/transformer.py`
(`build_block(stage)` -> `BlockDiagram` with `.boxes` Embed/Attention/FFN/Linear,
`.adds` (two ⊕), `.flow` arrows, `.skips`, `.bracket` N×, `.block`; read the
module docstring and `videos/006-diagram-grammar/01_hook.py` for how 006 draws it).
Frame 0: the whole diagram on screen, all marks FG_DIM / teal arrows as
`build_block` gives them, filling the stage. The sentence "my name is" (three
`label()` words, `TOKENS`, in a row) sits just below / at the Embed box. The
diagram may need `scale_to_fit_height` so the words fit under it inside the stage.
"takes a sequence of tokens" (0.3-2.8): the words move into Embed and a teal
pulse (`ShowPassingFlash` on HIGHLIGHT copies of the flow arrows, or a small
teal dot travelling the path) climbs the column through Attention, ⊕, FFN, ⊕
(the N× block), one HOLD-scale play, finishing around "tokens".
"produces updated representations" (3.9-5.2): the pulse stops at the top of
the N× block (below Linear; Linear stays dim) and a *tiny* `TokenMatrix(VALUES[0],
digits=False, bracketed=False)` scaled to fit there (about the width of a box)
pops in (FadeIn/GrowFromCenter, HOLD) with the three words `Transform`ed into
tiny word labels above the tiny columns (same word mobjects, keep identity).
"of those tokens" (5.2-6.2): still.
Hero: the climbing pulse is HIGHLIGHT (transient); nothing is magenta.
Ends: dim diagram + tiny matrix (with tiny words) sitting above the N× block.
Expose the end-state builder as a function in `01_hook.py` (e.g.
`opening_state(stage) -> (diagram, tiny_matrix, tiny_words)`) so beat 2 imports
it and opens on exactly the same frame.

### 2 `02_matrix.py` `Matrix` — 9.08 s  (v2: zoom in, then as before)
VO: "Each token is a vector of D numbers" 0.1-2.7 ("D numbers" ~1.9);
"and a sequence of L tokens is then an L by D matrix" 2.8-6.4 ("L by D matrix" ~5.0-6.4);
"Every block in the transformer stack keeps that shape" 6.5-9.1 ("keeps that shape" ~8.0).
Opens: beat 1's end (import `opening_state` from `01_hook.py`). "Each token"
(0.1-1.3): the zoom. The diagram fades out while the tiny matrix + tiny words
`Transform` into the canonical `build_matrix(self.stage, VALUES[0], digits=True,
bracketed=False)` columns + `word_labels` (one HOLD; the columns/words keep
identity: transform the tiny ones into the full ones, then swap to the real
`build_matrix` objects only if you must, invisibly). "vector of D numbers"
(~1.9): indicate one column, a small magenta "d" tag beside it (brace along the
column height; the current file places the "d" below the brace to stay in
safe). "L tokens": an "L" tag along the top across the three words. "L by D
matrix": the shared bracket pair draws in (`m.brackets`, Create). "keeps that
shape": the bracket outline pulses (`Indicate` on brackets, HIGHLIGHT) and the
d / L tags fade. Hero: the d/L tags then the bracket.
Ends: words + bracketed matrix (`VALUES[0]`, digits), no tags: byte-identical
layout to the state beat 3 opens on (`build_matrix` + `word_labels`).

### 3 `03_attention.py` `Attention` — 13.82 s
VO: "Attention is what combines information across the tokens" 0.05-3.4;
"Each token asks a query, which is what am I looking for" 3.4-6.4 ("query" ~4.5);
"Every token then offers a key, saying what do I have?" 6.4-9.5 ("key" ~7.5);
"So each token collects a weighted sum of these values" 9.5-11.9 ("weighted sum" ~10.8);
"that match the key and query" 11.9-13.8.
Opens: beat 2's end. "combines information across the tokens": arcs
(`attention_arcs`) Create with lag into the "sat" token. "query": a small
magenta tag "query?" rises from the sat token (or the sat word pulses magenta).
"key": tags "key" pulse on the other two tokens (FG_DIM/teal, not magenta: one
hero). "weighted sum": a passing flash runs along the arcs (`ShowPassingFlash`
on a HIGHLIGHT copy, `time_width` ~0.4) and a magenta update column
(`TokenMatrix(VALUES[1][TARGET:TARGET+1], bracketed=False, dots=False,
color=S.STRUCTURE)`) grows at the stage bottom under the sat column, cells
filling in with lag. "match the key and query": arcs settle to their final
widths; tags fade. Hero: the arcs + update column (one group).
Ends: words + bracketed matrix (VALUES[0]) + the magenta update column below
the sat column at `align_to(self.stage, DOWN)`. Arcs faded out, no tags.

### 4 `04_residual.py` `Residual` — 5.40 s
VO: "Now a residual connection just adds the update" 0.04-2.44 ("adds" ~1.9);
"to the existing representation instead of replacing it" 2.44-5.4
("existing" ~3.2, "instead of replacing" ~4.3).
Opens: beat 3's end. "adds": a magenta "+" appears between the update column
and the sat column; the update column slides up onto the sat column (HOLD).
"existing representation": the sat column's numbers tick
(`m.columns[TARGET].animate.set_values(VALUES[1][TARGET])`) as the update
merges and fades into it; the teal column is the same mobject throughout.
"instead of replacing it": a brief ghost (OP_GHOST copy of the old column
sliding off and fading, or a struck-through "replace") — keep it to one
play. Hero: the "+" / update. Ends: words + bracketed matrix with
`VALUES_AFTER_ATTN`, nothing else.

### 5 `05_ffn.py` `FeedForward` — 11.45 s
VO: "A feed forward network then works on each token alone" 0.03-3.16 ("alone" ~2.9);
"It learns which combinations of features matter" 3.17-5.2;
"amplifying the ones that do" 5.2-6.72;
"and then adds a non-linearity on top" 6.75-8.75 ("non-linearity" ~7.8);
"that lets the choice depend on the input" 8.78-11.41.
Opens: beat 4's end (`VALUES_AFTER_ATTN`). "feed forward network": one tiny
net draws under the first column in the lower region: 3 input dots (the cells)
-> a wider hidden row of ~5 dots -> 3 output dots, edges FG_DIM (reuse the
look of 004's `01_hook.py` build_net at small scale). "each token alone":
identical copies drop under the other two columns (`TransformFromCopy`, lag);
no lines between columns. "combinations of features": a few edges into one
hidden dot turn magenta. "amplifying": that hidden dot grows/brightens.
"non-linearity": a small ReLU kink glyph (two line segments) appears beside the
hidden row, magenta. "depend on the input": the outputs feed up and every
column ticks to `VALUES[2]` (`m.animate.set_values(VALUES[2])`), nets fade.
Hero: the magenta combination + kink. Ends: words + bracketed matrix (VALUES[2]).

### 6 `06_stack.py` `Stack` — 4.49 s
VO: "Now each block receives the previous block's output" 0.0-2.5 ("block" ~0.6, "output" ~2.3);
"and continues to refine it further" 2.5-4.49 ("refine" ~3.3).
Opens: beat 5's end (VALUES[2]). "block": a translucent panel (BG_PANEL fill,
FG_DIM stroke) labelled "block 1" closes around the matrix. "previous block's
output ... refine it further": two more panels "block 2", "block 3" stack
below in the lower region (they can be short slabs), the matrix's numbers tick
VALUES[2] -> VALUES[3] with a magenta flash passing down through the slabs
(the hero: the passing flash / the arrow of flow). Keep the matrix in its
canonical spot. Ends: words + bracketed matrix (VALUES[3]); panels faded out,
nothing else on screen.

### 7 `07_head.py` `Head` — 8.83 s
VO: "Now the final representations are not necessarily predictions" 0.03-2.93 ("not" ~2.0);
"but a task specific output layer" 2.93-5.0 ("output layer" ~4.3);
"will turn these representations" 5.0-6.4;
"into whatever the training objective is asking for" 6.4-8.69.
Opens: beat 6's end (VALUES[3]). "final representations": the whole matrix
pulses (Indicate, HIGHLIGHT). "not necessarily predictions": nothing is
predicted yet, hold. "output layer": a magenta rounded panel labelled "head"
appears in the lower region under the last column, with a thin arrow from the
sat column into it. "turn these representations": horizontal bars grow out of
the head: `NEXT_TOKENS = [("on",.58),("down",.27),("still",.09)]`, bar =
teal Rectangle width proportional to p, word label left of each bar (FG).
"whatever the training objective is asking for": the head label flips through
"next token" -> "class" -> "number" (Transform the Text, HOLD each) and the
bars can shrink to a single value for "number". Last frame still and clean.
Hero: the head panel. Ends: free (last beat).
