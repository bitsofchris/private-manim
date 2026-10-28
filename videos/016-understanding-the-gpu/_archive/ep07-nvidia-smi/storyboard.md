ENGINE: hyperframes

# What nvidia-smi tells you: storyboard (v1, VO draft for Chris)

THE QUESTION: "What is NVIDIA SMI? I don't know what this means exactly."
WHO IS ASKING: a research engineer who types `nvidia-smi` (or opens the
Ray dashboard) to see if training is running, sees a wall of numbers, and
only really reads the one that says 100 %.
THE ANSWER IN ONE SENTENCE: nvidia-smi is the GPU monitor that ships with
NVIDIA's driver; it prints one row per GPU with memory, power, temperature,
processes and GPU-Util, and GPU-Util is only the share of time any kernel
ran, so read it for "is my job on the GPU, is memory full, is it ever idle",
not "is it efficient".
THE SEARCH PHRASE: nvidia smi (checked 10/27 via YouTube's autocomplete
endpoint and results page, not a browser: "nvidia smi" autocompletes
verbatim, as does "nvidia smi tutorial"; the other offers are driver errors
("has failed because it couldn't communicate", "command not found"). The
results for "nvidia smi" are ML/Linux monitoring: "How To Monitor and
Manage GPUs with Nvidia-smi Command", "GPU Basics: Provisioning +
Debugging with NVIDIA-SMI", "Real-Time GPU Monitoring with Dmon". "nvidia
smi explained" and "what is nvidia smi" get no autocomplete of their own,
but their results are on topic, so "explained" can ride in the title.)

**Titles (runbook step 9, Chris picks):** search `nvidia-smi Explained: What Every Number Means` · hook `nvidia-smi says 100%. One tiny kernel would too.`

**One idea:** nvidia-smi answers "is it running and is there room", not "is
it efficient". GPU-Util is a clock, not a meter.

**Source note:** Chris's input is one question in the 10/27 chat ("What
is NVIDIA SMI? I don't know what this means exactly"), with no answer
sentences, so this VO is a draft in his voice for him to rewrite (same as
ep 8). His phrase kept as THE QUESTION.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): a terminal card with
the nvidia-smi table, the series chip, the time strip, a code card.
Nothing needs Manim.

Series context: ep 7 of `../SERIES.md` (Understanding the GPU). Owns "what
nvidia-smi shows; GPU-Util = share of time any kernel ran". Ep 8 opens on
the same `GPU-Util 100%` and says it in one line ("Utilization is the share
of time any kernel ran. One tiny kernel still counts as 100."); this
episode is the full readout behind that line and must stay word-for-word
consistent with it. MFU gets one clause here (ep 8's home); out-of-memory
one clause (ep 12's home); kernels are not re-defined (ep 6's home).

## Ledger excerpt (every beat copies these, nothing invented per beat)

- GPU: one **B200**, GPU memory (HBM) **180 GB**.
- Model: **8B parameters**, dense transformer, bf16 with Adam.
- Memory for weights + grads + Adam state: **128 GB** before activations.
- nvidia-smi on the run: **GPU-Util 100 %**; same run **MFU 43 %**.
- On-screen table values that are **illustrative, not ledger** (flag in the
  beat brief, never spoken): memory `143051MiB / 183359MiB` (~150 GB of
  180: 128 GB of state plus activations), power `880W / 1000W`, temp `62C`,
  one process `python` holding `143040MiB`. 183,359 MiB is how one source
  reports a B200's 180 GB in nvidia-smi; 1,000 W is the B200 board power
  (see Facts to verify).
- The chip: the series 12 × 12 grid of core cells, the time strip under it
  (ep 7 is where the strip first appears).

## VO (draft: 135 words without the if-time beat, 151 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | nvidia-smi is your GPU's dashboard. It ships with NVIDIA's driver; type it and you get one row per GPU. | Frame 0 already working: a terminal card top-middle, prompt `$ nvidia-smi` and the real-looking table under it (header row, one GPU row `0  NVIDIA B200`, a Processes block). Every column dim teal at rest. Below it the series chip: 12 × 12 core cells, most lit teal, with the time strip under it, every slot filled. On "one row per GPU" the GPU row brightens. ~3 rows of stage for the card, ~3 for the chip. |
| 02_memory | Memory used, out of total: how close you are to out of memory. | Magenta hero: the `143051MiB / 183359MiB` cell. A thin bar fills under it to ~80 %; to the right of the chip the `HBM 180 GB` slab appears (series image) with the same fill. |
| 03_power *(if time)* | Power draw against its cap, and temperature: a quick check the card is working, not idling. | Hero moves to `880W / 1000W` then `62C`; the memory cell returns to teal. Nothing else moves. |
| 04_processes | At the bottom, the processes on the GPU. Your training script should be listed. | Hero moves to the Processes row: `0  …  48213  C  python  143040MiB`. A short teal tick links the row's MiB to the memory cell above. |
| 05_util | Then GPU-Util: the share of recent time any kernel was running. Not how much of the chip it used. | Hero moves to `100%`. The time strip under the chip pulses slot by slot ("a kernel ran" in each). On "not how much of the chip" the grid dims except its lit cells, so the strip (time) and the grid (space) read as two different things. |
| 06_tiny | One tiny kernel running nonstop reads 100 percent. This 8-billion-parameter run shows 100 and uses 43 percent of the chip's math. | The grid goes dark but one cell (magenta hero); the strip stays full and the card still reads `100%`. Then ~43 % of cells light teal (same lit fraction as ep 8's MFU beat), the strip still full, `100%` unchanged: busy is not the same as efficient. |
| 07_code | To watch it live, add dash l one, or query just the columns you need as CSV and log them. | The code beat. The terminal card's prompt line retypes to `$ nvidia-smi -l 1`, then a second card bottom-middle: `$ nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 1` with three output lines scrolling under it: `utilization.gpu [%], memory.used [MiB]` / `100 %, 143051 MiB` / `100 %, 143051 MiB`. Magenta bar slides to the `--query-gpu` line on "query". |
| 08_same_number | PyTorch and Ray's dashboard show this same number. | Two small labels slide in beside the code card: `torch.cuda.utilization()  # 100` and "Ray dashboard → GPU util 100%", each with a thin line back to the `100%` cell. |
| 09_close | Use nvidia-smi to check your job is on the GPU, memory has room, and it's never idle. For efficiency, compute MFU. | Final visual: three cells lit on the card in turn as named (Processes row, memory cell, the time strip under the chip), then an empty MFU gauge outline fades in right of the chip, label `MFU`, in magenta (the hand-off to ep 8). Takeaway only, no outro. |

Line 1 says the search phrase and lands what it is in its first clause; the
table the title names is on screen at frame 0 and named by ~2 s. Beat 03 is
the *(if time)* cut: its columns stay on screen and the viewer can read
them. Beat 05 + 06 are the episode's one real insight and stay. Beat 07 is
the code-on-screen beat and the only "how". Beat 08 answers the audience's
"I watch Ray, not nvidia-smi" and stays (8 words). The closer is the
viewer's next move (three checks, then MFU for efficiency), not line 1 again.

## Facts to keep straight (notes, not VO)

- nvidia-smi = NVIDIA System Management Interface, a command-line utility
  built on NVML; NVIDIA's SMI page says it ships with the NVIDIA GPU display
  drivers on Linux (and 64-bit Windows). It also manages (clocks, power
  limits, MIG, persistence mode); the Short only covers the monitor half.
- GPU-Util is NVML `nvmlUtilization_t.gpu`: "Percent of time over the past
  sample period during which one or more kernels was executing on the GPU"
  (NVML docs and the nvidia-smi manual, same wording). The sample period
  is between 1 s and 1/6 s depending on the product, hence "recent time" in
  the VO, not "the last second". Older NVML docs said "any work", and an
  NVIDIA forum thread notes 3D/graphics work also counts; for a training
  box that's the same thing.
- `torch.cuda.utilization()` docstring is the same sentence, "as given by
  `nvidia-smi`" (checked in `torch/cuda/__init__.py`, main). Ray's dashboard
  reporter (`dashboard/modules/reporter/gpu_providers.py`, master, 10/27)
  calls `nvmlDeviceGetUtilizationRates(...)` and reports `.gpu`: the same
  number. So beat 08 is verified for both.
- Memory used in nvidia-smi is what the process holds from the driver. With
  PyTorch that includes the caching allocator's reserved-but-free blocks,
  so it reads higher than `torch.cuda.memory_allocated()`. That is why the
  VO says "how close you are", not "how much your model needs". Companion
  material; ep 12 owns memory.
- Processes in a container: nvidia-smi inside a container often shows no
  process names or PIDs (PID namespace), even when the job is on the GPU.
  The VO says "should be listed"; the caveat goes in the companion.
- `-l` / `--loop=SEC`: repeat at an interval; with no value it defaults to
  5 s. `watch -n 1 nvidia-smi` is the full-screen alternative. `nvidia-smi
  dmon` is the rolling one-line-per-interval view (up to 16 GPUs). Both
  companion material.
- `--query-gpu=utilization.gpu,memory.used --format=csv -l 1`: valid; the
  CSV header prints units (`utilization.gpu [%], memory.used [MiB]`);
  `--format=csv,noheader,nounits` for bare numbers; `-f FILE` to log.
  `nvidia-smi --help-query-gpu` lists every field.
- Deeper counters: DCGM `SM_ACTIVE` (fraction of SMs with work) and
  `PIPE_TENSOR_ACTIVE` (tensor-core pipe busy) say how much of the chip
  is used; companion material for ep 7 / ep 8.
- The table layout on screen follows the classic nvidia-smi box layout
  (driver/CUDA header, `GPU Name Persistence-M | Bus-Id Disp.A | Volatile
  Uncorr. ECC`, `Fan Temp Perf Pwr:Usage/Cap | Memory-Usage | GPU-Util
  Compute M.`, then Processes). Fan reads `N/A` on an SXM B200. Exact
  column order varies a little by driver version; the beat agent copies a
  real recent output if one is at hand.

## Facts to verify

- `183359MiB` as nvidia-smi's total for a B200: from one web source
  (search result summary, 10/27), not an NVIDIA page. If unconfirmed, use
  a round `180GB`-consistent figure and note it, or show `183359MiB` only
  if someone pastes a real B200 readout.
- `1000W` power cap: B200 TDP/TGP 1,000 W per Lenovo Press (ThinkSystem
  B200 180GB 1000W) and SemiAnalysis; some B200 SKUs run lower caps.
  Illustrative on screen, never spoken.
- `880W`, `62C`, PID `48213`: invented for the picture, never spoken.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-middle: the terminal card with the nvidia-smi table, ~3 rows.
  Columns must be phone-legible: if the full table is too wide, show the
  two classic GPU rows plus Processes and crop the header text, never
  shrink below the label floor.
- Stage middle: the series chip (12 × 12 grid), `HBM 180 GB` slab to its
  right (from beat 02), the time strip directly under the grid.
- Stage bottom-middle: the code card (beat 07 on), the torch / Ray labels
  beside it (beat 08).
- One magenta hero at a time: GPU row → memory cell → (power, temp) →
  Processes row → `100%` → the one lit cell → `--query-gpu` line → MFU
  gauge outline.
