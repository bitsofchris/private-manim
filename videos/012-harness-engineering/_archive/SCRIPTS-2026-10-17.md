# Harness Engineering: recording scripts

**Name:** harness-engineering-scripts
**Description:** One VO script per episode in `SERIES.md`, in recording
order, with the YouTube title. Each one is written from that episode's
`key-points.md` (sources checked 2026-10-16) and Chris's own notes and
posts. The KB Shorts 3a–3c come from `agents/plans/agentic-kb-shorts.md`.
**When to use:** the recording session. Each script becomes the VO column
of that episode's `storyboard.md` once its folder is built.
**How it works:** read each script once, straight through (runbook
step 2). A blank line marks a beat, so pause about a second there. Flub?
Pause and re-read the sentence. Lines marked *(if time)* are the first cut
if the take runs long. Every script opens on the answer, not the question.
If a line doesn't sound like you, say it your way: the transcript, not
this file, becomes the captions. Lines marked **[your words]** have no
source sentence yet. Say them however they come out.

**Before you record:** each episode's "Notes for Chris" lists which lines
are yours and which are drafted for you, and any fact to know before you
say it out loud. Say episode 3's Short D beats, and cut later if they
don't fit. Episode 10 has a Short and a long cut, so record both.

Titles follow the runbook rule (step 9). Search phrases were checked on
2026-10-17 against YouTube autocomplete (US English) and the top results;
✗ marks a phrase autocomplete doesn't offer.

Status: draft, 2026-10-16; tightened 2026-10-17 (repeats and lines that delay the point cut). Not yet recorded.

---

## Ep 1. What Is an Agent Harness?

**Title:** `What Is an Agent Harness? The 4 Parts Explained`
**Backup:** `What Is an Agent Harness? Everything But the Model`
**Searched as:** "what is agent harness", "agent harness", "ai harness engineering" (autocomplete ✓ 10/17). Not plain "harness engineering": it returns wiring harnesses.
**Words:** 205 (~85 s)

> An agent harness is everything except the model. It decides what the model sees, what it can do, what it remembers, and when it's done.
>
> Context is what goes in on this turn: your instructions, the files it opened, the last error.
>
> Tools are what it can touch: read a file, run a command, search the web. The model only asks. The harness runs it.
>
> Memory is what carries over when the session ends: notes and rules, like an AGENTS.md, loaded back in next time.
>
> The loop runs the model, runs the tool, feeds the result back, and checks the work. Try again, or stop.
>
> Here's all four at once. You ask Claude Code to fix a failing test. The test and your request go into context. The model asks to run the tests. The harness runs them, and the error goes back in. It edits the code, and the loop runs the tests again. Green. It stops.
>
> The model can be the same in every app. The harness is why one agent fixes your bug and another goes in circles.
>
> So when your agent fails, don't blame the model first. Ask which piece was missing: the context, a tool, the memory, or the check.

**Notes for Chris**
- Rewritten 10/17 around the four parts: what a harness is, its pieces, how they work together, why it matters. The four are your 9/7 note ([[2026-09-07 - harness matters]]: "Context, state (memory), tools, prompts"); prompts fold into context. The sentences are drafted, so say them your way.
- There's no official taxonomy (write-ups list 4 to 12 parts), but the sources worth citing all come down to these four: Anthropic's *Building Effective Agents* (an LLM "enhanced with augmentations such as retrieval, tools, and memory", and agents as "LLMs using tools based on environmental feedback in a loop"), Lewis (a harness "decides what the model sees, which tools it can use, and how the work continues"), LangChain's *Anatomy*. Guardrails sit inside tools, checks and stop conditions inside the loop, subagents are a loop calling a loop. Details in `ep01-what-is-a-harness/key-points.md`.
- "The model only asks. The harness runs it." is literal: the model outputs a tool call, and harness code runs it and returns the result.
- "The model can be the same in every app" is the only why-it-matters line; episode 2 was dropped 10/17, so no episode carries the Astra numbers.
- Hashimoto, the OpenAI million-lines story and "Agent = Model + Harness" are out of the Short; they're in the key points' companion material. The blob and pipes can stay as the visual: the blob is the model, and four labelled pipes are the harness.

---

## Ep 3. Harness 101: good primitives

**Title:** `Claude Code Best Practices: Files, Tools, Checks`
**Backup:** `How to Write AGENTS.md: Fix the Repo, Not the Chat`
**Searched as:** "claude code best practices", "how to write agents.md", "agents.md best practices" (autocomplete ✓ 10/17).
**Question:** How do I set up my repo so Claude Code stops making the same mistakes?
**Who's asking:** someone who corrects their agent in chat and sees the same mistake next session.
**Answer:** "Have good primitives, then let the agents do things": files, small CLIs, checks.
**Words:** 170 (~71 s)

> Have good primitives, then let the agents do things. That's how you set up a repo for Claude Code.
>
> You correct your agent in chat. Next session, the chat is gone and the mistake is back.
>
> Put the fix in the repo instead, as one of three primitives.
>
> One: everything is a file. Your plan, your rules, your notes. The agent reads them every session. Keep AGENTS.md short, a map that points to the rest.
>
> Two: small tools chained together. Lots of little CLIs, specific to your work. Then it's easier for the agent to do stuff.
>
> Three: checks. A test or a linter that fails loud, with an error message that says how to fix it.
>
> This repo makes my videos. AGENTS.md is the map. There's a CLI for every step: clean the audio, cut it, burn in the captions. A font bug that showed up twice is now a rule.
>
> Next time you type the same correction twice, turn it into a file, a tool, or a check.

**Notes for Chris**
- Rewritten 10/17 from your notes, around one answer: good primitives. Your words: "Have good primitives and then let the agents do things" ([[2026-06-02 - Good Primitives]]), "Everything is a file" and "small tools chained together - making lots of CLIs - specific to your use case, then it's easier for agent to do stuff" ([[2026-01-21 - Unix philosophy - cli for agents]]). The rest is drafted; say it your way.
- The receipt is this repo: `AGENTS.md` (the map), `tools/` (`enhance_vo.sh` cleans the audio, tighten cuts it, `assemble.py` burns in captions), and the font bug: `agents/changelog.md`, "Beat brief trap: monospace… rendered in Inter", logged at ep01 and ep03, then made a rule.
- "An error message that says how to fix it" is OpenAI's custom-lint idea (Lopopolo, 11 Feb 2026), in plain words.
- Out of this Short: OpenAI's "underspecified" opening, the doc-vs-linter line, and the changelog idea (ep 5 owns it). Ep 1's closer diagnoses ("which piece was missing?"); this one builds ("a file, a tool, or a check").

---

## Ep 3a. The four layers an LLM wiki needs (KB Short A)

**Title:** `LLM Wiki: The 4 Layers It Needs`
**Searched as:** "llm wiki", "llm knowledge base" (autocomplete ✓ 10/17). Results are all Karpathy's LLM Wiki: searchers arrive expecting his pattern.
**Status:** script agreed 10/11, pending one read-aloud. Every line is
yours (the 10/2 note and your 10/11 chat answer). Built on the building
set.

> A good LLM wiki needs four layers.
>
> One place for agents to write, one place for humans. That needs to be separate.
>
> The agent layer. A place where agents write for agents. They include the details needed to resume a task later: hashes, branches, commits. You never have to read it.
>
> The human layer. A clean, distilled view that links out to the detailed agent nodes. A dashboard, a Kanban board, a map.
>
> The curated layer. Agent context and rules the human needs visible. The things you maintain carefully and edit to keep accurate.
>
> The janitor. As you iterate and change the system, something has to keep it clean.
>
> With all four layers you get a strong agentic knowledge base.

---

## Ep 3b. Your system needs a janitor (KB Short B)

**Title:** `Why Your AI Agent Setup Gets Messy` (feed Short; checked 10/17, no search phrase fits)
**Status:** draft. Beat 3 needs your words.

> The janitor for agents: de-dupe and have fewer things to maintain.
>
> As you iterate and change the system, something has to keep it clean.
>
> **[your words]** The queue story: an agent drafted post ideas every week, nothing removed them, it reached sixty-seven, and you stopped opening it.
>
> It catches conflicting rule sets before they spread. It keeps the source of truth clean. It files away or cleans up old material so the human layer stays useful.

---

## Ep 3c. Let your agent write notes you never read (KB Short C)

**Title:** `Claude Code Memory: Notes You Never Read`
**Searched as:** "claude code memory" (autocomplete ✓ 10/17), one of the strongest phrases in the series.
**Status:** draft. Every line is from your 10/2 note except the last beat,
which needs your words.

> You never have to read it or go there. It's the agent's own memory of what's worth keeping.
>
> Agents can be as verbose as they need to be. They include the details needed to resume a task later: hashes, branches, commits, table names, file counts.
>
> The point is to save context for later, not to be readable.
>
> Your view is a clean, distilled one that links out to the detailed agent nodes.
>
> **[your words]** One sentence on how this fits "same surface, two authors, visible seam": the agent's detail lives in its own layer, and your view links to it.

---

## Ep 4. Give Your Agent a Map

**Title:** `Context Engineering: Give Your Agent a Map`
**Backup:** `Context Engineering for Agents Made Simple`
**Searched as:** "context engineering", "context engineering for agents", "claude code context window" (autocomplete ✓ 10/17). ✗ "agents.md too long".
**Words:** 145 (~60 s)

> Context engineering is giving your agent a map. Today agents are using a magnifying glass to search through a warehouse.
>
> Humans search when they know what they're looking for. We turn to agents when we're unsure what we need. So they explore.
>
> The obvious fix is to stuff everything in. It backfires. As the window fills, the model gets a little worse at finding what's in it. Researchers call this context rot.
>
> OpenAI landed in the same place. One giant AGENTS.md failed. When everything is important, nothing is. So they cut it to about a hundred lines: a table of contents.
>
> The map holds pointers, not data. The agent reads the map, drills in, then retrieves only what it needs.
>
> Ask one question: does your agent read a map before it retrieves? If not, that's your bottleneck: the index.

**Notes for Chris**
- Your own lines, from *Context Engineering is Index Design for Agents*: the magnifying glass and warehouse, "Humans search when…/We turn to agents when…", Map → Assess → Drill → Retrieve, cut down to map, drill, retrieve (the only "how" beat, so it's no longer *(if time)*), and the closing test question, nearly word for word. Cut as repeats of line 1: "Agents need a map. An index…" and "data engineering where the consumer is an agent" (a second definition just before the closer); both fit the companion.
- Line 1's first sentence, "Context engineering is giving your agent a map", is mine. I wrote it to get the search phrase in up front. If it doesn't sound like you, say "Context engineering is index design for agents" (your 3/27 note) instead.
- Context rot: don't say Anthropic coined it. The term comes from Chroma's 2025 report. It's a gradient, not a cliff, which is why the line says "a little worse".
- OpenAI: their post (Feb 2026) came before your essay (Mar 2026), and you got there independently. Say "landed in the same place", not "copied" or "called it first". "When everything is important, nothing is" is a paraphrase of their line, not your own words.
- No Long cut. The key points call for a Short, and the essay is the written companion.

- Closer changed 10/17 from "Not the model. Not the prompt. The index." to "that's your bottleneck: the index" (effective-writing bans the "it's not X, it's Y" pattern).
---

## Ep 5. Context as a Playbook

**Title:** `CLAUDE.md Best Practices: Don't Rewrite It`
**Backup:** `How to Write CLAUDE.md (Don't Rewrite It)`
**Searched as:** "claude.md best practices", "how to write claude.md" (autocomplete ✓ 10/17). "agents.md best practices" now belongs to ep 3.
**Question:** How do I keep my CLAUDE.md from turning into a mess?
**Who's asking:** someone who ends sessions with "update CLAUDE.md with what we learned."
**Answer:** grow it one line at a time, one place per rule, and never let the agent rewrite the whole file.
**Words:** 151 (~63 s)

> Your CLAUDE.md stays useful when it grows one line at a time. Let the agent rewrite it, and it throws away the lessons that mattered.
>
> You end a session and say "update CLAUDE.md with what we learned." The agent rewrites the file. It comes back shorter and cleaner, and the quirk that saved you an hour is gone.
>
> A paper called ACE measured this. One rewrite took an agent's notes from eighteen thousand tokens to a hundred and twenty-two. Then it did worse than with no notes at all.
>
> The fix is a playbook. Each lesson is one bullet. The agent adds bullets. It doesn't rewrite them.
>
> My video repo runs on two rules. One home per rule: never state the same rule in two files, link instead. And one changelog line for every change, with the video that forced it.
>
> Next time your agent learns something: one line, one place.

**Notes for Chris**
- Rewritten 10/17: your system leads, ACE is one beat. The two rules are this repo's (`AGENTS.md`, "Keeping the system clean": "Never state the same rule in two files. Link instead."; `agents/changelog.md`: "One line per change … with the video that forced it"). The sentences are drafted; say them your way.
- The "quirk that saved you an hour" scene is a second-person example of ACE's *brevity bias* (rewrites drop domain detail for concision), not a story from your sessions. If you have a real one, use it as "I".
- Collapse numbers: step 60 was 18,282 tokens; step 61 was 122 tokens, at 57.1% vs a 63.7% no-notes baseline (AppWorld, Dynamic Cheatsheet's full-rewrite mode). "Eighteen thousand" is rounded.
- "The agent adds bullets" is true of ACE's public code (the curator is ADD-only). Your systems do edit single rules in place, so don't say yours never rewrite.
- Out: the 3.6-vs-17 ablation, the helped-or-hurt count, and the janitor (3b owns it).

---

## Ep 6. Write the Skill After the Work

**Title:** `Claude Skills Explained: Write Them After the Work`
**Backup:** `Claude Code Skills Explained: Save What Worked`
**Searched as:** "claude skills explained", "claude code skills explained" (autocomplete ✓ 10/17). Avoid plain "agent skills": autocomplete mixes in Digimon.
**Words:** 171 (~71 s)

> A Claude skill is a procedure that worked, saved where the agent can find it. The trick is writing it after the work.
>
> It's a folder with a SKILL.md file: a name, a description, and the steps. The agent only reads the description until a task matches.
>
> My Minecraft agents kept getting stuck at the house. They couldn't open the door.
>
> So an agent built a small door tool, with tests, and found the real bug: the pathfinder treated an open door as a wall.
>
> Then it wrote the steps down as a skill. It was only promoted after a second, separate run worked.
>
> That order matters. A benchmark called SkillsBench had agents write skills up front, before doing the task. They did worse than with no skills. Claude Code with Opus 4.7 dropped about eight points.
>
> Expert-written skills helped by about sixteen points. A skill written before the work is a confident guess, written down.
>
> Save the skill from the run that worked, and trust it once it works again.

**Notes for Chris**
- His own words: "couldn't open the door" (10/12 journal, [[2026-10-11 - LLM Plays Minecraft - AugiCraft]]). Everything else is built from key-points "Say it" lines, not his notes; say any of it your way.
- "About eight points" is minus 8.1 percentage points, and that run used effort "max" vs "high" for the baseline; the authors call it a diagnostic. Don't say "percent". "Sixteen points" is the curated average across 18 configs, not the same three.
- Only the door skill (and livestock hunting) is validated. Don't ad-lib climbing or fighting. Both door successes were logged back to back on 10/12, so "second, separate run", not "another day".
- "An agent" built the door tool; a manager agent installed part of the fix. Keep it plural-safe, not "my bot did it alone".
- No long cut: key points call for a Short plus a written companion (progressive disclosure, SkillForge, MemSkill go there).
- The door skill's steps (walk to the entrance, open the door, step inside, check, deposit) go on screen as the SKILL.md, not in the VO: that's this Short's code beat. The expert-skills beat is no longer *(if time)*: without it, viewers hear "skills hurt".

---

## Ep 7. The check is the pipe that matters

**Title:** `Evals for AI Agents: The Check Matters Most`
**Backup:** `AI Evals Explained: The Check Owns the Loop`
**Searched as:** "evals for ai agents", "ai evals explained" (autocomplete ✓ 10/17). ✗ "verifier's law".
**Words:** 166 (~69 s; 154 without the *(if time)* beat)

> The most important part of an agent setup is the eval: the check that tells it whether it got better.
>
> AI researcher Jason Wei calls this the verifier's law. The easier a task is to verify, the easier it is to train AI to do it.
>
> Your agent loop is the same idea: try, check, try again. With a vague check, it just circles.
>
> At work, a coding agent spent two weeks on a data loader. The goal: "faster with less memory." That sounds like a target. It isn't. Faster than what?
>
> The loop only started compounding once I wrote an experiment contract. This config, this many steps. Measure these five things. Beat the baseline.
>
> Then the check lied. Memory looked scary bad, until I fixed how I measured it. Most of it was reclaimable cache. The verdict flipped.
>
> A bad gauge is worse than no gauge.
>
> *(if time)* It can lead the loop to optimize confidently in the wrong direction.
>
> Whoever owns the check owns the loop.

**Notes for Chris**
- Your published words (The Anatomy of a Self-Improving Loop): "That sounds like a target. It isn't. Faster than what", the experiment-contract line (trimmed for speech: dropped "this model", "this data mix" and "while holding correctness"), "scary bad", "reclaimable cache", and "A bad gauge is worse than no gauge. It can lead the loop to optimize confidently in the wrong direction."
- "Whoever owns the check owns the loop" is from your 9/6 verifiable note ("Whoever owns that owns the loop"), so it's the one closer; the drafted "Write the check before you let it loop" was cut as a second takeaway. "It just circles" is the key-points framing, not a quote. "The eval" in line 1 is there for the search phrase.
- Wei wrote about *training* AI; the loop beat says "the same idea", not that his law proves anything about harnesses. His live page now says "verifier's rule"; either name is fine.
- "Two weeks" and "data loader" are as published. Keep it generic: no internal format name, no colleagues.
- If "Beat the baseline" feels thin, add back "while holding correctness" (+3 words, 175, still under the cap).

---

## Ep 8. A Self-Improving Agent

**Title:** `Self-Improving AI Agents Made Simple`
**Backup:** `Self-Improving Agent: Harness That Edits Itself`
**Searched as:** "self improving ai agents", "self improving agents" (autocomplete ✓ 10/17). Results lead with Stanford's CS329A course: on topic.
**Question:** How do I make an agent loop improve instead of going in circles?
**Who's asking:** someone who has let an agent loop run and come back to churn.
**Answer:** your four ingredients: visibility, an objective that fights back, lessons that persist, space to step outside.
**Words:** 175 (~73 s)

> A self-improving agent needs four things: visibility, an objective that fights back, lessons that persist, and space to step outside the loop. Miss one, and it circles.
>
> A prompt plus a retry can run all night and end where it started.
>
> Visibility: you can see what changed and why. Metrics, logs, the raw traces.
>
> An objective that fights back: a check the agent can't talk its way past. Tests it hasn't seen. A judge that gets stricter as the agent gets better.
>
> Lessons that persist: what worked gets written down as notes, skills and tools, so round two starts ahead of round one.
>
> Space to step outside: someone looks at the loop itself and asks if it's headed the right way.
>
> My data loader loop had the first three, and it still got stuck. The agent only read one file at a time and never considered just scanning rows. I had to step in. That's the fourth.
>
> Before you let your agent loop overnight, check all four. The one you're missing is where it'll circle.

**Notes for Chris**
- Rewritten 10/17 on your published *The Anatomy of a Self-Improving Loop* (bitsofchris.com, 14 Jun 2026): the four ingredients as published ("visibility, an objective that fights back, lessons that persist, and space to step outside the loop"). Draft in [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]].
- "Tests it hasn't seen" is LangChain Better-Harness's holdout sets; "a judge that gets stricter" is Recursive's evaluator arms race. Both are in your post.
- The stuck beat is your 6/11 note in [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]]: "It got stuck to this idea of only reading a single a file and never considered just scanning rows from a file." Ep 7 uses the same project's vague-goal and lying-gauge beats; this is a different slice. Keep it generic: no internal format name, no colleagues.
- Out: AHE (Terminal-Bench numbers, the 79-line prompt twist) and Pi / "less harness". Both go to the companion.

---

## Ep 9. Agents That Share a Notebook

**Title:** `Parallel Claude Code Agents: Share One Notebook`
**Backup:** `Multi-Agent Coding Made Simple (Shared Git Repo)`
**Searched as:** "parallel claude code", "parallel coding agents", "multi agent coding", "agent swarm" (autocomplete ✓ 10/17). Results are mostly git worktrees; the shared-notebook angle is the difference.
**Question:** How do I run several agents without them redoing each other's work?
**Who's asking:** someone running parallel Claude Code agents.
**Answer:** give them one shared record where each agent writes what it learned and what it built on.
**Words:** 198 (~82 s)

> Parallel coding agents get better together when they share one notebook: a place where every agent writes what it learned and what it built on.
>
> Run agents in parallel without one, and each starts from zero. When a session ends, what it learned is gone.
>
> I built agents to play Minecraft. The first one started badly. Agents don't know how to play Minecraft. They generate text. So I let it learn and take notes for itself, until it mined diamonds and brought them back to a chest.
>
> Once one worked, it was easy to add more. I spawned four agents, each with its own job, all reading the same notes.
>
> Hours later, a new bot that had never seen our front door loaded the door skill the first bot saved. When pillagers showed up, it retreated through that door.
>
> A paper called GitSwarm does this with a git repo. Every attempt gets committed, even the failures, and every agent says what it built on. On a coding benchmark, about ninety-five percent of the work got built on later.
>
> Give your parallel agents one shared record. Have each one write what it learned, and say what it built on.

**Notes for Chris**
- Rewritten 10/17 from your AugiCraft journal ([[2026-10-11 - LLM Plays Minecraft - AugiCraft]]): the 10/17 entry ("had to let it learn and take notes for itself", "agents don't know how to play Minecraft they generate text", "once we had one working it was easy to add more") and 10/12 ("spawned an army of 4 agents… gave each their own jobs", diamonds returned with a chest). Say it your way.
- Door timeline (10/12, UTC): skill validated 17:05; worker AugiDiamonds used it to retreat from pillagers at 20:50. "Loaded the skill" comes from its episode log (`skills_used`), the bot reporting on itself. Ep 6 tells how the skill was made; this beat only shows reuse.
- GitSwarm (Shah et al., arXiv 2610.04862): "about ninety-five percent" is 94.7% on ProgramBench ("a coding benchmark"); on the proof benchmark it's 44.4%, so keep "coding". The paper shows reuse, not that the shared repo caused the gains.
- Out: the 79-vs-65 comparison and the three-rules list.

---

## Ep 10. Prompt or Train? (+ the human in the harness, long cut)

**Title:** `When to Fine-Tune an LLM: Prompt a Big Model First`
**Backup:** `When Should You Fine-Tune an LLM? Prompt First`
**Searched as:** "when to fine tune llm", "prompt optimization", "gepa prompt optimization" (autocomplete ✓ 10/17). ✗ "prompt optimization vs reinforcement learning", "when to fine tune vs prompt".
**Question:** Should I fine-tune, or just prompt?
**Who's asking:** an engineer weighing fine-tuning or RL for an agent task.
**Answer:** "Prompt a big model first - establish a baseline, then distill."
**Words:** 203 (~85 s)

> Prompt a big model first. Establish a baseline. Then decide if training is worth it.
>
> Training feels like the serious move. But with training, nothing you intend matters. Only what the gradient rewards.
>
> And a prompt can go a long way. A paper called GEPA has a model read its own traces, what it did and what the grader said, and rewrite its own prompt. On a small open model, that beat RL training on five of six tasks, with up to thirty-five times fewer rollouts.
>
> So when do you train the weights? When you need better judgement on one thing. Or when it has to be fast.
>
> My Minecraft bots hit that wall. A big model figured out the skills: get through a door, hunt an animal. But it was slow at every step. It would hit, stop, look, see the animal moved, plan a step, plan another hit. The animal got away.
>
> So here's what I'm trying next. The big model writes the tools and the rules. A small, fast classifier learns which one to use. Prompt first, then distill.
>
> Before you train anything, prompt the biggest model you can and measure it. That number is what training has to beat.

**Long cut** (604 words, ~4.5 min). **Title:** `Prompt Optimization Can Beat RL (GEPA Explained)` ("prompt optimization", "gepa prompt optimization" ✓ 10/17). Not yet rebuilt on the Short's rule; revisit after the Short.

> You can often match reinforcement learning without training anything. Let a model read its own mistakes and rewrite its own prompt.
>
> I train models for a living. So I want to know when I don't have to.
>
> A paper called GEPA runs your agent on a few examples. Then it hands a second model the whole trace: what the agent did, what the grader said, even the compiler error.
>
> That model writes a better instruction. Keep it if it scores higher, and repeat.
>
> The first prompt in the paper is one line. Given the question and a summary, produce a query. After a few rounds, it's a page of rules for that exact task. Things like: don't just paraphrase the question.
>
> And it doesn't only keep the single best prompt. It keeps every prompt that wins on at least one example. That way it doesn't get stuck polishing one idea.
>
> In their tests, on a small open model, that beat RL training on five of six tasks. About six points on average, up to nineteen, with up to thirty-five times fewer rollouts.
>
> Five of six, not six. RL still won on the math competition set. And thirty-five times fewer rollouts isn't thirty-five times cheaper. The rewriting model costs something too.
>
> It works because RL squeezes a whole attempt into one number. With RL, nothing you intend matters, only what the gradient rewards. The trace says why it failed: which step went off, what the test complained about.
>
> Here's the catch. The harness learned it, the model didn't. Take the prompt away, and the model is exactly as good as it was.
>
> One paper calls this kind of agent memory a memo, not true memory. It's a diary you have to remember to open, not a lesson you've learned.
>
> That's usually fine, and often better. You can read it, edit it and delete it. But the paper argues that for new combinations the model never saw, weights can learn from fewer examples than a growing pile of notes. It's a position paper, and it also says notes were the right thing to ship.
>
> So here's the rule I use. Prompt a big model first. That's your baseline, and often it's enough.
>
> Train the weights when you need better judgement on one thing, or when it has to be cheap, fast, private, or off what frontier models have seen. Train the loop when the problem is long, or made of many steps.
>
> My Minecraft bots showed me where this goes. A big model is great at figuring out a skill: getting through a door, hunting animals.
>
> But it's slow at every single step. My bot would hit an animal, stop, look, notice it moved, plan a step, plan another hit. And the animal got away.
>
> So that's what I'm trying next. The big model writes the tools and the rules. A small, fast classifier learns which one to use next. The harness teaches, and the weights learn.
>
> *(if time)* If the harness improves itself, and the weights learn from the harness, what's left for you?
>
> On my loop, every reframe that unstuck progress came from me. The agent did the grinding. The step-back was human, every time.
>
> We have our capable interns. They don't tire. So let them run in loops, and nudge them when they're stuck.
>
> And read the raw traces yourself. The Langfuse team makes this point, and I agree: that's where your opinion forms, and how you notice you're measuring the wrong thing.
>
> Let the harness learn, and let the weights learn from it. The step-back and steer is the part that stays human.

**Notes for Chris**
- The Short was rewritten 10/17 around your rule from [[2026-09-06 - Post Training, Loss functions, verifiable]]: "Prompt a big model first - establish a baseline, then distill". Also yours: "Nothing you intend matters, only what the gradient rewards", "train when need better judgement on the thing", and the AugiCraft hit-observe-plan story and big-model-writes-tools / small-classifier idea (10/12 journal). Connecting lines are drafted; say them your way.
- "Or when it has to be fast" replaces "cheap, fast, or private": that list is from the 9/6 "They're not successive…" line, a pasted AI reply, not yours. Your bots are the fast case.
- GEPA is one beat. "Five of six tasks" on Qwen3 8B against GRPO; RL won on AIME. Thirty-five times is rollouts on one task (IFBench), not cost.
- Long cut: unchanged and still GEPA-led, with the human-in-the-harness ending. "Capable interns… nudge them when stuck" is your 6/13 draft; "every reframe that unstuck progress came from me" and "the step-back was human, every time" are from your published *The Anatomy of a Self-Improving Loop*. "I train models for a living" is your standing, not a line from your notes.
- Numbers: six points is v2 of the paper (v1 said 10 percent, so older blog posts will disagree). Nineteen is HotpotQA. Thirty-five times is rollouts on one task (IFBench), not cost. The small open model is Qwen3 8B, mostly LoRA, with a fixed 24,000 RL rollouts.
- The distillation hasn't been run. Keep it as "what I'm trying next", never "I trained". The big model wrote and validated the door and hunting skills on 10/12. The self-defense skill was deprecated, so don't name it.
