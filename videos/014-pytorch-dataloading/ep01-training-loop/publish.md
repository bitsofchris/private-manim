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

Reviewed on a 30-tile sheet of `media/short.mp4` (43.07 s) 2026-10-28,
second cut. On screen: the machine with samples hopping and the
`[32, 512]` batch card (beats 1, 9, 10); the DataLoader card and the
glyph riding past forward, loss, backward, update and back (beats 2, 3,
5, 7); the four body lines typed with `loss = loss_fn(out, y)` lit (beat
4), lit together on "one training step" (beat 6), the two `for` headers
typed above them with inner then outer lit (beat 8), and the six lines
with the four lit on "same four lines every time" (beat 11, the last
frame). The description's "four lines" is the VO's phrase; the card
shows those four under the two loop headers. No number is claimed
beyond `[32, 512]`.
