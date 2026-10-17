ENGINE: hyperframes

# LLM Wiki: The 4 Layers Every Repo Needs (Harness Engineering ep 3): storyboard

THE QUESTION: "How do I make my agent setup get better instead of messier?"
WHO IS ASKING: an engineer who runs coding agents (Claude Code, Codex) in
their repos every day and watches the notes, rules and plans pile up.
THE ANSWER IN ONE SENTENCE: an agent layer, a human layer, a curated layer,
and a janitor: separate what agents write from what you read, and run a
janitor.
THE SEARCH PHRASE: llm wiki (YouTube autocomplete, checked 10/17 in
SERIES.md; the results are about Karpathy's LLM Wiki). Said in VO line 1:
"A good LLM wiki needs four layers."

**Motion rule (Chris, 10/17):** only the part of the building the VO is
discussing moves. The agents write only during "agents can write for
agents" (beat 1) and the agent-layer beat (2); the human moves only in
beat 3; the janitor stays on the basement floor after its sweep.

**One idea:** a repo's knowledge base stays useful when each kind of text
has its own floor, and something cleans between them.

**The VO** is `script.md` (what Chris said, cut to 63.9 s), not a planned
script. Captions follow the audio.

**Code beat:** one small one. Beat 2 lifts one agent page out of the
basement as a callout card whose three monospace lines land on "hashes,
branches, commits". That is the only text drawn in the scene.

## Ledger (every beat uses exactly these)

**The building** (the whole episode is one frame; nothing leaves it).
Captions are anchored bottom (`assemble.py --captions-anchor bottom`), so
the stage runs to y 1330. Coordinates are frame pixels.

- Walls: ink, x 80 and x 930, from the roof (y 262) to the basement floor
  (y 1310). Roof: one ink line y 262. Everything is in `_kit/wiki.js`
  (`WIKI.POS`, `WIKI.B`, `WIKI.LADDER`, `WIKI.LANDING`).
- The ground floor slab: ink, y 700, from x 80 to x 600. The hatch is
  x 600–930. Outside the walls the ground continues as a muted line at
  y 700 to both frame edges, so the lower floor reads as a basement.
- **Upstairs (y 262–700): the human layer.** The human (`CAST.human`,
  s 0.66) at x 160, feet on y 700. The board (`CAST.board`, cards
  `[2, 1, 3]`, 312 × 270) at x 262, y 396.
- **Between the floors: the curated layer and the janitor.** A ladder down
  the hatch (rails x 600 and 648, slab to basement floor) and a landing on
  the right (y 1000, x 652–930). On the landing: the janitor
  (`CAST.janitor`, s 0.5) at x 716 and the glass case (`CAST.vitrine`,
  s 0.38) at x 806. (The storyboard first said stairs; a stick figure
  can't stand on a flight that steep in 280 px, so it's a ladder and a
  landing.)
- **The basement (y 700–1310, x 80–600): the agent layer.** Two agents
  (`CAST.agent`, s 0.58) at x 175 (A) and x 410 (B), feet on y 1310, each
  holding the page it is writing (`CAST.page`, s 0.5) at shoulder height to
  its right. Five wall pages (s 0.36) along the top of the basement, y 728:
  three at the start, the 4th and 5th fade in on "verbose". Under the
  landing, on the floor, two **old** pages: muted, dashed, no hash.
- **Order the layers are named in, always:** agent layer → human layer →
  curated layer → janitor. Any beat that lights them in turn uses this
  order.
- **The callout card** (beat 2): a panel card, teal outline, three
  monospace lines at 60 px, teal: `hash a3f9c2`, `branch fix/auth`,
  `commit 9e1b04`. The hash matches the page's own top line (`a3f9c2`, the
  kit default).
- **The link** (beat 3): a dashed line from the board's middle card down
  through the slab to agent B's page.
- **The conflict** (beat 5): the 4th line of agent B's page turns magenta;
  its copy then draws on agent A's page ("spread"); the janitor's broom
  sweeps both out.
- Colour jobs: teal is what agents write (pages, the agents' eyes, the
  callout). Ink is people, the building and the board. Magenta is the one
  thing the beat points at. The case glass is the kit's glass cyan.

## Beats (VO from script.md; times from the trial cut, master seconds)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Four layers | A good LLM wiki needs four layers. A place where agents can write for agents, a clean surface for humans to read, a curated layer of slowly changing context and rules that you review, and a janitor that keeps it all up to date and consistent. | Frame 0: the whole building, already working (the two agents' pens moving, lines filling their pages; the human looking at the board). Each layer turns magenta as it's named and goes back to rest as the next is named: "agents can write for agents" → the basement's pages; "clean surface for humans" → the board; "curated layer" → the case; "a janitor" → the janitor (a sweep of the broom on "up to date"). | each layer in turn |
| 2 | Agent layer | The agent layer is written by agents for other agents. Agents can be as verbose as they need to be. This can include details that they need to resume a task later, like hashes, branches, commits. You never need to read it or go here. | "written by agents for other agents": one agent hands its page to the other. "verbose": the pages' lines run long, the 4th and 5th wall pages fade in. "resume a task later": the callout card lifts out of the right agent's page and grows over the middle of the building (a solid panel, y 712–1008, the scene dimmed behind it); "hashes, branches, commits": its three lines land one per word. "never need to read it": the card sinks back into the page; upstairs the human stays turned to the board. | the callout card |
| 3 | Human layer | The human layer is the clean, distilled view that you link out, and that goes to these detailed agent notes when necessary. Think of a dashboard or a Kanban board. It's less about reviewing what the agent's up to and more about managing your own context. | "The human layer": the board goes magenta. "link out … detailed agent notes": the middle card draws the dashed link down to the agent's page (page pulses teal). "Kanban board": a card slides from column 1 to column 2. "less about reviewing what the agent's up to": the human glances down at the basement, then back; "managing your own context": the human points at the board. | the board |
| 4 | Curated layer | The curated layer, this is the slowly changing context that you need to handle with care. These are the skills and rules, the conventions of your repo. | "curated layer": the case goes magenta, the link fades. "handle with care": the glass glints once. "skills and rules": the rules item inside the case becomes the hero (the case returns to glass); "conventions of your repo": hold. | the case, then its rules |
| 5 | Janitor | And then you need the janitor. This looks to catch conflicting rules in your agent notes before they spread. And it cleans up old material so the human layer stays useful. | "the janitor": the janitor goes magenta and climbs down the ladder into the basement. "conflicting rules": a line on agent B's page turns magenta; "before they spread": a copy starts to draw on agent A's page, and the broom sweeps both out (the broom is the hero). "old material": the two old dashed pages are swept off the floor. "human layer stays useful": the board upstairs settles, clean. | the janitor, then the conflict |
| 6 | Close | With all four layers, you can build a strong agentic knowledge base for research, personal growth, project work, or anything else. | The whole building at rest, the janitor still on the basement floor. "all four layers": the four light once each in the ledger order, quickly, and return to rest. Still to the end. | each in turn, then none |

## Final beats (the contract; `vo_final.wav` 59.12 s, master seconds)

Beat brief for the agents: `BRIEF.md` (seam states `WIKI.SEAM` in
`_kit/wiki.js`). Word times: `words.json` (master seconds; spellings fixed
against `transcript_final_text.txt`). Captions anchored bottom, so the
stage runs to y 1330.

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_four_layers` | 0.00 | 13.55 | A good LLM wiki needs four layers. A place where agents can write for agents, a clean surface for humans to read, a curated layer of slowly changing context and rules that you review, and a janitor that keeps it all up to date and consistent. |
| 2 | `02_agent_layer` | 13.55 | 11.80 | The agent layer is written by agents for other agents. Agents can be as verbose as they need to be. This can include details that they need to resume a task later, like hashes, branches, commits. You never need to read it or go here. |
| 3 | `03_human_layer` | 25.35 | 12.20 | The human layer is the clean, distilled view that you link out and that goes to these detailed agent notes when necessary. Think of a dashboard or a Kanban board. It's less about reviewing what the agent's up to and more about managing your own context. |
| 4 | `04_curated_layer` | 37.55 | 7.50 | The curated layer, this is the slowly changing context that you need to handle with care. These are the skills and rules, the conventions of your repo. |
| 5 | `05_janitor` | 45.05 | 8.00 | And then you need the janitor. This looks to catch conflicting rules in your agent notes before they spread. And it cleans up old material so the human layer stays useful. |
| 6 | `06_close` | 53.05 | 6.07 | With all four layers, you can build a strong agentic knowledge base for research, personal growth, project work, or anything else. |

## Cut list (approved by Chris, 10/17; applied)

No phrase cuts (the content cut was done and approved before this
session). The take is already clean (−72 dB in the pauses, LRA 4.9), so
runbook step 3 is gain only: the first build ran the full
`enhance_vo.sh` chain (denoise, de-ess, 3:1 compressor) and Chris said the
audio sounded bad; rebuilt 10/17 from `vo_raw.m4a` with the same cut pieces
(`timemap.json`), so every beat time is unchanged:

| # | Change | Saves |
|---|---|---:|
| 1 | `tighten_vo.py --max-gap 0.25 --noise=-40dB --min-silence 0.3` (pauses capped; −40 dB keeps word tails) | 3.9 s |
| 2 | `atempo=1.02`, then `volume=10.7dB,alimiter=limit=0.79` (−14.5 LUFS, −2.0 dBTP; the limiter touches 0.8 % of samples). Two-pass linear loudnorm can't reach −14 under −1.5 dBTP on this take, and single-pass loudnorm is dynamic | 1.2 s |

63.9 s → **58.82 s**. `timemap.json` maps `vo_clean` → the tightened file
*before* the 1.02 tempo (divide its new times by 1.02 for `vo_final`).
The five tight joins from script.md (after "commits", "here", "repo",
"useful", "base") were checked by ear by Chris: fine. On the clean audio both
recognizers hear "This can include", as script.md has it (the processed
audio read "These"). Captions follow the audio.

## New ending (Chris, 10/17, after watching v2)

The take-2 last line stopped at "…knowledge base" while Chris's voice ran
on into "for research…", so the Short ended mid-sentence. Chris picked
option C of three auditions: finish the sentence (master 428.20–433.85,
"…for research, personal growth, project work, or anything else.") and
drop the take-1 line "This is how I structure all of my repos these days."
Spliced into `vo_final.wav` after 53.10 (same gain, limiter and 1.02 tempo
as the rest); everything before 53.10 is unchanged, so beats 1–5 keep
their timing. `words.json` keeps the old word times before 53 s and takes
the new recognition after. 58.82 s → 59.12 s. `vo_raw.m4a`, `vo_clean.wav`
and `timemap.json` still describe the original cut up to "useful".
