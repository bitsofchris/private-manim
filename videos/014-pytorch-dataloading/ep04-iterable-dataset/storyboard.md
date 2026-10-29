ENGINE: hyperframes

# PyTorch IterableDataset (series 014, ep 4 of 5): storyboard (recorded VO)

THE QUESTION: "When do I need an IterableDataset instead of a normal Dataset?"
WHO IS ASKING: someone writing their first real PyTorch training script who
has seen `IterableDataset` in the docs and can't say when map-style stops
being enough.
THE ANSWER IN ONE SENTENCE: if looking up one sample isn't cheap, you use an
iterable dataset: one function, `__iter__`, that yields samples, and the
DataLoader on top stays the same.
THE SEARCH PHRASE: pytorch iterable dataset (not in autocomplete, checked
2026-10-25; ships under it anyway, judged at day 10: SERIES.md "Agreed").

**One idea:** an iterable dataset has no sample i, so no sampler; the loader
just asks for the next one, and shuffling and splitting become yours.

Series context: `../SERIES.md` (ledger, images, decisions). The VO is
`script.md` (what Chris said), not `../SCRIPTS.md`.

## Ledger (copied from SERIES.md; every beat uses exactly these)

- The data: synthetic time series, **512 points** each. One sample is a
  `[512]` tensor, drawn as one row of numbers in brackets (the readout
  `0.3 −1.2 ⋯ / 0.7 0.1 ⋯ / −0.8 0.5 ⋯`). **One batch is `[32, 512]`.**
- The loader: `DataLoader(dataset, batch_size=32, shuffle=True,
  drop_last=True)`; the four stations sampler, fetch, batching, collate.
- Iterable: `__iter__` only; `len(stream)` raises `TypeError`. The card
  types `kit/data.js` `code.iterable` (the ledger's `SyntheticSeriesStream`
  as the kit abbreviates it):

  ```python
  class Stream(IterableDataset):
    def __iter__(self):
      while True:
        yield next_series()
  len(stream)  # TypeError
  ```

- Map-style's method, for the contrast card: `def __getitem__(self, i):`
  (`code.mapStyle[3]`). Beat 9's card shows it under `def __iter__(self):`.
- No number is drawn that is not above. The shards carry no index or count.

## The look

Two images, never both at once (Chris, 10/28), and something new on
screen about every 5 s (`agents/style.md`, Shorts rules):

1. **The machine, iterable** (`kit/machine.js`, `mode: "iterable"`,
   `strike: 1`): the Dataset card shows `__iter__` only, the sampler station
   is struck through, samples hop from the card into the DataLoader box.
   Frame 0 is this, `__iter__` the hero. Episode prop, **the shards**
   (`_kit/ep4.js`, `S.shards`): three small file cards (panel, ink border,
   teal rows, the worker-card style) in a row under the Dataset card's left
   half, y 416–484, clear of the hopping samples. They appear on "shards",
   reorder on "pre-shuffle", and one rises into the Dataset card on "load
   one shard into memory". Through the machine run (beats 5–8, 15 s) the
   image moves through distinct states: sampler hero, shards
   shuffle/load, workers 0 → 2, stations lighting.
2. **The code card** (`kit/code.js`), flipped to with `S.flip` 0 → 1 over
   0.4 s, typed with `SC_typedAt`. Rows at 46 px in this episode (the class
   line is 30 characters; `_kit/ep4.js`). Three cards: `EP4.ITER` (beat 2),
   `EP4.LEN` (beat 4), `EP4.CMP` (beat 9). The hero is the lit line.

Beat 10 flips back to the machine in **map** mode (`__len__`,
`__getitem__`, sampler not struck; the mode change is hidden by the flip)
and swaps it to iterable on "swap", so the last frame is frame 0 again.

Captions in the band (y 1100–1536) as usual. Palette and sizes from the
kit. Seam states are code: `_kit/seam.js` (`SC.SEAM[0..10]`).

## Beats (VO from script.md; times are vo_final seconds, master)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook | If looking up one sample isn't cheap, you use an iterable dataset. | Frame 0: the iterable machine running (SEAM[0]). "iterable dataset" (2.76): `__iter__` pulses once (a `hero` dip to null and back, 0.3 s). Otherwise still; samples hop. | `__iter__` |
| 2 | One function (code) | Here, we use one function, iter, that just yields samples. | "Here" (4.08): flip to the card, `EP4.ITER` types fast (cps ~34; the class line may land already typed so the rest fits). `def __iter__(self):` the hero by "iter" (5.36); the yield line typed and the hero by "yields" (6.16). Cursor off, still: SEAM[2]. | the line being typed → `__iter__` → yield |
| 3 | Shards | I most frequently use this when training bigger models. You pack the data into shards and just stream them through. | "I" (7.61): flip back to the machine, `__iter__` the hero. "shards" (10.62): the three shards fade in under the Dataset card, hero passes to them (machine hero null). "stream" (11.46): samples keep hopping; the shards pulse once (opacity dip). Still: SEAM[3]. | `__iter__` → the shards |
| 4 | No length (code) | There's no length and no get item. Sample i doesn't exist until the iterator produces it. | "There's" (12.69): flip to `EP4.LEN` with the four class lines already typed and row 5 empty; `len(stream)  # TypeError` types from ~12.9 and is the hero by "length" (13.00)–"get item" (13.50). "produces" (16.24): the hero passes to the yield line. Still: SEAM[4]. | the TypeError line → yield |
| 5 | No sampler | This means there's no sampler. The loader just calls your dataset over and over and it yields the next sample. | "This" (17.24): flip back to the machine, shards on at rest. "sampler" (17.92): the struck sampler station the hero. "calls your dataset" (19.06): the Dataset card the hero. "yields" (20.54): `__iter__` the hero. Samples keep hopping. Still: SEAM[5]. | sampler → dataset → `__iter__` |
| 6 | Shuffle | So shuffling is now your problem. You pre-shuffle the data into shards, load one shard into memory, and yield from it. | "shuffling" (22.08): the shards the hero. "pre-shuffle" (23.74–24.5): the three reorder to `[2, 0, 1]` (hop between slots, `S.shards.pos`). "load" (25.42)–"memory" (26.16): the first card (card 2) rises into the Dataset card and fades (`load` 0 → 1). "yield" (26.62): `__iter__` the hero, shards back to ink. Still: SEAM[6]. | shards → `__iter__` |
| 7 | Splits *(if time)* | Splits are also your problem, too. If you run multiple workers, splitting the stream between them is up to you to determine. | "Splits" (27.58): the shards pulse as the hero. "multiple workers" (29.42): `workers` 0 → 2 (the second photocopy fades in, `×2` appears), fetch the hero. Still from ~30.5: SEAM[7]. | shards → fetch |
| 8 | Same loader | The data loader on top is the same though. Same batch size, same collate, same batch out. | "data loader" (32.96): the Dataset card and shards dim to 0.45 (`S.dataset`), hero null: the loader box stands alone. "batch size" (35.16): batching the hero; "collate" (35.82): collate; "batch out" (36.40): the batch card. Dataset back to 1 by 36.6. Still: SEAM[8]. | batching → collate → batch |
| 9 | Next, not i (code) | The only thing that changes the data loader is asking for the next sample, not for the sample at index i. | "The" (37.24): flip to `EP4.CMP`; `def __iter__(self):` types, then `def __getitem__(self, i):`, both done by ~39.3. "next sample" (39.50): `__iter__` line the hero. "index i" (41.22): the hero passes to the `__getitem__` line. The machine's hidden fields go to SEAM[9]'s (workers 0, shards off) once flip ≥ 0.6. Still: SEAM[9]. | `__iter__` → `__getitem__` |
| 10 | Swap | So use map until you can't, and the day sample i stops being cheap, swap to an iterable dataset. | "So" (42.32): flip back to the machine in **map** mode, sampler unstruck, `__getitem__` the hero (continuing the card's lit line). "swap" (45.38): mode → iterable (methods swap), the strike draws across the sampler over 0.6 s, `__iter__` the hero by "iterable" (45.92). The last frame is frame 0's state. | `__getitem__` → `__iter__` |

## Final beats (the contract; `vo_final.wav` 47.243 s, master seconds)

Beat brief: `BRIEF.md` (reads `agents/beat-brief-hyperframes.md`) plus this
table; seam states `SC.SEAM` in `_kit/seam.js`; links per beat: `vendor`,
`kit`, `ep`.

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook_iter` | 0.000 | 3.750 | If looking up one sample isn't cheap, you use an iterable dataset. |
| 2 | `02_iter_code` | 3.750 | 3.535 | Here, we use one function, iter, that just yields samples. |
| 3 | `03_shards` | 7.285 | 5.150 | I most frequently use this when training bigger models. You pack the data into shards and just stream them through. |
| 4 | `04_no_len_code` | 12.435 | 4.595 | There's no length and no get item. Sample i doesn't exist until the iterator produces it. |
| 5 | `05_no_sampler` | 17.030 | 4.710 | This means there's no sampler. The loader just calls your dataset over and over and it yields the next sample. |
| 6 | `06_shuffle` | 21.740 | 5.620 | So shuffling is now your problem. You pre-shuffle the data into shards, load one shard into memory, and yield from it. |
| 7 | `07_splits` | 27.360 | 5.199 | Splits are also your problem, too. If you run multiple workers, splitting the stream between them is up to you to determine. |
| 8 | `08_same_loader` | 32.559 | 4.501 | The data loader on top is the same though. Same batch size, same collate, same batch out. |
| 9 | `09_next_code` | 37.060 | 4.980 | The only thing that changes the data loader is asking for the next sample, not for the sample at index i. |
| 10 | `10_swap` | 42.040 | 5.203 | So use map until you can't, and the day sample i stops being cheap, swap to an iterable dataset. |

## Seam states (`_kit/seam.js`; machine fields: `mode: "iterable"`, `strike: 1`, `workers: 0` unless named)

| Cut | After beat | Image | State |
|---|---|---|---|
| 0 | frame 0 | machine | iterable, sampler struck, hero `iter`, shards off |
| 1 | hook | machine | same |
| 2 | one function | card | flip 1, `EP4.ITER` fully typed, lit `yield`, cursor 0 |
| 3 | shards | machine | hero null, shards on `[0,1,2]`, shards hero |
| 4 | no length | card | `EP4.LEN` fully typed, lit `yield` |
| 5 | no sampler | machine | hero `iter`, shards on `[0,1,2]` at rest |
| 6 | shuffle | machine | hero `iter`, shards `[2,0,1]`, card 2 loaded (gone) |
| 7 | splits | machine | hero `fetch`, shards as 6, workers 2 |
| 8 | same loader | machine | hero `batch`, shards as 6, workers 2 |
| 9 | next, not i | card | `EP4.CMP`, lit `getitem` (machine fields hidden: iterable, workers 0, shards off) |
| 10 | end | machine | = cut 0: iterable, struck, hero `iter`, shards off |

## Cut list (awaiting Chris)

Raw take 52.7 s (Descript export; Studio Sound unknown, so loudnorm only,
no denoise: SERIES.md "How it was recorded"). `tighten_vo.py --max-gap 0.25
--noise=-40dB --level -14` → **47.2 s, 8 pieces, no phrase cuts.**
`--noise auto` put the threshold at −53 dB (the take's floor is −73 dB)
and kept the breaths as speech: 52.6 s with a 1.5 s hole at 8 s. −40 dB,
as ep 1 used, closes every pause to 0.25 s; every piece begins and ends
on a whole sentence.

Flagged in the take:
- "There's no length **and** no get item": WhisperKit hears "and",
  Parakeet "of" (on the cut) or nothing (on the take), `script.md` has
  "no length, no get item". No join falls in that sentence; the caption
  follows the ear.
- "The only thing that changes the data loader…": WhisperKit added "is
  that" pinned 20 ms before "the" (a hallucination; Parakeet and
  `script.md` agree). Joined away in `words.json`.
- "Splits are **also** your problem **too**": a doubled "also … too". Left
  in (a mid-phrase cut for 0.3 s isn't worth a splice).
- The *(if time)* splits beat (beat 7, 5.2 s) was read; cutting it gives
  42.0 s and shortens the machine run to ~10 s.

Caption fixes in `words.json`: `pre -shuffle` → `pre-shuffle`; `getItem.`
→ `get item.`; `batch i,` → `batch size,`; the closer's "iterable" came
through right on WhisperKit (no `interval` fix needed).

## Not in this Short (on purpose)

Shuffle buffers and pre-shuffled shard layouts (companion). The
`get_worker_info()` shard fix (ep 5's payoff; beat 7 only says splitting is
yours). torchdata.
