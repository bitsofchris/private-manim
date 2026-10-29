ENGINE: hyperframes

# Python GIL explained (ep 1 of 2): storyboard v4 (the redo: build the scene up, cut between the kitchen and a Python view, cooks that cut)

Chris, 10/29, on the v3 cut: "the first 20 seconds are the same animation
of a stick figure wagging a knife … build the scene sequentially, go back
and forth between a Python view and the kitchen … the knife looks fat and
ridiculous; they should actively be cutting something." Same VO
(`vo_final.wav`, 46.09 s, same `beats.json`), new picture. Kit:
`../_kit/kitchen.js` (v1 kept as `kitchen_v1.js` until ep 2 is redone).
Approved frames: `00_layout/proto.png` (12 frames, `SC.PROTO`; Chris, 10/29).

THE QUESTION / WHO / THE ANSWER / search phrase / titles: unchanged from
`storyboard_v3.md`.

## What changed

- **Two views on one frame.** The kitchen on top (y 380–900), a Python
  panel below (y 965–1300). The panel starts as a terminal
  (`$ python main.py`), gains one `Thread(target=chop)` line per cook as
  they walk in, then the same four rows become a thread timeline: magenta
  bars = running Python (the knife), dashed = waiting on I/O, teal = native
  code. The kitchen shows what happens; the panel shows what a Python dev
  would see. Emphasis alternates: each beat's new thing appears in the
  kitchen first and its Python name lands in the panel or the chip a word
  later.
- **The scene builds.** Frame 0 is the terminal line alone. The box draws
  in on "kitchen", the cooks walk in on "cooks", the carrots land on the
  board on "memory", the knife drops on "knife", the oven on "oven", the
  appliance on "appliance". Nothing is on screen before its word.
- **The knife.** A chef's knife, tip resting on the cutting board, handle
  in the holder's hand; the handle rocks ~8° (`S.chop`). The carrot under
  the blade shortens and slices pile up left of the tip (`cooks[i].cut`).
- **Labels.** "kitchen / process" top-left stays. One top-right slot shows
  the thing just named (cooks / threads → counter / shared memory →
  knife / GIL → oven / I/O → appliance / native code → second kitchen /
  another process). One code chip inside the kitchen (`requests.get(url)`,
  `open(f).read()`, `time.sleep(1)`, `np.dot(a, b)`, `Image.open(f)`,
  `tokenizer(text)`), each on its word.
- **The close.** The kitchen shrinks to half size, left; the dashed second
  kitchen stands at right; "waiting → threads" and "running Python →
  processes" land in the gap above the panel, which keeps the timeline as
  the evidence.

Traded away: the v3 rule "the thing the title names is on screen at frame
0". The GIL arrives at 7.6 s. Frame 0 is `$ python main.py`.

## Beats (same cuts as `beats.json`; word times in `words.json`)

| # | Folder | Start | Len | VO | Visual |
|---|---|---:|---:|---|---|
| 1 | `01_kitchen` | 0.000 | 7.250 | In Python, think of a process as a kitchen. Here, threads are cooks, and they all share the kitchen's memory. | 0.0 panel with `$ python main.py` typed (0.4–1.3). "process" 1.78: the panel border pulses. "kitchen" 2.66: the box draws in (outline, then the fill, then the counter and board), "kitchen / process" top-left. "threads" 4.22: `Thread(target=chop)` lines 1–4 appear 0.25 s apart; "cooks" 4.60: the four cooks walk in from the left, one per line, slot "cooks / threads". "share" 6.02: the four carrots land on the board; "memory" 6.74: slot "counter / shared memory". |
| 2 | `02_knife` | 7.250 | 7.550 | The knife is the GIL, the global interpreter lock. Whoever holds the knife is what runs the Python code while everyone else waits. | "knife" 7.62: the knife drops onto the board (magenta, the only magenta), "GIL" 8.48: slot "knife / GIL" (magenta); "lock" 9.72: the panel's code lines slide into timeline rows `Thread 1–4`. "holds" 10.84: cook 1 picks it up and chops (slices appear); "runs the Python code" 12.6: Thread 1's magenta bar grows with each chop. "everyone else waits" 13.68–14.28: cooks 2–4 fold arms and dim, one per word. |
| 3 | `03_loop` | 14.800 | 7.030 | This is why threading a CPU loop makes it no faster. Four threads with one knife, you have one core's worth of work still. | "threading" 15.46: the knife hops 1→2→3→4, ~1.3 s each, only the holder chops; each hop ends that thread's bar and starts the next: a staircase, never two bars at once. "one core's worth" 20.26–20.84: a bracket over the whole lane, label `1 core`, pulses once. |
| 4 | `04_oven` | 21.830 | 9.940 | But a cook puts the knife down to wait on the oven. That could be an I/O, a request, a file read, a sleep. The GIL is released while the thread waits, so another thread can run. | "cook" 22.26: the bars clear; "down" 23.06: cook 2 sets the knife on the board; "oven" 24.08: the oven appears at right, cook 2 walks to it, slot "oven / I/O"; Thread 2's bar is dashed from here. "request" 25.88 chip `requests.get(url)`, "file read" 26.42 `open(f).read()`, "sleep" 27.20 `time.sleep(1)`. "released" 28.46: cook 3 takes the knife and chops; "another thread can run" 30.08: Thread 3's magenta bar grows under the dashed Thread 2 bar: two bars at once for the first time. |
| 5 | `05_appliance` | 31.770 | 4.110 | Same for an appliance. Think of NumPy, image decoding, a tokenizer. | "appliance" 32.96: the food processor appears at far left, cook 4 walks to it and runs it (no knife), slot "appliance / native code"; Thread 4 gets a teal bar beside Thread 3's magenta one. Chips: "NumPy" 33.82 `np.dot(a, b)`, "image decoding" 34.25 `Image.open(f)`, "tokenizer" 35.14 `tokenizer(text)`. |
| 6 | `06_close` | 35.880 | 10.210 | But when threads don't help, ask one thing. Is this thread waiting, or is it running Python? If it's waiting, then threads work. But if it's running Python, you need a second kitchen or another process. | "threads don't help" 36.38: the kitchen shrinks to half size, left; the chip fades. "waiting" 38.82: the dashed bar pulses; "running Python" 39.68: the magenta bars pulse. "threads work" 41.64: "waiting → threads" lands; "running Python" 42.80: "running Python → processes" lands. "second kitchen" 44.04: the dashed kitchen draws at right; "another process" 44.50: slot "second kitchen / another process". Still from 45.0. |

## Seam states (`SC.SEAM1[n]` in `../_kit/kitchen.js`; `00_layout/proto.png` tiles 1, 4, 6(≈), 8, 10, 11, 12)

| cut | on screen (both sides draw `SC.SEAM1[n]`, chop 0) |
|---|---|
| 0 (frame 0) | panel with `$ python main.py`; nothing else |
| 1→2 | kitchen box, "kitchen / process", four cooks at the counter (smiling), four carrots, four `Thread(target=chop)` lines, slot "counter / shared memory" |
| 2→3 | timeline rows; knife with cook 1 (cut 0.5), Thread 1 bar 0–0.5; cooks 2–4 folded, dim; slot "knife / GIL" |
| 3→4 | knife with cook 4; staircase Thread 1–4; cooks 1–3 folded; every carrot half cut |
| 4→5 | oven; cook 2 at the oven; knife with cook 3 (cut 0.8); Thread 2 dashed 0–1, Thread 3 magenta 0.15–1; chip `time.sleep(1)`; slot "oven / I/O" |
| 5→6 | + appliance, cook 4 at it; Thread 4 teal 0.4–1; chip `tokenizer(text)`; slot "appliance / native code" |
| end | kitchen at half size left, dashed second kitchen right, slot "second kitchen / another process", both close lines, the timeline from 5→6 |

## Ep 2 (not prototyped yet)

Same kit. The panel shows `multiprocessing.Pool(4)` / `DataLoader(num_workers=4)`
and one row per process; the row of kitchens builds one kitchen per line;
the pickling beat shows the bowl crossing the pipe while a `pickle.dumps`
chip and a grey "copy" bar run in the panel; the fridge beat swaps the bar
for a short `shm` one. Storyboard after ep 1's frames are approved.
