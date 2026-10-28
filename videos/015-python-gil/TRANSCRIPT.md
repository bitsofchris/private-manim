# 015 python-gil: the take (2026-10-28, one file, both episodes)

Source: ~/Creating/015-python-gil.m4a (138.1 s, QuickTime raw). Parakeet v3 transcript of the whole file; episode cuts in each epNN/script.md.

00:01.360-00:04.640
Episode one, the Python Gill.

00:04.640-00:08.000
In Python, think of a process as a kitchen

00:08.240-00:12.639
Here, threads are cooks, and they all share the kitchen's memory.

00:12.639-00:15.920
The knife is the gill, the global interpreter lock.

00:15.920-00:20.800
Whoever holds the knife is what runs the Python code while everyone else waits.

00:20.820-00:24.660
This is why threading a CPU loop makes it no faster.

00:24.660-00:28.580
Four threads with one knife, you have one core's worth of work still.

00:28.920-00:31.960
But a cook puts the knife down to wait on the oven.

00:31.960-00:32.840
That could be an I.

00:32.920-00:33.080
O.

00:33.240-00:35.480
, a request, a file read, a sleep.

00:35.480-00:39.160
The gill is released while the thread waits so another thread can run.

00:40.980-00:42.100
Same for an appliance.

00:42.100-00:44.820
Think of NumPy, image decoding, a tokenizer.

00:44.820-00:47.140
But when threads don't help, ask one thing.

00:47.140-00:50.020
Is this thread waiting or is it running Python?

00:49.840-00:51.760
If it's waiting, then threads work.

00:51.760-00:55.360
But if it's running Python, you need a second kitchen or another process.

00:58.559-01:00.000
Episode 2

01:01.500-01:04.300
In Python, you use threads when you're stuck waiting for I.

01:04.379-01:04.540
O.

01:04.780-01:08.060
, or processes when you have more CPU work in Python to do.

01:12.420-01:16.660
The part people often miss is what an additional process actually costs.

01:16.660-01:18.820
Think of a process as a full kitchen

01:18.600-01:25.159
Threads are its cooks, the gill is one knife, threads overlap only while a cook was waiting on the oven, or I.

01:25.240-01:25.320
O.

01:25.479-01:26.440
in this case.

01:26.440-01:29.000
Multiprocessing builds more kitchens.

01:28.660-01:34.580
Each process has its own interpreter and its own GIL, so Python actually runs in parallel.

01:34.580-01:38.340
PyTorch's data loader workers are new processes.

01:38.320-01:42.480
But the cost is that kitchens don't actually share counter space.

01:42.480-01:45.280
Similarly, processes don't share memory.

01:45.280-01:50.479
Every result crossing between processes needs to be pickled, pushed through a pipe, and then unpickled again

01:50.360-01:53.719
For a big array, that copy can cost more than the compute.

01:53.719-01:56.920
The fix here is a shared fridge or shared memory.

01:56.920-02:00.520
You put the big tensor in once and pass a note that says shelf three.

02:00.520-02:04.119
The pipe carries the note, not the actual food.

02:04.220-02:05.660
Think if you're waiting on I.

02:05.740-02:05.900
O.

02:06.060-02:07.100
, use threads.

02:07.100-02:12.460
If you're blocked by Python or CPU intensive work, use more processes.

02:12.460-02:16.380
And if you have big data between processes, be sure to use shared memory.


