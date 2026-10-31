# PyTorch Dataloading: the scripts

Five Shorts, one recording (`agents/series.md` steps 2–3). Chris tightens
in his own words before recording. Every script: line 1 is the answer and
says the search phrase; each thing said once; code on screen, not in the
VO; the closer is the viewer's next move. One beat per script is marked
*(if time)*: the detour the viewer would not miss, since takes run long.
Numbers come from the ledger in `../../agents/archive/014-pytorch-dataloading-series.md`
(the notebook: 512-point series, batch `[32, 512]`, two workers, batch
size four).

Recording: say "Episode N: title", pause 2 s, read, pause 3 s. Flub: pause
and re-read the sentence.

Openers picked by Chris, 2026-10-25: ep 1 the batch line; ep 2 the two
jobs then the four stations; ep 3 the two functions; ep 4 the "not cheap"
line then "what I use for bigger models"; ep 5 the worker copy, said
generally.

---

## Episode 1: PyTorch Training Loop Explained (One Batch at a Time) (125 words + 29 if time)

Search phrase: pytorch training loop explained. Frame 0: diagram 1, the
batch already riding the loop. Hero: the batch. Code beat: the eight-line
loop, `for batch in loader:` first.

A batch is just a bunch of samples packed into one tensor so the GPU can parallelize, and a PyTorch training loop is what happens to that one batch.

The data loader yields it.

The batch goes into the forward pass, and the model makes a prediction.

We compare that prediction to the target. That's the loss.

The loss is propagated backwards, and the weights are updated as part of gradient descent.

That is one training step.

Then we go back to the data loader for the next batch.

*(if time)* An epoch is one pass through the whole dataset, so this inner loop runs once per epoch, and the outer loop runs for as many epochs as you set.

The model never sees your dataset. It only ever sees one batch at a time.

So if your loss isn't moving, check the batch first. Everything downstream of it is the same four lines every time.

---

## Episode 2: PyTorch DataLoader Explained (4 Stations, 4 Arguments) (151 words + 16 if time)

Search phrase: pytorch dataloader explained. Frame 0: the machine, samples
flowing in one at a time, a batch leaving. Hero: the batch tensor, then
each station as it is named. Code beat: `DataLoader(dataset,
batch_size=32, shuffle=True, drop_last=True, num_workers=2)` typed in the
band, each argument lighting its station.

In PyTorch the Dataset's job is to hand back one sample, and the DataLoader's job is to call it 32 times and hand back a batch.

The DataLoader is a machine with four stations, and every argument you pass it is one of those stations.

Your dataset sits at the front. All it knows is how to go get one sample, wherever that data lives.

First station, the sampler. It decides the order. shuffle equals true is a random sampler: a random sequence of indices.

Second, fetch. Workers call your dataset with those indices, in parallel if you ask for them.

Third, batching. It collects batch-size samples.

Fourth, collate. It packs them into one tensor shaped for the GPU.

Out comes the batch, and that's what goes into the forward pass.

*(if time)* So the DataLoader never loads your data. Your dataset does. Everything else is machinery around it.

When you set a DataLoader argument, you're turning a knob on one station. Find the station first, then the argument.

---

## Episode 3: PyTorch Dataset Class: Two Functions and You're Done (141 words + 20 if time)

Search phrase: pytorch dataset class (also "pytorch custom dataset").
Frame 0: `SeriesDataset`, 13 lines, `__len__` and `__getitem__` lit.
Hero: `__getitem__(idx)`. Code beat: the hand-rolled loop with its three
parts named in turn (randperm, the range step, the slice).

A PyTorch Dataset class is two functions: how many samples, and give me sample i. Everything else is the DataLoader's job.

Len returns the number of samples. Get item returns sample number i.

In this one the series are precomputed into one tensor, so get item is just a slice.

Because the dataset is indexable, the sampler owns the order. It uses the length to make a random sequence of indices, and calls get item on each one.

So shuffling is free. And a validation split is just a list of indices.

If you've ever shuffled with torch dot randperm and sliced batches by hand, you already wrote this. Randperm is the sampler. The range step is the batcher. The slice is get item plus collate.

*(if time)* Map-style isn't about fitting in memory. It's about cheap random access: in-memory tensors, memory-mapped files, parquet row groups all qualify.

Write these two functions first. The loader, the shuffle and the split come for free.

---

## Episode 4: PyTorch IterableDataset Explained (When Map Style Won't Work) (150 words + 19 if time)

Search phrase: pytorch iterable dataset (not in autocomplete; judged at day
10). Frame 0: the machine with the sampler crossed out, the Dataset card
showing `__iter__` only. Hero: `__iter__`. Code beat:
`SyntheticSeriesStream.__iter__`, and `len(stream)` raising `TypeError`.

If looking up one sample isn't cheap, you use an IterableDataset: one function, iter, that just yields samples.

It's what I use most when training bigger models. You pack the data into shards and stream them through.

There's no length and no get item. Sample i doesn't exist until the iterator produces it.

Which means there's no sampler. The loader just calls your dataset over and over, and it yields the next sample.

So shuffling is your problem now. You pre-shuffle the data into shards, load one shard into memory, and yield from it.

*(if time)* Splits are your problem too. And if you run multiple workers, splitting the stream between them is your problem.

The DataLoader on top is the same: same batch size, same collate, same batch out. The only thing that changed is the loader asks for next, not for number i.

So map until you can't. The day sample i stops being cheap, swap the two functions for one, and take the order into your own hands.

---

## Episode 5: PyTorch DataLoader num_workers: Why You Get Duplicate Batches (151 words + 14 if time)

Search phrase: pytorch dataloader num_workers. Frame 0: two worker cards,
photocopies of the Dataset, and two identical batches with `torch.equal
→ True` under them. Hero: the twin batches, then the fix. Code beat:
`DataLoader(stream, batch_size=4, num_workers=2)` → True; `get_worker_info()`
sharding in `__iter__` → False.

num_workers doesn't split your data across workers. Each worker is a full copy of your dataset, fetching and collating on its own.

So when you run an iterable dataset with multiple workers, every worker gets that same dataset object, and unless you split the stream yourself, they all deliver the same data.

With a map-style dataset you're fine. The sampler stays in the main process and hands each worker a different set of indices. Every sample gets fetched once.

With an iterable dataset there are no indices. Each worker starts the stream from the beginning. Same seed, same data.

Two workers, batch size four: the first two batches are identical.

The fix lives inside your iter function. Ask for the worker info, and have worker k take every Nth sample, starting at k.

*(if time)* Now the two copies walk the stream in step, and nothing is delivered twice.

So before you raise num_workers on a stream, open iter and check it knows which worker it is.
