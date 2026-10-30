# Publish: PyTorch DataLoader num_workers (PyTorch Dataloading, part 5 of 5)

Search phrase: **pytorch dataloader num_workers** (autocompletes, checked
2026-10-25). Before publishing, glance at YouTube's results for it.

Final cut: `media/short.mp4`, 57.7 s.

## Titles

Search title (SERIES.md's, recommended; the phrase first, 61 characters,
eleven over the ~50 the feed shows, the cut falls in "Duplicate"):

```
PyTorch DataLoader num_workers: Why You Get Duplicate Batches
```

Hook title, for the person scrolling past (the stake is their bug, the
phrase kept for search; 50 characters):

```
Same Batch Twice? (PyTorch DataLoader num_workers)
```

## Description

```
PyTorch DataLoader num_workers doesn't split your data: each worker is a full copy of your dataset.

With a map-style dataset that's fine: the sampler stays in the main process and hands each worker different indices.
With an IterableDataset there are no indices, so two workers with batch_size=4 deliver identical first batches: torch.equal(b1, b2) is True.
The fix lives in __iter__: get_worker_info() and have worker k take every nth sample starting at k. Now torch.equal is False.

Part 5 of 5 on PyTorch dataloading.
[POST LINK]

Level up human.

#pytorch #deeplearning #machinelearning #dataloader #Shorts
```

## Substack note

```
If you raised num_workers on a streaming dataset and got the same batch twice: num_workers doesn't split your data. Each worker is a full copy of your dataset, and an IterableDataset has no sampler to hand out indices, so every copy starts the stream from the beginning. Ask get_worker_info() inside __iter__ and have worker k take every nth sample. 58 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (57.73 s) 2026-10-29,
first cut, approved by Chris. On screen: the trap at frame 0 (iterable,
sampler struck, two worker photocopies, twin `[4, 512]` batches lit as a
pair), fetch then collate lit (beats 1–2); the iterable class card
typed (beat 3); map-style with the sampler back, one batch, the
photocopies pulsing in turn (beat 4); the strike drawn back across the
sampler and the twins returning (beat 5); the workers card
(`batch_size=4,` / `num_workers=2)` / `torch.equal(b1, b2)  # True`,
beat 6); `__iter__` lit (beat 7); the shard card (`info =
get_worker_info()`, `start = info.id  # k`, `step = info.num_workers`,
then `torch.equal(b1, b2)  # False`, beats 8–9); the last frame is the
shard card with `get_worker_info()` lit. No number is claimed beyond the
ledger's.
