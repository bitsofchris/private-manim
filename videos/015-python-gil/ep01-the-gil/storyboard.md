ENGINE: hyperframes

# Python GIL explained (series ep 1 of 2): storyboard (v1, VO draft for Chris)

THE QUESTION: "What is the Python GIL, and why don't my threads run in parallel?"
WHO IS ASKING: a Python engineer who put a CPU loop on four threads, got
no speedup, and has never read about the interpreter.
THE ANSWER IN ONE SENTENCE: the GIL is one lock per interpreter, so only
the thread holding it runs Python; threads overlap waiting (I/O, native
code), never Python work; for Python work use processes.
THE SEARCH PHRASE: python gil explained (checked 10/25; "python gil" also
autocompletes).

**One idea:** one interpreter, one lock. Whoever holds it runs.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): a box, lanes and a
token that moves. Nothing needs Manim.

Series context: `../SERIES.md` (the two images, search phrases). VO is a
draft in Chris's voice; he edits before recording (runbook step 1).

## VO (draft: 126 words without the *(if time)* beats, 155 with)

| beat | VO | visual |
|---|---|---|
| 01_hook | The Python GIL is one lock per interpreter, and only the thread holding it can run your Python. | Frame 0 already working: the interpreter box, four thread lanes, the magenta lock token sitting in lane 1; lane 1 bright, the other three dim. Top-middle of the stage, ~5 rows. |
| 02_turns | So four threads in one process take turns. They never run your Python at the same time. | The token hops lane 1 → 2 → 3 → 4 on the word "turns" (one move per `S.BEAT`); each lane lights only while it holds the token. |
| 03_cpu | That's why threading a CPU loop makes it no faster. Each thread is waiting for the lock the others hold. | A small code card bottom-middle: `for t in threads: t.start()` over a loop; a timer bar under the box fills at the same rate for one lane or four. The three dim lanes show a clock glyph. |
| 04_waiting | Threads still help when the work is waiting: a network call, a disk read, or C code like NumPy that drops the lock while it runs. One thread waits, another takes the lock. | Lane 2 turns into a "network" lane (a small cloud), lane 3 a NumPy lane; as each starts waiting it releases the token, which jumps to a lane that has Python to run. Timer bar now fills faster. |
| 05_processes | For Python-heavy work, use processes. Each process is its own interpreter with its own lock, so they really run in parallel. | The single box splits into four boxes side by side (the process row), each with its own magenta token; all four bright at once. Hero passes to the row of tokens. |
| 06_boundary *(if time)* | The cost is a boundary: anything that crosses between processes gets copied. | A thick line between two boxes; a small array slides across and a copy appears on the other side. |
| 07_free *(if time)* | Python 3.13 can run free-threaded, without the lock, but that's still the exception. Default Python has it. | The first box briefly shows its lanes all bright with the token gone, then the token returns; a "3.13t" tag fades. |
| 08_close | Next time threads don't help, ask one thing: is the work waiting, or is it running Python? | Final visual: the box on the left ("waiting → threads"), the process row on the right ("Python → processes"). Takeaway only, no outro. |

Line 1 lands the answer in its first clause and says the search phrase.
The thing the title names (the GIL, the lock) is on screen at frame 0.
Beats 06 and 07 are the *(if time)* cuts; 04 and 05 are the contrast that
stops the wrong takeaway ("threads are useless") and stay.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-middle: the interpreter box, 4 lanes, ~5 rows tall.
- Stage bottom-middle: the code card (beat 3) / the timer bar.
- One magenta hero at a time: the lock token; in beat 5 the row of tokens
  as one tight group.
