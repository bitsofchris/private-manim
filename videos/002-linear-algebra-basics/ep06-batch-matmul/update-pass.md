# Update pass notes: ep06 (PyTorch matrix multiplication)

**Name:** ep06-update-pass
**Description:** What episode 6's session found that should change the
system, sorted into its one home, for the series-wide update pass. Nothing
here is applied outside this folder.
**When to use:** runbook step 11, alongside the other episodes' notes
(`../ep02-change-of-basis/`, `../ep04-matrix-multiplication/`,
`../ep05-nn-linear-shape/update-pass.md`).
**How it works:** one item per change: trigger, cause, fix. "Also ep05 n"
marks an item that another episode's notes found too (a second use, so a
promotion or a rule).

## Series copy → `SERIES.md`

1. **Checklist boxes ep 6 now ticks:** Storyboard, Beats, Assembled.
2. **Section 6, as built.** Frame 0: the code line `Y = X @ W` alone,
   centred at 1.6×, typing; it docks at the band top on "pushes", then `X`,
   `W` and `Y` build in, and `Y` is computed row by row. Hero: the row
   being computed, then the code card's shape comment. No plane (item 9).
   Ends on CANON: `W` and `b` above, `X (5, 3)` beside `Y (5, 2)`, card
   `Y = X @ W + b  # (5,3) @ (3,2) → (5,2)`. Episode 7 can open on `W`.
3. **The code-beat line should use the on-screen names.** SERIES.md gives
   `y = X @ W`; the batch output is the matrix `Y (5, 2)` on screen, so the
   card says `Y = X @ W` (Chris did not object). Code-beat lines for later
   episodes: a batch output is a capital, as its matrix label.
4. **Open from ep05 (its note 3, "ep 6 inherits"):** ep05 asked that an
   episode which renames a matrix show the identity in code
   (`W = weight.T`). Ep06 calls it `W` throughout and never says it is
   ep05's `weight.T`; the ledger notes it, the screen does not. If 5 and 6
   are watched back to back and someone asks, a `W = weight.T` tag in beat 3
   ("W is the map") is the fix.

## Rules → `agents/animation-rules.md` / runbook / `agents/style.md`

5. **A result is never pre-filled** (Chris, 00_layout review: "don't
   populate the resulting matrix … go row by row as you do the
   computation"). Trigger: the canonical frame showed `Y` full. Fix that
   worked: `Y`'s brackets wait empty and each row appears only when its
   computation runs (the row's numbers flash with `W`'s rows, its `→`
   lights, then first number, then second); a fast cascade for "all five
   in parallel". Home: `agents/animation-rules.md` (it is the narrated-
   change rule applied to results): "an output appears when it is
   computed, never before".
6. **Build the hook part by part from the one line of code** (Chris, after
   the first watch: "just have that one line of PyTorch in the center …
   then move it down … build beat one part by part"). Fix that worked:
   frame 0 is the code line alone, centred, large, typing (so frame 0
   moves); it docks on the next phrase; each part builds in on the word
   that names it ("whole batch" → `X`, "through a layer" → `W`, then
   `Y`). Also ep05 note 5 ("open on the code the viewer would write, then
   zoom in"). Two PyTorch episodes, same correction: runbook step 0's
   "frame 0 is the finished visual already working" needs its PyTorch
   form: when VO line 1 names the code, frame 0 is that code, and the
   visual builds out of it. Home: runbook step 0 (hook) beside step 1
   "Show the code".
7. **A code card that shares the band for the whole Short caps captions
   at ~15 characters.** Trigger: with the card up throughout, 8 of 58
   captions wrapped to two lines (all over 15 characters: "The inner
   dimensions", "whole batch through"). The existing rule (`agents/style.md`
   "Share the band": every caption one line while the element is up) was
   right but gave no number. Fix that worked: split every caption over 15
   characters at a word boundary (by hand, `captions.json`); measured all
   67 in the final video, one line each. Home: the number in
   `agents/style.md` "Share the band"; the split in the tool (item 14).
   Also ep05 note 16 (caption length by hand).
8. **Monospace at 60 px holds ~24 columns in the safe width.** Trigger:
   the code beat `y = X @ W  # (5, 3) @ (3, 2) → (5, 2)` is 37 columns.
   Fix: two lines, and the comment's tuples compact, `# (5,3) @ (3,2) →
   (5,2)` (23 columns). Home: the HyperFrames brief's layout budget
   (beside "~38 px a character" for Inter) and `agents/style.md`'s code row.
9. **No plane when the episode's numbers do not fit it.** `Y` runs −5.2 to
   5.8; beside fifteen input numbers a plane would be ~35 px a step. Chris
   OK'd a notation-only stage. With ep05 note 7 (92 px a step read as
   "squished"), a floor for `agents/style.md` "Linear algebra": a plane
   shares the stage with matrices only at ≥ ~110 px a step; otherwise the
   stage is notation.
10. **`--muted` text fails `check`'s 3:1 contrast** (the "disappeared"
    inner 3s). Fix: faded text is `--dim`; `--muted` is for lines and
    retired shapes only. Home: `agents/style.md` palette usage or the
    brief's palette table (one line).

## Parts → `agents/parts.md` and code (from the beat agents' wishes)

11. **The episode kit pattern is at its third use.** ep04 `parts()` +
    `canon()`, ep05 `_ep/ep05.js`, ep06 `_ep/ep06.js`: the ledger, where
    things sit, `parts(root)` once, `state(P, g, NAME)` at the top of
    `render(t)`. With states as functions, 8 of 9 ep06 cuts diffed 0/255
    on the first try across four parallel agents (the ninth: item 15).
    Promote the pattern: a section in the HyperFrames brief and a starter
    `_ep/epNN.js` beside `prototypes/hyperframes/vec-plane/`.
12. **`state()` must reset everything a beat may touch.** Beats set
    `textShadow`, the card's `width` / `height` / `overflow`, span text and
    opacity; anything `state()` does not reset leaks across seeks. Rule
    for the pattern in item 11: `state()` resets every style property any
    beat writes.
13. **Kit wishes, by count** (worked around locally):
    - `pulse(t, t0, d)` exactly 0 outside its window (a `sin(π·seg)`
      leaves ~1e-16 that silently blocked a colour test in beat 5): every
      ep06 agent copied one; also ep05. Promote to `vec.js` or `iso.js`.
    - more than three highlight boxes (beats 4, 5, 9 built 3–5 local
      ones); also ep04, ep05 note 12. `VEC.hboxes(root, n)` or `parts()`
      taking a count.
    - typing a code-card line and easing its width between two contents
      (beats 1, 6, 8); also ep05 note 9 (`swapCard`). One card helper:
      `type(spans, k)`, `resize(fromFn, toFn, k)`.
    - a span for every token a beat may pulse (beat 6 split "(5,2)" to
      reach "2)", and a permanently split span shifted a seam by 55/255);
      also ep05 note 13 (swelling one character).
    - "row goes through W" sweep (beats 1 and 5 each wrote it) and "build
      a matrix in" (label, brackets, rows dropping) for `_ep` (item 11).
    - `data-layout-allow-overlap` on matrix cells that swell (beats 2, 3,
      5): a `VEC.cell` option, or a line in the brief's trap list.

## Tools

14. **`tools/captions_from_transcript.py --max-chars 15`** (item 7): split
    any chunk over N characters at the word boundary nearest its middle,
    times from `words.json`. A blind middle split is wrong for some:
    "with 3 features." and "a transformation." (17) fit on one line, and
    one split left "a" alone; so measure the rendered pill width, not
    characters, if the tool can (the caption is rasterized by Manim, so it
    can).
15. **An invisible highlight box still changes pixels.** The 08→09 cut
    failed `seam_check.py` at 12/255 on 2 px of `W`'s bracket: 09's
    `hbox` at opacity 0 over `W` makes a compositing layer that shifts the
    bracket's anti-aliasing. Fix in `vec.js` `hbox.rect`: `visibility:
    hidden` at alpha 0. Accepted as is in ep06 (invisible).
16. **`words.json` evenly spaced inside phrases** (every agent re-placed
    cues on the RMS envelope; "data" 0.13 s late, "stack" 0.16 s late).
    Cause: this session ran steps 4–5 before the runbook moved the timing
    transcript to WhisperKit Large v2 (commit 9ef41b3, during the session),
    so `word_times.py` used its envelope fallback. Also ep05 note 14.
    Nothing to fix if WhisperKit's per-word times hold on the next
    episode; check there.
17. **`hyperframes snapshot -o` does not overwrite**, so re-snapshotting
    a layout leaves `snap_`, `snap2_`, `snap3_` folders in `media/hf/`.
    The brief could give one command that writes to a fresh temp folder
    and copies the PNG out.

## Process

18. **The runbook changed under a running session.** Steps 0, 1, 4, 5 and
    9 were edited mid-session (search phrase, code beat, WhisperKit); the
    search phrase and code beat reached this session by a pasted
    heads-up, the timing change did not. Lesson for parallel sessions:
    re-read the runbook step before running it, not only at the start.
19. **Numbers for the runbook's "proven on" line:** a clean take with no
    phrase cuts, pauses capped at 0.25 s: 55.1 s → 49.8 s; nine beats by
    four parallel agents off one episode kit; two of Chris's changes
    (row-by-row `Y`, part-by-part hook) and no re-record.
