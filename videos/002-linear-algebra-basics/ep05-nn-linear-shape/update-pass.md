# Update pass notes: ep05 (how a PyTorch linear layer works)

**Name:** ep05-update-pass
**Description:** What episode 5's session found that should change the
system, sorted into its one home, for the series-wide update pass. Nothing
here is applied outside this folder.
**When to use:** runbook step 11, alongside the other episodes' notes.
**How it works:** one item per change: trigger, cause, fix.

## Series copy → `SERIES.md`

1. **Title.** Ep 5's title is now `How a PyTorch Linear Layer Works | Linear
   Algebra for AI Engineers` (was "PyTorch nn.Linear Explained"). Search
   phrase `pytorch linear layer`: YouTube autocomplete offers it first for
   "pytorch linear"; no phrasing of the transpose question is offered.
   Chris's rule: "title it with what it actually answers."
2. **Checklist boxes ep 5 now ticks:** Storyboard, Beats, Assembled.
3. **The episode's point needs saying on screen.** Chris after cut 2: "how is
   x @ W correct in the previous video, and now x @ weight.T?" Episodes that
   rename a matrix across episodes should show the identity in code
   (`W = weight.T`) on the line that names it. Ep 6 (`X @ W`) inherits this.

## Rules → runbook / `agents/beat-brief-hyperframes.md` / `agents/style.md`

4. **No forced long final hold.** Trigger: I briefed "last ≥ 0.5 s still";
   all four agents dropped the last word's highlight to meet it (beats end
   in the pause midpoint, ~0.2 s after the last word). Fix that worked:
   mid-Short beats end on ≥ 5 still frames; only the last beat holds
   ≥ 0.8 s. Put the number in the beat brief so orchestrators don't invent one.
5. **Open on the code the viewer would write, then zoom in.** Chris after
   cut 1: "I don't really understand what this video is about at the
   beginning … show a basic network, no more than 5 lines, then zoom in."
   The fix (4-line `nn.Sequential`, zoom into its `nn.Linear` line, return
   to it at the end, code cards at beats 2–4) is a pattern for every
   PyTorch-specific episode: frame 0 is the model, not the layer.
6. **A Short may take dead air for a visual.** 1.0 s of silence inserted in
   the pause after VO line 1 bought beat 1 its zoom (Chris OK'd it). Runbook
   step 5: inserting silence at a pause is an alternative to re-recording.
7. **A plane sharing the stage with labelled matrices.** Chris: the plane at
   92 px a step "looks a little squished". Fix: drop the matrix names and
   shapes once the plane is in and lift the matrices (plane 118 px a step).
   Rule for `agents/style.md` "Linear algebra": names/shapes are shown while
   the VO is about the shape, and give way to the plane after.
8. **One letter, two matrices.** The VO says "W times v" (W = weight) then
   "x @ W" (W = weight.T). When the VO reuses a symbol, the screen labels
   each use (`W = weight`, `W = weight.T`).

## Parts → `agents/parts.md` and code (from the beat agents' wishes)

9. **Code-card swap** (one card giving way to another in place, the matrix
   names stepping aside): written locally in 02, 03, 04 and 06. Promote to
   `vec.js` (`VEC.swapCard`) or a shared helper.
10. **Card that zooms to one of its lines** (01: text-only card over a
    resizable panel, `clip-path` on the text). Same promotion candidate.
11. **`EP.network` options:** wire growth, ring pulse, separate ring colour
    and wire brightness, an alpha for fading the whole network. Five beats
    rewrote parts of it.
12. **More highlight boxes in `parts()`** (agents built 3–6 local hboxes),
    a per-arrow `u` and a width/colour pulse on the plane's arrows, and a
    pulse/glow on code-card spans.
13. **Swelling one character** of a label or card without retyping it as
    spans (spans break kerning; it moved "(2, 3)" 2 px and failed a seam).

## Tools

14. **`words.json` runs late inside phrases** (0.2–0.6 s here; one sentence
    end placed "two by three" in a silence). Every agent re-derived cues from
    the RMS envelope. Either fix `tools/word_times.py` (it spreads words by
    syllables across the phrase) or say in the brief that it is a first
    guess only.
15. **YouTube autocomplete from the shell:**
    `curl "https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q=..."`
    returns the suggestions as JSON (the `suggestqueries-clients6.youtube.com`
    host returns 400). Worth a `tools/yt_suggest.py` for runbook step 0.
16. **Captions over 4 words** (`x @ weight.T` counts as three) fail
    `assemble.py`; the fix was splitting the caption by hand.
