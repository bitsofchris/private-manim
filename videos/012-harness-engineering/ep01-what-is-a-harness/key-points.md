# Ep 1: What is an agent harness? (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 7 primary (OpenAI post in full, Böckeler, Guo, Hashimoto, LangChain "Anatomy", LangChain "Improving Deep Agents", marmelab), plus 1 paper abstract reused from ep 2 (Lewis), plus 8 vault notes.
**Question:** what is an agent harness / what does "harness engineering" mean?
**Who's asking:** an engineer who uses Claude Code or Codex daily, keeps hearing "harness" on X and in blog posts, and wants a crisp definition plus why it matters to them.
**Answer in one sentence:** the harness is everything in an agent that isn't the model, and it has four parts: context (what it sees), tools (what it can do), memory (what carries over), and the loop (runs it, checks the work, decides when to stop).
**Search phrase:** "what is an agent harness" / "harness engineering explained" (guess) **Superseded:** checked against autocomplete 2026-10-17; the checked phrase and title are in `SCRIPTS.md`.
**Length:** Short. Revised 2026-10-17 (Chris): the Short is the definition, the four parts, one worked example of them together, and why it matters. Hashimoto's rule, the OpenAI receipt and "Agent = Model + Harness" (points 3–5 below) go to the companion.

## The four parts (the taxonomy)

There is no official taxonomy; write-ups list 4 to 12 parts (Cloudzy 9, a DEV post 12, a readthedocs survey 6). The sources worth citing come down to four:

| Part | What it is | Sources |
|---|---|---|
| Context | what goes into the model this turn: instructions, system prompt, retrieved files, the last tool result | Lewis "decides what the model sees"; Anthropic "retrieval"; LangChain system prompts, compaction, tool-call offloading |
| Tools | what it can act on: file ops, bash, browser, search; the model emits a call, the harness runs it | Anthropic "tools"; Lewis "which tools it can use"; LangChain bash, sandbox, filesystem |
| Memory | what survives the session and is loaded back: AGENTS.md, notes, files, git | Anthropic "memory"; LangChain "memory file standards like AGENTS.md"; Chris "state (memory)" |
| The loop | call model → run tool → feed result back → check → continue or stop | Anthropic "LLMs using tools based on environmental feedback in a loop", "stopping conditions", "ground truth from the environment at each step"; Lewis "how the work continues"; LangChain Ralph loops, self-verification |

Where the longer lists fit: prompts and retrieval are context; guardrails and permissions are tools; checks, hooks and stop conditions are the loop; subagents are a loop calling a loop.

Sources: Anthropic, [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents), 19 Dec 2024 (fetched 10/17); LangChain, The Anatomy of an Agent Harness (fetched 10/17); Lewis (below); Chris, [[2026-09-07 - harness matters]].

## Hook options

1. "Two people use the same model. One gets slop, one ships a million lines of code. The difference isn't the model. It's the harness." (Built on OpenAI's numbers, point 4.)
2. "Your AI isn't generic because the model is dumb. It's generic because you're poking a blob." (Built on the idea.md image, Chris's framing.)
3. "Code used to be our leverage - now its setting up, steering, managing, and connecting agents." (**Chris's own sentence**, [[New Programming Language is Agent Orchestration]], 1/19. Typo "its" is his; fix only in on-screen text if wanted.)

## Key points, in episode order

### 1. An agent is a model plus a harness, and the harness is everything that isn't the model.
- **Say it:** The model is a big blob of intelligence. On its own it can only answer what's in front of it. The harness is all the code around it: what it gets to see, what it remembers, what tools it can call, and what happens after it answers.
- **Evidence:** LangChain (Vivek Trivedy, "The Anatomy of an Agent Harness", 10 Mar 2026): "Agent = Model + Harness" and "If you're not the model, you're the harness." Also: "A harness is every piece of code, configuration, and execution logic that isn't the model itself." (blog, read via fetch). Böckeler's current article credits the formula to this LangChain post. Lewis (arXiv 2608.26218, abstract and full text, read for ep 2) gives the cleanest one-liner: a harness "decides what the model sees, which tools it can use, and how the work continues."
- **Chris's own line:** "Harness is: Context, state (memory), tools, prompts" from [[2026-09-07 - harness matters]]. (Verbatim in the note: "Harness is:\nContext, state (memory), tools, prompts".)
- **Visual:** the blob alone, then a thin outline labelled "harness" drawn around it. Label the blob "model (weights)" and everything outside it "harness".

### 2. The harness has a handful of parts, and each one is a pipe.
- **Say it:** Context is what goes in. Memory is what carries over between runs. Tools are what the model can reach out and touch. The loop is the part that checks the work and decides: try again, or stop. Each one is a pipe the blob flows through.
- **Evidence:** LangChain "Anatomy" names instruction prompts; tools, skills and MCP servers; built-in infrastructure (file storage, sandboxes, browsers); orchestration (subagents, handoffs, model routing); and hooks/middleware for "context compaction, continuation, and lint checks" (blog). LangChain's Feb post lists the knobs: "system prompts, tools, hooks/middleware, skills, sub-agent delegation, memory systems, and more" (blog, and Chris's Readwise highlight).
- **Chris's own line:** his margin note on that knob list: "Basically what I'm building with open augi Cli right now?" from [[Improving Deep Agents With Harness Engineering]]. Also "I'm building a personal agent harness." from [[2026-02-21 - AE3 - Issue 3]].
- **Visual:** the four idea.md stages compressed: poke (fuzzy blob out), prompt + context (some shape), memory (sharper), then the pipe maze, with each pipe labelled context / memory / tools / check-and-stop.

### 3. "Harness engineering" is one rule: every time the agent makes a mistake, you fix the machine so it never makes that mistake again.
- **Say it:** You don't argue with the agent. When it gets something wrong, you ask what was missing (a doc, a tool, a check) and you add it to the repo. The fix stays. Next run, that mistake is gone.
- **Evidence:** Mitchell Hashimoto, "My AI Adoption Journey", 5 Feb 2026, "Step 5: Engineer the Harness": "I've grown to calling this 'harness engineering.' It is the idea that anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again." His receipt: an AGENTS.md in Ghostty where "Each line in that file is based on a bad agent behavior, and it almost completely resolved them all." (blog, read via fetch). OpenAI says the same: "When the agent struggles, we treat it as a signal: identify what is missing—tools, guardrails, documentation—and feed it back into the repository, always by having Codex itself write the fix." (full post).
- **Chris's own line:** his margin note on that OpenAI sentence: "Like last week - compounding teams, tool helping tool get better" from [[Harness Engineering]] (Readwise). And on Guo's AGENTS.md advice: "Continually improve, habit of experimeting" from [[The Emerging Harness Engineering Playbook]] (typo his).
- **Visual:** the agent's output hits a wall (a red X). A new pipe segment snaps into the maze at that spot. The next particle flows through cleanly.

### 4. The receipt: OpenAI built a product with zero hand-written code, and the hard part was the harness, not the model.
- **Say it:** An OpenAI team spent five months shipping an internal product where no human wrote a line of code. About a million lines, about 1,500 merged PRs, three engineers to start. They said early progress was slow, and not because the model couldn't code. The environment was underspecified.
- **Evidence:** Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 11 Feb 2026 (full post read in a browser): "0 lines of manually-written code"; "on the order of a million lines of code"; "roughly 1,500 pull requests ... with a small team of just three engineers driving Codex", "3.5 PRs per engineer per day", team "now seven engineers"; "We estimate that we built this in about 1/10th the time" (their estimate, not measured). Key line: "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified." And: "Humans steer. Agents execute."
- **Chris's own line:** "Code used to be our leverage - now its setting up, steering, managing, and connecting agents." from [[New Programming Language is Agent Orchestration]].
- **Visual:** a counter ticking up lines of code while a human hand only ever touches the pipes, never the output.

### 5. The job moves from writing code to building the machine the code comes out of.
- **Say it:** The skill isn't prompting harder. It's designing what the model sees, what it can touch, and how its work gets checked. That's harness engineering, and it's what the rest of this series builds, one pipe at a time.
- **Evidence:** OpenAI closes: "building software still demands discipline, but the discipline shows up more in the scaffolding rather than the code" and "Our most difficult challenges now center on designing environments, feedback loops, and control systems" (full post). Guo: "the bottleneck was never the agent's ability to write code, but rather the lack of structure, tools, and feedback mechanisms surrounding it." (Chris's Readwise highlight, paraphrasing OpenAI.)
- **Chris's own line:** "I'm moving away from chatting with AIs and moving towards managing them" is Guo's, not Chris's (it's in his highlights). For Chris, reuse the point-4 line or none.
- **Visual:** pull back to the full pipe maze with the blob flowing through it and a sharp shape coming out. This is the series' master shot.

## The takeaway

Short (10/17): when your agent fails, don't blame the model first; ask which piece was missing: the context, a tool, the memory, or the check.

Companion: Next time your agent gets something wrong, don't just correct it in chat. Ask "what was missing?" and add one line, one script, or one check to the repo so it can't make that mistake again. Keep an AGENTS.md where every line traces back to a real failure, like Hashimoto's.

## Bridge

"Those are the four parts. Next: how to build yours, starting with your repo. That's Harness 101." (Ep 2 was dropped 10/17.)

## Extra material (for a long cut or a written companion)

- **Who named it.** The earliest use of the phrase I could find and read is Hashimoto, 5 Feb 2026: "I've grown to calling this 'harness engineering.'" He doesn't say he invented it, and he says he doesn't know if the industry has a name yet. Six days later, 11 Feb, OpenAI's Lopopolo post put "Harness engineering" in its title, and that's what spread it. LangChain's Trivedy published "Improving Deep Agents with harness engineering" on 17 Feb. Guo (22 Feb) credits Hashimoto with the name and writes "There isn't an official term for this yet." Marmelab (Sep 2026) calls the OpenAI post "The text that named the discipline", which the dates contradict. Safe line: "Mitchell Hashimoto named it in early February 2026, and an OpenAI post made it famous a week later." Don't say "coined".
- **Map, not manual** (good for ep 3/4, cut from ep 1): OpenAI tried "one big AGENTS.md" and it failed: "Context is a scarce resource ... Too much guidance becomes non-guidance ... It rots instantly ... It's hard to verify." They switched to a roughly 100-line AGENTS.md as "the table of contents", pointing into a structured `docs/` folder, checked by linters and a recurring "doc-gardening" agent. Line: "give Codex a map, not a 1,000-page instruction manual."
- **"From the agent's point of view, anything it can't access in-context while running effectively doesn't exist."** (OpenAI). Strong line for ep 2 or ep 4.
- **Custom lints as teaching:** "Because the lints are custom, we write the error messages to inject remediation instructions into agent context." (OpenAI). Good for ep 7.
- **Garbage collection:** the team "used to spend every Friday (20% of the week) cleaning up 'AI slop'", then encoded "golden principles" and background Codex tasks that open cleanup PRs, "Most of these can be reviewed in under a minute and automerged." (OpenAI). Good for ep 3b, the janitor.
- **Böckeler's newer framing** (2 Apr 2026, supersedes her Feb memo at the same URL): harness controls are *guides* ("anticipate the agent's behaviour and aim to steer it before it acts") and *sensors* ("observe after the agent acts and help it self-correct"), each either *computational* (deterministic, CPU) or *inferential* (LLM judge). She also pictures "harness templates" teams pick per tech stack. Her Feb memo's three groups (context engineering, architectural constraints, garbage collection) are the ones Chris highlighted; the live page no longer shows them.
- **Marmelab's state-of report** (Zaninotto, 24 Sep 2026; he builds harnesses, disclosed): of 97 open-source harnesses big enough to test, "60%" have neither a test nor an eval. Good for ep 7. Its other numbers are mostly secondhand; check before use.
- **Stripe Minions** (via Guo): over a thousand merged PRs a week, 400+ internal tools via MCP. Belongs to ep 3.

## Don't say

- **"OpenAI says the model is the engine and the harness is the chassis."** The car analogy is not in the OpenAI post. It's in Chris's vault summary [[OpenAI - Harness Engineering]], which cites a Medium post by Aakash Gupta. If you use the image, own it as yours, or drop it. The blob and pipes is the series image anyway.
- **"Hashimoto coined the term"** or **"OpenAI coined the term."** Unverified. Say "named it" (Hashimoto) and "made it famous" (OpenAI).
- **"10x faster."** OpenAI wrote "We estimate that we built this in about 1/10th the time." It's their estimate. If used, say "they estimate".
- **"Three engineers built a million lines."** It started with three and grew to seven. Say "a small team, starting with three".
- **Anything from the vault summary [[OpenAI - Harness Engineering]] as an OpenAI quote.** It's a ChatGPT summary citing LinkedIn, Medium and parallel.ai posts mixed with the real post.

## Corrections to SERIES.md

1. Ep 1 "Definitions to choose from": the car analogy is attributed to [[OpenAI - Harness Engineering]] "(vault summary)". It isn't in the OpenAI post; it comes from a Medium post that summary cites. Mark it as not OpenAI's.
2. Ep 1 sources: the OpenAI post is by Ryan Lopopolo, dated 11 Feb 2026. Read: full (it can now be marked full, not "vault summary").
3. Ep 1 sources: the Böckeler URL now serves a rewritten article dated 2 Apr 2026, "Harness engineering for coding agent users", which supersedes the Feb memo Chris highlighted. Its categories are now maintainability / architecture fitness / behaviour, framed as guides and sensors. The three groups SERIES.md ep 3 quotes ("as Böckeler groups them": knowledge base, constraints, garbage collection) are from the superseded Feb memo. Still fine to use, but say "Böckeler's February memo".
4. "Who coined the term": settled as far as it can be. Hashimoto, 5 Feb 2026, "I've grown to calling this 'harness engineering'" is the earliest use found. OpenAI's post (11 Feb) popularized it. Guo credits Hashimoto with the name and says there's no official term. Use "named", not "coined".
5. "Agent = Model + Harness" comes from LangChain's "The Anatomy of an Agent Harness" (Trivedy, 10 Mar 2026). Marmelab credits it to Böckeler, but Böckeler herself links it to LangChain.
6. The marmelab source can move from "read: search" to "read: blog (fetched summary)".

## Sources

- OpenAI, Ryan Lopopolo, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), 11 Feb 2026. **Full** (read in a browser; WebFetch is blocked). Gives the receipt: zero hand-written code, about 1M lines, about 1,500 PRs, the "environment was underspecified" line, and the "what is missing" rule.
- Mitchell Hashimoto, [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey), 5 Feb 2026. **Blog, the relevant section** (via fetch). The name and the one-line rule, plus the Ghostty AGENTS.md receipt.
- LangChain, Vivek Trivedy, [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness), 10 Mar 2026. **Blog** (via fetch). The definition "Agent = Model + Harness" and the component list.
- LangChain, Vivek Trivedy, [Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering), 17 Feb 2026. **Blog** (via fetch). The knob list; its numbers are used in ep 2.
- Birgitta Böckeler, [Harness engineering for coding agent users](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html), 2 Apr 2026 (supersedes the Feb memo). **Blog** (via fetch) plus Chris's highlights of the Feb memo. Gives the guides/sensors framing and the "Codex itself write the fix" quote.
- Charlie Guo, [The Emerging "Harness Engineering" Playbook](https://www.ignorance.ai/p/the-emerging-harness-engineering), 22 Feb 2026. **Blog** (via fetch) plus highlights. Gives the definition "constraints, tools, documentation, and feedback loops" and the naming credit to Hashimoto.
- François Zaninotto, [The State Of AI Harness Engineering 2026](https://marmelab.com/blog/2026/09/24/the-state-of-ai-harness-engineering-2026.html), marmelab, 24 Sep 2026. **Blog** (via fetch summary). Gives the "60% have no test or eval" audit, used in the extra material only.
- Lewis, [Same Model, Different Harness](https://arxiv.org/abs/2608.26218). **Full** (read for ep 2). Gives the one-sentence definition of a harness.
- Vault notes: [[2026-09-07 - harness matters]] (Chris), [[New Programming Language is Agent Orchestration]] (Chris), [[2026-02-21 - AE3 - Issue 3]] (Chris), [[Post - Harness Engineering 101]] (Chris, a stub: "Claude thread on this"), [[OpenAI - Harness Engineering]] (ChatGPT summary, treat with care), [[The Emerging Harness Engineering Playbook]] (Readwise), [[Improving Deep Agents With Harness Engineering]] (Readwise), [[Harness Engineering]] (Readwise, Böckeler). Plus `ep01-what-is-a-harness/idea.md` for the image.
