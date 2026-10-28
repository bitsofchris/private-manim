# ep02-threads-vs-processes: what was said

**Working name:** Most Python devs get this wrong (multithreading vs multiprocessing python)
**Duration:** vo_raw 74.3 s → vo_final 58.5 s
**Source cut:** from `~/Creating/015-python-gil.m4a` at 61.70–136.00 s, episode announcement removed (`../TRANSCRIPT.md` is the whole take).
**Recorded:** QuickTime raw, 2026-10-28. Cleaned with the default chain (`enhance_vo.sh`, no denoise; floor −69 dB).
**Tighten:** pause cap 0.25 s at −42 dB; two phrase cuts (Chris to approve): the 5 s dead air after the hook (clean 6.05–11.05 s) and the recap's second sentence "Threads overlap only while a cook was waiting on the oven, or I/O in this case" (clean 19.40–24.30 s, 5.3 s; the hook already says it); then `atempo=1.03` + loudnorm (runbook step 5.5), 74.3 → 60.3 → 58.5 s.
**Planned script:** `storyboard.md` (v3) in this folder.

## As recorded (vo_final.wav, spellings fixed in words.json)

In Python, you use threads when you're stuck waiting for I/O, or processes when you have more CPU work in Python to do. The part people often miss is what an additional process actually costs. Think of a process as a full kitchen. Threads are its cooks, the GIL is one knife. Multiprocessing builds more kitchens. Each process has its own interpreter and its own GIL, so Python actually runs in parallel. PyTorch's data loader workers are new processes. But the cost is that kitchens don't actually share counter space. Similarly, processes don't share memory. Every result crossing between processes needs to be pickled, pushed through a pipe, and then unpickled again. For a big array, that copy can cost more than the compute. The fix here is a shared fridge or shared memory. You put the big tensor in once and pass a note that says shelf 3. The pipe carries the note, not the actual food. Think if you're waiting on I/O, use threads. If you're blocked by Python or CPU intensive work, use more processes. And if you have big data between processes, be sure to use shared memory.

## Where the take leaves the script

- Hook as recorded: "In Python, you use threads when you're stuck waiting for I/O, or processes when you have more CPU work in Python to do." (the search phrase "multithreading vs multiprocessing" was not said; it goes in the title and description).
- "The part people often miss is what an additional process actually costs" is the stake line; kept, it opens beat 2.
- Recap trimmed to "Think of a process as a full kitchen. Threads are its cooks, the GIL is one knife." (see tighten).
- "PyTorch's data loader workers are new processes" (planned: "are processes").
- The asyncio *(if time)* beat was not recorded.
- Close as recorded has three sentences (waiting → threads; blocked by Python/CPU → processes; big data → shared memory), 10.7 s.
