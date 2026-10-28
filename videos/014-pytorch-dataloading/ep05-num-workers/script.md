# Episode 5: PyTorch DataLoader num_workers: Why You Get Duplicate Batches

- **Duration:** 67.5 s raw (`vo_raw.m4a`); over 60, see the cut candidates below.
- **Source:** cut from `~/Creating/014-pytorch-dataloading.m4a` at 255.00–322.50 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, Episode 5.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").

## As recorded

In PyTorch, num_workers doesn't split your data across the workers. Each worker is a full copy of your dataset, fetching and collating on its own.

So when you run an iterable dataset with multiple workers, every worker gets the same dataset object. And unless you split the stream yourself, they all deliver the same data.

With a map style dataset, you're fine. The sampler stays in the main process and hands each worker a different set of indices. Every sample here gets fetched once.

But with an iterable dataset, there are no indices. Each worker starts the stream from the beginning. So if you have the same seed, you're getting the same data.

Two workers, batch size four, the first two batches will be identical.

The fix lives inside your iter function. Ask for the worker info and have worker k take every nth sample starting at k, or spread the shards out among workers based on the worker's identity.

Now the two copies can walk the stream in step and nothing is delivered twice.

So before you increase num_workers on an iterable dataset, be sure you're passing that worker info to each iter function so you can split the stream accordingly.

## Where the take leaves the script

- Line 1 gained "In PyTorch," and "across the workers". Keep.
- Added, not in the script: "or spread the shards out among workers based on the worker's identity" (take 303.8–308.9 s, 5.1 s). First cut candidate: the previous clause already gives the fix.
- The *(if time)* beat ("Now the two copies can walk the stream in step…") was read (take 308.9–313.1 s, 4.2 s). Second cut candidate.
- The closer is longer than scripted (8.8 s: "…be sure you're passing that worker info to each iter function so you can split the stream accordingly"). Keep: it is the viewer's next move.
- With the two candidates cut and pauses capped, the episode lands near 55 s.
