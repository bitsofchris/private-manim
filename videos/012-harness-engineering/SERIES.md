# Harness Engineering: the series

**Name:** harness-engineering-series
**Description:** Four Shorts on working with coding agents, all recorded
in Chris's own words on 2026-10-17: what a harness is, why the agent
needs a map, the four layers of an agentic knowledge base, and why the
goal is your understanding rather than busy agents.
**When to use:** at the start of any session on this series. Pick the
next unticked episode from the checklist and paste `EPISODE_PROMPT.md`
(with `FOLDER` set) into a fresh session; it runs `agents/runbook.md` in
that folder.
**How it works:** there is no script. What Chris said is the VO. The
full take is `~/Creating/012-harness-engineering-series.m4a` (492 s),
transcribed in `TRANSCRIPT.md`. Each episode folder has its cut
`vo_raw.m4a` and a `script.md` with what was said and the exact cut
times. Status (Chris, 2026-10-17): the ten-episode plan is dropped; these
four are the series. The old plan, scripts and research are in
`_archive/`, for reference only.

## Who it is for

Engineers who use coding agents (Claude Code, Codex) every day and want
to get more out of them in their own repos. They know what a prompt, RAG
and RL are. They don't follow the agent papers.

## The episodes

| # | Title | Their question | The answer | What they do after |
|---|---|---|---|---|
| 1 | `What Is an Agent Harness? The 4 Parts Explained` | What's an agent harness? | Everything except the model: context, tools, memory, and the loop. | When the agent fails, ask which piece was missing. |
| 2 | `Context Engineering: Give Your Agent a Map` | Why does my agent miss what's in my repo? | Stuffing the context backfires; give the agent a map that points to the files. | Keep AGENTS.md a short map, not a manual. |
| 3 | `LLM Wiki: The 4 Layers Every Repo Needs` | How do I make my agent setup get better instead of messier? | An agent layer, a human layer, a curated layer, and a janitor. | Separate what agents write from what you read, and run a janitor. |
| 4 | `Is AI Making Us Dumber? Stop Keeping Agents Busy` | I run more agents than ever; why don't I feel better at my work? | The goal is to maximize the rate at which you understand things. | Go fast on what teaches you nothing, slow on the core; block time to do the work yourself. |

Search phrases (YouTube autocomplete, checked 10/17): "what is agent
harness", "agent harness"; "context engineering", "context engineering
for agents"; "llm wiki" (results are about Karpathy's LLM Wiki); "is ai
making us dumber". Backup title for 3: `Claude Code Best Practices: A
Self-Improving Repo`.

## The look (locked 2026-10-17)

`ENGINE: hyperframes` for every episode. The cast kit is
`videos/_shared/web/cast/cast.js`; its rules are `agents/style.md`
"Agents and knowledge bases", and the sign-off frame is
`prototypes/hyperframes/cast/`. One stick-figure body: the human has a
round head, the agent a rectangle head with 1 and 0 eyes; the janitor is
an agent with a broom. Teal is what agents write, magenta is the one thing
the beat points at, ink is people and structure.

| # | Scene (frame 0 already moving) | The hero moves |
|---|---|---|
| 1 | The model blob with its four pipes (`CAST.blob`), the human beside it | one pipe per part as it's named: context, tools, memory, the loop; on "which piece was missing" the four light in turn |
| 2 | An agent at a long column of files, then the map card (`CAST.mapCard`) whose arrows point to just three | the stuffed window, then the map, then the one file it drills into |
| 3 | The building in cross-section: agents writing pages in the basement, the human at one board upstairs, the glass case on the stairs, the janitor between floors | each layer as it's named, in the opener's order; then the janitor's broom on the conflicting rule |
| 4 | The human at a desk while agents stream finished pages at them | the pile (the bottleneck), then the human writing the core alone while an agent does the plumbing |

Code beat: none is planned. Each session decides in its storyboard
whether one line on screen earns its place (Ep 2 could show a short
`AGENTS.md` map).

## What was cut from the take

Times are seconds into the full take; exact segments are in each
`script.md`.

- **1:** 10.8–53.2, the announcement removed.
- **2:** 249.8–294.6, the announcement and the magnifying-glass line
  (253.2–257.3, rejected in the take) removed.
- **3:** the second reading of the four rules (303–435) in 12 segments
  (tightened to 63.9 s on 10/17),
  plus "This is how I structure all of my repos these days" from the
  first take (163.6). The first take of episode 3 (the primitives,
  59–187) and of 3A (190–241) are not used: 3A says the same thing with
  fewer specifics, and the primitives were a second thesis next to the
  four layers.
- **4:** 439.1–490.0, as recorded.

## Not recorded (for a written companion)

- "One surface, two authors, visible seam" (ep 3): the agent writes into
  the same notes he does, marked as agent-written. From
  [[What Works - Running a Second Brain With Agents]], 9/13.
- "Context is stored. Intent is all you review and discuss with the
  agent." (ep 3) From [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]], 6/11.
- The 67-idea queue nothing pruned (ep 3, the case for the janitor).
- Ep 4's essay version: the robot that won't bench press for you, the
  Sophia talk, the METR and MIT studies. Session "agents busy post",
  2026-09-20.

## Checklist

| # | Folder | VO | Storyboard | Beats | Assembled | Shipped |
|---|---|:-:|:-:|:-:|:-:|:-:|
| 1 | `ep01-what-is-a-harness/` | x | | | | |
| 2 | `ep02-give-your-agent-a-map/` | x | | | | |
| 3 | `ep03-llm-wiki-four-layers/` | x | | | | |
| 4 | `ep04-dont-keep-agents-busy/` | x | | | | |

VO means cut into the folder's `vo_raw.m4a`, with `script.md`. The
`key-points.md` files in eps 1–3 are research from the dropped plan:
background only, not the episode's content.
