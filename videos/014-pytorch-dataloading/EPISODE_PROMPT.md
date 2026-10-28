Build one Short end to end: videos/014-pytorch-dataloading/FOLDER

Start by reading AGENTS.md (the entry point) and follow agents/runbook.md as the process. Everything you need is in this repo.

Where this episode stands:
- The voice is recorded and cut: FOLDER/vo_raw.m4a. FOLDER/script.md is what I actually said, with where the take left the planned script. That transcript, not the planned script, is the VO.
- Runbook steps 0–2 are done. The preflight lines (question, who is asking, one-sentence answer, search phrase), the YouTube title, frame 0 and hero, the code beat, and the ledger are in this episode's row and the ledger of videos/014-pytorch-dataloading/SERIES.md. Carry the search phrase into the storyboard's preflight lines and build the code beat on the VO line it names. The planned script is in SCRIPTS.md for reference only.

Do, in runbook order:
1. Write FOLDER/storyboard.md (step 1): `ENGINE: hyperframes` first; the preflight lines; the ledger from SERIES.md, used identically in every beat; a beat | VO | visual table built from script.md.
2. Clean, transcribe, tighten (steps 3–5). The take's recording chain is in SERIES.md "How it was recorded" (loudnorm only unless it says otherwise). Flag any flubbed or repeated phrase in the take; script.md lists the known ones and the cut candidates. Write the final beat table and the seam-states table into the storyboard.
3. Render FOLDER/00_layout (this episode's frame 0 on the shared kit) while the cut list waits. Send me the cut list and the frame together, and build beats only after I approve both.
4. Build the beats (step 6) with parallel agents, each briefed with agents/beat-brief-hyperframes.md; one agent owns both sides of a cut that a beat-only prop crosses. Each renders and reviews its own contact sheet. Then check every cut with tools/seam_check.py.
5. Captions, assembly, review (steps 7–8): sequential clean re-render, assemble, contact sheets, fix what the sheets show. Then tell me the media/short.mp4 path to watch on my phone, and iterate on what I say.
6. Write FOLDER/publish.md (step 9) with the title from SERIES.md; description line 1 contains the search phrase. Send the hand-off pack (step 10) when I say done.

This series: flat house style, HyperFrames. The shared kit is videos/014-pytorch-dataloading/_kit/ (machine.js: the Dataset card, the sampler, the DataLoader box with its four stations, worker photocopies, the batch tensor, the model; code.js: the typed code card in the band, kb-code style; data.js: the ledger's numbers and lines) and the approved canonical frame is videos/014-pytorch-dataloading/00_layout/. Link the kit from every beat folder (`ln -s ../../_kit NN_beat/kit` from the episode folder) and never copy it; episode-only helpers go in FOLDER/_kit/. The machine's seam states (sampler on/off, worker count, lit station, batch in flight/landed) are the kit's API; every beat's seam row names them. One magenta hero at a time: the thing the VO names. Teal is data (samples, batch rows). The code card shares the band with captions: `assemble.py --captions-anchor bottom`, every caption one line (agents/style.md, "Share the band with a scene element").

Traps:
- Episode folders are one level deeper than a normal videos/NNN-slug/. HyperFrames symlinks: ../../../_shared/web/vendor (and ../../_kit as above). Call tools as "$(git rev-parse --show-toplevel)"/tools/NAME. Render from inside the beat folder, never from the repo root, never two renders at once in one folder.
- No LaTeX: Text only. Monospace set on every code span from the script (the CSS-class trap in the beat brief).
- Numbers come from SERIES.md's ledger; never invent one.

Other sessions are building other episodes at the same time, so:
- Write only inside FOLDER. Don't edit videos/_shared/, agents/, AGENTS.md, SERIES.md, SCRIPTS.md or _kit/. If a part, token, rule or kit state should change, list it in your hand-off and I'll take it to the update pass.
- Commit only FOLDER's files (git add with explicit paths), small and often, scenes separate from anything else.
- Finish your hand-off with the SERIES.md checklist boxes this episode now ticks (Storyboard, Beats, Assembled), and I'll update the checklist.

Skip step 11 (the update pass). It runs once, after all episodes are done.
