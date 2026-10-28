# Episode 4: floating point precision

- **Duration:** 51.9 s raw (`vo_raw.m4a`); ~43.2 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 177.62–229.48 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep04-floating-point-precision`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

bf16 makes training faster because each number is half the bits of fp32.

Fewer bits means more numbers per memory read and more multiply-adds per tensor-core cycle. A B200 peaks near 2,250 teraflops in bf16. fp8 doubles that.

fp16 is also 16 bits, but it spends them on precision, so anything past 65,504 will overflow. bf16 keeps fp32's eight exponent bits: same range, less precision, and training stays stable.

fp8 keeps just three bits, so training in it needs a scaling library like NVIDIA's Transformer Engine.

In PyTorch, wrap your forward pass in autocast with bf16. You get faster math without the overflow.

## Where the take leaves the script

- Not recorded: "Half the bits, twice the peak math", the three-parts line (sign, exponent, mantissa), and the sparse spec-sheet trap. "Exponent bits" and "precision" now arrive undefined; the visual can carry the three fields.
- The *(if time)* fp8 line is recorded but says "three bits", not "three mantissa bits": fp8 is 8 bits, 3 of them mantissa (E4M3). The visual/caption must show "3 mantissa bits" so the frame doesn't state a wrong number.
- A 5.0 s pause before "In PyTorch" (take 218.7–223.7 s); the tightener caps it.
- "Floating time precision" in the take is the announcement, removed.
