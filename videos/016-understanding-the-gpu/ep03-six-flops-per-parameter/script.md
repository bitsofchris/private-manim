# Episode 3: six FLOPs per parameter

- **Duration:** 48.2 s raw (`vo_raw.m4a`); ~44.0 s with pauses capped at 0.4 s (an estimate, before step 5).
- **Source:** cut from `~/Creating/016-gpu-understanding.m4a` at 122.15–170.30 s, announcement removed.
- **Planned script:** `../SCRIPTS.md`, `ep03-six-flops-per-parameter`. Reference only; what is below is the VO.
- **Recorded:** 2026-10-28, one take for the series (see `../SERIES.md`, "How it was recorded").
- **Working name only.** Titles are proposed at runbook step 9.

## As recorded

Training an LLM costs about six FLOPs per parameter per token. You spend two FLOPs on the forward pass and about four on the backward pass.

Almost every parameter sits in a weight matrix. Here's a tiny one: three inputs, two outputs, six weights. Going forward, each weight does one multiply and one add. So you have two FLOPs per weight, 12 for this entire layer.

Coming backwards now, the error has to reach the layer before, so the same weights in reverse, another multiply and add each.

Then each weight needs its own gradient for the optimizer. Error times input, added to a running total, is two more. That's six per weight per token.

So training compute is six times parameters times tokens. An 8-billion-parameter model at 15,000 tokens per second per GPU is doing 720 teraflops.

## Where the take leaves the script

- Line 1 now says "about six"; the forward/back split is its own sentence ("You spend two FLOPs on the forward pass and about four on the backward pass").
- Not recorded: "Backward costs twice the forward", the *(if time)* Llama 3 line, and the closer ("Before your next run, multiply six by parameters by tokens…"). The take ends on "720 teraflops", with no next move for the viewer.
- Mishearings fixed (both checked against Chris's transcript): "Training an LLM" (Parakeet: "Training in LLM"), "one multiply and one add", "two FLOPs per weight".
