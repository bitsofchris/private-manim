# Publish: FLOPs explained (Understanding the GPU, part 2 of 8)

Search phrase: **flops explained** (SERIES.md "Search phrases": offered by
autocomplete; the results are AI explainers, the suggestions mostly
flip-flops, so the title keeps "FLOPs" in its own case and the description
says AI and GPU in line 1). Before publishing, glance at YouTube's results
for it.

Final cut: `media/short.mp4`, 58.4 s.

## Titles

Search title, for the person typing the phrase (40 characters, the phrase
first, the answer after it):

```
FLOPs Explained: One Multiply or One Add
```

Hook title, for the person scrolling past (the stake first, the phrase
kept for search; 41 characters, the phrase starts at 26):

```
You pay for AI in these (FLOPs explained)
```

## Description

```
FLOPs explained: a FLOP is one multiply or one add, the unit all AI and GPU compute is measured in.

FLOP stands for floating-point operation: a number stored like scientific notation (a sign, digits, an exponent), so one format holds a ten-millionth and three million.
FLOPs with a small s is a count: training an 8B-parameter model on 15,000 tokens is about 720 trillion FLOPs. FLOPS with a capital S is a rate: a B200 peaks near 2,250 teraFLOPS in bf16.
A matmul is only multiplies and adds, and a GPU does thousands at once. Divide the FLOPs by the FLOPS you get and you have GPU-hours: the bill.

Part 2 of 8 on understanding the GPU. Next: why training costs 6 FLOPs per parameter per token.
[POST LINK]

Level up human.

#gpu #deeplearning #machinelearning #nvidia #Shorts
```

## Substack note

```
"FLOPs" and "FLOPS" are two different things, and mixing them up is how GPU-hour estimates go wrong. Small s is a count (what your training run costs); capital S is a rate (what the chip does per second). Divide one by the other and you have the bill. 58 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (58.37 s) 2026-10-29. On
screen: `a × b + c` with a FLOPs counter ticking 1, 2 on "multiply" and
"add" (beat 1); `floating-point` / `operation` with fl and op lit (2); the
panel zoomed out of one core, `0.0000001 → +1.0 × 10⁻⁷` and the sign /
digits / exponent boxes (3); the point gliding, then `3000000 → +3.0 × 10⁶`
(4); memory lit under `weights` / `activations` / `gradients` (5);
`FLOPs`, the code line `flops = 6 * 8e9 * 15_000  # 7.2e14` and `720
trillion` (6); `FLOPS` / `per second`, the chip renamed B200, `2,250
TFLOPS` / `bf16`, `tera = a trillion` (7); `y = x @ W`, `x1*w1 + x2*w2 +
x3*w3`, every core lit (8); `FLOPs ÷ FLOPS = GPU-hours = $` (9). Numbers
match the ledger: 720 trillion = 6 × 8e9 × 15,000; 2,250 TFLOPS is the
B200's bf16 dense peak. The card shows no GPU-hours figure.
