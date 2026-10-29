# Publish: 6 FLOPs per parameter (Understanding the GPU, part 3 of 8)

Search phrase: **flops llm** (storyboard preflight: offered by
autocomplete 10/27; second choice "scaling laws llm"). Both titles carry
"FLOPs" and "LLM"; the description's line 1 has both in its first
clause. Before publishing, glance at YouTube's results for it.

Final cut: `media/short.mp4`, 45.4 s.

## Titles

Search title, for the person typing the phrase (40 characters, the
phrase first, the answer after it):

```
LLM FLOPs: Why Training Costs 6 × Params
```

Hook title, for the person scrolling past (the stake first, the phrase
kept for search; 43 characters, the phrase starts at 34):

```
Every training bill starts here (LLM FLOPs)
```

## Description

```
LLM FLOPs: training costs about 6 FLOPs per parameter per token, 2 forward and 4 backward.

A tiny layer (3 inputs, 2 outputs, 6 weights) shows where the 6 comes from: forward, each weight does one multiply and one add (12 FLOPs); backward, the same weights pass the error to the layer before (24) and build their own gradient (36 = 6 × 6).
So training compute is 6 × parameters × tokens: an 8B model at 15,000 tokens per second per GPU is doing 720 TFLOPS.

Part 3 of 8 on understanding the GPU. Next: what bf16, fp16 and fp8 mean for the spec sheet.
[POST LINK]

Level up human.

#gpu #llm #deeplearning #machinelearning #Shorts
```

## Substack note

```
"6 × params × tokens" is in every scaling-law paper and MFU formula, but where does the 6 come from? Each weight does a multiply and an add going forward (2), then twice that coming back: once to pass the error on, once to build its own gradient (4). That's the whole rule. 45 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (45.40 s) 2026-10-29. On
screen: `6 × params` over the full FLOP bar labelled `→ 2` / `← 4`, the
layer `x1 x2 x3` → `y1 y2` with pulses running (beat 1); the matrix `W`
and `y = W x`, the six lines flashing (2); `0 FLOPs` → `12 FLOPs` with ×
and + riding each line (3); `dx` / `dy`, `dx = Wᵀ dy`, 12 → `24 FLOPs`
(4); `dW = dy xᵀ`, the dW cells filling, 24 → `36 FLOPs` (5); `36 = 6 ×
6` (6); the layer shrinking into one core of the chip and the card
`flops = 6 * n_params * n_tokens` (7); `6 * 8e9 * 15_000  # 7.2e14 /s`
and `720 TFLOPS` under the chip (8). Numbers match the ledger: 720 TFLOPS
= 6 × 8e9 × 15,000 per second.
