# PyTorch Dataloading: the series

**Name:** pytorch-dataloading-series
**Description:** Five Shorts on how a batch reaches a PyTorch model: the
training loop, the DataLoader as a machine with four stations, the
map-style Dataset class, the IterableDataset, and what `num_workers`
really does. Each is found alone by its own search phrase and shares one
example (synthetic 512-point time series, batch `[32, 512]`) and one
image (the machine).
**When to use:** at the start of any session on this series. Take the
next unticked episode from the checklist and paste `EPISODE_PROMPT.md`
(with `FOLDER` set) into a fresh session; it runs `agents/runbook.md` in
that folder.
**How it works:** the scripts (`SCRIPTS.md`) were drafted from Chris's
2026-07-24 lecture take and the notebook, he tightened them and recorded
all five in one file on 2026-10-28 (`TRANSCRIPT.md`), split into each
folder's `vo_raw.m4a` + `script.md`. What he said is the VO. The shared
kit (`_kit/`) and the canonical frame (`00_layout/`) are built once here
before episode sessions start (`agents/series.md`, step 5).

Agreed (Chris, 2026-10-25 / 10-28):
- Five episodes, in this order; the collate_fn episode is dropped.
- Re-recorded from the lecture's lines, not spliced from the lecture.
- Ep 4 ships under "pytorch iterable dataset" even though it does not
  autocomplete; judged at day 10.
- Ep 5's claim is the general one: each worker is a full copy of the
  Dataset plus fetch and collate; the sampler stays in the main process.
- "NanoTST" is never in a title (zero search volume); in VO it is "a tiny
  time-series transformer" if named at all.

Plan and the lecture-take line mine: `agents/plans/014-pytorch-dataloading-series.md`.

## Who it is for

Someone writing their first real PyTorch training script. They have typed
`DataLoader(dataset, batch_size=32, shuffle=True)` from a tutorial and
cannot say what it does, which of the two Dataset classes to subclass, or
why `num_workers=4` sometimes hands the model the same batch four times.

## The promise

The Dataset hands back one sample; the DataLoader is the machinery that
turns "one sample" into a batch tensor. Every argument you pass it is one
station in that machine, and knowing the stations tells you which
Dataset to write and what `num_workers` really does.

## Ledger (identical in every episode; agents copy from here)

From `~/repos/deep-learning/code/18_time-series-transformer-from-scratch/`
(`dataloading_1_map_vs_iterable.ipynb`, `tst_data.py`). No beat invents a
number; `_kit/data.js` holds the ones drawn.

- **The data:** synthetic time series, **512 points** each (16 patches of
  32). A `SeriesDataset` of **512 series**, seed 77. One sample is a
  `[512]` tensor; drawn as one row of numbers in brackets. A batch on screen
  is rows of numbers in one pair of brackets with its shape beside it,
  never a stack of squiggles (Chris, ep 1's second cut: "people just see
  a bunch of squiggles"). The readout (`_kit/data.js` `series.readout`):
  `0.3 −1.2 ⋯ / 0.7 0.1 ⋯ / −0.8 0.5 ⋯`, the first values of the first
  three series, one decimal.
- **The loader:** `DataLoader(dataset, batch_size=32, shuffle=True,
  drop_last=True)`. **One batch is `[32, 512]`.** Ep 5 uses
  `batch_size=4, num_workers=2`.
- **The four stations** (ep 2's order, Chris's words): sampler, fetch,
  batching, collate. `shuffle=True` → sampler; `num_workers` → fetch;
  `batch_size` → batching; collate packs them; `drop_last` is the
  batcher's stop.
- **Map-style:** `__len__` + `__getitem__`; `SeriesDataset`, 13 lines:

  ```python
  class SeriesDataset(Dataset):
      def __init__(self, n_series=1000, length=512, seed=77):
          generator = torch.Generator().manual_seed(seed)
          self.series = make_series(n_series, length, generator)

      def __len__(self):
          return len(self.series)

      def __getitem__(self, idx):
          return self.series[idx]
  ```

- **The hand-rolled loop** (`nano_tst.train_model`), ep 3's code beat:

  ```python
  perm = torch.randperm(len(data))                       # the sampler
  for i in range(0, len(data) - batch_size, batch_size): # the batcher (+ drop_last)
      batch = data[perm[i : i + batch_size]]             # __getitem__ + collate
  ```

- **Iterable:** `__iter__` only; `len(stream)` raises `TypeError`:

  ```python
  class SyntheticSeriesStream(IterableDataset):
      def __iter__(self):
          start, step = 0, 1
          info = get_worker_info()
          if self.shard_per_worker and info is not None:
              start, step = info.id, info.num_workers
          index = start
          while True:
              yield series_at(self.seed, index)
              index += step
  ```

- **The worker trap** (ep 5): `DataLoader(SyntheticSeriesStream(seed=77),
  batch_size=4, num_workers=2)`, then `torch.equal(b1, b2)` → **True**.
  With `shard_per_worker=True` → **False**. Worker k takes samples k,
  k+N, k+2N.
- **Splits** (ep 3): `Subset(dataset, indices)`; train 460, val 52.
- **The training loop** (ep 1), diagram 1's pseudo-code:

  ```python
  for epoch in range(num_epochs):
      for batch in loader:
          outputs = model(batch)
          loss = loss_fn(outputs, target)
          loss.backward()
          optimizer.step()
  ```

- **The model:** "a tiny time-series transformer", 807,872 params. Its
  losses over three epochs of 14 steps: 1.68, 1.42, 1.30 (ep 1 only, if a
  loss number is drawn at all).

## The two recurring images

1. **The machine** (`_kit/machine.js`): a left-to-right pipe, redrawn from
   Chris's diagram 2 (`~/Creating/pytorch dataloading/ChatGPT Image …
   08_26_59 AM.png`). Front: the Dataset card (map-style, fed indices by
   a sampler; or iterable, no sampler). Then the DataLoader's dashed box
   with four stations: sampler, fetch (worker cards, N photocopies of the
   Dataset), batching (a stack of N samples), collate (the stack becoming
   one `[32, 512]` tensor). Out: the batch, then the model. Frame 0 of
   eps 2–5 is this machine already running: samples flowing one at a
   time, a batch leaving. Seam states the kit must expose: sampler
   on/off (crossed out for iterable), worker count 0/1/2, which station is
   lit, the batch in flight or landed.
2. **The code card in the band** (`_kit/code.js`, from
   `prototypes/hyperframes/kb-code/`): the editor types the ledger's real
   lines, and as each argument or method lands, its station or card in
   the machine lights. "That line IS this box."

**Never both at once** (Chris, 10/28): the screen shows the machine, or
the code, not the two together. A code beat flips (`S.flip` 0 → 1, a
crossfade of about 0.4 s) from the machine to the code card, which then
fills the stage, types its lines with a typist's uneven rhythm
(`SC_typedAt`, deterministic jitter per character), and flips back when
the VO returns to the machine. The hero passes with the flip: in the
machine it is a part; on the code card it is the line being typed.

The **magenta hero** is whatever the VO names: the batch (ep 1, 2), a
station as it is named (ep 2), `__getitem__` (ep 3), `__iter__` with the
sampler crossed out (ep 4), the twin batches then the fix (ep 5). Teal is
data you can see (samples, the batch tensor's rows).

Engine: `ENGINE: hyperframes` for every episode. Nothing needs axes. Ep 1
draws the training loop (diagram 1's six boxes) with the same card style,
so the batch that leaves ep 1's loader is the batch that leaves ep 2's
machine.

Look: flat house style (Chris did not choose the isometric kit). The kit
was built 2026-10-28 (`_kit/data.js`, `machine.js`, `code.js`, since 2026-10-31 a link to
`videos/_shared/web/code/code.js` mounted `CODE.STAGE`; `window.SC`
with `mount`, `REST`, an empty `SEAM` each episode fills in its own
`_kit/seam.js`). The canonical frame `00_layout/layout.png` shows it in
three states (ep 2's frame 0, ep 5's twins, ep 3's `__getitem__`);
**approval pending** before any episode session starts.

## The episodes

| # | Folder | Search phrase (title starts with it) | Their question | VO line 1 | Hero | Code beat |
|---|---|---|---|---|---|---|
| 1 | `ep01-training-loop` | pytorch training loop explained | What happens in one training step? | A batch is a bunch of samples packed into one tensor; the loop is what happens to that one batch. | the batch riding the loop | the eight-line loop, `for batch in loader:` first |
| 2 | `ep02-dataloader-explained` | pytorch dataloader explained | What does the DataLoader actually do? | The Dataset hands back one sample; the DataLoader calls it n times and hands back a batch. | the batch, then each station as named | `DataLoader(dataset, batch_size=32, shuffle=True, num_workers=2)` (the kit's `code.loader`; `drop_last` is the written companion's) typed on "every argument you pass is one of those stations", each argument lighting a station |
| 3 | `ep03-dataset-class` | pytorch dataset class (also "pytorch custom dataset") | How do I write a custom Dataset? | Two functions: how many samples, and give me sample i. | `__getitem__(idx)` | `SeriesDataset`; then the hand-rolled loop with its three parts named |
| 4 | `ep04-iterable-dataset` | pytorch iterable dataset (not in autocomplete; day-10 read decides) | When do I need an IterableDataset? | If looking up one sample isn't cheap, you use an iterable dataset: one function, iter. | `__iter__`, sampler crossed out | `__iter__`; `len(stream)` → `TypeError` |
| 5 | `ep05-num-workers` | pytorch dataloader num_workers | Why does num_workers give me duplicate batches? | num_workers doesn't split your data; each worker is a full copy of your dataset. | the twin batches, then the fix | `num_workers=2` → `torch.equal` True; `get_worker_info()` shard → False |

Titles (≤ 50 characters where possible; the phrase first):

1. `PyTorch Training Loop Explained (One Batch at a Time)`
2. `PyTorch DataLoader Explained (4 Stations, 4 Arguments)`
3. `PyTorch Dataset Class: Two Functions and You're Done`
4. `PyTorch IterableDataset Explained (When Map Style Won't Work)`
5. `PyTorch DataLoader num_workers: Why You Get Duplicate Batches`

Search phrases checked in YouTube autocomplete 2026-10-25: "pytorch
training loop explained" ✓, "pytorch dataloader explained" ✓, "pytorch
dataset class" ✓ ("pytorch custom dataset" ✓), "pytorch iterable dataset"
✗ (offers "pytorch dataset"), "pytorch dataloader num_workers" ✓. Before
publishing, glance at the results page for each.

Each Short is found alone, so none says "last episode". Ep 1 ends on the
batch arriving, which is ep 2's frame 0. The decision rule "map until you
can't" is said once, in ep 4's closer. Ep 2 as recorded has no closer (see
its `script.md`).

## How it was recorded

One file, `~/Creating/014-pytorch-dataloading.m4a` (323.5 s), 2026-10-28,
"Episode N: title" before each, series order. Exported with a title tag,
so likely Descript; **whether Studio Sound was on is not known: ask
Chris before step 3** (the default chain is loudnorm only either way;
never denoise a Studio Sound take). Split 2026-10-28; cut times are in
`TRANSCRIPT.md` and each `script.md`.

Settled by ear (Chris, 10/28): ep 4's last words are "swap to an
iterable dataset" (both recognizers wrote "interval"; fix the caption at
step 7). Ep 2 ends as recorded, on the batch arriving, with no closer.

## Written companion (lines that did not make a script)

- Map-style is not "fits in memory"; it is cheap random access
  (in-memory tensors, memory-mapped files, parquet row groups). Dropped
  from ep 3's take.
- `drop_last=True` is the range stop condition in the hand-rolled loop.
- The DataLoader never loads your data; your Dataset does (ep 2's unread
  if-time beat).
- Shuffling on a stream: a shuffle buffer, or pre-shuffled shards.
- torchdata.nodes: the next series (`agents/plans/014-pytorch-dataloading-series.md`,
  "Out of scope").

## Checklist

| # | Folder | VO | Storyboard | Beats | Assembled | Shipped |
|---|---|:-:|:-:|:-:|:-:|:-:|
| 1 | `ep01-training-loop/` | x | x | x | x | |
| 2 | `ep02-dataloader-explained/` | x | x | x | x | |
| 3 | `ep03-dataset-class/` | x | x | x | x | |
| 4 | `ep04-iterable-dataset/` | x | | | | |
| 5 | `ep05-num-workers/` | x | x | x | x | |

VO means cut into the folder's `vo_raw.m4a`, with `script.md`. Build
order once the kit is approved: 2, 3, 5, 4, 1 (the series image first,
the on-ramp last). Day-10 read (runbook step 12) per episode into its
`publish.md`.
