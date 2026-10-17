# Ep 2: Same model, different harness (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 7 (three arXiv papers in full text, the LangChain blog post, ARC Prize's Astra blog post and results page, Hashimoto for context), plus 3 vault notes.
**Question:** does the harness matter as much as the model?
**Who's asking:** an engineer choosing between "switch to the newer model" and "fix my agent setup", who sees leaderboard numbers and isn't sure what they measure.
**Answer in one sentence:** often yes, and sometimes more: the same model can score 55% or 99.9% depending on its harness. But the gap is biggest where the model is starved (tight context, long messy tasks), and it can shrink to nothing when the model already has room.
**Search phrase:** "does the harness matter more than the model" / "same model different harness" (guess) **Superseded:** checked against autocomplete 2026-10-17; the checked phrase and title are in `SCRIPTS.md`.
**Length:** Short + companion. The Short carries the hook, one mechanism, one controlled experiment, and the catch. The leaderboard evidence and the counter-study go to the companion.

## Hook options

1. "Same model. Same reasoning setting. 55% in one harness, 99.9% in another." (GPT-6 Astra on ARC-AGI-3, point 1.)
2. "Astra arc agi 99.9 was the harness" (**Chris's own sentence**, [[2026-09-07 - harness matters]]. Spoken: "Astra's 99.9 on ARC-AGI? That was the harness.")
3. "Before you switch models, look at what your agent was actually seeing when it failed." (Plain pain hook.)

## Key points, in episode order

### 1. The same model scored 55% in one harness and 99.9% in another.
- **Say it:** In September, OpenAI's GPT-6 Astra posted 99.9% on ARC-AGI-3. Under ARC Prize's own neutral harness, at the same reasoning setting, the same model scored 54.8%. Same weights, same puzzles. The only thing that changed was the harness. The high-scoring run was also cheaper.
- **Evidence:** ARC Prize, "OpenAI's GPT-6 Astra on ARC-AGI-3", 3 Sep 2026, plus the verified results page (both read via fetch). ARC-AGI-3 Semi-Private. Standard harness: high 54.8% ($40,705), max 62.7% ($26,098). Provider Adapter harness: high 99.9% ($18,817), max 98.6% ($17,332). Even with reasoning set to *none*, the adapter scored 96.7%, above the standard harness at max. The standard harness "enables a model to carry forward notes it chooses to keep with it throughout the environment." The Provider Adapter "preserves opaque reasoning state between requests and uses compaction for longer conversations". In other words, it uses the provider's own context-management features. ARC Prize: "we are not claiming that it is AGI." The results page shows 99.95% for high, and the blog 99.9%. Use "99.9".
- **Chris's own line:** "Astra arc agi 99.9 was the harness" from [[2026-09-07 - harness matters]]. **Now verified.**
- **Visual:** one blob, two pipe sets side by side. Left: a thin straight pipe, a fuzzy output, "55%". Right: the maker's own tuned pipes, a sharp output, "99.9%". The blob is identical in both: same colour, same size.

### 2. Why: the model only acts on what the harness puts in front of it.
- **Say it:** A model can't see your repo, your logs, or what it did ten steps ago. It sees one block of text, and the harness decides what's in that block. Change what's in the block and you change what the model can do. And models are post-trained inside a particular harness, so they do their best work in the one they grew up in.
- **Evidence:** Lewis (2608.26218, full text): a harness "decides what the model sees, which tools it can use, and how the work continues"; "The window is working space for the model's next decision, not the permanent archive of everything that has happened." Zhang et al. (2605.23950, full text) frame the LLM as "open-loop": "It has no direct access to [the state], only to ... the projection of state into context that the harness chooses to expose." OpenAI's harness post: "From the agent's point of view, anything it can't access in-context while running effectively doesn't exist."
- **Chris's own line:** "When you post-train (especially with RL) inside a specific scaffold, the model isn't learning 'how to do the task.' It's learning a policy conditioned on the context distribution that scaffold produces." from [[2026-09-07 - harness matters]]. Also "Managing contest the whole game." from [[2026-09-11]] (his typo for "context"; on screen, write "context").
- **Interpretation, label it as Chris's:** Astra's winning harness was the one that kept the provider's own reasoning state, which is the context distribution it was trained on. ARC Prize doesn't say why the gap exists. This is Chris's research-engineer read, so say it as "my read is".
- **Visual:** zoom into the pipe mouth where it meets the blob. Only what passes through that opening reaches the blob. The rest of the world is greyed out.

### 3. The clean experiment: one harness setting, same model, 28% to 49%.
- **Say it:** One researcher held everything fixed (model, tasks, context size, time limit) and flipped a single configuration package in her harness. The package trims old tool output as the context fills, keeping the newest results whole, and nudges the model when it's stuck repeating itself. On 169 SWE-bench Verified tasks, the share of required tests fixed went from 28% to 49%, and fully solved tasks went from 43 to 72. It helped three other models too, with no retuning.
- **Evidence:** Sydney Lewis, "Same Model, Different Harness: Different Coding-Agent Results", arXiv 2608.26218, 26 Aug 2026 (full text). Model: Qwen3.6-35B-A3B, 4-bit, served locally. Window: 20,480 tokens. Budget: 480 s per attempt. Mean per-task fail-to-pass fraction (F2PF): 28.0% → 49.1%; solutions 43 → 72 (34 tasks solved only by treatment, 5 only by control). The treatment is a package of three things: (a) a "half-life" rule that starts trimming once the prompt reaches half the window, keeps the newest four tool results in full, and cuts older ones to their beginning and end ("as age doubles ... the character cap halves"), with no model summary; (b) a stall detector that spots repeated failing commands or rereading without edits, and tells the model to try something different; (c) small command safeguards. The paper does not separate their effects. Other models on the same 169 tasks and window: Devstral 17→37% F2PF (22→53 solved), Nemotron 12→18% (16→25), Qwen3.8 20→35% (32→54). SWE-bench Pro: 15→33% F2PF, 31→72 solved out of 316.
- **Chris's own line:** his questions, which this paper answers: "how or why? ... What are they changing in the harness? Can we do this for our own harness?" from [[2026-09-07 - harness matters]].
- **Visual:** the context window as a pipe segment filling with old tool-output blocks. Control: the pipe clogs and the flow stops. Treatment: old blocks shrink to stubs (head and tail with a gap), and new ones stay full size, so the flow keeps going.

### 4. The catch: give the model a big window and the gap disappears.
- **Say it:** The 21-point jump happened in a tiny 20K-token window. At 43K the gain was about 6 points. At 262K, effectively unlimited, it was zero. So the harness matters most when the model is squeezed: long tasks, big logs, small windows. Part of the win is simply that the control ran out of room and stopped, while the treated agent kept working.
- **Evidence:** Lewis, Table 6 (full text): F2PF difference +21.1 pp at 20,480; +6.4 at 43,008; −0.3 [−4.5, +3.9] at 262,144 tokens. The paper says that because the campaigns ran one after another, the window ordering "does not isolate window size from run-era change". Under pressure the treatment used about twice the model turns (3,280 → 6,517 on Verified) and about 3.5x the wall time. The authors say the gains are not "a compute-matched efficiency estimate". All four models are open-weight, 4-bit, locally served. No frontier hosted model was tested. One greedy run per task per arm.
- **Chris's own line:** none.
- **Visual:** the same pipe drawn wide. Old blocks don't crowd anything, the trim rule barely fires, and both outputs come out equally sharp.

### 5. On the leaderboards, harness changes move scores as much as model upgrades do.
- **Say it:** LangChain kept its model fixed, changed only the harness, and went from outside the top 30 to the top 5 on Terminal-Bench 2.0. A position paper ran three frontier models through three harnesses: switching harness moved a model by 8 to 13 points, and switching model moved scores by only 2 to 5.
- **Evidence:** LangChain, Trivedy, "Improving Deep Agents with harness engineering", 17 Feb 2026 (blog): GPT-5.2-Codex fixed, Terminal Bench 2.0 (89 tasks), 52.8% → 66.5% (+13.7), "Top 30 to Top 5". Changes: build-and-verify prompting, a pre-completion checklist hook that forces a verification pass before exit, a hook that maps the directory at startup, a loop-detection hook, and a "reasoning sandwich" (xhigh-high-xhigh). Running at xhigh throughout scored worse (53.9%, from timeouts) than high (63.6%). Zhang et al., "Stop Comparing LLM Agents Without Disclosing the Harness", arXiv 2605.23950, 7 May 2026 (full text): 100-task SWE-bench Verified subset, GPT-5.4, Kimi K2.6 and GLM-5.1, two runs per cell. The harness moved GLM-5.1 by 13.0 points and the other two by 8.5. The model moved scores by 2.5–5.0 at a fixed harness, and rankings flipped in 6 of 9 comparisons.
- **Chris's own line:** none.
- **Visual:** a leaderboard where the bars are labelled by model, then the labels peel off to show a harness name underneath each one.

### 6. But it isn't always a win: two good harnesses on a frontier model can tie.
- **Say it:** A team ran Opus 4.8 and GPT-5.5 each in its maker's own harness and in a neutral one, on 80 private tasks. Average solve rates came out within about a point. The difference showed up in cost and behaviour instead: the neutral harness made twice the tool calls, hit the time limit more often, and cost 1.2 to 1.6 times as much per solved task. So "the harness matters" means it depends on your workload, your context budget, and what you measure.
- **Evidence:** Arjmandi, "Harness or Model?", arXiv 2609.11987, revised 8 Sep 2026 (full text). claude-agent-sdk vs deepagents on claude-opus-4-8: 48.8% vs 50.0% (−1.25 pp, CI [−10.0, +7.5]). openai-codex SDK vs deepagents on gpt-5.5: 55.6% vs 54.4% (+1.25, CI [−4.4, +6.9]). On Opus, the native harness trailed by 9.0 pp on repo tasks and led by 23.7 pp on contest tasks. That split was post-hoc. Its own summary of Lewis: "a large effect under a tight context window and almost none under a wide one", and "the harness effect is conditional on workload, context regime and the endpoint measured".
- **Chris's own line:** none.
- **Visual:** two well-built pipe mazes side by side, the same sharp output from both, but one has a fuel gauge draining faster.

## The takeaway

Before you blame the model or pay for a bigger one, look at what your agent was seeing when it failed: how full was the context, and how much of it was stale logs and repeated output? Try one harness change on your own tasks this week: trim old tool output, add a "you're repeating yourself" check, or force a verify step before it says done. Measure before and after.

## Bridge

"If the harness can move the score this much, the next question is obvious: how do you build a good one for your own repo? That's Harness 101."

## Extra material (for a long cut or a written companion)

- **The Astra cost twist.** At high reasoning, the 99.9% run cost $18,817 and the 54.8% run cost $40,705. A better harness was both more accurate and cheaper. At every reasoning level the adapter was cheaper (ARC Prize blog table).
- **Lewis's reading boundary.** The treatment more than doubled how much a task could require reading before the agent filled its window without editing anything (Verified: 0.71 → 1.81 windows' worth). Good for showing why trimming helps: the agent can finish reading before it runs out of room.
- **Lewis tuned the setting during development and then froze it.** Her probes found that scaling the trim caps up 2x or down 0.5x, or changing when trimming starts, did worse (Table 18, 15 tasks). The operating point matters.
- **Lewis's recommendation:** turn trimming on from the start, because "We cannot know at the start of a long task whether context will bind," and with a wide window it cost nothing. At 262K it served 7.2% fewer prompt tokens per turn with no loss.
- **Lewis on evaluation:** evaluations "should report the model, harness, tool interface, model-visible context, context limit and policy, time limits". Zhang et al. propose a "Harness Card" with seven layers: Execution, Tool, Context, Scheduling, Observability, Verification, Governance (ETCSOVG).
- **Zhang et al.'s control-theory framing:** the harness is a controller, the LLM an open-loop policy. Three harness-only properties: stability, context drift, control lag. "Open-loop systems do not become reliable through bigger actuators. They become reliable through feedback control." This is a good line for a research-engineer audience.
- **Leaderboard examples cited in Zhang et al.** (secondhand, attribute them): Claude Opus 4.5 got 45.9% on SWE-bench Pro under the standard SEAL scaffold and 55.4% under Claude Code (Morph leaderboard). HAL reports 34-point cross-scaffold gaps for Claude Sonnet 4.5 on SWE-bench Verified Mini (68% → 34%).
- **LangChain on per-model tuning:** Claude Opus 4.6 scored 59.6% "with an earlier harness version", and the post says tailoring harnesses per model helps. This supports Chris's RL line: the harness and model are fitted to each other.
- **Arjmandi's other finding:** 22 of 81 runs that hit the time ceiling had already produced a passing patch. "Correct output and autonomous completion are different endpoints." This is a good ep 7 beat: knowing when to stop is a harness job.
- **The work talk** in [[2026-09-07 - harness matters]] (a team's custom harness beat the platform harness). Keep it out of VO, as SERIES.md says. If used at all: "I've seen this at work too: a team's own harness beat the platform default."

## Don't say

- **"One change, shortening old tool results, took it from 28% to 49%."** The treatment is a package: trimming, a stall detector with nudges, and command safeguards. The paper doesn't isolate trimming. Say "one harness setting" or "a context-trimming package".
- **"28% to 49% on SWE-bench"** without the conditions. Add "in a tight 20K window, with a mid-size open model". At 262K the gain was zero.
- **"The harness matters more than the model, period."** Arjmandi found no average difference between vendor and neutral harnesses on frontier models. Zhang et al. limit their thesis to long-horizon tasks across comparably strong models.
- **"Lewis showed it on frontier models."** All four models were open-weight, 4-bit, served locally.
- **"Free gain."** The treated agent used about 2x the turns and 3.5x the wall time under pressure. Partly, it won by not stopping.
- **"Astra is AGI"** or **"Astra scored 99.9% on ARC-AGI."** Say "ARC-AGI-3, with OpenAI's provider harness". ARC Prize says it isn't claiming AGI.
- **"Claude Opus 5 went from 30% to 100% in NVIDIA's scaffold."** This appears in blog coverage of Astra (kingy.ai and similar). ARC Prize's Astra post doesn't report it. Unverified, so drop it.
- **The "46% vs 80%" Cursor figure.** Secondhand, as SERIES.md already says. Also skip Vercel's "80% → 100% by removing tools", which marmelab itself labels secondhand and unverified.

## Corrections to SERIES.md

1. **Answer line:** "One change, shortening old tool results as the context fills" is wrong in detail. The treatment is one configuration package: half-life trimming of old tool results, plus a stall detector with fixed nudges, plus command safeguards. Their effects aren't separated. Suggested rewrite: "One harness configuration (trimming old tool output as the context fills, plus a nudge when the agent repeats itself) took a model from 28% to 49% ..."
2. **Missing conditions on 28% → 49%:** model Qwen3.6-35B-A3B (4-bit, local), window 20,480 tokens, 480 s budget, 169 tasks. The numbers are confirmed: 28.0 → 49.1% mean per-task F2PF, and 43 → 72 solved. "Helped three other models too" is confirmed: Devstral, Nemotron, Qwen3.8, all open-weight. Why the effect shrinks when the window is wide: at 262K tokens fewer than 1% of runs hit the context limit, so trimming barely matters (−0.3 pp). Also, the gain partly comes from the treated agent continuing after the control would have run out of room (about 2x turns).
3. **Astra claim: verified, so un-mark "unverified".** ARC Prize, 3 Sep 2026, ARC-AGI-3 Semi-Private, GPT-6 Astra: Standard harness 54.8% (high) / 62.7% (max); Provider Adapter harness 99.9% (high) / 98.6% (max). It can move into VO and is the best hook.
4. **LangChain claim: confirmed.** The benchmark is Terminal Bench 2.0 (89 tasks), the model GPT-5.2-Codex fixed, 52.8% → 66.5%. The "Top 30 to Top 5" phrasing is the post's own TLDR. Author Vivek Trivedy, 17 Feb 2026, blog URL now https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering. (The Readwise note is the X thread version.)
5. **Sources read status:** Lewis is now full; 2605.23950 (Zhang, Wang, Ge, Xu, Hamm, Reddy; position paper, 7 May 2026) is full; 2609.11987 (Arjmandi, revised 8 Sep 2026) is full. Note 2609.11987 is a **counterweight**, not support: it found no average harness effect between vendor-native and neutral harnesses on Opus 4.8 and GPT-5.5.
6. **Answer "Often, yes"** should carry the condition: the effect is largest under tight context and on long, messy tasks, and can vanish for strong models with room to spare.

## Sources

- Sydney Lewis, [Same Model, Different Harness: Different Coding-Agent Results](https://arxiv.org/abs/2608.26218), arXiv 2608.26218, 26 Aug 2026. **Full text** (HTML), including appendix tables. The controlled experiment: 28 → 49% F2PF and its context-width condition. Code: https://github.com/sydches/yuj.
- Yunbei Zhang et al., [Stop Comparing LLM Agents Without Disclosing the Harness](https://arxiv.org/abs/2605.23950), arXiv 2605.23950, 7 May 2026. **Full text** (main body; appendices skimmed via the TOC). The 3×3 grid (harness moves 8.5–13 pp, model 2.5–5 pp), the "open-loop policy, harness as controller" framing, and the Harness Card.
- Mohsen Arjmandi, [Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite](https://arxiv.org/abs/2609.11987), arXiv 2609.11987, revised 8 Sep 2026. **Full text** (abstract, design, discussion, limits, related work). The counterweight: no average difference between vendor and neutral harnesses on frontier models, with cost and completion differences.
- ARC Prize, [OpenAI's GPT-6 Astra on ARC-AGI-3](https://arcprize.org/blog/astra), 3 Sep 2026, and [GPT-6 Astra results page](https://arcprize.org/results/openai-gpt-6-astra). **Blog and results table** (via fetch). The 54.8% vs 99.9% hook and the harness descriptions.
- LangChain, Vivek Trivedy, [Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering), 17 Feb 2026. **Blog** (via fetch). The Terminal Bench 2.0 result: 52.8 → 66.5%, Top 30 → Top 5, model fixed.
- OpenAI, Lopopolo, [Harness engineering](https://openai.com/index/harness-engineering/), 11 Feb 2026. **Full** (read for ep 1). The line "anything it can't access in-context ... effectively doesn't exist".
- Vault notes: [[2026-09-07 - harness matters]] (Chris; the RL line, the Astra lead, his questions), [[2026-09-11]] (Chris; "Managing contest the whole game."), [[Improving Deep Agents With Harness Engineering]] (Readwise, Trivedy thread).
