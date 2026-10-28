# Episode 2: FLOPs explained

- **Duration:** 61.9 s raw (`vo_raw.m4a`); ~55.8 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 54.10–116.00 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep02-flops-explained`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

A FLOP is one multiply or one add, and it's the unit that all AI compute is measured in. FLOP stands for floating-point operation.

Computers store decimals as a floating point: scientific notation in binary, a sign, digits, and an exponent. The point floats, so one format holds a ten-millionth and three million. Every weight, activation, and gradient is one of these numbers.

FLOPs with a small s is a count. Training an 8-billion-parameter model on 15,000 tokens costs about 720 trillion FLOPs.

FLOPS with a capital S is per second. This is a rate. A B200 peaks near 2,250 teraFLOPS in bf16. Tera is a trillion.

A transformer's compute is nearly all matrix multiplies, and a matmul is only multiplies and adds. GPUs are built to do exactly that, thousands at once.

Divide a run's FLOPs by the FLOPS you get, and you have GPU-hours. This is the bill.

## Where the take leaves the script

- Added "FLOP stands for floating-point operation." and "This is a rate."
- The *(if time)* GPU-hours line is recorded and is now the closer ("…and you have GPU-hours. This is the bill."). The scripted closer (find dense FLOPS at your precision on a spec sheet) is not recorded.
- Raw 61.9 s; about 55.8 s once pauses are capped, so under 60 without cutting a line.
- Ear checks: "Divide a run's FLOPs" (both recognizers heard "Divider runs FLOPs", clip `check_divide.m4a`); "three million" (Parakeet heard "three millionth"; Chris's transcript and the script say "million").
