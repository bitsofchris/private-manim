# Ep 9: Agents that share a notebook (GitSwarm) (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 1
paper (full text, including the worker prompt and appendices C, G.5), 3
AugiCraft docs, 11 AugiCraft knowledge files (10 episodes, 1 skill), 4
vault notes.
**Question:** What happens when many agents build on one shared record
instead of each starting fresh?
**Who's asking:** an engineer who already runs several Claude Code or Codex
sessions in parallel and watches them redo each other's work.
**Answer in one sentence:** Give parallel agents one shared git repo where
every attempt, including the failures, is committed with a note on what it
built on, and their work starts to compound instead of repeat.
**Search phrase:** multi-agent coding / agent swarm / parallel claude code
agents (guess) **Superseded:** checked against autocomplete 2026-10-17; the checked phrase and title are in `SCRIPTS.md`.
**Length:** Short + companion. The Short carries one paper, one number, and
one Minecraft moment. The design details (the commit format, the three
actions, the controlled tests) fit a written companion.


## The Short, as rewritten 2026-10-17 (Chris)

Rebuilt from Chris's own notes using his writing guidance (content-preflight, notes-to-post, effective-writing). Where this block and the points below disagree, this block wins for the Short; the points below are companion material. Script: `SCRIPTS.md`.

- **Question:** How do I run several agents without them redoing each other's work?
- **Answer:** Give them one shared record where each agent writes what it learned and what it built on.
- **What the viewer does after:** Give your parallel agents one shared record; have each one write what it learned and say what it built on.
- **Built from:** Chris's AugiCraft journal leads (10/17: "had to let it learn and take notes for itself… once we had one working it was easy to add more"; 10/12: four agents with their own jobs; the door-skill reuse). GitSwarm is one beat (94.7% built on, ProgramBench).

## Hook options

1. "The idea that won started as a failure. Another agent wrote it down,
   and a third one picked it up two days later." (RMT run: a failed idea
   revisited 49.5 hours later went into the final model.)
2. "Run five coding agents in parallel and most of them redo each other's
   work. One paper gave them a shared git repo, and 95% of everything they
   committed got built on later."
3. "My Minecraft bot fixed a door at lunch. Nearly four hours later a different
   bot, which had never seen that door, used the fix to escape pillagers."
   (Chris's demo, from the AugiCraft episode files. Chris's own story, not
   his sentence.)

## Key points, in episode order

### 1. Most parallel agents throw their work away.
- **Say it:** You can run ten agents at once. Each one starts from zero,
  and when its session ends, what it learned is gone. Partial solutions,
  dead ends, the experiment that almost worked: all lost. The next agent
  rediscovers it, or never does.
- **Evidence:** GitSwarm's framing: "If such work disappears when an
  episode terminates, later computation may need to rediscover it." They
  call the fix *compounding inference*: intermediate work persists and can
  be "inspected, extended, combined, or challenged" by later agents
  (arXiv 2610.04862, full text, §1).
- **Chris's own line:** "one meta agent or orchestrator that can kick off
  tasks and selectively fetch context from other agents." From
  [[2026-01-26 - Human Agent Workflows]]. (It's the centralized version.
  GitSwarm drops the orchestrator, which makes a good contrast.)
- **Visual:** five blobs, each with its own short pipe, each output
  dripping onto the floor and evaporating.

### 2. GitSwarm's fix is a git repo with three rules: keep everything, allow branches, say what you built on.
- **Say it:** Every agent works in its own git worktree. Each finished
  attempt is one commit, even a failed experiment. And every commit
  message has to say which earlier commits it used, even ones on other
  branches. No planner hands out roles. Each agent reads the repo and
  decides for itself.
- **Evidence:** the three design principles are *persistence*,
  *branchability* and *attribution* (§2.1). The commit format from the
  worker prompt (Appendix H.2), verbatim:
  `[<brief description of the type of contribution>|informed_by=<sha1>,<sha2>,...] <summary>`.
  The git parent says where the agent started. `informed_by=` says what it
  used, so an agent can extend one branch and borrow from another without
  a merge. Each commit also carries `MY_THOUGHTS.md` (sources used,
  reasoning, evidence, open TODOs) and `EVALUATION.md` (a candid
  assessment). Full text.
- **Chris's own line:** none.
- **Visual:** the pipes now drain into one shared tank (the repo). Each
  drop that lands is tagged with thin threads back to the drops it came
  from.

### 3. How an agent picks what to build on: read a few commits, claim a gap, or step aside.
- **Say it:** Each new agent starts with `git log --graph`, opens a handful
  of promising commits, and checks what the agents still running are
  doing. Then it picks one of three moves. It can add one bounded piece of
  work, nominate the best existing answer, or abstain if the useful work
  is already done or under way. Before it edits anything, it posts its
  plan: the gap, the deliverable, how it'll know it worked, and when it'll
  quit.
- **Evidence:** the worker prompt says "Choose work with high expected
  marginal value given both the completed graph and active work" and
  "abstain rather than manufacture redundant work" (App. H.2). The scope
  is announced with
  `gs_inflight announce --summary "Gap: … | Deliverable: … | Success: … | Abort: …"`
  (§2.4). Workers don't reread the whole history. On ProgramBench they
  open about 6 of roughly 72 available candidates. Proof workers open
  about 3 (App. G.5). About one in six ProgramBench workers abstained
  after finding equivalent work (§3.5). The final answer is chosen by
  vote: the candidate with the most nominations wins (§2.5). Full text.
- **Chris's own line:** none.
- **Visual:** a new blob arrives at the tank, shines a small flashlight on
  three or four tagged drops (not the whole tank), then attaches its pipe
  to one of them.

### 4. The numbers: it scores higher, and you can measure the compounding.
- **Say it:** On a benchmark where agents rebuild real programs from docs,
  the swarm averaged 79% against 65% for one strong agent told to keep
  going. On 30 olympiad-level proofs it solved all 30 in one run. The
  better number is about reuse: 95% of what agents committed was built on
  later, and the winning program's family tree covered more than 80% of
  everything the swarm did.
- **Evidence (full text, checked):**
  - ProgramBench: 79.39% mean with Codex (GPT-5.5-High) workers at 500
    workers. The baseline, "Forced Codex", is a single Codex (GPT-5.5-High)
    agent re-prompted with "Keep working..." each time it stops, and it
    sat between 63.1% and 65.1%. Measured on a fixed 50-task subset of
    ProgramBench's 200 tasks (§3.2, §4).
  - IMOProofBench-Advanced: 30/30 in one run with GPT-5.5-High workers, at
    budgets of 40 and 80 workers (28/30 at 20). The paper adds its own
    caveat: Best-of-N with an oracle verifier also reaches the ceiling at
    lower token cost, "so saturating this benchmark does not establish a
    unique advantage for GitSwarm" (§3.2).
  - Reuse: on ProgramBench, 94.7% of contributions are later named as a
    git parent or an `informed_by=` source. The selected solution's
    transitive ancestry covers 81.6–92.6% of the graph (on average, across
    budgets). Git-parent ancestry alone is only about a quarter, and the
    cross-branch `informed_by=` links carry the rest (§3.4). On proofs the
    numbers are much lower: 44.4% built on, 21.3–33.0% ancestry. There,
    later agents mostly check and compare proofs instead of extending them.
- **Chris's own line:** none.
- **Visual:** the tank's family tree lights up green from the winning
  output backward, and most of the tank glows.

### 5. Failures are worth committing.
- **Say it:** In the open-ended research runs, the failures did real work.
  One agent tried an idea that didn't pan out and wrote it down. Two days
  later another agent extended it, and it ended up in the final
  architecture. In another run, a fix that was rejected early was
  re-tested on more data and turned out to be the winner.
- **Evidence (full text, §3.3):**
  - Residual Matrix Transformer: "one of them began as a failed attempt to
    use the previous token's memory. Another worker revisited the result
    49.5 hours later" and built the temporal mixer that went into the
    final model. Held-out loss was 2.890 and 2.894 against 3.147 for the
    reference, on the same 1.3B training tokens.
  - Looped Transformer: the winning adapter was rejected after a
    128-example eval. Others re-ran it on 512 examples and confirmed it.
    74% of negative architectural results were later cited.
  - NanoChat: 70.1% of negative-labelled commits were cited by later
    accepted work.
- **Chris's own line:** none in his notes. (Close in spirit: the 6/12
  draft's Darwin Gödel Machine line, "greedy circles, archives spiral", is
  his summary of DGM. It fits as a bridge if he wants it.)
- **Visual:** a red, crossed-out drop sits in the tank. Later a new thread
  reaches back to it, and it turns green.

### 6. The demo: in AugiCraft, one bot's door fix let another bot escape pillagers.
- **Say it:** My Minecraft bots share one knowledge folder. At midday the
  original bot, Augi, couldn't walk through its own front door, because
  the pathfinder treated an open door as a wall. It diagnosed the problem,
  fixed it, did the trip twice, and saved the procedure as a skill. Nearly
  four hours later I spun up new worker bots that had never touched that door.
  They searched the shared knowledge, loaded the skill, and when pillagers
  showed up, one retreated through that door to safety.
- **Evidence (from Chris's repo `~/repos/augi-craft/knowledge/`, read in
  full; times are UTC from the file IDs, all on 2026-10-12):**
  - 17:03, episode `augi-return-to-base-repair-diagnose-door` (failure):
    "Original planner treated open door as physical block". After that fix
    the planner "aimed at top of panel… causing jump stall". Its lesson:
    "Opening a door and navigating through it are separate runtime
    capabilities".
  - 17:03:34 and 17:03:38, two successful runs through the door. 17:04:42,
    skill `learned/validated/return-to-base-open-door-and-deposit.md` is
    saved. 17:05:04, it is promoted to `validated` (promotion needs
    successes from distinct episodes). Its `evidence:` field lists both
    episode IDs. That's AugiCraft's version of `informed_by=`.
  - 20:50, two new worker bots in separate Codex sessions. AugiDiamonds'
    episode lists `kb_search`, `kb_get` and `kb_recent_episodes` in its
    tools, and `return-to-base-open-door-and-deposit` under `skills_used`.
    Action: "Retreated through open verified door to base_inside after
    observing pillagers outside; did not engage." AugiMiner lists the same
    skill and "Retreated walk-only to base_inside".
  - 21:22, AugiDiamonds uses the skill again to deposit into the base
    chest.
  - Four minutes before the fix (16:59), another bot, AugiTwo, was stuck at
    the same doorway with the same top-of-panel bug, and logged "Manager
    installed normalizeDoorPath during diagnosis; requires own MCP reload."
    Two agents were debugging one bug at the same moment. That's the
    duplicate-work problem from point 1, in Chris's own logs.
- **Chris's own line:** "spawned an army of 4 agents to join us with deeper
  roles - more walking issues but eventually got there" and "stood around
  - blocked by house or unable to craft things, couldnt open the door".
  From [[2026-10-11 - LLM Plays Minecraft - AugiCraft]] (his 10/12 journal
  block).
- **Visual:** two small blobs in Minecraft-block style. The first leaves a
  glowing note on the door. The second arrives later, reads the note, and
  slips through as pillagers close in.

### 7. What AugiCraft does differently, and what to copy.
- **Say it:** My crew has assigned roles and a lock, so two bots can't
  write the notebook at once. GitSwarm has no roles at all. It gets its
  safety from git itself: separate worktrees, one atomic commit per
  attempt. If you're building a shared notebook for agents, start with a
  git repo and a commit message rule before you build anything fancier.
- **Evidence:** `docs/WORKER_CREW.md`: "Concurrent writers are NOT safe in
  the current runtime." On 10/12 Chris shipped "a reentrant PID lock on
  the knowledge root" with atomic file replacement. GitSwarm: "No central
  intellectual planner assigns tasks or roles" (§1). Every worker runs in
  an isolated git worktree (§2.3).
- **Chris's own line:** none.
- **Visual:** left, a single notebook with a padlock and a queue of blobs.
  Right, a git branch tree where each blob writes on its own branch.

## The takeaway

Short (10/17): Give your parallel agents one shared record; have each one write what it learned and say what it built on.

Companion: When you run agents in parallel, have them share one git repo. Add three
rules to your AGENTS.md: read `git log` before you start, commit every
attempt (failed ones too) with a short notes file, and list the commits
you built on in the commit message (`informed_by=<sha>`). Tell them to
stop if the work is already done or under way.

## Bridge

If the harness can teach many agents through a shared notebook, the last
question is whether it can stand in for training the weights at all
(ep 10).

## Extra material (for a long cut or a written companion)

- **The three controlled tests (App. C).** Each one isolates a property.
  *Persistence (Hidden Rulebook):* independent agents re-query the same
  first links of a chain. Shared memory lets a later agent continue where
  the last one stopped. *Branchability (Hidden Maze):* if an agent can
  restore a saved checkpoint, it doesn't pay again for the known path.
  Repeated moves drop a lot. *Attribution (Retracted Evidence):* when one
  lab's result is retracted, agents with parent links read far less of
  the archive to find what's invalid, and the gap widens with lineage
  depth. These are clean, animatable toy problems. The paper says they
  don't prove which property drives the benchmark gains.
- **Roles emerge without being assigned.** On ProgramBench, after an
  initial burst, agents keep expanding, repairing and synthesizing, and
  nomination rises near the end. The winning candidate first appears at
  93–98% of run progress. On proofs, agents switch to judging early, and
  the selected proof appears at 8.6–17.5% of progress (§3.5).
- **Async vs sync, voting vs a judge (§3.5, small dev set).** Async
  finished in 38.0 min against 49.3 for synchronized waves. A central
  selector was slightly faster than voting. The paper says these don't
  establish equivalence.
- **Votes are not evidence.** The prompt tells agents that "apparent
  agreement can be correlated or redundant" and not to "copy the apparent
  majority". It's a good line for anyone building judge agents.
- **Seeded reuse across runs.** Seeding a new swarm with the winners of
  three earlier swarms brought dev loss from 2.909 to 2.898 in about 28
  hours (§3.3).
- **Costs.** Input tokens grow as agents read a bigger repo, and gains
  flatten at larger budgets (§3.2, §4).
- **The authors' next step:** train agents with RL to make contributions
  "whose value emerges through subsequent work" (§5). This is a natural
  link to ep 10.
- **Chris's goal list,** from [[MOC - System of AI agents - Army of Agents]]:
  "Ideas to learn - Orchestration frameworks - eval / feedback loops -
  self-improving agents". From 2025-06-14: "Saw the potential - me the ceo
  of a company of AI agents." Also from 2025-11-07: "Just use Claude code
  subagents?"
- **Other AugiCraft details:** the skill format's `evidence:` list, the
  promotion rule ("`kb_promote` needs `promotion.minSuccesses` successes
  from distinct episodes"), and `learned/deprecated/` (one skill,
  `automatic-self-defense-and-shelter`, was retired after Chris asked for
  local defense only). That last one is the "challenge" path.
- The OpenAugi task-file comparison SERIES asked for wasn't done in this
  pass.

## Don't say

- "GitSwarm solved IMO problems no one else could." The paper says Best-of-N
  with an oracle verifier also hits 30/30 at lower token cost.
- "79 vs 65 on ProgramBench" without saying who the 65 is. It's one
  re-prompted Codex agent, on a 50-task subset.
- "94.7% of everything gets reused" as a general claim. It's ProgramBench
  only. On proofs it's 44.4%.
- "The shared memory caused the gains." The paper says its analyses show
  reuse, not causation, and `informed_by=` is declared by the agents. The
  same goes for AugiCraft's `skills_used`: it's self-reported.
- "Better than any single agent on research." The paper says the results
  "do not establish superiority over every single-agent configuration".
  On RMT, plain Codex reached 2.690, but it used 10.1B tokens against 1.3B.
- Don't name GPT-6-Astra or GPT-5.6-sol as if the viewer knows them. They
  appear only in the research runs, so leave them out of the Short.
- Don't present AugiCraft's crew as roleless like GitSwarm. Its bots have
  assigned jobs and a human manager.

## Corrections to SERIES.md

- **Answer line:** "94.7% of contributions get built on later" and
  "82–93%" are ProgramBench-only figures. On IMOProofBench they are 44.4%
  and 21.3–33.0%. The exact range is 81.6–92.6%, averaged across budgets.
- **Numbers line:** "65.1% for the strongest reported baseline" is a single
  Codex (GPT-5.5-High) agent re-prompted to keep working ("Forced Codex"),
  at its best checkpoint (range 63.1–65.1%), on a 50-task subset. Add that.
- **Numbers line:** "all 30 … solved in one run (GPT-5.5)". The model is
  Codex GPT-5.5-High. Add the paper's caveat that oracle Best-of-N also
  saturates the benchmark.
- **"Better architectures on three … tasks":** the accurate version is
  "improves on the starting architectures in all three". It is not better
  than every baseline.
- **Read status:** GitSwarm is now read in full (it was marked "abstract").
- **Affiliation, for the record:** Meta Superintelligence Labs (plus Mila,
  CMU, Princeton, Columbia). Authors as listed are fine.
- **AugiCraft line:** "The bots write `knowledge/episodes/` that the next
  bot reads." True, but the stronger receipt is the validated skill file
  plus the later episodes that cite it (point 6).

## Sources

- Shah et al., *GitSwarm: Decentralized Compounding Inference*,
  https://arxiv.org/abs/2610.04862 (HTML full text: §1–5, App. C, G.5,
  H.2 worker prompt). Contributes the mechanism, the commit format, all
  the numbers, and the failed-idea-revived stories.
- `~/repos/augi-craft/README.md` (full): the three knowledge levels and
  the skill format with `evidence:`.
- `~/repos/augi-craft/docs/WORKER_CREW.md` (full): the crew design, why
  concurrent KB writes needed a lock, and the 10/12 launch.
- `~/repos/augi-craft/docs/LIVE_RUN_2026-10-12.md` (full): the single-bot
  timeline before the crew.
- `~/repos/augi-craft/knowledge/learned/validated/return-to-base-open-door-and-deposit.md`
  and episodes `2026-10-12-16-59-36-augitwo-…-diagnose-open-do`,
  `…-17-03-28-augi-return-to-base-repair-diagnose-door`,
  `…-17-03-34-…-enter-through`, `…-20-50-08-augidiamonds-…-prep`,
  `…-20-50-59-augiminer-…-preparation`, `…-21-22-18-augidiamonds-…-retu`,
  `…-20-59-34-develop-shared-automatic-self-defense-fo`,
  `…-21-10-46-augidiamonds-self-defense-reload`,
  `…-21-13-21-manager-coordinated-worker-mcp-reloads-f`,
  `…-21-17-29-original-augi-local-self-defense-live-sp` (all full). These
  give the door-skill moment.
- Vault notes: [[2026-10-11 - GitSwarm and self improving agents with knowledge bases]]
  (a 3-line capture: the arXiv link, a Substack note link, "Have gpt
  thread on this idea". No other content) · [[2026-10-11 - LLM Plays Minecraft - AugiCraft]]
  (his 10/12 journal; the body below it is Augi-written) ·
  [[2026-01-26 - Human Agent Workflows]] · [[MOC - System of AI agents - Army of Agents]].
