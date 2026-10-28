ENGINE: hyperframes

# Multi-GPU training, why 8 GPUs aren't 8× faster: storyboard (v1; VO draft for Chris)

THE QUESTION: "Why doesn't 8 GPUs give me 8× the speed?"
WHO IS ASKING: a research engineer who moved a training run from one GPU
to an 8-GPU node with PyTorch DDP (or torchrun / Ray Train), got less than
8× the tokens per second, and doesn't know what the GPUs are doing in the
missing time or what to change.
THE ANSWER IN ONE SENTENCE: in data-parallel training every GPU must
average its gradients with all the others (an all-reduce) before anyone
can take the optimizer step; that sync is communication, not math, so
whatever part of it isn't overlapped with the backward pass is time no
GPU spends on the model, and MFU drops.
THE SEARCH PHRASE: multi gpu training pytorch (checked 10/27 via YouTube's
autocomplete endpoint, not a browser: "multi gpu training" offers "multi
gpu training pytorch", and its results are DDP code walkthroughs.
"distributed data parallel" offers "distributed data parallel pytorch" and
"pytorch ddp" autocompletes, both with on-topic results (the PyTorch DDP
series), so `DDP` goes in the title as the second phrase. "all reduce"
autocompletes but mixes in body-fat results; "nccl" mixes in volleyball
and schools; "multi gpu" alone is PC builds and gaming.)

**Titles (runbook step 9, Chris picks):** search `Multi-GPU Training in PyTorch: Why 8 GPUs Aren't 8× Faster (DDP)` · hook `8 GPUs, not 8× faster. Here's where the time goes.`

**One idea:** more GPUs means more talking. The gradient sync is the tax;
overlap hides it, syncing less often shrinks it.

**Source note:** adjacent episode; Chris didn't ask this question, so the
VO is a draft in his voice (plain, short sentences) for him to rewrite.
No scaling-efficiency percentage is claimed anywhere: it depends on model,
batch, and fabric, and no ledger number pins it.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): eight copies of the
series chip, gradient tiles moving between them, per-chip time strips, the
MFU meter, a code card. Nothing needs Manim.

Series context: ep 13 of `../SERIES.md` (Understanding the GPU), the last
one. Builds on ep 8 (MFU, one clause here), ep 9 (the profiler, named in
the closer only), ep 12 (what fills memory, one clause: each GPU holds a
full copy). FSDP is not named in the VO; it is a companion line.

## Ledger (every beat copies these, nothing invented per beat)

- GPU: **B200**, here **eight** in one server (an HGX / DGX B200 node).
- Model: **8B parameters**, dense transformer, trained in **bf16** with Adam.
- Gradients per step: one bf16 number per parameter = 8e9 × 2 bytes =
  **16 GB per GPU**, all-reduced every step (new, derived from the
  ledger's 8B and bf16 grads; see Facts).
- DDP default bucket: **25 MiB** (`bucket_cap_mb`; verified in the PyTorch
  DDP API docs: "When unset, DDP uses a 25 MiB bucket size").
- NVLink 5 on B200: **1.8 TB/s per GPU total, 900 GB/s each direction**
  (18 links × 100 GB/s; third-party sources citing Lenovo's HGX B200 guide;
  not in the VO, on screen only as the label "NVLink").
- Between servers: **400 Gb/s** InfiniBand per GPU (= 50 GB/s; DGX B200
  compute fabric, 8 × single-port ConnectX-7). Not in the VO.
- MFU, ep 8: 43 % on one B200 (one clause at most; no multi-GPU MFU is
  claimed).

## VO (draft: 150 words without the if-time beat, 167 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Eight GPUs don't train eight times faster, because every step they have to stop and share their gradients. | Frame 0 already working: eight small copies of the series chip (each a rounded box with the 12 × 12 grid shrunk to fit) in a ring mid-stage, all cells lit teal mid-backward. Under each chip a short time strip. Then all eight grids go dark at once and magenta gradient tiles start moving chip to chip around the ring. Magenta hero: the tiles. ~7 rows of stage. |
| 02_ddp | In PyTorch DDP, each GPU holds a full copy of the model and trains its own slice of the batch. | A batch stack enters from the left (the ep 10 loader box), splits into eight slices, one slides into each chip. Each chip gets a tiny `8B` tag (same model on all eight). Grids light teal: forward, backward. |
| 03_code | Setup is two lines: start NCCL, NVIDIA's library for GPUs talking to each other, and wrap the model. | Code card, bottom-middle (real lines, the code beat): `dist.init_process_group("nccl")` / `model = DDP(model, device_ids=[rank])`. Each line lights as it's named; the ring's links appear on "NCCL". Magenta hero: the `DDP(...)` call. |
| 04_allreduce | After backward, each GPU has different gradients. An all-reduce averages them, so every copy takes the same step. | Each chip shows its own gradient tile in a different teal shade. Tiles pass around the ring; on "averages" all eight tiles become the same shade. Label on the ring: `all-reduce`. Then all eight chips tick `step` together. Magenta hero: the averaged tile. |
| 05_volume | For an 8-billion-parameter model in bf16, that's 16 gigabytes of gradients, every step. | A slab `16 GB` stacks up beside one chip (the volume, drawn as a slab like the HBM slab), arrow into the ring. Magenta hero: `16 GB`. |
| 06_wait | That's communication, not math. If it waits until backward ends, no GPU does model math until it's done, and MFU drops. | The time strips: each shows `forward | backward` in teal, then a wide grey slot labeled `all-reduce` before `step`. The grid cells sit dark during the grey slot. The MFU meter (ep 8's) appears right of the ring and drops. Magenta hero: the grey slot on one strip. |
| 07_overlap | DDP overlaps them. It packs gradients into 25-megabyte buckets and sends each one while backward is still computing the rest. | The grey slot breaks into small bucket tiles that slide left underneath the backward segment (two lanes: compute on top, communication below). Only the last bucket's sliver remains after backward. The meter climbs back. Code card adds a comment: `# bucket_cap_mb=25 (default)`. Magenta hero: the first bucket leaving early. |
| 08_network *(if time)* | Inside one server that's NVLink. Across servers it crosses the network, at a fraction of the bandwidth. | The ring's links labeled `NVLink`. A second ring of eight appears below (a second server); one thin link between the rings labeled `network`. The tiles crawl across the thin link. |
| 09_close | So profile one step. If a gap shows up after backward, sync less often: bigger batches per GPU, or accumulate with no_sync. | Final visual: one time strip, large, with a small grey sliver after backward. Code card swaps to `with model.no_sync():` / `    model(x).sum().backward()  # accumulate, no all-reduce` then `model(x).sum().backward()  # this one syncs`. The strip shows four backward segments then one all-reduce. Magenta hero: `no_sync`. Takeaway only, no outro. |

Line 1 answers the question in its first clause and names the cause in
its second; "DDP" and the ring are on screen and said by ~6 s. Beat 08 is
the *(if time)* cut: an 8-GPU single server is the question as asked, and
the network is the next episode's worry, not this one. Beat 06 stays: it
is the contrast that stops the wrong takeaway ("the GPUs are busy, so
it's fine"). Beat 07 is the only "how DDP fixes it" beat and stays. The
closer is the viewer's next move (profile, then sync less often), not line
1 again.

## Facts to keep straight (notes, not VO)

- **Averaging:** the PyTorch DDP design note: the allreduce operations
  "calculate mean of gradients across all processes", and "averaged
  gradients are written to the `param.grad` field of all parameters".
  So every replica runs the same optimizer step on the same gradients.
- **Overlap:** same note: "DDP's performance advantage comes from
  overlapping allreduce collectives with computations during backwards";
  when all gradients in a bucket are ready, the Reducer launches an async
  allreduce on it while backward continues. Buckets are filled roughly in
  reverse parameter order, which is why the last layers' gradients go
  first. The last bucket cannot overlap (backward is done), so some sync
  time is always exposed; that's why the VO says "overlaps", not "hides".
- **25 MiB:** `bucket_cap_mb` default `None` → 25 MiB (DDP API docs,
  PyTorch 2.14). VO says "25-megabyte"; the card says `bucket_cap_mb=25`.
- **no_sync:** DDP's `no_sync()` context manager: gradients accumulate
  locally and sync on the first forward-backward after the context
  exits. The docs warn the forward pass must be inside the context too,
  or gradients still sync; the on-screen code must show forward and
  backward inside `with model.no_sync():` (shorten to
  `loss = model(x).sum(); loss.backward()` if space is tight, never just
  the backward).
- **16 GB assumes bf16 gradients**, per the ledger (bf16 weights + bf16
  grads + fp32 master + Adam). With `torch.autocast` and fp32 params (the
  common AMP setup), DDP all-reduces fp32 gradients: 32 GB. DDP also has
  a bf16 compression hook (`bf16_compress_hook`). Keep the VO on the
  ledger's setup.
- **Bytes on the wire:** a ring all-reduce sends and receives about
  2 × (N−1)/N × the gradient size per GPU: 2 × 7/8 × 16 GB = 28 GB per
  GPU per step on 8 GPUs. At NVLink's 900 GB/s per direction that is
  ~31 ms in the ideal case; NCCL picks ring or tree algorithms and real
  bus bandwidth is lower. Not in the VO (no step time in the ledger to
  compare it against).
- **NVLink vs network:** 900 GB/s per direction vs 50 GB/s (400 Gb/s
  InfiniBand) per GPU, ~18× less, on a DGX B200. The VO says only "a
  fraction". Verify against NVIDIA's DGX B200 datasheet before putting
  any ratio on screen.
- **GPU-Util during the sync:** NCCL runs as GPU kernels, so nvidia-smi's
  GPU-Util (ep 7) still reads busy while the all-reduce runs. That's why
  beat 06 says "no model math", not "idle". A good companion line: the
  all-reduce is another case of busy-but-not-useful.
- **"Full copy of the model":** true for DDP (ep 12 owns the memory: 16
  bytes per param = 128 GB for 8B with Adam, which fits in a B200's 180 GB
  before activations). FSDP shards weights, grads and optimizer state
  across GPUs instead; companion material, not this Short.
- **Bigger per-GPU batches** sync the same 16 GB but do more compute per
  sync, so the sync is a smaller share of the step. Accumulation over k
  micro-batches syncs once per k. Both change the effective batch size
  (learning-rate implications are companion material).
- No scaling-efficiency number (e.g. "7.x× on 8 GPUs") is claimed; none
  is cited for this setup.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: the batch / loader box enters from the upper left (beat 2);
  otherwise empty.
- Stage middle: eight small chips in a ring (a 3-2-3 arrangement on a
  1080-wide frame, ~260 px per chip, each with the 12 × 12 grid drawn at
  that size, the same drawing as the series chip, just scaled). Links
  between neighbors form the ring. The MFU meter sits right of the ring
  (beat 6 on), small. Beat 8 shrinks the ring and adds a second one below.
- Under the ring: the time strips. Beats 1–5 a short strip under each
  chip; beat 6 on, one representative strip, full width, two lanes
  (compute on top, communication below) for beat 7.
- Stage bottom-middle: the code card (beat 3 on; swaps in beat 9).
- One magenta hero at a time: the gradient tiles → `DDP(...)` → the
  averaged tile → `16 GB` → the grey all-reduce slot → the first bucket →
  `no_sync`.
