# Beat briefs: 015 ep 2, "Multithreading vs multiprocessing python" (v4, the redo on kit v2)

Read first: `agents/beat-brief-hyperframes.md` (the contract), then this
file's "Common" section, then your beat's section. `storyboard.md` holds
the beat table (start, length, VO, visual) and the seam-states table.
The kit is `../_kit/kitchen.js`: read its header comment, the `REST` /
`SEAM1` / `PROTO` block and the `// ---- episode 2 ----` block (`SEAM2`,
`PROTO2`, the helpers `ONE`, `GRID4`, `PAR_ROWS`, `COST_ROWS`, `SHM_ROWS`,
`PROC`, `DIM34`, `RECAP`, `EP2_FRAME0`) and `draw()` before writing
anything. `00_layout/proto.png` is the approved look: tiles 1–14 are
`SC.PROTO2[0..13]`, and the seam states are tiles 1, 2, 5, 8, 11, 13, 14.

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
exactly (every `chop` 0). Between them, `SC.state(base, patch, patch…)`
(REST, then each patch merged in turn; arrays replace wholesale, so patch
a cook by spreading the base cook) and `SC.tween(A, B, u)` to blend two
full states. `SC.PROTO2[k]` are the approved in-between frames: use them
as keyframes where they match your beat. Fields a beat animates:

- The main kitchen: `K.o`, `K.draw`, `K.lab`, `K.half` (0..1, scales to
  the grid's top-left cell), `cooks[i].{in, at, u, wait, cut}`, `veg`,
  `knife.{o, holder, hero}`, `oven.o`, `appl.o`, `S.chop` (0..1, the
  holder's stroke). Same meanings as ep 1 (`in`: walked in from off-left;
  `wait`: folded and dim; `cut`: how much of its carrot is sliced, grow it
  only while that cook holds the knife and chops; `holder` −1 = on the
  board, integer = held, fractional = between hands).
- The other kitchens `twin`, `k3`, `k4` (grid cells top-right,
  bottom-left, bottom-right): each is `{ o, draw, cooks, veg, knife, oven,
  appl, chop }` with its own `chop`. `SC.ONE(cut, hero)` is a kitchen with
  one cook holding the knife (the other three cooks `in: 0`, so they stay
  off-screen). Cooks are hidden until `draw` reaches 1.
- `tag.o`: the magenta price tag on the second kitchen's corner.
- `wall: { o, draw }` (draw 0..1 grows it top-down), `pipe.o`.
- `bowl: { o, x, y, box }`: frame coordinates; `box` 0..1 crossfades the
  bowl into a crate. Rest points: `SC.BOWL.k1` (kitchen 1's counter),
  `SC.BOWL.pipeIn`, `SC.BOWL.pipeOut`, `SC.BOWL.k2`, `SC.BOWL.fridge`
  (shelf 3). Move it along straight lines between those with `SC.io`.
- `note: { o, x, y }`: the "shelf 3" note (hero), same coordinates.
- `fridge: { o, draw, shelf }`: the slab draws in with `draw`; `shelf` 1
  lights the "3" magenta.
- `slot: { o, top, bottom, hero }`: the top-right label. Ready-made:
  `SC.SLOT.knife`, `.cooks`, `.kitchens`, `.knives`, `.wall`, `.pipe`,
  `.fridge`, `.note`. To swap, fade `o` 1 → 0 over 0.15 s, change the text,
  fade back over 0.2 s landing on the word.
- `panel: { o, title, lanes, split, proc, titleText, rows, pulse }`:
  `titleText` is the title row (swap it like the slot, by fading `title`);
  `split` 0..1 is ep 1's two-half layout (frame 0 of this episode);
  `proc` 0..1 crossfades `Thread n` lanes into `Process n` (bars start
  further right); `rows[i] = [{ a, b, k }]` with `k` `"py"` (magenta) |
  `"io"` (dashed) | `"nat"` (teal) | `"copy"` (grey); grow a bar by moving
  `b`, and add a bar to a row only once `b > a` (the state check treats a
  zero-length bar as a mismatch). `panel2.rows` is the right half while
  split. `pulse.py` / `pulse.io` 0..1.
- `close: { a, b, c, panel }`: the close lines. With `panel` 0 they use
  ep 1's places (inside the kitchen while full size, the gap below it
  when `K.half` is 1); with `panel` 1 all three sit where the panel was.

`SC.chopAt(t, from, to, rate)` gives a phase that is 0 at both ends with
~`rate` strokes per second (use 2); chop between those times only, never
across a seam, and set each kitchen's own `chop`. `SC.io(u)` is
ease-in-out, `SC.seg(t, a, b)` is `clamp01((t−a)/(b−a))`, `SC.pulse(t,
at, w)` one sine bump. Use `SC.lerp`, `SC.clamp01`, `SC.merge`.

**Cues** are beat-local seconds (master − beat start) from `words.json`;
the per-beat sections below list every word with its time. Name them as
constants with the word in a comment. A thing lands ON its word (ramp
0.15–0.25 s ending at the word), never before it. Where a cue sum would
land exactly on a hold boundary, write the constant out (float sums miss
by 1e-15 and the state check sees a missing bar).

**Hero.** Magenta = the GIL: the knives, the "py" bars, the "knife / GIL"
and "own knife / own GIL" slots, the price tag, the "shelf 3" note and
its slot. Nothing else goes magenta. Knives go ink (`hero: 0`) during the
cost beat and come back magenta at the close.

**Layout.** Captions are anchored bottom: the stage runs y 230–1330, the
caption band y 1330–1536 stays empty, nothing below y 1330. The kit
places everything; you set state, not pixels (the bowl and note take
frame coordinates from `SC.BOWL`).

**Check, render, review** (from the episode folder; `ROOT=$(git rev-parse --show-toplevel)`):

```
node "$ROOT"/tools/hf_state_check.js NN_beat FROM TO      # FROM = n-1, TO = n
cd NN_beat && HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx --yes --prefer-offline hyperframes@0.8.115 check
HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
cd .. && "$ROOT"/tools/review_frames.sh --at CUE1,CUE2 media/hf/NN_beat.mp4 4
ffprobe -v error -show_entries format=duration -of csv=p=0 media/hf/NN_beat.mp4
```

Do not run `seam_check.py` (it is run once for all beats afterwards; two
agents running it at once corrupt its scratch folder). Open your contact
sheet with the Read tool and look: does each thing land on its word, are
knives on a board or in a hand (never floating), is the last frame still.
`check` must be 0 errors (`rotation_pivot_drift` warnings on knife groups
and `content_overlap` warnings during a label crossfade are expected).
State check must pass on both cuts. Do not edit `../_kit/` or
`videos/_shared/`. Do not commit. Scratch files go in the session
scratchpad under your agent name.

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

Opens on SEAM2[0] (PROTO2[0]), ep 1's last frame: kitchen 1 at half size
with its four cooks (cook 2 holds the knife, its carrot done, so no
`cut` growth; chop anyway), the second kitchen with its cook 1 holding
the knife (`twin.cooks[0].cut` 0.3 → 0.3, chop), the panel split. Both
holders chop from 0.2 to 5.8 (`S.chop` and `twin.chop`, `SC.chopAt`).
On "threads" (1.20) `close.a` 0 → 1 over 0.2 s landing at 1.20;
"waiting" (2.08) `pulse.io` bumps (`SC.pulse(t, 2.08, 0.6)`). On
"processes" (3.42) `close.b` 0 → 1 landing at 3.42; "Python" (5.28)
`pulse.py` bumps. End state SEAM2[1] (PROTO2[1]), still from HOLD = 5.86.

## 02_recap (6.160, 7.890 s): SEAM2[1] → SEAM2[2]

VO: "The part people often miss is what an additional process actually
costs. Think of a process as a full kitchen. Threads are its cooks, the
GIL is one knife."

Words: The@0.20 part@0.26 people@0.55 often@0.74 miss@1.02 is@1.22
what@1.34 an@1.50 additional@1.62 process@2.00 actually@2.42 costs.@2.74
Think@3.62 of@3.74 a@3.84 process@3.94 as@4.28 a@4.42 full@4.50
kitchen.@4.70 Threads@5.54 are@5.74 its@5.80 cooks,@5.98 the@6.60 GIL@6.72
is@6.86 one@6.98 knife.@7.16

Opens on SEAM2[1]. On "process" (2.00) the two close lines fade out over
0.2 s. On "costs" (2.74) `tag.o` 0 → 1 over 0.2 s landing at 2.74
(PROTO2[2]). On "kitchen" (4.70) the rebuild, 0.6 s ending at 4.70: the
tag and the second kitchen fade out (`tag.o`, `twin.o` → 0 over the first
0.2 s), `panel.split` 1 → 0 (`SC.io`), `K.half` 1 → 0 (`SC.io`; PROTO2[3]
is the midpoint), the panel rows become `[[{ a: 0, b: 0.3, k: "py" }],
[], [], []]` (crossfade: fade the split rows with `split`, show the new
row from `split` 0.5; `panel2.rows` empty from there). As the kitchen
grows back, cooks 2 and 4 walk to the counter: `cooks[1].at`, `u` 1 → 0
then `at = "counter"`, `u` 1 (0.5 s from 4.10); `cooks[3]` likewise; cook
1 unfolds (`wait` 1 → 0 over 0.3 s ending at 4.70) and the knife hops
from cook 2 to cook 1 (`knife.holder` 1 → 0 over 0.3 s ending at 4.70,
cook 2 folding as it leaves). `cooks[1].cut` 1 → 0.5 and `cooks[2].cut`
0.8 → 0.5 happen during the rebuild (a fresh carrot; snap them at the
midpoint while the kitchen is in motion, 4.40). On "cooks" (5.98) slot
`SC.SLOT.cooks` lands (fade in 0.2 s) and cooks 2–4 pulse once (their
`wait` 1 → 0.6 → 1 over 0.4 s). On "knife" (7.16) the slot swaps to
`SC.SLOT.knife` and cook 1 chops once (`SC.chopAt(t, 7.16, 7.59, 2)`,
`cooks[0].cut` stays 0.5). End state SEAM2[2] (PROTO2[4]), still from
HOLD = 7.59.

## 03_processes (14.050, 10.470 s): SEAM2[2] → SEAM2[3]

VO: "Multiprocessing builds more kitchens. Each process has its own
interpreter and its own GIL, so Python actually runs in parallel.
PyTorch's data loader workers are new processes."

Words: Multiprocessing@0.41 builds@0.89 more@1.17 kitchens.@1.37
Each@2.31 process@2.55 has@3.07 its@3.33 own@3.47 interpreter@3.69
and@4.11 its@4.39 own@4.55 GIL,@4.81 so@5.41 Python@5.47 actually@5.89
runs@6.39 in@6.69 parallel.@6.85 PyTorch's@7.77 data@8.25 loader@8.43
workers@8.69 are@8.95 new@9.43 processes.@9.65

Opens on SEAM2[2]. On "Multiprocessing" (0.41) the title swaps to
`multiprocessing.Pool(4)` (fade `panel.title` out 0.15 s, change
`titleText`, in 0.2 s landing at 0.41) and `panel.proc` 0 → 1 over 0.3 s
ending at 0.41; the Thread 1 bar fades with the lane labels (drop it from
`rows` once `proc` ≥ 0.5). On "kitchens" (1.37) kitchen 1 shrinks:
`K.half` 0 → 1 over 0.5 s ending at 1.37 (`SC.io`), slot swaps to
`SC.SLOT.kitchens` landing at 1.37, and `cooks[0].cut` stays 0.5. Then
the other three draw in: `twin.draw` 0 → 1 over 0.3 s from 1.5, `k3`
from 1.85, `k4` from 2.2 (`o` 1 from their start), each followed by its
cook walking in (`cooks[0].in` 0 → 1 over 0.5 s from the end of its draw)
and `veg` 1 with the cook; knives `o` 0 for now (PROTO2[5] is the
midpoint). On "GIL" (4.81) a knife appears in every hand: `knife.o` 0 → 1
over 0.2 s landing at 4.81 in `twin`, `k3`, `k4` (`holder` 0, `hero` 1;
kitchen 1's knife is already with cook 1), slot swaps to
`SC.SLOT.knives` landing at 4.81 (PROTO2[6]). On "parallel" (6.85) all
four cooks chop (`S.chop`, `twin.chop`, `k3.chop`, `k4.chop` =
`SC.chopAt(t, 6.85, HOLD, 2)`), and four magenta bars grow together:
`rows[i] = [{ a: 0, b, k: "py" }]`, `b` 0 → 0.5 linearly 6.85 → HOLD
(add the bars at 6.85 + one frame, so `b > a`); every holder's `cut`
0.5 → 0.5 (ep 1 convention: hold the seam value, the strokes are the
motion). On "workers" (8.69) the title swaps to `num_workers=4` and the
slot swaps back to `SC.SLOT.kitchens` landing at 8.69. End state SEAM2[3]
(PROTO2[7]), still from HOLD = 10.17.

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

Opens on SEAM2[3]: no chopping in this beat. On "cost" (0.46) the knives
go ink (`knife.hero` 1 → 0 in all four kitchens, snap), `k3.o` and `k4.o`
1 → 0.3 over 0.3 s ending at 0.46, the title swaps back to
`multiprocessing.Pool(4)`, and the bars shrink 0.5 → 0.3 over 0.3 s
(their `b`). On "counter" (2.80) the wall draws: `wall.o` 1, `wall.draw`
0 → 1 over 0.3 s ending at 2.80 (PROTO2[8] minus the bowl); on "memory"
(5.70) slot swaps to `SC.SLOT.wall` landing at 5.70. On "result" (6.76)
the bowl appears on kitchen 1's counter: `bowl.o` 0 → 1 over 0.2 s at
`SC.BOWL.k1`. On "pickled" (8.92) `bowl.box` 0 → 1 over 0.3 s ending at
8.92, title swaps to `pickle.dumps(arr)`, slot swaps to `SC.SLOT.pipe`
landing at 8.92, and Process 1's grey bar starts: `rows[0]` gets `{ a:
0.3, b, k: "copy" }`, `b` 0.3 → 0.9 linearly 8.92 → 13.26 ("compute").
On "pipe" (9.74) `pipe.o` 0 → 1 over 0.2 s landing at 9.74, then the
crate travels: `SC.BOWL.k1` → `SC.BOWL.pipeIn` over 9.74 → 10.0,
`pipeIn` → `pipeOut` over 10.0 → 10.4 (PROTO2[9] is the midpoint), on
"unpickled" (10.18 → 10.54) `pipeOut` → `SC.BOWL.k2` and `bowl.box`
1 → 0 over the last 0.3 s ending at 10.54, title swaps to
`pickle.loads(buf)` landing at 10.54. The grey bar keeps growing through
"that copy can cost more than the compute" and reaches 0.9 on "compute"
(13.26), visibly past the magenta 0.3: that length is the point. End
state SEAM2[4] (PROTO2[10]), still from HOLD = 13.54.

## 05_fridge (38.360, 9.490 s): SEAM2[4] → SEAM2[5]

VO: "The fix here is a shared fridge or shared memory. You put the big
tensor in once and pass a note that says shelf 3. The pipe carries the
note, not the actual food."

Words: The@0.26 fix@0.32 here@0.62 is@0.82 a@0.96 shared@1.12 fridge@1.42
or@1.74 shared@2.00 memory.@2.30 You@3.07 put@3.12 the@3.39 big@3.46
tensor@3.72 in@4.04 once@4.16 and@4.48 pass@4.66 a@4.96 note@5.02
that@5.16 says@5.31 shelf@5.52 3.@5.80 The@6.46 pipe@6.64 carries@6.90
the@7.22 note,@7.40 not@8.24 the@8.38 actual@8.54 food.@8.82

Opens on SEAM2[4]. On "fridge" (1.42) kitchens 3–4 fade (`k3.o`, `k4.o`
0.3 → 0 over 0.3 s ending at 1.12) and the fridge draws in: `fridge.o`
1, `fridge.draw` 0 → 1 over 0.4 s ending at 1.42; slot swaps to
`SC.SLOT.fridge` landing on "memory" (2.30). On "put" (3.12) the bowl
goes back to kitchen 1: `bowl` moves `SC.BOWL.k2` → `SC.BOWL.k1` over
3.12 → 3.6 (over the wall, no pipe: lift it in an arc, `y` − 60·sin(πu)).
On "once" (4.16) it drops into the fridge: `SC.BOWL.k1` → `SC.BOWL.fridge`
over 3.9 → 4.16 (`SC.io`), `fridge.shelf` 0 → 1 (snap at 4.16), the grey
bar shrinks `b` 0.9 → 0.36 over 0.3 s ending at 4.16 and the title swaps
to `SharedMemory(name)` landing at 4.16. On "note" (5.02) the note
appears on kitchen 1's counter: `note.o` 0 → 1 over 0.2 s at
`SC.BOWL.k1`; on "3." (5.80) slot swaps to `SC.SLOT.note` landing at
5.80. On "pipe" (6.64) the note travels `SC.BOWL.k1` → `pipeIn` →
`pipeOut` → `SC.BOWL.k2` over 6.64 → 7.40 ("note,"; PROTO2[11] is the
midpoint). On "food" (8.82) the bowl in the fridge bobs once (`y` −
12·sin(πu) over 0.4 s). End state SEAM2[5] (PROTO2[12]), still from
HOLD = 9.19.

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

Opens on SEAM2[5]. On "Think" (0.29) the panel fades (`panel.o` 1 → 0
over 0.3 s ending at 0.29), the slot fades out, `note.o` 1 → 0.5,
`close.panel` 1 (snap at 0), knives go magenta again (`knife.hero` 1 in
kitchen 1 and `twin`, snap at 0.29) and both holders chop from 0.29 to
9.81 (`S.chop`, `twin.chop`; `cut` values hold). On "threads." (1.95)
`close.a` 0 → 1 over 0.2 s landing at 1.95; on "processes." (5.51)
`close.b`; on "memory." (9.81) `close.c`. Chop stops at 9.81. End state
SEAM2[6] (PROTO2[13]), still from HOLD = 9.81 (the last frame is the
end of the Short).
