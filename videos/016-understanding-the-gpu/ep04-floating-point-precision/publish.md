# Publish: floating point precision (Understanding the GPU, part 4 of 8)

Search phrase: **bf16 vs fp16** (storyboard preflight: autocompletes
verbatim, checked 2026-10-27; "fp32 vs fp16" second; "mixed precision
training" for the description). The take says bf16, fp16 and fp32 in its
first 18 s. Before publishing, glance at YouTube's results for it.

Final cut: `media/short.mp4`, 44.7 s.

## Titles

Rewritten 2026-10-31 at Chris's ask for a more generic frame: the Short
compares the number types AI models train in, not a PyTorch or Python
detail. YouTube autocomplete (checked 2026-10-31): "bf16 vs fp16", "fp16
vs fp32", "fp16 vs fp8" and "mixed precision training" (+ "pytorch") all
complete; "pytorch data types" / "pytorch dtype" don't; "data types in
deep learning" does, but its results are about data (images, text), not
number formats, so it isn't used.

**Recommended: the hook title.** The day-10 read records which was used
and its search %.

Hook title, for the person scrolling past (the general stake, AI models;
42 characters, the phrase starts at 29):

```
Why AI models train in bf16 (bf16 vs fp16)
```

Search title, for the person typing a phrase (38 characters; the broader
"mixed precision training" first, the comparison after it):

```
Mixed Precision Training: bf16 vs fp16
```

Previous pair (2026-10-31, before the rewrite): `Your fp16 training can
overflow (bf16 vs fp16)` / `bf16 vs fp16: Why bf16 Doesn't Overflow`.

## Description

```
bf16 vs fp16 for AI training: both halve fp32's bits for speed, but only bf16 keeps its range.

Every weight and activation in a model is a number, and its data type sets how many bits it gets: fp32 (32), fp16 and bf16 (16), fp8 (8). Fewer bits means more numbers per memory read and more math per cycle: a B200 does about 2,250 TFLOPS in bf16 and 4,500 in fp8.
fp16 spends its bits on precision, so 70,000 becomes inf (its max is 65,504). bf16 keeps fp32's 8 exponent bits: 70,000 becomes 70,144, less precise but in range. That's why mixed precision training on modern GPUs usually picks bf16 (PyTorch's autocast still defaults to fp16, so you name it).
fp8 keeps 3 mantissa bits and tops out at 448, so it needs a scaling library like NVIDIA's Transformer Engine. In PyTorch it's one line: torch.autocast with dtype=torch.bfloat16.

Part 4 of 8 on understanding the GPU. Next: tensor cores vs memory.
[POST LINK]

Level up human.

#machinelearning #deeplearning #llm #pytorch #Shorts
```

## Substack note

```
Why do AI models train in bf16 instead of fp32 or fp16? Every weight is a number, and fewer bits per number means twice the math per cycle. fp16 gets there by spending its bits on precision, so anything past 65,504 becomes inf. bf16 keeps fp32's range instead: 70,000 stays 70,144, a little less precise, never infinite. 45 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (44.70 s, v3) 2026-10-31.
On screen: the chip with fp32 / fp16 / bf16 / fp8 bit rows above it, bf16
the hero, a dashed ghost showing bf16 is half of fp32 (beat 1); tiles
streaming from GPU memory, each cell splitting in two, tensor cores (2);
the dense ladder TF32 1,125 / bf16 2,250 / fp8 4,500 TFLOPS, cells split
to four (3); the bits view with field counts and the value table: 1/3 →
0.33333334 / 0.33325195 / 0.33398438 / 0.34375, 70,000 → 70,000 / inf
(4); bf16's exponent outlined with fp32's, 70,144 (5); fp8 "4 exponent ·
3 mantissa", "max 448", "× scale", "Transformer Engine" (6); the autocast
card with `dtype=torch.bfloat16` (7).

Every number in the description is on screen or in the VO and was checked
2026-10-31 (storyboard "Facts"; sources: Lenovo's HGX B200 product guide
for 2,250 / 4,500 dense, NVIDIA's Transformer Engine FP8 primer for E4M3's
448, PyTorch's AMP docs for the autocast pattern; values from
`_kit/formats.py`). The description says "3 mantissa bits" where the VO
says "3 bits".
