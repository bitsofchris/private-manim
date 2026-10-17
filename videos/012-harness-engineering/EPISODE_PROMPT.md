# Episode prompt: build one Harness Engineering Short

**Name:** harness-engineering-episode-prompt
**Description:** The prompt Chris pastes into a fresh session to build one
episode of the series, start to hand-off, through the repo's runbook.
**When to use:** one session per episode folder. Replace `FOLDER` with
the folder name (e.g. `ep03-llm-wiki-four-layers`). Several sessions can
run at once; the prompt keeps them out of each other's files.
**How it works:** points the session at the repo's own entry point and
process, says which runbook steps are already done, names the shared cast
kit, and lists the traps specific to this series' folder layout. Built
from the template in `agents/series.md` step 5.

---

```text
Build one Short end to end: videos/012-harness-engineering/FOLDER

Start by reading AGENTS.md (the entry point) and follow agents/runbook.md as the process. Everything you need is in this repo.

Where this episode stands:
- The voice is recorded and cut: FOLDER/vo_raw.m4a. FOLDER/script.md is what I actually said, with the cut times. That transcript is the VO; there is no planned script. Don't reword it.
- Runbook steps 0–2 are done. The title, the viewer's question, the one-sentence answer, what the viewer does after, and the search phrases are in videos/012-harness-engineering/SERIES.md ("The episodes"); this episode's scene and hero moves are in "The look". Carry the search phrase into the storyboard's preflight lines. FOLDER/key-points.md, where there is one, is research from a dropped plan: background only.

Do, in runbook order:
1. Write FOLDER/storyboard.md (step 1): ENGINE: hyperframes on the first line; the preflight lines; a ledger of what must match across beats (the parts on screen, their places, the order the layers or pipes are named); a beat | VO | visual table built from script.md, using the scene in SERIES.md "The look".
2. Clean, transcribe, tighten (steps 3–5). The content cut is done; this is loudness, pauses and timing. Bring me the cut list and wait for my approval before building beats. Flag any flubbed or repeated phrase in the take.
3. Render FOLDER/00_layout (the canonical frame) from prototypes/hyperframes/cast/index.html and send it to me; build beats only after I OK the look.
4. Build the beats (step 6) with parallel agents, each briefed with agents/beat-brief-hyperframes.md. Each renders and reviews its own contact sheet. Then check every cut (last frame of beat N beside the first frame of beat N+1).
5. Captions, assembly, review (steps 7–8): sequential clean re-render, assemble, contact sheets, fix what the sheets show. Then tell me the media/short.mp4 path to watch on my phone, and iterate on what I say.
6. Write FOLDER/publish.md (step 9) with the title from SERIES.md; description line 1 contains the search phrase. Send the hand-off pack (step 10) when I say done.

This series: line-drawn people and flat outlined props on the house background, all from the shared cast kit videos/_shared/web/cast/cast.js (rules in agents/style.md "Agents and knowledge bases"; starter prototypes/hyperframes/cast/index.html). The human is the round-headed stick figure; the agent is the same body with a rectangle head and 1 and 0 eyes; the janitor is an agent with a broom. Teal is what agents write, magenta is the one thing the beat points at, ink is people and structure. Draw with CAST parts; a part the kit lacks goes in a local helper in FOLDER and into your hand-off, not into the kit.

Traps:
- Episode folders are one level deeper than a normal videos/NNN-slug/. HyperFrames symlinks from a beat folder: ../../../_shared/web/vendor, ../../../_shared/web/iso and ../../../_shared/web/cast. Render from inside the beat folder, never from the repo root, never two renders at once in one folder.
- Load order in index.html: vendor/gsap.min.js, iso/iso.js, cast/cast.js. The literal window.__timelines["main"] = ISO.start(...) stays in the beat's own index.html.
- Set monospace from the script (el.style.fontFamily), as cast.js does for the agent's eyes; set in HTML it renders in Inter.
- No LaTeX: Text only.

Other sessions are building other episodes at the same time, so:
- Write only inside FOLDER. Don't edit videos/_shared/, agents/, AGENTS.md, SERIES.md, TRANSCRIPT.md or prototypes/. If a part, token or rule should change, list it in your hand-off and I'll take it to the update pass.
- Commit only FOLDER's files (git add with explicit paths), small and often, scenes separate from anything else.
- Finish your hand-off with the SERIES.md checklist boxes this episode now ticks (Storyboard, Beats, Assembled), and I'll update the checklist.

Skip step 11 (the update pass). It runs once, after all episodes are done.
```
