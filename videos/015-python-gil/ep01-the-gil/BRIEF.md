# Beat briefs: 015 ep 1, "Python GIL explained"

Read first: `agents/beat-brief-hyperframes.md` (the contract), then this
file's "Common" section, then your beat's section. `storyboard.md` holds
the Final beats table (start, length, VO) and the seam-states table.
The kit is `../_kit/kitchen.js`: read its header comment and the
`REST` / `SEAM1` block (lines ~60–95) before writing anything.

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
same `#root`. Change `data-duration` to your `BEAT_SECONDS`, keep
`SC.SEAM = SC.SEAM1;` before `SC.mount(root)`, drop `ISO.guides(root)`,
and replace `render(t)`.

**The state model.** `kit.draw(null, S)` draws one full state `S`. Build
every frame from the seam states: `S(0)` is `SC.SEAM1[n-1]`, `S(end)` is
`SC.SEAM1[n]` (n = your beat number), and the last 0.3 s hold `SEAM1[n]`
exactly (`chop: 0`). Between them, `SC.state(SC.SEAM1[k], patch)` for a
keyframe, `SC.tween(A, B, u)` to blend two full states (numbers lerp,
strings come from B). Fields a beat may animate between seams:

- `knife.holder` fractional: 1.6 puts the knife 60 % of the way from cook
  1's hand to cook 2's, lifted in an arc. Integer = held.
- `cooks[i].u` (default 1): how far cook i has walked from its counter
  spot to `cooks[i].at` ("oven" / "appl"). Set `at` to the target and
  ramp `u` 0 → 1 over ≥ 0.6 s.
- `cooks[i].wait` fractional: fold, dim and flat face come in together.
- `S.chop` 0..1: the chop phase of whoever holds the knife (and the
  appliance cook's arm). `sin(π·chop)` is the swing, so chop runs 0 → 1
  per stroke and must be 0 at the seam. A stroke every 0.5 s reads as
  work; `chop = (t * 2) % 1` then clamp to 0 after `HOLD`.
- Every `o` / `lab` / `fill` field is a 0..1 opacity or amount: ramp over
  ~0.2 s to land on a word.

`SC.io(u)` is ease-in-out, `SC.seg(t, a, b)` is `clamp01((t−a)/(b−a))`.
Use `SC.lerp`, `SC.clamp01`.

**Cues** are beat-local seconds (master − beat start) from `words.json`;
the per-beat sections below list every word with its time. Name them as
constants with the word in a comment. Check a cue that carries a move on
the RMS envelope of `vo_final.wav` if it looks off.

**Hero.** The knife is the one magenta thing (`knife.hero: 1` in every
SEAM1 state). Nothing else goes magenta.

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

## 01_kitchen (0.000, 7.250 s): SEAM1[0] → SEAM1[1]

VO: "In Python, think of a process as a kitchen. Here, threads are cooks,
and they all share the kitchen's memory."

Words: In@0.42 Python,@0.50 think@1.33 of@1.50 a@1.64 process@1.78 as@2.26
a@2.50 kitchen.@2.66 Here,@3.56 threads@4.22 are@4.48 cooks,@4.60 and@5.72
they@5.78 all@5.86 share@6.02 the@6.22 kitchen's@6.38 memory.@6.74

Frame 0 is SEAM1[0]: the kitchen box with "kitchen / process", four cooks
at the counter, cook 1 holding the magenta knife. This is the hook, so
something is already moving at frame 0: cook 1 chops from t = 0 (chop
strokes every 0.5 s) and keeps chopping to the hold. On "process" (1.78)
the "kitchen / process" label pulses once (the kit has no pulse field:
briefly drop `K.lab` to 0.6 and back over 0.3 s, or leave it; a label
already on screen is fine). On "cooks" (4.60) `cooksLab` ramps 0 → 1 over
0.2 s. On "share ... memory" (6.02–6.74) nothing new appears (memory is
the box itself): optionally the four bowls on the counter are already
there. End state SEAM1[1] = SEAM1[0] + `cooksLab: 1`, chop 0 from
HOLD = 6.95.

## 02_knife (7.250, 7.550 s): SEAM1[1] → SEAM1[2]

VO: "The knife is the GIL, the global interpreter lock. Whoever holds the
knife is what runs the Python code while everyone else waits."

Words: The@0.25 knife@0.37 is@0.79 the@0.99 GIL,@1.23 the@1.69 global@1.75
interpreter@2.05 lock.@2.47 Whoever@3.27 holds@3.59 the@4.21 knife@4.41
is@4.73 what@5.01 runs@5.35 the@5.45 Python@5.61 code@5.95 while@6.25
everyone@6.43 else@6.75 waits.@7.03

Opens on SEAM1[1] (cook 1 holding the knife, chopping carries on from
beat 1). On "knife" (0.37) the "knife / GIL" label ramps in (`knife.lab`
0 → 1 over 0.2 s). On "holds" (3.59) cook 1 chops a little harder (keep
the stroke period). On "everyone else waits" (6.43–7.03) cooks 2, 3, 4
fold their arms and dim: ramp `cooks[1..3].wait` 0 → 1 over 0.4 s starting
at 6.43, staggered 0.1 s each. End state SEAM1[2]: `cooksLab 1`,
`knife.lab 1`, cooks 2–4 `wait: 1`, chop 0 from HOLD = 7.25.

## 03_loop (14.800, 7.030 s): SEAM1[2] → SEAM1[3]

VO: "This is why threading a CPU loop makes it no faster. Four threads
with one knife, you have one core's worth of work still."

Words: This@0.26 is@0.44 why@0.54 threading@0.66 a@1.24 CPU@1.38 loop@1.74
makes@2.36 it@2.60 no@2.72 faster.@2.82 Four@3.90 threads@4.04 with@4.40
one@4.54 knife,@4.74 you@5.17 have@5.32 one@5.46 core's@5.74 worth@6.04
of@6.26 work@6.36 still.@6.56

Opens on SEAM1[2]. On "threading" (0.66) the code card
(`code: { o: 1, text: "threads" }`) ramps in over 0.2 s and the timer bar
appears empty (`timer: { o: 1, fill: 0 }`). From "loop" (1.74) the knife
hops cook 1 → 2 → 3 → 4, one hop per 0.6 s (`knife.holder` 0 → 1 → 2 → 3
with `SC.io` on each hop; whoever holds it chops between hops; the other
three show `wait: 1`, the holder `wait: 0`, swapping as the knife lands).
The timer bar fills steadily from 1.74 to reach `fill: 1` at "still"
(6.56): it fills at one cook's rate however many cooks there are. The
knife lands with cook 4 by "one knife" (4.74) and stays. End state
SEAM1[3]: knife `holder: 3`, cooks 1–3 `wait: 1`, cook 4 `wait: 0`, code
card on, timer `fill: 1`, chop 0 from HOLD = 6.73.

## 04_oven (21.830, 9.940 s): SEAM1[3] → SEAM1[4]

VO: "But a cook puts the knife down to wait on the oven. That could be an
I/O, a request, a file read, a sleep. The GIL is released while the thread
waits, so another thread can run."

Words: But@0.23 a@0.33 cook@0.43 puts@0.75 the@0.93 knife@1.03 down@1.23
to@1.59 wait@1.79 on@2.03 the@2.13 oven.@2.25 That@2.99 could@3.07 be@3.21
an@3.33 I/O,@3.41 a@3.99 request,@4.05 a@4.44 file@4.59 read,@4.89 a@5.27
sleep.@5.37 The@6.13 GIL@6.27 is@6.47 released@6.63 while@6.97 the@7.21
thread@7.41 waits,@7.59 so@8.05 another@8.25 thread@8.63 can@8.89 run.@9.05

Opens on SEAM1[3] (knife with cook 4, code card and full timer). The
oven: `oven.o` 0 → 1 over 0.3 s from "oven" (2.25) minus 0.2, label
`oven.lab` on "oven". Story: the knife is with cook 4 at frame 0, but the
seam out has it with cook 3 and cook 2 at the oven. So: on "cook" (0.43)
the code card fades (`code.o` → 0 over 0.3 s). On "puts the knife down"
(0.75–1.23) cook 4 hands the knife back: hop `holder` 3 → 1 over 0.6 s
(cook 2 takes it; choose 3 → 1 directly, the arc reads as a pass). On
"wait on the oven" (1.79–2.25) cook 2 walks to the oven: `cooks[1].at =
"oven"`, `u` 0 → 1 over 0.8 s, and as it leaves, the knife hops to cook 3
(`holder` 1 → 2 over 0.6 s, from 1.79). "I/O, a request, a file read, a
sleep" (3.41–5.37): the oven label is already there; the oven glow is
automatic while a cook is at the oven; nothing else. "The GIL is released"
(6.27–6.63): the knife label pulses (drop `knife.lab` to 0.5 and back over
0.3 s). "another thread can run" (8.25–9.05): cook 3 chops harder, the
timer bar (still `o: 1`) empties and refills faster: set `fill` 1 → 0 at
8.25 then → 1 by 9.3, with the kit's bar. End state SEAM1[4]: knife
`holder: 2`, oven on with label, cook 2 at the oven (`wait: 1`), cooks 1
and 4 `wait: 1` at the counter, cook 3 `wait: 0`, code off, timer `o: 1,
fill: 1`, chop 0 from HOLD = 9.64.

## 05_appliance (31.770, 4.110 s): SEAM1[4] → SEAM1[5]

VO: "Same for an appliance. Think of NumPy, image decoding, a tokenizer."

Words: Same@0.71 for@0.99 an@1.11 appliance.@1.19 Think@1.77 of@1.89
NumPy,@2.05 image@2.48 decoding,@2.73 a@3.27 tokenizer.@3.37

Opens on SEAM1[4]. On "appliance" (1.19) minus 0.2 the appliance ramps in
(`appl.o`, then `appl.lab` on the word). From 1.19 cook 4 walks to it
(`cooks[3].at = "appl"`, `u` 0 → 1 over 0.8 s, `wait` 1 → 0 as it
arrives). From "NumPy" (2.05) cook 4 works at the appliance without the
knife (the kit's appliance pose moves with `chop`) while cook 3 chops with
the knife: two cooks visibly working at once. End state SEAM1[5]:
SEAM1[4] + appliance on with label, cook 4 at the appliance `wait: 0`,
chop 0 from HOLD = 3.81.

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

Opens on SEAM1[5] (both cooks working, timer on). On "ask one thing"
(1.60) the timer bar fades (`timer.o` → 0 over 0.3 s). On "waiting" (2.94)
the oven label pulses (`oven.lab` 0.5 and back); on "running Python"
(3.80) the knife label pulses the same way. On "then threads work"
(5.62–6.00) the first close line "waiting → threads" appears: `close.o`
0 → 1 over 0.2 s at 5.62 (the kit draws both close lines from `close.o`;
the second line's opacity is also gated by `ghost.o`, so it stays hidden
until the ghost comes). On "second kitchen" (7.92) the ghost kitchen grows
in: `ghost.o` 0 → 1 over 0.3 s, which also reveals "running Python →
processes" and the ghost's own "second kitchen / another process" label.
Cook 3 keeps chopping to the hold. End state SEAM1[6]: SEAM1[5] with timer
off, `ghost.o: 1`, `close.o: 1`, chop 0 from HOLD = 9.9. The last frame is
the episode's takeaway; hold it still.
