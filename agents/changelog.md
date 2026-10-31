# Design-system changelog

One line per change to a rule, token, part, tool, or doc, with the video
that forced it. Newest first.

## 2026-10-31

- `tools/seam_check.py`: snapshots in a per-run temp folder, so parallel beat agents no longer overwrite each other's frames. (015 ep1)
- `tools/hf_state_check.js`: a bar `{ a, b }` with `b <= a` compares as hidden. (015 ep1)
- `videos/015-python-gil/_kit/kitchen.js`: `SC.swap`, `SC.pulseUntil`, `SC.hopKnife`, `SC.pathAlong`, `SC.cooksPatch`; `pulse` exactly 0 at both ends; `state()` takes several patches; header lists the drawing changes deferred to the next kit pass. (015 ep1, ep2)
- `agents/beat-brief-hyperframes.md`: traps for zero-length bars, cue sums on a hold boundary, pulses inside a hold. (015)
- `agents/runbook.md`: storyboard cue tables quote `words.json` times, and name the real cue word when it is not the obvious one. (015 ep2)

## 2026-10-31

- `tools/hf_state_check.js`: the stub DOM has `insertBefore`, and the mount wrapper takes a one-argument `draw(S)` kit (016's) as well as `draw(g, S)`; tests for the 016 kit shape. All three ep01 beat agents had crashed on it and run a patched copy from scratch. (016 ep01)
- `tools/review_frames.sh`: the default sheet name is `<video folder>_<clip>_sheet.png`, so parallel episode sessions stop overwriting each other's `01_hook_sheet.png`. (016 ep01)
- 016 `_kit/chip.js`: `SC.mount` returns a handle per part (`chip`, `cpu`, `hbm`, `meter`, `strip`); additive, no frame changes. `agents/parts.md` lists the chip kit and ep 1's `ep.js` (4-core CPU, `y = x @ W`, the tiny network, `focus`). (016 ep01: beats reached the chip box through `cells[0].body.parentNode`)
- `agents/style.md` Shorts rules: a part arrives when the VO names it (Chris, 016 ep01: the CPU box parked from frame 0, "we don't need it sitting there"); an equation sits next to the picture it describes, stacked, the shared image shrinking for those beats (Chris: the network and `y = x @ W` stacked, the GPU at 0.8×). 016 `SERIES.md`: ep 1 ticked Storyboard v5, Beats 6, Assembled 44.0 s. (016 ep01)
- Promoted the HyperFrames code card to `videos/_shared/web/code/code.js` at its second use: one `CODE.make(root, opts)` with placement options and presets `STAGE` (014, full stage) and `DOCK` (016, bottom slot, shrink-to-fit), `look` `dark+` / `plain`; both series' `_kit/code.js` are now links to it, `machine.js` / `chip.js` pass their preset; `SC_*` globals kept as aliases; tests `tests/test_code_card.py` (typing pinned to 014's numbers). Both `00_layout`s and six code beats snapshot pixel-identical, every seam beat's `hf_state_check.js` unchanged. 016 still uses `plain` (magenta text for the hero line, which `agents/style.md` rules out); moving it to `dark+` would change shipped frames, so it waits for Chris. STAGE carries 014 ep05's long-line rule as `fitChars: 28` (merged after the promotion: every row at 48 × 28 / length, the pitch kept). (014 ep02 update pass, "2 → promote")
- 014 `_kit/machine.js`: hero `"twins"` lights both batch cards (it lit only the second), and the batching station's `×N` reads the batch size from `S.shape` (it was a fixed `×32`; ep 5's batch is `[4, 512]`). 014 `_kit/code.js`: a line over 28 characters sets every row at 48 × 28 / length px so it fits the card (`class Stream(IterableDataset):`, 30 characters, ran off it). Shipped episodes are unchanged: only eps 4–5 have such lines and both still set their own size. HyperFrames brief: a group hero and a ledger label belong to the kit; ep05's wishes listed (mode dip as one field, cursor on the lit line, typing from a character). `agents/parts.md` rows updated; 014 `SERIES.md`: ep 5 ticked Storyboard, Beats, Assembled. (014 ep05: `ep5.js` patched all three after `kit.draw`; ep04's `ep4.js` set 46 px for the same overflow)
- `tools/tighten_vo.py --noise auto` never goes below −45 dB (`NOISE_MIN`, `auto_threshold`, tests): on a quiet room floor + 12 sits under the breaths. Runbook step 5: rerun at −40 dB if a breath survives as its own piece. (014 ep02; auto had failed on 014 eps 2–5 and 016 eps 1 and 3, each falling back by hand; ep03: auto at −53.2 capped nothing, and a 2.8 s breath was cut by hand)
- `tools/seam_check.py --mask x0,y0,x1,y1` (tests): blanks a part that runs on the master clock before the diff. HyperFrames brief: check by eye that the strip is the only difference, then mask it and report the box. (014 ep02: 7 of 8 cuts flagged on the sample hop alone; ep03: all 5 cuts out of the machine)
- HyperFrames brief, what a kit owes its beats: a `pulse(part, k)` call, a handle for every label the VO can name, and fields that can grow (`workers: 1.5`), on the code card's rows too; briefs name labels by text until then. (014 ep02 and ep03: ten beats hand-wrote the same pulse; ep02 beat 6 grew a worker inside the station's `<g>`; ep03's brief said `sampler.dom[0]` for the indices, which is the station's name; ep03 beat 10 swelled code rows to pass `sweep_static`)
- Runbook Tools: run Python tools through `uv run --no-sync python` (direct runs get system python3, no numpy); zsh doesn't word-split `$LIST` (use an array for explicit-path `git add`); check `git diff --cached --stat` before committing, since another session may have staged files. Runbook step 5: a spoken code name is captioned as the card spells it (`__getitem__`). `agents/parts.md`: the `__getitem__` label touches the Dataset card's border (swell from its right centre; a margin would move every episode's frame, so left as is). 014 `SERIES.md` checklist: eps 2 and 3 ticked Storyboard, Beats, Assembled. (014 ep02, ep03)
- `agents/style.md` code typing row: if the typing outruns the line that names the code, ≤ ~30 cps, hold the card through the next line, flip back on the line that returns to the other image. `agents/series.md`: the episode's code beat is written exactly as the kit's card shows it, with its VO line. 014 `SERIES.md` ep 2 row fixed to the shipped card (`drop_last` is the written companion's). (014 ep02)
- Janitor: AGENTS.md map lists the 014, 015, 016 and 017 series; `agents/parts.md` lists 014's machine kit (5 uses) and code card (2 uses with 016's adapted copy → promote to `web/code/`); `agents/style.md` caption rule says one line, ≤ 15 characters for VO captions (it still said 2 to 4 words). (janitor)

## 2026-10-29

- style.md, "Vectors and matrices as numbers": a batch drawn as an icon is still digits (rows of the ledger's readout in brackets), never a stack of squiggles. From 014 ep 1's second cut: Chris saw the batching station's squiggle stack and the `32` as "a bunch of squiggles", not data. The shared `videos/014-pytorch-dataloading/_kit/machine.js` grew `readout()` and the ledger a `series.readout`.

## 2026-10-28

- `agents/style.md` Shorts rules: the scene changes about every 5 s; images may repeat (a flip to the code card and back) but no run on one image longer than ~6 s unless it is moving through states. Chris, 014 ep01: 26 s on the loop image was too long. The storyboard's beats table plans it. (014)
- `agents/style.md` "Code on screen": code cards use VS Code Dark+ colours, the hero line is a magenta gutter bar and a lighter row (not magenta text), and code the VO introduces is typed at a human's uneven pace (`SC_typedAt` / `SC_typingSeconds` in `videos/014-pytorch-dataloading/_kit/code.js`). Chris, 014 ep01: "not just purple", "simulate the typing like a human when it makes sense". (014)

## 2026-10-26

- Runbook step 9: two titles, not one. The search title (phrase first, ≤ 50 chars) and the hook title (a stake about the viewer, then the phrase in parentheses). Chris, from 015: a scroller rolls past "GIL"; the phrase still has to be there for search. The day-10 read judges the pair. Hand-off pack item 2 carries both.

## 2026-10-25

- Runbook step 0, "From a vault block": a Short may start as a dispatched task from Chris's notes (`Zzz short: <idea>` under the block, or `do` on the board's Short from today); the block's quoted chat prompt is THE QUESTION, its `Source:` URL is one evidence beat at most, and the task stops at the storyboard with the session left open under Remote Control. The dispatch side (openaugi `routes:` in the vault's Repos.md) is documented there, not here. Plan archived: `agents/archive/idea-to-short-intake.md`.

## 2026-10-22

- New prototype `prototypes/hyperframes/kb-code/`: kb-graph's Short with a code editor in the band (zoom into a function, type the agent's saved code, zoom out to the hierarchy). Shares kb-graph's footage, edit map and captions by symlink so a re-edit carries over. Trap: a script error in a HyperFrames render gives a frozen video with only a `sub_timeline_readiness_timeout` warning; `snapshot` can pass on an older file, so run `validate` right before the render. (AugiCraft diamond-run Short)

## 2026-10-21

- New prototype `prototypes/hyperframes/kb-graph/`: real gameplay footage under HyperFrames graphics. One clock → video map (`edit.json`) cuts the timelapse (`make_timelapse.py`) and times every card, chip, the run timer and the voiceover lines (`make_audio.sh` ties lines and the music dip to run-clock moments), so trims keep everything in sync; a local `<video class="clip">` renders frame-accurately; captions sit over the footage because the graph owns the band (`make_captions.py`). Lessons in `concept.md`: events from cut-out stretches are shown on the shot where the skill was used, with the real time in a comment. (AugiCraft diamond-run Short)

## 2026-10-17

- Runbook read end to end after 013 ep04: a tracked move is ≥ `S.BEAT` (was "≥ 1 s", against animation-rules 9 and both briefs); the research summary no longer says captions are "2–4 key words" (they are the VO, ≤ 3 words); a caption fits one line at ≤ 15 characters, not "3 words"; step 1 no longer puts the question in the band (step 0: with VO the band is the captions'); step 8 checks every caption is on one line. (013 ep04 update pass)
- Janitor: the Manim brief's frame-0 rule now matches `agents/style.md` (later beats may hold until their first cue); the HyperFrames brief's stage row points to the y 1330 anchored-bottom variant; runbook step 5's pause map uses the measured floor, not a fixed −35 dB; the runbook's `beats.json` comment shows the `{"beats": [...]}` shape `assemble.py` requires; AGENTS.md points to runbook step 11 instead of repeating it; `design-system` and `diagram-shorts` plans archived (both done), research links updated. (013 ep04 update pass)
- New `tools/hf_state_check.js` (a seam-state beat's S(0) / S(end) against the kit's `SEAM`, in Node, no render; test `tests/test_hf_state_check.py`) and `seam_check.py --beat`. HyperFrames brief: run it before rendering; a kit's `mount` returns its parts and its `00_layout` cycles every seam state; agents keep temp files in their own scratch folder. (013 ep04: every beat agent wrote its own state check; a label that never drew; two agents overwrote each other's scripts)
- `agents/animation-rules.md` 7a: things that trade places move on arcs that bow apart; review the swap at 10 fps. Runbook step 5: numbers the recognizers dispute and spliced lines go to Chris as clips with the cut list. AGENTS.md "Which engine": one image in every beat keeps the Short in one engine. `agents/parts.md`: ep04's ROC / PR plot. (013 ep04)
- `agents/series.md` step 5: build a series' recurring image once at the series root (`_kit/`, `00_layout/`) before the episode sessions; 013's five sessions each wrote their own `score.js`. `agents/parts.md`: the score line + confusion box kit (5 uses). AGENTS.md map: the 013 series. (013 update pass)
- Runbook step 1: the thing the title names is on screen and said within ~8 s, and setup frame 0 already shows is not spoken. Step 8: a late line cut goes through `tools/cut_vo.py` (new, tested) on the finished VO so later beats keep their audio. (Chris, 013 ep01: two late cuts, "confusion matrix" from 20.8 s to 6.4 s)
- `captions_from_transcript.py --max-chars 15` (default) and a flash report; `agents/style.md` band row points to it. (013: ep01, ep02, ep05 each kept captions to one line by hand)

- Update pass from 012 eps 2–4 (useful lessons only): frame 0 moves in the hook beat; later beats move only what the VO names and may hold still until the first cue (`agents/style.md` Shorts rules, HyperFrames brief, `agents/animation-rules.md` rule 1 "in practice"; Chris, ep03: the agents writing in the basement through every beat); one visual action ≤ ~6–8 s (rule 3; Chris, ep04: a 13 s pile); end every kept piece where the take's sentence ends (runbook step 5, `agents/series.md` split; Chris, ep03: "knowledge base" sounded cut off); `sweep_static` also fails colour-only beats, monospace fits ~22 characters at 60 px, and seam states live in the kit as data (`SEAM` / `START`, third use: 013, ep02, ep04) (HyperFrames brief). (012 eps 2–4)
- `CAST.hand` follows `lean` (the upper body rotates about the hip); test added. (012 ep04: a pencil floated off a leaning hand)
- 012 `SERIES.md`: all four episodes ticked shipped (10/17), day-10 and day-30 read dates. (012)
- `tools/captions_from_transcript.py`: a caption never crosses a sentence end (. ? !), and words.json segments follow file order, not their index. Tests added. (012 ep01: "last error. Tools are"; a hand-split segment's captions sorted to the end)
- New `tools/fix_words.py` (`--join`, `--sub`, `--break-after`, `WORD@SECONDS`) for words.json spellings and caption breaks, and `tools/beat_cuts.py` (cuts mid-pause before each beat's first word, ≥ 80 ms lead → `beats.json` + the final beat table). Runbook step 5 and tools table; tests `tests/test_fix_words.py`, `tests/test_beat_cuts.py`. Python tools are executable. (012 ep01: both were ad hoc Python; beat_cuts reproduces its beats.json)
- `tools/review_frames.sh`: the last tile is always the final frame; `--at T1,T2` adds tiles at cue times. Runbook step 8, both beat briefs. (012 ep01: every beat agent pulled these by hand)
- Runbook step 5: a seam-states table (every cut, what is on screen) under the final beat table; the HyperFrames brief reads it for first and last frames. (012 ep01: five of six cuts pixel-identical on the first render)
- Runbook step 6, `agents/series.md` template, AGENTS.md session table: the canonical frame is two or three takes on the hero image side by side, rendered while the cut list waits and sent with it in one message; one agent owns both sides of a cut a beat-only prop crosses. (Chris, 012 ep01: the single rig was rejected; three stills settled it)
- HyperFrames brief: frame 0 moves by carrying on from the previous beat or growing an element in over ~0.2 s, never a new element at full size; agents run `seam_check.py` once a neighbour's render exists and report every flagged cut. (012 ep01: the 04 → 05 loop dot, 222/255, caught by the beat 3–4 agent)
- Tool paths: runbook and briefs call tools as `"$(git rev-parse --show-toplevel)"/tools/NAME` (nested series folders broke `../../tools`); the brief notes the extra `../` for series symlinks. (012 ep01)
- `agents/style.md` two-hero rule: a shared part is never magenta at rest; `CAST.blob`'s model now rests dim (`hero(part.body, true)` makes it the hero), test added. Ep01's agent-wearing-its-harness kit listed in `agents/parts.md`. (012 ep01)
- Janitor: runbook step 8 "one magenta hero per beat" → "at a time" (AGENTS.md rule 2); 012 `SERIES.md` look row 1 describes the shipped look C and ep 1's checklist is ticked (Storyboard, Beats, Assembled). (janitor)

- Audio: `enhance_vo.sh` defaults to high-pass + loudnorm (Chris's pick by ear); `--denoise` sets `afftdn`'s floor from the take (new `tools/vo_floor.py`) and the compressor is gone. `tighten_vo.py`: the 80 ms pad never re-enters a `--remove` range, `--noise auto` (floor + 12 dB), `--level -14` after the cut, `--map-in` to re-clean without moving beats. Runbook steps 3 and 5 and its tools table; `agents/series.md` split step records how the take was recorded. Tests `tests/test_vo_floor.py`, `tests/test_tighten_vo.py`. (Chris, 013 ep01: the fixed `nf=-25` smeared a −54 dB room; "flags 100 requests and" came back as "flies and")

- Shared cast kit `videos/_shared/web/cast/cast.js` (SVG, `check`-visible): human, agent (rectangle head, 1 and 0 eyes), janitor (agent + broom), the agent-notes page, the human board, the curated case, the map card, the model blob with four pipes; starter and sign-off frame `prototypes/hyperframes/cast/`; tests `tests/test_cast_kit.py`; `agents/style.md` "Agents and knowledge bases", `agents/parts.md`, prototypes README. (Chris, 012: look locked)
- Harness series 012 split: four episodes cut from `~/Creating/012-harness-engineering-series.m4a` into `ep01`–`ep04` (`vo_raw.m4a` + `script.md`), folders renamed to publish order; ep 3 is the second reading of the four rules plus one line from take 1. Cut points at the quietest 10 ms near WhisperKit word boundaries, 15 ms fades, 0.2 s between joined segments; each cut re-transcribed with Parakeet and diffed against its `script.md`. (012)
- Harness series 012 cut to the three episodes Chris recorded (harness; ep 3 + 3A merged as the self-improving repo; the map). `SERIES.md` rewritten around them with cut lists, the take saved as `TRANSCRIPT.md`; the old plan, scripts and eps 5–10 moved to `_archive/`; `agents/plans/agentic-kb-shorts.md` archived. AGENTS.md map updated. (Chris, 012)
- Runbook step 1, first bullet: scripts are drafted from Chris's own notes with `content-preflight`, `notes-to-post` and `effective-writing`; one idea, one action; a paper is one evidence beat at most, and key-points research supplies evidence, not the shape. (Chris, harness series 012: eps 2, 3, 5, 8, 9, 10 came out as paper tours)
- `agents/series.md`: the series process as the standard for any new series (arc in `SERIES.md`, all scripts in `SCRIPTS.md`, one recording with "Episode N: title" announcements, split into `epNN-slug/vo_raw.m4a` + `script.md`, a generic `EPISODE_PROMPT.md` template, one session per episode, one update pass at the end). AGENTS.md map and runbook step 2 point to it. (Chris, from the linear algebra series 002)
- Runbook step 1, "Say each thing once, and get to it fast": ten script checks (answer in line 1's first clause, one new thing per beat, closer is the viewer's next move, detours to the companion, no hedges, lists on screen, story detail only for the payoff, one home Short per sentence, title matches script). The *(if time)* mark moves from the last line, which is the takeaway, to the detour beat. (harness series 012, script tightening)

## 2026-10-11

- Linear algebra series: titles 6, 7, 10 and the trailer changed after a YouTube autocomplete check (6 and 10 matched another meaning, 7 and T matched nothing); every episode section in `SERIES.md` now has a search phrase and a code beat, the episode prompt passes both on, and 1–4 get a day-10 read before 7–10 ship. (series 5–T, from the analytics)
- Runbook "Why this shape", steps 0, 1, 9 and a new step 12, from the channel's analytics (`~/repos/yt-stats`): Shorts here are found by search (62 % of views). Preflight adds THE SEARCH PHRASE, checked in YouTube search (autocomplete, other meanings, learner vs news term); VO line 1 is a visible reframe, not a definition; show the code when there is code; the title starts with the search phrase; every Short gets a day-10 and day-30 read. AGENTS.md map points at yt-stats. (analytics of 004–009)
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
- Timing transcript is WhisperKit Large v2 JSON (per-word times from the recognizer, ~20 s): `word_times.py` reads it, moves a word placed in pre-speech silence onto the speech, and writes `words.json` with `end` and `seg`; captions are now built from `words.json` (chunks start on their first word) so a spelling is fixed once. ep03: median 0.07 s, worst 0.20 s against the 14 hand cues; the envelope estimator stays as the fallback. (Chris, ep03)
- Runbook step 4, MacWhisper Pro measured: Parakeet v3 gives word timings but they are coarser than `word_times.py` on Whisper Small (median 0.12 s vs 0.045 s on ep03's 14 hand cues); Parakeet v3 now makes every transcript a person reads (the take in step 4, the cut checks and `transcript_final_text.txt` in step 5, the spelling reference in step 7); Whisper Small makes only the timing transcript `transcript_final.txt` that feeds `word_times.py` and the captions; always pass `--model`; `--overwrite` replaces the rm-first gotcha. (Chris, ep03)
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
