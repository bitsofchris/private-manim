# Design-system changelog

One line per change to a rule, token, part, tool, or doc, with the video
that forced it. Newest first.

## 2026-10-03

- Everything agents maintain moved under `agents/` (runbook, beat brief, style, animation rules, parts, changelog, research, plans, archive). Code stays in `videos/_shared/` and `tools/`. (janitor)
- No retro files: the update pass (runbook step 11) mines the session and writes straight into the rules, parts and changelog. (Chris)
- Repo entry point: `AGENTS.md` is the map and the rules; `CLAUDE.md` points at it; `README.md` is for humans. (janitor)
- `agents/beat-brief.md` replaces the per-session contract file for beat subagents. (008)
- `agents/parts.md` inventory; promote at second use; `videos/_graveyard/` for retired scenes. (008)
- `agents/style.md`: removed the "math = LaTeX" rows (no LaTeX on this machine); caption rows split into 16:9 in-scene vs Shorts burned-in; render example moved into a video folder. (janitor)
- Hook rule in the runbook: frame 0 = the finished visual already working, with the question as on-screen text; question spoken in the first second; takeaway last, no outro. (research digest)
- Captions bold on a dark pill: `SHORT_CAPTION_WEIGHT`, `CAPTION_PILL_OPACITY`, `CAPTION_PILL_PAD`; `short_caption(pill=True)`. (008)
- `transformer.py`: `BOX_PAD` 0.08, `ADD_RADIUS` 0.26, `BOTTOM_BLEED` 0.45, `ARROW_GAP` 0.06. (006, 008)
- Runbook steps 9–10: title/description rules, hand-off pack, no pinned comments. (006)
- Runbook: finals render with `--disable_caching`, one scene per folder at a time; Descript takes get loudnorm only. (006, 007)

### Lessons from 008 (would have been the retro)

- A word cloud is decoration: frame 0 is the finished visual already working.
- Nine pieces at the text floor do not fit one stage: budget rows and widths before building; merge beats that share a visual.
- Captions must not read as diagram labels: pill + bold.
- The example must be a decision someone would make (ticket → bug / query / spam, not "server down → yes / no / later").
- A badge on a corner reads as "brand"; a tree reads as "is-a".
- Numbers go in the description, not on screen, in a 60 s Short.
- Storyboards mark the last script line "if time"; the take dropped it.
- Open: no layout check before render; no on-screen question at frame 0.

## 2026-10-01

- `transformer.py`: shared transformer block diagram with named parts and the matching PyTorch. (006, 007)
- `BocShortScene`, safe area, `hold_until`, `short_caption`, assembly tools. (004)
