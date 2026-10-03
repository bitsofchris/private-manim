# Research digest: what other LLM-to-Manim pipelines learned

**Name:** llm-to-manim-pipelines
**Description:** TLDR of the published systems that turn a prompt into a
Manim video, what each found, and the handful of rules worth borrowing.
One agent report, 2026-10-03, read from arXiv pages and repo prompts (not
full PDFs); numbers are as those pages state them.
**When to use:** before changing how beats are planned, briefed, checked
or repaired. Feeds `agents/plans/design-system.md`.

## The one finding that matters

Layout is the weakest score in every system that relies on prompt rules
alone, and it only improves when structure is in code. TheoremExplainAgent
wrote careful layout rules into its prompts and still scored 0.61 on
element layout. Code2Video put a named grid in a base class and scored
90.6 against 30.5 for free-form code (hand-made 3Blue1Brown: 98.3). That
is our experience too: every 008 fix was a layout fix.

## The systems, one paragraph each

- **Code2Video** (planner → parallel coders → render → vision critic).
  The canvas is a 6×6 grid of named cells; a base class has
  `place_at_grid` and `place_in_area`; an occupancy table records what
  sits where. The critic returns at most three fixes, each naming the
  object, the source line and the target cell. Repairs go smallest scope
  first: the line, then the block, then the section. Ablations: no planner
  costs 41 points, no grid 10–27, no critic 7–21; parallel coding cut 87
  minutes to 15. Humans notice brief occlusions the vision judge misses.
  https://arxiv.org/abs/2510.01174
- **TheoremExplainAgent** (planner → coder → error-fix loop, with docs
  retrieval). Four plan documents per video. Layout by prompt: 0.5-unit
  margin, 0.3 spacing, relative positioning only, fixed font tiers, wrap
  over ten words. Docs retrieval *lowered* success for strong models
  (93.8% → 82.1%) and only helped weak ones. Failure list: hallucinated
  APIs, LaTeX errors, overlapping text, inconsistent sizes.
  https://arxiv.org/abs/2502.19400
- **ManimAgent** (storyboard → coder with memory → render → text review →
  vision review → revise). Two kinds of memory: reference examples
  (passing scenes) and known pitfalls (trigger, root cause, fix recipe,
  good and bad example), written only when the fix measurably helped.
  First-try pass went 62% → 85% and review rounds halved. Loops are
  bounded (two visual rounds, stop on a repeated error class) and it ships
  the best-scoring take, not the last. Its vision judge agreed poorly with
  humans. https://arxiv.org/abs/2606.30296
- **Manimator** (scene description → code → render, no review). Credits
  its layout score mostly to the choice of code model.
  https://arxiv.org/abs/2507.14306
- **LLM2Manim** (brief → scene plan → narration and code in parallel →
  timed assembly). The plan template has a symbol ledger (so notation
  doesn't drift), narration cues, and an allowed-primitives list. Overlaps
  were fixed by a human editing only the broken part. Students learned
  more from it than from slides (d = 0.67). https://arxiv.org/abs/2604.05266
- **ManiBench** (benchmark). Few-shot examples were the only prompting
  strategy that raised success on a weak model; rule lists and
  chain-of-thought did not. https://arxiv.org/abs/2603.13251

## What we already do that they confirm

A planner before code (their biggest single effect), parallel coders per
beat, a human-recorded voice setting exact beat lengths, a frame review
before shipping, a pinned Manim version, and a traps list.

## What to borrow (small, in order)

1. **Named cells instead of free coordinates.** A grid over the stage
   (say 4 columns × 6 rows) with `place_at(cell)` and `place_in(cell_a,
   cell_b)` on `BocShortScene`. The storyboard says which cell each thing
   sits in, so the layout is decided before any code. This is the single
   biggest lever in the literature and it attacks our one recurring bug.
2. **Check geometry in code.** The planned `check_layout()`: text width
   against the safe area, pairwise overlap, margins. Vision review misses
   things and disagrees with people; a bounding-box check doesn't.
3. **Worked examples over rules.** Point each beat agent at two or three
   of our own passing beats that resemble its brief, not only at the rule
   docs. Evidence says examples beat rule lists, and docs retrieval can
   hurt a strong model.
4. **Pitfalls with a recipe.** Our traps list becomes entries with
   trigger, cause, fix and a bad example, and a trap is added only after
   the fix worked. That is what the update pass should write.
5. **Smallest repair first.** When a review finds a problem, fix the line,
   then the block, and only then rewrite the beat. Reviews name the object
   and the line.
6. **Bounded loops.** Two review rounds per beat; if the same class of
   error repeats, stop and escalate to the orchestrator.
7. **A ledger in the storyboard.** The fixed names, labels and example
   values used across beats ("bug / query / spam", "I can't log in"), so
   agents working in parallel don't drift.

Not borrowing: docs retrieval (hurts strong models), a vision-model score
as the gate (poor agreement with people), four plan documents (one
storyboard is enough at 60 seconds).
