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
- "The model can be the same in every app" points at ep 2 without using its numbers, so ep 2's 55-vs-99.9 hook stays fresh.
- Hashimoto, the OpenAI million-lines story and "Agent = Model + Harness" are out of the Short; they're in the key points' companion material. The blob and pipes can stay as the visual: the blob is the model, and four labelled pipes are the harness.

---

## Ep 2. Same Model, Different Harness

**Title:** `AI Agent Harness vs Model: Which Matters More?`
**Backup:** `Same Model, Different Harness (AI Agent Harness)`
**Searched as:** "ai agent harness" (autocomplete ✓ 10/17); top results include "Why The Harness Matters More Than The Model". ✗ "does the harness matter…", "same model different harness".
**Words:** 123 (~51 s)

> Same model, same puzzles. Fifty-five percent in one harness, ninety-nine point nine in another.
>
> That's GPT-6 Astra on ARC-AGI-3: ARC Prize's neutral harness, then OpenAI's own. Same weights, same reasoning setting. Only the harness changed.
>
> The model sees one block of text, and the harness picks what's in it.
>
> A 2026 paper held everything fixed and flipped one setting: trim old tool output as the context fills, and nudge the agent when it repeats itself.
>
> A mid-size open model in a tight twenty-K window went from twenty-eight percent of required tests passing to forty-nine.
>
> The catch: with a huge window, the gain was zero.
>
> The harness matters most when your model is starved for context, so check what it saw before you switch.

**Notes for Chris**
- Your "my read" line from [[2026-09-07 - harness matters]] (post-training inside a scaffold learns a policy for that scaffold's context) was cut: it's a second idea, why a vendor harness wins, between the mechanism and the evidence. It belongs in the companion, framed as your read, since ARC Prize doesn't say why the gap exists.
- "Partly, the old setup just ran out of room" was cut as a hedge on the payoff. The nuance stands: part of the 20K gain is the baseline running out of context.
- The hook rounds 54.8 to "fifty-five". If you want it exact, say "fifty-four point eight" in beat 2. Astra's run is ARC-AGI-3, with OpenAI's provider harness. Don't call it AGI, and don't say "99.9 on ARC-AGI" without the "3".
- Beats 5–6 are Lewis, *Same Model, Different Harness* (arXiv, Aug 2026): Qwen3.6-35B, 4-bit, local, 169 SWE-bench Verified tasks. The setting was a package (trimming, a stall nudge, command safeguards), so don't say "one change". "Huge window" is 262K tokens, where the gain was minus 0.3 points.
- Your Astra line ("Astra arc agi 99.9 was the harness") would fit as a second sentence in beat 1 if you'd rather say it your way: "That was the harness."
- LangChain's Terminal-Bench jump and the Arjmandi counter-study (vendor and neutral harnesses tied on frontier models) belong in the written companion. No long cut was asked for.

---

## Ep 3. Harness 101: build your own

**Title:** `How to Write AGENTS.md: Fix the Repo, Not the Chat`
**Backup:** `AGENTS.md Best Practices Made Simple`
**Searched as:** "how to write agents.md", "agents.md best practices" (autocomplete ✓ 10/17). ✗ "how to set up agents.md".
**Words:** 130 (~54 s); 91 without the two Short D beats

> Your agent isn't the problem. Your repo is underspecified. AGENTS.md is where the fix starts.
>
> When the agent gets something wrong, don't retype the correction. Ask what was missing, and have the agent add it to the repo.
>
> Keep AGENTS.md short: a map that points to your docs, not a manual.
>
> A rule in a doc is a suggestion. A rule in a linter is a wall. Write the error message as the fix, and every failure teaches the agent.
>
> I run the repo that makes these videos this way. After every Short, the agent finds every correction I made and writes each one into the repo.
>
> One font bug showed up twice. Now it's a rule, with a changelog line.
>
> Have good primitives, then let the agents do things.

**Notes for Chris** (max 5 bullets)
- **From Short D (cut these two first if the take runs long, or if D gets its own Short):** "I run the repo that makes these videos this way…" and "One font bug showed up twice…". Without them the script is 91 words and still lands. The font bug is real: `agents/changelog.md`, "Beat brief trap: monospace… rendered in Inter", logged at ep01 and again at ep03, then made a rule. "Into the repo" simplifies runbook step 11 ("into its one home", then a janitor step); say "its one home" if you'd rather.
- **Your own words:** "Have good primitives and then let the agents do things" ([[2026-06-02 - Good Primitives]]), trimmed for the last line. "Fix the repo, not the chat" was cut from the closer; beat 2 already says it.
- **Title:** retitled 10/17 to "How to Write AGENTS.md: Fix the Repo, Not the Chat". The old "AGENTS.md Best Practices" promised more about the file than the script has. "Best practices" is now the backup, and ep 5 owns the CLAUDE.md version.
- **Line 1 is adapted from OpenAI's post**, not yours: "not because Codex was incapable, but because the environment was underspecified." If you want to credit it, say "OpenAI's team found…".
- **Doc vs linter beat** carries Böckeler's guides-vs-sensors framing (martinfowler.com, Apr 2026); the separate "docs steer, checks catch" line was cut as a repeat. The error-message-as-fix idea is OpenAI's custom lints. Don't call ~100 lines a rule if you ad-lib a number for AGENTS.md.
- **The janitor hand-off to 3b was cut**: it gave this Short's viewer nothing. The map beat still hands off to ep 4; the bridge to 3a happens in the visuals.

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
> Ask one question: does your agent read a map before it retrieves? If not, that's your bottleneck. Not the model. Not the prompt. The index.

**Notes for Chris**
- Your own lines, from *Context Engineering is Index Design for Agents*: the magnifying glass and warehouse, "Humans search when…/We turn to agents when…", Map → Assess → Drill → Retrieve, cut down to map, drill, retrieve (the only "how" beat, so it's no longer *(if time)*), and the closing test question, nearly word for word. Cut as repeats of line 1: "Agents need a map. An index…" and "data engineering where the consumer is an agent" (a second definition just before the closer); both fit the companion.
- Line 1's first sentence, "Context engineering is giving your agent a map", is mine. I wrote it to get the search phrase in up front. If it doesn't sound like you, say "Context engineering is index design for agents" (your 3/27 note) instead.
- Context rot: don't say Anthropic coined it. The term comes from Chroma's 2025 report. It's a gradient, not a cliff, which is why the line says "a little worse".
- OpenAI: their post (Feb 2026) came before your essay (Mar 2026), and you got there independently. Say "landed in the same place", not "copied" or "called it first". "When everything is important, nothing is" is a paraphrase of their line, not your own words.
- No Long cut. The key points call for a Short, and the essay is the written companion.

---

## Ep 5. Context as a Playbook (ACE)

**Title:** `CLAUDE.md Best Practices: Don't Rewrite It`
**Backup:** `How to Write CLAUDE.md (Don't Rewrite It)`
**Searched as:** "claude.md best practices", "how to write claude.md" (autocomplete ✓ 10/17). "agents.md best practices" now belongs to ep 3.
**Words:** 159 (~66 s; 143 without the *(if time)* beat)

> Don't let your agent rewrite its CLAUDE.md. Have it make small, labeled edits, or it throws lessons away.
>
> A paper called ACE watched this happen. At step sixty, the agent's notes were eighteen thousand tokens. One rewrite later, a hundred and twenty-two.
>
> The agent did worse than with no notes at all. That's context collapse.
>
> *(if time)* Rewrites also drift toward short, generic advice. The tool quirks that saved you get cut first.
>
> ACE's fix: the context is a list of bullets. Each is one lesson, with a helped-or-hurt count. The model only adds bullets.
>
> Same system, same test. Full rewrites gained three point six points over the baseline. Small edits gained seventeen.
>
> My video repo and my notes vault landed on the same shape. One home per rule. One changelog line per change. A weekly janitor flags rules that repeat or conflict. It reports. I tick what gets fixed.
>
> **[your words]** Next time your agent learns something, have it add one bullet.

**Notes for Chris** (max 5 bullets)
- None of the lines are verbatim from your notes. The receipt beat paraphrases your repo's `AGENTS.md` / runbook step 11 and the OpenAugi janitor ("Drift is proposed, never fixed"). If you want your own words in there, swap the janitor line for "the janitor for agents to de-dupe and have fewer things to maintain" ([[2026-09-13]]).
- Collapse numbers: step 60 was 18,282 tokens; step 61 was 122 tokens, at 57.1% vs a 63.7% no-notes baseline (AppWorld, Dynamic Cheatsheet's full-rewrite mode). "Eighteen thousand" is rounded.
- "Three point six vs seventeen" are percentage points over the ReAct baseline (ACE ablation, AppWorld, DeepSeek-V3.1). Don't say "percent".
- "The model only adds bullets" is true of ACE's public code (the curator is ADD-only; update/delete are TODO). Don't say it updates or deletes bullets.
- Your systems do edit single rules in place, so the script says "same shape", not "never rewrites". If you ad-lib, don't claim you had the idea first.
- The closer is drafted, not yours: it replaced "Don't rewrite the file. Add one small, labeled lesson at a time", which restated line 1. It should be the viewer's next move; say it your way.

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

## Ep 8. A Harness That Improves Itself

**Title:** `Self-Improving AI Agents Made Simple`
**Backup:** `Self-Improving Agent: Harness That Edits Itself`
**Searched as:** "self improving ai agents", "self improving agents" (autocomplete ✓ 10/17). Results lead with Stanford's CS329A course: on topic.
**Words:** 173 (~77 s; ~154 and ~69 s without the *(if time)* beat)

> A self-improving agent is a loop where every change it makes to itself must predict what it fixes.
>
> A 2026 paper, Agentic Harness Engineering, gave a coding agent one shell tool and nothing else.
>
> Every part of the harness was a file. A second agent read the run logs and edited them.
>
> Each edit named what it should fix and what it might break. Next round, if the prediction missed, the edit got reverted.
>
> Ten rounds took Terminal-Bench 2 from sixty-nine point seven percent to seventy-seven, past the hand-built Codex harness.
>
> They added each new piece alone. Memory helped most. So did a better shell tool, and a hook forcing one last real check.
>
> But the agent's seventy-nine lines of prompt advice, added alone to the bare harness, cost two point three points.
>
> *(if time)* The agent kept deleting its own correct output. Prompt advice didn't stop it. A guard in the shell tool did.
>
> Make every harness edit predict what it fixes, revert the misses, and keep the lessons in tools, hooks and memory.

**Notes for Chris**
- No line here is your verbatim wording; none of your key-point lines fit the loop-plus-twist arc in under 170 words. Your published closer, "The loop can do more of the improving now. But it still cannot decide what improvement is for," belongs to the regression-blindness point (7), which this Short skips. Use it in the companion.
- "Alone" appears twice in the twist on purpose. If you ad-lib, keep it: only the prompt swapped in by itself scored worse (67.4 vs 69.7). A prompt edit was part of a winning round, so never say "prompts hurt".
- "Past the hand-built Codex harness" means the paper's own run (Codex 71.9%, GPT-5.4 high, same infrastructure), not a leaderboard. It trails Codex on the Hard tier, so don't say "beat Codex on everything".
- The Pi / "less harness" beat is left out: adding it (four tools, under a thousand tokens, "You don't need ten thousand tokens to tell them you're a coding agent") pushes the take past 90 s. It goes in the companion, framed as "start minimal, let each piece earn its place", not "less harness wins".
- The guard beat (Appendix C, path-tracing) is the first cut. Without it, the takeaway's "tools, hooks and memory" still follows from the ablation beat.

---

## Ep 9. Agents That Share a Notebook (GitSwarm)

**Title:** `Parallel Claude Code Agents: Share One Git Repo`
**Backup:** `Multi-Agent Coding Made Simple (Shared Git Repo)`
**Searched as:** "parallel claude code", "parallel coding agents", "multi agent coding", "agent swarm" (autocomplete ✓ 10/17). Results are mostly git worktrees; the shared-repo angle is the difference.
**Words:** 178 (~74 s); 158 without the *(if time)* beat

> Parallel coding agents should share one notebook. A git repo where every attempt gets committed, even the failures.
>
> Run ten agents and each one starts from zero. When its session ends, what it learned is gone.
>
> A 2026 paper called GitSwarm adds three rules. Keep everything. Allow branches. Say what you built on.
>
> A new agent reads the log, opens a few commits, and picks a gap. If the work is already done, it steps aside.
>
> On ProgramBench, a coding benchmark, about ninety-five percent of what the agents committed got built on later.
>
> *(if time)* The swarm scored seventy-nine percent there. One Codex agent, told to keep working, got sixty-five. That's on a fifty-task subset.
>
> My Minecraft bots share one knowledge folder. My bot Augi couldn't get through its own front door. It fixed that and saved a skill.
>
> Hours later, a new worker bot that had never seen that door loaded the skill. When pillagers showed up, it retreated through that door.
>
> Give parallel agents one git repo, commit every attempt, and make them say what they built on.

**Notes for Chris** (max 5 bullets)
- None of these sentences are quoted from your notes; your only lines on this (the orchestrator line from 1/26, "couldnt open the door" from your 10/12 AugiCraft journal) didn't fit a Short. Say the door beats your own way.
- "About ninety-five percent" is 94.7%, ProgramBench only. On the proof benchmark it's 44.4%, so don't drop "On ProgramBench".
- The 65 is one Codex (GPT-5.5-High) agent re-prompted with "Keep working...", best checkpoint, on 50 of ProgramBench's 200 tasks. If you cut that beat, cut it whole; never say 79 vs 65 without who the 65 is.
- Door timeline (10/12, UTC): skill validated 17:05, worker AugiDiamonds used it to retreat from pillagers at 20:50. "Loaded the skill" comes from its episode log, which lists the knowledge-search tools and the skill under `skills_used`. That's the bot reporting on itself.
- Avoid saying the shared repo *caused* the gains: the paper shows reuse, not causation.

---

## Ep 10. Harness Instead of RL? (+ the human in the harness)

**Title:** `Prompt Optimization Can Beat RL (GEPA Explained)`
**Backup:** `GEPA Prompt Optimization Made Simple`
**Searched as:** "prompt optimization", "gepa prompt optimization", "dspy gepa" (autocomplete ✓ 10/17). ✗ "prompt optimization vs reinforcement learning", "when to fine tune vs prompt".
**Words:** 156 (~65 s)

> You can often match reinforcement learning without training anything. Let a model read its own mistakes and rewrite its own prompt. That's prompt optimization.
>
> A paper called GEPA runs your agent, then hands a second model the whole trace: what it did, what the grader said, even the compiler error.
>
> That model writes a better instruction. Keep it if it scores higher. Repeat.
>
> On a small open model, that beat RL training on five of six tasks. About six points on average, up to nineteen, with up to thirty-five times fewer rollouts.
>
> It works because RL squeezes a whole attempt into one number. The trace says why it failed.
>
> *(if time)* The catch: the harness learned it, the model didn't. Take the prompt away, and the model is no better.
>
> Fix the prompt from your traces first. Train the weights when you need better judgement on one thing, or when it has to be cheap, fast, or private.

**Long cut** (604 words, ~4.5 min). **Title:** `When to Fine-Tune an LLM vs Optimize the Prompt` ("when to fine tune llm" ✓ 10/17)

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
- "That's prompt optimization" (line 1, drafted) says the search phrase; "prompt optimization vs reinforcement learning" isn't something people type. The Short and the long cut now have different titles: the long cut covers when to train, so it takes "when to fine tune llm".
- In the Short, "My rule: prompt a big model first" and the "train the weights when…" beat merged into one traces-first closer; the rule had been said twice. "Prompt a big model first" stays in the long cut.
- Your own words: "Nothing you intend matters, only what the gradient rewards" and "Prompt a big model first", plus the weights-vs-loop pair (9/6 note). The Minecraft hit-observe-plan story and "big model writes the action rules and tools, small classifier decides" are from your 10/12 AugiCraft journal. "Capable interns… nudge them when stuck" is your 6/13 draft. "On my loop, every reframe that unstuck progress came from me", "The step-back was human, every time" and "The step-back and steer is the part that stays human" are from your published post *The Anatomy of a Self-Improving Loop*.
- Rule beat: "cheap, fast, private, off-distribution" is the idea from the 9/6 "They're not successive…" line, which isn't yours. It's reworded here, not quoted. Say it your own way.
- Numbers: six points is v2 of the paper (v1 said 10 percent, so older blog posts will disagree). Nineteen is HotpotQA. Thirty-five times is rollouts on one task (IFBench), not cost. The small open model is Qwen3 8B, mostly LoRA, with a fixed 24,000 RL rollouts.
- The distillation hasn't been run. Keep it as "what I'm trying next", never "I trained". The big model wrote and validated the door and hunting skills on 10/12. The self-defense skill was deprecated, so don't name it.
- "I train models for a living" is hook option 2, your standing, not a sentence from your notes. Swap it for your own phrasing if it feels off.
