# Publish: Python GIL explained (The Python GIL, part 1 of 2)

Search phrase: **python gil explained** (SERIES.md "Search phrases";
autocompletes, checked 2026-10-25). Before publishing, glance at YouTube's
results for it.

Final cut: `media/short.mp4`, 46.1 s.

## Titles

Hook title, for the person scrolling past (recommended: a scroller rolls
right past "GIL"; the stake first, the phrase kept for search; 50
characters, the phrase starts at 28):

```
Every Python dev needs this (Python GIL explained)
```

Search title, for the person typing the phrase (40 characters, the phrase
first):

```
Python GIL Explained (Beginner Friendly)
```

## Description

```
Python GIL explained: one lock per process, so only the thread holding it runs Python code at a time.

A process is a kitchen, threads are cooks, the knife is the GIL. Whoever holds the knife runs Python; the rest wait, so threading a CPU loop is no faster.
A cook puts the knife down to wait on the oven (a request, a file read, a sleep) and another cook runs meanwhile. Same for an appliance: NumPy, image decoding, a tokenizer.
When threads don't help, ask one thing: is the thread waiting, or running Python? Waiting → threads. Running Python → a second kitchen, another process.

Part 1 of 2 on the Python GIL. Next: threads vs processes, and what a process costs.
[POST LINK]

Level up human.

#python #gil #multithreading #programming #Shorts
```

## Substack note

```
If you added threads to a Python loop and it got no faster: a process is a kitchen, threads are cooks, and there is one knife (the GIL). Only the cook holding it runs Python; the rest wait. Cooks hand it over to wait on the oven (I/O) or run an appliance (NumPy), so threads help when a thread is waiting, never when it is running Python. 46 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (46.09 s) 2026-10-31. On
screen: `$ python main.py`, the kitchen box drawing in, four cooks walking
in with four `Thread(target=chop)` lines, carrots on the board (beat 1);
the knife landing, the code lines becoming a thread timeline, cook 1
slicing while Thread 1's magenta bar grows, the other three folded (beat
2); the knife hopping cook to cook, the staircase of bars, `= 1 core` on
the title row (beat 3); the oven, cook 2 at it with Thread 2 dashed, the
chips `requests.get(url)` / `open(f).read()` / `time.sleep(1)`, cook 3
chopping meanwhile, then the oven dinging and cook 2 getting the knife
back, Thread 2 magenta again (beat 4); the food processor with cook 4 at
it, Thread 4 teal, chips `np.dot(a, b)` / `Image.open(f)` /
`tokenizer(text)` (beat 5); the bars pulsing on "waiting" and "running
Python", the two close lines, the kitchen shrinking and a second kitchen
filling with four cooks and running, the panel split into `process 1` /
`process 2` (beat 6). The description's "one lock per process" is the
label "kitchen / process" plus one knife; the VO says "the global
interpreter lock". "At a time" is the staircase (never two magenta bars
in one kitchen). Free-threaded Python is not mentioned anywhere.
