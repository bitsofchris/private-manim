# Ep 7: The check is the pipe that matters (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 5 web (Wei blog full, LangChain Better-Harness blog full, Chris's published Substack post full, AHE paper full text for the bridge beat, Zechner talk transcript excerpts) + 6 vault notes.
**Question:** What's the most important part of my coding agent setup?
**Who's asking:** An engineer whose agent keeps "finishing" work that isn't right, or keeps circling on an optimization without getting better.
**Answer in one sentence:** The check: an agent can only get as good as the thing that tells it whether it got better, so write the check before you let it loop, and make sure the check measures what you actually care about.
**Search phrase:** evals for ai agents / verifier's law (guess)
**Length:** Short (45–90 s). One idea (the check), one receipt (the data-loader loop), one rule. Extra material goes to the companion, which already exists: Chris's published post "The Anatomy of a Self-Improving Loop" (bitsofchris.com, 14 Jun 2026).

## Hook options

1. "Your agent isn't stuck because it's dumb. It's stuck because nobody told it what 'better' means." (Built from Chris's post; not verbatim.)
2. "A bad gauge is worse than no gauge." (Chris's own sentence, published post.)
3. "Tasks get solved in proportion to how cheap they are to verify." (Chris's own sentence, [[2026-09-06 - Post Training, Loss functions, verifiable]], his paraphrase of Jason Wei. Credit Wei in the next line if used.)

## Key points, in episode order

### 1. AI gets good first at the things that are cheap to check.
- **Say it:** AI researcher Jason Wei called this the verifier's law. The easier a task is to verify, the easier it is to train an AI to do it. Code and math went first because you can run the test.
- **Evidence:** Wei, "Asymmetry of verification and verifier's law," jasonwei.net, 15 Jul 2025 (blog, read in full). His wording: "The ease of training AI to solve a task is proportional to how verifiable the task is. All tasks that are possible to solve and easy to verify will be solved by AI." His five properties of a good verifier: objective truth, fast to verify, scalable to verify, low noise, continuous reward. Note: the live page now headlines it "verifier's **rule**"; the URL slug and 2025 coverage say "law". Either name is fine; credit Wei.
- **Chris's own line:** "Tasks get solved in proportion to how cheap they are to verify" and "Verifiers law." Plus his ladder: "code and math (fully verifiable, moving fastest) → structured extraction and classification (verifiable against labels) → agentic tasks with a checkable end state → open-ended writing and judgment (verifiable only by preference, slowest to improve)." From [[2026-09-06 - Post Training, Loss functions, verifiable]]. The ladder is Chris's extension, not Wei's.
- **Visual:** the blob flows through the pipes and out the end into a gauge. Code and math have a big clear dial; "open-ended writing" has a dial with no needle.

### 2. The same law holds inside your own harness: your agent improves only against a check.
- **Say it:** Wei wrote about training. But your agent loop is the same shape, with no gradient. It tries, it checks, it tries again. If the check is vague, the loop just circles. And you can move a task up the ladder: Wei's point is that you can make verification cheaper by doing work up front, like writing tests with good coverage.
- **Evidence:** Wei: "it is possible to actually improve the asymmetry by front-loading some research about the task… if you have test cases with ample coverage, you can quickly check any given solution; indeed, this is what Leetcode does." Zechner's AI Engineer talk, same idea from the builder side: "If you can give it a function to evaluate how well it did the job, even better." (transcript at 16:25).
- **Chris's own line:** "validation loop to be fast - CC can self correct when you tell it how" from [[Post - augmented engineering 101]] (2025). And from his published post: "build the eval first, hold out cases it never sees, and start where verification is easy."
- **Visual:** a pipe loops from the gauge back to the start of the machine. With a blank gauge the blob goes round and round (circle). With a sharp gauge it spirals upward.

### 3. Receipt: a data-loading loop that circled for weeks until the check was pinned down.
- **Say it:** At work I let a coding agent spend two weeks making a data loader faster and lighter on memory. The goal was "faster with less memory." That sounds like a target. It isn't. Faster than what? Which memory? It only started compounding once I wrote a contract: this config, this many steps, measure these five things, beat the baseline and stay correct.
- **Evidence:** Chris's own experience; published in "The Anatomy of a Self-Improving Loop" (bitsofchris.com, 14 Jun 2026, read in full). Distilled retro: [[2026-06-11 - PVC at work retrospective]] *(Augi; the title has an internal name, never say it aloud)* lists the five missing specs: "faster *than what*, *which* throughput, *which* memory, *what* scale, *what* starting conditions."
- **Chris's own line (published, verbatim):** "'Faster with less memory at this scale' sounds like a target. It isn't. Faster than what, from what baseline? The loop only started compounding once I wrote an experiment contract: this config, this model, this many steps, this data mix; measure these five things; beat the baseline while holding correctness. That contract should have been step zero." Also from [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]] (6/11): "Clear objective to improve against".
- **Visual:** a gauge labeled "better?" with no units, then the same gauge relabeled with five small dials and a baseline line.

### 4. The twist: the check can lie.
- **Say it:** Early on, the new approach looked terrible on memory. Then I fixed how memory was measured. Most of it was cache the system could give back. Same numbers, opposite verdict. So owning the check also means checking the check.
- **Evidence:** Chris's published post and the retro note (gauge misread: "much of it was reclaimable cache, while the incumbent's smaller-looking footprint was non-reclaimable. The verdict *flipped*"). Same pattern at research scale in AHE (ep 8): the most common failure its trace analysis found was "proxy validation instead of evaluator-isomorphic validation": the agent checked row counts or "file exists" instead of what the grader actually checked (AHE paper, Appendix C.1.1, full text).
- **Chris's own line (published, verbatim):** "A bad gauge is worse than no gauge. It can lead the loop to optimize confidently in the wrong direction." And: "Spend your human time setting up eval but also reviewing how you are measuring success."
- **Visual:** two gauges reading the same dial differently (the doodle from his post). The pipe arrow flips direction.

### 5. Agents grade themselves too easily, and they cheat if they can.
- **Say it:** Left alone, a model takes its first plausible answer and calls it done. Push it to run the real check. And once it is optimizing a number, it will game the number if it can. So keep some test cases the loop never sees, and look at the changes yourself.
- **Evidence:** LangChain, "Improving Deep Agents With Harness Engineering" (Readwise highlights only): "Models are biased towards their first plausible solution. Prompt them aggressively to verify their work by running tests and refining solutions." LangChain, "Better Harness: A Recipe for Harness Hill-Climbing with Evals," Vivek Trivedy, 8 Apr 2026 (blog, read in full): "agents are famous cheaters"; split evals into an optimization set and a holdout set; run a baseline first; "one change at a time to avoid confounding"; human review as a "gate against overfitting"; evals are "the 'training data' for harness engineering."
- **Chris's own line:** "We want loops and improvement not optimization. Optimization can lead to reward hacking." From [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]].
- **Visual:** the blob reaches into the gauge and nudges the needle. A second, covered gauge (the holdout) doesn't move.

### 6. Whoever owns the check owns the loop.
- **Say it:** Writing code is getting cheap. Writing the check is the skill that carries over: the test, the eval, the label set. Whoever writes it decides where the loop goes.
- **Evidence:** Chris's synthesis; consistent with Wei ("virtually anything that can be measured can be optimized") and Better-Harness ("tracing and maintaining good evals is what makes this system work in practice").
- **Chris's own line:** "The common skill across all three is building the verifier: the eval, the test, the label set. Whoever owns that owns the loop" from [[2026-09-06 - Post Training, Loss functions, verifiable]]. Published closer: "You decide what 'better' means." (Anatomy post.)
- **Visual:** zoom out to the full pipe machine; a hand holds the gauge at the end. That gauge is the pipe the whole machine flows toward.

## The takeaway

Before your next long agent task, write a short contract in the repo: the baseline, the exact command that checks the result, and the numbers that count as "better". Give the agent that command. When the same idea fails twice, add a gauge or reframe the problem instead of turning another knob.

## Bridge

Once the check exists, the agent can use it on something bigger than your code: its own harness (ep 8).

## Extra material (for a long cut or a written companion)

- **Wei's other good bits.** Some tasks are harder to check than to do: fact-checking an essay vs writing it (Brandolini's law). AlphaEvolve as "a very clever instantiation of guess-and-check." "We will likely have a jagged edge of intelligence, where AI is much smarter at verifiable tasks." Good for a longer cut on why agents feel brilliant at some tasks and useless at others.
- **The fails-twice rule.** Chris's published version: "when a hypothesis fails twice, add a gauge or reframe the problem." Retro version: "When the same fix fails twice, the next move is instrumentation or reframing, never a third adjacent knob."
- **Errors find problems, not fixes.** Retro: "Crashes proved a risk was real but never identified the design fix."
- **Better-Harness details.** Sources for evals: hand-curated, production traces ("A trace where a user corrected the agent is even better"), adapted external datasets. Tag evals by behavior. Passing evals become regression tests; prune saturated ones ("spring cleaning of evals is good!"). Their example learned instructions: "Use reasonable defaults when the request clearly implies them," "Do not ask for details the user already supplied." A research version of the scaffold is open source.
- **AHE's verification-shaped fixes** (bridge material for ep 8). The evolved harness kept adding checks: a finish-hook that forces "one evaluator-isomorphic closure check," and a shell guard that stops the agent deleting its own verified output during "cleanup." In the loop itself, the verifier was read-only to the evolving agent, so it couldn't win by editing the test. That is "whoever owns the check" made literal.
- **Recursive's evaluator arms race** (from Chris's post): as the search got stronger, the correctness audit had to get stronger too. Not re-read for this pass; cite via his post.
- **The Software 1.0/2.0/3.0 split** from the 9/6 note belongs to ep 10, not here.

## Don't say

- "Jason Wei coined 'tasks get solved in proportion to how cheap they are to verify'." That sentence is Chris's paraphrase. Wei's wording is about how easy it is to *train* AI on a task. Say "Jason Wei calls it the verifier's law" and paraphrase.
- The ladder (code → extraction → agentic → writing) as Wei's. It's Chris's.
- "The verifier's law proves your harness…" Wei wrote about RL training. Applying it to agent loops is the episode's argument, so say it as "the same idea".
- The internal name of the data format or anything about colleagues. Say "a data loader at work."
- Wei's employer. It wasn't checked for this pass; "AI researcher Jason Wei" is enough.
- "Better-Harness moved Terminal-Bench 52.8% → 66.5%." That figure is from a third-party summary citing a different LangChain post. It isn't in the Better-Harness post. It's ep 2 territory anyway.
- That the agent "made real progress then got stuck" in ways that sound like the agent failed at coding. The retro's point is the opposite: "the stuck points weren't coding failures. They were loop failures."

## Corrections to SERIES.md

- **Verifier's law origin:** credit Jason Wei, "Asymmetry of verification and verifier's law," jasonwei.net, 15 Jul 2025. The SERIES quote "Tasks get solved in proportion to how cheap they are to verify" is Chris's paraphrase, not Wei's wording. The live page now titles it "verifier's rule".
- **PVC receipt quote:** "The loop only started compounding once a benchmark contract pinned down exactly what 'better' meant" is Augi's distillation, not Chris's words. Chris's published wording is "The loop only started compounding once I wrote an experiment contract…". Use that for VO.
- **"Learn first: nothing new to read":** mostly true, but the story is already public. Chris published it on 14 Jun 2026 in "The Anatomy of a Self-Improving Loop" (bitsofchris.com/p/the-anatomy-of-a-self-improving-loop), generalized as "a data loader for our foundation model." That post is the companion and the best VO source.
- **LangChain Better-Harness:** confirmed: "Better Harness: A Recipe for Harness Hill-Climbing with Evals," Vivek Trivedy, LangChain blog, 8 Apr 2026. "Agents are famous cheaters", holdout sets, one change per iteration and the human review gate are all in the post.

## Sources

- Jason Wei, [Asymmetry of verification and verifier's law](https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law), 15 Jul 2025. Read: full. Contributes: the origin and exact wording of the law, five properties of a good verifier, and "you can improve the asymmetry by front-loading work" (tests).
- LangChain (Vivek Trivedy), [Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://blog.langchain.com/better-harness-a-recipe-for-harness-hill-climbing-with-evals), 8 Apr 2026. Read: full. Contributes: evals as training data, holdouts, "agents are famous cheaters", the human gate.
- Chris Lettieri, [The Anatomy of a Self-Improving Loop](https://bitsofchris.com/p/the-anatomy-of-a-self-improving-loop), 14 Jun 2026. Read: full. Contributes: the receipt in his own published words ("A bad gauge is worse than no gauge", the contract, fails-twice).
- Lin et al., [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850) (arXiv 2604.25850v4). Read: full text (HTML). Contributes: "proxy validation" as the top failure, and the read-only verifier (bridge to ep 8).
- Mario Zechner, [Building pi in a World of Slop](https://ai.engineer/talks/RjfbvDXpFls-pi-coding-agent), AI Engineer Europe 2026. Read: transcript excerpts. Contributes: "If you can give it a function to evaluate how well it did the job, even better."
- LangChain (Viv), Improving Deep Agents With Harness Engineering (X article). Read: Chris's Readwise highlights only. Contributes: "Models are biased towards their first plausible solution."

**Vault notes used:** [[2026-09-06 - Post Training, Loss functions, verifiable]] *(Chris)* · [[2026-06-11 - PVC at work retrospective]] *(Augi; work, generalized)* · [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]] *(Chris)* · [[2026-06-12 - Draft - Self-Improving Loops and AutoResearch]] *(Chris)* · [[Post - augmented engineering 101]] *(Chris)* · [[Improving Deep Agents With Harness Engineering]] *(Readwise)*.
