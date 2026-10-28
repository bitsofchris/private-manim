# Episode 4: PyTorch IterableDataset Explained (When Map Style Won't Work)

- **Duration:** 52.7 s raw (`vo_raw.m4a`).
- **Source:** cut from `~/Creating/014-pytorch-dataloading.m4a` at 193.30–246.00 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, Episode 4.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").

## As recorded

If looking up one sample isn't cheap, you use an iterable dataset. Here we use one function, iter, that just yields samples.

I most frequently use this when training bigger models. You pack the data into shards and just stream them through.

There's no length, no get item. Sample i doesn't exist until the iterator produces it.

This means there's no sampler. The loader just calls your dataset over and over and it yields the next sample.

So shuffling is now your problem. You pre-shuffle the data into shards, load one shard into memory and yield from it.

Splits are also your problem too. If you run multiple workers, splitting the stream between them is up to you to determine.

The data loader on top is the same though. Same batch size, same collate, same batch out. The only thing that changes: the data loader is asking for the next sample, not for the sample at index i.

So use map until you can't, and the day sample i stops being cheap, swap to an iterable dataset.

## Where the take leaves the script

- Line 1 split in two: "…you use an iterable dataset. Here we use one function, iter, that just yields samples." Keep.
- The *(if time)* beat (splits, workers) was read, with "is up to you to determine" (script: "is your problem"). Candidate cut if the episode needs seconds; it does not (52.7 s raw).
- "Same batch size": Parakeet heard "batch I" on both passes; Chris's own transcript has "batch size". Caption spelling fix at step 7.
- The last words: both recognizers heard "swap to an **interval** dataset"; Chris confirmed by ear (10/28) that he said **iterable**. Caption spelling fix at step 7 (`fix_words.py --sub interval iterable`).
