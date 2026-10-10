# Update pass notes: ep02 (change of basis)

**Name:** ep02-update-pass
**Description:** Everything episode 2's session found that should change the
system, sorted into its one home (AGENTS.md "Keeping the system clean"),
written as ready-to-apply edits. Nothing here has been applied: other
sessions were editing `agents/` and `SERIES.md` in parallel, so the update
pass runs once for the whole series.
**When to use:** the series-wide update pass (runbook step 11), alongside the
other episodes' notes.
**How it works:** one section per home; each item says the trigger, the
cause, the fix, and what the wrong version looked like. Apply, then add one
`agents/changelog.md` line per item citing ep02.

## Rules → `agents/style.md` (or `agents/animation-rules.md`)

1. **No 3D lattice through the volume.**
   - **Trigger:** a 3D beat needs a grid that changes with the basis.
   - **Cause:** drawing all three families of grid lines through the volume gives hundreds of overlapping lines and no depth cue in a still projection.
   - **Fix:** draw a solid floor carrying one 2D grid (the first two basis vectors), a dashed stalk for height, and the address as a route of legs laid tip to tail.
   - **Wrong version:** ep02's first build (commit 933dae6); Chris: "way too confusing."
   - **Right version:** `ep02-change-of-basis/_kit/basis.js`.
2. **Ghost grid alpha ≈ 0.14.**
   - **Trigger:** the old grid is left faint under a sheared new grid.
   - **Cause:** at 0.3 the two grids together read as a triangle mesh.
   - **Fix:** keep the ghost alpha around 0.14.
3. **Choose the example so the change happens in a plane.**
   - **Trigger:** a 3D change-of-basis example.
   - **Fix:** pick a basis whose third vector stays fixed. ep02 uses v1 = (0, −1, 0), v2 = (1, 1, 0), v3 = z, so the whole change is a floor shear and the third number stays the same on screen. The spoken numbers were unchanged.
4. **Camera drift and the final hold.**
   - **Trigger:** a slow camera drift computed from master time, while each beat freezes its last ~0.4 s.
   - **Cause:** freezing the drift for each hold leaves a 0.1–0.8° jump at every cut.
   - **Fix:** no drift. If a beat needs life, move the camera inside the beat and return it to the canonical view before the hold.

## Process → `agents/runbook.md`

5. **Step 0 and rule 6 conflict.**
   - **The conflict:** step 0 puts the question on screen in the caption band at frame 0, but with VO that band belongs to the burned-in captions (AGENTS.md rule 6, `agents/style.md`).
   - **What ep02 did:** dropped the on-screen question; frame 0 shows the address flipping instead.
   - **Decide:** either the question goes at the top of the stage for the first ~2 s, or step 0 says "no question text when the Short has VO".
6. **Mock the main visual before briefing beat agents.**
   - **Trigger:** the hero visual is new (no prior beat shows it).
   - **Fix:** render one canonical frame (`00_layout/`) and show it to Chris before spawning agents.
   - **Cost of skipping it:** ep02 built and assembled the whole Short before the look was rejected. The 2-frame mock in the rethink settled it in one exchange.
7. **Episode folders one level deeper.** The series layout (`videos/002-…/epNN-slug/`) adds a level to every relative path:
   - symlinks `../../../_shared/web/vendor`
   - tools at `../../../tools/`
   - Manim shim `parents[3]`

   Note this in step 6 and both beat briefs, or in `SERIES.md`.
8. **Resume beat agents for a rework.** Sending the same agents (by name) a brief that lists only what changed cost a third of a fresh spawn: they kept their audio-derived cue times.

## Tools → `tools/`

9. **`captions_from_transcript.py`: spoken numbers.**
   - **Problem:** Whisper writes "352", "minus 232" and "One one". After fixing them to "3, 5, 2", a caption can exceed `assemble.py`'s 4-word limit, because the commas split the numbers into words.
   - **Option:** count a run of numbers like "3, 5, 2" as one word in the limit.
   - **Option:** a `--fix` mapping file applied before splitting.
   - Add a test for each.
10. **Word-level timestamps.**
    - **Problem:** beat agents timed spoken numbers by transcribing 0.5–2 s sub-clips, and Whisper misheard several ("minus two" as "to").
    - **Option:** a small tool that returns the start time of each word in a window, from forced alignment against the known script text, or from the energy envelope plus the transcript.

## Parts → `agents/parts.md`

11. **Local to ep02, 1 use each; promote if ep01/ep03 reuse them:**
    - `_kit/basis.js`: the floor-and-route world (`BK.world`, `route`, `floorGrid`, `coordsAt`), the address readout `makeReadout` (numbers that tick, one colour per basis vector; options `lit`, `pulse`, `visible`, `dy`), and `makeBasisLabels`.
    - The 2D world in `07_feature/index.html`: a lattice that rotates and stretches to the d1, d2 basis, with legs.
12. **Kit wishes the beat agents reported:**
    - a shared hero glow
    - a hook to draw between the grid and the arrows (beat 2 redraws its arrows locally)
    - a "dim full grid under a growing grid" option (beat 2 borrows `ghost`)
    - a built-in stage clip plus bottom fade for camera push-ins
    - a 2D mode (`S` takes a projection; `makeLabel.place` takes screen coordinates)
13. **Colour.** The basis colours teal / blue / gold reuse the iso kit's token triple. Blue `#60A5FA` is still not in `style.py`; it is now used by 009–011 and ep02. Add it as a token.

## Series → `SERIES.md`

14. **Checklist, episode 2:** tick Storyboard, Beats and Assembled.
15. **Episode 2 section:**
    - **Frame 0 / hero is now:** the point on its stalk, the floor grid shearing, the route re-routing, and the address ticking (3, 5, 2) ⇄ (−2, 3, 2).
    - **Reuse:** note that the basis differs from `basis_transformation_3d.py` (item 3).
    - **Ends on:** the 2D still u = (1, 1) lying on d1 with the address (1, 0). Episode 3 can open on two basis arrows.

## Nothing to do

- The HyperFrames engine choice held: the problem was the mesh, not the engine.
- Beat 7 (2D) survived both builds unchanged except its grid weight.
