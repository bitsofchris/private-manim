ENGINE: hyperframes

# PyTorch Dataset class (series 014, ep 3 of 5): storyboard (recorded VO)

THE QUESTION: "How do I write a custom Dataset in PyTorch?"
WHO IS ASKING: someone writing their first real training script who has
seen `class MyDataset(Dataset)` in a tutorial and doesn't know which
methods matter or what the DataLoader does with them.
THE ANSWER IN ONE SENTENCE: two functions, how many samples (`__len__`)
and give me sample i (`__getitem__`); the sampler, batching and collate
do the rest.
THE SEARCH PHRASE: pytorch dataset class (also "pytorch custom dataset";
both autocomplete, checked 2026-10-25).

**One idea:** a map-style Dataset is `__len__` + `__getitem__`; because it
is indexable, the sampler owns the order, so shuffle and splits are free.

Series context: `../SERIES.md` (ledger, images, decisions). The VO is
`script.md` (what Chris said), not `../SCRIPTS.md`.

## Ledger (copied from SERIES.md; every beat uses exactly these)

- The data: synthetic time series, **512 points** each; a `SeriesDataset`
  of **512 series**. One sample is a `[512]` tensor (one row of numbers in
  brackets); a batch is `[32, 512]`.
- The loader: `DataLoader(dataset, batch_size=32, shuffle=True,
  drop_last=True)`; the four stations sampler, fetch, batching, collate.
- The sampler's indices: `7 2 5 0 3 1` (`DL_DATA.indices`).
- The Dataset card (`EP.MAP`, from `DL_DATA.code.mapStyle`, text unchanged):

  ```python
  class Series(Dataset):
    def __len__(self):
      return len(self.series)
    def __getitem__(self, i):
      return self.series[i]
  ```

- The hand-rolled loop (`EP.HAND`, from `DL_DATA.code.handRolled`):

  ```python
  perm = torch.randperm(n)
  for i in range(0, n, 32):
    idx = perm[i : i + 32]
    batch = data[idx]
  ```

  randperm → sampler, the range step → batching (the batcher), the slice
  → `__getitem__` plus collate.
- Splits: `Subset(dataset, indices)`, train 460 / val 52 (not drawn; the
  VO's "list of indices" is the sampler's index glyph).

## The look

Two images, never both at once (Chris, 10/28), switching every ~5 s:

1. **The code card** (beats 1, 4, 7, 9, 10; shared `_kit/code.js`): the
   Dataset card `EP.MAP` (five lines) or the hand-rolled loop `EP.HAND`
   (four lines). The hero is a line (magenta gutter bar): `lit` names
   `dataset`, `len`, `getitem`, `slice` (EP.MAP) or `sampler`,
   `batching`, `collate` (EP.HAND). `EP.TWO` lights both methods.
2. **The machine** (beats 2, 3, 5, 6, 8; shared `_kit/machine.js`,
   `SC.REST`, map-style, workers 0): samples hopping from the Dataset card
   into the loader; the hero is a part: `len`, `getitem` (the method names
   on the Dataset card), `sampler`, `batching`, `collate`, `dataset`.

The flip (`S.flip` 0 ↔ 1 over 0.4 s) lands on the word that names the
other image. The longest run on one image is the machine, 20.65–31.14
(10.5 s), which moves through five hero states (sampler, len, sampler,
getitem, sampler + the index pulse), so it is not a still hold.

Captions in the band (y 1100–1536) as usual; the stage is y 230–1100.

Seam states are code: `_kit/seam.js` (`SC.SEAM[0..10]`); the table below
is its prose. Episode helpers: `_kit/ep.js` (`EP.MAP`, `EP.HAND`,
`EP.TWO`, `EP.litAt`).

## Beats (VO from script.md; times are vo_final seconds, master)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Hook: two functions | A PyTorch dataset class has two functions. How many samples, and how do I get sample i? | Frame 0: the Dataset card on stage, the last line `return self.series[i]` already typing (`SEAM[0]`), done by ~0.9 s, cursor blinking. "two functions" (2.20): both method lines lit (`EP.TWO`). "How many samples" (3.36): `__len__` line. "get sample i" (4.98): `__getitem__` line. Cursor off by 5.6; still: SEAM[1]. | the line being typed → both methods → len → getitem |
| 2 | The loader's job | Everything else is the data loader's job. | "Everything" (6.32): flip to the machine (hero none). "data loader's" (7.34): a sweep down the stations, sampler → fetch → batching → collate, ~0.22 s each; ends with none lit. Still: SEAM[2]. | each station in turn |
| 3 | len, getitem | `__len__` returns the number of samples. `__getitem__` returns sample at index i. | Machine. "`__len__`" (8.54): `len` the hero. "`__getitem__`" (10.94): `getitem` the hero. "index i" (12.80): a short `getitem` emphasis (label swell via `kit.parts.getitem.dom`, restored). Samples keep hopping (SC.clock). Still from ~13.4: SEAM[3]. | len → getitem |
| 4 | Just a slice | Here, the series are precomputed into one tensor, so `__getitem__` is just a slice. Because you can index into the dataset, | "Here" (14.02): flip to the Dataset card, fully typed, `getitem` lit. "slice" (18.16): the hero passes to `return self.series[i]` (`slice`). "index" (19.50): back to `getitem`. Still: SEAM[4]. | getitem → slice → getitem |
| 5 | The sampler owns the order | the sampler owns the order. It uses the length to make a random sequence of indices and calls `__getitem__` on each one. | Beat opens on the card; flip to the machine over the first 0.4 s, `sampler` the hero on "sampler" (20.92). "length" (23.34): `len`. "random sequence of indices" (24.02): `sampler`. "calls `__getitem__`" (25.44): `getitem`. Samples hop throughout. Still: SEAM[5]. | sampler → len → sampler → getitem |
| 6 | Shuffling is free | So shuffling is free, and the validation split is just a list of indices. | Machine. "shuffling" (27.56): `sampler`. "list of indices" (30.22): the sampler's index glyph `7 2 5 0 3 1` pulses once (scale via `kit.parts.sampler.dom`, restored by 30.9). Still: SEAM[6]. | sampler |
| 7 | You already wrote this | If you've ever shuffled with `torch.randperm` and sliced batches by hand, you already wrote this. | "If" (31.45): flip to the empty `EP.HAND` card; it types from 31.6 (`SC_typedAt`, ~28 cps) so `perm = torch.randperm(n)` is done near "torch.randperm" (32.48–33.4) and all four lines by ~35.0; the hero is the line being typed (`EP.litAt`). "already wrote this" (35.14): cursor off, nothing lit. Still: SEAM[7]. | the line being typed |
| 8 | The three parts | Randperm is the sampler. The range step is the batcher, and the slice is `__getitem__` plus collate. | Beat opens on the card; flip to the machine over the first 0.4 s. "Randperm"/"sampler" (36.48/37.24): `sampler`. "range step" (38.22): `batching`. "the slice is `__getitem__`" (40.56): `getitem`. "collate" (41.30): `collate`. Still: SEAM[8]. | sampler → batching → getitem → collate |
| 9 | Map style | This is called a map style dataset. You use it when random access is cheap. | "This" (42.22): flip to the Dataset card, fully typed; "map style dataset" (42.78): `class Series(Dataset):` lit (`dataset`). "random access" (44.64): the hero passes to `slice`. Still: SEAM[9]. | dataset → slice |
| 10 | Closer | If you write these two functions first, the loader, the shuffle, and the split will come for free. | The Dataset card stays. "two functions" (46.96): both method lines lit (`EP.TWO`), held to the end. The last frame is this card. | the two methods |

## Final beats (the contract; `vo_final.wav` 50.500 s, master seconds)

Links per beat (from this folder): `ln -s ../../../_shared/web/vendor NN/vendor`,
`ln -s ../../_kit NN/kit`, `ln -s ../_kit NN/ep`. Clips `media/hf/NN.mp4`
(`beats.json`).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.000 | 6.050 | A PyTorch dataset class has two functions. How many samples and how do I get sample i? |
| 2 | `02_loader_job` | 6.050 | 2.260 | Everything else is the data loader's job. |
| 3 | `03_len_getitem` | 8.310 | 5.440 | `__len__` returns the number of samples. `__getitem__` returns sample at index i. |
| 4 | `04_slice` | 13.750 | 6.900 | Here, the series are precomputed into one tensor, so `__getitem__` is just a slice. Because you can index into the dataset, |
| 5 | `05_sampler` | 20.650 | 6.570 | the sampler owns the order. It uses the length to make a random sequence of indices and calls `__getitem__` on each one. |
| 6 | `06_shuffle` | 27.220 | 3.915 | So shuffling is free and the validation split is just a list of indices. |
| 7 | `07_by_hand` | 31.135 | 5.085 | If you've ever shuffled with torch.randperm and sliced batches by hand, you already wrote this. |
| 8 | `08_three_parts` | 36.220 | 5.750 | Randperm is the sampler. The range step is the batcher, and the slice is `__getitem__` plus collate. |
| 9 | `09_map_style` | 41.970 | 4.165 | This is called a map style dataset. You use it when random access is cheap. |
| 10 | `10_closer` | 46.135 | 4.365 | If you write these two functions first, the loader, the shuffle, and the split will come for free. |

Cues (master, from `words.json`): two@2.20 functions@2.32 How@3.36
samples@3.68 get@4.98 sample@5.18 i?@5.52 | Everything@6.32 data@7.34
loader's@7.56 job@7.88 | `__len__`@8.54 number@9.58 `__getitem__`@10.94
index@12.80 i@13.18 | Here@14.02 tensor@15.88 slice@18.16
Because@19.02 index@19.50 dataset@20.22 | the@20.80 sampler@20.92
order@21.72 length@23.34 random@24.02 indices@24.92 calls@25.44
`__getitem__`@25.86 | So@27.46 shuffling@27.56 free@28.12
validation@28.92 list@30.22 indices@30.52 | If@31.45 torch.randperm@32.48
sliced@33.80 hand@34.82 already@35.14 this@35.78 | Randperm@36.48
sampler@37.24 range@38.22 batcher@39.06 slice@39.80
`__getitem__`@40.56 collate@41.30 | This@42.22 map@42.78 dataset@43.24
random@44.64 cheap@45.46 | If@46.41 two@46.96 functions@47.14
loader@48.04 shuffle@48.50 split@48.88 free@49.58

## Seam states (`_kit/seam.js`; machine fields as `SC.REST` unless named)

| Cut | After beat | Image | State |
|---|---|---|---|
| 0 | frame 0 | card | flip 1, `EP.MAP` typed to line 5 + 6 chars, lit getitem, cursor 1 |
| 1 | hook | card | `EP.MAP` fully typed, lit getitem, cursor 0 |
| 2 | loader job | machine | REST, hero none |
| 3 | len, getitem | machine | REST, hero getitem |
| 4 | just a slice | card | `EP.MAP`, lit getitem |
| 5 | sampler owns order | machine | REST, hero getitem |
| 6 | shuffling is free | machine | REST, hero sampler (index glyph at rest scale) |
| 7 | already wrote this | card | `EP.HAND` fully typed, lit none, cursor 0 |
| 8 | three parts | machine | REST, hero collate |
| 9 | map style | card | `EP.MAP`, lit slice |
| 10 | end | card | `EP.MAP`, lit `EP.TWO` |

The machine is map-style, workers 0, batch landed, sampler on in every
machine state. The flip is the kit's (S.flip); a beat flipping out of a
card passes the card state through so the fade matches.

## Cut list (pending Chris)

Raw take 63.6 s → **50.5 s**, 9 pieces. Loudnorm only (default chain; the
take's Studio Sound status is unknown, and no denoise was applied).
`tighten_vo.py --max-gap 0.25 --noise=-45dB --level -14 --remove
16.05-21.40 --remove 55.4-58.7`.

- **Cut:** the flub "In this" + its 4.1 s pause (take 16.05–21.40, 5.4 s).
- **Cut:** a 2.8 s breath before the closer (take 55.4–58.7; −53 dB, which
  `--noise auto` (−53.2) would have kept as speech).
- Pauses capped at 0.25 s (−45 dB threshold: `--noise auto` read
  room-tone peaks as speech and capped nothing).
- No phrase cuts; every piece starts and ends on a sentence. Parakeet on
  the result reads clean.

For the ear (both recognizers agree, the script differs):
"has two functions" (script: "is two functions"); "the validation
split" (script: "a"); "the loader, the shuffle" (Parakeet on the raw take
heard "the load or the shuffle"; on the final it reads "the loader").

Caption spellings in `words.json`: Len/GetItem → `__len__`/`__getitem__`
(the names on the card), "pre -computed" → "precomputed", "torch
.randperm" → "torch.randperm", "+" → "plus", "colate" → "collate", "i?"
after "sample i".

## Not in this Short (on purpose)

Map-style is cheap random access, not "fits in memory" (written
companion). `drop_last` as the range stop. `Subset` code (the VO's "list
of indices" is drawn as the sampler's indices). Workers (ep 5).
