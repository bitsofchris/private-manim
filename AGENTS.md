# private-manim: start here

Explainer Shorts (9:16, 45–60 s) and 16:9 explainer scenes in Manim
Community 0.18.1, with HyperFrames (HTML/SVG rendered by headless Chrome)
as a second engine for Short beats, in the Bits of Chris house style.
Chris records the voice; agents build every visual. This file is the single entry point: the map,
the rules of precedence, how a session runs, and how the repo stays clean.
Everything agents maintain lives in `agents/`; code lives in `videos/_shared/`
and `tools/`; videos live in `videos/NNN-slug/`. If something here
disagrees with another file, fix it here first (see "Keeping the system
clean").

## The map

| You want | Go to | Owns |
|---|---|---|
| The process for a Short, start to hand-off | `agents/runbook.md` | steps 0–11, tools, what to hand Chris |
| The brief a beat-building subagent gets | `agents/beat-brief.md` (Manim) / `agents/beat-brief-hyperframes.md` (HyperFrames) | the contract every beat must meet |
| Tokens: colors, type, durations, strokes, safe areas | `videos/_shared/style.py` | the only place a constant lives |
| How to use the tokens; what to use for X; Manim traps | `agents/style.md` | the "want X, use Y" tables |
| When and how things move | `agents/animation-rules.md` | 15 sourced rules |
| What already exists to reuse | `agents/parts.md` | inventory of shared and per-video parts, naming, promotion |
| Shared code | `videos/_shared/*.py` | scene bases, mobjects, the transformer diagram |
| Vendored web assets (GSAP, Inter) | `videos/_shared/web/vendor/` | offline HyperFrames renders; versions, licenses, sha256 in its README |
| HyperFrames worked examples | `prototypes/hyperframes/` | two silent Shorts with field notes |
| Audio and assembly tools | `tools/` | tighten, captions, assemble, contact sheets |
| Tests | `tests/` | `uv run --no-sync python -m unittest discover -s tests` |
| What changed in the system and why | `agents/changelog.md` | one line per rule, token, part, or tool change |
| Evidence behind the rules | `agents/research/` | digests with sources: shorts craft and hooks; what other LLM-to-Manim pipelines learned |
| Plans in flight / done | `agents/plans/` / `agents/archive/` | |
| A finished video | `videos/NNN-slug/` | storyboard, VO, scenes, `publish.md`, `media/` (gitignored) |
| Retired code | `videos/_graveyard/` | kept for reference, never imported |

## Which engine

Chosen per Short at storyboard time (runbook step 1) and written as the
first line of `storyboard.md`: `ENGINE: manim` or `ENGINE: hyperframes`.
A Short may mix engines (`ENGINE: mixed`); then each beat row names its
engine.

- **Manim** for diagrams, math, code, data: anything with axes, arrows
  between named parts, or a shared part in `videos/_shared/`.
- **HyperFrames** for characters, props, UI mock-ups, abstract ideas.

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
   (`S.STRUCTURE`) is the discovered structure. One magenta hero per beat.
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
| Preflight + storyboard | orchestrator | `content-preflight` (the question, who asks, the one-sentence answer), then `storyboard.md` from the runbook step 1, starting with the `ENGINE:` line. Chris edits the VO in his words. |
| Record | Chris | one take, `vo_raw.m4a` into the video folder |
| Clean, transcribe, cut | orchestrator | runbook steps 3–5; Chris approves the cut list |
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
