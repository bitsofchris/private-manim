ENGINE: hyperframes

# Transformer block in 60 seconds, isometric — storyboard

**What this is:** `videos/005-transformer-short` rebuilt beat for beat in the
isometric HyperFrames style (house palette), over the same voice-over, cut
and captions. Made 2026-10-04 to see whether HyperFrames can carry a whole
technical Short in a more distinctive look. The idea, hook, preflight and VO
are 005's and live in `../005-transformer-short/storyboard.md`; nothing was
re-recorded.

**Audio and captions (not copied):** `../005-transformer-short/vo_final.wav`
and `../005-transformer-short/captions.json`.

## The look

An isometric world on the house navy with a faint floor grid. The matrix is a
tray of 3 x 3 extruded tiles, coloured by token column (my teal, name blue,
is gold; tall = large, a darker shade = negative); a flat readout card above
it carries `my name is` and the nine numbers in the same three colours. Blocks are slabs and rings the tray passes through. Data flows down.
One magenta hero per beat. The shared kit is `_iso/iso.js`; the canonical
frame is `00_layout/`; the contract the beat agents built to is `BRIEF.md`.

## Final beats

| # | Beat | Master start | Length | Folder | VO (author's words) |
|---|------|-------------:|-------:|--------|---------------------|
| 1 | Hook | 0.00 | 6.20 | `01_hook` | A transformer takes a sequence of tokens and produces updated representations of those tokens. |
| 2 | Matrix | 6.20 | 9.08 | `02_matrix` | Each token is a vector of D numbers, and a sequence of L tokens is then an L by D matrix. Every block in the transformer stack keeps that shape. |
| 3 | Attention | 15.28 | 13.82 | `03_attention` | Attention is what combines information across the tokens. Each token asks a query, which is what am I looking for. Every token then offers a key, saying what do I have? So each token collects a weighted sum of these values that match the key and query. |
| 4 | Residual | 29.10 | 5.40 | `04_residual` | Now a residual connection just adds the update to the existing representation instead of replacing it. |
| 5 | Feed-forward | 34.50 | 11.45 | `05_ffn` | A feed forward network then works on each token alone. It learns which combinations of features matter, amplifying the ones that do, and then adds a non-linearity on top that lets the choice depend on the input. |
| 6 | Stack | 45.95 | 4.49 | `06_stack` | Now each block receives the previous block's output and continues to refine it further. |
| 7 | Head | 50.44 | 8.83 | `07_head` | Now the final representations are not necessarily predictions, but a task specific output layer will turn these representations into whatever the training objective is asking for. |

Total 59.27 s.

## Render and assemble

```
cd videos/009-transformer-short-iso
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
for b in 01_hook 02_matrix 03_attention 04_residual 05_ffn 06_stack 07_head; do
  (cd $b && npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/$b.mp4)
done
uv run --no-sync python ../../tools/assemble.py beats.json \
    --vo ../005-transformer-short/vo_final.wav \
    --captions ../005-transformer-short/captions.json \
    -o media/transformer_short_hyperframe.mp4
```
