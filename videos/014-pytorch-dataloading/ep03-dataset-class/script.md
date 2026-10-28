# Episode 3: PyTorch Dataset Class: Two Functions and You're Done

- **Duration:** 63.6 s raw (`vo_raw.m4a`); over 60, tightening expected to land it (3.6 s of pauses over 1.2 s inside).
- **Source:** cut from `~/Creating/014-pytorch-dataloading.m4a` at 122.80–186.40 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, Episode 3.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").

## As recorded

A PyTorch dataset class is two functions. How many samples? And how do I get sample i? Everything else is the data loader's job.

Len returns the number of samples. Get item returns sample at index i.

~~In this~~ Here the series are pre-computed into one tensor, so get item is just a slice.

Because you can index into the dataset, the sampler owns the order. It uses the length to make a random sequence of indices and calls get item on each one.

So shuffling is free, and a validation split is just a list of indices.

If you've ever shuffled with torch.randperm and sliced batches by hand, you already wrote this. Randperm is the sampler. The range step is the batcher, and the slice is get item plus collate.

This is called a map style dataset. You use it when random access is cheap.

If you write these two functions first, the loader, the shuffle, and the split will come for free.

## Where the take leaves the script

- Line 1 gained "and how do I get sample i?" (script: "give me sample i"). Keep.
- Flub at take 138.7–140.1 s: "In this", a 4.2 s pause, then the re-read "Here the series are pre-computed…". Cut "In this" and the pause (the biggest single saving).
- The *(if time)* beat (map-style is cheap random access, not fitting in memory) was replaced by two new sentences: "This is called a map style dataset. You use it when random access is cheap." (take 173.3–177.7 s). Keep: it names the term the ep 4 title relies on.
- A 4.9 s pause before the closer (take 177.2–182.2 s); the tightener caps it.
- Closer as scripted, with "will come for free".
