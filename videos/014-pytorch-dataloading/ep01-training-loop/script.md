# Episode 1: PyTorch Training Loop Explained (One Batch at a Time)

- **Duration:** 51.3 s raw (`vo_raw.m4a`).
- **Source:** cut from `~/Creating/014-pytorch-dataloading.m4a` at 5.70–57.00 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, Episode 1. The planned script is reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").

## As recorded

A batch is just a bunch of samples packed into one tensor so the GPU can parallelize. And a PyTorch training loop is what happens to that one batch.

The data loader yields it, the batch goes into the forward pass, and the model makes a prediction.

We compare that prediction to the target and that's the loss.

The loss is then propagated backwards and the weights are updated as part of gradient descent. That is one training step.

Then we go back to the data loader for the next batch.

An epoch is one pass through the whole dataset. So this inner loop runs once per epoch and the outer loop runs for as many epochs as you set.

The model never sees your dataset, it only ever sees one batch at a time.

So if your loss isn't moving, check the batch first. Everything downstream of it is the same four lines every time.

## Where the take leaves the script

- As scripted, including the *(if time)* epoch beat (37.0–46.0 s of the take; 31.3–40.2 s here). Candidate cut if over 60 s after tightening (it is not: 51.3 s raw).
- A 2.4 s pause after "makes a prediction" (take 20.2–22.6 s); the tightener caps it.
