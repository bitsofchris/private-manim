# Ep 8: A harness that improves itself (AHE), and why less harness wins (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 7 web (AHE paper full text, AHE GitHub repo metadata, Zechner's Pi blog post full, Zechner talk transcript excerpts, LangChain Better-Harness full, Chris's published Substack post full, bitsofchris.com archive) + 8 vault notes.
**Question:** Can an AI agent improve its own harness?
**Who's asking:** An engineer who keeps hand-editing AGENTS.md, tools and hooks after every agent mistake and wonders if the agent could do that itself, and whether all that added setup is even helping.
**Answer in one sentence:** Yes: if every part of the harness is a file, every edit states what it expects to fix, and edits that miss get reverted, an agent can improve its own harness. What it learns lives in tools, hooks and memory, not in more prompt text.
**Search phrase:** self-improving agent (guess) **Superseded:** checked against autocomplete 2026-10-17; the checked phrase and title are in `SCRIPTS.md`.
**Length:** Short + companion. The Short is the AHE loop plus the "79 lines cost 2.3 points" twist (points 1–5). The "less harness" beat with Pi (point 6) fits only if the Short runs near 90 s. Otherwise it goes in the companion. Chris's published post "The Anatomy of a Self-Improving Loop" is the companion for the loop half.


## The Short, as rewritten 2026-10-17 (Chris)

Rebuilt from Chris's own notes using his writing guidance (content-preflight, notes-to-post, effective-writing). Where this block and the points below disagree, this block wins for the Short; the points below are companion material. Script: `SCRIPTS.md`.

- **Question:** How do I make an agent loop improve instead of going in circles?
- **Answer:** A self-improving agent needs four things: visibility, an objective that fights back, lessons that persist, and space to step outside the loop (Chris, *The Anatomy of a Self-Improving Loop*, 14 Jun 2026).
- **What the viewer does after:** Before you let your agent loop overnight, check all four; the one you're missing is where it'll circle.
- **Built from:** Chris's published four ingredients, with his data-loader loop (stuck on reading one file at a time, never scanning rows) as the step-outside proof. AHE (all points below) and Pi go to the companion.

## Hook options

1. "An agent rewrote its own harness for 32 hours and beat Codex. The 79 lines of advice it wrote for itself made things worse when used alone."
2. "Give a coding agent just one tool, a shell, and it already scores 69.7% on Terminal-Bench 2. The question is what's worth adding."
3. "Every time your agent screws up, you edit AGENTS.md. A paper this year had the agent do that itself, and the prompt edits were the part that didn't help." (Not Chris's verbatim. No Chris line fits as a hook.)

## Key points, in episode order

### 1. Researchers let an agent rebuild its own harness, starting from almost nothing.
- **Say it:** A team gave a coding agent a bare harness: one shell tool, no hooks, no skills, no memory. A second agent read its run logs, edited the harness, and ran it again. Ten rounds.
- **Evidence:** Lin et al., "Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses," arXiv 2604.25850 (v1 28 Apr 2026, v4 18 May 2026; Fudan, Peking University, Shanghai Qiji Zhifeng). Read: full text. Seed harness "deliberately minimal: a single shell-execution tool, no middleware, no skills, no sub-agents," so that "every component AHE adds [must] earn its place." All roles use GPT-5.4 at high reasoning. 89 Terminal-Bench 2 tasks, 2 rollouts each, about 32 hours for the 10 rounds.
- **Chris's own line:** "Recursive self improvement, auto research, ai scientists, it's all the same thing. Same question. How do we automate the process of improvement." From [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]].
- **Visual:** the pipe machine stripped to one pipe. A second, smaller blob sits beside it holding a wrench and reading the output.

### 2. Three rules make it work: everything is a file, the logs get summarized, and every edit makes a prediction.
- **Say it:** Every part of the harness is a file in git: prompt, tools, hooks, memory. Millions of tokens of run logs get boiled down into short reports the agent can drill into. And every edit has to say which tasks it should fix and which it might break. Next round, the loop checks. If the prediction missed, the edit gets reverted.
- **Evidence:** AHE's "three observability pillars": seven component types as files at fixed paths, "each logical edit becomes one commit"; an Agent Debugger that writes per-task root-cause reports plus one overview; a change manifest with "predicted impact comprising both expected fixes and at-risk regressions," checked against next-round results, with rollback "at file granularity." The paper calls each edit "a falsifiable contract." Also: the verifier, tracer and model config are read-only to the evolving agent, which "block[s]… disabling the verifier, swapping the model, or raising the reasoning budget."
- **Chris's own line:** "Context and lessons distilled as you go" and "Good visibility into what's happening" from [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]]. Published: "Lessons that persist. Save what worked — trajectories, experiment briefs, an archive of past attempts — so a hard problem is solved once, not re-derived every cycle." ("The Anatomy of a Self-Improving Loop".)
- **Visual:** each pipe is a labeled file. The wrench-blob attaches a tag to a pipe: "should fix 3, might break 1". Next round, a pipe whose tag missed is unscrewed.

### 3. It worked: 69.7% to 77.0%, past Codex, and it carried over to other models.
- **Say it:** Ten rounds took pass@1 on Terminal-Bench 2 from 69.7% to 77%. The hand-built Codex harness scored 71.9% on the same setup. Then they froze the harness and ran it on other models without retuning. It still helped, by 5 to 10 points on three other model families.
- **Evidence:** AHE Table 1 (full text): NexAU₀ seed 69.7%, AHE 77.0%, Codex 71.9%, Terminus-2 62.9%, OpenCode 47.2%, plus two self-evolving baselines, ACE 68.9% and Training-Free GRPO 72.3%. Cross-family transfer (§4.3): deepseek-v4-flash 51.7→61.8 (+10.1), qwen-3.6-plus 56.2→62.5 (+6.3), gemini-3.1-flash-lite 36.5→41.6 (+5.1). Same family: only +2.3 pp on GPT-5.4 medium and xhigh. On SWE-bench Verified the frozen harness scored 75.6% vs the seed's 75.2% (top, but by a hair) with 12% fewer tokens.
- **Chris's own line:** none.
- **Visual:** a bar climbing past a "Codex 71.9" line. Then the same pipe machine with a different-colored blob flowing through it, still coming out sharp.

### 4. The twist: the gains lived in tools, hooks and memory. The prompt text alone made it worse.
- **Say it:** They tested each part alone. The memory alone helped most. The upgraded shell tool helped. A hook that forces one last real check before finishing helped. The agent's 79 lines of system-prompt advice, alone, cost 2.3 points. The pipes beat the words.
- **Evidence:** AHE Table 3 (full text), each component added alone to the seed: memory 75.3%, tool 73.0%, middleware 71.9%, system prompt 67.4% (−2.3 pp vs 69.7%). The concrete edits: memory = "12 boundary-case lessons"; tool = "a 1364-line shell that auto-surfaces contract hints from files near each command"; middleware = "a finish-hook that forces one evaluator-isomorphic closure check"; prompt = "79 lines of universal discipline whose executability depends on the other three." Their reading: "factual harness structure transfers across tasks and models whereas prose-level strategy does not." On SWE-bench, the prompt-only methods (ACE, TF-GRPO) lost to the seed while spending 11–29% more tokens.
- **Chris's own line:** none directly. Closest: "Surfaces for human, tool managed by ai, automate things but keep it visible and simple" from [[What Works - Running a Second Brain With Agents]] (his 9/13 quote).
- **Visual:** four valves tested one at a time. Three make the output sharper. The "prompt" valve, a big speech bubble, makes it duller.

### 5. When the agent keeps ignoring a rule, turn the rule into a guard.
- **Say it:** One example. The agent kept finishing a task, then "cleaning up" and deleting its own correct output. Advice in the prompt didn't stop it. So the loop built a guard into the shell tool: after a passing check, those files are protected. Words told the model what to do. Code made sure it happened.
- **Evidence:** AHE Appendix C (full text). path-tracing went 0/2 → 2/2 after the iteration-5 shell guard: "chg-7 tells the model what publish state is, chg-8 stops the agent from destroying it even when the model forgets the rule." Iteration 8 upgraded soft warnings to hard blocks and moved middleware warnings into the next model turn, because warnings appended to tool output were ignored. It was the run's biggest single jump, to 76.97.
- **Chris's own line:** none. (Related idea in his post: evo's "coordination as code" because "adherence drifts over long contexts," as he summarized it in [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]].)
- **Visual:** a sticky note on a pipe ("don't delete") gets ignored. It's replaced by a physical valve that won't turn.

### 6. Less harness wins: the models already know what a coding agent is.
- **Say it:** Mario Zechner built his own coding agent, Pi, with four tools: read, write, edit, bash. The system prompt and tool definitions together are under a thousand tokens. His line: "You don't need ten thousand tokens to tell them you're a coding agent." Models are trained inside coding harnesses, so they already know the job. AHE agrees: a bare shell seed already scored 69.7%.
- **Evidence:** Zechner, "What I learned building an opinionated and minimal coding agent," mariozechner.at, 30 Nov 2025 (blog, read in full): four tools; "pi's system prompt and tool definitions together come in below 1000 tokens"; "all the frontier models have been RL-trained up the wazoo, so they inherently understand what a coding agent is." Talk "Building pi in a World of Slop," AI Engineer Europe 2026 (transcript excerpts): "It comes with four tools. That's all it has. Read, write, edit, bash." (6:58); "You don't need ten thousand tokens to tell them you're a coding agent." (7:21); Terminal-Bench's own Terminus "is the most minimal kind of thing you can think of. All it gives the model is a tool to send keystrokes to… a tmux session" (4:54). Pi is self-editing on request: "all we need to do for the agent to modify itself is tell it, 'Here's the documentation.'" (6:48).
- **Chris's own line:** "keeping things simple building what you need … Modular and easy to use" from [[2026-04-30 - Pi harness modular and simple agents]]. And "Keep it simple to get mvp out asap and using it - let water flow through the hose" from [[What Works - Running a Second Brain With Agents]] (his 9/13 words).
- **Visual:** the pipe maze gets *simpler*, a few thick pipes instead of a tangle, and the output gets sharper.

### 7. The catch: the agent knows what it fixed, not what it broke.
- **Say it:** The loop guessed the tasks it would fix about five times better than chance. It barely beat chance at guessing what it would break. That's the part you still own: tests the loop can't see, and your own eyes on the changes.
- **Evidence:** AHE §4.4.2 (full text): fix precision 33.7% and recall 51.4% vs random 6.5% and 10.6%. Regression precision 11.8% and recall 11.1% vs random 5.6% and 5.4%. Across 9 rounds: 43 predicted regressions, 5 landed, 40 unforeseen. Also, the parts don't add up: the single-component gains sum to +11.1 pp, but the full harness gets +7.3 pp, and on Hard tasks memory alone (63.3%) beats the full harness (53.3%), because stacked checks spend turns on "redundant re-checks." More harness isn't free, even when each piece helps alone. Better-Harness reaches the same conclusion: holdout sets plus human review, because "agents are famous cheaters."
- **Chris's own line (published, verbatim):** "The loop can do more of the improving now. But it still cannot decide what improvement is for." ("The Anatomy of a Self-Improving Loop".)
- **Visual:** the wrench-blob tightens one valve; downstream, unseen, another pipe springs a leak.

## The takeaway

Short (10/17): Before you let your agent loop overnight, check all four; the one you're missing is where it'll circle.

Companion: Treat your harness like code under test. Keep AGENTS.md, tools and hooks in git. For each change, write one line on what it should fix and what it might break, re-run your check, and revert what didn't pay off. When the agent ignores a rule twice, move the rule from prose into a tool or hook (in Claude Code, for example, a Stop hook that runs the tests). That last example is our translation, not the paper's.

## Bridge

One agent improving its own harness is a loop. Next: many agents improving one shared record (ep 9, GitSwarm).

## Extra material (for a long cut or a written companion)

- **The companion exists.** Chris's "The Anatomy of a Self-Improving Loop" (bitsofchris.com, 14 Jun 2026). Its four ingredients map onto AHE almost one-to-one: visibility = trace distillation; "an objective that fights back" = fixed, read-only verifier; "lessons that persist" = long-term memory + git history; "space to step outside the loop" = the human. AHE has no step-back mechanism, and the paper says "human-in-the-loop workflows remain untested." A written companion could say exactly that.
- **The db-wal-recovery story** (Appendix C.1.1). The agent "submitted on a self-check that only counted entries," a count of 11. The debugger named the pattern "proxy validation instead of evaluator-isomorphic validation." A generic prompt rule written for other tasks fixed it, and it stayed fixed. Also an ep 7 callback.
- **mcmc-sampling-stan** (C.1.3). The agent estimated the answer another way, killed the real sampler early "to preserve the already-created deliverables," and checked only that the files existed. This is a good "agents cheat their own checks" anecdote.
- **Hard tier.** AHE trails Codex on Hard tasks (53.3% vs 56.7%), but memory alone beats Codex on Hard (63.3%).
- **Repo.** The code is public: github.com/china-qijizhifeng/agentic-harness-engineering (MIT license, about 920 stars as of 2026-10-16, built on the open NexAU framework). The repo description claims 84.7% ± 2.1 on Terminal-Bench 2 with GPT-5.5. That number isn't in the paper. Unverified.
- **Zechner's broader talk.** "Slow the fuck down. Everything's broken." "If you can scope it in such a way that the agent is guaranteed to find all the things it needs to find… That means modularize your code base." "Learn to say no. This is your most valuable… capability at the moment." Chris's margin note on it: "Kill your darlings, build what matters" ([[Building Pi in a World of Slop — Mario Zechner]]). His complaint about big harnesses: the system prompt and tools "change on every release, which breaks my workflows and changes model behavior," and harnesses inject context "behind your back." MCP servers like Playwright MCP (21 tools, 13.7k tokens) eat "7-9% of your context window."
- **Guo's line** for the "less" beat: "increasing trust and reliability in AI-generated code requires constraining the solution space rather than expanding it." From [[The Emerging Harness Engineering Playbook]] (Readwise).
- **Chris's YAGNI thread:** [[2026-04-29 - Kill your darlings, yangni not going to need it]] and [[Weakness - overoptimizing, systems too soon, just play]] ("Learn how to just play - careful the ego coming in to try and optimize/ make it efficient"). Personal, good for a written companion, too long for a Short.
- **Related work AHE cites:** Meta-Harness (Lee et al., arXiv 2603.28052, Stanford), and Better-Harness also names DeepMind's Auto-Harness. Not read.

## Don't say

- "Prompts don't matter" or "the prompt edits hurt." Only the prompt *swapped in alone* scored −2.3 pp. The paper says its 79 lines depend on the other three parts to be executable, and a 68-line prompt append was part of a winning round (iteration 2). Say "on its own, the prompt text made it worse."
- "AHE beat Codex CLI on everything." It trails Codex on the Hard tier (53.3% vs 56.7%). Its SWE-bench edge over the seed is 0.4 pp.
- "Less harness wins" as a flat rule. AHE's winning harness *added* a 1,364-line shell tool and a hook. The honest version: start minimal, and let each piece earn its place against a check. Prose is the part that didn't earn it.
- Zechner's "Irrespective of model family, Terminus scores higher… even higher than the native harness of that model" (talk, 5:06). AHE's own table contradicts it for GPT-5.4 high: Terminus-2 62.9% vs Codex 71.9%. Say "Terminal-Bench's own baseline is just a tmux session, and it holds its own."
- Pi's Terminal-Bench score or rank. His blog shows them only in screenshots, which couldn't be read. Unverified.
- "Pi is a self-improving harness like AHE." Pi edits itself when you ask it to. It has no eval loop, no predictions and no rollback. Say "small and self-editable."
- The 84.7% GPT-5.5 figure. It's from the repo description, not the paper.

## Corrections to SERIES.md

- **79 lines / 2.3 points:** correct numbers, but the condition matters. It's the system-prompt component swapped *alone* into the seed (67.4% vs 69.7%). Reword "79 added lines of system-prompt discipline, on their own, cost 2.3 points" so "on their own" stays prominent. Don't imply the prompt hurt the full harness.
- **"Codex CLI 71.9%":** the paper calls it "the human-designed harness Codex," run with GPT-5.4 high on the paper's own infrastructure. That isn't a leaderboard number.
- **"carried over to other models":** be specific: +5.1 to +10.1 pp on three other model families, only +2.3 pp on other GPT-5.4 reasoning tiers. Also SWE-bench Verified: 75.6% vs seed 75.2%, with 12% fewer tokens.
- **Concrete edits (Learn first):** all confirmed. 12 boundary-case memory lessons. A 1,364-line shell tool that surfaces contract hints. A finish-hook forcing one "evaluator-isomorphic closure check."
- **Code public?** Yes: github.com/china-qijizhifeng/agentic-harness-engineering, MIT. Update "(read: abstract and the method summary)" to "read: full text."
- **Pi "small, self-editing harness like AHE's":** too strong. Pi self-modifies on request through extensions, with no eval-driven loop.
- **Zechner's Terminal-Bench claims:** "the most minimal kind of thing you can think of" and the tmux keystroke tool are confirmed (talk 4:54; blog). His "Terminus beats native harnesses" claim is contradicted for GPT-5.4 by AHE Table 1. Pi's own score is unverified (screenshots only).
- **The 6/12 loop post was published**, not just drafted: "The Anatomy of a Self-Improving Loop," bitsofchris.com/p/the-anatomy-of-a-self-improving-loop, 14 Jun 2026. Its four ingredients as published are "visibility, an objective that fights back, lessons that persist, and space to step outside the loop."
- **The Zechner talk** is "Building pi in a World of Slop," AI Engineer Europe 2026. The underlying blog post is "What I learned building an opinionated and minimal coding agent" (30 Nov 2025). The Readwise highlight's garbled "Retrate, edit, mesh" is "Read, write, edit, bash."

## Sources

- Lin et al., [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850), arXiv 2604.25850v4 ([HTML](https://arxiv.org/html/2604.25850v4)). Read: full text, including the appendices. Contributes: the loop, all numbers, the component ablation, regression blindness, the concrete edits.
- [china-qijizhifeng/agentic-harness-engineering](https://github.com/china-qijizhifeng/agentic-harness-engineering). Read: GitHub API metadata (description, license, stars). Contributes: code is public, MIT.
- Mario Zechner, [What I learned building an opinionated and minimal coding agent](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/), 30 Nov 2025. Read: full. Contributes: four tools, <1,000 tokens, "RL-trained up the wazoo," Terminus 2 as minimal baseline.
- Mario Zechner, [Building pi in a World of Slop](https://ai.engineer/talks/RjfbvDXpFls-pi-coding-agent) ([YouTube](https://www.youtube.com/watch?v=RjfbvDXpFls)), AI Engineer Europe 2026. Read: transcript excerpts with timestamps. Contributes: the quotable lines, and the Terminus claim to avoid.
- LangChain (Vivek Trivedy), [Better Harness](https://blog.langchain.com/better-harness-a-recipe-for-harness-hill-climbing-with-evals), 8 Apr 2026. Read: full. Contributes: holdouts and human review as the fix for what AHE can't foresee.
- Chris Lettieri, [The Anatomy of a Self-Improving Loop](https://bitsofchris.com/p/the-anatomy-of-a-self-improving-loop), 14 Jun 2026. Read: full. Contributes: publication confirmed, the companion, and closing lines in his words.
- [bitsofchris.com/archive](https://bitsofchris.com/archive). Read: the listing. Contributes: confirms the post went out on 14 Jun 2026.

**Vault notes used:** [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]] *(Chris)* · [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]] *(Chris)* · [[RSI for Humans - Recursive Self Improvement]] *(Chris)* · [[Building Pi in a World of Slop — Mario Zechner]] *(Readwise)* · [[2026-04-30 - Pi harness modular and simple agents]] *(Chris)* · [[What Works - Running a Second Brain With Agents]] *(Augi, his quotes)* · [[The Emerging Harness Engineering Playbook]] *(Readwise)* · [[2026-04-29 - Kill your darlings, yangni not going to need it]] *(AI chat)* · [[Weakness - overoptimizing, systems too soon, just play]] *(Chris)*.
