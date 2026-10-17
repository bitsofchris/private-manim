# Ep 5: Context as a playbook (ACE) (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 7 (ACE full text v3 with appendix; ACE public code: curator and reflector prompts, `playbook_utils.py`, `bulletpoint_analyzer.py`, `ace.py`; this repo's runbook step 11, `AGENTS.md` "Keeping the system clean" and `agents/changelog.md`; OpenAugi `system-janitor.md` and `augi-agent.md`), plus 5 vault notes.
**Question:** How do I stop my CLAUDE.md / AGENTS.md from rotting when the agent keeps updating it?
**Who's asking:** an engineer whose agent "updates the context file with what it learned" every session, and the file keeps getting blander, or longer and contradictory.
**Answer in one sentence:** Never let the agent rewrite the whole file. Have it add or change one small, labeled item at a time, each in its one home, and keep a log line per change. Whole-file rewrites quietly throw lessons away.
**Search phrase:** how to write CLAUDE.md / AGENTS.md best practices (guess). Alt: "context engineering" (guess; ep 4 may own it). **Superseded:** checked against autocomplete 2026-10-17; the checked phrase and title are in `SCRIPTS.md`.
**Length:** Short + companion. The core (rewrite vs. small edits, with one number) fits 60–75 s. The three-role loop, dedupe details and the comparison with Chris's two systems need the companion.

## Hook options

1. "At step 60, the agent's playbook was eighteen thousand tokens. One rewrite later it was a hundred and twenty-two, and the agent did worse than with no playbook at all." (ACE, §2.2. The strongest. A real number, and it's the viewer's fear.)
2. "Every time you tell your agent 'update CLAUDE.md with what you learned,' you might be deleting what it learned last week."
3. "Your agent's context file has two ways to die: it gets shorter until it says nothing, or it gets longer until it contradicts itself." (Sets up brevity bias and the janitor. Not Chris's sentence.)

None of these are Chris's own sentences. His closest is "Avoid context rot/ drift" ([[2026-09-13]]), which is too short to be a hook alone but works as the line after one.

## Key points, in episode order

### 1. Asking a model to rewrite its own notes makes the notes collapse.
- **Say it:** The obvious way to keep a context file current is to hand the model the whole file and say "rewrite this with what you learned." Researchers watched what happens. The file grows for a while, then one rewrite crushes it to almost nothing, and the agent gets worse than if it had no notes.
- **Evidence:** ACE paper (Zhang et al., ICLR 2026), §2.2, "context collapse", measured on AppWorld with Dynamic Cheatsheet's full-rewrite mode: at step 60 the context was 18,282 tokens at 66.7% accuracy. At step 61 it was 122 tokens at 57.1%, below the 63.7% no-adaptation baseline. They call it "a fundamental risk of end-to-end context rewriting with LLMs, where accumulated knowledge can be abruptly erased instead of preserved." Checked: full text.
- **Chris's own line:** "Also the janitor for agents to de dupe and have fewer things to maintain." … "Avoid context rot/ drift". From [[2026-09-13]] (verified in the daily note; also quoted in [[What Works - Running a Second Brain With Agents]]).
- **Visual:** the context pipe carries a long scroll. A "rewrite" press stamps it, and it comes out a scrap. The blob downstream goes dull and soft.

### 2. The second failure is slower: rewrites drift toward short and generic.
- **Say it:** Even without a crash, optimizers that rewrite a prompt drift toward short, safe, generic advice. The specific stuff, the tool quirks and the failure modes that actually saved you, is what gets cut first. The paper calls it brevity bias.
- **Evidence:** ACE §2.2, citing Gao et al. 2025 on test-generation prompts, where iterative optimizers kept converging to near-identical lines like "Create unit tests to ensure methods behave as expected." ACE's position: "contexts should function not as concise summaries, but as comprehensive, structured playbooks." Unlike humans, LLMs "are more effective when provided with long, detailed contexts and can distill relevance autonomously." Checked: full text.
- **Chris's own line:** none fits directly. Optional nod: "Prompts that evolve, tailoring to use case." From [[2025-03-12 - Augi defensible edge open core]] (the line sits under the 2025-03-13 heading). He wrote it about seven months before ACE appeared (see Corrections).
- **Visual:** the scroll is re-copied by hand, each copy shorter and blurrier, and the details fall off as little crumbs.

### 3. The fix: the context is a list of small, labeled items, and updates only add or change items.
- **Say it:** ACE stores the context as a playbook of bullets. Each bullet is one small lesson with an ID and two counters: how often it helped and how often it hurt. After each task the system doesn't rewrite the playbook. It writes a small "delta", a few new bullets, and plain code slots them into the right section. Nothing old is touched by the model.
- **Evidence:** ACE §3.1. A bullet is "(1) metadata, including a unique identifier and counters tracking how often it was marked helpful or harmful; and (2) content, capturing a small unit such as a reusable strategy, domain concept, or common failure mode." Deltas "are merged deterministically into the existing context by lightweight, non-LLM logic." In the public code (github.com/ace-agent/ace) a bullet line literally reads `[ctx-00263] helpful=1 harmful=0 :: <content>`, and the curator's only allowed operation is `ADD` ("Do NOT regenerate the entire playbook - only provide the additions needed"). UPDATE, MERGE and DELETE are listed as TODO in `playbook_utils.py`. Checked: full text + code.
- **The number:** the ablation in Appendix A.5 / C.2. Same system, AppWorld test-normal, DeepSeek-V3.1: with full rewrites the gain over the ReAct baseline is +3.6 points on average. With delta updates it's +17.0 (70.3 vs 56.9 average of TGC and SGC). Removing deltas costs 8.9 points TGC and 17.9 points SGC (the paper's C.2 text says "-11.7% TGC and -27.8% SGC", which appear to be relative drops; quote the table's points, not those). Checked: full text, Table 18.
- **Chris's own line:** none. (His "Never state the same rule in two files" is in this repo's `AGENTS.md`, written by agents with him; not a vault quote.)
- **Visual:** the scroll becomes a rack of numbered index cards. A new card clicks into a slot. Each card has a tiny ✓/✗ tally.

### 4. Three roles do the work: one acts, one reflects, one files the lesson.
- **Say it:** The Generator does the task and flags which bullets helped or misled it. The Reflector reads the trace and the result and writes down what went wrong and why. The Curator turns that into a few new bullets and decides where they go. Splitting "what happened" from "what goes in the file" is part of why it works.
- **Evidence:** ACE §3, Figure 4. The Reflector prompt in the code asks for `error_identification`, `root_cause_analysis`, `correct_approach`, `key_insight`, and a helpful/harmful/neutral tag per bullet used. Ablation (Table 3, AppWorld offline): no Reflector and no multi-epoch gives 55.1 average; adding the Reflector gives 56.8; adding multi-epoch gives 59.4 (baseline 42.4). Defaults: up to 5 Reflector rounds and 5 epochs. All three roles use the same model, to show the gain comes from the context and not from a stronger teacher. Checked: full text + code.
- **Chris's own line:** Böckeler's line with his margin note: "always by having Codex itself write the fix." Note: "Like last week - compounding teams, tool helping tool get better" ([[Harness Engineering]], Readwise).
- **Visual:** three small figures at the pipe: a worker, an inspector with a magnifier on the trace, and a clerk filing a card.

### 5. Headline results: it works when the feedback is real.
- **Say it:** Across agent and finance benchmarks ACE beat strong prompt optimizers by about ten points, and on AppWorld an open-weights model with an ACE playbook roughly matched the top production agent. It also learned without answer labels when the environment itself said pass or fail, like code that runs or crashes. Where there was no reliable signal, it could make things worse.
- **Evidence:** ACE abstract and §4. "+10.6% on agents and +8.6% on finance." These are average point gains over the selected baselines. AppWorld: ACE 59.4% average vs IBM CUGA 60.3% (GPT-4.1), on the 20 Sept 2025 leaderboard, with DeepSeek-V3.1; online ACE beat CUGA by 8.4 points TGC on test-challenge. The paper says CUGA "is not used as a methodological baseline." Without labels on AppWorld: +14.8 average over ReAct. Finance without labels, online: FiNER fell 3.4 points below the base model. The paper: "context adaptation depends critically on feedback quality." Cost: vs GEPA offline, 82.3% lower adaptation latency and 75.1% fewer rollouts. Checked: full text, Tables 1, 2, 4.
- **Chris's own line:** none. (Ep 7 owns his verifier's-law lines; this is the bridge to them.)
- **Visual:** the ✓/✗ tallies on the cards only move when a green or red light at the end of the pipe flashes. With the light off, cards pile up unchecked and a few are wrong.

### 6. Chris's two systems do the same thing by hand, with a human on the gate.
- **Say it:** My video repo and my notes vault both hit this problem, and both landed on ACE's shape without the paper. After each video an update pass mines the session for every correction and workaround, decides whether each one is a rule, a token, a part, a tool or nothing, edits it into its one home, and logs one changelog line. Once a week a janitor checks that no rule is stated twice or contradicts another. It reports and doesn't fix. I tick what gets fixed.
- **Evidence (mapping, checked by reading the files):**

| ACE | This repo's update pass (`agents/runbook.md` step 11, `AGENTS.md`) | OpenAugi janitor (`lenses/system-janitor.md`) |
|---|---|---|
| Generator: does the task | The session that made the Short | (n/a; it audits, it doesn't act) |
| Reflector: trace → lessons | "Mine the session. List every change Chris asked for and every workaround or wish an agent reported." | Weekly inventory of `AGENT/`, lenses, launchd jobs |
| Curator: lessons → delta bullets, by section | "Decide: rule, token, part, tool, or nothing. Make the edits in their one home." Sections are files. | Proposes drift fixes as `- [ ] fix:` boxes; never edits rules |
| Bullet = one small lesson | "A new trap is written as trigger, cause, fix, and what the wrong version looked like, and only once the fix has actually worked." | One drift item = one checkbox line |
| helpful/harmful counters | `agents/parts.md` use counts, "promote at two" | (none) |
| Embedding dedupe | "Never state the same rule in two files. Link instead. If you find a duplicate or a contradiction, resolve it toward the precedence order" | Checks every rule against the files that state it; "a finding that is still true and already sits in a kept entry is not repeated" |
| Append-only delta log | `agents/changelog.md`: "One line per change … with the video that forced it." | Deck changelog rows from commits; git keeps history |
| No human gate | Chris says "go" to start; commit is separate | "Drift is proposed, never fixed"; he ticks, a `zzz:` task fixes |

- **One real example of the dedupe step (changelog, 2026-10-11):** "Hero rule, janitor: `AGENTS.md` rule 2 is the one home … `agents/style.md`, `agents/animation-rules.md` rule 12 and the HyperFrames brief said 'per beat' and now point to it." Three files had drifted on one rule. The fix kept one home and turned the other copies into links.
- **Where Chris's version differs (say at least one):** his rule files are edited in place when a rule changes ("Rule files state the current state only … no dated rulings … The why lives with the work", [[augi-agent]]). ACE's public code only ever adds. Both avoid whole-file rewrites, but his keeps the file current and pushes history into the changelog and git. ACE keeps everything in the playbook and leans on helpful/harmful counts and lazy pruning.
- **Chris's own line:** "Also the janitor for agents to de dupe and have fewer things to maintain." [[2026-09-13]]. Alt, for the build/prune tension: "Keep it simple to get mvp out asap and using it - let water flow through the hose" (same note).
- **Visual:** the card rack from point 3, now with a janitor between floors (the building image's janitor) holding a clipboard of checkboxes, and a human hand ticking one.

## The takeaway

Next time you ask your agent to update CLAUDE.md or AGENTS.md, forbid a rewrite. Have it return a short list of additions or single-item edits, each with the file and section it belongs in and the evidence that it worked, and log one line per change. Then diff: if the file got shorter and you didn't ask for a deletion, something was lost.

## Bridge

A playbook bullet is one lesson. When a lesson grows into a whole procedure you can load on demand, it's a skill, and that's the next episode.

## Extra material (for a long cut or a written companion)

- **Grow-and-refine, the dedupe step (§3.2).** New bullets are appended. Existing ones are updated in place (counters). Then a dedupe step "prunes redundancy by comparing bullets via semantic embeddings", either after every delta or lazily when the context exceeds its window. In the public code this is `BulletpointAnalyzer`: `all-mpnet-base-v2` embeddings, cosine threshold 0.90 by default, near-duplicate groups merged into one bullet by an LLM call with summed helpful/harmful counts. It is off by default (`use_bulletpoint_analyzer: False`). Note the small mismatch: the paper says merging and dedupe are "non-LLM", but the code's dedupe merge uses an LLM. The delta merge itself is plain code.
- **Hyperparameters barely matter (A.6).** Dedupe threshold 50/70/90% gave FiNER 77.0/73.9/78.6. Pruning trigger at 10K/50K/100K tokens gave 78.6/78.4/78.3. Reflector rounds: 1 round gave +8.0, 5 rounds +14.3, 10 rounds +11.9 (overthinking hurts).
- **Robust to a bad reflector (A.4).** Swapping in a weaker reflector (GPT-OSS-120B) still gave +5.9 on FiNER vs +7.6. A deliberately harmful reflector every 5 steps still left +5.4. Only harm on every single step dropped it below base (−4.0).
- **Long contexts aren't as expensive as they look (§4.7).** ACE playbooks are longer than GEPA prompts, but with OpenAI prompt caching 91.8% of input tokens were cache hits, cutting billed input cost by 82.6%. Relevant to Claude Code users: a stable, append-mostly CLAUDE.md is also cache-friendly. (The caching link to Claude Code is an inference, not in the paper.)
- **It generalizes across models (A.1).** GPT-OSS-120B, GPT-5.1, and Llama-3.3-70B all gained, usually 5–12 points. Llama gained least, which the authors put down to noisier reflections from a weaker model.
- **Beyond finance (A.2).** DDXPlus medical: 75.2 → 90.2 (GEPA 76.4). BIRD-SQL: 47.8 → 52.9 (GEPA 52.2; GEPA did better on the harder splits).
- **When not to bother (§5).** HotPotQA-style tasks do better with short, high-level instructions. Game of 24 needs one rule. ACE pays off "in settings that demand detailed domain knowledge, complex tool use, or environment-specific strategies."
- **Tension with ep 8 (write this down for the companion).** ACE says longer and more detailed beats short. AHE (ep 8) found 79 added lines of prompt discipline cost 2.3 points. SkillsBench (ep 6) found focused skills beat exhaustive ones. A reconciliation to test, not a finding: ACE's length is itemized, evidence-backed lessons the model can scan, not general advice about how to behave. Detail about the task helps; rules about conduct may not.
- **Where Chris's notes already had this.** [[Data for Agentic Retrieval]] lists "ACE paper - agentic context engineering" next to just-in-time context and hierarchical retrieval. That's a pointer only, no commentary.
- **Claude Code's own compaction is a whole-history summary.** It's tempting to say "/compact is context collapse". Don't say it in VO: ACE measured a different thing (a persistent playbook, not a conversation). It's fine as a question in the companion.

## Don't say

- "ACE improved agents by 10.6%" as if relative. It's an average of percentage-point gains over the selected baselines. Say "about ten points."
- "Beat the top production agent." Offline, it was 59.4 vs 60.3 (slightly below). It beat CUGA only on the test-challenge split in the online setting, and the authors explicitly don't treat CUGA as a baseline. Say "roughly matched."
- "A smaller model" with no qualifier. DeepSeek-V3.1 is a 671B mixture-of-experts open-weights model. GPT-4.1's size isn't public. Say "an open-weights model."
- "It learns without labels" as a blanket claim. It held on AppWorld (execution feedback) and failed on FiNER without labels (−3.4 online).
- "Chris had the idea eighteen months early." His note is from 2025-03-13 and ACE v1 is from 2025-10-06, about seven months. Better still, don't claim priority. "Prompts that evolve" is a direction, not ACE's mechanism.
- "ACE merges and dedupes with no LLM." True of the delta merge. The code's dedupe merges near-duplicate groups with an LLM call.
- "The curator updates and deletes bullets." Not in the public code (ADD only; the rest is TODO).
- "Chris's systems never rewrite." They avoid whole-file rewrites, but edit single rules in place by design.

## Corrections to SERIES.md

- **"He had the idea eighteen months early"** is wrong. The line "Prompts that evolve, tailoring to use case." is under the 2025-03-13 heading of [[2025-03-12 - Augi defensible edge open core]]. ACE v1 was posted 2025-10-06, so the gap is about seven months. Suggest dropping the priority framing.
- **Numbers line:** "+10.6% on agent benchmarks and +8.6% on finance" are average point gains over the paper's selected baselines (finance: offline +10.9 over ICL/MIPROv2/GEPA, online +6.2 over DC). "Matched the top production agent on AppWorld using a smaller open model" should be "roughly matched (59.4% vs 60.3% for IBM CUGA on GPT-4.1, Sept 2025 leaderboard) with open-weights DeepSeek-V3.1". "Learning from execution feedback without labels" holds for AppWorld (+14.8 over ReAct) but not finance (FiNER −3.4 online without labels).
- **Böckeler margin note** verbatim is "Like last week - compounding teams, tool helping tool get better". SERIES.md drops "Like last week -".
- **Worked example "no rewrites":** the repo and OpenAugi avoid whole-file rewrites, but rule files are edited in place when a rule changes ("Rule files state the current state only"). The janitor doesn't curate lessons in. It reports drift as checkboxes, and a separate ticked task fixes them. Suggested wording: "one home per rule, small edits only, a changelog line per change, and a human ticks before anything is fixed."
- **Source read status:** ACE is now read in full (v3, 29 Mar 2026, with appendix), plus the public code.
- **Learn-first answered:** a delta entry is a set of new bullets `[id] helpful=n harmful=m :: content`, added to a named section. Merge is deterministic code that appends to sections. Dedupe is embedding similarity (threshold 0.90 in code) with an LLM merge of near-duplicates, run after each delta or lazily when the window overflows.

## Sources

- Zhang et al., *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*, arXiv 2510.04618 (ICLR 2026; v1 2025-10-06, read v3 2026-03-29). https://arxiv.org/abs/2510.04618. **Read: full text including appendices** (prompts are images and weren't read). Contributes context collapse (18,282 → 122 tokens), brevity bias, the bullet/delta design, the three roles, and the A.5 ablation (+3.6 vs +17.0).
- ACE code, https://github.com/ace-agent/ace. **Read:** `ace/prompts/curator.py`, `ace/prompts/reflector.py`, `playbook_utils.py`, `ace/core/bulletpoint_analyzer.py`, `ace/ace.py` (config lines). Contributes the exact bullet format, ADD-only curation, and dedupe defaults.
- This repo: `/Users/chris/repos/private-manim/agents/runbook.md` step 11; `AGENTS.md` "Keeping the system clean"; `agents/changelog.md` (2026-10-10 and 10-11 entries). **Read: full sections.** Contributes the manual curator.
- OpenAugi: `/Users/chris/Documents/ZK Home/OpenAugi/AGENT/lenses/system-janitor.md` and `OpenAugi/AGENT/augi-agent.md` ("Rule files state the current state only"). **Read: full.** Contributes the report-don't-fix janitor and the human gate.
- Vault notes used: [[2026-09-13]] *(Chris; verified verbatim)*; [[What Works - Running a Second Brain With Agents]] *(Augi, quoting Chris)*; [[2025-03-12 - Augi defensible edge open core]] *(Chris)*; [[Harness Engineering]] *(Readwise, Böckeler, with his margin note)*; [[Data for Agentic Retrieval]] *(Chris; one-line ACE pointer)*.
