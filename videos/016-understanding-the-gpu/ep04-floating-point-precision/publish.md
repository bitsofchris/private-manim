# Publish: floating point precision (Understanding the GPU, part 4 of 8)

Search phrase: **bf16 vs fp16** (storyboard preflight: autocompletes
verbatim, checked 2026-10-27; "fp32 vs fp16" second; "mixed precision
training" for the description). The take says bf16, fp16 and fp32 in its
first 18 s. Before publishing, glance at YouTube's results for it.

Final cut: `media/short.mp4`, 44.7 s.

## Titles

**Chosen (Chris, 2026-10-31): the hook title.** The day-10 read records
its search %.

Search title, for the person typing the phrase (39 characters, the phrase
first, the answer after it):

```
bf16 vs fp16: Why bf16 Doesn't Overflow
```

Hook title, for the person scrolling past (the stake first, a claim about
them; the phrase kept for search; 46 characters, the phrase starts at 34):

```
Your fp16 training can overflow (bf16 vs fp16)
```

## Description

```
bf16 vs fp16: both are 16 bits, but bf16 keeps fp32's range, so training doesn't overflow.

Fewer bits per number means more numbers per memory read and more math per tensor-core cycle: a B200 does about 2,250 TFLOPS in bf16 and 4,500 in fp8.
fp16 spends its bits on precision, so 70,000 becomes inf (its max is 65,504). bf16 keeps fp32's 8 exponent bits: 70,000 becomes 70,144, less precise but in range.
fp8 keeps 3 mantissa bits and tops out at 448, so it needs a scaling library like NVIDIA's Transformer Engine. Mixed precision training in PyTorch: torch.autocast with dtype=torch.bfloat16.

Part 4 of 8 on understanding the GPU. Next: tensor cores vs memory.
[POST LINK]

Level up human.

#bf16 #deeplearning #machinelearning #pytorch #Shorts
```

## Substack note

```
bf16 vs fp16: both are 16 bits, so why does everyone train in bf16? fp16 spends its bits on precision and tops out at 65,504; anything bigger becomes inf. bf16 keeps fp32's 8 exponent bits, so 70,000 stays 70,144: a little less precise, never infinite. Half the bits of fp32 also means twice the peak math. 45 seconds.
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
