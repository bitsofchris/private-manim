# Series process: many Shorts, one recording

**Name:** series-process
**Description:** How a series of Shorts runs, from the arc to the update
pass: plan every episode up front, script them all, Chris records the
whole series in one file, Claude splits it into one folder per episode,
then one session per episode builds it through `agents/runbook.md`.
**When to use:** any new series (several Shorts on one topic, one shared
example). A single Short runs `agents/runbook.md` alone.
**How it works:** the series folder `videos/NNN-slug/` holds what every
episode shares (`SERIES.md`, `SCRIPTS.md`, `TRANSCRIPT.md`,
`EPISODE_PROMPT.md`), and each episode is a subfolder `epNN-slug/` laid
out like any other Short. The runbook's per-Short steps run inside the
subfolder; this file covers what happens once for the whole series.
Proven on `videos/002-linear-algebra-basics/` (11 Shorts from one 2026-10-09
take).

---

## 1. Arc (Claude + Chris)

Write `SERIES.md` at the series root. It is the series' one home:

- Who it is for, the promise, and the agreed decisions (dated, Chris's).
- The **ledger**: the shared example, names and numbers, identical in
  every episode. Generated data lives in `_data/` with a fixed seed; no
  beat invents a number.
- One section per episode: the runbook step 0 preflight (question in the
  viewer's words, who is asking, one-sentence answer, search phrase
  checked in YouTube autocomplete), the title, frame 0 and the magenta
  hero, the code beat, the parts to reuse.
- A **checklist** table, one row per episode: title, folder, Script, VO,
  Storyboard, Beats, Assembled, Shipped.

## 2. Scripts (Claude, Chris edits)

All episodes in one file, `SCRIPTS.md` at the series root, one `##`
heading per episode with its title and word count. Every script passes
runbook step 1's VO rules ("VO line 1", "Say each thing once, and get to
it fast", 130–150 words). Chris tightens in his own words before he
records.

## 3. Record once (Chris)

One file for the whole series, in script order (runbook step 2 for mic and
flubs):

- Before each episode, say **"Episode N: title"**, then pause ~2 s.
- Pause ~3 s between episodes. Flub: pause, re-read the sentence.
- Departing from the script is fine; what was said is the VO.

Hand Claude the file's path (e.g. `~/Creating/NNN-slug-ALL.m4a`), and a
timestamped transcript if there is one.

## 4. Split (Claude, one session)

1. Transcribe the whole file with Parakeet (runbook step 4), or use
   Chris's timestamped transcript. Save it as `TRANSCRIPT.md` at the
   series root.
2. Find each "Episode N" announcement. An episode runs from the end of
   its announcement's pause to the start of the next announcement, with
   lead and tail silence trimmed. Listen to (or re-transcribe) each
   boundary: a cut must not clip the first or last word.
3. Cut each one into its folder, announcement removed:
   `ffmpeg -ss START -to END -i ALL.m4a -ac 1 -c:a aac -b:a 160k epNN-slug/vo_raw.m4a`
4. Write `epNN-slug/script.md`: the title, the duration, the source cut
   times ("cut from ALL.m4a at 132.16–182.73 s, announcement removed"), a
   pointer to `../SCRIPTS.md`, how it was recorded (QuickTime raw, or
   Descript with Studio Sound: ask Chris if you don't know; runbook step 3
   never denoises a Studio Sound take), and an **As recorded** section with what
   was actually said. Fix only mishearings (check them against the
   planned script); keep Chris's departures from it.
5. Report one line per episode: duration, and where the take leaves the
   script (lines left out, flubs, repeats), since those shape each
   episode's cut list.
6. Tick the VO column, write `EPISODE_PROMPT.md` (step 5), and commit the
   audio, scripts, transcript and prompt together.

Cleaning and tightening stay per episode (runbook steps 3–5), so Chris
approves each cut list where the episode is built.

## 5. Episode prompt (Claude)

`EPISODE_PROMPT.md` at the series root is the prompt Chris pastes into a
fresh session per episode, with `FOLDER` replaced. Start from the template
below and fill the series slot from `SERIES.md` (look, conventions,
shared kit). Example: `videos/002-linear-algebra-basics/EPISODE_PROMPT.md`.

```text
Build one Short end to end: videos/NNN-slug/FOLDER

Start by reading AGENTS.md (the entry point) and follow agents/runbook.md as the process. Everything you need is in this repo.

Where this episode stands:
- The voice is recorded and cut: FOLDER/vo_raw.m4a. FOLDER/script.md is what I actually said. That transcript, not the planned script, is the VO.
- Runbook steps 0–2 are done. The preflight lines (question, who is asking, one-sentence answer, search phrase), the YouTube title, frame 0 and hero, the code beat, and the parts to reuse are in this episode's section of videos/NNN-slug/SERIES.md. Carry the search phrase into the storyboard's preflight lines and build the code beat on the VO line it names. The planned script is in SCRIPTS.md for reference only.

Do, in runbook order:
1. Write FOLDER/storyboard.md (step 1): the ENGINE line first, chosen by AGENTS.md "Which engine"; the preflight lines; the ledger from SERIES.md, used identically in every beat; a beat | VO | visual table built from script.md.
2. Clean, transcribe, tighten (steps 3–5). Flag any flubbed or repeated phrase in the take. Write the final beat table and the seam-states table into the storyboard.
3. Render FOLDER/00_layout (the canonical frame) while the cut list waits: two or three takes on the hero image side by side in one PNG. Send me the cut list and the frame together, and build beats only after I approve both.
4. Build the beats (step 6) with parallel agents, each briefed with the matching beat brief; one agent owns both sides of a cut that a beat-only prop crosses. Each renders and reviews its own contact sheet. Then check every cut (last frame of beat N beside the first frame of beat N+1).
5. Captions, assembly, review (steps 7–8): sequential clean re-render, assemble, contact sheets, fix what the sheets show. Then tell me the media/short.mp4 path to watch on my phone, and iterate on what I say.
6. Write FOLDER/publish.md (step 9) with the title from SERIES.md; description line 1 contains the search phrase. Send the hand-off pack (step 10) when I say done.

This series: SERIES-SPECIFIC LOOK, CONVENTIONS AND SHARED KIT.

Traps:
- Episode folders are one level deeper than a normal videos/NNN-slug/. Manim scene shim: parents[3], not parents[2]. HyperFrames symlinks: ../../../_shared/web/vendor (and any other shared kit). Call tools as "$(git rev-parse --show-toplevel)"/tools/NAME. Render from inside FOLDER (or the beat folder, for HyperFrames), never from the repo root, never two renders at once in one folder.
- No LaTeX: Text only.

Other sessions are building other episodes at the same time, so:
- Write only inside FOLDER. Don't edit videos/_shared/, agents/, AGENTS.md, SERIES.md or SCRIPTS.md. If a part, token or rule should change, list it in your hand-off and I'll take it to the update pass.
- Commit only FOLDER's files (git add with explicit paths), small and often, scenes separate from anything else.
- Finish your hand-off with the SERIES.md checklist boxes this episode now ticks (Storyboard, Beats, Assembled), and I'll update the checklist.

Skip step 11 (the update pass). It runs once, after all episodes are done.
```

## 6. One session per episode (Chris starts them)

Paste the episode prompt, one session per folder; several can run at
once since each writes only inside its folder. Ship the first few, and
give them a day-10 read (runbook step 12) before the later episodes
ship: what search brings in can change the remaining titles.

## 7. Update pass, once (Claude, when every episode is done)

Runbook step 11 over the whole series: every hand-off's wish list and
every change Chris asked for in any episode session. Tick the checklist.
