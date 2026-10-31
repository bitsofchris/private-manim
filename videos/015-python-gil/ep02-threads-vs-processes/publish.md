# Publish: Multithreading vs multiprocessing python (The Python GIL, part 2 of 2)

Search phrase: **multithreading vs multiprocessing python** (SERIES.md
"Search phrases"; autocompletes, checked 2026-10-25; "…vs asyncio python"
is also offered, so the description names asyncio once). Before
publishing, glance at YouTube's results for it.

Final cut: `media/short.mp4`, 58.5 s.

## Titles

Hook title, for the person scrolling past (recommended, Chris's
preference 10/26; the stake first, the phrase kept for search; 71
characters, the phrase starts at 32, so the feed may cut it after
"multithreading vs"):

```
Most Python devs get this wrong (multithreading vs multiprocessing python)
```

Search title, for the person typing the phrase (54 characters, the phrase
first):

```
Multithreading vs Multiprocessing Python (Made Simple)
```

## Description

```
Multithreading vs multiprocessing python: threads for work that waits, processes for work that runs Python.

A process is a kitchen with one knife (the GIL). Multiprocessing builds more kitchens, each with its own knife, so Python really runs in parallel.
The cost: kitchens don't share counters, processes don't share memory. Every result that crosses is pickled, pushed through a pipe and unpickled, and for a big array that copy can cost more than the compute.
The fix is a shared fridge: shared memory. Put the big tensor in once and pass a note that says shelf 3.

Part 2 of 2 on the Python GIL. Part 1: what the GIL is. (All waiting and no CPU work? That is asyncio's case, not covered here.)
[POST LINK]

Level up human.

#python #multiprocessing #multithreading #programming #Shorts
```

## Substack note

```
If you reached for multiprocessing and it got slower: a process is a second kitchen with its own knife (its own GIL), so Python really runs in parallel. But kitchens don't share counters. Every result that crosses between processes is pickled through a pipe, and for a big array that copy costs more than the compute. Put it in the shared fridge (shared memory) once and pass a note that says shelf 3. 58 seconds.
```

## Checked against the final cut

Reviewed on frame sheets of `media/short.mp4` (58.54 s) 2026-10-31. On
screen: ep 1's two kitchens and the split panel, "waiting → threads" and
"running Python → processes" landing on their words (beat 1); the price
tag on the second kitchen, the first kitchen growing back to full size,
"cooks / threads", "knife / GIL" (beat 2); `multiprocessing.Pool(4)`, the
kitchen shrinking into a 2×2 grid as three more draw in with one cook
each, a magenta knife in every kitchen on "own GIL", four magenta bars
growing together, `num_workers=4` (beat 3); knives going grey, the wall
between kitchens 1 and 2, "wall / separate memory", the bowl crated on
"pickled" under `pickle.dumps(arr)`, through the pipe, unboxed under
`pickle.loads(buf)`, Process 1's grey copy bar growing past its magenta
bar (beat 4); the fridge with shelves 1–3, the bowl dropping onto shelf 3
with the "3" lit, the copy bar shrinking under `SharedMemory(name)`, the
"shelf 3" note crossing the pipe, "a note / not the data" (beat 5); the
panel giving way to "waiting → threads", "running Python → processes",
"big data → shared memory" (beat 6). The description's "its own knife"
is the slot "own knife / own GIL"; "pickled, pushed through a pipe and
unpickled" is beat 4 in that order; asyncio is named only in the
description, not on screen or in the VO.
