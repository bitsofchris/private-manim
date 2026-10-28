# Understanding the GPU: all scripts (VO drafts for Chris)

All 13 VOs in one file, the order to record them (`agents/series.md` step 2). Each is a draft in Chris's voice from his 10/27 questions; rewrite in your own words before recording. Beats marked *(if time)* are the first cut. The full storyboards (preflight, visuals, sources) are in each `epNN-slug/storyboard.md`.

## ep01-why-gpus-for-ai: 145 words (159 with if-time)

**Titles:** search `Why GPUs for AI? GPU vs CPU Explained` · hook `Your CPU has a few cores. Your GPU has thousands.`

**Question:** "Why does AI run on GPUs and not CPUs?"

**Search phrase:** why gpu for ai

> AI runs on GPUs because a neural network is mostly multiply-adds, and they can all happen at the same time.
>
> Take one layer: y equals x times W. Each output is its own row times column. None of them waits on another.
>
> In BERT, matrix multiplies like this are over 99 percent of the arithmetic.
>
> A CPU is built to run one thread as fast as possible: a few big cores, big caches, smart branching. It works through that pile a few at a time.
>
> A GPU trades per-core speed for count. This grid is the chip: thousands of small cores, all working at once.
>
> *(if time)* Newer GPUs add tensor cores, which do a small matrix multiply in one step.
>
> In PyTorch, that's one line. Move x and W to cuda, and the same at sign runs across the whole grid.
>
> Try it: time one big matmul on the CPU, then on cuda. Call synchronize before you stop the clock.

Storyboard: `ep01-why-gpus-for-ai/storyboard.md`

## ep02-flops-explained: 136 words (153 with if-time)

**Titles:** search `FLOPs Explained: What GPUs Actually Count (AI)` · hook `Every AI chip is rated in one thing. (FLOPs explained)`

**Question:** "FLOP is a floating point operation? What does that mean

**Search phrase:** flops explained

> A FLOP is one multiply or one add, and it's the unit all AI compute is measured in.
>
> Computers store decimals as floating point: scientific notation in binary, a sign, digits and an exponent. The point floats, so one format holds a ten-millionth and three million.
>
> Every weight, activation and gradient is one.
>
> FLOPs, small s, is a count. Training an 8-billion-parameter model on 20,000 tokens costs about 960 trillion FLOPs.
>
> FLOPS, capital S, is per second. A B200 peaks near 2,250 teraflops in bf16. Tera is a trillion.
>
> A transformer's compute is nearly all matrix multiplies, and a matmul is only multiplies and adds. GPUs are built to do exactly that, thousands at once.
>
> *(if time)* Divide a run's FLOPs by the FLOPS you get and you have GPU-hours. GPU-hours are the bill.
>
> Next time you read a GPU spec, find dense FLOPS at the precision you train in. That's your run's real ceiling.

Storyboard: `ep02-flops-explained/storyboard.md`

## ep03-six-flops-per-parameter: 143 words (161 with if-time)

**Titles:** search `How Many FLOPs to Train an LLM? (6 per Parameter, Explained)` · hook `Backprop costs twice the forward pass. Here's why.`

**Question:** "Why is it 6 FLOPs per parameter per token? How much

**Search phrase:** flops llm

> Training an LLM costs six FLOPs per parameter, per token: two forward, four back.
>
> Almost every parameter sits in a weight matrix. Here's a tiny one: three inputs, two outputs, six weights.
>
> Going forward, each weight does one multiply and one add. Two FLOPs per weight, twelve for the layer.
>
> Coming back, the error has to reach the layer before: the same weights in reverse, another multiply and add each.
>
> Then each weight needs its own gradient, for the optimizer. Error times input, added to a running total. Two more.
>
> That's six per weight, per token. Backward costs twice the forward.
>
> So training compute is six, times parameters, times tokens. An 8-billion-parameter model at 20,000 tokens a second is doing 960 teraflops.
>
> *(if time)* At that pace, Llama 3 8B's 15 trillion tokens would keep one B200 busy for about 24 years.
>
> Before your next run, multiply six by parameters by tokens. Divide by what one GPU actually delivers, and that's your GPU-hours.

Storyboard: `ep03-six-flops-per-parameter/storyboard.md`

## ep04-floating-point-precision: 144 words (162 with if-time)

**Titles:** search `bf16 vs fp16 vs fp32 (Explained for Training)` · hook `Half the bits, twice the math (bf16 explained)`

**Question:** "Why does bf16 / fp8 make training faster, and what do fp32,

**Search phrase:** bf16 vs fp16

> bf16 makes training faster because each number is half the bits of fp32. Half the bits, twice the peak math.
>
> A floating-point number has three parts: a sign, an exponent for how big it gets, and a mantissa for how precise.
>
> Fewer bits means more numbers per memory read and more multiply-adds per tensor-core cycle. A B200 peaks near 2,250 teraflops in bf16. fp8 doubles that.
>
> fp16 is also 16 bits, but it spends them on precision, so anything past 65,504 overflows. bf16 keeps fp32's 8 exponent bits: same range, less precision, and training stays stable.
>
> *(if time)* fp8 keeps just three mantissa bits, so training in it needs a scaling library like NVIDIA's Transformer Engine.
>
> One spec-sheet trap: the biggest number is sparse. It's twice dense, and only counts if two of every four weights are zero. Compare dense, in the precision you train in.
>
> In PyTorch, wrap your forward pass in autocast with bf16. You get the faster math without the overflow.

Storyboard: `ep04-floating-point-precision/storyboard.md`

## ep05-tensor-cores-vs-memory: 140 words (150 with if-time)

**Titles:** search `Tensor Cores Explained: Compute-Bound vs Memory-Bound` · hook `Your GPU's fastest part spends most of its time waiting`

**Question:** "Where does the time go inside the GPU? Are the tensor cores

**Search phrase:** tensor cores explained

> Tensor cores are the part of a GPU that does matrix math. They're only as fast as memory can feed them.
>
> Your data lives in GPU memory, HBM. Before any math happens, it flows through cache into the cores.
>
> A B200's tensor cores do about 2,250 teraflops. Memory delivers about 8 terabytes a second.
>
> So each byte you load needs about 280 FLOPs done on it, or the cores sit waiting. That's arithmetic intensity.
>
> A matrix multiply clears that easily. Each number it loads gets used in thousands of multiply-adds. It's compute-bound.
>
> ReLU does one operation per number, four bytes moved, and never touches the tensor cores. That's over a thousand times short. It's memory-bound.
>
> *(if time)* Add, dropout, layernorm: same story. A few operations per number.
>
> When a step is slow, look at the small ops between the matmuls. That's your GPU waiting on memory, and fusing them is the fix.

Storyboard: `ep05-tensor-cores-vs-memory/storyboard.md`

## ep06-cuda-kernel-training-step: 150 words (163 with if-time)

**Titles:** search `What Is a CUDA Kernel? (One PyTorch Training Step)` · hook `Your CPU isn't training your model. It's filling a queue.`

**Question:** "What is a kernel? Why not just say function? And what

**Search phrase:** what is a cuda kernel

> Every op in your PyTorch training step becomes CUDA kernels: functions your CPU hands the GPU to run.
>
> Why not just say function? It doesn't run once. It runs as thousands of threads, each on its own slice of the data, in blocks across the chip.
>
> It returns nothing; it writes to GPU memory. And the CPU doesn't wait: it drops the launch in a queue and moves on.
>
> Watch one step. Forward queues a kernel or more per op: matmul, add, ReLU. Backward queues more. So does the optimizer. The CPU runs ahead while the GPU drains the queue.
>
> Then loss dot item. The CPU needs a number, so it waits until the queue is empty.
>
> And if the next batch isn't ready, the queue runs dry and the GPU sits idle.
>
> *(if time)* Not the Linux kernel, and not a convolution's weights. Same word, different thing.
>
> Call item only on the steps you log. The CPU stays ahead, and the queue stays full.

Storyboard: `ep06-cuda-kernel-training-step/storyboard.md`

## ep07-nvidia-smi: 135 words (151 with if-time)

**Titles:** search `nvidia-smi Explained: What Every Number Means` · hook `nvidia-smi says 100%. One tiny kernel would too.`

**Question:** "What is NVIDIA SMI? I don't know what this means exactly."

**Search phrase:** nvidia smi

> nvidia-smi is your GPU's dashboard. It ships with NVIDIA's driver; type it and you get one row per GPU.
>
> Memory used, out of total: how close you are to out of memory.
>
> *(if time)* Power draw against its cap, and temperature: a quick check the card is working, not idling.
>
> At the bottom, the processes on the GPU. Your training script should be listed.
>
> Then GPU-Util: the share of recent time any kernel was running. Not how much of the chip it used.
>
> One tiny kernel running nonstop reads 100 percent. This 8-billion-parameter run shows 100 and uses 43 percent of the chip's math.
>
> To watch it live, add dash l one, or query just the columns you need as CSV and log them.
>
> PyTorch and Ray's dashboard show this same number.
>
> Use nvidia-smi to check your job is on the GPU, memory has room, and it's never idle. For efficiency, compute MFU.

Storyboard: `ep07-nvidia-smi/storyboard.md`

## ep08-gpu-utilization-vs-mfu: 153 words (160 with if-time)

**Titles:** search `nvidia-smi GPU Utilization vs MFU (Explained)` · hook `Your GPU says 100%. It's lying. (MFU explained)`

**Question:** "MFU vs GPU saturation, what's the difference? How do I know

**Search phrase:** nvidia smi gpu utilization

> nvidia-smi says your GPU is at 100 percent. That only means it's busy. MFU tells you if it's doing useful work.
>
> Utilization is the share of time any kernel ran. One tiny kernel still counts as 100.
>
> That's saturation. When it's low, your data loader is starving the GPU. Fix that first.
>
> A FLOP is one floating-point operation, one multiply or one add. Training costs about six FLOPs per parameter, per token.
>
> MFU, model FLOPs utilization, is the FLOPs your model does each second, divided by what the chip could do.
>
> An 8-billion-parameter model at 20,000 tokens a second does 960 teraflops. A B200 peaks near 2,250. That's 43 percent.
>
> PyTorch's profiler shows the idle gaps. Ray shows the same busy number. Neither gives you MFU; you log it.
>
> *(if time)* For scale: PaLM trained at 46 percent.
>
> Utilization tells you if the GPU is waiting. MFU tells you if the busy time is useful. Log tokens per second and watch MFU.

Storyboard: `ep08-gpu-utilization-vs-mfu/storyboard.md`

## ep09-pytorch-profiler: 148 words (162 with if-time)

**Titles:** search `PyTorch Profiler Tutorial: Find Where Your GPU Sits Idle` · hook `Your GPU is idle between kernels. Here's how to see it.`

**Question:** "How does PyTorch show me where my training step wastes GPU

**Search phrase:** pytorch profiler

> The PyTorch profiler draws your training step as a timeline, and the gaps are where your GPU sits idle.
>
> Wrap a few steps in torch dot profiler. Skip the first couple, so you record real training, not startup.
>
> It writes a trace file; open it in Perfetto. The top rows are the CPU. Below them, the GPU stream: one block per kernel.
>
> A gap in that row is the GPU doing nothing, waiting on the next batch, on Python launching small kernels, or on a sync like loss dot item.
>
> Find the biggest gap first. Look at what the CPU was doing right then; that's what the GPU was waiting for.
>
> Once the gaps are closed, sort the summary table by CUDA time. That's your list of kernels worth making faster.
>
> *(if time)* On Ray Train, the same block goes inside your training function, on each worker.
>
> Profile a few steps, open the trace, and close the biggest gap before you touch the model.

Storyboard: `ep09-pytorch-profiler/storyboard.md`

## ep10-gpu-idle-dataloader: 145 words (160 with if-time)

**Titles:** search `PyTorch DataLoader num_workers: Why GPU Utilization Is Low` · hook `Your GPU isn't slow. It's waiting on your data loader.`

**Question:** "Why is my GPU utilization low during training?"

**Search phrase:** pytorch dataloader num_workers

> If your GPU utilization is low, your GPU isn't slow. It's waiting on your data loader.
>
> It can finish a training step before one Python process has read, decoded and batched the next. Then it sits idle until the batch shows up.
>
> By default, num_workers is zero: batches load in your main process, the same one that queues the GPU's work.
>
> The data loader has workers that you can spin out in parallel. Set num_workers, and that many processes prepare batches while the GPU trains.
>
> Turn on pin_memory, and the copy to the GPU gets faster. Add non_blocking, and Python keeps queueing work while it copies.
>
> Now the next batch is waiting when the step ends, and the gaps close.
>
> *(if time)* prefetch_factor sets how many batches each worker keeps ready. persistent_workers keeps them alive between epochs.
>
> Before you touch the model, loop over the loader alone and time it. If a batch takes longer than a step, fix the loader first.

Storyboard: `ep10-gpu-idle-dataloader/storyboard.md`

## ep11-raising-mfu: 143 words (157 with if-time)

**Titles:** search `torch compile and 3 more ways to raise MFU` · hook `Your training is wasting the GPU (torch compile)`

**Question:** "My GPU is busy but MFU is low. What do I change?"

**Search phrase:** torch compile

> Four changes raise MFU on a busy GPU, tried in this order: bf16, bigger batches, torch compile, CUDA graphs.
>
> First, autocast to bf16. By default, PyTorch runs fp32 matmuls without the tensor cores. In bf16, they run on them.
>
> Second, a bigger batch or longer sequences, as far as memory allows. Each kernel gets more work, so it fills more of the chip.
>
> Third, torch compile. Small elementwise ops, like adds and activations, wait on memory: each one reads its data and writes it back. Compile fuses a chain of them into one kernel, so the data goes through memory once.
>
> Fourth, CUDA graphs, for steps made of many tiny kernels the CPU can't launch fast enough. Reduce-overhead mode records the step once and replays it in one launch.
>
> *(if time)* Your first compiled step is slow; that's the compile. Time the steps after it.
>
> Make one change, re-measure MFU, and keep it only if the number goes up.

Storyboard: `ep11-raising-mfu/storyboard.md`

## ep12-cuda-out-of-memory: 145 words (156 with if-time)

**Titles:** search `CUDA Out of Memory in PyTorch: What's Filling Your GPU` · hook `Your 8B model needs 128 GB before it sees a single token`

**Question:** "Why do I get CUDA out of memory, and what's filling my GPU?"

**Search phrase:** cuda out of memory pytorch

> CUDA out of memory means four things filled your GPU: weights, gradients, optimizer state, and activations. Only activations grow with your batch.
>
> Train an 8-billion-parameter model in mixed precision with Adam. Each parameter costs 16 bytes.
>
> Two for the bf16 weight, two for its gradient, four for an fp32 master copy, eight for Adam's two running averages.
>
> That's 128 gigabytes on a 180 gigabyte B200, before a single activation.
>
> Activations are what the forward pass keeps for the backward pass. They grow with batch size times sequence length, and fill the rest. That's what overflows.
>
> So shrink the micro-batch and use gradient accumulation to keep the same effective batch. Still over? Turn on activation checkpointing: recompute most of them in the backward pass instead of storing them.
>
> *(if time)* Past that, FSDP splits weights, gradients and optimizer state across GPUs.
>
> Next time it crashes, print the peak with max memory allocated, then cut the micro-batch until it fits.

Storyboard: `ep12-cuda-out-of-memory/storyboard.md`

## ep13-multi-gpu-communication: 150 words (167 with if-time)

**Titles:** search `Multi-GPU Training in PyTorch: Why 8 GPUs Aren't 8× Faster (DDP)` · hook `8 GPUs, not 8× faster. Here's where the time goes.`

**Question:** "Why doesn't 8 GPUs give me 8× the speed?"

**Search phrase:** multi gpu training pytorch

> Eight GPUs don't train eight times faster, because every step they have to stop and share their gradients.
>
> In PyTorch DDP, each GPU holds a full copy of the model and trains its own slice of the batch.
>
> Setup is two lines: start NCCL, NVIDIA's library for GPUs talking to each other, and wrap the model.
>
> After backward, each GPU has different gradients. An all-reduce averages them, so every copy takes the same step.
>
> For an 8-billion-parameter model in bf16, that's 16 gigabytes of gradients, every step.
>
> That's communication, not math. If it waits until backward ends, no GPU does model math until it's done, and MFU drops.
>
> DDP overlaps them. It packs gradients into 25-megabyte buckets and sends each one while backward is still computing the rest.
>
> *(if time)* Inside one server that's NVLink. Across servers it crosses the network, at a fraction of the bandwidth.
>
> So profile one step. If a gap shows up after backward, sync less often: bigger batches per GPU, or accumulate with no_sync.

Storyboard: `ep13-multi-gpu-communication/storyboard.md`

