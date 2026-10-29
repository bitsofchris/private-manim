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

Three images, never two at once, and **the image changes about every
5 s** (`agents/style.md`, Shorts rules; Chris on the first cut: 26 s on
the loop was too long). Each image comes back whenever the VO returns to
it; the seam-state kit makes a return cheap.

1. **The machine** (beats 1, 9, 10; shared `_kit/machine.js`, `SC.REST`):
   the series image, samples hopping from the Dataset card into the
   DataLoader box, the `[32, 512]` batch going to the model chip. The
   batch is the hero. The Short opens on it (a batch is samples packed
   into one tensor: that is the collate station and the batch card).
2. **The loop** (beats 2, 3, 5, 7; `_kit/loop.js`, take `ring`):
   diagram 1 redrawn in the card style. The DataLoader card at the top
   with a slot where a batch glyph sits; four boxes under its right half:
   forward, loss, backward, update. A muted track leaves the slot, runs
   down past the boxes, under update, and back up the left gutter,
   dashed, into the slot. The glyph rides the track and is the hero while
   the VO is about it; a box turns magenta as the VO names it.
3. **The code card** (beats 4, 6, 8, 11; shared `_kit/code.js`): the
   stage flips to it (`S.flip` 0 → 1 over 0.4 s). Beats 4 and 6 show the
   four body lines (`LOOP.BODY`, indented as they will sit under the
   headers); beat 8 types the two `for` headers in above them
   (`code.typedLines`); beat 11 shows all six with the four body lines
   lit together (`LOOP.STEP`). VS Code colours; the hero line is a
   magenta gutter bar. Typing is human-paced (`SC_typedAt`).

Captions in the band (y 1100–1536) as usual; the stage is y 230–1100 and
the code card is centred on it. Palette and sizes from the kit: 60 px
Inter 800 labels, 48 px monospace code.

Seam states are code: `_kit/seam.js` (`SC.SEAM[0..11]`); the table below
is its prose.

## Beats (VO from script.md; times are vo_final seconds, master)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook: the batch | A batch is just a bunch of samples packed into one tensor so the GPU can parallelize. | Frame 0: the machine at rest, samples already hopping (the series image). "packed into one tensor" (2.26–3.0): the batch card pulses once. Still otherwise. | the batch |
| 2 | Hook: the loop | And a PyTorch training loop is what happens to that one batch. | "And" (5.38): flip 0 → the loop appears (machine fades, loop fades in over 0.4 s via `S.flip`-style crossfade: the beat lerps `loop.o` 0→1 and `SC.LOOP_ONLY` opacities 1→0). "training loop" (5.98): the whole track pulses magenta once. "one batch" (7.24): the glyph in the slot pulses (lit batch from here). Ends still: SEAM[2]. | the track, then the batch |
| 3 | Forward | The data loader yields it, the batch goes into the forward pass, and the model makes a prediction. | "yields it" (8.82): the glyph leaves the slot and rides to beside forward, arriving on "forward pass" (10.64); forward lights on arrival. "prediction" (12.18): forward pulses once. Ends: SEAM[3]. | the batch, then forward |
| 4 | Loss, the code | We compare that prediction to the target, and that's the loss. | "We" (12.96): flip to the code card with the four body lines; they type fast (cps ~34) from 13.3 so `loss = loss_fn(out, y)` is complete by "loss" (15.12), when it becomes the hero; the other two lines finish by 15.5. Cursor off, still: SEAM[4]. | the line being typed, then loss |
| 5 | Backward + update | The loss is then propagated backwards, and the weights are updated as part of gradient descent. | "The loss" (15.94): flip back to the loop, the glyph beside loss with loss lit. "backwards" (17.04): rides to beside backward, backward lights. "updated" (18.34): rides to beside update, update lights. Still from 19.2: SEAM[5]. | loss → backward → update |
| 6 | One step, the code | That is one training step. | "That" (20.32): flip to the code card, four body lines fully typed, none lit; "one" (20.76): all four light together (`LOOP.STEP`). Still: SEAM[6]. | the four lines |
| 7 | Next batch | Then we go back to the data loader for the next batch. | "Then" (22.28): flip back to the loop, glyph beside update, update lit; "go back" (22.42): rides the dashed return up the left gutter into the slot, boxes muted, glyph the hero, arriving on "next batch" (23.64). Still: SEAM[7]. | the batch |
| 8 | Epoch, the code | An epoch is one pass through the whole dataset. So this inner loop runs once per epoch, and the outer loop runs for as many epochs as you set. | "An epoch" (24.66): flip to the six-line card with the four body lines already typed and the two header rows empty; the headers type in (`typedLines`, line 0 then line 1, ~22 cps) from 25.1, done by ~27.5. "inner loop" (27.97): `for batch in loader:` the hero; "outer loop" (30.12): `for epoch in range(epochs):` the hero. Cursor off, still from 31: SEAM[8]. | the line being typed, inner, outer |
| 9 | One batch | The model never sees your dataset, it only ever sees one batch at a time. | "The model" (33.0): flip back to the machine at rest; the model chip is the hero. "one batch" (35.82): the hero passes to the batch card. Still: SEAM[9]. | model → the batch |
| 10 | Check the batch | So if your loss isn't moving, check the batch first. | "check the batch" (38.22): the batch card pulses once. Still: SEAM[10]. | the batch |
| 11 | Four lines | Everything downstream of it is the same four lines every time. | "Everything" (39.64): flip to the six-line card, fully typed, none lit; "four lines" (41.38): the four body lines light together and hold. The last frame is this card. | the four lines |

Ep 1 no longer ends on ep 2's frame 0 (the machine): Chris wants the four
lines on screen for the closing line. Each Short is found alone; noted
for the update pass (SERIES.md "The look").

## Final beats (the contract; `vo_final.wav` 43.040 s, master seconds)

Beat brief: `BRIEF.md` (reads `agents/beat-brief-hyperframes.md`) plus
this table; seam states `SC.SEAM` in `_kit/seam.js`; links per beat:
`vendor`, `kit`, `ep`.

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook_batch` | 0.000 | 5.120 | A batch is just a bunch of samples packed into one tensor so the GPU can parallelize. |
| 2 | `02_hook_loop` | 5.120 | 2.880 | And a PyTorch training loop is what happens to that one batch. |
| 3 | `03_forward` | 8.000 | 4.750 | The data loader yields it, the batch goes into the forward pass, and the model makes a prediction. |
| 4 | `04_loss_code` | 12.750 | 2.930 | We compare that prediction to the target, and that's the loss. |
| 5 | `05_backward` | 15.680 | 4.320 | The loss is then propagated backwards, and the weights are updated as part of gradient descent. |
| 6 | `06_step_code` | 20.000 | 2.020 | That is one training step. |
| 7 | `07_next_batch` | 22.020 | 2.380 | Then we go back to the data loader for the next batch. |
| 8 | `08_epoch_code` | 24.400 | 8.370 | An epoch is one pass through the whole dataset. So this inner loop runs once per epoch, and the outer loop runs for as many epochs as you set. |
| 9 | `09_one_batch` | 32.770 | 4.175 | The model never sees your dataset, it only ever sees one batch at a time. |
| 10 | `10_check_batch` | 36.945 | 2.395 | So if your loss isn't moving, check the batch first. |
| 11 | `11_four_lines` | 39.340 | 3.700 | Everything downstream of it is the same four lines every time. |

## Seam states (`_kit/seam.js`; machine fields as `SC.REST` unless named)

| Cut | After beat | Image | State |
|---|---|---|---|
| 0 | frame 0 | machine | REST, hero batch, flip 0, loop off |
| 1 | hook: the batch | machine | same |
| 2 | hook: the loop | loop | `SC.LOOP_ONLY`, u 0 (in the slot), lit batch |
| 3 | forward | loop | u at forward, lit forward |
| 4 | loss code | card | flip 1, `LOOP.BODY` fully typed, lit loss, cursor 0 |
| 5 | backward | loop | u at update, lit update |
| 6 | step code | card | `LOOP.BODY`, lit `LOOP.STEP` (the four) |
| 7 | next batch | loop | u 0, lit batch |
| 8 | epoch code | card | `LOOP.CODE` fully typed, lit outer |
| 9 | one batch | machine | REST, hero batch |
| 10 | check batch | machine | same |
| 11 | end | card | `LOOP.CODE`, lit `LOOP.STEP` |

## Cut list (second cut, approved flow 2026-10-28)

Raw take 51.3 s. `tighten_vo.py --max-gap 0.25 --noise=-40dB --remove
15.55-16.25 --level -14` → **43.0 s, 13 pieces, no phrase cuts.** The
first cut (−45 dB) kept a 0.5 s breath after "makes a prediction" as
speech (Chris heard the 1.9 s hole at 13 s); −40 dB plus removing that
breath closes it to 0.25 s. Every piece begins and ends on a whole
sentence; Parakeet on the result reads clean. The *(if time)* epoch beat
stays: it is the code beat.

Caption fixes in `words.json`: "pi -towards" → "PyTorch" (joined);
"And epoch" → "An epoch" (WhisperKit). Two captions flash under 0.15 s
("descent.", "the"): the caption tool's usual warning.

## Not in this Short (on purpose)

What the four stations do (ep 2). The loss values (1.68 / 1.42 / 1.30 are
in the ledger but no beat draws them; "check the batch first" is about the
batch, not a curve). `optimizer.zero_grad()` and logging from diagram 1:
the VO says "four lines", and the card shows four under the loop headers.
