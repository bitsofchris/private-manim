# Beat briefs: 015 ep 1, "Python GIL explained" (v4, the redo on kit v2)

Read first: `agents/beat-brief-hyperframes.md` (the contract), then this
file's "Common" section, then your beat's section. `storyboard.md` holds
the beat table (start, length, VO, visual) and the seam-states table.
The kit is `../_kit/kitchen.js`: read its header comment, the `REST` /
`SEAM1` / `PROTO` block (lines ~60–125) and `draw()` before writing
anything. `00_layout/proto.png` is the approved look: tiles 1–12 are
`SC.PROTO[0..11]`, and the seam states are tiles 1, 4, 6 (≈, cut 0.5),
8, 10, 11, 12.

## Common to every beat

**Setup** (from this episode folder, `videos/015-python-gil/ep01-the-gil/`):

```
mkdir NN_beat
ln -s ../../../_shared/web/vendor NN_beat/vendor
ln -s ../../../_shared/web/iso    NN_beat/iso
ln -s ../../../_shared/web/cast   NN_beat/cast
ln -s ../../_kit                  NN_beat/kit
cp 00_layout/index.html NN_beat/index.html
```

`00_layout/index.html` is the starting file: same `<head>` (script order
`vendor/gsap.min.js`, `iso/iso.js`, `kit/kitchen.js`, `cast/cast.js`),
same `#root`. Change `data-duration` to your `BEAT_SECONDS`, add
`SC.SEAM = SC.SEAM1;` before `SC.mount(root)`, drop `ISO.guides(root)`,
and replace `render(t)`.

**The state model.** `kit.draw(null, S)` draws one full state `S`. Build
every frame from the seam states: `S(0)` is `SC.SEAM1[n-1]`, `S(end)` is
`SC.SEAM1[n]` (n = your beat number), and the last 0.3 s hold `SEAM1[n]`
exactly (`chop: 0`). Between them, `SC.state(SC.SEAM1[k], patch)` for a
keyframe, `SC.tween(A, B, u)` to blend two full states (numbers lerp,
strings and new array entries come from B). `SC.PROTO[k]` are the
approved in-between frames: use them as keyframes where they match
your beat. Fields a beat animates between seams:

- `K.o`, `K.draw` (0..1, the outline draws in; the fill follows, the
  counter and board appear at 1), `K.lab`, `K.half` (0..1, the kitchen
  shrinks to half size at its top-left).
- `cooks[i].in` 0..1: walked in from off-left to the counter spot
  (bobbing). `cooks[i].at` "counter" | "oven" | "appl" with `u` 0..1
  how far it has walked there. `cooks[i].wait` 0..1: fold, dim, flat
  face. `cooks[i].cut` 0..1: how much of its carrot is sliced (the
  carrot shortens, slices pile up); grow it only while that cook holds
  the knife and chops, about 0.1 per stroke, so it reaches the seam
  value exactly.
- `veg` 0..1: the carrots.
- `knife.o`; `knife.holder` −1 (on the board) | integer (held, pivoting on
  the tip) | fractional (between hands, lifted in an arc). `knife.hero`
  stays 1.
- `oven.o`, `appl.o`.
- `slot: { o, top, bottom, hero }`: the top-right label. `SC.SLOT.cooks`
  etc. are the six ready-made values. To swap, fade `o` 1 → 0 over
  0.15 s, change the text, fade back over 0.2 s.
- `chip: { o, text }`: the monospace line inside the kitchen. Same swap
  rule as the slot.
- `panel: { o, title, code, lanes, rows, pulse: { py, io }, core }`:
  `code` 0..4 lines of `Thread(target=chop)` (fractional fades the last);
  `lanes` 0..1 crossfades those lines into the `Thread 1–4` timeline
  rows; `rows[i] = [{ a, b, k }]` bars from `a` to `b` (0..1 of the lane)
  of kind `"py"` (magenta, running Python) | `"io"` (dashed, waiting) |
  `"nat"` (teal, native code), up to 4 per row, grow a bar by moving `b`;
  `pulse.py` / `pulse.io` 0..1 make those bars pulse; `core` 0..1 shows
  `= 1 core` on the title row.
- `ghost.o`: the dashed second kitchen. `close.a`, `close.b`: the two
  close lines.
- `S.chop` 0..1: the holder's stroke (and the appliance's blades).
  `SC.chopAt(t, from, to, rate)` gives a phase that is 0 at both ends
  with ~`rate` strokes per second (use 2): chop between those times only,
  never across the seam. `S.chop` must be 0 at the beat's first and last
  frame.

`SC.io(u)` is ease-in-out, `SC.seg(t, a, b)` is `clamp01((t−a)/(b−a))`,
`SC.pulse(t, at, w)` is one sine bump. Use `SC.lerp`, `SC.clamp01`.

**Cues** are beat-local seconds (master − beat start) from `words.json`;
the per-beat sections below list every word with its time. Name them as
constants with the word in a comment. A thing lands ON its word (ramp
0.15–0.25 s ending at the word), never before it.

**Hero.** The knife and the "py" bars are magenta, and so are the
"knife / GIL" slot and the "= 1 core" tag: all one idea, the GIL.
Nothing else goes magenta. `knife.hero: 1` always.

**Layout.** Captions are anchored bottom: the stage runs y 230–1330, the
caption band y 1330–1536 stays empty, nothing below y 1330. The kit
places everything; you set state, not pixels.

**Check, render, review** (from the episode folder; `ROOT=$(git rev-parse --show-toplevel)`):

```
node "$ROOT"/tools/hf_state_check.js NN_beat FROM TO      # FROM = n-1, TO = n
cd NN_beat && HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx --yes --prefer-offline hyperframes@0.8.115 check
HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
cd .. && "$ROOT"/tools/review_frames.sh --at CUE1,CUE2 media/hf/NN_beat.mp4 4
ffprobe -v error -show_entries format=duration -of csv=p=0 media/hf/NN_beat.mp4
uv run --no-sync --project "$ROOT" python "$ROOT"/tools/seam_check.py beats.json --beat NN_beat   # once a neighbour's render exists; plain python3 lacks PIL
```

Open your contact sheet with the Read tool and look: does each thing
land on its word, is the knife on the board or in a hand (never
floating), is the last frame still. `check` must be 0 errors (a
`rotation_pivot_drift` warning on the knife group is expected). State
check must pass on both cuts. Do not edit `../_kit/` or `videos/_shared/`.
Do not commit. Scratch files go in the session scratchpad under your
agent name.

**Report:** cue constants with words, mp4 path and measured duration,
check summary, state-check result, anything changed from this brief and
why, anything you wished the kit had.

## 01_kitchen (0.000, 7.250 s): SEAM1[0] → SEAM1[1]

VO: "In Python, think of a process as a kitchen. Here, threads are cooks,
and they all share the kitchen's memory."

Words: In@0.42 Python,@0.50 think@1.33 of@1.50 a@1.64 process@1.78 as@2.26
a@2.50 kitchen.@2.66 Here,@3.56 threads@4.22 are@4.48 cooks,@4.60 and@5.72
they@5.78 all@5.86 share@6.02 the@6.22 kitchen's@6.38 memory.@6.74

Frame 0 is SEAM1[0]: the panel with `$ python main.py`, nothing else. The
title is typed: the kit has no typing field, so leave `panel.title` 1
from frame 0 (PROTO[0]) and instead let the panel's box fade in over
0.3 s from 0.0 and the title appear at 0.42 ("In") over 0.1 s. On
"process" (1.78) the panel pulses once: `panel.o` dips to 0.7 and back
over 0.3 s (the box is the process; no text pulse). On "kitchen" (2.66)
the box draws in: `K.o` 1 and `K.draw` 0 → 1 over 0.6 s (2.5 → 3.1) with
`SC.io`, then `K.lab` 0 → 1 over 0.2 s landing at 3.3 (PROTO[1]). On
"threads" (4.22) `panel.code` 0 → 4, one line every 0.2 s (4.22, 4.42,
4.62, 4.82, each a 0.15 s fade). On "cooks" (4.60) the cooks walk in:
`cooks[i].in` 0 → 1 over 0.8 s each, starting 4.60, 4.80, 5.00, 5.20
(cook 1 first, to the far spot; they overlap in time, PROTO[2]);
`slot` = `SC.SLOT.cooks` landing at 4.75. On "share" (6.02) `veg` 0 → 1
over 0.2 s; on "memory" (6.74) swap the slot to `SC.SLOT.counter`.
End state SEAM1[1] (PROTO[3]), still from HOLD = 6.95. No knife, no
chop in this beat.

## 02_knife (7.250, 7.550 s): SEAM1[1] → SEAM1[2]

VO: "The knife is the GIL, the global interpreter lock. Whoever holds the
knife is what runs the Python code while everyone else waits."

Words: The@0.25 knife@0.37 is@0.79 the@0.99 GIL,@1.23 the@1.69 global@1.75
interpreter@2.05 lock.@2.47 Whoever@3.27 holds@3.59 the@4.21 knife@4.41
is@4.73 what@5.01 runs@5.35 the@5.45 Python@5.61 code@5.95 while@6.25
everyone@6.43 else@6.75 waits.@7.03

Opens on SEAM1[1]. On "knife" (0.37) the knife drops onto the board:
`knife.o` 0 → 1 over 0.15 s with `holder: -1` (it is drawn at the
board; to make it a drop, there is no y field, so fade it in; fine). On
"GIL" (1.23) swap the slot to `SC.SLOT.knife` (magenta). On "lock"
(2.47) `panel.lanes` 0 → 1 over 0.4 s (the code lines become the
timeline rows, PROTO[4]). On "holds" (3.59) `knife.holder` −1 → 0: there
is no tween from the board to a hand, so cut it at 3.59 (one frame) and
begin chopping at once: `chop = SC.chopAt(t, 3.59, HOLD, 2)`. From
"runs" (5.35) Thread 1's bar grows: `rows[0] = [{ a: 0, b, k: "py" }]`
with `b` 0 → 0.5 linearly 5.35 → HOLD, and `cooks[0].cut` 0 → 0.5 over
the same span (PROTO[5] is the mid-point). On "everyone else waits"
(6.43, 6.75, 7.03) cooks 2, 3, 4 fold: `cooks[i].wait` 0 → 1 over
0.3 s, one per word. End state SEAM1[2], still from HOLD = 7.25.

## 03_loop (14.800, 7.030 s): SEAM1[2] → SEAM1[3]

VO: "This is why threading a CPU loop makes it no faster. Four threads
with one knife, you have one core's worth of work still."

Words: This@0.26 is@0.44 why@0.54 threading@0.66 a@1.24 CPU@1.38 loop@1.74
makes@2.36 it@2.60 no@2.72 faster.@2.82 Four@3.90 threads@4.04 with@4.40
one@4.54 knife,@4.74 you@5.17 have@5.32 one@5.46 core's@5.74 worth@6.04
of@6.26 work@6.36 still.@6.56

Opens on SEAM1[2]: cook 1 holds the knife, Thread 1's bar at 0–0.5. At
0.0 the bars reset for the staircase: fade `panel.lanes` is NOT the way
(the rows stay); instead shrink Thread 1's bar `b` 0.5 → 0.25 over
0.3 s from 0.0 (it becomes the first stair). From "threading" (0.66) the
knife hops 1 → 2 → 3 → 4: each hop is `knife.holder` i → i+1 over 0.35 s
(`SC.io`), hops starting at 1.00, 2.20, 3.40, so cook 4 holds it by
"knife" (4.74) and keeps it. Between hops the holder chops
(`SC.chopAt` over that holder's span) and its bar grows: Thread 2
`a: 0.25` `b` → 0.5 during 1.35–2.20, Thread 3 `a: 0.5` `b` → 0.75
during 2.55–3.40, Thread 4 `a: 0.75` `b` → 1.0 during 3.75–HOLD; never
two bars growing at once; each holder's `cut` grows 0 → 0.5 over its
span. A cook folds (`wait` → 1 over 0.25 s) as the knife leaves it, and
unfolds (`wait` → 0) as it arrives (PROTO[6] is mid-staircase). On
"one core's" (5.46–5.74) `panel.core` 0 → 1 over 0.2 s landing at 5.74
and `pulse.py` bumps once (`SC.pulse(t, 5.74, 0.5)`). End state
SEAM1[3] (PROTO[7]; `core` is 0 there, so fade `core` out over 0.2 s
ending at HOLD = 6.73). Still from HOLD.

## 04_oven (21.830, 9.940 s): SEAM1[3] → SEAM1[4]

VO: "But a cook puts the knife down to wait on the oven. That could be
an I/O, a request, a file read, a sleep. The GIL is released while the
thread waits, so another thread can run."

Words: But@0.23 a@0.33 cook@0.43 puts@0.75 the@0.93 knife@1.03 down@1.23
to@1.59 wait@1.79 on@2.03 the@2.13 oven.@2.25 That@2.99 could@3.07 be@3.21
an@3.33 I/O,@3.41 a@3.99 request,@4.05 a@4.44 file@4.59 read,@4.89 a@5.27
sleep.@5.37 The@6.13 GIL@6.27 is@6.47 released@6.63 while@6.97 the@7.21
thread@7.41 waits,@7.59 so@8.05 another@8.25 thread@8.63 can@8.89 run.@9.05

Opens on SEAM1[3]: cook 4 holds the knife, the staircase is full. On
"cook" (0.43) the staircase clears: every bar's `b` → its `a` over 0.3 s
(bars shrink to nothing), and the knife hops 4 → 2 over 0.4 s (0.43 →
0.83, `holder` 3 → 1, cook 4 folds, cook 2 unfolds) so cook 2 is the one
who puts it down. On "down" (1.23) `knife.holder` → −1 (the board; cut
it). On "oven" (2.25) `oven.o` 0 → 1 over 0.2 s landing at 2.25, swap the
slot to `SC.SLOT.oven`, and cook 2 walks: `cooks[1].at = "oven"`, `u`
0 → 1 over 0.7 s from 2.25 (`SC.io`), `wait` 0. From "wait" (1.79)
Thread 2's dashed bar grows: `rows[1] = [{ a: 0, b, k: "io" }]`, `b`
0 → 1 linearly 1.79 → HOLD. Chips, each a 0.15 s swap: "request" (4.05)
`requests.get(url)`, "read" (4.89) `open(f).read()`, "sleep" (5.37)
`time.sleep(1)` (PROTO[8] is between the first two). On "released"
(6.63) `knife.holder` → 2 (cut; cook 3 unfolds over 0.25 s ending at
6.63) and cook 3 chops `SC.chopAt(t, 6.63, HOLD, 2)`; from "another
thread" (8.25) Thread 3's bar grows `rows[2] = [{ a: 0.15, b, k: "py" }]`,
`b` 0.15 → 1 linearly 8.25 → HOLD, with `cooks[2].cut` 0.5 → 0.8 over
6.63 → HOLD. End state SEAM1[4] (PROTO[9]), still from HOLD = 9.64.

## 05_appliance (31.770, 4.110 s): SEAM1[4] → SEAM1[5]

VO: "Same for an appliance. Think of NumPy, image decoding, a tokenizer."

Words: Same@0.71 for@0.99 an@1.11 appliance.@1.19 Think@1.77 of@1.89
NumPy,@2.05 image@2.48 decoding,@2.73 a@3.27 tokenizer.@3.37

Opens on SEAM1[4]: cook 3 chopping (keep chopping the whole beat,
`SC.chopAt(t, 0, HOLD, 2)`; `cooks[2].cut` 0.8 → 1.0 over 0 → HOLD).
On "appliance" (1.19) `appl.o` 0 → 1 over 0.2 s landing at 1.19, swap
the slot to `SC.SLOT.appl`, cook 4 unfolds (`wait` → 0 over 0.2 s) and
walks: `cooks[3].at = "appl"`, `u` 0 → 1 over 0.6 s from 1.19. When it
arrives (1.79) Thread 4's teal bar grows: `rows[3] = [{ a: 0.4, b,
k: "nat" }]`, `b` 0.4 → 1 linearly 1.79 → HOLD. Chips, 0.15 s swaps:
"NumPy" (2.05) `np.dot(a, b)`, "decoding" (2.73) `Image.open(f)`,
"tokenizer" (3.37) `tokenizer(text)`. End state SEAM1[5] (PROTO[10]),
still from HOLD = 3.81.

## 06_close (35.880, 10.210 s): SEAM1[5] → SEAM1[6]

VO: "But when threads don't help, ask one thing. Is this thread waiting,
or is it running Python? If it's waiting, then threads work. But if it's
running Python, you need a second kitchen or another process."

Words: But@0.28 when@0.34 threads@0.50 don't@0.80 help,@1.16 ask@1.60
one@1.82 thing.@1.96 Is@2.34 this@2.48 thread@2.73 waiting,@2.94 or@3.54
is@3.62 it@3.74 running@3.80 Python?@4.00 If@4.96 it's@5.06 waiting,@5.20
then@5.62 threads@5.76 work.@6.00 But@6.68 if@6.74 it's@6.82 running@6.92
Python,@7.08 you@7.50 need@7.62 a@7.82 second@7.92 kitchen@8.16 or@8.54
another@8.62 process.@8.82

Opens on SEAM1[5]: cook 3 chopping (chop `SC.chopAt(t, 0, 0.50, 2)`,
then still: the kitchen stops being the subject). On "threads don't
help" (0.50 → 1.16) the kitchen shrinks: `K.half` 0 → 1 over 0.6 s
(`SC.io`), the chip fades out over 0.2 s from 0.50, the slot fades out.
On "waiting" (2.94) `pulse.io` bumps (`SC.pulse(t, 2.94, 0.6)`); on
"running Python" (3.80) `pulse.py` bumps (`SC.pulse(t, 3.80, 0.6)`). On
"threads work" (5.76) `close.a` 0 → 1 over 0.2 s landing at 5.76; on
"running Python" (6.92) `close.b` 0 → 1 landing at 7.08. On "second
kitchen" (7.92) `ghost.o` 0 → 1 over 0.3 s landing at 8.16; on "another
process" (8.62) the slot comes back as `SC.SLOT.twin` landing at 8.82.
End state SEAM1[6] (PROTO[11]), still from HOLD = 9.3 (the VO ends at
9.1; the last frame holds for 0.9 s).
