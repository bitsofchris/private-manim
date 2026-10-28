# Episode 2: PyTorch DataLoader Explained (4 Stations, 4 Arguments)

- **Duration:** 52.1 s raw (`vo_raw.m4a`).
- **Source:** cut from `~/Creating/014-pytorch-dataloading.m4a` at 63.90–116.00 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, Episode 2.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").

## As recorded

In PyTorch, the dataset's job is to hand back one sample, and the data loader's job is to call it n number of times and hand back a batch.

The data loader is a machine with four different stations, and every argument you pass is one of those stations.

Your dataset sits at the front. All it knows is how to go get one sample, wherever that data lives.

The first station is the sampler. It decides the order. Shuffle equals true is a random sampler, ~~a random sequences of indies~~, a random sequence of indices.

Second up is fetch. Workers will call your dataset with those indices in parallel if you ask for them.

Third is batching. It collects batch-sized samples.

And fourth is collate. This is what packs them into one tensor shaped for the GPU.

Out comes the batch and what goes into the forward pass.

## Where the take leaves the script

- "call it **n number of times**" (script: 32 times). The number is on the code card anyway.
- Flub at take 93.4–94.6 s ("a random sequences of indies"), re-read at once: cut the first reading.
- The *(if time)* beat ("the DataLoader never loads your data") was not read.
- **No closer was read**, and Chris decided (10/28) the episode ends as recorded: on "Out comes the batch and what goes into the forward pass", with the batch arriving at the model as the final still. The next word in the master take is "so episode three", so the cut must end on the pause after "pass".
- "and what goes into the forward pass" (script: "and that's what goes into"); keep as said.
