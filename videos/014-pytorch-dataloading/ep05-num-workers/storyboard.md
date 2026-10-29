ENGINE: hyperframes

# PyTorch DataLoader num_workers (series 014, ep 5 of 5): storyboard (recorded VO)

THE QUESTION: "Why does num_workers give me duplicate batches?"
WHO IS ASKING: someone writing their first real PyTorch training script who
raised `num_workers` on a streaming dataset and got the same batch twice.
THE ANSWER IN ONE SENTENCE: num_workers doesn't split your data; each
worker is a full copy of your dataset, so an iterable dataset has to split
the stream itself with `get_worker_info()`.
THE SEARCH PHRASE: pytorch dataloader num_workers (autocompletes, checked
2026-10-25).

**One idea:** each worker is a photocopy of the Dataset; with no sampler
to hand out indices, the copies deliver the same data until `__iter__`
asks which worker it is.

Series context: `../SERIES.md` (ledger, images, decisions). The VO is
`script.md` (what Chris said), not `../SCRIPTS.md`.

## Ledger (copied from SERIES.md; every beat uses exactly these)

- The data: synthetic time series, **512 points** each; a `SeriesDataset`
  of **512 series**, seed 77. A batch on screen is rows of numbers in
  brackets with its shape beside it (`_kit/data.js` `series.readout`).
- The loader in this episode: `DataLoader(SyntheticSeriesStream(seed=77),
  batch_size=4, num_workers=2)`. **One batch is `[4, 512]`** (`smallShape`);
  the batching station reads `×4` (`EP5.mount`).
- The worker trap: `torch.equal(b1, b2)` → **True**; with
  `shard_per_worker=True` → **False**. Worker k takes samples k, k+N, k+2N.
- The four stations: sampler, fetch, batching, collate. Two worker
  photocopies of the Dataset in fetch (`workers: 2`, `×2`). The sampler is
  struck through for an iterable dataset.
- Code cards (`_kit/data.js` text, exactly; `EP5.LINES`):
  - `iterable`: `class Stream(IterableDataset):` / `def __iter__(self):` /
    `while True:` / `yield next_series()`
  - `workers`: `loader = DataLoader(stream,` / `batch_size=4,` /
    `num_workers=2)` / `torch.equal(b1, b2)  # True`
  - `shard`: `info = get_worker_info()` / `start = info.id        # k` /
    `step = info.num_workers` / `torch.equal(b1, b2)  # False`
    (ep 5 tags `start` as lit `k` and `step` as lit `step`)

## The look

Two images, never at once, and something new every ~5 s
(`agents/style.md`): the machine (`../_kit/machine.js`) and the code card
(`../_kit/code.js`), flipped by `S.flip` over 0.4 s. The machine runs in
three states: **the trap** (iterable, sampler struck, two workers, twin
`[4, 512]` batches side by side), **map** (map-style, sampler back, one
batch, the model chip), and **fixed** (the trap with one batch, only ever
under the card at the end). Three code cards: the iterable class (beats 3
and 5), the workers call that prints True (6), the shard that prints
False (8–10).

The magenta hero is what the VO names: the twin pair (both cards, a tight
group: `EP5.draw`), a station, `__iter__`, or the code line being typed.
Teal is data (digits, samples). Captions in the band (y 1100–1536); the
stage is y 230–1100.

Episode helpers in `_kit/` (linked as `ep`): `ep5.js` (`EP5.mount`,
`EP5.draw`, `EP5.LINES`, `EP5.SHARD3`) and `seam.js` (`SC.SEAM[0..10]`).
Every beat mounts with `EP5.mount(root)` and draws with `EP5.draw(kit, S)`.

## Beats (VO from script.md; cue times are vo_final master seconds, words.json)

| # | Beat | VO (as recorded, after the cut) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook: the twins | In PyTorch, num_workers doesn't split your data across the workers. | Frame 0 = SEAM[0]: the trap already running, samples hopping into the loader, two identical `[4, 512]` cards side by side, the pair magenta. "num_workers" (1.56): hero → fetch (the two photocopies, `×2`). | twins → fetch |
| 2 | Full copy | Each worker is a full copy of your dataset, fetching and collating on its own. | "full copy" (5.48): the two worker photocopies pulse once, in turn (fetch stays the hero). "collating" (7.26): hero → collate. | fetch → collate |
| 3 | Same data | So when you run an iterable dataset with multiple workers, every worker gets the same dataset object, and unless you split the stream yourself, they all deliver the same data. | "iterable" (9.42): flip to the iterable card, typed (~30 cps) from ~9.7, the hero following the line being typed (dataset → iter). "same dataset object" (12.54): the class line is the hero. "they" (15.24): flip back to the trap; "same data" (16.12): the twin pair is the hero and pulses once. Ends SEAM[3]. | the line typed → class line → twins |
| 4 | Map is fine | With a map-style dataset, you're fine. The sampler stays in the main process and hands each worker a different set of indices. Every sample here gets fetched once. | "map-style" (17.30): mode → map (dataset card dips and returns with `__len__`/`__getitem__`), the strike pulls back 1 → 0, the twin slides out (twins 1 → 0), the model chip returns; hero dataset. "sampler" (19.28): hero → sampler. "each worker a different set" (21.94–22.82): the two photocopies pulse in turn. "fetched once" (25.08): hero → batch. Ends SEAM[4]. | dataset → sampler → batch |
| 5 | No indices | But with an iterable dataset, there are no indices. Each worker starts the stream from the beginning. So if you have the same seed, you're getting the same data. | "iterable" (26.54): mode → iterable, hero sampler. "no indices" (27.64): the strike draws across the sampler 0 → 1. "Each worker" (28.7): flip to the iterable card, fully typed, `__iter__` lit. "same data" (32.64): flip back; the twin slides in (0 → 1), the pair the hero. Ends SEAM[5]. | sampler → `__iter__` → twins |
| 6 | Code: True | Two workers, batch size four, the first two batches will be identical. | "Two" (33.58): flip to the workers card, typed fast (~40 cps) so the last line is in by ~36.2, hero following the typed line; "identical" (36.32): `torch.equal(b1, b2)  # True` is the hero. Cursor off, still. Ends SEAM[6]. | the typed line → `# True` |
| 7 | The fix lives in iter | The fix lives inside your iter function. | "The" (37.30): flip back to the trap. "iter function" (38.34): hero → `__iter__` on the Dataset card. Ends SEAM[7]. | `__iter__` |
| 8 | Code: worker info | Ask for the worker info and have worker k take every nth sample, starting at k. | "Ask" (39.42): flip to the shard card (the machine under it changes to *fixed* once hidden). Line 0 typed by "worker info" (40.30), lit fetch; line 1 (`start = info.id  # k`) by "worker k" (41.92), lit k; line 2 (`step = …`) by "every nth" (42.90), lit step; "starting at k" (43.96): k and step lit together. The `# False` line not started. Ends SEAM[8]. | the typed line → start + step |
| 9 | Code: False | Now the two copies can walk the stream in step and nothing is delivered twice. | Card stays. "nothing" (47.38): line 3 types (`torch.equal(b1, b2)  # False`), finished on "twice" (48.12), the hero. Still. Ends SEAM[9]. | `# False` |
| 10 | Closer | So before you increase num_workers on an iterable dataset, be sure you're passing that worker info to each iter function so you can split the stream accordingly. | "So" (49.08): flip back to the machine, *fixed* (one batch); "num_workers" (50.36): hero fetch. "passing" (52.66): flip to the shard card, fully typed, `info = get_worker_info()` the hero; holds to the end. The last frame is this card. | fetch → `get_worker_info()` |

## Cut list (proposed; waiting on Chris)

Take: `vo_raw.m4a`, 67.4 s. Clean: `tools/enhance_vo.sh` (high-pass +
loudnorm, the default chain; SERIES.md doesn't say Studio Sound was on, so
no denoise). Floor −73.9 dB raw, −66.9 dB clean.

No flubs or repeated phrases in the take. The two candidates `script.md`
named:

| Cut | Take (s) | Seconds | Proposal |
|---|---|---:|---|
| "…or spread the shards out among workers based on the worker's identity." | 48.30–53.40 | 5.1 | **Cut.** The clause before already gives the fix, and the card shows only the k / N stride. |
| *(if time)* "Now the two copies can walk the stream in step and nothing is delivered twice." | 53.40–57.90 | 4.2 | **Keep.** It is where the card types `# False`, the fix working. Cutting it too gives 53.8 s. |

`tighten_vo.py --max-gap 0.25 --noise=-45dB --level -14 --remove
48.30-53.40` → **57.7 s, 15 pieces.** `--noise auto` (−54.9 dB) found no
pauses: the room tone between phrases on this take sits at −55 to −50 dB, so
the threshold is set by hand (ep01 did the same at −40). Parakeet on the
result reads clean, and it closes "starting at K." with a full stop, so
the voice falls where the cut lands.

Word fixes in `words.json`: "NumWorkers"/"numWorkers" → "num_workers",
"map -style" → "map-style", "Each" (dropped by WhisperKit at 28.7) put
back as "Each worker", "info," → "info".

## Final beats (the contract; `vo_final.wav` 57.717 s, master seconds)

Beat brief: `BRIEF.md` (reads `agents/beat-brief-hyperframes.md`) plus
this table; seam states `SC.SEAM` in `_kit/seam.js`; links per beat:
`vendor`, `kit`, `ep`.

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook_twins` | 0.000 | 4.390 | In PyTorch, num_workers doesn't split your data across the workers. |
| 2 | `02_full_copy` | 4.390 | 3.970 | Each worker is a full copy of your dataset fetching and collating on its own. |
| 3 | `03_same_data` | 8.360 | 8.450 | So when you run an iterable dataset with multiple workers, every worker gets the same dataset object and unless you split the stream yourself, they all deliver the same data. |
| 4 | `04_map_fine` | 16.810 | 9.100 | With a map-style dataset, you're fine. The sampler stays in the main process and hands each worker a different set of indices. Every sample here gets fetched once. |
| 5 | `05_no_indices` | 25.910 | 7.410 | But with an iterable dataset, there are no indices. Each worker starts the stream from the beginning. So if you have the same seed, you're getting the same data. |
| 6 | `06_true_code` | 33.320 | 3.700 | Two workers, batch size 4, the first two batches will be identical. |
| 7 | `07_iter_fix` | 37.020 | 2.110 | The fix lives inside your iter function. |
| 8 | `08_worker_info` | 39.130 | 5.725 | Ask for the worker info and have worker k take every nth sample, starting at k. |
| 9 | `09_false_code` | 44.855 | 3.835 | Now the two copies can walk the stream in step and nothing is delivered twice. |
| 10 | `10_closer` | 48.690 | 9.027 | So before you increase num_workers on an iterable dataset, be sure you're passing that worker info to each iter function so you can split the stream accordingly. |

## Seam states (`_kit/seam.js`; every state has `workers: 2`, `shape: [4, 512]`)

| Cut | After beat | Image | State |
|---|---|---|---|
| 0 | frame 0 | machine | trap (iterable, strike 1, twins 1), hero twins, flip 0 |
| 1 | hook | machine | trap, hero fetch |
| 2 | full copy | machine | trap, hero collate |
| 3 | same data | machine | trap, hero twins |
| 4 | map fine | machine | map (strike 0, twins 0), hero batch |
| 5 | no indices | machine | trap, hero twins |
| 6 | code: True | card | `workers` fully typed, lit twins (`# True`); under it the trap, hero twins |
| 7 | iter fix | machine | trap, hero iter |
| 8 | worker info | card | `shard`, typed `EP5.SHARD3` (three lines), lit [k, step]; under it fixed (twins 0), hero fetch |
| 9 | code: False | card | `shard` fully typed, lit twins (`# False`); under it fixed, hero fetch |
| 10 | end | card | `shard` fully typed, lit fetch (`get_worker_info()`); under it fixed, hero fetch |

## Not in this Short (on purpose)

Spreading shards by worker id (cut from the take; the stride is the one
fix shown). Shuffling a stream, `persistent_workers`, `prefetch_factor`.
How many workers to pick. The map-style card's code (ep 3).
