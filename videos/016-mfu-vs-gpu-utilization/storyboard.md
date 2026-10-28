ENGINE: hyperframes

# MFU vs GPU utilization: storyboard (v1, VO draft for Chris)

THE QUESTION: "MFU vs GPU saturation, what's the difference? How do I know
if my training is actually using my GPUs fully?"
WHO IS ASKING: a research engineer whose run shows 100 % in nvidia-smi (or
the Ray dashboard), who has heard "MFU" and doesn't know which number says
the training is efficient, how it's measured, or where PyTorch / Ray show it.
THE ANSWER IN ONE SENTENCE: GPU utilization only says the GPU is busy
(some kernel was running); MFU says how much of the chip's peak math your
model actually used, and you compute it yourself from tokens per second.
THE SEARCH PHRASE: nvidia smi gpu utilization (checked 10/27 via YouTube's
autocomplete endpoint, not a browser: "nvidia smi" autocompletes and its
results are ML/Linux monitoring videos. "gpu utilization 100" autocompletes
but its results are gaming fixes. "mfu" and "model flops utilization" get
no autocomplete; the latter's results are on topic, so it goes in the title
as the second phrase.)

**Titles (runbook step 9, Chris picks):** search `nvidia-smi GPU Utilization vs MFU (Explained)` · hook `Your GPU says 100%. It's lying. (MFU explained)`

**One idea:** busy is not efficient. Utilization is a clock; MFU is a meter.

**Source note:** the vault block is all questions, with no answer sentences,
so this VO is a draft in Chris's voice for him to rewrite (same as 015).
His own phrases kept: "effectively using your GPUs", "the metric to look
at", "how is it measured".

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): one GPU chip drawn
as a grid of SMs, a time strip, a meter, and a code card. Nothing needs Manim.

Series context: fits the Bytes to Tensor / dataloading thread
(`../014-pytorch-dataloading/`): low utilization is the loader's problem;
this Short is the metric that tells you which problem you have.

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one H100 SXM, bf16 dense peak **989 TFLOPS** (say "about 990").
- Model: **1B parameters**, dense transformer.
- Throughput: **60,000 tokens/s** on that GPU.
- FLOPs per token, training: **6 × params** (forward 2, backward 4).
- Achieved: 6 × 1e9 × 60,000 = **360 TFLOPS** → MFU **36 %**.
- nvidia-smi on the same run: **GPU-Util 100 %**.
- Reference point: PaLM 540B trained at **46 % MFU** (Chowdhery et al. 2022,
  the paper that named MFU).
- The SM grid: 12 × 11 = 132 cells (an H100 has 132 SMs).

## VO (draft: 154 words without the if-time beat, 161 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | nvidia-smi says your GPU is at 100 percent. That only means it's busy. MFU tells you if it's doing useful work. | Frame 0 already working: a terminal card top-middle with the real nvidia-smi row, `GPU-Util 100%` in magenta. Below it the chip: a 12 × 11 grid of SM cells, a handful lit teal, most dark. ~6 rows of stage. |
| 02_util | Utilization is the share of time any kernel was running. One tiny kernel on one core still counts as 100. | A time strip under the chip, every slot filled ("a kernel ran"); on "one tiny kernel" a single SM cell lights and the strip still reads 100 %. The magenta hero moves from the `100%` to that one lit cell. |
| 03_saturation | That's saturation. When it's low, your data loader is starving the GPU. Fix that first. | Gaps open in the time strip (grey slots, label "idle: waiting on data"); a small loader box at the left feeds batches in late. Gaps close as batches arrive on time. |
| 04_mfu | MFU, model FLOPs utilization, is the metric to look at: the math your model needs, divided by the math the chip could do. | A meter appears right of the chip, label `MFU`. The SM grid now lights proportionally: ~36 % of cells teal, filling as the meter rises. The fraction draws under it: `model FLOPs / peak FLOPs`. Magenta hero: the meter needle. |
| 05_measure | Here's how it's measured: six times parameters times tokens per second. One billion parameters at sixty thousand tokens is 360 teraflops. An H100 peaks near 990. Thirty-six percent. | The code card, bottom-middle (the payoff beat, real lines): `flops = 6 * n_params * tokens_per_sec` / `mfu = flops / 989e12` / `# 0.36`. Each line lands on its number; the meter settles at 36 %. Under the terminal card, `GPU-Util 100%` stays lit: the two numbers side by side. |
| 06_tools | PyTorch's profiler shows the idle gaps. Ray's dashboard shows the same busy number as nvidia-smi. Neither gives you MFU; you log it yourself. | Two small labeled panels swap into the terminal card's place: "torch.profiler → idle gaps" (the time strip with gaps), "Ray dashboard → GPU util" (a 100 % gauge). A pen icon on the code card: "log it yourself". |
| 07_good *(if time)* | For scale: PaLM trained at 46 percent. | A tick on the meter at 46 % labeled "PaLM 540B". |
| 08_close | Utilization tells you if the GPU is waiting. MFU tells you if the busy time is useful. Log tokens per second and watch MFU. | Final visual: the time strip (left, label "busy?") and the MFU meter (right, label "useful?"), the meter in magenta. Takeaway only, no outro. |

Line 1 says the search phrase and lands the claim ("only means it's
busy") in its second sentence; MFU is named and on screen by ~6 s.
Beat 07 is the *(if time)* cut. Beat 03 stays: it is the contrast that
stops the wrong takeaway ("ignore utilization"). Beat 06 answers Chris's
"how does PyTorch or Ray show you this" and stays.

## Facts to keep straight (notes, not VO)

- nvidia-smi `utilization.gpu` / `torch.cuda.utilization()`: "percent of
  time over the past sample period during which one or more kernels was
  executing on the GPU" (NVML header). Time-based, says nothing about how
  many SMs or tensor cores were used.
- Better hardware counters exist (DCGM `SM_ACTIVE`, `PIPE_TENSOR_ACTIVE`);
  cut from the VO for length, companion material.
- 6·N·T ignores attention FLOPs (small at short context) and counts no
  activation recompute; counting recompute gives HFU, not MFU.
- `torch.utils.flop_counter.FlopCounterMode` can count a step's FLOPs
  exactly instead of 6·N; companion material.
- To verify before publish: that Ray (Train / dashboard) still has no
  built-in MFU metric in the current release. The dashboard's GPU panel
  is NVML utilization.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: terminal card / tool panels (beats 1, 6), ~1.5 rows.
- Stage middle: the SM grid (12 × 11) with the MFU meter to its right; the
  time strip directly under the grid.
- Stage bottom-middle: the code card (beat 5 on).
- One magenta hero at a time: `100%` → the one lit SM → the MFU needle.
