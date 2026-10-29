# Publish: PyTorch training loop explained (PyTorch Dataloading, part 1 of 5)

Search phrase: **pytorch training loop explained** (SERIES.md "Search
phrases"; autocompletes, checked 2026-10-25). Before publishing, glance at
YouTube's results for it.

Final cut: `media/short.mp4`, 43.0 s.

## Titles (two; Chris picks)

Search title, for the person typing the phrase (49 characters, phrase first):

```
PyTorch Training Loop Explained (4 Lines, 1 Batch)
```

Hook title, for the person scrolling past (the stake first, the phrase
kept for search; 57 characters, the phrase starts at 25):

```
Your loss isn't moving? (pytorch training loop explained)
```

SERIES.md's working name, `PyTorch Training Loop Explained (One Batch at
a Time)`, is 53 characters, over the 50 limit; the search title above
keeps its claim in fewer.

## Description

```
PyTorch training loop explained: the loop is just what happens to one batch, four lines at a time.

A batch is a bunch of samples packed into one tensor. The DataLoader yields it, the model makes a prediction, you compare it to the target for a loss, the loss goes backwards and the weights update. That is one training step; then the next batch.
An epoch is one pass through the whole dataset: the inner loop runs once per epoch, the outer loop as many times as you set.
The model never sees your dataset, only one batch at a time. So if your loss isn't moving, check the batch first.

Part 1 of 5 on PyTorch dataloading. Next: what the DataLoader actually does.
[POST LINK]

Level up human.

#pytorch #deeplearning #machinelearning #trainingloop #Shorts
```

## Substack note

```
If you've typed a PyTorch training loop from a tutorial and can't say what each line does to the batch: the loop is four things that happen to one batch, every time. The DataLoader yields it, forward, loss, backward, update, then the next one. 45 seconds.
```

## Checked against the final cut

Reviewed on a 44-tile sheet of `media/short.mp4` (44.77 s) 2026-10-28.
On screen: the DataLoader card with the batch glyph riding the loop past
forward, loss, backward, update and back (beats 1–5, each box lit as the
VO names it, all four on "one training step"); the six-line loop typed on
the code card with `for batch in loader:` lit on "inner loop" and
`for epoch in range(epochs):` on "outer loop" (beat 6); the machine at
rest with the `[32, 512]` batch card and the model chip (beats 7–8). The
description's "four lines" is the VO's phrase; the card shows six lines,
two loop headers and the four. No numbers are claimed beyond `[32, 512]`.
