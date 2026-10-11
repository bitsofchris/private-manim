# Update pass notes: ep04 (x @ W)

**Name:** ep04-update-pass
**Description:** What episode 4's session found that should change the
system, sorted into its one home, for the series-wide update pass. Nothing
here is applied, except the notation rule (Chris asked for it mid-session;
`agents/style.md` "Vectors and matrices as numbers", commit e0ac380).
**When to use:** runbook step 11, alongside the other episodes' notes.
**How it works:** one item per change: trigger, cause, fix.

## Parts → `agents/parts.md` and code

1. **Matrix kit.** `ep04-matrix-multiplication/_vec/vec.js` adds the
   following to ep01's plane kit. Episodes 5 and 6 will want them, so
   promote them at their second use:
   - number grids (`grid`, `cell`)
   - bracket pairs (`brackets`)
   - the highlight box (`hbox`, `RECT`)
   - `parts()` + `canon()`, which give one rest state shared by every beat
2. **Kit wishes from the beat agents**, all worked around locally:
   - **`canon()` overrides.** Allow per-arrow overrides (draw progress, tail offset) and a "no output arrow" mode. Beats 1, 5, 6 and 8 each re-drew the plane by hand.
   - **`canon({bias:true})` layout.** It needs a wider code-label box, wider cells for `−1.2` / `−0.2` (125 px is too narrow at 64 px), and brackets spread 18 px. Beats 8 and 9 carry these as local `widen` / `SPREAD`.
   - **`RECT` boxes.** They should enclose the brackets, with an optional inset for stacked boxes. Beats 2, 3 and 7 used local rects.
   - **Shared helpers.** `pulse`, `swell` and `lerpRect` went into the kit nowhere and were copied into four beats.
   - **Bracket pairs.** Need a settable height, so a flat vector can morph into a column instead of cross-fading.

## Rules → `agents/style.md`

3. **A plane that shares the stage with matrices.**
   - **Trigger:** numbers on top, plane below.
   - **What ep04 did:** about 100 px per step instead of 165, x −1…4 and y −2…2, with the grid clipped to the plane's half (`PLANE_TOP` 650, bottom at the stage's 1100).
   - **To decide:** Chris has not commented on the smaller step. If it held up on the phone, write it as the exception to the 165 px row.
4. **Row colours for a matrix's rows** (teal, blue, gold = `COL.tokens`) carried onto that row's arrow, its weight in `x` and its weighted row. Magenta stays free for the hero. This is already in the new notation table; add ep04 as the worked example.

## Process

5. **Scratch files.** Parallel agents share the session scratchpad; one agent's `env.py` was overwritten mid-task. The beat brief should say: scratch scripts in `scratchpad/<beat>/`.
6. **Rate limit mid-build.** Two of five agents hit the session limit. Resuming them by name with a note of what was on disk finished the work without a rebuild (same lesson as ep02's item 8).
7. **zsh arrays start at 1.** A cut-check loop written for bash shifted every pair by one. Put the cut check in `tools/` as a script, so nobody hand-writes it per episode.
