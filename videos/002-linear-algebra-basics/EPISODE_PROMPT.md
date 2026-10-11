# Episode prompt: build one Linear Algebra Short

**Name:** linear-algebra-episode-prompt
**Description:** The prompt Chris pastes into a fresh session to build one
episode of the series, start to hand-off, through the repo's runbook.
**When to use:** one session per episode folder. Replace `FOLDER` with
the folder name (e.g. `ep03-what-a-matrix-does`). Several sessions can
run at once; the prompt keeps them out of each other's files.
**How it works:** points the session at the repo's own entry point and
process, says which runbook steps are already done, and lists the traps
specific to this series' folder layout.

---

```text
Build one Short end to end: videos/002-linear-algebra-basics/FOLDER

Start by reading AGENTS.md (the entry point) and follow agents/runbook.md as the process. Everything you need is in this repo.

Where this episode stands:
- The voice is recorded and cut: FOLDER/vo_raw.m4a. FOLDER/script.md is what I actually said. That transcript, not the planned script, is the VO.
- Runbook steps 0–2 are done. The preflight lines (question, who is asking, one-sentence answer, search phrase), the YouTube title, frame 0 and hero, the code beat, and the parts to reuse are in this episode's section of videos/002-linear-algebra-basics/SERIES.md. Carry the search phrase into the storyboard's preflight lines and build the code beat on the VO line it names. The planned script is in SCRIPTS.md for reference only.
- The 16:9 draft scenes and UNIT_1_3_RECAP.md in the 002 folder are reference for layout, motion and numbers. Rebuild every beat as a 9:16 Short; don't port the old BocScene code.

Do, in runbook order:
1. Write FOLDER/storyboard.md (step 1): the ENGINE line first, chosen by AGENTS.md "Which engine"; the preflight lines; the ledger (the numbers in SERIES.md "Series rules" and the draft scenes, used identically in every beat); a beat | VO | visual table built from script.md.
2. Clean, transcribe, tighten (steps 3–5). Bring me the cut list and wait for my approval before building beats. Flag any flubbed or repeated phrase in the take.
3. Build the beats (step 6) with parallel agents, each briefed with the matching beat brief. Each renders and reviews its own contact sheet.
4. Captions, assembly, review (steps 7–8): sequential clean re-render, assemble, contact sheets, fix what the sheets show. Then tell me the media/short.mp4 path to watch on my phone, and iterate on what I say.
5. Write FOLDER/publish.md (step 9) with the title and the series description line from SERIES.md ("Series rules", publish copy); description line 1 contains the search phrase. Send the hand-off pack (step 10) when I say done.

Look and checks for this series:
- Linear algebra uses the flat 2D number plane, not the isometric floor (agents/style.md "Linear algebra"). The plane kit is shared: link ../../../_shared/web/vec into each beat as vec/ (next to vendor/ and iso/), keep only this episode's numbers and views in a local script, and start from prototypes/hyperframes/vec-plane/index.html. Don't copy or edit the shared kit; list what it lacks in the hand-off.
- Before spawning beat agents, render FOLDER/00_layout (the canonical frame) and send it to me; build beats only after I OK the look.
- After the parallel build, check every cut (last frame of beat N beside the first frame of beat N+1) before assembling.

Traps in this series:
- Episode folders are one level deeper than a normal videos/NNN-slug/. Every path relative to the repo gains a level. Manim scene shim: parents[3], not parents[2]. HyperFrames symlinks: ../../../_shared/web/vendor, ../../../_shared/web/iso and ../../../_shared/web/vec. Render from inside FOLDER (or the beat folder, for HyperFrames), never from the repo root, never two renders at once in one folder.
- Use the row-vector (PyTorch) convention throughout: x @ W, rows of W are where input directions land (SERIES.md "Series rules").
- No LaTeX: Text only.

Other sessions are building other episodes at the same time, so:
- Write only inside FOLDER. Don't edit videos/_shared/, agents/, AGENTS.md, SERIES.md or SCRIPTS.md. If a part, token or rule should change, list it in your hand-off and I'll take it to the update pass.
- Commit only FOLDER's files (git add with explicit paths), small and often, scenes separate from anything else.
- Finish your hand-off with the SERIES.md checklist boxes this episode now ticks (Storyboard, Beats, Assembled), and I'll update the checklist.

Skip step 11 (the update pass). It runs once, after all episodes are done.
```
