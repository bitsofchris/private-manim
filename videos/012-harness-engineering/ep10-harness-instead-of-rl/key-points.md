# Ep 10: Harness instead of RL? And the human in the harness (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 2
papers in full (GEPA v2 including App. C, E.3; the Memo position paper,
body), GEPA v1 abstract for the changed headline number, 9 vault notes,
and the AugiCraft repo (no distillation experiment exists yet).

**Ruled 2026-10-16 (Chris):** the 3/3 "just notes / files are the layer" line and the 9/6 "They're not successive…" and "The job of swe splits three ways…" lines are **not his words**. They're pasted AI replies. Use the ideas, never as VO or as "Chris's own line".

**Question:** Can you get RL-level gains without training, just by
improving the prompt and loop?
**Who's asking:** an engineer who has an agent that works "okay" and
wonders whether to fine-tune or RL it, or just keep editing prompts and
context.
**Answer in one sentence:** Often you can. Letting a model read its own
traces and rewrite its instructions beat RL training on 5 of 6 tasks, with
far fewer tries. But that learning lives in text, not in the model, so
prompt a big model first, then distill what works into weights when you
need it cheap, fast or durable, and keep a human on the reframes.
**Search phrase:** prompt optimization vs reinforcement learning / when to
fine-tune vs prompt (guess)
**Length:** needs a long cut. The Short core is points 1–4 (about 75 s).
Points 5–6, the series close, and the extra material make a 16:9 long cut
or a written companion.

## Hook options

1. "A prompt that rewrote itself by reading its own mistakes beat RL
   training on five of six tasks, and used up to 35 times fewer tries."
2. "I train models for a living. Here's when I wouldn't." (Chris's
   standing. Not a sentence from his notes.)
3. "My Minecraft bot would hit a cow, stop, think, notice the cow moved,
   plan a step, plan another hit, and the cow got away." Paraphrase of
   Chris's own journal line (point 5). Use it as the hook for the long
   cut.

## Key points, in episode order

### 1. A prompt that learns from its own traces can beat RL, with far fewer tries.
- **Say it:** GEPA runs your agent on a few examples, then hands a second
  model the whole trace: what the agent did, what the grader said, even
  the compiler error. That model writes a better instruction. Keep it if
  it scores higher, and repeat. On a small open model, this beat RL
  training (GRPO) on five of six tasks, by about 6 points on average and
  up to 19, with up to 35 times fewer rollouts.
- **Evidence (full text, v2, Table 1, Qwen3 8B):** aggregate 54.85 for
  GEPA against 48.91 for GRPO, a gain of 5.94 points. Per task: HotpotQA
  +19.0, HoVer +13.66, PUPA +5.19, IFBench +2.73, LiveBench-Math +0.69,
  and AIME-2025 −6.0 (32.0 vs 38.0, so GRPO wins there). GRPO used a fixed
  24,000 rollouts per task with LoRA. GEPA used 1,839–7,051. "35x" is
  IFBench: GEPA found its best prompt after 678 rollouts (24,000 ÷ 678 ≈
  35). Most of GEPA's budget goes to validation. Counting only training
  rollouts, it needed 79–737 to reach its best (§4, Obs. 1). The paper
  also ran one full-parameter GRPO check (2-hop HoVer) and saw a similar
  gap (Fig. 11). ICLR 2026 oral, confirmed on the arXiv page.
- **Chris's own line:** none for the result itself.
- **Visual:** two blobs side by side. Left: an RL blob gets 24,000 tiny
  pokes of a single number (a scalar drip) and slowly changes shape.
  Right: a harness blob gets a few long paper strips of written feedback
  fed into a pipe, and a new instruction sheet comes out of a slot.

### 2. Why it works: words carry more signal than one number.
- **Say it:** RL squeezes a whole attempt into one score, right or wrong.
  The trace already says *why*: which step went off, what the test
  complained about. A model can read that and fix the instruction
  directly. And GEPA doesn't only keep the single best prompt. It keeps
  every prompt that's best on at least one example, so it doesn't get
  stuck polishing one idea.
- **Evidence (full text):** the abstract argues "the interpretable nature
  of language often provides a much richer learning medium for LLMs,
  compared to policy gradients derived from sparse, scalar rewards." The
  feedback function returns "a numeric score and text feedback including
  details about the evaluation (like compiler error messages, failed
  rubrics, etc.)" (§3). The reflection meta-prompt asks the model to
  "Identify all niche and domain specific factual information about the
  task and include it in the instruction" (App. C). Pareto selection
  against always-pick-best, holding everything else fixed: +12.44 against
  +6.05 aggregate (Table 3).
- **Chris's own line:** "Nothing you intend matters, only what the
  gradient rewards." From [[2026-09-06 - Post Training, Loss functions, verifiable]].
  It's the RL side of the contrast: the gradient only sees the score.
- **Visual:** zoom into the scalar drip, which is just "0". Then zoom
  into the paper strip: "failed: query repeated the question; missed the
  album-level doc." The strip lights up a specific pipe joint.

### 3. The catch: the harness learned it, the model didn't.
- **Say it:** Everything GEPA learned lives in a prompt. Take the prompt
  away and the model is exactly as good as it was. One paper calls this
  kind of agent memory "a memo, not true memory". It's a diary you have to
  remember to open, not a lesson you've learned. That's usually fine, and
  often better: you can read it, edit it and delete it. But for new
  combinations the model never saw, the paper argues weights can learn
  from fewer examples than a growing pile of notes.
- **Evidence (full text, position paper, no experiments of its own):**
  "Agentic memory is the former; weight-based learning is the latter"
  (the diary contrast, §2). The "Frozen Novice" claim: each session
  "begins from the same frozen weights even if memory-assisted performance
  improves" (§1, §3.3). The authors also say retrieval "was the right
  choice to ship" (§1). Their sample-complexity theorem only applies when
  the frozen model, given examples in context, still falls short of the
  target. If in-context use already gets there, "the theorem makes no
  separation claim" (§3.2). They list "the absence of a compute-matched
  frontier-model validation" as a limitation (abstract).
- **Chris's own line:** "save some special tokens to a memory like place
  for retrieval almost rather than learning them". From
  [[2026-06-12 - Engram and token memory for models]]. It's the other
  direction, memory built into the model. Better for the long cut.
- **Visual:** the blob with its new instruction sheet clipped on. Unclip
  the sheet and the blob goes back to its old fuzzy shape.

### 4. So when do you train? Chris's rule.
- **Say it:** Here's the rule I use. Prompt a big model first. That's
  your baseline, and often it's enough. Train the weights when you need
  better judgement on one specific thing, or when it has to be cheap,
  fast, private, or the task is off what frontier models have seen. Train
  the loop when the problem is long or made of many steps.
- **Evidence:** this is his practice, not a paper result. It lines up
  with GEPA (edit the loop first, it's cheap) and the memo paper (weights
  for durable, off-distribution skill).
- **Chris's own line**, all from [[2026-09-06 - Post Training, Loss functions, verifiable]]:
  - "Prompt a big model first - establish a baseline, then distill"
  - "Model - the weights, train when need better judgement on the thing"
  - "Agents - the loop around the weights, train this when compositional
    solution or long horizon"
  - "They’re not successive; they’re a tradeoff. 3.0 when the task is
    general and a frontier model already does it, 2.0 when you need cheap,
    fast, private, or the task is off the frontier model’s distribution."
    (**Check with Chris:** this line sits right after an `Aaa:` request
    in the note and may be a pasted agent answer. See "Don't say".)
- **Visual:** a fork in the pipe. One branch goes to "edit the harness"
  (pipes reshape), the other to "train the weights" (the blob itself
  changes texture). A small gauge reads "cheap / fast / private /
  off-distribution?"

### 5. The turn: let the big model write the rules, and let a small model learn to use them.
- **Say it:** My Minecraft bots taught me where this goes. A big model is
  great at figuring out a skill: how to get through a door, how to climb,
  how to fight. But it's slow at every single step. My bot would hit an
  animal, stop, look, notice it moved, plan, hit again, and the animal got
  away. So the plan is: the big model writes the tools and the rules, and
  a small, fast classifier learns which one to use next. The harness
  teaches, and the weights learn.
- **Evidence:** this is a plan, not a result. There's no distillation code
  or experiment in `~/repos/augi-craft` yet (checked). What exists: the
  big model did write and validate reusable skills on 10/12 (doors,
  hunting, local self-defense; see `knowledge/learned/validated/`).
  "Jev" is the text classifier from Raschka's article; Chris's highlight:
  "the ChatGPT moment for classification, where it can cheaply classify
  all kinds of text inputs without having to fine-tune a custom
  classifier for each task".
- **Chris's own line** (verbatim, from his 10/12 journal in
  [[2026-10-11 - LLM Plays Minecraft - AugiCraft]]):
  - "attacking animal - would hit, then observe, then realize animal
    moved, then plan a move, then plan a hit - very slow and animals kept
    getting away"
  - "now that we learned all this can I train a Jev like thing to pick
    next action? So the big model trains or writes the action rules and
    tools then the small classifier just decides what to do and how to use
    it?"
  - And his margin note on the Jev article ([[Language Models for Text Classification From Bag-of-Words to Jev]]):
    "So you have a representation then you train a classifier - that’s
    it? Thats the key now?"
- **Visual:** the big blob, slow and glowing, draws the pipe layout (the
  rules and tools) on a blueprint. A tiny, quick blob then runs through
  those pipes, picking a valve at each junction in real time.

### 6. What's left for you: the reframes, and reading the raw traces.
- **Say it:** If the harness improves itself and the weights learn from
  the harness, what's your job? On my own long agent loop at work, the
  agent did the grinding, but every big change of direction came from me.
  The part you shouldn't hand off is reading the raw traces yourself.
  That's where your opinion forms, and it's how you notice the objective
  has gone stale. Let the interns run; you nudge.
- **Evidence:** [[2026-06-11 - PVC at work retrospective]] is an
  **Augi-written** distillation of his agent's retro (#ai-generated), not
  Chris's own words. Usable as a paraphrased fact: "Every major pivot came
  from human steering" and "Human steering drove every architecture
  pivot". Generalize it: a data-loading agent at work, no project name.
  The "read raw traces" point is Langfuse's, as distilled in his 6/12
  draft ("Keep manual: reading raw traces yourself — that's where your
  opinion forms and where the eval target stays fresh"). That section of
  the draft reads like an agent distillation too, so credit Langfuse and
  don't quote it as Chris.
- **Chris's own line** (from [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]],
  the 6/13 journal draft, which reads as his own typing):
  - "we have our "capable interns" they don't tire so let them run in
    loops and just nudge them when stuck or give them the tools and
    resources to get unstuck"
  - "steer and help introduce entropy"
  - "space to step back - steering, entropy, fresh session"
  - Close: "Augment, stay human." From
    [[2026-09-19 - Agents in my second brain video update]] (also used in
    the 6/12 outline).
- **Visual:** pull back to the full pipe machine from ep 1. A small human
  figure stands at one valve, turning it. The machine runs, and the human
  reads a printed trace strip.

## The takeaway

Before you fine-tune anything, run one reflection loop: save 20 failing
traces with the grader's actual messages, have a strong model rewrite the
instruction from them, and keep the rewrite only if it scores higher on
held-out examples. Train weights only when that plateaus, or when you need
the result to be cheap, fast, private or off-distribution. Then distill
from the big model's best traces.

## Bridge

Series close. It hands off to Chris's research-engineer track: the
AugiCraft "big model writes the rules, small model picks the action"
experiment is the natural next video. (From ep 9: the GitSwarm authors'
own next step is RL on top of a shared notebook, which is this episode's
question from the other side.)

## Extra material (for a long cut or a written companion)

- **How GEPA's loop works, step by step (§3, Alg. 1).** Pick a candidate
  from the Pareto front → pick one module (round-robin) → run on a
  minibatch → collect traces, score and text feedback → a reflection LM
  writes a new instruction → re-run on the same minibatch → if better,
  score on the validation set and add to the pool with its parent
  recorded. *Merge* (App. D.1) combines modules from separate lineages.
  It helped on GPT-4.1 Mini and hurt on Qwen3 8B (Obs. 5).
- **The before/after prompt (Fig. 2).** The seed: "Given the fields
  question, summary_1, produce the fields query." The evolved prompt is a
  page of task-specific rules ("Avoid merely paraphrasing the original
  question…"). It's a great on-screen visual.
- **Prompts transfer across models.** Prompts optimized on Qwen3 8B gave
  +9.00 aggregate on GPT-4.1 Mini, beating optimizers that tuned on
  GPT-4.1 Mini directly (Obs. 6, Table 2).
- **Shorter prompts won.** GEPA prompts were around 33% shorter than
  MIPROv2's (App. I), and higher-scoring optimizers tended to produce
  shorter prompts (Obs. 4). This echoes ep 8's "less harness".
- **Cost.** All GPT-4.1 Mini runs in Table 2 cost under $500. GEPA's share
  was $86 (App. E.3).
- **Against other prompt optimizers:** +12.19 / +13.33 aggregate on GPT-4.1
  Mini against +5.64 for MIPROv2 (Table 2).
- **Inference-time search.** On AMD NPU kernels, mean vector utilization
  went from 4.25% (10 refinements alone) to 30.52% with GEPA. On
  KernelBench CUDA, it went from near 0% to above 20% of tasks faster than
  PyTorch-eager (§5.1). The authors call these early results.
- **Adversarial flip.** GEPA searched for a distracting prompt (trivia
  about honey and the Nile) that cut GPT-5 Mini's AIME-2025 pass@1 from
  76% to 10% (§5.2). It's a vivid warning about how brittle prompts are.
- **Memo paper, the other claims.** (a) Security: once agents write their
  own memory, a one-time prompt injection can persist across sessions.
  The paper cites MINJA at a 98.2% injection success rate. That figure is
  secondhand, quoted in the paper; I didn't read MINJA. (b) The
  brain-science frame: hippocampus (fast notes) against neocortex
  (consolidated during sleep). (c) Their ask: a "consolidation channel"
  from logged experience into weights, gated by provenance, versioned
  checkpoints and regression guards (§5.1). (d) A benchmark idea:
  "Compositional Generalization over Time": does the agent get better at
  novel combinations, with the notes withheld?
- **Ep 2 callback,** from [[2026-09-07 - harness matters]]: "When you
  post-train (especially with RL) inside a specific scaffold, the model
  isn’t learning 'how to do the task.' It’s learning a policy conditioned
  on the context distribution that scaffold produces." That's one more
  reason to try the harness first.
- **The verifier tie-in (ep 7).** GEPA needs a grader, and it needs its
  text, not just its score. From the 9/6 note: "Tasks get solved in
  proportion to how cheap they are to verify." The post-training ladder in
  the same note (continued pretraining → SFT → DPO → RL, with "RL … Use
  when can verify if it’s correct but the path there is unclear or long
  horizon") works as a long-cut explainer.
- **Comprehension debt** (Extended_Brain, via his 6/12 draft notes): "the
  faster the loop ships what you didn't write, the wider the gap between
  what exists and what you understand". Credit Extended_Brain. Link
  [[Post - augmented engineering 101]] and
  [[Post Seed - Automate the Shallows, Protect the Deep Layer]] instead of
  absorbing them (SERIES's instruction).
- **More of Chris's 6/12 voice:** "Recursive self improvement, auto
  research, ai scientists, it’s all the same thing. Same question." / "How
  do we automate the process of improvement."
- **Other usable PVC-retro facts** (Augi-written, generalize): "visibility
  can lie"; the verdict flipped once memory was attributed properly; "When
  the same fix fails twice, the next move is instrumentation or reframing,
  never a third adjacent knob."

## Don't say

- **"GEPA beats RL by 10% on average."** That's the v1 abstract (July
  2025). The current v2 (Feb 2026) says 6%. The table gives +5.94 points.
- **"GEPA beats RL on every task."** GRPO wins AIME-2025 (38.0 vs 32.0).
- **"GEPA beats RL" with no scope.** GRPO was run only on Qwen3 8B, mostly
  with LoRA, at a fixed 24k rollouts. Say "in their tests, on a small open
  model".
- **"Up to 20%"** is the abstract's rounding. The table maximum is +19.0
  (HotpotQA). Use 19.
- **"35x cheaper."** It's 35x fewer *rollouts* on one task (IFBench), not
  35x less compute or money. Reflection calls cost extra.
- **"The memo paper proves agent memory can't learn."** It's a position
  paper with a conditional theorem and no experiments. It also says
  retrieval was the right thing to ship.
- **"I distilled a small model for my Minecraft bot."** Not done. Present
  it as the next experiment.
- **Quoting the PVC retro as Chris's words,** or naming the project. It's
  Augi's distillation of a work agent's retro.
- **Quoting the Langfuse, Extended_Brain or "comprehension debt" lines as
  Chris's.** They're his reading notes on other people's work.
- **The 9/6 lines "They're not successive…" and "The job of swe splits
  three ways…" as Chris's own sentences, until he confirms.** The second
  one says "where you are", which suggests it was written *to* him by an
  agent. Both follow `Aaa:` lines in the note. The other 9/6 lines (the
  model-vs-agents pair, "Prompt a big model first…", "Nothing you
  intend…") read as his.
- Avoid technical detail about Jev's training method. All we have is one
  highlight ("trained via 'Reinforcement Learning for Calibrated
  Decisions'").

## Corrections to SERIES.md

- **"beats GRPO by 6 points on average (up to 19)":** correct against v2.
  Add "on five of six tasks (GRPO wins AIME-2025)", "Qwen3 8B only", and
  that the v1 abstract said 10%, so older blog posts will disagree.
- **"up to 35x fewer rollouts":** correct (IFBench, 678 vs 24,000). Say
  rollouts, not compute.
- **GEPA read status:** now full text. ICLR 2026 oral confirmed.
- **Memo paper:** now read in full (body). Add that it's a position paper
  by Xu, Dai and Zhang (CUHK / Zhejiang), and that its gap claim is
  conditional ("the theorem makes no separation claim" when in-context
  accuracy already reaches the target). The SERIES phrase "because it
  never consolidates into the weights" is fair.
- **Human-in-the-harness quotes:** "Human steering drove every
  architecture pivot" is from an Augi-written note (#ai-generated), not
  Chris's own writing. "Keep manual: reading raw traces yourself" is
  Langfuse's point in his distilled reading notes. Mark both as
  secondhand, not *(Chris)*.
- **Spine quotes:** flag the "They're not successive…" line as "confirm
  authorship" (see Don't say).
- **"If the AugiCraft distillation experiment runs":** it hasn't. There's
  no code or plan doc in the repo yet.

## Sources

- Agrawal et al., *GEPA: Reflective Prompt Evolution Can Outperform
  Reinforcement Learning*, https://arxiv.org/abs/2507.19457 (v2 HTML full
  text: §1–5, Tables 1–3, App. C meta-prompt, E.3 costs; v1 abstract
  checked for the 10% vs 6% change). Contributes the result, the
  mechanism, and the caveats.
- Xu, Dai, Zhang, *Contextual Agentic Memory is a Memo, Not True Memory*,
  https://arxiv.org/abs/2604.27707 (v2 HTML, full body through §8; proofs
  in the appendix skipped). Contributes the counter-argument: the diary
  contrast, the frozen novice, the consolidation channel.
- Raschka, *Language Models for Text Classification: From Bag-of-Words to
  Jev* (Chris's Readwise highlights only, not the article). Contributes
  what Jev is, for the turn.
- `~/repos/augi-craft` (README, `knowledge/learned/validated/`, git log).
  Confirms the skills exist and the distillation experiment doesn't.
- Vault notes, all read in full:
  [[2026-09-06 - Post Training, Loss functions, verifiable]] (Chris, the
  spine) · [[2026-10-11 - LLM Plays Minecraft - AugiCraft]] (his 10/12
  journal; the body is Augi's) ·
  [[Language Models for Text Classification From Bag-of-Words to Jev]]
  (Readwise + his margin notes) · [[2026-06-11 - PVC at work retrospective]]
  (Augi-written) · [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]]
  (his journal draft plus distilled reading notes) ·
  [[2026-09-19 - Agents in my second brain video update]] (Chris) ·
  [[2026-06-12 - Engram and token memory for models]] (Chris) ·
  [[2026-09-07 - harness matters]] (Chris) · [[AMOC - AI Research Engineer]]
  (skimmed: no Jev or distillation content beyond a 10/7 mention of "jeff
  Klein jev idea").
