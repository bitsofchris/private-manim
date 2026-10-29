# Beat briefs: 015 ep 2, "Multithreading vs multiprocessing in Python"

Read first: `agents/beat-brief-hyperframes.md` (the contract), then this
file's "Common" section, then your beat's section. `storyboard.md` holds
the Final beats table (start, length, VO) and the seam-states table.
The kit is `../_kit/kitchen.js`: read its header comment and the
`REST` / `EP2_KITCHEN` / `EP2_ROWBIG` / `SEAM2` block (lines ~60–110)
before writing anything.

## Common to every beat

**Setup** (from this episode folder, `videos/015-python-gil/ep02-threads-vs-processes/`):

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
same `#root`. Change `data-duration` to your `BEAT_SECONDS`, keep
`SC.SEAM = SC.SEAM2;` before `SC.mount(root)`, drop `ISO.guides(root)`,
and replace `render(t)`.

**The state model.** `kit.draw(null, S)` draws one full state `S`. Build
every frame from the seam states: `S(0)` is `SC.SEAM2[n-1]`, `S(end)` is
`SC.SEAM2[n]` (n = your beat number), and the last 0.3 s hold `SEAM2[n]`
exactly (`chop: 0`). Between them, `SC.state(base, patch)` for a keyframe
(`base` may be `SC.SEAM2[k]`, `SC.EP2_KITCHEN`-style objects are not
exported: start from a seam state), `SC.tween(A, B, u)` to blend two
full states (numbers lerp, strings come from B). Fields a beat may
animate between seams:

- `knife.holder` fractional: the knife between two cooks' hands, in an
  arc. `cooks[i].u` (default 1): the walk from the counter spot to
  `cooks[i].at`. `cooks[i].wait` fractional.
- `S.chop` 0..1: chop phase of the knife holder (one kitchen) and, times
  `row.chop`, of every row cook. `sin(π·chop)` is the swing, so chop runs
  0 → 1 per stroke, a stroke every 0.5 s, and is 0 at the seam.
- `row.big` 0..1: the row of four kitchens interpolates from its small
  home (bottom zone, y 1050–1300) to its big home (the kitchen box's
  place, y 420–860). `row.hero` makes the four knives magenta (one
  group). `row.lab` is "kitchens / processes".
- `K.o` fades the one kitchen and all its labels together.
- `tag.o`: the price tag on the row (small home only).
- `wall.o` the wall + pipe between kitchens 2 and 3 of the big row;
  `wall.lab` its label; `wall.bowl` 0..1 moves the bowl from kitchen 2's
  counter, through the pipe, to kitchen 3's counter (`pipePath`);
  `wall.boxed` 0..1 draws the pickle box around the bowl; `wall.bowlO`
  the bowl's opacity.
- `fridge.o`, `fridge.lab`, `fridge.bowl` (the bowl on shelf 3),
  `fridge.note` 0..1 moves the note "shelf 3" along the same pipe path,
  `fridge.noteO`, `fridge.noteHero` (magenta note, and the "3" goes
  magenta whenever `note > 0`).
- `timer.o`, `timer.fill`: the "work done" bar in the bottom zone.
- `close.o`: "waiting → threads" under the kitchen and "running Python →
  processes" above the small row (the second is shown only while the row
  is small or the ghost is on).
- Every `o` / `lab` / `fill` field is a 0..1 opacity or amount: ramp over
  ~0.2 s to land on a word.

`SC.io(u)` is ease-in-out, `SC.seg(t, a, b)` is `clamp01((t−a)/(b−a))`.
Use `SC.lerp`, `SC.clamp01`.

**Cues** are beat-local seconds (master − beat start) from `words.json`;
the per-beat sections below list every word with its time. Name them as
constants with the word in a comment. Check a cue that carries a move on
the RMS envelope of `vo_final.wav` if it looks off.

**Hero.** One magenta thing at a time: the single kitchen's knife
(beats 1–2), then the row of four knives as one group (beat 3 and the
close), then the note "shelf 3" (beat 5). While the note is the hero the
row knives are ink (`row.hero: 0`). The seam states already encode this.

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
```

Open your contact sheet with the Read tool and look. `check` must be 0
errors (1 "file too large" warning is normal). State check must pass on
both cuts. Do not edit `../_kit/` or `videos/_shared/`. Do not commit.
Scratch files go in the session scratchpad under your agent name.

**Report:** cue constants with words, mp4 path and measured duration,
check summary, state-check result, anything changed from this brief and
why, anything you wished the kit had.

## 01_hook (0.000, 6.160 s): SEAM2[0] → SEAM2[1]

VO: "In Python, you use threads when you're stuck waiting for I/O, or
processes when you have more CPU work in Python to do."

Words: In@0.39 Python,@0.46 you@0.98 use@1.04 threads@1.20 when@1.56
you're@1.72 stuck@1.86 waiting@2.08 for@2.34 I/O,@2.54 or@3.36
processes@3.42 when@3.92 you@4.18 have@4.26 more@4.36 CPU@4.50 work@4.88
in@5.20 Python@5.28 to@5.62 do.@5.86

Frame 0 is SEAM2[0]: ep 1's close with the small row real (the kitchen
with every label, cook 2 at the oven, cook 4 at the appliance, the knife
with cook 3; "waiting → threads"; the small row of four kitchens with
"running Python → processes" above it). Hook: something already moves at
frame 0: cook 3 chops and the four row cooks chop (`row.chop: 1`, the
seam has it) from t = 0 to the hold. On "threads" (1.20) the "cooks /
threads" label pulses (`cooksLab` 0.5 and back over 0.3 s); on "waiting"
(2.08) the oven label pulses; on "I/O" nothing more. On "processes"
(3.42) the small row pulses as a group: `row.o` 0.6 and back over 0.3 s.
On "CPU work in Python" (4.50–5.28) the knife label pulses. SEAM2[1] =
SEAM2[0]; chop 0 from HOLD = 5.86.

## 02_recap (6.160, 7.890 s): SEAM2[1] → SEAM2[2]

VO: "The part people often miss is what an additional process actually
costs. Think of a process as a full kitchen. Threads are its cooks, the
GIL is one knife."

Words: The@0.20 part@0.26 people@0.55 often@0.74 miss@1.02 is@1.22
what@1.34 an@1.50 additional@1.62 process@2.00 actually@2.42 costs.@2.74
Think@3.62 of@3.74 a@3.84 process@3.94 as@4.28 a@4.42 full@4.50
kitchen.@4.70 Threads@5.54 are@5.74 its@5.80 cooks,@5.98 the@6.60 GIL@6.72
is@6.86 one@6.98 knife.@7.16

Opens on SEAM2[1] (cook 3 and the row cooks chopping carry on). On
"costs" (2.74) the price tag grows in on the row: `tag.o` 0 → 1 over 0.25 s
(this is the stake of the episode; it is the only new element). On
"process as a full kitchen" (3.94–4.70) the "kitchen / process" label
pulses; on "cooks" (5.98) "cooks / threads" pulses; on "knife" (7.16) the
knife label pulses (a pulse: the label's `lab` to 0.5 and back over
0.3 s). The pulse on "knife" at 7.16 must be done by HOLD = 7.59, so make
it 0.3 s. End state SEAM2[2] = SEAM2[1] + `tag.o: 1`, chop 0 from HOLD.

## 03_processes (14.050, 10.470 s): SEAM2[2] → SEAM2[3]

VO: "Multiprocessing builds more kitchens. Each process has its own
interpreter and its own GIL, so Python actually runs in parallel.
PyTorch's data loader workers are new processes."

Words: Multiprocessing@0.41 builds@0.89 more@1.17 kitchens.@1.37
Each@2.31 process@2.55 has@3.07 its@3.33 own@3.47 interpreter@3.69
and@4.11 its@4.39 own@4.55 GIL,@4.81 so@5.41 Python@5.47 actually@5.89
runs@6.39 in@6.69 parallel.@6.85 PyTorch's@7.77 data@8.25 loader@8.43
workers@8.69 are@8.95 new@9.43 processes.@9.65

The big move of the episode. Opens on SEAM2[2] (kitchen on top, small row
with price tag below). On "builds more kitchens" (0.89–1.37): the price
tag fades (`tag.o` → 0 over 0.2 s at 0.89), the close lines fade
(`close.o` → 0), the one kitchen fades (`K.o` 1 → 0 over 0.5 s from 0.89,
which takes all its labels with it), and the row rises and grows into
the kitchen's place: `row.big` 0 → 1 with `SC.io` over 0.9 s from 0.89
(a move the viewer tracks). On "kitchens" (1.37) the row label
"kitchens / processes" ramps in (`row.lab`). On "its own GIL" (4.55–4.81)
the four knives go magenta as one group: `row.hero` 0 → 1 over 0.2 s at
4.81. From "runs in parallel" (6.39) all four row cooks chop (`row.chop`
1, chop strokes every 0.5 s) to the hold. On "data loader" (8.25) the
code card `DataLoader(ds, num_workers=4)` ramps in (`code: { o: 1, text:
"loader" }`). End state SEAM2[3]: `K.o: 0`, `row: { o: 1, big: 1, lab: 1,
hero: 1, chop: 1 }`, code card on; chop 0 from HOLD = 10.17 (the seam has
`row.chop: 1` but `S.chop` 0, so the knives are raised and still).

## 04_cost (24.520, 13.840 s): SEAM2[3] → SEAM2[4]

VO: "But the cost is that kitchens don't actually share counter space.
Similarly, processes don't share memory. Every result crossing between
processes needs to be pickled, pushed through a pipe, and then unpickled
again. For a big array, that copy can cost more than the compute."

Words: But@0.26 the@0.34 cost@0.46 is@0.72 that@0.86 kitchens@1.82
don't@2.10 actually@2.36 share@2.56 counter@2.80 space.@3.12
Similarly,@3.93 processes@4.48 don't@5.04 share@5.46 memory.@5.70
Every@6.66 result@6.76 crossing@7.12 between@7.60 processes@7.90
needs@8.32 to@8.64 be@8.76 pickled,@8.92 pushed@9.40 through@9.50 a@9.62
pipe,@9.74 and@10.00 then@10.08 unpickled@10.18 again.@10.54 For@11.30
a@11.38 big@11.48 array,@11.64 that@11.87 copy@12.04 can@12.30 cost@12.46
more@12.78 than@13.02 the@13.16 compute.@13.26

Opens on SEAM2[3] (big row, magenta knives raised, code card). On "cost"
(0.46) the code card fades (`code.o` → 0 over 0.3 s) and the knives go
ink (`row.hero` → 0: nothing is the hero until the bowl travels; the
bowl itself stays teal, the kit has no hero field for it, so this beat
has no magenta, which is allowed). On "don't share counter space"
(2.10–3.12) the wall and pipe grow in between kitchens 2 and 3: `wall.o`
0 → 1 over 0.3 s at 2.10, and the bowl appears on kitchen 2's counter
(`wall.bowl: 0`, `wall.bowlO` 0 → 1 at 2.56). On "memory" (5.70) the wall
label "wall / separate memory" ramps in (`wall.lab`). On "pickled" (8.92)
the box draws around the bowl (`wall.boxed` 0 → 1 over 0.25 s). On
"pushed through a pipe" (9.40–9.74) the boxed bowl travels: `wall.bowl`
0 → 1 with `SC.io` over 1.0 s from 9.40 (counter 2 → pipe → counter 3). On
"unpickled" (10.18) the box fades (`wall.boxed` → 0 over 0.25 s, so by
10.54 the bowl is unboxed on counter 3). On "that copy can cost" (12.04):
the timer bar appears (`timer.o` 0 → 1 at 11.48 "big array") and fills
only to 0.55 by "compute" (13.26): the copy ate the time. The row cooks
are still throughout (`row.chop: 0` in the seam out; let the cooks stop
chopping on "cost" at 0.46 by taking `row.chop` 1 → 0 over 0.3 s). End
state SEAM2[4]: `row: { chop: 0, hero: 0 }`, `wall: { o: 1, lab: 1,
bowl: 1, boxed: 0, bowlO: 1 }`, `timer: { o: 1, fill: 0.55 }`, chop 0
from HOLD = 13.54.

## 05_fridge (38.360, 9.490 s): SEAM2[4] → SEAM2[5]

VO: "The fix here is a shared fridge or shared memory. You put the big
tensor in once and pass a note that says shelf 3. The pipe carries the
note, not the actual food."

Words: The@0.26 fix@0.32 here@0.62 is@0.82 a@0.96 shared@1.12 fridge@1.42
or@1.74 shared@2.00 memory.@2.30 You@3.07 put@3.12 the@3.39 big@3.46
tensor@3.72 in@4.04 once@4.16 and@4.48 pass@4.66 a@4.96 note@5.02
that@5.16 says@5.31 shelf@5.52 3.@5.80 The@6.46 pipe@6.64 carries@6.90
the@7.22 note,@7.40 not@8.24 the@8.38 actual@8.54 food.@8.82

Opens on SEAM2[4] (big row, wall with label, bowl on counter 3, timer at
0.55). On "fix" (0.32) the timer bar and the wall label fade (`timer.o`
→ 0, `wall.lab` → 0 over 0.3 s). On "fridge" (1.42) minus 0.2 the fridge
grows in below the row (`fridge.o` 0 → 1 over 0.3 s), label "fridge /
shared memory" on "shared memory" (2.00). On "put the big tensor in once"
(3.12–4.16) the bowl leaves counter 3 and lands on shelf 3: the kit has
no path for that, so fade the counter bowl out (`wall.bowlO` → 0 over
0.3 s at 3.72) and the fridge bowl in (`fridge.bowl` 0 → 1 over 0.3 s at
4.04); the "3" goes magenta with the note. On "pass a note" (4.66–5.02)
the note appears at kitchen 2's counter as the hero: `fridge.noteO` 0 → 1
over 0.2 s at 4.66, `fridge.noteHero: 1`, `fridge.note: 0`. On "shelf 3"
(5.52–5.80) the note pulses (scale is fixed in the kit; pulse `noteO` to
0.6 and back). On "the pipe carries the note" (6.64–7.40) the note
travels: `fridge.note` 0 → 1 with `SC.io` over 0.9 s from 6.64. On "not
the actual food" (8.24–8.82) nothing moves: the bowl sits in the fridge,
the note sits on counter 3. End state SEAM2[5]: `row: { chop: 0, hero:
0 }`, `wall: { o: 1, lab: 0 }` (bowl hidden: `bowlO: 0`), `fridge: { o:
1, lab: 1, bowl: 1, note: 1, noteO: 1, noteHero: 1 }`, timer off, chop 0
from HOLD = 9.19.

## 06_close (47.850, 10.694 s): SEAM2[5] → SEAM2[6]

VO: "Think if you're waiting on I/O, use threads. If you're blocked by
Python or CPU intensive work, use more processes. And if you have big
data between processes, be sure to use shared memory."

Words: Think@0.29 if@0.47 you're@0.59 waiting@0.71 on@0.99 I/O,@1.19
use@1.89 threads.@1.95 If@2.81 you're@2.93 blocked@3.08 by@3.35
Python@3.53 or@3.93 CPU@4.09 intensive@4.39 work,@4.69 use@5.19 more@5.31
processes.@5.51 And@6.77 if@6.83 you@6.95 have@6.97 big@7.09 data@7.35
between@7.59 processes,@7.89 be@8.87 sure@8.95 to@9.27 use@9.33
shared@9.55 memory.@9.81

Opens on SEAM2[5] (big row still, fridge with the magenta note on
counter 3). The takeaway in three pairs of labels. On "waiting on I/O,
use threads" (0.71–1.95): the kit's `close` lines need the kitchen or the
small row, which are gone here, so this beat has no "waiting → threads"
text on screen; instead the row label "kitchens / processes" stays, and
on "threads" (1.95) nothing new appears. Keep it simple: on "use more
processes" (5.19–5.51) the four knives go magenta again (`row.hero` 0 → 1
over 0.2 s at 5.51) and the note dims (`fridge.noteHero` → 0 at the same
moment: the hero passes from the note to the knives), and the row cooks
chop (`row.chop` 0 → 1 at 5.51, strokes every 0.5 s to the hold). On
"shared memory" (9.55–9.81) the fridge label pulses (`fridge.lab` 0.5 and
back over 0.3 s, done by HOLD). `close.o: 1` is in SEAM2[6] but draws
nothing while the row is big and there is no ghost; set it at 5.51 anyway
so the state check passes. End state SEAM2[6]: `row: { chop: 1, hero:
1 }`, `wall: { o: 1, lab: 0 }`, `fridge: { ..., noteHero: 0 }`, `close.o:
1`, chop 0 from HOLD = 10.39. The last frame is the episode's takeaway;
hold it still.
