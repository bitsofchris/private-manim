ENGINE: hyperframes

# Python GIL explained (series ep 1 of 2): storyboard (v2, kitchen image, VO draft for Chris)

THE QUESTION: "What is the Python GIL, and why don't my threads run in parallel?"
WHO IS ASKING: a Python engineer who put a CPU loop on four threads, got
no speedup, and has never read about the interpreter.
THE ANSWER IN ONE SENTENCE: the GIL is one lock per interpreter, so only
the thread holding it runs Python; threads overlap waiting (I/O, native
code), never Python work; for Python work use processes.
THE SEARCH PHRASE: python gil explained (checked 10/25; "python gil" also
autocompletes).

**Titles (runbook step 9, Chris picks):** search `Python GIL Explained (Beginner Friendly)` · hook `Every Python dev needs this (Python GIL explained)` (Chris's preference, 10/26).

**One idea:** one kitchen, one knife. Only the cook holding it does Python work.

**Engine:** HyperFrames (`AGENTS.md` "Which engine"): a box, line-drawn
cooks from the cast kit (`videos/_shared/web/cast/cast.js`) and a knife
token that moves. Nothing needs Manim.

Series context: `../SERIES.md` (the two images, search phrases). VO is a
draft in Chris's voice; he edits before recording (runbook step 1).

## VO (draft: 130 words without the two if-time beats, 167 with; the kitchen-and-knife image from Chris's chat, 10/26)

| beat | VO | visual |
|---|---|---|
| 01_hook | The Python GIL is one knife in one kitchen: only the cook holding it can do Python work. | Frame 0 already working: the kitchen (a rounded box, label "one process"), four cooks (cast.js line-drawn humans) at a counter, the magenta knife token in cook 1's hand; cook 1 bright, the other three dim. Top-middle of the stage, ~5 rows. |
| 02_cooks | The kitchen is a process. The cooks are threads. Ten cooks, one knife, one cook chopping at a time. | Labels land on the words: "process" on the box, "threads" over the cooks. On "one knife" the token hops cook 1 → 2 → 3 → 4, one hop per `S.BEAT`; only the holder chops (a small chop motion). |
| 03_loop | That's why threading a Python loop makes it no faster. The other cooks just stand there waiting for the knife. | A code card bottom-middle: `for t in threads: t.start()`; a timer bar under the kitchen fills at the same rate with one cook or four. The three dim cooks get a clock glyph. |
| 04_down | Cooks put the knife down when they wait for the oven, that's disk or the network, or when they use an appliance that doesn't need it: NumPy, image decoding, a tokenizer. While one cook waits, another chops. | An oven appears right of the counter, a small appliance (labelled "numpy") left. Cook 2 walks to the oven and sets the knife down; the token jumps to cook 3, who chops. Timer bar fills faster. |
| 05_kitchens | Want two cooks chopping at once? Build a second kitchen. That's a process: its own interpreter, its own knife. | The box duplicates into a row of four kitchens, each with one cook and its own magenta knife; all four chop at once. Hero passes to the row of knives as one group. |
| 06_containers *(if time)* | But kitchens don't share counters. Passing food between them means packing it into a container, sending it through a pipe, unpacking it. | A thick wall between two kitchens; a bowl gets boxed (label "pickle"), slides through a pipe, is unboxed on the far side. |
| 07_free *(if time)* | Free-threaded Python takes the knife away, so every cook can chop. It's still the exception. | The first kitchen briefly shows all four cooks chopping with no token; a "3.13t" tag fades; the token returns. |
| 08_close | So when threads don't help, ask one thing: is the cook waiting, or is the cook chopping? | Final visual: the kitchen on the left ("waiting → threads"), the row of kitchens on the right ("chopping → processes"). Takeaway only, no outro. |
Line 1 lands the answer in its first clause and says the search phrase.
The thing the title names (the GIL, the lock) is on screen at frame 0.
Beats 06 and 07 are the *(if time)* cuts; 04 and 05 are the contrast that
stops the wrong takeaway ("threads are useless") and stay.

## Layout (decided before any code)

- Top band: nothing (captions burn in below; safe areas from `style.py`).
- Stage top-middle: the kitchen, four cooks at a counter, oven right,
  appliance left, ~5 rows tall.
- Stage bottom-middle: the code card (beat 3) / the timer bar.
- One magenta hero at a time: the knife; in beat 5 the row of knives as
  one tight group.
