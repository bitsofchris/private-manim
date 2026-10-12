# Update pass notes: ep07 (why layers need activations)

**Name:** ep07-update-pass
**Description:** What episode 7's session found that should change the
system, sorted into its one home, for the series-wide update pass. Nothing
here is applied outside this folder.
**When to use:** runbook step 11, alongside the other episodes' notes.
**How it works:** one item per change: trigger, cause, fix.

## Series copy → `SERIES.md`

1. **Checklist boxes ep 7 now ticks:** Storyboard, Beats, Assembled.
2. **Ep 7's frame 0 changed.** It now opens on the plane turning under W
   ("a linear map … can't bend"), not on two W boxes collapsing. The
   collapse is the middle of the Short. The SERIES.md "Frame 0 / hero" line
   is stale.

## Rules → runbook / `agents/style.md`

3. **Open on the strongest visual, even if line 1 isn't the answer.**
   Trigger: Chris after cut 1, "I'd like to open there … that's the
   strongest part". Line 1 is now "A linear map keeps the origin fixed …",
   and the search phrase comes at 7.1 s. This contradicts runbook step 1
   ("VO line 1 is THE ANSWER"). Decide at the day-10 read whether step 1
   gets an exception for a visual hook.
4. **Re-ordering a recorded take works.** Splice whole phrases from
   `vo_final.wav` in the new order (8 ms fades, keep a pause at each join),
   then remap `words.json` by the same offsets. The re-splice moved the
   phrases out of segment order, so `seg` must be renumbered in time order
   or `captions_from_transcript.py` emits overlapping captions (`assemble.py`
   failed: "starts before previous ends"). Worth a `tools/resplice_vo.py`
   that does the cut, the word remap and the renumber in one step.
5. **Dropping a word with no gap after it** (the "Now" in "Now a linear
   map"): sweep cut points in 40 ms steps and transcribe each sub-clip with
   Parakeet. 30.06 still read "Our linear map"; 30.10 read "A linear map".
   Cut 20 ms past the first clean point.

## Parts → `agents/parts.md` and code

6. **`warp(g, f)`:** the plane's grid pushed through any map, linear or not,
   as sampled polylines, plus `stage({w1, relu, w2, post})` as dials.
   Promote to `vec.js` when a second episode draws a nonlinearity on the
   plane.
7. **Code-card row helpers:** open or close one row with its gap (08, 10:
   `openGap`), card-to-card morph in place (04, 05, 06: panel stretch plus
   clipped cross-fade). This is the third episode to hand-roll the morph
   (ep05 too). Promote as `VEC.codeCard` row access plus `VEC.swapCard`.
8. **`EP.plane` trail options:** partial draw (`u`) and a lit colour per hop.
   Beats 2, 3 and 4 each redrew the plane locally to get them.
9. **00_layout should render every state a beat opens or ends on**
   (here STACK and LINEAR were missing), so agents can compare pixels
   instead of eyeballing.

## Process

10. **A rate limit killed all six beat agents mid-read.** Resuming each by
    name with "continue from where you stopped" worked with no lost work.
11. **Agents shared one scratchpad directory and overwrote each other's
    helper scripts.** Give each agent its own scratch subfolder in the brief.
