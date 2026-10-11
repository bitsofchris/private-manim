# Design-system changelog

One line per change to a rule, token, part, tool, or doc, with the video
that forced it. Newest first.

## 2026-10-11

- `agents/style.md` "Vectors and matrices as numbers": a matrix acting on the plane is on screen when the VO says "this matrix", and the row doing the work lights while its direction moves; pointing at a row is magenta digits first, a box only if colour is not enough. (Chris, ep03)
- `agents/style.md` "Linear algebra": named camera views in the kit for numbers that don't fit one scale (ep03 `VEC.view`). (ep03)
- `agents/style.md` "Share the band": the element's bottom edge ≤ y 1330 and every caption on one line while it is up; a two-line caption grew into ep03's code card. Runbook step 7 now points there instead of restating it. (ep03)
- Beat brief trap: monospace set in the HTML (CSS class, ep01; inline `style` attribute, ep03) rendered in Inter; set `el.style.fontFamily` from the script. `agents/style.md`'s code row points to the trap instead of restating it. (ep03)
- Beat brief review: pixel-diff seams with `hyperframes snapshot` PNGs, not mp4 frames (h264 noise up to ~60/255 around text). (ep03)
- Hero rule, janitor: `AGENTS.md` rule 2 is the one home and says "one magenta hero on screen at a time; it may pass when the VO moves on", which is how ep01–ep03 were built and approved; `agents/style.md`, `agents/animation-rules.md` rule 12 and the HyperFrames brief said "per beat" and now point to it. (janitor)
- The 2D plane kit is shared: `videos/_shared/web/vec/vec.js` merges ep01's plane, ep03's camera views and linear map, and ep04's matrix notation, with a code card; tests in `tests/test_vec_kit.py`; starter `prototypes/hyperframes/vec-plane/`. Shipped episodes keep their `_vec/` copies; new episodes link the shared kit (`SERIES.md`, `EPISODE_PROMPT.md`, `agents/style.md`, `agents/parts.md`, `AGENTS.md` map). Plan archived. (ep01, ep03, ep04)
- `SERIES.md`: episode 3 ticked (Storyboard, Beats, Assembled); its section brought up to the build. (ep03)
- `tools/seam_check.py`: snapshots both sides of every HyperFrames cut, pixel-diffs them, writes side-by-side PNGs; runbook step 8 and the beat brief point to it. All seven ep03 cuts diff at 0/255. (ep03)
- `iso.js` `ISO.start` draws again on `document.fonts.ready`: a snapshot at t = 0 placed width-measured DOM text ~66 px off (ep03 00_layout card); verified to match the mp4 after the fix. Renders were never affected. (ep03)
- Beat brief: never `hyperframes snapshot` without `--describe false`; it sends frames to Gemini whenever `GEMINI_API_KEY` is set. (janitor)
- Runbook step 4, MacWhisper Pro measured: Parakeet v3 gives word timings but they are coarser than `word_times.py` on Whisper Small (median 0.12 s vs 0.045 s on ep03's 14 hand cues); Whisper Small stays for timing (always pass `--model`, the app default is now Parakeet), Parakeet v3 becomes the spelling reference for captions; `--overwrite` replaces the rm-first gotcha. (Chris, ep03)
- `tools/word_times.py` → `words.json` in runbook step 5: every word's start from the phrase transcript and the audio envelope, no model or new dependency. ep03 check against 14 hand-found cues: median error 0.045 s, worst 0.24 s. Beat briefs start cues from it; sub-clips only for a missing or misheard word. MacWhisper Pro does not help: its v15 CLI has no word-level timestamps (runbook step 4 corrected). Closes ep02's tool item 10. (Chris, ep03)
- Text floor, one per engine, said once in `agents/style.md` (Shorts rules): Manim `SHORT_LABEL_SCALE` (~96 px line height), HyperFrames 60 px font-size at weight 800 (the brief), the size every HyperFrames Short (009–011, ep01–ep04) passed on a phone. (janitor)

## 2026-10-10

- `agents/style.md` "Vectors and matrices as numbers": the default notation for tensors on screen. Vectors are a bracketed row with commas, matrices are bare numbers in brackets with no cell boxes, shapes are written as `(3, 2)`, monospace only for code, and colour goes on digits per row. Deviate when it clearly helps a video. (Chris, ep04)
- `agents/style.md` "Linear algebra": a flat 2D number plane, not the isometric floor, for vectors and coordinates; at least ±2 steps, ~165 px per step; a vector the viewer reads gets axes, ticks and guides to its coordinates; thin arrows (`VEC.THIN`); the hero by colour alone, no halo; more dimensions are more axes, never more arrows. (Chris, ep01)
- `agents/style.md` "Linear algebra": 3D change of basis as floor + stalk + route, never a 3D lattice; ghost grid alpha ~0.14; a basis that keeps v3 fixed; no camera drift across cuts. (ep02)
- Runbook step 0: no question text with VO; the band is the captions' (AGENTS.md rule 6 wins over the runbook, as the precedence order says). Both ep01 and ep02 had already dropped it. (ep02)
- Runbook step 6: show Chris the canonical `00_layout` frame before spawning beat agents when the look is new; ep01 and ep02 each assembled a whole Short in a look that was then rejected. (ep01, ep02)
- Runbook step 8: check every cut side by side; parallel agents rebuild a neighbour's end state from the brief and drift (three cuts in ep01). Beat brief: match the previous beat's rendered last frame when it exists. A rework resumes the same agents by name. (ep01, ep02)
- Beat brief trap: monospace set by a CSS class rendered in Inter; set it inline. (ep01)
- `style.py`: `CONTENT_BLUE = "#60A5FA"`, the second categorical slot, already used by 009–011 and ep02. (ep02)
- `agents/parts.md`: ep01's 2D plane kit and ep02's 3D basis kit listed as local parts, with the helpers their agents wished for. (ep01, ep02)
- `SERIES.md`: folder-depth note in the series rules; ep02 ticked and its section brought up to the build. `EPISODE_PROMPT.md`: the 2D look, the canonical-frame OK and the cut check. `AGENTS.md` map: the series row. (ep01, ep02)
- Lesson: on these Studio Sound takes, loudnorm lands near −16.5 LUFS because the −1.5 dBTP ceiling caps it; 006–008 sit at −16.3 to −15.9, so it matches. (ep01)
- Open: ep02's tool items, spoken-number captions in `captions_from_transcript.py` and a word-timing helper (`ep02-change-of-basis/update-pass.md` items 9–10).

## 2026-10-09

- The preflight is a runbook step (step 0), not an outside skill: `AGENTS.md` and the runbook no longer name `content-preflight`. The repo process is self-contained. (Chris)
- Hook rule: the first spoken line is the answer plus why it matters, never the question. Replaces "question spoken in the first second". Lives in runbook step 1 ("VO line 1"), where the script is written, with a check before hand-off; step 0 points to it. The question stays as on-screen text. (Chris, linear algebra scripts)
- `videos/002-linear-algebra-basics/SERIES.md` and `SCRIPTS.md`: the Linear Algebra for Engineers arc, checklist, titles and VO scripts for 10 episodes plus a trailer. (002)

## 2026-10-04

- HyperFrames is the default engine for Shorts; Manim stays for axes and plotted data, 3D camera moves, existing shared parts and all 16:9 scenes (`AGENTS.md` "Which engine"). Nothing Manim is retired. (Chris, after 009)
- `videos/009-transformer-short-iso/`: 005 rebuilt beat for beat in an isometric HyperFrames look over the same VO and captions; final at `media/transformer_short_hyperframe.mp4`. Its kit `_iso/iso.js` is the first shared HyperFrames script, linked into each beat by symlink; `00_layout/` is the canonical frame; `BRIEF.md` is the contract four parallel agents built to. (009)
- Matrix tiles, words and digits are coloured by token column (my teal, name blue, is gold; a darker shade for a negative value), not by sign, so a column reads as belonging to its word. The blue `#60A5FA` is new and lives only in the kit until a second video needs it in `style.py`. (Chris, 009)
- The head beat ends on the output: the whole tray sinks into the head and `Chris` comes out the other side; bars and label flips removed. (Chris, 009)
- `agents/beat-brief-hyperframes.md`: "What `check` and the renderer trip on" (transform-only tweens, timeline registration in the beat file, canvas and blend-mode text unseen by the audit, the `data-layout-allow-*` waivers, generic `serif` fails, grain file size, the 60 px width budget) and "One driver, and a shared kit". (stack-styles, 009)
- `prototypes/hyperframes/stack-styles/`: one five-second beat in ten styles plus the house-style control, with a scaffold and a builder brief. `agents/research/2026-10-04-hyperframes-styles.md` holds the style research behind it. (experiment)
- Candidates for the kit when it is promoted (written locally in 009's beats): round-capped `line` / `dot`, `traveller`, `flashEdge`, world-space arcs with partial draw, a `clipZ` option on `ISO.tray` (the sinking tray), a slab with a well, `slabStack`, a glow colour option on slabs, an x offset for the view, a cross-fading label flip. (009)
- `agents/style.md`: "The isometric house look": objects are isometric, anything read exactly is a flat upright card; one colour per token or choice; the floor in every beat. (Chris, after 009-011)
- 010 (006 rebuilt) and 011 (008 rebuilt) in the isometric look; `_diagram/diagram.js` is the transformer figure with its marks and bottom-to-top flow locked; `_jev/jev.js` holds probability pillars, labelled slabs and flat cards. (010, 011)
- The isometric kit and the transformer figure are shared code now: `videos/_shared/web/iso/iso.js` and `diagram.js` (two users each), linked into each beat as `iso/` and `diagram/`. 011's `_jev/jev.js` stays with its video (one user). (janitor)
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
