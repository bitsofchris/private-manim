ENGINE: hyperframes

# PyTorch DataLoader explained (series 014, ep 2 of 5): storyboard (recorded VO)

THE QUESTION: "What does the PyTorch DataLoader actually do?"
WHO IS ASKING: someone writing their first real training script who has
typed `DataLoader(dataset, batch_size=32, shuffle=True)` from a tutorial
and can't say what it does with those arguments.
THE ANSWER IN ONE SENTENCE: the Dataset hands back one sample; the
DataLoader calls it n times and hands back a batch, through four stations
(sampler, fetch, batching, collate), and every argument you pass is one of
those stations.
THE SEARCH PHRASE: pytorch dataloader explained (autocompletes, checked
2026-10-25).

**One idea:** the DataLoader is a machine with four stations; each argument
is a knob on one of them.

Series context: `../SERIES.md` (ledger, images, decisions). The VO is
`script.md` (what Chris said), not `../SCRIPTS.md`. Ep 2 ends as recorded,
on the batch arriving at the model; there is no closer (Chris, 10/28).

## Ledger (copied from SERIES.md; every beat uses exactly these)

- The data: synthetic time series, **512 points** each; a `SeriesDataset`
  of **512 series**. One sample is a `[512]` tensor, drawn as one row of
  numbers in brackets. The batch card is the readout `0.3 −1.2 ⋯ / 0.7
  0.1 ⋯ / −0.8 0.5 ⋯` with its shape `[32, 512]` beside it.
- The loader: `DataLoader(dataset, batch_size=32, shuffle=True,
  drop_last=True)`. **One batch is `[32, 512]`.**
- The four stations, in this order: sampler, fetch, batching, collate.
  `shuffle=True` → sampler; `num_workers` → fetch; `batch_size` →
  batching; collate packs them into one tensor.
- The sampler's glyph: `7 2 5 0 3 1` (`_kit/data.js` `indices`).
- Workers: 0 until the fetch beat, then **2** (`num_workers=2`, the
  photocopies `×2`).
- The code card (shared `_kit/data.js` `code.loader`, the approved
  canonical frame's card; each line lights its station's name as the hero):

  ```python
  loader = DataLoader(dataset,     # lit: dataset
    batch_size=32,                 # lit: batching
    shuffle=True,                  # lit: sampler
    num_workers=2)                 # lit: fetch
  ```

  `drop_last=True` is in the ledger's loader but not on the kit's card,
  and the VO never names it (hand-off note).

## The look

Two images, never both at once (Chris, 10/28):

1. **The machine** (shared `_kit/machine.js`, `SC.REST`): the Dataset card
   at the top, samples (one bracketed row of numbers each) hopping into
   the DataLoader's dashed box with its four stations, the `[32, 512]`
   batch card leaving to the model chip. Running from frame 0 (`SC.clock`
   = master seconds keeps the hop continuous across cuts). The hero is
   whatever the VO names: the batch, the dataset, each station in turn,
   the model.
2. **The code card** (shared `_kit/code.js`): beat 3 only. `S.flip` 0 → 1
   over 0.4 s, the four lines typed with `SC_typedAt` (cps 30), the line
   being typed is the hero; on "sits at the front" the `dataset` line is
   lit again (the dataset is the call's first argument), and beat 4 flips
   back to the machine with the Dataset card lit.

Captions in the band (y 1100–1536) as usual; the stage is y 230–1100.
Palette and sizes from the kit. Seam states are code: `_kit/seam.js`
(`SC.SEAM[0..9]`); the seam table below is its prose.

**Why the code beat sits on "every argument you pass is one of those
stations"**: it is the line that names the arguments. Typing all four
lines takes 2.6 s at cps 30 (3.5 s at the kit's default 22), so the card
holds through "Your dataset sits at the front" and flips back on "All it
knows", the line that returns to the Dataset card in the machine.

## Beats (VO from script.md; times are vo_final seconds, master)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook | In PyTorch, the dataset's job is to hand back one sample, and the data loader's job is to call it n number of times and hand back a batch. | Frame 0: the machine running (SEAM[0]), the batch card the hero. "dataset's" (1.40): hero → Dataset card. "one sample" (2.78): the sample leaving the card is the one the eye follows (no new part; the hop is already running). "call it n number of times" (5.40–6.86): hero → batching (its `×32`). "a batch" (7.78): hero → the batch card, which pulses once. Still from ~8.2: SEAM[1]. | batch → dataset → batching → batch |
| 2 | Stations | The data loader is a machine with four different stations, | "machine" (9.48): hero off the batch (null). "four" (10.08): the four stations light in turn, top to bottom, ~0.25 s each (sampler, fetch, batching, collate), one at a time, the last returning to rest by ~11.0. Ends SEAM[2]. | each station in turn |
| 3 | Arguments, the code | and every argument you pass is one of those stations. Your dataset sits at the front. | "and" (11.18): flip 0 → 1 (0.4 s). Typing from 11.30 (cps 30, `SC_typedAt(code.loader, t − 11.30, 30)`): the line being typed is the hero (dataset, batching, sampler, fetch), done ~13.9; cursor blinks, then off. "sits" (14.06): `lit` back to `dataset`. Still from ~14.2: SEAM[3]. | the line being typed, then dataset |
| 4 | Dataset | All it knows is how to go get one sample wherever that data lives. | "All" (15.20): flip 1 → 0, the machine back with the Dataset card the hero (SEAM[3] → SEAM[4] differ only in flip). "one sample" (16.48): the Dataset card pulses once. Still otherwise. | dataset |
| 5 | Sampler | The first station is the sampler. It decides the order. Shuffle equals true is a random sampler, a random sequence of indices. | "sampler" (19.88): hero → sampler. "order" (21.18): the indices `7 2 5 0 3 1` pulse once. "random sequence of indices" (24.32): the indices pulse again (or a one-frame accent). Ends SEAM[5]. | sampler |
| 6 | Fetch | Second up is fetch. Workers will call your dataset with those indices in parallel if you ask for them. | "fetch" (26.80): hero → fetch. "Workers" (27.45): workers 0 → 1 (the half-faint photocopy firms up). "parallel" (29.80): workers 1 → 2 (the second photocopy and `×2` grow in, ~0.3 s). Ends SEAM[6]. | fetch |
| 7 | Batching | Third is batching. It collects batch-sized samples. | "batching" (31.87): hero → batching. "batch-sized" (32.94): the `×32` pulses once. Ends SEAM[7]. | batching |
| 8 | Collate | And fourth is collate. This is what packs them into one tensor shaped for the GPU. | "collate" (35.68): hero → collate. "one tensor" (37.28): hero → the batch card. "shaped" (37.90): the batch card's `[32, 512]` pulses once. Ends SEAM[8]. | collate → batch |
| 9 | Out | Out comes the batch and what goes into the forward pass. | "Out comes the batch" (39.66): the batch card pulses (it leaves). "forward pass" (41.16): a copy of the batch card rides the arrow into the model chip (episode-local glyph, ≥ 0.6 s), arriving as the hero passes to the model. The last frame is still: the batch landed at the model, the model lit: SEAM[9]. | batch → model |

## Final beats (the contract; `vo_final.wav` 42.362 s, master seconds)

Beat brief: `agents/beat-brief-hyperframes.md` plus this table; seam
states `SC.SEAM` in `_kit/seam.js`; links per beat: `vendor`
(`../../../_shared/web/vendor`), `kit` (`../../_kit`), `ep` (`../_kit`).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.000 | 8.470 | In PyTorch, the dataset's job is to hand back one sample, and the data loader's job is to call it n number of times and hand back a batch. |
| 2 | `02_stations` | 8.470 | 2.630 | The data loader is a machine with four different stations, |
| 3 | `03_args_code` | 11.100 | 3.920 | and every argument you pass is one of those stations. Your dataset sits at the front. |
| 4 | `04_dataset` | 15.020 | 3.730 | All it knows is how to go get one sample wherever that data lives. |
| 5 | `05_sampler` | 18.750 | 7.130 | The first station is the sampler. It decides the order. Shuffle equals true is a random sampler, a random sequence of indices. |
| 6 | `06_fetch` | 25.880 | 5.355 | Second up is fetch. Workers will call your dataset with those indices in parallel if you ask for them. |
| 7 | `07_batching` | 31.235 | 3.665 | Third is batching. It collects batch-sized samples. |
| 8 | `08_collate` | 34.900 | 4.390 | And fourth is collate. This is what packs them into one tensor shaped for the GPU. |
| 9 | `09_out` | 39.290 | 3.072 | Out comes the batch and what goes into the forward pass. |

## Seam states (`_kit/seam.js`; machine fields as `SC.REST` unless named)

| Cut | After beat | Image | State |
|---|---|---|---|
| 0 | frame 0 | machine | REST, workers 0, hero batch, flip 0 |
| 1 | hook | machine | same: hero batch |
| 2 | stations | machine | workers 0, hero null (no station lit) |
| 3 | arguments code | card | flip 1, `code.loader` fully typed, lit dataset, cursor 0; machine under it hero dataset |
| 4 | dataset | machine | workers 0, hero dataset |
| 5 | sampler | machine | workers 0, hero sampler |
| 6 | fetch | machine | **workers 2**, hero fetch |
| 7 | batching | machine | workers 2, hero batching |
| 8 | collate | machine | workers 2, hero batch |
| 9 | end | machine | workers 2, hero model (plus beat 9's landed batch copy at the chip) |

The sampler is never struck (map-style), twins 0, shape `[32, 512]`
throughout.

## Cut list

Raw take 52.1 s (studio chain unknown; `enhance_vo.sh` default, loudnorm
only, floor −65 dB). `tighten_vo.py --max-gap 0.25 --noise=-40dB --remove
28.12-30.62 --level -14` → **42.4 s, 10 pieces, one phrase cut.**

- **Cut 28.12–30.62 s (2.5 s):** the flub "a random sequences of indices"
  and the breath after it; the re-read "a random sequence of indices"
  follows "random sampler," directly. Edges at the envelope dips (end of
  "sampler" at 28.1, the re-read's onset at 30.65).
- `--noise auto` (−53 dB) found no pauses (breaths sit above it) and left
  50.7 s; −45 dB kept a 0.8 s breath after "lives" as a piece; −40 dB
  drops it (as ep 1 needed).
- Kept as said: "n number of times" (script: 32), "Second up", "Workers
  will call", "and what goes into the forward pass". No other repeats.
- The last piece ends on "pass." (51.46 in the take; the file ends at 52.1,
  before "so episode three").
- Parakeet on `vo_final.wav` reads clean, every sentence whole.

Caption fixes in `words.json`: "batch -sized" → "batch-sized" (joined).

## Not in this Short (on purpose)

`drop_last` (the batcher's stop: written companion); "the DataLoader never
loads your data" (the unread *(if time)* beat); a closer (none recorded);
`num_workers` duplicates (ep 5).
