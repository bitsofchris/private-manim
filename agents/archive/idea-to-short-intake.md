# Plan: from a daily-note idea to a storyboarding session, without a hand-off

**Name:** idea-to-short-intake
**Description:** Why an idea written in a daily note (`2026-10-24`: "the
Python GIL, processes vs threads") does not today become a session running
this repo's runbook, and the smallest set of changes that makes it one
line of capture. Status: **built 2026-10-25** (openaugi `1404cc8`, vault Repos.md `routes:`).
The same morning's Sunday session switched the Shorts Queue off in favour of
the board's *Short from today*, so the route writes the storyboard and leaves
the session open under Remote Control instead of appending to a queue; the
queue references below are the state when this was drafted.
**When to use:** when wiring the vault's capture grammar to this repo, and
as the reference for "how do I hand an idea from Obsidian to private-manim".
**How it works:** nothing new is invented. The vault already has the
grammar (`qqq` / `zzz:` / `aaa:`), the queue ([[Shorts Queue]], lens
`shorts-queue`) and the dispatcher (openaugi `zzz:` → task file → tmux
`claude`). Three gaps keep them from reaching this repo; each gets one fix.

## Where the idea stalls today (the three gaps)

Traced through `OpenAugi/AGENT/lenses/shorts-queue.md`,
`lenses/currency-board.md` step 6, openaugi `docs/reference/task-dispatch.md`,
`src/openaugi/agents/task_watcher.py`, and `OpenAugi/AGENT/Repos.md`.

1. **The marker was prose, not the verb.** The board queues a block only
   when a line starts exactly `Aaa: short` (or `Aaa: note`). The 10/24
   block says `Aaa: this is a short, how do I…`, which is a question to the
   board, not the intake verb. So the idea is filed, not queued.
2. **The context lives in a Claude.ai chat the vault cannot see.** The
   prompt that scoped the idea (determinism across substrates, processes vs
   threads in the state loader, what the GIL is, the Zephon article) was
   typed into claude.ai. `chat-harvest` reads only local Claude Code and
   Codex transcripts. Nothing carries that prompt to the block, so any agent
   that picks the idea up starts from one sentence.
3. **`zzz:` dispatch never lands in this repo.** The dispatcher writes no
   `repo:` into the task file, so the task watcher defaults to the vault and
   gives the agent the `augi-agent` brief, not `AGENTS.md`. And
   `Repos.md` does not list private-manim, so even a hand-written
   `repo: private-manim` would not resolve.

The bottleneck is not "idea → Short". It is that the two systems share no
verb and no path. The runbook's step 0 (question, who asks, answer in one
sentence, search phrase) is exactly what the Shorts Queue item already
carries; only the hand-off is missing.

## The capture (what Chris types)

One block in the daily note, same as any other `Qqq` block:

```markdown
Qqq

<the idea, in his words. One or two lines.>

Source: <article URL> · <claude.ai share link, or the prompt pasted as a quote>
> <the prompt he typed into the chat, verbatim>

Aaa: short
```

- `Aaa: short` is the approve-and-queue verb. The next board appends the
  item to [[Shorts Queue]] from the block, and the Question / Who's asking /
  Answer / Search phrase it writes become the top of `storyboard.md`
  (runbook step 0). Storyboards happen when he says "storyboard the queue".
  This is the batch path and it already exists.
- `Zzz: short` is the new **do-it-now** verb (gap 3). It dispatches a
  session in this repo that runs runbook steps 0–1 on that block and
  reports the storyboard path. For an idea he wants to record this week.
- The `Source:` line and the quoted prompt are the context (gap 2). The
  chat's *question* matters more than its answer: the prompt is the
  viewer's question in his own words, which is what step 0 asks for. The
  article URL is one evidence beat at most (runbook step 1, "a paper is
  one evidence beat, never the spine").

The 10/24 block, rewritten this way, is the first test case.

## The changes (three small ones, two repos)

| # | Where | Change | Closes |
|---|---|---|---|
| 1 | `OpenAugi/AGENT/Repos.md` | add `private-manim: /Users/chris/repos/private-manim` | gap 3 |
| 2 | openaugi `pipeline/dispatch.py` (+ `tests/test_dispatch.py`) | when a `zzz:` instruction's first word is `short` (or `storyboard`), write `repo: private-manim` into the task frontmatter and make the `## Task` section: "Read `AGENTS.md`. Run `agents/runbook.md` steps 0–1 for the block in `## Context`: next `videos/NNN-slug/`, the four preflight lines, `ENGINE:`, the beat table. VO from his sentences in the block. Append the item to `OpenAugi/Docs/Shorts Queue.md` with status `storyboarded → videos/NNN-slug/`. Report the storyboard path and the VO word count." Restart the daemon after (`launchctl kickstart -k gui/$(id -u)/com.openaugi.up`). | gap 3 |
| 3 | this repo, `agents/runbook.md` step 0 | one paragraph: a Short may start from a vault block (a `Zzz: short` task file or a Shorts Queue item). Its `## Context` is the source; the quoted prompt is THE QUESTION in the viewer's words; the `Source:` URL is evidence, not the spine. Everything else in step 0 is unchanged. | gap 2 |

Change 2 is generic if the first word is used as a route key (`short` →
private-manim, later `wiki` → earnings-wiki); the lens `shorts-queue` gets
one line under "How an idea gets in": *3. `Zzz: short` storyboards it now.*
The shorts-queue lens stays the owner of the queue format; the runbook
stays the owner of step 0. Nothing is stated twice.

## What this does not do

- It does not pull the Claude.ai chat automatically. Claude.ai has no local
  transcript; the paste (or share link) is the honest capture, and it is
  ten seconds on the phone. If that proves to be the friction, the next
  step is a `chat-harvest` extension reading claude.ai exports, which is a
  separate task.
- It does not record, cut or render. The dispatched session ends at the
  storyboard, like "storyboard the queue" does. Production stays a session
  Chris opens here (AGENTS.md, "How a session runs").

## The title question (already ruled)

Runbook step 9 covers "hook" titles and rules against them, from the
channel's own data: titles that are a phrase people type get 50–77 % of
views from search and keep growing; clever titles get their views from the
feed and stop at 300–600. The rule: *the title starts with the search
phrase from step 0, in those words, then promises it's simple; no clever
hook in the title; the visual is the hook.* So "Everyone writing Python
must know this (the GIL made simple)" becomes `Python GIL Made Simple
(Beginner Friendly)` or `What is the Python GIL? One lock, one thread`,
and the "every Python engineer must know this" line goes in description
line 1 or the Substack note, where it does no harm to search. Step 0's
autocomplete check decides between "python gil", "python global
interpreter lock" and "multithreading vs multiprocessing python".

## Decisions Chris owns

1. Two verbs (`Aaa: short` queue, `Zzz: short` now) or one? Two is the
   recommendation: it keeps the existing batch path untouched.
2. Does `Zzz: short` also append to the Shorts Queue (recommended, so the
   queue stays the one list of what is in flight), or stay off it?
3. Who does change 2: this session (openaugi is a sibling repo on this
   machine) or a session in the openaugi repo?
