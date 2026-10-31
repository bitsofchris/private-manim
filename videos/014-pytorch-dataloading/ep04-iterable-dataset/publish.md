# Publish: PyTorch IterableDataset (PyTorch Dataloading, part 4 of 5)

Search phrase: **pytorch iterable dataset** (not in YouTube autocomplete,
checked 2026-10-25: it offers "pytorch dataset"; ships under it anyway,
the day-10 read decides). Before publishing, glance at YouTube's results
for it.

Final cut: `media/short.mp4`, 47.2 s.

Chosen: **the search title** (Chris, 2026-10-31).

## Titles

Search title (SERIES.md's, recommended). 61 characters, so the feed cuts
it inside the parenthesis; the phrase is in the first 31. It spells
`IterableDataset` as the class is written, while the searched phrase is
"iterable dataset", two words:

```
PyTorch IterableDataset Explained (When Map Style Won't Work)
```

Hook title, for the person scrolling past (the stake from the VO's "if
looking up one sample isn't cheap" and "training bigger models", the
phrase in its searched spelling; 54 characters):

```
When Your Data Gets Too Big (PyTorch Iterable Dataset)
```

## Description

```
PyTorch iterable dataset: when looking up one sample isn't cheap, write one function, __iter__.

An iterable dataset has no length and no __getitem__: sample i doesn't exist until the iterator yields it, so there's no sampler. The DataLoader just asks for the next sample, over and over.
You pack the data into shards and stream them through. Shuffling becomes yours (pre-shuffle the shards, load one into memory, yield from it), and so does splitting the stream across workers.
The DataLoader on top stays the same: same batch size, same collate, same batch out. Use map-style until you can't.

Part 4 of 5 on PyTorch dataloading. Next: why num_workers gives you duplicate batches.
[POST LINK]

Level up human.

#pytorch #deeplearning #machinelearning #dataloader #Shorts
```

## Substack note

```
If you've seen IterableDataset in the PyTorch docs and can't say when you'd need it: when looking up one sample isn't cheap. You write one function, __iter__, that yields samples; there's no length and no sampler, so shuffling and splitting across workers become your job, and the DataLoader on top doesn't change. Map-style until you can't. 47 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (47.24 s) 2026-10-31,
cut 3, approved by Chris. On screen: frame 0 is the machine in iterable
mode, `__iter__` the hero, the sampler struck through, samples hopping
(beat 1); the code card types `class Stream(IterableDataset):` …
`yield next_series()` (beat 2); the stream: three shards at the top, one
pipe through `__iter__`, samples one at a time into the DataLoader (beat
3); `len(stream)  # TypeError` typed under the class (beat 4); a struck
`sampler` tag, then `next()` from the loader up to `__iter__` (beat 5);
the shards reordered, one dropped into a memory box and its rows read out
mixed (beat 6); the pipe forked to two workers' `__iter__`, samples
dealt round robin, a "?" between them (beat 7); back on the machine,
batching, collate and the `[32, 512]` batch lit in turn (beat 8);
`def __iter__(self):` over `def __getitem__(self, i):` (beat 9); the map
machine (`__len__`, `__getitem__`, sampler on) swapped to iterable on
"swap", the last frame frame 0 (beat 10). "Pre-shuffle", "memory" and
"workers" are the VO's; no `get_worker_info()` code is drawn (ep 5's).
No number is claimed beyond the ledger's.
