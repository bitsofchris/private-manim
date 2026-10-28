# Understanding the GPU: all scripts (VO drafts for Chris)

All 8 VOs in one file, in recording order (`agents/series.md` step 2). Each is a draft in Chris's voice from his 10/27 questions; rewrite in your own words before recording. *(if time)* beats are the first cut. Full storyboards (preflight, visuals, sources) are in each `epNN-slug/storyboard.md`.

## ep01-why-gpus-for-ai: 145 words (159 with if-time)

**Search title:** `Why GPU for AI? Made Simple (Beginner Friendly)` · **Hook title:** `You use it daily. Here's why (why GPU for AI)`

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

**Search title:** `FLOPs Explained Made Simple (Beginner Friendly)` · **Hook title:** `Every AI engineer needs this number (FLOPs explained)`

**Search phrase:** flops explained

> A FLOP is one multiply or one add, and it's the unit all AI compute is measured in.
>
> Computers store decimals as floating point: scientific notation in binary, a sign, digits and an exponent. The point floats, so one format holds a ten-millionth and three million.
>
> Every weight, activation and gradient is one.
>
> FLOPs, small s, is a count. Training an 8-billion-parameter model on 15,000 tokens costs about 720 trillion FLOPs.
>
> FLOPS, capital S, is per second. A B200 peaks near 2,250 teraflops in bf16. Tera is a trillion.
>
> A transformer's compute is nearly all matrix multiplies, and a matmul is only multiplies and adds. GPUs are built to do exactly that, thousands at once.
>
> *(if time)* Divide a run's FLOPs by the FLOPS you get and you have GPU-hours. GPU-hours are the bill.
>
> Next time you read a GPU spec, find dense FLOPS at the precision you train in. That's your run's real ceiling.

Storyboard: `ep02-flops-explained/storyboard.md`

## ep03-six-flops-per-parameter: 145 words (163 with if-time)

**Search title:** `FLOPs LLM Training Made Simple (Beginner Friendly)` · **Hook title:** `You can price any training run (FLOPs LLM)`

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
> So training compute is six, times parameters, times tokens. An 8-billion-parameter model at 15,000 tokens a second per GPU is doing 720 teraflops.
>
> *(if time)* At that pace, Llama 3 8B's 15 trillion tokens would keep one B200 busy for about 32 years.
>
> Before your next run, multiply six by parameters by tokens. Divide by what one GPU actually delivers, and that's your GPU-hours.

Storyboard: `ep03-six-flops-per-parameter/storyboard.md`

## ep04-floating-point-precision: 144 words (162 with if-time)

**Search title:** `bf16 vs fp16 Made Simple (Beginner Friendly)` · **Hook title:** `You use this without knowing why (bf16 vs fp16)`

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

**Search title:** `Tensor Cores Explained (Beginner Friendly)` · **Hook title:** `Your GPU is waiting on memory (tensor cores explained)`

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

**Search title:** `What is a CUDA Kernel? Your code, on the GPU` · **Hook title:** `Your CPU just fills a queue (what is a CUDA kernel)`

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

## ep07-nvidia-smi-utilization-vs-mfu: 149 words (156 with if-time)

**Search title:** `nvidia-smi GPU-Util vs MFU, Made Simple` · **Hook title:** `Your GPU says 100%. It's lying (nvidia-smi)`

**Search phrase:** nvidia smi

> nvidia-smi says your GPU is at 100 percent. That only means it's busy. MFU tells you if it's doing useful work.
>
> It's the monitor that ships with NVIDIA's driver: memory, power, and GPU-Util, per GPU.
>
> GPU-Util is the share of time any kernel was running, not how much of the chip it used. One tiny kernel counts as 100.
>
> That's saturation. If it drops, your data loader is starving the GPU.
>
> MFU, model FLOPs utilization, is the FLOPs your model does each second, divided by what the chip could do.
>
> An 8-billion-parameter model at 15,000 tokens a second per GPU does 720 teraflops. A B200 peaks near 2,250. That's 32 percent.
>
> Ray's dashboard shows the same busy number. Neither gives you MFU; you log it.
>
> *(if time)* For scale: PaLM trained at 46 percent.
>
> Utilization tells you if the GPU is waiting. MFU tells you if the busy time is useful. Log tokens per second and watch MFU.

Storyboard: `ep07-nvidia-smi-utilization-vs-mfu/storyboard.md`

## ep08-pytorch-profiler: 148 words (162 with if-time)

**Search title:** `PyTorch Profiler Made Simple (Beginner Friendly)` · **Hook title:** `Your GPU sits idle. Find where (PyTorch profiler)`

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

Storyboard: `ep08-pytorch-profiler/storyboard.md`

