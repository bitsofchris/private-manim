# Publish: why GPUs for AI (Understanding the GPU, part 1 of 8)

Search phrase: **why gpu for ai** (storyboard preflight: autocompletes
verbatim, results on topic, checked 2026-10-27; "gpu vs cpu explained"
also autocompletes, general hardware results). The take's line 1 says
"neural network" and "GPUs", not "AI", so the phrase is carried by the
title and description line 1. Before publishing, glance at YouTube's
results for it.

Final cut: `media/short.mp4`, 44.0 s.

## Titles

Search title, for the person typing the phrase (43 characters, the phrase
first, the answer after it):

```
Why GPUs for AI: Thousands of Cores at Once
```

Hook title, for the person scrolling past (the stake first, a claim about
them; the phrase kept for search; 39 characters, the phrase starts at 25):

```
Your CPU can't keep up (why GPU for AI)
```

## Description

```
Why GPU for AI: a neural network is mostly multiply-adds, and a GPU does thousands of them at once.

One layer is y = x @ W: each output is its own row times column, and none of them waits on another.
A CPU is a few big cores built to run one thread fast; it works through that pile a few at a time.
A GPU trades per-core speed for count: thousands of small cores, all working at once. In PyTorch it's one line: move x and W to cuda.

Part 1 of 8 on understanding the GPU. Next: FLOPs explained.
[POST LINK]

Level up human.

#gpu #deeplearning #machinelearning #nvidia #Shorts
```

## Substack note

```
Why does AI run on GPUs and not CPUs? A neural network is mostly multiply-adds whose outputs don't depend on each other. A CPU is a few big cores built to run one thread fast; a GPU is thousands of small ones built to do the whole pile at once. Same y = x @ W, moved to cuda. 44 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (44.04 s, round 3)
2026-10-31. On screen: a tiny 4-4-4-2 network firing, `y = x @ W` stacked
under it, the chip smaller below, shimmering, then the whole grid lit and
every y cell filled at once (beat 1); the network's first layer lit as
`y = x @ W`, one row of x, one column of W, their y cell and the output
node with its 4 incoming edges, then every y cell at once (2); the CPU
growing into the chip's place, 4 big cores with cache blocks and branch
forks, filling y one row of four per tick (3); the chip back, every core
lit at once (4); tensor-core sub-blocks, "tensor cores" (5); the code card
`x, W = x.to("cuda"), W.to("cuda")` / `y = x @ W`, the grid's wave (6).
No core counts, FLOP counts or timings are shown or said; the description
claims nothing beyond the VO and these frames. The memory slab (`GPU
memory (VRAM) 180 GB`, the series ledger) is on screen at rest, never said.
