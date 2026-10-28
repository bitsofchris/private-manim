# The series take, transcribed

Source: `~/Creating/016-gpu-understanding.m4a` (497.6 s, recorded
2026-10-28, eight episodes in script order; "Episode N: working name"
before episodes 2–8, none before episode 1). Parakeet v3 (runbook step 4),
2026-10-28. Chris's own 1-second transcript is `voice-over-transcript.md`.
Where the two disagree, each episode's `script.md` says which it kept.

Episode cuts (seconds into the file, announcement removed). Each was
re-transcribed after cutting: no announcement words, no clipped first or
last word.

| Ep | Folder | Cut | Raw | Pauses capped |
|---|---|---|---|---|
| 1 | `ep01-why-gpus-for-ai` | 0.00–49.45 | 49.5 s | ~44.4 s |
| 2 | `ep02-flops-explained` | 54.10–116.00 | 61.9 s | ~55.8 s |
| 3 | `ep03-six-flops-per-parameter` | 122.15–170.30 | 48.2 s | ~44.0 s |
| 4 | `ep04-floating-point-precision` | 177.62–229.48 | 51.9 s | ~43.2 s |
| 5 | `ep05-tensor-cores-vs-memory` | 236.07–290.40 | 54.3 s | ~47.0 s |
| 6 | `ep06-cuda-kernel-training-step` | 294.47–354.12 | 59.6 s | ~46.5 s |
| 7 | `ep07-nvidia-smi-utilization-vs-mfu` | 363.06–438.71 | 75.6 s | ~62.3 s |
| 8 | `ep08-pytorch-profiler` | 444.40–491.86 | 47.5 s | ~43.1 s |

The take, Parakeet's segments (mishearings left as heard):

00:00.001-00:03.040
A neural network is mostly multiplication and addition.

00:03.040-00:06.320
GPUs allow these to all happen at the same time.

00:06.320-00:13.440
So if you take one layer, y equals x times w, each output is its own row times column.

00:13.240-00:15.000
None of them waits on the other.

00:15.000-00:18.040
GPUs allow this to run in parallel.

00:18.040-00:21.960
Now a CPU is built to run one thread as fast as possible.

00:21.960-00:24.920
A few big cores, some big caches, some smart branching.

00:24.920-00:27.720
It works through that pile a few at a time.

00:27.520-00:31.840
A GPU trades per core speed for count.

00:31.840-00:33.520
This grid is the chip.

00:33.520-00:36.800
Thousands of small cores all working at once.

00:36.720-00:42.400
Newer GPUs add tensor cores, which do a small matrix multiply in one step.

00:42.400-00:44.800
In PyTorch, that's one line.

00:44.800-00:50.160
Move X and W to CUDA, and the same at sign runs the whole grid.

00:51.180-00:53.980
Episode 2, Flops Explained.

00:53.980-00:59.739
A flop is one multiply or one add, and it's the unit that all AI compute is measured in.

00:59.840-01:02.719
Flop stands for floating point operation.

01:02.719-01:09.040
Computers store decimals as a floating point, scientific notation in binary, assign, digits, and an exponent

01:09.040-01:14.720
The point floats, so one format holds a 10 millionth and three millionth.

01:14.720-01:18.400
Every weight, activation, and gradient is one of these numbers.

01:18.960-01:21.520
Flops with a small s is a count.

01:21.520-01:28.080
Training an 8 billion parameter model on 15,000 tokens costs about 720 trillion flops

01:28.820-01:31.140
Flops with a capital S is per second.

01:31.140-01:32.420
This is a rate.

01:32.420-01:37.620
A B200 peaks near 2250 teraflops in BF16.

01:37.620-01:39.300
Tera is a trillion.

01:39.420-01:45.500
A transformers compute is nearly all matrix multiplies, and a mat mollus only multiplies and adds.

01:45.500-01:49.740
GPUs are built to do exactly that, thousands at once.

01:49.880-01:52.520
Divider runs flops by the flops.

01:52.520-01:55.000
You get and you have GPU hours.

01:55.000-01:56.200
This is the bill.

01:58.800-02:02.000
Episode 3, 6 flops for parameter.

02:02.000-02:06.320
Training in LLM costs about 6 flops per parameter per token.

02:06.320-02:10.560
You spend 2 flops on the forward pass and about 4 on the backward pass.

02:11.580-02:14.220
Almost every parameter sits in a weight matrix.

02:14.220-02:15.180
Here's a tiny one.

02:15.180-02:17.340
Three inputs, two outputs, six weights.

02:17.340-02:20.700
Going forward, each weight does one multiply in one add.

02:20.600-02:23.800
So you have two flops for weight, 12 for this entire layer.

02:23.800-02:26.760
Coming backwards now the error has to reach the layer before.

02:26.760-02:30.440
So the same weights in reverse, another multiply and add each.

02:30.340-02:33.700
Then each weight needs its own gradient for the optimizer.

02:33.700-02:37.140
Error times input added to a running total is two more.

02:37.140-02:39.220
That's six per weight per token

02:40.240-02:44.400
So training compute is six times parameters times tokens.

02:44.400-02:51.360
An 8 billion parameter model at 15,000 tokens per second per GPU is doing 720 teraflops.

02:51.360-02:52.880
Episode 4.

02:55.760-02:57.760
Floating time precision.

02:57.760-03:03.600
BF sixteen makes training faster because each number is half the bits of FP32.

03:03.300-03:08.740
Fewer bits means more numbers per memory red and more multiply adds per tensor core cycle.

03:08.740-03:12.980
A B200 peaks near 2250 teraflops in BF16.

03:12.980-03:14.580
FP8 doubles that

03:15.160-03:20.120
FP16 is also 16 bits, but it spends them on precision.

03:20.120-03:24.520
So anything past 65,504 will overflow.

03:24.879-03:28.720
BF sixteen keeps FP thirty two's eight exponent bits.

03:28.720-03:32.239
Same range, less precision, and training stays stable.

03:32.239-03:39.360
FP eight keeps just three bits, so training in it needs a scaling library like NVIDIA's Transformer Engine.

03:43.379-03:47.299
In PyTorch, wrap your forward pass in autocast with BF16.

03:47.299-03:50.180
You get faster math without the overflow.

03:51.519-03:55.920
Episode 5, Tensor Cores versus Memory.

03:55.920-03:59.200
Tensor Cores are the part of a GPU that does matrix math.

03:59.200-04:02.000
They're only as fast as memory can feed them.

04:02.040-04:04.440
Your data lives in GPU memory.

04:04.440-04:08.120
Before any math happens, it flows through cache into the cores.

04:08.120-04:12.280
A B200's tensor cores do about 2250 teraflops.

04:12.280-04:15.560
Memory delivers about 8 terabytes a second.

04:15.460-04:22.820
So each byte you load needs about 280 flops done on it or the cores will sit waiting.

04:22.820-04:25.620
A matrix multiply can clear that easily.

04:25.360-04:29.200
Each number it loads gets used in thousands of multiply and ads.

04:29.200-04:30.560
It's compute bound.

04:30.560-04:35.840
RELU does one operation per number, four bytes moved, and never touches the tensor course.

04:35.840-04:37.760
That's over a thousand times short.

04:37.760-04:40.160
It's memory bound.

04:39.840-04:42.720
At dropout layer norm and is a similar story.

04:42.720-04:44.720
A few operations per number.

04:44.720-04:48.720
When a step is slow, look at the small operations between the matmals.

04:48.720-04:50.560
That's your GPU waiting on memory.

04:50.560-04:51.840
Episode six.

04:52.120-04:54.199
CUDA kernel training.

04:54.199-04:57.800
Every op in your PyTorch training set becomes CUDA kernels.

04:57.800-05:00.919
Functions your CPU hands the GPU to run.

05:04.440-05:06.920
Now we call these kernels because they don't run just once.

05:06.920-05:12.840
They run thousands of threads, each on its own slice of the data in blocks across the GPU chip.

05:12.620-05:16.780
It returns nothing, it writes the GPU memory, and the CPU doesn't wait.

05:16.780-05:19.259
It drops the launch in a queue and moves on.

05:19.259-05:20.620
Watch one step.

05:21.020-05:24.620
Forward cues a kernel or more per op.

05:24.620-05:27.420
Forward cues up a kernel or more per op.

05:27.420-05:30.860
Mat mole, ad, relu, backward then cues more.

05:30.800-05:32.560
So does the optimizer.

05:32.560-05:37.039
The CPU runs ahead while the GPU trains the queue.

05:37.039-05:37.919
Then lost.

05:38.080-05:41.919
item, the CPU needs a number, so it waits until the queue is empty.

05:41.500-05:45.820
And if the next batch isn't ready, the queue runs dry and the GPU sits idle.

05:49.500-05:51.980
Call item only on the steps you log.

05:51.980-05:54.380
The CPU stays ahead and the queue stays full.

05:55.780-06:02.979
Episode 7, GPU utilization versus MFU.

06:02.979-06:07.940
GPU saturation can stay at 100%, but that only means your GPU is busy.

06:08.000-06:15.360
MFU tells you if it's doing useful work.

06:15.360-06:20.000
GPU utilization manages the share of time any kernel was running.

06:20.000-06:22.560
A kernel is a single operation.

06:22.680-06:24.840
The GPU could be doing.

06:24.840-06:30.760
GPU utilization is the share of time any kernel was running, not how much of the chip it used.

06:30.760-06:33.800
One tiny kernel function can count as 100%.

06:36.100-06:40.500
If saturation drops though, your data loader is likely starving the GPU.

06:40.500-06:45.460
But model flops utilization or MFU is the flops your model does each second.

06:45.000-06:50.440
This is the number of floating point operations divided by what the chip could actually do.

06:50.440-06:56.920
An 8 billion parameter model at 15,000 tokens a second per GPU does 720 teraflops.

06:57.039-07:02.319
A B200 peaks near 2250, so that's about 32% utilization.

07:02.319-07:08.000
Dashboards like OnRay will show you the busy number, GPU utilization, not MFU.

07:08.000-07:10.240
You need to log this yourself.

07:10.580-07:13.140
Utilization tells you if the GPU is waiting.

07:13.140-07:15.780
MFU tells you if the busy time is useful.

07:15.780-07:19.060
So log the tokens per second and watch the MFU.

07:21.280-07:21.840
8.

07:21.840-07:22.560
Episode 8.

07:22.560-07:24.160
PyTorch Profiler.

07:24.160-07:30.160
The PyTorch Profiler draws your training step as a timeline, and the gaps are where your GPU sits idle.

07:30.039-07:31.560
Wrap a few steps in torch.

07:31.720-07:35.479
profiler, skip the first couple so you record real training, not startup.

07:35.479-07:37.240
It writes a trace file.

07:37.240-07:42.520
The top rows are the CPU, below them the GPU stream, one block per kernel.

07:42.000-07:45.840
A gap in that row is the GPU doing nothing, waiting on the next batch.

07:45.840-07:48.960
On Python launching small kernels or a sync-like loss.

07:49.120-07:49.840
item.

07:49.840-07:53.840
Find the biggest gap first, look at what the CPU is doing right.

07:53.840-07:54.240
Then

07:54.940-07:57.660
What was the GPU waiting for?

07:57.660-08:01.340
Once the gaps are closed, sort the summary table by CUDA time.

08:01.340-08:03.820
That's your list of kernels worth making faster

08:03.860-08:07.700
On Ray Train, the same block goes inside your training function on each worker.

08:07.700-08:12.180
Profile a few steps, open the trace, and close the biggest gap before you touch the model.


