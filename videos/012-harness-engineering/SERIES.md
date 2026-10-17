# Harness Engineering: the series

**Name:** harness-engineering-series
**Description:** Home base for a series on agent harnesses: what wraps the
model (context, memory, tools, checks, the loop), why it moves results as
much as the model does, how to build your own, and what research is doing
with it now. The arc, one entry per episode, the sources each episode
stands on, Chris's own vault notes behind each one, and what Chris needs
to learn or try before recording.
**When to use:** at the start of any session on this series. Pick the next
episode from the checklist, do its "learn first" step, then run
`agents/runbook.md` from step 0 in that episode's folder. Update the
checklist in the same pass as the work.
**How it works:** each episode has a researched `epNN-slug/key-points.md`
(done 2026-10-16). It has hook options, the points in episode order with
checked evidence, Chris's own lines, a visual, the takeaway, and a
"Don't say" list. All scripts, in recording order, are in `SCRIPTS.md`
(drafted 2026-10-16 from the key points). The folder becomes a normal Short folder once the
script is agreed. **Where this page and a key-points file disagree, the
key-points file wins.** It was checked against the primary sources; this
page is the overview. Episodes 3a–3c are the agentic KB Shorts. Their scripts live in
`agents/plans/agentic-kb-shorts.md`, not here. Status: **spike,
2026-10-13**. Agreed so far (Chris, 10/13):
- The KB Shorts fold in, and the series keeps two recurring images
  (below).
- The episode list below is final for now: ten episodes plus 3a–3c.
- KB Short D gets tried inside episode 3. What stays is decided at script
  time.
- **Recording is in series order, audio first.** Chris records each
  episode's whole script as audio, then the visuals are built.

**Vault pointers.** `[[Note name]]` is a note in Chris's Obsidian vault
(`~/Documents/ZK Home`). Open it with the quick switcher. *(Chris)* marks
his own writing. *(Readwise)* marks his highlights of someone else's
piece. *(Augi)* marks an agent-written note. Quotes from his notes are
his words and can be cut into VO. Anything else is a summary.

## Who it is for

Engineers and research engineers who use coding agents (Claude Code,
Codex) every day. They want to understand the state of harnesses and
context management well enough to get more out of the model: in their
own tooling, their repo's agent setup, and their day-to-day agent
sessions. They know what a prompt, RAG, and RL are. They don't follow the
agent papers.

## The promise

**The same model does very different work depending on what you build
around it. Here is what that harness is, why it matters this much, how to
build yours, and where the research is taking it.**

Chris's angle, which no other harness explainer has: he builds models for
a living (so he can say when to train instead), and he runs his own
harnesses daily. This repo, OpenAugi over his vault, and AugiCraft
(Minecraft agents) give him receipts for nearly every episode.

## The two recurring images

1. **The blob and the pipes** (the series image, from
   `ep01-what-is-a-harness/idea.md`). The model's intelligence is a blob
   of energy. Poke it and you get a blob back. With a prompt and context
   it gets shape and texture. Memory and use make it sharper. A harness is
   a machine of pipes it flows through, and it comes out as sharp work.
   Every later episode zooms into one pipe.
2. **The building in cross-section** (Act 2's knowledge-base episodes
   3a–3c, from `agents/plans/agentic-kb-shorts.md`). Basement is the agent
   layer, upstairs the human layer, a glass case for the curated layer,
   and a janitor between floors. The bridge between the two images is that
   the knowledge-base pipe, opened up, is the building.

## The arc

| Act | Episodes | The viewer leaves able to say |
|---|---|---|
| 1. What and why | 1–2 | Agent = model + harness. Changing the harness alone can move results a lot, because the model only acts on what the harness shows it. |
| 2. Build yours | 3–7 (with 3a–3c) | My repo's knowledge base, checks and cleanup are a harness. My agent needs a map, not a search box. Context grows by small edits. Skills are saved procedures. The check is the pipe that matters most, and whoever owns it owns the loop. |
| 3. The frontier | 8–10 | An agent can improve its own harness from its traces, and more harness isn't better. Many agents can build on one shared record. Language feedback can sometimes beat RL, which tells me when to edit context and when to train, and the human still supplies the reframes. |

## Episodes

The search phrases below are the first guesses. The checked phrases and
titles (YouTube autocomplete, 2026-10-17) are in `SCRIPTS.md`. "Read" marks how deep each source has been checked so
far. *abstract* means only the abstract has been read. *search* means
only a search summary. *highlights* means only Chris's Readwise
highlights. **New 10/13** marks an episode added from the vault pass.

---

## Act 1. What and why

### 1. What is an agent harness?

- **Question:** What do people mean by "harness"?
- **Answer:** Everything around the model except the weights: the
  context it sees, the memory it keeps, the tools it can call, and the
  loop that checks its work and decides when to stop.
- **Search phrase:** agent harness / what is harness engineering
- **Hook image:** the blob, then the pipes.
- **Chris's own words:**
  - "Harness is: Context, state (memory), tools, prompts". From
    [[2026-09-07 - harness matters]] *(Chris)*.
  - "Code used to be our leverage - now its setting up, steering,
    managing, and connecting agents." From
    [[New Programming Language is Agent Orchestration]] *(Chris, 1/19)*.
  - "I'm building a personal agent harness." From
    [[2026-02-21 - AE3 - Issue 3]] *(Chris)*. That issue already
    gathered the four Feb reads on harnesses and was never sent.
  - [[Post - Harness Engineering 101]] *(Chris)* is a one-line stub
    (2/22). It becomes this episode's written companion.
- **Definitions to choose from:**
  - The car: the model is the engine, and the harness is the chassis,
    transmission and safety systems. From [[OpenAI - Harness Engineering]]
    (vault summary). **Not OpenAI's**: it comes from a Medium post that
    summary cites.
  - "Agent = Model + Harness". From LangChain, *The Anatomy of an Agent
    Harness* (Trivedy, 10 Mar 2026).
  - "A harness is the set of constraints, tools, documentation, and
    feedback loops that keep an agent productive and on track." From
    [[The Emerging Harness Engineering Playbook]] *(Readwise, Guo)*.
  - "An agent harness has a lot of knobs: system prompts, tools,
    hooks/middleware, skills, sub-agent delegation, memory systems." From
    [[Improving Deep Agents With Harness Engineering]] *(Readwise,
    LangChain)*. Chris's margin note on it: "Basically what I'm building
    with open augi Cli right now?"
- **Sources:** OpenAI, [Harness engineering: leveraging Codex in an
  agent-first world](https://openai.com/index/harness-engineering/)
  (vault summary: [[OpenAI - Harness Engineering]]) · Böckeler, [Harness
  Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
  ([[Harness Engineering]], highlights) · Guo, [The Emerging Harness
  Engineering Playbook](https://www.ignorance.ai/p/the-emerging-harness-engineering)
  (highlights) · [The State of AI Harness Engineering
  2026](https://marmelab.com/blog/2026/09/24/the-state-of-ai-harness-engineering-2026.html)
  (read: search).
- **Key points:** `ep01-what-is-a-harness/key-points.md`.
- **Settled (10/16):** Mitchell Hashimoto *named* it on 5 Feb 2026 ("I've
  grown to calling this 'harness engineering'"), and OpenAI's post
  (Ryan Lopopolo, 11 Feb 2026, now read in full) made it famous. Say
  "named", not "coined". The core rule is his: "anytime you find an
  agent makes a mistake, you take the time to engineer a solution such
  that the agent never makes that mistake again".

### 2. Same model, different harness

- **Question:** Does the harness matter as much as the model?
- **Answer:** Often, yes, and sometimes more. The same model scored 54.8%
  in ARC Prize's standard harness and 99.9% in its provider's own harness
  (ARC-AGI-3, GPT-6 Astra). The gap is biggest where the model is
  starved, with a tight context or long messy tasks, and it can shrink to
  nothing when the model has room. The model only acts on what the harness
  puts in front of it.
- **The controlled experiment:** one harness configuration took a local
  open model from 28.0% to 49.1% mean fail-to-pass on 169 SWE-bench
  Verified tasks (43 to 72 solved), and it helped three other open models
  too. The configuration was three changes together: trimming old tool
  output, a nudge when the agent repeats itself, and command safeguards.
  The paper doesn't separate their effects. Conditions: a 20K-token
  window. At 262K tokens the gain was −0.3 points.
- **Search phrase:** does the harness matter more than the model (guess)
- **Why it works (the explainer beat):** from
  [[2026-09-07 - harness matters]] *(Chris)*: "When you post-train
  (especially with RL) inside a specific scaffold, the model isn't
  learning 'how to do the task.' It's learning a policy conditioned on
  the context distribution that scaffold produces."
- **More evidence from the vault:**
  - LangChain went from 52.8% to 66.5% on Terminal Bench 2.0 (Top 30 to
    Top 5) with GPT-5.2-Codex fixed, by changing only the harness. From
    [[Improving Deep Agents With Harness Engineering]] (confirmed 10/16).
  - Two leads in [[2026-09-07 - harness matters]] *(Chris)*: a talk where
    a team's custom harness beat the platform harness (**work, keep out
    of VO**), and "Astra arc agi 99.9 was the harness" (**verified 10/16**
    on ARC Prize's results; the best hook).
  - **Counterweight:** [Harness or Model?](https://arxiv.org/pdf/2609.11987)
    found no average difference between vendor-native and neutral
    harnesses on frontier models. The episode has to address it.
    His open questions there are the episode's questions: "how or why?
    … What are they changing in the harness? Can we do this for our own
    harness?"
- **Sources:** Lewis, [Same Model, Different Harness](https://arxiv.org/abs/2608.26218)
  (Aug 2026; read: abstract) · [Stop Comparing LLM Agents Without
  Disclosing the Harness](https://arxiv.org/abs/2605.23950) (read: search) ·
  [Harness or Model?](https://arxiv.org/pdf/2609.11987) (read: search).
- **Key points:** `ep02-same-model-different-harness/key-points.md`. All
  three papers were read in full. **Avoid:** the "46% vs 80%" Cursor
  figure that circulates on blogs. It is secondhand.

---

## Act 2. Build yours

### 3. Harness 101: build your own

- **Question:** How do I set up my repo so a coding agent does good work
  in it?
- **Answer:** Three parts, as Böckeler's February memo grouped OpenAI's
  write-up. (Her current article, 2 Apr 2026, at the same URL, reframes
  them as guides and sensors.)
  a knowledge base the agent reads and keeps current, constraints it
  can't argue with (linters, structural tests), and garbage collection
  (agents that find drift and clean it up). When the agent struggles,
  ask what was missing, and have the agent write the fix into the repo.
- **Search phrase:** AGENTS.md best practices / how to set up a coding
  agent (guess)
- **Chris's own words:**
  - "Have good primitives and then let the agents do things. Like having
    a repo knowledge base or context base." From
    [[2026-06-02 - Good Primitives]] *(Chris)*. This is the one-line
    answer.
  - "Context is stored. Intent is all you review and discuss with the
    agent. Not the code." From
    [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]], 6/11
    *(Chris; it's a repo design at work, so generalize it)*.
  - "Everything is a file … small tools chained together - making lots of
    CLIs - specific to your use case, then it's easier for agent to do
    stuff." From [[2026-01-21 - Unix philosophy - cli for agents]] *(Chris)*.
  - The orchestration layer is "just notes. You can open a plan and
    reorder steps, edit a task prompt, correct agent memory." From
    [[2026-03-03 - OS for humans and agents - files are the layer]].
    **Not his words** (Chris, 10/16): it's a pasted AI reply. Use the
    idea only, never as VO.
- **Worked examples:**
  - This repo: `AGENTS.md`, the runbook, the update pass, and
    `agents/changelog.md` are a harness that improves after every Short.
  - OpenAugi: lenses, the janitor, and "rule files state the current
    state only". See [[What Works - Running a Second Brain With Agents]]
    *(Augi, his quotes)*.
  - His Feb Substack post *How I run AI agents from my Obsidian*
    (bitsofchris.com/p/how-i-run-ai-agents-from-my-obsidian, linked from
    [[2026-02-21 - AE3 - Issue 3]]).
  - Stripe gives its agents "the same context and tooling as human
    engineers, not a bolted-on, afterthought integration": 400+ internal
    tools via MCP, in sandboxed devboxes. From
    [[The Emerging Harness Engineering Playbook]] *(Readwise)*.
- **KB Short D, "The same four layers in any repo," is tried inside this
  episode** (Chris, 10/13). Its question ("What should go in AGENTS.md?")
  is close to this episode's. Draft ep 3's script with D's material in it,
  and decide at script time what stays. D's notes so far, from the plan:
  "Merging these into a portable system for any project, repo, etc." (10/3)
  and "Entrypoint in private-manim is now the AGENTS.md. Turned it into a
  self-improving repo." (PMOC, 10/3). Both are from
  [[PMOC - Shorts Augi Shorts - Augi content system]] and [[2026-10-03]].
- **The KB Shorts (3a–3c) are this episode's knowledge-base part, drawn
  on the building set.** Scripts and status live in
  `agents/plans/agentic-kb-shorts.md`:
  - **3a. The four layers an LLM wiki needs.** Script agreed 10/11,
    pending a read-aloud. It's the first one to record. Source:
    [[2026-10-02 - 4 rules for agentic knowledge bases]] *(Chris)*.
  - **3b. Your system needs a janitor.** It needs the queue story in his
    words. Also uses [[What Works - Running a Second Brain With Agents]].
  - **3c. Let your agent write notes you never read.** It needs one
    sentence on how this fits the 9/13 "visible seam" rule. A useful
    tension is "Not agent memory, human memory. I want my agents dumb and
    single purpose." From
    [[PMOC - Audacity to take Action - Season 2 - Q2 2026]] (4/5) and
    [[2026-04-02 - The Human Context Layer]] *(Chris)*.
- **Background reading for the written companion:**
  [[Auto Knowledge Base - Canonical Formula and 5-System Comparison]]
  *(Augi)*: LLM Wiki, OpenAugi, gbrain, knowledge-agent. The split
  between pre-synthesizing pages and routing an agent to raw data is a
  good beat. Also [[AutoWiki]] *(Chris)*: "LLM Wiki that recursively self
  improves through knowledge agents."
- **Key points:** `ep03-harness-101/key-points.md`. Short D's material is
  point 6, marked "[From Short D]".
- **Sources:** OpenAI post (Lopopolo, 11 Feb 2026) · Böckeler (Feb memo,
  and the 2 Apr rewrite) · Guo (22 Feb 2026) · Hashimoto, *My AI Adoption
  Journey* (5 Feb 2026).

### 4. Give your agent a map (context engineering is index design) — New 10/13

- **Question:** Why does my agent waste its context searching, and what
  do I give it instead?
- **Answer:** Agents explore. They don't know what to search for yet.
  Give them an index to read before they touch raw data: short summaries
  that say what's where, linked so they can drill down. Context
  engineering is data engineering where the consumer is an agent.
- **Search phrase:** context engineering (guess; it might fit here better
  than ep 5)
- **Chris's own words (published):**
  - [[Post - Context Engineering is Index Design for Agents]] *(Chris,
    shipped 3/28)*: "Today agents are using a magnifying glass to search
    through a warehouse … Agents need a map." "RAG assumes you know what
    to search for. Agents exploring a new problem don't." It also has
    four layers: data blocks, context blocks, the context graph, and
    snapshots.
  - "context engineering is index design for agents - build the index
    that is the first place an agent will look." From
    [[Data for Agentic Retrieval]] *(Chris, 3/27)*. The same note has
    "progressive disclosure … oh yea, news papers, libraries, books,
    parquet footers, Iceberg."
  - "SaaS companies survive by becoming context engineering harnesses."
    From [[2026-02-24 - Context engineering is the edge, open augi privacy story]]
    *(Claude TLDR of his voice note)*.
- **Hook image:** a magnifying glass in a warehouse, then a map on the
  wall. It sits in the pipes image as the pipe that decides what flows in.
- **Also in this episode:** LangChain's "context engineering on behalf of
  agents": onboard the model with directory structure, tools, and
  strategies to "reduce the error surface for poor search" (ep 1 source).
  Anthropic's *Effective context engineering for AI agents* (29 Sep 2025)
  uses **context rot**, credited to Chroma's 2025 report (cited in
  [[Data for Agentic Retrieval]]). OpenAI's post has a section, "give
  Codex a map, not a 1,000-page instruction manual". It's the strongest
  outside confirmation of his thesis.
- **Key points:** `ep04-give-your-agent-a-map/key-points.md`. The essay is
  the written companion as is. Erratum to consider: it says HippoRAG is
  "10–20x cheaper" (the paper says 10–30x), and its 82.5% vs 73.3%
  figure doesn't match the cited paper's table.

### 5. Context as a playbook (ACE)

- **Question:** How do I keep my agent's context file from rotting?
- **Answer:** Treat it as a playbook that grows by small, itemized
  edits: one role does the work, one reflects on what went right or
  wrong, and one curates the lessons in. Don't rewrite the whole file.
  Rewriting causes *brevity bias* (insight squeezed out for concision)
  and *context collapse* (detail lost over repeated rewrites).
- **Search phrase:** context engineering / AGENTS.md (guess)
- **Numbers:** +10.6 points on agent benchmarks and +8.6 on finance over
  the paper's baselines. It roughly matched the top production agent on
  AppWorld (59.4% vs 60.3%) with open-weights DeepSeek-V3.1. Learning
  without labels worked on AppWorld but not on finance.
- **Chris's own words:**
  - "Prompts that evolve, tailoring to use case." From
    [[2025-03-12 - Augi defensible edge open core]] *(Chris, 3/13/2025,
    about seven months before ACE; don't lean on priority)*.
  - Böckeler's line "always by having Codex itself write the fix," with
    his margin note: "compounding teams, tool helping tool get better."
    From [[Harness Engineering]] *(Readwise)*.
- **Worked example:** OpenAugi's janitor and this repo's update pass solve
  ACE's problem by hand: one home per rule, small edits only, a changelog
  line per change, and a human ticks before anything is fixed. (They do
  edit single rules in place.)
- **Key points:** `ep05-context-as-a-playbook/key-points.md`. ACE was read
  in full, with its code. A "delta" is a set of new labeled bullets; dedupe
  is by embedding similarity.
- **Sources:** Zhang et al., [Agentic Context Engineering: Evolving
  Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618)
  (ICLR 2026; read: abstract).
- **Learn first:** read the method section. What exactly is a "delta"
  entry, and how does the curator merge and dedupe? Then compare it with
  how this repo's update pass and OpenAugi's janitor handle the same
  problem.

### 6. Skills: procedures the agent can load

- **Question:** What are agent skills, and why do they help?
- **Answer (draft):** a skill is a saved procedure, the steps that
  worked last time, which the agent loads only when the task calls for
  it. It is procedural memory kept outside the weights. The best ones
  are written by the agent the moment it learns how.
- **Search phrase:** claude skills / agent skills explained (guess)
- **Chris's own words:**
  - "Are claude skills a way to do this?" (small composable tools). From
    [[2026-01-21 - Unix philosophy - cli for agents]] *(Chris)*.
  - "The Unix hive mind - skill files the right idea. Composable and
    reusable that's how it scales to hive mind." From [[2026-02-10]]
    *(Chris, #ae3/idea)*.
- **The ladder (best framing found):** "Prompts expire. Loops run.
  Skills compound." Prompting means the human is the loop. With loops,
  the human designs the loop. With skills, the loop calls tested,
  reusable capability: "tacit knowledge made explicit." From Extended_Brain,
  as distilled in [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]]
  *(Chris's reading notes)*.
- **Worked example: AugiCraft (the demo).** The Minecraft agents are
  allowed to write their own tools when blocked. They implement the
  smallest reusable action, test it, try it live once, and "record the
  result and reusable procedure" in the knowledge base
  (`~/repos/augi-craft/docs/CAPABILITY_DEVELOPMENT.md`). On 10/12 they
  wrote skills for doors, climbing and fighting mobs. Only the door skill
  (and livestock hunting) is validated; climbing is still a candidate. See
  [[2026-10-11 - LLM Plays Minecraft - AugiCraft]] *(Chris's 10/12
  journal)*. Also LangChain turned its trace analysis into a skill (ep 1
  source). Chris's `claude-skills-private` repo is the everyday version.
- **The finding (10/16):** SkillsBench (arXiv 2602.12670): skills an agent
  writes *before* doing the task scored below no skills (Claude Code +
  Opus 4.7: −8.1 points). Expert-written skills added about 16.6. Write
  skills after a success, from the trace, and keep one only after it
  works again. AugiCraft's door skill is that case.
- **Key points:** `ep06-skills/key-points.md`.
- **Sources:** [MemSkill](https://arxiv.org/abs/2602.02474) (no venue
  listed; read: in part) · [A Comprehensive Survey on Agent Skills](https://arxiv.org/pdf/2605.07358)
  (read: search) · [SkillForge](https://arxiv.org/pdf/2604.08618) (read:
  search) · "Agent Skills from the Perspective of Procedural Memory"
  (TechRxiv, Jan 2026; read: search).
- **Learn first:** this episode is no longer thin, because AugiCraft is
  the hook ("my Minecraft bot wrote its own door-opening skill"). Read
  the survey and the Anthropic Agent Skills docs, then decide the one
  thing a Claude Code user doesn't already know.

### 7. The check is the pipe that matters — New 10/13

- **Question:** What's the highest-leverage part of an agent setup?
- **Answer (draft):** the verifier: the test, the eval, the benchmark
  contract. Tasks get solved in proportion to how cheap they are to
  check. A loop with a vague objective circles. A loop with a precise
  one compounds. Whoever owns the check owns the loop.
- **Search phrase:** evals for ai agents / verifier's law (guess)
- **Chris's own words:** [[2026-09-06 - Post Training, Loss functions, verifiable]]
  *(Chris)*:
  - "Tasks get solved in proportion to how cheap they are to verify."
    This is his paraphrase of Jason Wei's verifier's law ("Asymmetry of
    verification and verifier's law", jasonwei.net, 15 Jul 2025). Credit
    Wei.
  - "The common skill across all three is building the verifier: the
    eval, the test, the label set. Whoever owns that owns the loop."
  - The ladder: code and math, then extraction and classification, then
    agentic tasks with a checkable end state, then open-ended writing.
- **His receipt:** [[2026-06-11 - PVC at work retrospective]] *(Augi,
  distilled from his agent's retro; work, generalized)*. A data-loading
  agent with the vague objective "faster with less memory" kept circling.
  His published wording, for VO: "The loop only started compounding once
  I wrote an experiment contract…" (from *The Anatomy of a Self-Improving
  Loop*, bitsofchris.com, 14 Jun 2026). And the twist: **visibility can lie.**
  Once memory was attributed properly, the verdict flipped. His own
  ingredients, from [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]]:
  "Good visibility … Clear objective to improve against … Context and
  lessons distilled as you go … Space to reflect and step back".
- **More:** "Models are biased towards their first plausible solution.
  Prompt them aggressively to verify their work." From
  [[Improving Deep Agents With Harness Engineering]] *(Readwise)*.
  LangChain's Better-Harness work treats evals as training data: holdout
  sets, one change per iteration, and a human review gate ("agents are
  famous cheaters"). As distilled in
  [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]]. From
  2025: [[Post - augmented engineering 101]] *(Chris)*: "validation loop to
  be fast - CC can self correct when you tell it how."
- **Bridge to Act 3:** once the check exists, the agent can use it to
  improve its own harness (ep 8).
- **Key points:** `ep07-the-check/key-points.md`. The companion already
  exists: his 14 Jun post. Better-Harness is confirmed (Trivedy, LangChain,
  8 Apr 2026). Strip the work specifics before using the PVC story.

---

## Act 3. The frontier

### 8. A harness that improves itself (AHE), and why less harness wins

- **Question:** Can an agent improve its own harness?
- **Answer:** Yes, if every part of the harness is a file it can edit
  and every edit makes a falsifiable prediction. Agentic Harness
  Engineering exposes each component as a file, distills traces into an
  evidence corpus, and pairs each edit with the fixes and regressions it
  predicts. Next round, it reverts edits whose predictions failed. Ten
  rounds took Terminal-Bench 2 pass@1 from 69.7% to 77.0%, past the
  hand-built Codex CLI harness (71.9%), and the evolved harness carried
  over to other models.
- **The twist (likely the hook):** the gains came from tools,
  middleware, and long-term memory. 79 lines of system-prompt discipline,
  added *alone* to the bare seed harness, cost 2.3 points (67.4% vs
  69.7%). Keep "alone" in the VO. A prompt edit was part of a winning
  round, so don't say "prompts hurt".
- **Search phrase:** self-improving agent (guess)
- **How to use it:** the TL;DR for a viewer. Keep your harness in files,
  keep traces, make each change with a stated expectation, and revert
  what doesn't pay off. This repo's update pass is the manual version.
- **Chris's own words (published):**
  *The Anatomy of a Self-Improving Loop* (bitsofchris.com, published
  14 Jun 2026; draft in
  [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]]). Its four
  ingredients as published: "visibility, an objective that fights back,
  lessons that persist, and space to step outside the loop". Its evidence: Recursive's evaluator arms race, evo's "a
  small loop watching and editing a big loop" (coordination as code,
  because instruction adherence decays over long contexts), and Darwin
  Gödel Machine's archive ("greedy circles, archives spiral").
  "We want loops and improvement not optimization. Optimization can lead
  to reward hacking." From
  [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]] *(Chris)*.
  Related: [[RSI for Humans - Recursive Self Improvement]] (Backlog, the
  human version).
- **The "less harness" beat (merged in 10/13).** It expands the twist:
  more harness isn't better. Models are post-trained inside coding
  harnesses, so they already know what one is, and every line of prompt
  and every tool is something the model can misuse.
  - Mario Zechner built Pi, a coding agent with four tools: "You don't
    need 10,000 Tokens to tell them you're a coding agent." Terminal
    Bench's own baseline harness is "the most minimal kind of thing you
    can think of": one tool that sends keystrokes to tmux. His agent
    modifies itself by writing extensions when asked. There's no eval
    loop, so it isn't AHE. His claim that Terminus beats native harnesses
    is contradicted for GPT-5.4 by AHE's own table (62.9% vs 71.9%). From
    [[Building Pi in a World of Slop — Mario Zechner]] *(Readwise)*.
  - "increasing trust and reliability in AI-generated code requires
    constraining the solution space rather than expanding it". This is
    Böckeler's point, quoted in
    [[The Emerging Harness Engineering Playbook]] *(Readwise)*.
  - Chris: [[2026-04-30 - Pi harness modular and simple agents]]
    *(Chris)*: "keeping things simple building what you need … Modular
    and easy to use". It links his
    [[Weakness - overoptimizing, systems too soon, just play]] and
    [[2026-04-29 - Kill your darlings, yangni not going to need it]]. From
    [[What Works - Running a Second Brain With Agents]]: "Keep it simple
    to get mvp out asap and using it - let water flow through the hose."
  - Image: the pipe maze gets *simpler*, and the output gets sharper.
- **Key points:** `ep08-self-improving-harness/key-points.md`. The
  concrete edits are confirmed. The evolved harness carried over +5.1 to
  +10.1 points on three other model families. "Codex 71.9%" is the
  paper's own run, not a leaderboard number.
- **Sources:** Lin et al., [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850)
  (Apr 2026; read: full; code public, MIT) · Zechner, "Building pi in a
  World of Slop" (AI Engineer Europe 2026) and his blog post "What I
  learned building an opinionated and minimal coding agent".

### 9. Agents that share a notebook (GitSwarm) — New 10/13

- **Question:** What happens when many agents build on one shared record
  instead of starting fresh?
- **Answer (draft):** the work compounds. GitSwarm's agents share a
  branchable git repo, and every result persists so later agents can
  extend, combine, or challenge it. On ProgramBench, 94.7% of
  contributions get built on later, and the winning solution's ancestry
  covers 82–93% of the work (on proofs: 44.4% and 21–33%). The knowledge
  base *is* the harness, for a team of agents.
- **Search phrase:** multi-agent / agent swarm (guess)
- **Numbers:** all 30 IMOProofBench-Advanced problems solved in one run
  (Codex GPT-5.5-High), though oracle Best-of-N also reaches 30/30.
  ProgramBench 79.4% mean vs 65.1% for one re-prompted Codex agent on a
  50-task subset. It improved on the starting architectures in all three
  neural-architecture tasks.
- **Key points:** `ep09-agents-share-a-notebook/key-points.md`. The
  AugiCraft receipt: a new worker found Augi's validated door skill in the
  shared notes nearly four hours later, and used it to retreat from
  pillagers.
- **Chris's own words and demo:**
  - The 10/11 capture [[2026-10-11 - GitSwarm and self improving agents with knowledge bases]]
    *(Chris)*, plus a GPT thread on it that isn't in the vault yet.
  - AugiCraft 10/12: "spawned an army of 4 agents to join us with deeper
    roles … gave each their own jobs." The bots write
    `knowledge/episodes/` that the next bot reads. From
    [[2026-10-11 - LLM Plays Minecraft - AugiCraft]] *(Chris)*.
  - "one meta agent or orchestrator that can kick off tasks and
    selectively fetch context from other agents." From
    [[2026-01-26 - Human Agent Workflows]] *(Chris)*.
  - [[MOC - System of AI agents - Army of Agents]] *(Chris)*: his list of
    what to learn ("Orchestration frameworks, eval / feedback loops,
    self-improving agents …").
- **Sources:** Shah et al., [GitSwarm: Decentralized Compounding
  Inference](https://arxiv.org/abs/2610.04862) (Oct 2026; Goyal, Weston,
  Arora, Fergus et al.; Meta Superintelligence Labs and others; read:
  full).
- **Learn first:** read the paper. How do agents pick what to build on,
  and what do the dependency records look like? Compare it with
  AugiCraft's episode notes and with OpenAugi's task files.

### 10. Harness instead of RL? And the human in the harness (series close)

- **Question:** Can you get RL-level gains without training?
- **Answer (draft):** sometimes. GEPA evolves prompts by reflecting in
  language on its own trajectories. Across six tasks it beats GRPO by 6
  points on average (up to 19), winning five of the six (GRPO wins AIME),
  with up to 35x fewer rollouts. GRPO was run on Qwen3 8B only. Older posts
  quote 10%, from the v1 abstract. Language
  is a richer signal than one scalar reward. The counter-argument:
  context-held memory is "a memo, not true memory," because it never
  consolidates into the weights. And RL done inside one scaffold ties
  the model to that scaffold (ep 2).
- **Search phrase:** prompt optimization vs reinforcement learning (guess)
- **The spine, in Chris's words:** [[2026-09-06 - Post Training, Loss functions, verifiable]]
  *(Chris)*:
  - "Model - the weights, train when need better judgement on the thing.
    Agents - the loop around the weights, train this when compositional
    solution or long horizon."
  - Software 2.0 vs 3.0. **Not his words** (Chris, 10/16): "They're not
    successive; they're a tradeoff…" is a pasted AI reply. Use the idea
    only, never as VO.
    3.0 when the task is general and a frontier model already does it,
    2.0 when you need cheap, fast, private, or the task is off the
    frontier model's distribution."
  - "Prompt a big model first - establish a baseline, then distill."
  - "Nothing you intend matters, only what the gradient rewards." (Why
    RL needs the verifier from ep 7.)
- **The turn:** Chris's AugiCraft idea (10/12): "now that we learned all
  this can I train a Jev like thing to pick next action? So the big model
  trains or writes the action rules and tools then the small classifier
  just decides what to do and how to use it?" The harness teaches, and
  the weights learn. This is the "prompt a big model, then distill" line
  made concrete, and it's where the series hands off to his
  research-engineer track ([[AMOC - AI Research Engineer]]). Jev
  background: [[Language Models for Text Classification From Bag-of-Words to Jev]].
- **The last beat: the human in the harness (merged in 10/13).** If the
  agent improves its harness and the weights learn from it, what's left
  for you is the reframes and the taste. In Chris's own loop, every big
  pivot came from him. The part you can't automate is reading the raw
  traces yourself, which is where your opinion forms and where the
  objective stays honest. The same loop that makes you faster on work you
  understand lets you stop understanding it ("comprehension debt").
  - The PVC retro: "Human steering drove every architecture pivot." From
    [[2026-06-11 - PVC at work retrospective]] (an **Augi-written** note,
    so it isn't his VO; use his published post's wording).
  - The 6/12 draft's kicker on comprehension debt, and the Langfuse
    point: "Keep manual: reading raw traces yourself." From
    [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]].
  - "we have our 'capable interns' they don't tire so let them run in
    loops and just nudge them when stuck." From the same draft.
  - Augment, stay human: [[2026-09-19 - Agents in my second brain video update]]
    *(Chris)*, and Guo's "moving away from chatting with AIs and moving
    towards managing them" (ep 1 source).
  - It overlaps with [[Post - augmented engineering 101]] and
    [[Post Seed - Automate the Shallows, Protect the Deep Layer]]. Those
    are about where *the human's* effort goes. Link to them; don't absorb
    them.
- **Also:** [[2026-06-12 - Engram and token memory for models]] *(Chris)*,
  on memory that lives in the model, for the "memo, not memory" beat.
- **Sources:** Agrawal et al., [GEPA: Reflective Prompt Evolution Can
  Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457)
  (ICLR 2026 oral; read: search) · [Contextual Agentic Memory is a Memo,
  Not True Memory](https://arxiv.org/abs/2604.27707) (position paper;
  read: search).
- **Key points:** `ep10-harness-instead-of-rl/key-points.md` (needs a
  long cut; the Short core is points 1–4). GEPA and the Memo paper were
  read in full. The AugiCraft distillation hasn't been run, so the script
  presents it as a plan.

---

## Recording plan (agreed 10/13)

Series order, audio first. For each episode in turn: do its "learn first"
step, agree the whole script, and record it as audio. Then the visuals
are built (runbook from step 3). The KB Shorts 3a–3c go in at their
place after ep 3. 3a's script is already agreed, so it only needs the
read-aloud.

## Open decisions (Chris)

1. **Format.** One question per 45–60 s Short fits episodes 1, 2, 3a–3c,
   4, 7 and 8. Episodes 3, 5, 9 and 10 carry more than a minute holds.
   Options: a Short plus a written companion per episode (the linear
   algebra series ships YT and Substack; eps 4 and 8 already have
   published companions), or a longer 16:9 piece for eps 9–10. Decide per
   episode at script time, once the script's length is known.
2. **What stays from KB Short D in ep 3.** Decide at script time.

## Checklist

In recording order. "Key points" means researched against the primary
sources (10/16). "Scripted" means its VO is in `SCRIPTS.md`, ready to
record.

| # | Folder | Working title | State |
|---|---|---|---|
| 1 | `ep01-what-is-a-harness/` | What is an agent harness? | scripted · key points (Short) |
| 2 | `ep02-same-model-different-harness/` | Same model, different harness | scripted · key points (Short + companion); Astra hook verified |
| 3 | `ep03-harness-101/` | Harness 101: build your own (tries KB Short D) | scripted · key points (Short + companion) |
| 3a | (plan: `agents/plans/agentic-kb-shorts.md`) | The four layers an LLM wiki needs | scripted (agreed), pending read-aloud |
| 3b | (plan) | Your system needs a janitor | scripted, needs one line in your words |
| 3c | (plan) | Let your agent write notes you never read | scripted, needs one line in your words |
| 4 | `ep04-give-your-agent-a-map/` | Give your agent a map | scripted · key points (Short); essay is the companion |
| 5 | `ep05-context-as-a-playbook/` | Context as a playbook (ACE) | scripted · key points (Short + companion) |
| 6 | `ep06-skills/` | Skills | scripted · key points (Short + companion); SkillsBench hook |
| 7 | `ep07-the-check/` | The check is the pipe that matters | scripted · key points (Short); 6/14 post is the companion |
| 8 | `ep08-self-improving-harness/` | A harness that improves itself (+ less harness) | scripted · key points (Short + companion) |
| 9 | `ep09-agents-share-a-notebook/` | Agents that share a notebook (GitSwarm) | scripted · key points (Short + companion) |
| 10 | `ep10-harness-instead-of-rl/` | Harness instead of RL? (+ the human in the harness) | scripted · key points (needs a long cut) |
