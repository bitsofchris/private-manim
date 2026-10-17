# private-manim: start here

Explainer Shorts (9:16, 45–60 s) in HyperFrames (HTML / SVG / canvas
rendered by headless Chrome), the default engine since 2026-10-04, and in
Manim Community 0.18.1, which also makes the 16:9 explainer scenes, all in
the Bits of Chris house style.
Chris records the voice; agents build every visual. This file is the single entry point: the map,
the rules of precedence, how a session runs, and how the repo stays clean.
Everything agents maintain lives in `agents/`; code lives in `videos/_shared/`
and `tools/`; videos live in `videos/NNN-slug/`. If something here
disagrees with another file, fix it here first (see "Keeping the system
clean").

## The map

| You want | Go to | Owns |
|---|---|---|
| The process for a Short, start to hand-off | `agents/runbook.md` | steps 0–12, tools, what to hand Chris |
| The process for a series: arc, scripts, one recording split per episode, one session per episode | `agents/series.md` | the series-level steps and the episode-prompt template; each episode then runs the runbook |
| The brief a beat-building subagent gets | `agents/beat-brief.md` (Manim) / `agents/beat-brief-hyperframes.md` (HyperFrames) | the contract every beat must meet |
| Tokens: colors, type, durations, strokes, safe areas | `videos/_shared/style.py` | the only place a constant lives |
| How to use the tokens; what to use for X; Manim traps | `agents/style.md` | the "want X, use Y" tables |
| When and how things move | `agents/animation-rules.md` | 15 sourced rules |
| What already exists to reuse | `agents/parts.md` | inventory of shared and per-video parts, naming, promotion |
| Shared code | `videos/_shared/*.py` | scene bases, mobjects, the transformer diagram |
| Vendored web assets (GSAP, Inter) | `videos/_shared/web/vendor/` | offline HyperFrames renders; versions, licenses, sha256 in its README |
| HyperFrames worked examples | `prototypes/hyperframes/` | two silent Shorts with field notes; `stack-styles/`, one beat in ten visual styles plus the house-style control |
| A whole Short in HyperFrames, and its isometric kit | `videos/009-transformer-short-iso/` | `videos/_shared/web/iso/iso.js` (world, tray, card, slabs, palette), `00_layout/` (the canonical frame), `BRIEF.md` (the beat contract) |
| The Linear Algebra for AI Engineers series (2D plane look) | `videos/002-linear-algebra-basics/` | `SERIES.md` (arc, checklist, series rules), `EPISODE_PROMPT.md` (one session per episode), the plane kit is shared: `videos/_shared/web/vec/vec.js`, starter `prototypes/hyperframes/vec-plane/` |
| Line-drawn agents and knowledge bases (human, agent with 1 and 0 eyes, janitor, layer props) | `videos/_shared/web/cast/cast.js` | the cast kit; starter and sign-off frame `prototypes/hyperframes/cast/`; rules in `agents/style.md` "Agents and knowledge bases" |
| The Classifier Metrics series (five Shorts: the accuracy trap / confusion matrix, precision vs recall, ROC, AUC and the PR curve, the operating point) | `videos/013-classifier-metrics/` | `SERIES.md` (ledger, the two recurring images, search phrases, checklist), `_data/make_scores.py` (every number, seed 13), each episode's `_kit/score.js` |
| The Harness Engineering series (four Shorts: the harness, the map, the four-layer knowledge base, not keeping agents busy) | `videos/012-harness-engineering/` | `SERIES.md` (the episodes, what was cut, checklist), `TRANSCRIPT.md` (the full take), each `epNN/script.md` (what was said, cut times); the dropped plan is in `_archive/` |
| Audio and assembly tools | `tools/` | tighten, word fixes, beat cuts, captions, assemble, contact sheets, seam check |
| Tests | `tests/` | `uv run --no-sync python -m unittest discover -s tests` |
| What changed in the system and why | `agents/changelog.md` | one line per rule, token, part, or tool change |
| Evidence behind the rules | `agents/research/` | digests with sources: shorts craft and hooks; what other LLM-to-Manim pipelines learned |
| What is working on the channel | `~/repos/yt-stats` (`sync`, then `report`) | every Short's stats: search terms, traffic sources, retention, subs; read at runbook step 12 |
| Plans in flight / done | `agents/plans/` / `agents/archive/` | |
| A finished video | `videos/NNN-slug/` | storyboard, VO, scenes, `publish.md`, `media/` (gitignored) |
| Retired code | `videos/_graveyard/` | kept for reference, never imported |

## Which engine

Chosen per Short at storyboard time (runbook step 1) and written as the
first line of `storyboard.md`: `ENGINE: manim` or `ENGINE: hyperframes`.
A Short may mix engines (`ENGINE: mixed`); then each beat row names its
engine.

- **HyperFrames is the default** (Chris, 2026-10-04, after 009 rebuilt a
  whole technical Short in it: matrices, a block diagram, attention arcs,
  small networks). Renders take seconds, its `check` lints layout and
  contrast, and the look is not tied to Manim's primitives.
- **Manim** when the beat needs what it has and a canvas does not: real
  axes and plotted data, 3D camera moves, an existing shared part in
  `videos/_shared/` that would cost more to redraw than to reuse, and all
  16:9 scenes. Nothing Manim is retired; the Manim rules below stand.

Both engines share the house style (palette, safe area, one magenta hero,
captions burned in by `tools/assemble.py`) and the whole process; only
step 6 (the beat brief and the render command) differs.

## Hard rules (the ones that break the repo or the signature)

Rules 1, 3–5, 7 and 8 are Manim's; a HyperFrames beat follows
`agents/beat-brief-hyperframes.md`, which carries 1, 2 and 6 over.

1. **Constants come from `videos._shared.style`.** Never hardcode a color,
   font, duration, stroke width, or safe-area number in a scene. Missing
   constant: add it to `style.py` first.
2. **Two heroes.** Teal (`S.DATA`) is data you can see; magenta
   (`S.STRUCTURE`) is the discovered structure. One magenta hero on screen
   at a time (one thing, or one tight group such as a matrix row and the
   arrow it makes); when the VO moves on it may pass to the next thing and
   the old one returns to rest.
3. **Subclass the house scenes:** `BocShortScene` for Shorts, `BocScene` /
   `Boc3DScene` for 16:9. Use the preconfigured mobjects for their roles.
4. **Three durations:** `S.QUICK` / `S.BEAT` / `S.HOLD` (multiples of HOLD
   for long rides). Never `self.wait(0.45)`.
5. **Render from inside the video folder**, one scene at a time, with
   `--disable_caching` for finals:
   `cd videos/NNN-slug && uv run --no-sync manim -qh --disable_caching FILE.py Class`.
   Never from the repo root (it scatters `media/`); never two renders in
   one folder at once (they race on the text cache).
6. **Captions:** in a Short with VO, word captions are burned in by
   `tools/assemble.py` and scenes draw nothing in `self.band`. In-scene
   `show_caption` is for 16:9 scenes and VO-less clips only.
7. **No LaTeX on this machine.** `Text` only, never `MathTex` / `Tex`.
8. **One Scene class per file, ~120 lines.** Shared helpers go in a local
   `_parts.py` (see `agents/parts.md`), never duplicated across files.

Precedence when files disagree: `style.py` (tokens) → this file (rules)
→ `agents/style.md` / `agents/animation-rules.md` (how and when) → runbook (process)
→ a video's storyboard (that video only).

## How a session runs

Chris opens a session with a big model (Fable) as the orchestrator. The
orchestrator does the judgment work and farms out the parallel work:

| Step | Who | What |
|---|---|---|
| Preflight + storyboard | orchestrator | the preflight from runbook step 0 (the question, who asks, the one-sentence answer), then `storyboard.md` from the runbook step 1, starting with the `ENGINE:` line. Chris edits the VO in his words. |
| Record | Chris | one take, `vo_raw.m4a` into the video folder |
| Clean, transcribe, cut | orchestrator | runbook steps 3–5; Chris approves the cut list and, for a new look, the canonical frame, in one message (runbook step 6) |
| Build beats | subagents (one per 1–2 beats) | each gets the brief for its beat's engine + its beat's VO and visual brief; renders and reviews its own contact sheet |
| Assemble + review | orchestrator | sequential clean re-render, assemble, contact sheets, fix what the sheets show |
| Iterate | Chris + orchestrator | Chris watches on a phone and says what's off; every change request is material for the update pass |
| Hand-off | orchestrator | runbook step 10: file path, title, description, Substack note |
| Update pass | orchestrator, when Chris says go | runbook step 11: janitor the docs, mine the session for what to add, changelog, commit |

A subagent never edits `videos/_shared/`; it reports what it wished existed
and the orchestrator decides whether it becomes a rule, a token, or a part.

## Keeping the system clean (janitor rules)

One home per topic, from the map above. When you learn something:

- A constant → `style.py`. A "use X for Y" → `agents/style.md`. A "move it this
  way" → `agents/animation-rules.md`. A process step → the runbook. A reusable
  thing → a part, listed in `agents/parts.md`. Evidence → `agents/research/`.
  Everything else → `agents/changelog.md` as a lesson line.
- Never state the same rule in two files. Link instead. If you find a
  duplicate or a contradiction, resolve it toward the precedence order
  and note it in `agents/changelog.md`.
- After the hand-off pack, ask Chris: "Ready for the update pass?" On yes
  (runbook step 11): go back through the session for every change Chris
  asked for and every workaround an agent made, and decide for each
  whether it becomes a rule, a token, a part, a tool, or nothing; make
  those edits in their one home; update `agents/parts.md` use counts and
  promote anything at two uses; move finished plans to `agents/archive/`;
  move retired scene files to `videos/_graveyard/`; delete `_preview.py`
  files; re-read this file and `agents/` for anything stale or
  contradictory; add changelog lines; commit separately from the video.
- Commit small and often: one concern per commit, scenes separate from
  system changes.
