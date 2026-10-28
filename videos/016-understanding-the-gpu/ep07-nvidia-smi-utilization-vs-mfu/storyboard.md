ENGINE: hyperframes

# nvidia-smi: GPU-Util vs MFU: storyboard (v3, merged with the old ep 7 nvidia-smi Short; realistic numbers; VO draft for Chris)

THE QUESTION: "MFU vs GPU saturation, what's the difference? How do I know
if my training is actually using my GPUs fully?"
WHO IS ASKING: a research engineer whose run shows 100 % in nvidia-smi (or
the Ray dashboard), who has heard "MFU" and doesn't know which number says
the training is efficient, how it's measured, or where PyTorch / Ray show it.
THE ANSWER IN ONE SENTENCE: nvidia-smi's GPU-Util only says some kernel
was running (busy); MFU says how much of the chip's peak math your model
actually used, and you compute it yourself from tokens per second.
THE SEARCH PHRASE: nvidia smi (checked 10/27 via YouTube's autocomplete
endpoint, not a browser: offered verbatim, and "nvidia smi tutorial";
results are ML/Linux monitoring videos. "gpu utilization 100" returns gaming
fixes; "mfu" and "model flops utilization" get no autocomplete.)

**One idea:** busy is not efficient. Utilization is a clock; MFU is a meter.

**Source note:** Chris's note was all questions, so this VO is a draft in
his voice for him to rewrite. His phrases kept: "saturation", "the metric
to look at". v3 folds in the old standalone nvidia-smi Short
(`../_archive/ep07-nvidia-smi/`, whose fact checks still apply).

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip, an
nvidia-smi card, the time strip, the MFU meter, a code card.

Series context: ep 7 of `../SERIES.md`. Kernels are ep 6 (one clause here),
6 × params is ep 3 (on the code card only, not derived in the VO), the
profiler is ep 8.

## Ledger (from `../SERIES.md`)

- One **B200** in an 8-GPU run, bf16 dense peak **2,250 TFLOPS**.
- **8B** dense model, **15,000 tokens/s per GPU**.
- 6 × 8e9 × 15,000 = **720 TFLOPS** → **MFU 32 %**.
- nvidia-smi on the same run: **GPU-Util 100 %**, ~143 GB used
  (illustrative; take the B200's reported total from a real readout).
- PaLM 540B: **46 % MFU** (Chowdhery et al. 2022, the paper that named MFU).

## VO (draft: 149 words without the if-time beat, 156 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | nvidia-smi says your GPU is at 100 percent. That only means it's busy. MFU tells you if it's doing useful work. | Frame 0 already working: the nvidia-smi card top-middle, `GPU-Util 100%` in magenta. Below it the chip, a 12 × 12 grid, a handful of cells lit teal, most dark. |
| 02_smi | It's the monitor that ships with NVIDIA's driver: memory, power, and GPU-Util, per GPU. | The card's columns light in turn as named: `Memory-Usage`, `Pwr:Usage/Cap`, `GPU-Util`. A small gloss under the card: "nvidia-smi: NVIDIA's GPU monitor". |
| 03_util | GPU-Util is the share of time any kernel was running, not how much of the chip it used. One tiny kernel counts as 100. | The time strip under the chip, every slot filled ("a kernel ran"). On "one tiny kernel" a single cell lights and the strip still reads 100 %. Magenta moves from `100%` to that cell. |
| 04_saturation | That's saturation. If it drops, your data loader is starving the GPU. | Grey gaps open in the time strip, label "idle: waiting on data"; a small loader box at left feeds batches late. Gaps close. |
| 05_mfu | MFU, model FLOPs utilization, is the FLOPs your model does each second, divided by what the chip could do. | The MFU meter appears right of the chip. The fraction draws under it: `model FLOPs/s ÷ peak FLOPs/s`. Magenta: the needle. |
| 06_measure | An 8-billion-parameter model at 15,000 tokens a second per GPU does 720 teraflops. A B200 peaks near 2,250. That's 32 percent. | Code card bottom-middle (the payoff, real lines): `flops = 6 * 8e9 * 15_000  # 7.2e14` / `mfu = flops / 2250e12` / `# 0.32`. ~32 % of cells light teal as the meter settles at 32 %. `GPU-Util 100%` stays lit above: the two numbers side by side. |
| 07_tools | Ray's dashboard shows the same busy number. Neither gives you MFU; you log it. | A small "Ray dashboard → GPU util 100 %" panel slides in beside the nvidia-smi card; a pen icon on the code card: "log it". |
| 08_scale *(if time)* | For scale: PaLM trained at 46 percent. | A tick on the meter at 46 %, labeled "PaLM 540B". |
| 09_close | Utilization tells you if the GPU is waiting. MFU tells you if the busy time is useful. Log tokens per second and watch MFU. | Final visual: the time strip (left, "busy?") and the meter (right, "useful?"), the meter in magenta. Takeaway only. |

Line 1 says the search phrase and the claim; MFU is named by ~5 s. Beat
08 is the *(if time)* cut. Beat 04 stays: it answers Chris's
"saturation" and stops the wrong takeaway ("ignore utilization").

## Facts to keep straight (notes, not VO)

- GPU-Util = NVML `utilization.gpu` = `torch.cuda.utilization()`: "percent
  of time over the past sample period during which one or more kernels
  was executing on the GPU". Sample window 1/6 s to 1 s by GPU, so never
  "the last second".
- Ray's dashboard reads the same NVML number
  (`dashboard/modules/reporter/gpu_providers.py`, checked by the old ep 7).
- 15,000 tokens/s per GPU and 32 % are the series' illustrative numbers,
  in the range real 8B runs report (torchtitan's H100 table: 5,762
  tokens/s/GPU in plain bf16 ≈ 28 %; NVIDIA's tuned recipes ~39–40 %).
  Big tuned runs: PaLM 46 %, Llama 3 405B 38–43 % (secondhand).
- 6N skips attention FLOPs (~13 % more at 8K context); torchtitan and
  Megatron count them, so their MFU reads a little higher than ours.
  Counting activation recompute gives HFU, not MFU.
- `torch.utils.flop_counter.FlopCounterMode` counts a step's FLOPs exactly:
  companion material.

## Layout

- Top band empty (captions burn in below).
- Stage top: the nvidia-smi card (Ray panel beside it in beat 07).
- Stage middle: the chip (12 × 12), the MFU meter right of it, the time
  strip under it; the loader box left in beat 04 only.
- Stage bottom-middle: the code card (beat 06 on).
- One magenta hero at a time: `100%` → the one lit cell → the needle.
