# Publish: PyTorch Dataset class (PyTorch Dataloading, part 3 of 5)

Search phrase: **pytorch dataset class** (also "pytorch custom dataset";
both autocomplete, checked 2026-10-25). Before publishing, glance at
YouTube's results for it.

Final cut: `media/short.mp4`, 50.5 s.

## Titles

Search title (SERIES.md's, recommended; the phrase first, 52 characters,
two over the ~50 the feed shows, the cut falls in "You're Done"):

```
PyTorch Dataset Class: Two Functions and You're Done
```

Hook title, for the person scrolling past (the stake from the VO's "you
already wrote this", the phrase kept for search; 46 characters):

```
You Already Wrote This (PyTorch Dataset Class)
```

## Description

```
PyTorch dataset class: two functions, __len__ and __getitem__, and the DataLoader does the rest.

__len__ says how many samples; __getitem__ hands back sample i. Because the dataset is indexable, the sampler owns the order, so shuffling is free and a validation split is just a list of indices.
If you've shuffled with torch.randperm and sliced batches by hand, you already wrote this: randperm is the sampler, the range step is the batcher, the slice is __getitem__ plus collate.
This is a map-style dataset: use it when random access is cheap.

Part 3 of 5 on PyTorch dataloading. Next: when you need an IterableDataset.
[POST LINK]

Level up human.

#pytorch #deeplearning #machinelearning #dataset #Shorts
```

## Substack note

```
If you've copied class MyDataset(Dataset) from a tutorial and aren't sure which parts matter: it's two functions. __len__ says how many samples, __getitem__ hands back sample i, and the DataLoader's sampler, batcher and collate do everything else. If you've ever sliced batches by hand with randperm, you already wrote one. 50 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (50.50 s) 2026-10-29,
first cut, approved by Chris. On screen: the Dataset card
(`class Series(Dataset)`, `__len__`, `__getitem__`, `return
self.series[i]`) typing its last line at frame 0, the two methods lit on
"two functions", then each in turn (beat 1, and again in beats 4, 9, 10);
the machine with samples hopping as bracketed rows into the DataLoader
and its four stations swept on "the data loader's job" (beat 2);
`__len__` / `__getitem__` lit on the Dataset card (beat 3); the sampler
(`7 2 5 0 3 1`), length, getitem lit as the VO names them, the index
list pulsing on "a list of indices" (beats 5–6); the hand-rolled loop
typed (`perm = torch.randperm(n)` … `batch = data[idx]`, beat 7); the
sampler, batching, getitem and collate lit in turn (beat 8); the last
frame is the Dataset card with both methods lit. The description's
"validation split" is the VO's; no `Subset` code is drawn. No number is
claimed beyond the ledger's.
