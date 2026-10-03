# private-manim: start here

Explainer Shorts (9:16, 45–60 s) and 16:9 explainer scenes in Manim
Community 0.18.1, in the Bits of Chris house style. Chris records the voice;
agents build every visual. This file is the single entry point: the map,
the rules of precedence, how a session runs, and how the repo stays clean.
If something here disagrees with another file, fix it here first (see
"Keeping the system clean").

## The map

| You want | Go to | Owns |
|---|---|---|
| The process for a Short, start to hand-off | `docs/shorts-runbook.md` | steps 0–11, tools, what to hand Chris |
| The brief a beat-building subagent gets | `docs/beat-agent-brief.md` | the contract every beat scene must meet |
| Tokens: colors, type, durations, strokes, safe areas | `videos/_shared/style.py` | the only place a constant lives |
| How to use the tokens; what to use for X; Manim traps | `videos/_shared/STYLE.md` | the "want X, use Y" tables |
| When and how things move | `videos/_shared/ANIMATION_RULES.md` | 15 sourced rules |
| What already exists to reuse | `videos/_shared/PARTS.md` | inventory of shared and per-video parts, naming, promotion |
| Shared code | `videos/_shared/*.py` | scene bases, mobjects, the transformer diagram |
| Audio and assembly tools | `tools/` | tighten, captions, assemble, contact sheets |
| Tests | `tests/` | `uv run --no-sync python -m unittest discover -s tests` |
| What was learned per video | `docs/retros/` | one retro per video, from `TEMPLATE.md` |
| What changed in the system and why | `videos/_shared/CHANGELOG.md` | one line per rule, token, part, or tool change |
| Evidence behind the rules | `docs/research/` | digests with sources |
| Plans in flight / done | `docs/plans/` / `docs/archive/` | |
| A finished video | `videos/NNN-slug/` | storyboard, VO, scenes, `publish.md`, `media/` (gitignored) |
| Retired code | `videos/_graveyard/` | kept for reference, never imported |

## Hard rules (the ones that break the repo or the signature)

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
   `_parts.py` (see `PARTS.md`), never duplicated across files.

Precedence when files disagree: `style.py` (tokens) → this file (rules)
→ `STYLE.md` / `ANIMATION_RULES.md` (how and when) → runbook (process)
→ a video's storyboard (that video only).

## How a session runs

Chris opens a session with a big model (Fable) as the orchestrator. The
orchestrator does the judgment work and farms out the parallel work:

| Step | Who | What |
|---|---|---|
| Preflight + storyboard | orchestrator | `content-preflight` (the question, who asks, the one-sentence answer), then `storyboard.md` from the runbook step 1. Chris edits the VO in his words. |
| Record | Chris | one take, `vo_raw.m4a` into the video folder |
| Clean, transcribe, cut | orchestrator | runbook steps 3–5; Chris approves the cut list |
| Build beats | subagents (one per 1–2 beats) | each gets `docs/beat-agent-brief.md` + its beat's VO and visual brief; renders and reviews its own contact sheet |
| Assemble + review | orchestrator | sequential clean re-render, assemble, contact sheets, fix what the sheets show |
| Iterate | Chris + orchestrator | Chris watches on a phone and says what's off; every change request is recorded for the retro |
| Hand-off | orchestrator | runbook step 10: file path, title, description, Substack note |
| Retro + janitor | orchestrator | runbook step 11: `docs/retros/NNN-slug.md`, changelog, parts inventory, this file |

A subagent never edits `videos/_shared/`; it reports what it wished existed
and the orchestrator decides whether it becomes a rule, a token, or a part.

## Keeping the system clean (janitor rules)

One home per topic, from the map above. When you learn something:

- A constant → `style.py`. A "use X for Y" → `STYLE.md`. A "move it this
  way" → `ANIMATION_RULES.md`. A process step → the runbook. A reusable
  thing → a part, listed in `PARTS.md`. Evidence → `docs/research/`.
  Everything else → the retro.
- Never state the same rule in two files. Link instead. If you find a
  duplicate or a contradiction, resolve it toward the precedence order
  and note it in `CHANGELOG.md`.
- After every video (runbook step 11): write the retro; update
  `PARTS.md` use counts and promote anything at two uses; move finished
  plans to `docs/archive/`; move retired scene files to
  `videos/_graveyard/`; delete `_preview.py` files once the beats exist;
  re-read this file and fix anything stale.
- Commit small and often: one concern per commit, scenes separate from
  system changes.
