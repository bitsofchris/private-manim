# Design-system changelog

One line per change to a rule, token, part, tool, or doc, with the video
that forced it. Newest first.

## 2026-10-04

- HyperFrames is the default engine for Shorts; Manim stays for axes and plotted data, 3D camera moves, existing shared parts and all 16:9 scenes (`AGENTS.md` "Which engine"). Nothing Manim is retired. (Chris, after 009)
- `videos/009-transformer-short-iso/`: 005 rebuilt beat for beat in an isometric HyperFrames look over the same VO and captions; final at `media/transformer_short_hyperframe.mp4`. Its kit `_iso/iso.js` is the first shared HyperFrames script, linked into each beat by symlink; `00_layout/` is the canonical frame; `BRIEF.md` is the contract four parallel agents built to. (009)
- Matrix tiles, words and digits are coloured by token column (my teal, name blue, is gold; a darker shade for a negative value), not by sign, so a column reads as belonging to its word. The blue `#60A5FA` is new and lives only in the kit until a second video needs it in `style.py`. (Chris, 009)
- The head beat ends on the output: the whole tray sinks into the head and `Chris` comes out the other side; bars and label flips removed. (Chris, 009)
- `agents/beat-brief-hyperframes.md`: "What `check` and the renderer trip on" (transform-only tweens, timeline registration in the beat file, canvas and blend-mode text unseen by the audit, the `data-layout-allow-*` waivers, generic `serif` fails, grain file size, the 60 px width budget) and "One driver, and a shared kit". (stack-styles, 009)
- `prototypes/hyperframes/stack-styles/`: one five-second beat in ten styles plus the house-style control, with a scaffold and a builder brief. `agents/research/2026-10-04-hyperframes-styles.md` holds the style research behind it. (experiment)
- Candidates for the kit when it is promoted (written locally in 009's beats): round-capped `line` / `dot`, `traveller`, `flashEdge`, world-space arcs with partial draw, a `clipZ` option on `ISO.tray` (the sinking tray), a slab with a well, `slabStack`, a glow colour option on slabs, an x offset for the view, a cross-fading label flip. (009)
- Open: only Inter ExtraBold is vendored. A lighter weight or a condensed face would loosen every layout; a serif is needed for an editorial look. Adding one is a new asset and Chris's call.

## 2026-10-03

- HyperFrames ecosystem map in `agents/research/`, linked from the HyperFrames beat brief. (research)
- HyperFrames is a second engine for Short beats, chosen at storyboard time: `ENGINE:` line at the top of `storyboard.md`; Manim for diagrams, math, code, data; HyperFrames for characters, props, UI mock-ups, abstract ideas (`AGENTS.md` "Which engine", runbook steps 1 and 6). No house template yet. (Chris)
- `agents/beat-brief-hyperframes.md`: the beat contract for HyperFrames (folder `NN_beat/index.html` + `vendor` symlink, render to `media/hf/NN_beat.mp4`, palette from `style.py`, safe area in px, band empty with VO). `agents/beat-brief.md` now says it is the Manim brief. (Chris)
- HyperFrames renders offline: GSAP 3.14.2 and Inter 4.1 ExtraBold vendored in `videos/_shared/web/vendor/` with sha256; the prototypes load them through a `vendor` symlink (HyperFrames rejects `../` paths) and a local `@font-face` (no Google Fonts fetch); npm scripts use `--prefer-offline` and turn off telemetry. Verified by rendering both prototypes with outbound network denied. Guard: `tests/test_hyperframes_offline.py`. (Chris)
- `agents/parts.md`: what to copy from the two HyperFrames prototypes. (Chris)
- Janitor: runbook steps renumbered cleanly (one step 0, step 11 in order, tools last); its "next one, in practice" removed (README owns Chris's side) and its backlog moved to `agents/plans/design-system.md`; dead path to the archived pipeline plan fixed; style guide's Shorts caption row aligned with hard rule 6. (janitor)
- From the pipelines research: storyboard ledger and "if time" last line (runbook 1); worked examples named per agent (runbook 6, beat brief); smallest repair first and two review rounds (runbook 8, beat brief); traps recorded as trigger / cause / fix once the fix worked (runbook 11). (research)
- HyperFrames prototypes under `prototypes/hyperframes/`; not yet a path in the process. (experiment)

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
