# Plan: promote the 2D plane kit

**Name:** linear-algebra-plane-kit
**Description:** Merge the per-episode copies of the flat 2D plane kit
(`_vec/vec.js`) into one shared script, the way 009's isometric kit became
`videos/_shared/web/iso/iso.js`.
**When to use:** once the Linear Algebra episodes being built in parallel
have shipped (no session is editing an episode's `_vec/`), before the next
episode starts a new copy.
**Status:** done 2026-10-11: `videos/_shared/web/vec/vec.js`, `tests/test_vec_kit.py`, `prototypes/hyperframes/vec-plane/`. Agent wishes not yet in the kit are listed in `agents/parts.md`.
**How it works:** one kit, `videos/_shared/web/vec/vec.js`, linked into each
beat as `vec/` like `iso/`. Episode numbers (the ledger) stay in each
episode, passed in rather than baked into the kit.

## Why now

The kit is past the two-use promotion rule (`agents/parts.md`): ep01 wrote
it, and ep03 and ep04 each copied and extended it. The copies already
disagree on names (ep01 `oy` per call; ep03 a camera `VEC.view`; ep04
`canon(Pt, …)`), and every new episode starts another fork.

## What goes in

| From | Parts |
|---|---|
| ep01 | `floor`, `arrow` (with `THIN`), `line`, `axes`, `guides`, `puck`, `label` / `place`, `vecCard` |
| ep03 | camera views `view(A, B, u)` with per-view axis extents; `lattice` (the moved grid); `basis` / `basisTo` / `comb` / `map`; `spot` (landing ring); `matCard` (rows in identity colours with tags) |
| ep04 | `grid`, `brackets` (the matrix notation in `agents/style.md`), `cell`, `headers`, `hbox` |
| agent wishes | `step()` getter; label offsets per view that avoid the band and the left dead zone; a recipe drawer (legs with hop ticks, `tick`); a ring of vectors; a code card (ep03 beat 6) |

## Steps

1. Diff the three copies; pick ep04's matrix notation as the default card
   (`agents/style.md` "Vectors and matrices as numbers"); ep03's `matCard`
   becomes an option or is dropped.
2. Write the shared kit with the episode ledger passed in; tests for the
   pure math (`map`, `basisTo`, view interpolation) under `tests/`.
3. Do not re-point shipped episodes: their beats keep their local `_vec/`
   (rendered output is the record). New episodes link the shared one.
4. Update `agents/parts.md`, `agents/style.md` "Linear algebra" (the code
   path), `SERIES.md` series rules, `EPISODE_PROMPT.md` (copy step goes
   away), changelog.
