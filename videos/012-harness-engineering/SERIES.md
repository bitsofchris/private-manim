# Harness Engineering: the series

**Name:** harness-engineering-series
**Description:** Three Shorts on the agent harness, all recorded in
Chris's own words on 2026-10-17: what a harness is, how to make any repo
a self-improving loop for agents, and why the agent needs a map.
**When to use:** at the start of any session on this series. Pick the
next unticked episode from the checklist and build it through
`agents/series.md` (split) and `agents/runbook.md` (from step 3).
**How it works:** there is no script. What Chris said is the VO, in
`TRANSCRIPT.md`. Each episode below has its cut list against that
transcript, its title, and what the viewer takes away. Status (Chris,
2026-10-17): the ten-episode plan is dropped; these three are the series.
The old plan, scripts and research are in `_archive/`, kept for
reference only.

## Who it is for

Engineers who use coding agents (Claude Code, Codex) every day and want
to get more out of them in their own repos. They know what a prompt, RAG
and RL are. They don't follow the agent papers.

## The episodes

Publish in this order. "Recorded as" is the announcement in the take.

| # | Title | Recorded as | Their question | The answer | What they do after |
|---|---|---|---|---|---|
| 1 | `What Is an Agent Harness? The 4 Parts Explained` | Episode one (00:05–00:56) | What's an agent harness? | Everything except the model: context, tools, memory, and the loop. | When the agent fails, ask which piece was missing. |
| 2 | `LLM Wiki: The 4 Layers Every Repo Needs` | Episode three + 3A (00:56–04:05) | How do I make my agent setup get better instead of messier? | Every project can be a recursively self-improving loop for agents: an agent layer, a human layer, a curated layer, and a janitor. | Save every correction into the repo, and run a janitor. |
| 3 | `Context Engineering: Give Your Agent a Map` | Episode four (04:05–05:02) | Why does my agent miss what's in my repo? | Stuffing the context backfires; give the agent a map that points to the files. | Keep AGENTS.md a short map, not a manual. |

Search phrases (YouTube autocomplete, checked 10/17): "what is agent
harness", "agent harness"; "llm wiki" (results are about Karpathy's LLM
Wiki); "context engineering", "context engineering for agents". Backup
title for 2: `Claude Code Best Practices: A Self-Improving Repo`
("claude code best practices" is in autocomplete).

## Cut lists

Timestamps are from `TRANSCRIPT.md`.

**1. What is an agent harness.** 00:05–00:56 as recorded, minus the
announcement.

**2. LLM wiki for any repo.** Ep 3 and 3A merged (Chris, 10/17: the KB
material never needed four Shorts). In this order:

1. 01:14 "Every project can be a recursively self-improving loop for agents"
2. 02:09 "Anytime they do something wrong or could do it better, it needs to be saved in your repository" (stop before "and you can do it in one of three ways")
3. 03:13–04:01 the four layers, from "A good agentic knowledge base or LLM wiki needs four things" through "something has to keep it clean and remove any inconsistencies"
4. 02:43–02:58 "This is how I structure all of my repos these days. I have a map in my agents.md, a CLI for most of the steps. And a quick janitor script…"
5. 03:01 "Let your agents recursively self-improve by giving them access to these primitives so they can continually get better"

Left out: the 01:59 "continually self-improve" opener (it repeats line 1),
the files / tests list at 02:14–02:43 (a second list next to the four
layers; "keep AGENTS.md short with a map" belongs to episode 3), and
3A's closing line (it repeats the opener).

**3. Give your agent a map.** 04:05–05:02, minus the announcement and
04:13–04:18 ("Today, agents are using a magnifying glass to search. Oh my
God, that's fucking stupid."). Chris rejected that line in the take.

## Not recorded (for a written companion, not these Shorts)

Chris's own ideas from the vault that fit episode 2 but need explaining:

- "One surface, two authors, visible seam": the agent writes into the same
  notes he does, marked as agent-written. From
  [[What Works - Running a Second Brain With Agents]], 9/13.
- "Context is stored. Intent is all you review and discuss with the
  agent." From [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]], 6/11.
- The 67-idea queue that nothing pruned, so he stopped opening it (the
  case for the janitor).

## Checklist

| # | Folder | VO | Storyboard | Beats | Assembled | Shipped |
|---|---|:-:|:-:|:-:|:-:|:-:|
| 1 | `ep01-what-is-a-harness/` | x | | | | |
| 2 | `ep03-harness-101/` | x | | | | |
| 3 | `ep04-give-your-agent-a-map/` | x | | | | |

VO means recorded; it is not yet split into each folder's `vo_raw.m4a`
(`agents/series.md` step 4 needs the recording file's path). The folders'
`key-points.md` files are research from the dropped plan: background
only, not the episode's content.
