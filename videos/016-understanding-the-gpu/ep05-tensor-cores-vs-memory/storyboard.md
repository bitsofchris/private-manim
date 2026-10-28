ENGINE: hyperframes

# Tensor cores vs memory: storyboard (v1, B200 numbers; VO draft for Chris)

THE QUESTION: "Where does the time go inside the GPU? Are the tensor cores
the bottleneck, or is it memory?"
WHO IS ASKING: a research engineer who has heard "tensor cores" and
"memory-bound", trains on a B200, and can't picture why a matmul is fast
while a ReLU or a layernorm takes time out of all proportion to its math.
THE ANSWER IN ONE SENTENCE: tensor cores do the matrix math behind the
chip's peak FLOPS, but every number has to flow in from GPU memory (HBM)
first; a matmul uses each number it loads thousands of times, so the cores
stay fed (compute-bound), while an elementwise op like ReLU does one
operation per number, so the chip waits on memory (memory-bound).
THE SEARCH PHRASE: tensor cores explained (checked 10/27 via YouTube's
autocomplete endpoint, not a browser: "tensor cores" offers "tensor cores
explained", "tensor cores vs cuda cores", "how tensor cores work"; the
results page for "tensor cores explained" is all GPU/AI explainers ("What
are Tensor Cores?", "Tensor Cores in a Nutshell"). "memory bound vs compute
bound" gets no autocomplete but its results are on topic, so it goes in the
title as the second phrase. "compute bound" autocompletes to "cpu bound
games": avoid. "roofline model explained" and "arithmetic intensity"
autocomplete but are narrower; companion material.)

**Titles (runbook step 9, Chris picks):** search `Tensor Cores Explained: Compute-Bound vs Memory-Bound` · hook `Your GPU's fastest part spends most of its time waiting`

**One idea:** the math is cheap; moving the numbers is the cost. A matmul
reuses what it loads, an elementwise op doesn't.

**Source note:** Chris's idea is one line ("Tensor cores vs memory on the
GPU, maybe as data flowing through it") with no answer sentences, so this
VO is a draft in Chris's voice for him to rewrite (same as ep 8). His own
image kept as the spine: data flowing through the chip.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): the series chip, the
HBM slab and pipe, tiles moving down it, a code card. Nothing needs Manim.

Series context: ep 5 of `../SERIES.md` (Understanding the GPU). This
episode adds the HBM slab and the pipe to the series chip, and the
tensor-core sub-block inside each cell. It owns "tensor cores vs memory;
compute-bound vs memory-bound". FLOP is ep 2's (one clause here); the fix,
`torch.compile` fusion, is ep 11's (one clause in the closer).

## Ledger (every beat copies these, nothing invented per beat)

- GPU: one **B200**, bf16 dense peak **2,250 TFLOPS**; HBM **180 GB**,
  bandwidth about **8 TB/s**.
- **Needed intensity:** 2,250e12 ÷ 8e12 = **281 FLOPs per byte** (say
  "about 280"). This episode's derived number; listed under "Facts to
  verify" for SERIES.md.
- **Matmul on screen:** `x` 8192 × 4096, `W` 4096 × 4096, bf16. FLOPs
  2 × 8192 × 4096 × 4096 = 2.75e11; bytes if each matrix is read or
  written once = 2 × (8192·4096 + 4096·4096 + 8192·4096) = 168 MB;
  **~1,640 FLOPs per byte**. Each weight meets all 8,192 rows of `x`; each
  number in `x` meets all 4,096 columns of `W`: "thousands of multiply-adds".
- **ReLU in bf16:** read 2 bytes, write 2 bytes, one operation →
  **0.25 FLOPs per byte** (NVIDIA's own table lists ReLU at 0.25). Short of
  280 by a factor of ~1,100: say "over a thousand times short".
- **Add in bf16:** two in, one out = 6 bytes for 1 FLOP, ~0.17 per byte
  (if-time beat only, not spoken as a number).
- The grid is 12 × 12 cells, a picture, not the SM count; no label claims
  a number.

## VO (draft: 140 words without the if-time beat, 150 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | Tensor cores are the part of a GPU that does matrix math. They're only as fast as memory can feed them. | Frame 0 already working: the series chip mid-stage (12 × 12 cells), the HBM slab to its right (`HBM 180 GB`), a pipe joining them. Teal tiles stream down the pipe; every cell's tensor-core sub-block lit teal. On "tensor cores", one cell's sub-block goes magenta with a small label `tensor core`. ~7 rows of stage. |
| 02_flow | Your data lives in GPU memory, HBM. Before any math happens, it flows through cache into the cores. | Zoom along the path: one tile leaves the slab, passes a thin band labeled `cache` at the chip's edge, lands in a cell. The magenta hero moves to the travelling tile. Labels: `HBM`, `cache`, `cores`. |
| 03_numbers | A B200's tensor cores do about 2,250 teraflops. Memory delivers about 8 terabytes a second. | Two labels land on their words: above the grid `2,250 TFLOPS` (bf16), on the pipe `8 TB/s`. The pipe is drawn visibly narrow next to the grid. |
| 04_ratio | So each byte you load needs about 280 FLOPs done on it, or the cores sit waiting. That's arithmetic intensity. | The fraction draws under the chip: `2,250 TFLOPS ÷ 8 TB/s ≈ 280 FLOPs / byte`. A single byte-tile with a counter ticking to `280`. Magenta hero: the `280`. On "arithmetic intensity", the label `arithmetic intensity = FLOPs ÷ bytes` replaces the counter. |
| 05_matmul | A matrix multiply clears that easily. Each number it loads gets used in thousands of multiply-adds. It's compute-bound. | Code card bottom-middle (the payoff code, real lines): `y = x @ W   # 8192×4096 @ 4096×4096` / `# ~1,640 FLOPs per byte`. Tiles trickle down the pipe; every cell stays lit teal. One tile fans out into many arcs across a row of cells ("used thousands of times"). Label under the chip: `compute-bound`. Magenta hero: `@`. |
| 06_relu | ReLU does one operation per number, four bytes moved, and never touches the tensor cores. That's over a thousand times short. It's memory-bound. | Second code line lands under the first: `y = torch.relu(x)   # 0.25 FLOPs per byte`. The pipe fills and jams with tiles; most cells go dark, the tensor-core sub-blocks all dark; a few cells blink grey (the plain cores doing the max). Label swaps to `memory-bound`. Magenta hero: the jammed pipe. |
| 07_others *(if time)* | Add, dropout, layernorm: same story. A few operations per number. | Three more one-line chips slide under the ReLU line: `x + y`, `dropout(x)`, `layer_norm(x)`, each tagged `memory-bound` in grey. Pipe stays jammed. |
| 08_close | When a step is slow, look at the small ops between the matmuls. That's your GPU waiting on memory, and fusing them is the fix. | Final visual: a strip under the chip of one step's ops, wide teal `@` blocks with grey elementwise blocks between them; the grey blocks go magenta together (the tight group). Takeaway only, no outro. |

Line 1 says the search phrase and lands the claim in its second sentence;
"memory" is on screen from frame 0 and spoken by ~4 s. Beat 07 is the
*(if time)* cut. Beat 06 stays: it is the contrast the whole Short exists
for. Beat 04 names arithmetic intensity because it is the term the viewer
will search next; it is spoken once. The closer's fusion clause is ep 11's
home: one clause, no how. Code on screen: beats 05 and 06 (`x @ W` vs
`torch.relu(x)`).

## Facts to keep straight (notes, not VO)

- **ReLU does not run on tensor cores.** Tensor cores only execute
  matrix-multiply-accumulate on blocks; elementwise math runs on the
  regular CUDA cores (NVIDIA, *GPU Performance Background User's Guide*:
  "the element-wise addition of two half-precision tensors would be
  performed by CUDA cores, rather than Tensor Cores"). So beat 06 says
  "never touches the tensor cores" and "your GPU waiting on memory", not
  "the tensor cores wait". The visual keeps the sub-blocks dark and lets a
  few plain cells blink.
- **"Thousands of multiply-adds" is the math, not the traffic.** It counts
  how many multiply-adds each number takes part in. Whether HBM is read
  only once per number depends on tiling through cache and shared memory;
  real matmul kernels re-read some data and still land far above 280 at
  these sizes. The 1,640 figure assumes each matrix is read or written
  once (NVIDIA's guide makes the same assumption).
- **Small matmuls can be memory-bound too.** A batch-1 matmul (a
  matrix-vector product, as in inference decoding) is ~1 FLOP per byte.
  The VO says "a matrix multiply" with large shapes on the code card;
  narrow it to "a big matrix multiply" if Chris wants it airtight.
- **"Cache" is a simplification** of HBM → L2 → shared memory / registers
  → tensor cores. One band labeled `cache` stands for all of it.
- **280 is the B200's bf16 ridge point** (the roofline model's knee).
  "Roofline" is companion material, not VO.
- ReLU as a "FLOP": it is a compare (max), counted as one operation;
  NVIDIA's table counts it as 1 FLOP per element. The VO says "operation".
- Layernorm does several ops per element (mean, variance, scale, shift),
  still far under 280: memory-bound.

## Facts to verify before publish

- The 8 TB/s figure: most spec pages give 8 TB/s for B200 HBM3e; one
  lists 7.7 TB/s. At 7.7 the ratio is 292, still "about 280–290"; if
  Chris wants exact, say "almost 300". Confirm against NVIDIA's current
  datasheet.
- Add "needed intensity ≈ 280 FLOPs/byte (2,250 TFLOPS ÷ 8 TB/s)" to the
  SERIES.md ledger so ep 11 reuses the same number.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top: the `2,250 TFLOPS` label above the chip; the fraction (beat
  04) replaces it.
- Stage middle: the core grid (12 × 12) left-of-centre, the HBM slab to
  its right, the pipe between them (narrow, the bandwidth); the `cache`
  band on the chip's edge where the pipe enters. `compute-bound` /
  `memory-bound` label directly under the grid.
- Stage bottom-middle: the code card (beat 05 on), two lines, then up to
  three more in beat 07; the op strip replaces it in beat 08.
- One magenta hero at a time: a tensor-core sub-block → the travelling
  tile → `280` → `@` → the jammed pipe → the elementwise blocks (one group).
