# Publish: FLOPs explained (Understanding the GPU, part 2 of 8)

Search phrase: **flops explained** (SERIES.md "Search phrases": offered by
autocomplete; the results are AI explainers, the suggestions mostly
flip-flops, so the title keeps "FLOPs" in its own case and the description
says AI and GPU in line 1). Before publishing, glance at YouTube's results
for it.

Final cut: `media/short.mp4`, 40.2 s.

## Titles

Search title, for the person typing the phrase (40 characters, the phrase
first, the answer after it):

```
FLOPs Explained: One Multiply or One Add
```

Hook title, for the person scrolling past (the stake first, the phrase
kept for search; 45 characters, the phrase starts at 30). v4: was "You pay
for AI in these", dropped with the bill line it paid off; this one is the
hook's own claim ("the unit all AI compute is measured in"):

```
All AI is measured in these (FLOPs explained)
```

## Description

```
FLOPs explained: a FLOP is one multiply or one add, the unit all AI and GPU compute is measured in.

FLOP stands for floating-point operation: a number stored like scientific notation in binary: a sign, digits, an exponent.
FLOPs with a small s is a count: training an 8B-parameter model on 15,000 tokens is about 720 trillion FLOPs. FLOPS with a capital S is a rate: FLOPs per second.
A matmul is only multiplies and adds, and a GPU does thousands at once.

Part 2 of 8 on understanding the GPU. Next: why training costs 6 FLOPs per parameter per token.
[POST LINK]

Level up human.

#gpu #deeplearning #machinelearning #nvidia #Shorts
```

## Substack note

```
"FLOPs" and "FLOPS" are two different things. Small s is a count (what your training run takes); capital S is a rate (what the chip does per second). One FLOP is one multiply or one add, and a transformer's compute is nearly nothing else. 40 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (40.17 s, v4) 2026-10-31. On
screen: inside one core, `1.5 × 2.0 = 3.0`, the 3.0 carried into `3.0 +
0.5 = 3.5`, the counter 0 → 1 FLOP → 2 FLOPs, then out to the chip (beat
1); `FLOP` unpacking into FLOATING-POINT / OPERATION (2); the panel zoomed
into one number, `0.0000001 → +1.0 × 10⁻⁷`, sign / digits / exponent (3);
memory lit, numbers
streaming along the pipe, `weights` / `activations` / `gradients` (5);
`FLOPs`, the code line `flops = 6 * 8e9 * 15_000  # 7.2e14` typing while
the count rolls up to `720 trillion = 7.2 × 10¹⁴` (6); `FLOPS` / `per
second` and a 1 s clock (7); `y = x @ W`, then inside one core `y += x × w`
three times, y = 4.5, 6 FLOPs, then every core lit, held to the end (8). No bill card. Numbers: 720 trillion = 6 × 8e9 × 15,000 (ledger);
`1.5 × 2.0 + 0.5` and the dot product's x, w are illustration values Chris
approved. No GPU model or peak is shown or said.
