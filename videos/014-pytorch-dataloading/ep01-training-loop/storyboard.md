ENGINE: hyperframes

# PyTorch training loop (series 014, ep 1 of 5): storyboard (recorded VO)

THE QUESTION: "What actually happens in one PyTorch training step?"
WHO IS ASKING: someone writing their first real training script who has
typed the loop from a tutorial and can't say what each line does to the
batch.
THE ANSWER IN ONE SENTENCE: a batch is a bunch of samples packed into one
tensor, and the training loop is what happens to that one batch: the
loader yields it, forward, loss, backward, update, then the next batch.
THE SEARCH PHRASE: pytorch training loop explained (autocompletes, checked
2026-10-25).

**One idea:** the model only ever sees one batch; the loop is the four
things that happen to it, every time.

Series context: `../SERIES.md` (ledger, images, decisions). The VO is
`script.md` (what Chris said), not `../SCRIPTS.md`.

## Ledger (copied from SERIES.md; every beat uses exactly these)

- The data: synthetic time series, **512 points** each; a `SeriesDataset`
  of **512 series**. One sample is a `[512]` tensor (a squiggle).
- The loader: `DataLoader(dataset, batch_size=32, shuffle=True,
  drop_last=True)`. **One batch is `[32, 512]`.**
- The training loop (the code card, `_kit/loop.js` `LOOP.CODE`, from the
  ledger's "The training loop"; `out`/`y` abbreviations as the shared
  `_kit/data.js` `loop` uses them, so a line fits 28 characters):

  ```python
  for epoch in range(epochs):
    for batch in loader:
      out = model(batch)
      loss = loss_fn(out, y)
      loss.backward()
      optimizer.step()
  ```

- The model: "model" on its chip; never named in a title. No loss number
  is drawn.
- The four stations of the machine (beats 7–8): sampler, fetch, batching,
  collate; the dataset card shows `__len__`, `__getitem__`.

## The look

Three images, never two at once:

1. **The loop** (beats 1–5, `_kit/loop.js`, take `ring`; `00_layout/`):
   Chris's diagram 1 redrawn in the kit's card style. The DataLoader card
   at the top (the same geometry as the machine's Dataset card, x 190–825,
   y 250–400) with a slot at its left where a batch glyph sits; four boxes
   stacked under its right half: forward, loss, backward, update (x
   480–840, 90 tall). A muted track leaves the slot, runs down the right
   gutter past the boxes, under update, and back up the left gutter,
   dashed, into the slot. **The batch glyph rides the track** (a small
   teal tensor card: box + two rows) and is the hero while the VO is about
   it; a box turns magenta as the VO names it; "one training step" lights
   the four boxes together.
2. **The code card** (beat 6, shared `_kit/code.js`): the loop flips to
   the full-stage card (`S.flip` 0 → 1 over 0.4 s), which types the six
   lines with `SC_typedAt`; the line being typed is the hero; "inner loop"
   lights `for batch in loader:`, "outer loop" lights `for epoch …`.
3. **The machine** (beats 7–8, shared `_kit/machine.js`, `SC.REST`): the
   series image at rest, samples hopping from the Dataset card into the
   DataLoader box, the `[32, 512]` batch going to the model chip. The
   batch is the hero. Ep 1's last frame is this, so it is ep 2's frame 0.

Captions in the band (y 1100–1536) as usual; the stage is y 230–1100 and
the code card is centred on it. Palette and sizes from the kit: 60 px
Inter 800 labels, 48 px monospace code.

Seam states are code: `_kit/seam.js` (`SC.SEAM[0..8]`); the table below
is its prose.

## Beats (VO from script.md; times are vo_final seconds)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook | A batch is just a bunch of samples packed into one tensor so the GPU can parallelize. And a PyTorch training loop is what happens to that one batch. | Frame 0: the loop with the batch glyph already riding (out of the slot, down the right gutter). "packed into one tensor" (2.3 s): the glyph pulses. "training loop" (6.0 s): the whole track pulses magenta once, then back to muted. The glyph completes the lap and parks in the slot by 7.5 s; still to the end. | the batch |
| 2 | Forward | The data loader yields it, the batch goes into the forward pass, and the model makes a prediction. | "yields it" (8.9 s): the glyph leaves the slot and rides to beside forward, arriving on "forward pass" (10.7 s); forward lights on "forward". "prediction" (12.3 s): forward pulses once. Ends: glyph beside forward, forward lit. | the batch, then forward |
| 3 | Loss | We compare that prediction to the target, and that's the loss. | "compare" (14.7 s): the glyph rides down to beside loss; "loss" (16.7 s): loss lights, forward goes back to muted. | loss |
| 4 | Backward + step | The loss is then propagated backwards, and the weights are updated as part of gradient descent. That is one training step. | "backwards" (18.6 s): the glyph rides to beside backward, backward lights. "updated" (19.9 s): on to beside update, update lights. "one training step" (22.4 s): all four boxes light together and hold. | backward → update → the four boxes |
| 5 | Next batch | Then we go back to the data loader for the next batch. | "go back" (24.0 s): the glyph rides the dashed return up the left gutter into the slot, arriving on "next batch" (25.2 s) as the hero. Boxes back to muted. | the batch |
| 6 | Epoch, the code | An epoch is one pass through the whole dataset. So this inner loop runs once per epoch, and the outer loop runs for as many epochs as you set. | "An epoch" (26.3 s): flip to the code card (0.4 s); typing starts at 26.8 s, all six lines land by ~33 s (`SC_typingSeconds`). "inner loop" (29.5 s): `for batch in loader:` is the hero; "outer loop" (31.8 s): `for epoch in range(epochs):` is the hero. Cursor off and still from 33.5 s. | the line being typed, then inner, then outer |
| 7 | One batch | The model never sees your dataset, it only ever sees one batch at a time. | "The model" (34.6 s): flip back (0.4 s) onto the machine at rest, samples hopping into the DataLoader box; the model chip is the hero. "one batch" (37.7 s): the hero passes to the `[32, 512]` batch card. | model → the batch |
| 8 | Takeaway | So if your loss isn't moving, check the batch first. Everything downstream of it is the same four lines every time. | "check the batch" (39.9 s): the batch card pulses once. "four lines" (43.1 s): the four stations of the box dim slightly then return (the lines are not on screen: the card never shares the stage with the machine). Still from 44.0 s. | the batch |

## Final beats (the contract; `vo_final.wav` 44.737 s, master seconds)

Beat brief: `agents/beat-brief-hyperframes.md` plus this table; seam
states `SC.SEAM` in `_kit/seam.js`; links per beat: `vendor`, `kit`, `ep`.

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.000 | 8.050 | A batch is just a bunch of samples packed into one tensor so the GPU can parallelize. And a PyTorch training loop is what happens to that one batch. |
| 2 | `02_forward` | 8.050 | 5.505 | The data loader yields it, the batch goes into the forward pass, and the model makes a prediction. |
| 3 | `03_loss` | 13.555 | 3.705 | We compare that prediction to the target, and that's the loss. |
| 4 | `04_backward` | 17.260 | 6.340 | The loss is then propagated backwards, and the weights are updated as part of gradient descent. That is one training step. |
| 5 | `05_next_batch` | 23.600 | 2.400 | Then we go back to the data loader for the next batch. |
| 6 | `06_epoch_code` | 26.000 | 8.410 | An epoch is one pass through the whole dataset. So this inner loop runs once per epoch, and the outer loop runs for as many epochs as you set. |
| 7 | `07_one_batch` | 34.410 | 4.200 | The model never sees your dataset, it only ever sees one batch at a time. |
| 8 | `08_check_batch` | 38.610 | 6.127 | So if your loss isn't moving, check the batch first. Everything downstream of it is the same four lines every time. |

## Seam states (`_kit/seam.js`; machine fields as `SC.REST` unless named)

| Cut | After beat | Loop (`S.loop`) | Machine | Code |
|---|---|---|---|---|
| 0 | frame 0 | o 1, ring, u 0 (in the slot), batch 1, slot 0, lit batch | off (`SC.LOOP_ONLY`) | off |
| 1 | hook | same as 0: parked in the slot, lit batch | off | off |
| 2 | forward | u = `LOOP.at("ring","forward")`, lit forward | off | off |
| 3 | loss | u at loss, lit loss | off | off |
| 4 | backward | u at update, lit step (all four) | off | off |
| 5 | next batch | u 0, lit batch | off | off |
| 6 | epoch code | o 0 | REST under the card (invisible) | flip 1; `LOOP.CODE` fully typed, lit outer, cursor 0 |
| 7 | one batch | o 0 | REST, hero batch, flip 0 | off |
| 8 | end | o 0 | REST, hero batch | off |

## Cut list (approved by Chris 2026-10-28, with take `ring`)

Raw take 51.3 s. Pauses capped at 0.25 s (`tighten_vo.py --max-gap 0.25
--noise=-45dB`; `--noise auto` read −52.8 dB and found no pauses, the
room is −72 dB) → **44.7 s, 14 pieces, no phrase cuts.** Every piece
begins and ends on a whole sentence; Parakeet on the result reads clean.
The *(if time)* epoch beat (26.0–34.4 s) stays: it is the code beat.

Caption fixes in `words.json`: "pi -towards" → "PyTorch" (joined).
Parakeet heard "grade 8 descent" and "loss is in moving"; WhisperKit
(the word-time source) has "gradient descent" and "isn't moving", which
are right, so nothing else to fix. Two short captions flash under 0.15 s
("to that", "that's"): the caption tool's usual warning, judged on the
assembled sheet.

Nothing in the take needs an ear check: no number is spoken.

## Not in this Short (on purpose)

What the four stations do (ep 2). The loss values (1.68 / 1.42 / 1.30 are
in the ledger but no beat draws them; "check the batch first" is about the
batch, not a curve). `optimizer.zero_grad()` and logging from diagram 1:
the VO says "four lines", and the card shows four under the loop headers.
