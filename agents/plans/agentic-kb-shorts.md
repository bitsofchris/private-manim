# Plan: "Four layers of an agentic knowledge base" Shorts

**Name:** agentic-kb-shorts
**Description:** Up to four 9:16 HyperFrames Shorts from Chris's voice
note *Four Rules for Agentic Knowledge Bases* (2026-10-02) and the related
notes from that week. One anchor Short names the four layers; three
follow-ups take one layer or one application each. All four are drawn on
one shared set (a building in cross-section) with a recurring cast.
**When to use:** the status page for this series; scripts are agreed here
before any `videos/NNN-slug/` folder is opened. Move to `agents/archive/`
when the series is published or dropped.
**How it works:** the shorts runbook (`agents/runbook.md`), audio first,
`ENGINE: hyperframes`. VO uses Chris's own sentences (cut and reorder,
never reword); every VO line below names the note it was cut from. Lines
marked *(needs his words)* have no source sentence yet.
**Part of:** the harness engineering series (Chris, 2026-10-13). These are
A–C are its episodes 3a–3c, the knowledge-base part of episode 3, and they
keep this building set as their own recurring image. D gets tried inside
episode 3's script, and what stays is decided at script time. Recording is
in series order, audio first. Arc and sources:
`videos/012-harness-engineering/SERIES.md`. The scripts stay here.

Sources, all in the vault (`~/Documents/ZK Home`):

- `_private/0-Fleeting-Inbox/2026-10-02 - 4 rules for agentic knowledge bases.md` (the note; "OpenAuthkey" is a transcription slip for OpenAugi)
- `_private/0-Fleeting-Inbox/2026-10-03.md` ("a portable system for any project, repo")
- `_private/3-MOCs and Projects/PMOC - Shorts Augi Shorts - Augi content system.md`, 2026-10-03 ("Turned it into a self-improving repo")
- `OpenAugi/Notes/What Works - Running a Second Brain With Agents.md` (his 9/13 lines on the janitor and the visible seam)

Work detail stays out: the note names an internal tool; the VO says "at work".

## The set and the cast

One picture, reused in every Short, so the series reads as one thing and
the pieces reach two uses fast (`agents/parts.md` promotion rule).

| Where | What | Layer |
|---|---|---|
| Basement | a robot filling shelves with dense pages (hashes, branch names) | agent layer |
| Upstairs | the stick figure at one clean board; threads drop to the basement pages | human layer |
| Glass case on the upstairs wall | three items: rules, map, goals | curated layer |
| Moves between floors | a janitor with a broom | janitor |

Cast: the stick figure exists (`prototypes/hyperframes/quiz`, `ironies`).
The robot and the janitor are new. Teal = what is there; magenta = the one
thing the beat points at.

## The Shorts

| | Short | Status |
|---|---|---|
| A | The four layers an LLM wiki needs | script agreed 2026-10-11, pending a read-aloud |
| B | Your system needs a janitor | script draft below, not agreed |
| C | Let your agent write notes you never read | script draft below, not agreed |
| D | The same four layers in any repo | outline only: his words are two sentences |

Search phrases are guesses, not checked against YouTube autocomplete
(runbook step 0).

### A. The four layers an LLM wiki needs

- THE QUESTION: What does an LLM wiki need to stay useful?
- WHO IS ASKING: an engineer who pointed an agent at a folder of notes and watched it turn into a mess
- THE ANSWER IN ONE SENTENCE: Four layers: a place where agents write for agents, a clean surface for humans, the agent's rules and context kept where the human can see them, and a janitor.
- THE SEARCH PHRASE: llm wiki (guess)

Decided 2026-10-11 in chat: open on "LLM wiki", close on "agentic knowledge
base" (the switch is on purpose). Each layer is named as the first words of
its beat; the number sits on screen, not in the VO. The curated layer is
one layer, framed his way: the agent's context and rules, kept visible to
the human. Sources: N = the 10/2 note, C = his chat answer 2026-10-11.

| beat | VO | src | visual |
|---|---|---|---|
| 1 | "A good LLM wiki needs four layers." | N | the whole building already running; "What does an LLM wiki need?" in the band |
| 2 | "The agent layer. A place where agents write for agents. They include the details needed to resume a task later: hashes, branches, commits. You never have to read it." | N | basement; robot stacks dense pages. Hero: the pages. "1" on screen |
| 3 | "One place for agents to write, one place for humans. That needs to be separate." | C | the floor slab between basement and upstairs draws in. Hero: the slab |
| 4 | "The human layer. A clean, distilled view that links out to the detailed agent nodes. A dashboard, a Kanban board, a map." | N | upstairs; one board, threads drop through the slab to basement pages. Hero: the board. "2" |
| 5 | "The curated layer. Agent context and rules the human needs visible. The map, the rules, slowly changing context. The things you maintain carefully and edit to keep accurate." | C + N | a glass case on the stairs between floors: the robot looks up at it before writing, the figure opens it and edits one item. Hero: the case. "3" |
| 6 | "The janitor. As you iterate and change the system, something has to keep it clean. It catches conflicting rule sets before they spread." | N | two signs in the case point opposite ways; the janitor takes one down. Hero: the janitor. "4" |
| 7 | "With all four layers you get a strong agentic knowledge base." | N | all four lit, held. Takeaway line, no outro |

~135 words. Status: script agreed pending Chris reading it aloud once.

### B. Your system needs a janitor

- THE QUESTION: Why does my notes / agent setup turn into a mess a month in?
- WHO IS ASKING: someone who built an agent workflow that worked, then stopped opening it
- THE ANSWER IN ONE SENTENCE: Shipping fast only works if something prunes.
- THE SEARCH PHRASE: none found yet; likely a feed Short, not a search one

| beat | VO | source |
|---|---|---|
| 1 | "As you iterate and change the system, something has to keep it clean." | 10/2 note |
| 2 | "Keep it simple to get MVP out asap and using it. Let water flow through the hose." | 9/13 |
| 3 | *(needs his words)* the queue story: an agent drafted post ideas every week, nothing removed them, it reached 67 and he stopped opening it | 10/3: "I fall behind, good to capture things, but generating too much?" is the only line he wrote |
| 4 | "The janitor for agents: de-dupe and have fewer things to maintain." | 9/13 |
| 5 | "It catches conflicting rule sets before they spread. It keeps the source of truth clean. It files away or cleans up old material so the human layer stays useful." | 10/2 note |

Visual: the upstairs board fills with cards until the stick figure walks
away from it; the janitor sweeps; the figure comes back.

### C. Let your agent write notes you never read

- THE QUESTION: Should my agent's notes be readable by me?
- WHO IS ASKING: someone using Claude Code or a similar agent who loses the thread between sessions
- THE ANSWER IN ONE SENTENCE: No: give the agent its own layer to save what it needs to resume, and give yourself a clean view that links to it.
- THE SEARCH PHRASE: claude code memory (guess)

| beat | VO (from the 10/2 note) |
|---|---|
| 1 | "Agents can be as verbose as they need to be." |
| 2 | "They include the details needed to resume a task later: hashes, branches, commits, table names, file counts." |
| 3 | "The point is to save context for later, not to be readable." |
| 4 | "You never have to read it or go there. It's the agent's own memory of what's worth keeping." |
| 5 | "A clean, distilled view that links out to the detailed agent nodes." |

Open point: on 9/13 he was pleased with the opposite-sounding rule, "One
surface, two authors, visible seam… Not a separate agent-output folder."
The Short needs one sentence from him on how the two fit.

### D. The same four layers in any repo

- THE QUESTION: What should go in AGENTS.md?
- WHO IS ASKING: an engineer setting up a repo for coding agents
- THE ANSWER IN ONE SENTENCE: *(needs his words)*
- THE SEARCH PHRASE: AGENTS.md (guess)

His words so far: "Merging these into a portable system for any project,
repo, etc." (10/3) and "Entrypoint in private-manim is now the AGENTS.md.
Turned it into a self-improving repo." (PMOC, 10/3). The example would be
this repo: the map in `AGENTS.md`, the rules in `agents/`, the changelog,
the update pass as the janitor. Not enough of his sentences for a VO yet.

## Open questions for Chris

2. B: tell the queue story in his words (beat 3).
3. C: how rule 1 fits the 9/13 "visible seam" rule.
4. D: say the answer out loud once; then it has a script.
6. Order: A first (it builds the set), then B?
