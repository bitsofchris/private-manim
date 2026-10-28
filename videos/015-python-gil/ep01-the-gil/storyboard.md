ENGINE: hyperframes

# Python GIL explained (series ep 1 of 2): storyboard (v3, kitchen image mapped back to the real terms, VO draft for Chris)

THE QUESTION: "What is the Python GIL, and why don't my threads run in parallel?"
WHO IS ASKING: a Python engineer who put a CPU loop on four threads, got
no speedup, and has never read about the interpreter.
THE ANSWER IN ONE SENTENCE: the GIL is one lock per interpreter, so only
the thread holding it runs Python code; threads overlap while they wait
(I/O, native code), never while they run Python.
THE SEARCH PHRASE: python gil explained (checked 10/25; "python gil" also
autocompletes).

**Titles (runbook step 9, Chris picks):** search `Python GIL Explained (Beginner Friendly)` · hook `Every Python dev needs this (Python GIL explained)` (Chris's preference, 10/26).

**One idea:** one kitchen, one knife. Only the thread holding the GIL runs Python.

**Rule for this script (Chris, 10/27):** every kitchen beat lands on the
real term in the same breath (knife → GIL, oven → I/O, appliance → native
code). On screen, every label shows both: `knife / GIL`.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): a box, line-drawn
cooks from the cast kit (`videos/_shared/web/cast/cast.js`) and a knife
token that moves. Nothing needs Manim.

Series context: `../SERIES.md`. This episode stops at the diagnostic
(waiting vs running Python); processes, their cost and shared memory are
ep 2. Free-threaded Python is cut (opt-in build, not usable for this
audience yet).

## VO (draft: 151 words without the if-time beat, 164 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | The Python GIL is one knife in one kitchen: only the cook holding it can do Python work. | Frame 0 already working: the kitchen (a rounded box, label "kitchen / one process"), four cooks (cast.js line-drawn humans) at a counter, the magenta knife token in cook 1's hand; cook 1 bright, the other three dim. Top-middle of the stage, ~5 rows. |
| 02_map | The kitchen is a process. The cooks are threads; they share the kitchen's memory. The knife is the GIL: whoever holds it runs Python code. Everyone else waits. | Labels land on the words, each with both names: "kitchen / process" on the box, "cooks / threads" over the cooks, "knife / GIL" on the token. On "everyone else waits" the three dim cooks get a clock glyph. |
| 03_loop | That's why threading a CPU loop makes it no faster. Four threads, one knife, one core's worth of work. | A code card bottom-middle: `for t in threads: t.start()`; the token hops cook 1 → 2 → 3 → 4, one hop per `S.BEAT`, only the holder chops; a timer bar under the kitchen fills at the same rate with one cook or four. |
| 04_try *(if time)* | Try it: time the loop on one thread, then on four. Same number. | The code card gains two lines: `1 thread: 4.1s` / `4 threads: 4.2s`. |
| 05_oven | But a cook puts the knife down to wait on the oven. That's I/O: a request, a file read, a sleep. The GIL is released while the thread waits, so another thread runs. | An oven appears right of the counter, label "oven / I/O". Cook 2 walks to it and sets the knife down; the token jumps to cook 3, who chops. Timer bar fills faster. |
| 06_appliance | Same for the appliance: NumPy, image decoding, a tokenizer. Native code drops the GIL inside the call, so those threads really overlap. | A small appliance left of the counter, label "appliance / native code (numpy)". Cook 4 at the appliance with no knife, chopping anyway; the token stays with cook 3. Two cooks visibly working at once. |
| 07_close | So when threads don't help, ask one thing: is the thread waiting, or is it running Python? Waiting, threads work. Running Python, you need a second kitchen. That's the next one. | Final visual: the kitchen with the oven lit ("waiting → threads") on the left; on the right a ghost outline of a second kitchen ("running Python → processes, ep 2"). Takeaway only, no outro. |
Line 1 lands the answer in its first clause and says the search phrase.
The thing the title names (the GIL, the lock) is on screen at frame 0.
Beat 04 is the *(if time)* cut; 05 and 06 are the contrast that stops the
wrong takeaway ("threads are useless") and stay. Beat 07 ends on the
diagnostic and hands the second kitchen to ep 2 in one line.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-middle: the kitchen, four cooks at a counter, oven right,
  appliance left, ~5 rows tall. Every label is `kitchen thing / real thing`.
- Stage bottom-middle: the code card (beats 3–4) / the timer bar.
- One magenta hero at a time: the knife. The ghost second kitchen in beat 7
  is grey, not magenta.

## Final beats (the contract; `vo_final.wav` 46.09 s, master seconds; from `tools/beat_cuts.py`)

Captions are anchored bottom (`assemble.py --captions-anchor bottom`), so the stage runs to y 1330. Cut list: `script.md` (pause cap only, no phrase cuts).

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_kitchen` | 0.000 | 7.250 | In Python, think of a process as a kitchen. Here, threads are cooks, and they all share the kitchen's memory. |
| 2 | `02_knife` | 7.250 | 7.550 | The knife is the GIL, the global interpreter lock. Whoever holds the knife is what runs the Python code while everyone else waits. |
| 3 | `03_loop` | 14.800 | 7.030 | This is why threading a CPU loop makes it no faster. Four threads with one knife, you have one core's worth of work still. |
| 4 | `04_oven` | 21.830 | 9.940 | But a cook puts the knife down to wait on the oven. That could be an I/O, a request, a file read, a sleep. The GIL is released while the thread waits, so another thread can run. |
| 5 | `05_appliance` | 31.770 | 4.110 | Same for an appliance. Think of NumPy, image decoding, a tokenizer. |
| 6 | `06_close` | 35.880 | 10.210 | But when threads don't help, ask one thing. Is this thread waiting, or is it running Python? If it's waiting, then threads work. But if it's running Python, you need a second kitchen or another process. |

## Seam states (`SC.SEAM1[n]` in `../_kit/kitchen.js`; `00_layout/layout.png` shows them, state n at n–n+1 s)

| cut | what is on screen (both sides draw `SC.SEAM1[n]`, chop 0) |
|---|---|
| 0 (frame 0) | kitchen box + "kitchen / process"; four cooks at the counter, cook 1 holds the knife (hero), the others at rest, smiling; no other label |
| 1→2 | + "cooks / threads" |
| 2→3 | + "knife / GIL"; cooks 2–4 waiting (clock, dim, flat face) |
| 3→4 | knife with cook 4 (the hops happened in beat 3); cooks 1–3 waiting; code card `for t in threads: t.start()`; timer bar full |
| 4→5 | oven + "oven / I/O"; cook 2 at the oven (clock); knife with cook 3, chopping; code card gone; timer bar on |
| 5→6 | + appliance + "appliance / native code"; cook 4 at the appliance working without the knife; knife with cook 3 |
| end | same, timer bar gone; "waiting → threads" under the box; ghost second kitchen (dashed) with "second kitchen / another process" and "running Python → processes" above it |
