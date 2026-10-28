# ep01-the-gil: what was said

**Working name:** Every Python dev needs this (Python GIL explained)
**Duration:** vo_raw 50.2 s → vo_final 46.1 s
**Source cut:** from `~/Creating/015-python-gil.m4a` at 4.85–55.10 s, episode announcement removed (`../TRANSCRIPT.md` is the whole take).
**Recorded:** QuickTime raw, 2026-10-28. Cleaned with the default chain (`enhance_vo.sh`, no denoise; floor −69 dB).
**Tighten:** pause cap 0.25 s at −42 dB (auto put the threshold at −51 dB and left the pauses in); no phrase cuts; 50.2 → 46.1 s.
**Planned script:** `storyboard.md` (v3) in this folder.

## As recorded (vo_final.wav, spellings fixed in words.json)

In Python, think of a process as a kitchen. Here, threads are cooks, and they all share the kitchen's memory. The knife is the GIL, the global interpreter lock. Whoever holds the knife is what runs the Python code while everyone else waits. This is why threading a CPU loop makes it no faster. Four threads with one knife, you have one core's worth of work still. But a cook puts the knife down to wait on the oven. That could be an I/O, a request, a file read, a sleep. The GIL is released while the thread waits, so another thread can run. Same for an appliance. Think of NumPy, image decoding, a tokenizer. But when threads don't help, ask one thing. Is this thread waiting, or is it running Python? If it's waiting, then threads work. But if it's running Python, you need a second kitchen or another process.

## Where the take leaves the script

- The hook as recorded opens on the kitchen ("In Python, think of a process as a kitchen"), not on the knife; the GIL arrives at 7.5 s. Kept: it is what was said, and the knife is on screen from frame 0 anyway.
- The appliance beat lost its map-back line ("Native code drops the GIL inside the call, so those threads really overlap"): recorded as "Same for an appliance. Think of NumPy, image decoding, a tokenizer." The visual carries the map-back (label "appliance / native code").
- The *(if time)* "Try it" beat was not recorded.
- Close as recorded: "you need a second kitchen or another process" (the planned "That's the next one" tease was not said).
