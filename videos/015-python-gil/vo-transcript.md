# 015-python-gil

[00:00:00] [00:00:01] [00:00:02] Episode one, The [00:00:03] Python GIL [00:00:04] [00:00:05] In Python, [00:00:06] think of a process [00:00:07] as a kitchen. [00:00:08] Here, [00:00:09] threads are [00:00:10] cooks, and they all [00:00:11] share the kitchen's [00:00:12] memory. The [00:00:13] knife is the [00:00:14] GIL, the Global [00:00:15] Interpreter Lock. [00:00:16] Whoever holds [00:00:17] the knife is what [00:00:18] runs the Python code [00:00:19] while everyone else [00:00:20] waits. [00:00:21] This is why [00:00:22] threading a CPU [00:00:23] loop makes it no [00:00:24] faster.

[00:00:24] [00:00:25] Four threads with one [00:00:26] knife, you have one [00:00:27] core's worth of work [00:00:28] [00:00:29] still.

[00:00:29] But a cook puts [00:00:30] the knife down to [00:00:31] wait on the oven. [00:00:32] That could be an [00:00:33] IO, a request, a [00:00:34] file read, a [00:00:35] sleep. The gill [00:00:36] is released while the [00:00:37] thread waits, so [00:00:38] another thread can run [00:00:39] [00:00:40] [00:00:41] Same for an [00:00:42] appliance. Think of NumPy, [00:00:43] image decoding, a [00:00:44] tokenizer. [00:00:45] But when threads don't [00:00:46] help, ask one [00:00:47] thing, is this thread [00:00:48] waiting or is it running [00:00:49] Python?[00:00:50]

[00:00:50] If it's waiting, then [00:00:51] threads work. [00:00:52] But if it's running Python, [00:00:53] you need a second kitchen or [00:00:54] another process[00:00:55] [00:00:56] [00:00:57] [00:00:58]

[00:00:58] [00:00:59] Episode two. [00:01:00] [00:01:01] In [00:01:02] Python, you use [00:01:03] threads when you're stuck waiting [00:01:04] for IO [00:01:05] or processes when you have [00:01:06] more CPU work in [00:01:07] Python to [00:01:08] [00:01:09] [00:01:10] [00:01:11] [00:01:12] do

[00:01:12] the [00:01:13] part people often miss [00:01:14] is what an additional [00:01:15] process actually costs. [00:01:16] [00:01:17] Think of a process as a [00:01:18] full kitchen. [00:01:19] Threads are its cooks, [00:01:20] the GIL is one [00:01:21] knife. Threads [00:01:22] overlap only [00:01:23] while a cook was [00:01:24] waiting on the oven, or [00:01:25] I/O in this case. [00:01:26] [00:01:27] Multiprocessing builds more [00:01:28] kitchens.

[00:01:28] [00:01:29] Each process has [00:01:30] its own interpreter [00:01:31] and its own GIL, [00:01:32] so Python [00:01:33] actually runs in [00:01:34] parallel. [00:01:35] PyTorch's data loader [00:01:36] workers are [00:01:37] new [00:01:38] processes. But the [00:01:39] cost is that [00:01:40] kitchens don't [00:01:41] actually share counter [00:01:42] space.

[00:01:42] [00:01:43] Similarly, processes [00:01:44] don't share memory. [00:01:45] Every [00:01:46] result crossing between [00:01:47] processes needs to be [00:01:48] pickled, pushed through a pipe, [00:01:49] and then unpickled again. [00:01:50] For a [00:01:51] big array, that copy can [00:01:52] cost more than the [00:01:53] compute. [00:01:54] The fix here is a [00:01:55] shared fridge or [00:01:56] shared memory. [00:01:57] You put the big [00:01:58] tensor in once and [00:01:59] pass a note that says, "Shelf [00:02:00] three."

[00:02:00] The [00:02:01] pipe carries the [00:02:02] note, not the [00:02:03] actual [00:02:04] food. Think if you're [00:02:05] waiting on IO, [00:02:06] use threads. [00:02:07] If you're blocked by [00:02:08] Python or [00:02:09] CPU-intensive work, use more [00:02:10] processes.[00:02:11] [00:02:12]

[00:02:12] And if you have [00:02:13] big data between [00:02:14] processes, be sure [00:02:15] to use shared [00:02:16] [00:02:17] [00:02:18] memory

