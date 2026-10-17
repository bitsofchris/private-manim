# Ep 3: Harness 101: build your own (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 4 primary in full (OpenAI post, Böckeler's current article, Guo, Hashimoto's "Engineer the Harness" section), 4 repo files (`AGENTS.md`, `agents/runbook.md` step 11, `agents/changelog.md`, `agents/plans/agentic-kb-shorts.md`), 12 vault notes.

**Ruled 2026-10-16 (Chris):** the 3/3 "just notes / files are the layer" line and the 9/6 "They're not successive…" and "The job of swe splits three ways…" lines are **not his words**. They're pasted AI replies. Use the ideas, never as VO or as "Chris's own line".

**Question:** how do I set up my repo so Claude Code / Codex does good work in it?
**Who's asking:** an engineer who uses a coding agent daily and keeps correcting the same mistakes in chat.
**Answer in one sentence:** Give the agent a short map of the repo, checks that tell it when it's wrong and how to fix it, and a cleanup pass. Every time it fails, have it write the fix into the repo.
**Search phrase:** AGENTS.md best practices / how to set up AGENTS.md (guess; "AGENTS.md" is also Short D's guess) **Superseded:** checked against autocomplete 2026-10-17; the checked phrase and title are in `SCRIPTS.md`.
**Length:** Short + companion. The core (points 1, 2, 4, 6) fits about 75–90 s. Points 3 and 5 hand off to eps 4 and 3b, so the Short can name them in one line each. The D material (point 6) is the part that might push it past 90 s.

**Overlap with ep 1.** Ep 1's key points already use Hashimoto's rule ("anytime you find an agent makes a mistake…"), the OpenAI receipt (zero hand-written code), and the takeaway "ask what was missing and add a line, a script or a check." Ep 3 shouldn't re-explain that. Open on the rule in one line as the thing ep 1 promised, then spend the episode on *what you actually build*.


## The Short, as rewritten 2026-10-17 (Chris)

Rebuilt from Chris's own notes using his writing guidance (content-preflight, notes-to-post, effective-writing). Where this block and the points below disagree, this block wins for the Short; the points below are companion material. Script: `SCRIPTS.md`.

- **Question:** How do I set up my repo so Claude Code stops making the same mistakes?
- **Answer:** "Have good primitives, then let the agents do things" (Chris, [[2026-06-02 - Good Primitives]]): everything is a file, small tools chained together, checks.
- **What the viewer does after:** Next time you type the same correction twice, turn it into a file, a tool, or a check.
- **Built from:** Chris's primitives line and his 1/21 Unix-philosophy note; this repo as the receipt (AGENTS.md map, `tools/` CLIs, the font-bug rule). OpenAI's "underspecified" framing, Böckeler's groups and Hashimoto go to the companion.

## Hook options

1. "Your agent isn't the problem. Your repo is underspecified." This adapts OpenAI's own line: "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified." (Not Chris's sentence.)
2. "OpenAI's team spent every Friday cleaning up after their agents. Then they built the cleanup into the repo." (Fact from the OpenAI post: "Our team used to spend every Friday (20% of the week) cleaning up 'AI slop.'" Not Chris's sentence.)
3. "Have good primitives and then let the agents do things." This is **Chris's own sentence**, from [[2026-06-02 - Good Primitives]]. It works better as the answer line than the first line.

## Key points, in episode order

### 1. When the agent fails, the fix goes in the repo, not the chat.
- **Say it:** Ep 1 gave you the rule. Here's what it means day to day. When the agent gets something wrong, don't retype the correction. Ask what was missing (a doc, a tool, a check), add it to the repo, and have the agent write it.
- **Evidence:** OpenAI: "When something failed, the fix was almost never 'try harder.'" Engineers asked "what capability is missing, and how do we make it both legible and enforceable for the agent?" And "always by having Codex itself write the fix." (Lopopolo, OpenAI, 11 Feb 2026; full text.) Hashimoto names two kinds of fix: "Better implicit prompting (AGENTS.md)" and "Actual, programmed tools. For example, scripts to take screenshots, run filtered tests." (5 Feb 2026; section read in full.)
- **Chris's own line:** "feel the friction, experiment or add the improvement with toolinf" ([[2026-02-21 - AE3 - Issue 3]], 2/27 entry, typo as written). Also his margin note on Böckeler's "Codex itself write the fix" highlight: "Like last week - compounding teams, tool helping tool get better" ([[Harness Engineering]], Readwise).
- **Visual:** the blob hits a kink in a pipe and sputters. Instead of the blob being shaken, a hand adds a new pipe segment, and the blob is the one holding the wrench.

### 2. A harness has two directions: guides before the agent acts, and sensors after.
- **Say it:** Guides steer the agent before it writes anything: your AGENTS.md, your docs, your skills. Sensors catch it after: tests, linters, type checks, a review agent. You need both. With only guides, the agent never finds out its rules failed. With only sensors, it keeps making the same mistake.
- **Evidence:** Böckeler, "Harness engineering for coding agent users" (martinfowler.com, 2 Apr 2026; full text). Guides are "feedforward controls" that "anticipate the agent's behaviour and aim to steer it before it acts". Sensors are "feedback controls" that "observe after the agent acts and help it self-correct". "Separately, you get either an agent that keeps repeating the same mistakes (feedback-only) or an agent that encodes rules but never finds out whether they worked (feed-forward-only)." Each can be *computational* (deterministic: tests, linters) or *inferential* (an LLM judge). Run the cheap computational ones on every change.
- **Chris's own line:** none fits directly. The closest is "validation loop to be fast - CC can self correct when you tell it how" from [[Post - augmented engineering 101]] (quoted in SERIES.md ep 7; I didn't reopen that note). Save it for ep 7 if it fits better there.
- **Visual:** a funnel *before* the blob enters the pipes (guide), and a gauge *after* it leaves them, with a thin return pipe looping back (sensor).

### 3. Put the knowledge in the repo, and keep AGENTS.md a table of contents.
- **Say it:** If it's not in the repo, the agent can't see it. The Slack thread, the design call, what's in your head: none of it exists for the agent. So write it into versioned docs, and keep AGENTS.md short: a map that points to them, not a manual. Ep 4 is the whole story on why.
- **Evidence:** OpenAI: "From the agent's point of view, anything it can't access in-context while running effectively doesn't exist." "give Codex a map, not a 1,000-page instruction manual." "A short AGENTS.md (roughly 100 lines) is injected into context and serves primarily as a map, with pointers to deeper sources of truth." (Full text.) Guo's version: "a small AGENTS.md that pointed to deeper sources of truth - design docs, architecture maps, execution plans, quality grades." (Full text.)
- **Chris's own line:** "Have good primitives and then let the agents do things. Like having a repo knowledge base or context base." ([[2026-06-02 - Good Primitives]]). His margin note on Guo's "small AGENTS.md" highlight: "My docs folder" ([[The Emerging Harness Engineering Playbook]]). Optional work line, generalized: "Context is stored. Intent is all you review and discuss with the agent. Not the code" ([[PMOC - AutoDataEng - Loops and Recursive Self Improvement]], 6/11; it's a design for a repo at work, so say "at work, a data repo…").
- **Visual:** a small signpost at the mouth of the pipe maze, with arrows pointing down side pipes. Keep it to a beat, because ep 4 owns the map.

### 4. Turn your rules into checks, and write the error message as the fix.
- **Say it:** A rule in a doc is a suggestion. A rule in a linter is a wall. And if you write the linter's error message as an instruction ("move this import to the service layer"), every failure teaches the agent the fix. Once it's encoded, the rule applies everywhere at once.
- **Evidence:** OpenAI: "By enforcing invariants, not micromanaging implementations, we let agents ship fast." "Because the lints are custom, we write the error messages to inject remediation instructions into agent context." "With agents, they become multipliers: once encoded, they apply everywhere at once." "When documentation falls short, we promote the rule into code." (Full text.) Böckeler calls these messages "a positive kind of prompt injection". Guo calls the remediation-message lint "the cleverest idea in any of these writeups". (Both full text.)
- **Chris's own line:** none.
- **Visual:** a pipe wall with a small printed label. When the blob bumps it, the label lights and the blob reroutes down the right pipe.

### 5. Agents copy what's already there, so something has to clean up on a schedule.
- **Say it:** Your agent copies the patterns in your repo, bad ones included. So the mess grows. OpenAI's team spent every Friday cleaning it up by hand, and that didn't scale. So they wrote down a few golden rules and gave background agents the job of finding drift and opening small cleanup PRs. That's a janitor, and it gets its own episode (3b).
- **Evidence:** OpenAI: "Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones." "Our team used to spend every Friday (20% of the week) cleaning up 'AI slop.' Unsurprisingly, that didn't scale." They encoded "golden principles" and run "background Codex tasks that scan for deviations, update quality grades, and open targeted refactoring pull requests. Most of these can be reviewed in under a minute and automerged." A "doc-gardening" agent does the same for stale docs. (Full text.) Böckeler mentions Thoughtworks teams using a "janitor army". (Full text.)
- **Chris's own line:** "Also the janitor for agents to de dupe and have fewer things to maintain." (9/13, quoted in [[What Works - Running a Second Brain With Agents]].) And from the 10/2 note: "As you iterate and change the system, something has to keep it clean" ([[2026-10-02 - 4 rules for agentic knowledge bases]]). That second line is 3b's beat 1, so use it here only if 3b gets cut.
- **Visual:** sludge building up along the pipe walls. A small janitor figure walks the pipes with a broom. (This is the bridge into 3b's janitor on the building set.)

### 6. [From Short D] The same four layers work in any repo. Here's mine.
*Everything in this point is Short D's material, tried inside ep 3 as agreed on 10/13. Chris decides at script time what stays.*
- **Say it:** I run this repo, the one that makes these videos, the same way. AGENTS.md is the map and the rules. One folder holds what the agents maintain. A changelog records every rule change and the video that forced it. After every Short there's an update pass: the agent mines the session for every correction I made, writes each one into its one home, and cleans up duplicates. The repo gets better every time I use it.
- **Evidence (the repo, read 2026-10-16):**
  - `AGENTS.md` is 132 lines. It's "the single entry point: the map, the rules of precedence, how a session runs, and how the repo stays clean." `CLAUDE.md` only says "Read `AGENTS.md` first." That's OpenAI's "about 100 lines, a map" pattern at nearly the same size.
  - It has a map table ("You want / Go to / Owns"), eight hard rules, a precedence order for when files disagree, and janitor rules: "One home per topic… Never state the same rule in two files. Link instead."
  - `agents/runbook.md` step 11, the update pass: "List every change Chris asked for and every workaround or wish an agent reported. For each, decide: rule…, token…, part…, tool…, or nothing. Make the edits in their one home." Then a janitor step, then "One line per change in `agents/changelog.md`, with the video that forced it."
  - `agents/changelog.md` has 72 lines from 10/1 to 10/11. 17 are tagged as Chris's request and 8 as janitor fixes.
  - A Hashimoto-style line: "Beat brief trap: monospace set in the HTML (CSS class, ep01; inline `style` attribute, ep03) rendered in Inter; set `el.style.fontFamily` from the script." The same mistake happened twice, so it became a rule.
  - A janitor catch: "Hero rule, janitor: `AGENTS.md` rule 2 is the one home…; `agents/style.md`, `agents/animation-rules.md` rule 12 and the HyperFrames brief said 'per beat' and now point to it." Four files disagreed, and the pass resolved them to one. This is exactly the 10/2 note's "It catches conflicting rule sets before they spread."
  - Mapped onto the four layers (**my mapping, not Chris's words; he should confirm**). Curated layer: `AGENTS.md` and `agents/` (rules, map, style), kept small and edited with care. Agent layer: each video folder's working files (storyboard, transcripts, `words.json`, contact sheets) plus `agents/research/`. Human layer: `README.md` ("`README.md` is for humans", per the changelog) and the hand-off pack at runbook step 10. Janitor: runbook step 11 plus the "Keeping the system clean" section.
- **Chris's own line:** "Entrypoint in private-manim is now the AGENTS.md. Turned it into a self-improving repo." ([[PMOC - Shorts Augi Shorts - Augi content system]], 10/3). "Merging these [[2026-10-02 - 4 rules for agentic knowledge bases]] into a portable system for any project, repo, etc." and "OpenAugi being my main one for vault but what I just did for private Manim as one that's good too." ([[2026-10-03]]). D still has no one-sentence answer in his words (plan open question 4). He needs to say it out loud once.
- **Visual:** the pipe maze turns to show a repo's file tree. `AGENTS.md` glows as the signpost, `agents/` as the rulebook case, and the changelog as a ledger that gets one new line per pass. To bridge into 3a, zoom into the knowledge-base pipe until it becomes the building in cross-section.

## The takeaway

Short (10/17): Next time you type the same correction twice, turn it into a file, a tool, or a check.

Companion: This week, open your AGENTS.md (or CLAUDE.md). If it's long, cut it to a map that points to docs. Then pick the last mistake your agent made twice, have the agent turn it into a check whose error message says how to fix it, and log the change in one line.

## Bridge

Hand-off to the KB Shorts first (3a–3c), then ep 4. "The knowledge-base pipe is where most of this lives. Open it up and it's a building with four floors" leads to **3a** ("The four layers an LLM wiki needs"). After 3c: "And the first thing the agent reads in that building is the map" leads to **ep 4**.

Where ep 3 hands off to 3a–3c without redoing them:
- Point 3 (knowledge in the repo) names the KB and stops. 3a builds the four layers on the building set.
- Point 5 (garbage collection) names the janitor and stops. 3b tells the janitor story (it still needs Chris's queue story).
- Point 6 (this repo) could mention the agent writing detail it needs later (the changelog, the per-video files), and stop. 3c ("notes you never read") owns that idea.

## Extra material (for a long cut or a written companion)

- **Where to put each check (Böckeler, "keep quality left").** Fast checks (linters, quick tests, a basic review agent) run before a commit. Expensive ones (mutation testing, a broad architecture review) run after integration. Drift sensors (dead code, coverage quality, dependency scans) run continuously, outside any change. This is a useful checklist for the companion.
- **Harnessability.** "Not every codebase is equally amenable to harnessing." Strong typing gives you a free sensor, and clear module boundaries let you write architecture rules. Legacy code is the hard case: "the harness is most needed where it is hardest to build." (Böckeler, full text.) Guo makes the same point as "the retrofit problem".
- **Ashby's Law.** "A regulator must have at least as much variety as the system it governs." Committing to a fixed structure narrows what the agent can produce, so a harness can cover it. (Böckeler.) This sets up ep 8's "less harness" beat: "constraining the solution space rather than expanding it."
- **What still slips past every sensor (Böckeler).** "Misdiagnosis of issues, overengineering and unnecessary features, misunderstood instructions." Also: "Correctness is outside any sensor's remit if the human didn't clearly specify what they wanted in the first place." This is a good bridge to ep 7 (the check).
- **Make the app itself legible.** OpenAI made the app bootable per git worktree, wired Chrome DevTools into the agent, and gave each worktree its own logs, metrics and traces, queryable with LogQL and PromQL. Then prompts like "ensure service startup completes in under 800ms" become tractable. Single runs work "upwards of six hours (often while the humans are sleeping)." (Full text.)
- **Boring tech wins.** OpenAI favoured "boring" technologies for "composability, api stability, and representation in the training set". They sometimes had the agent reimplement a small helper instead of using an opaque library. (Full text.)
- **Tools, not just docs.** Stripe's Minions get "over 400 internal tools via MCP servers", in sandboxed devboxes that are the same as human engineers' environments. Brockman's advice: "Maintain a list of tools that your team relies on, and make sure someone takes point on making it agent-accessible (such as via a CLI or MCP server)." (Guo, full text; Brockman's thread itself was not read.) Chris's version: "making lots of CLIs - specific to your use case, then it's easier for agent to do stuff" ([[2026-01-21 - Unix philosophy - cli for agents]]).
- **Progress files for long runs.** Anthropic's long-running-agent work used structured progress files and feature lists, and JSON beat Markdown for feature tracking "because agents were less likely to edit or overwrite structured data inappropriately." (Guo's summary; the Anthropic post wasn't read.)
- **Chris's "files are the layer" line**, for the companion: "This system's orchestration layer is human-readable and human-editable — it's just notes. You can open a plan and reorder steps, edit a task prompt, correct agent memory." This is from [[2026-03-03 - OS for humans and agents - files are the layer]], **but it's in the part of the note that reads like a Claude reply he pasted in, not his own voice.** Don't put it in VO as his words without asking him. His own lines in that note are the bullets (for example "Notes frontmatter like skills - description as a note summary that gets updated").
- **OpenAugi as the second worked example.** The janitor lens, the "one surface, two authors, visible seam" rule, and "Ship the MVP and use it" all come from [[What Works - Running a Second Brain With Agents]] (Augi note, with his 9/13 quotes).
- **The synthesize-vs-route split** for the KB companion: [[Auto Knowledge Base - Canonical Formula and 5-System Comparison]] (Augi). LLM Wiki compiles pages, while OpenAugi routes to raw notes. It sits better in ep 4's companion.
- **His Feb post** *How I run AI agents from my Obsidian* (bitsofchris.com/p/how-i-run-ai-agents-from-my-obsidian, linked from [[2026-02-21 - AE3 - Issue 3]]). Not reread here.

## Don't say

- **"Böckeler groups them into three parts: knowledge base, constraints, garbage collection"** as if it were her current article. That grouping is from her Feb 2026 memo (Chris's Readwise highlight: "grouping based on my interpretation"). The URL now serves a rewritten 2 Apr 2026 article framed as guides and sensors. Say "Böckeler's February memo" or use the guides/sensors framing.
- **"OpenAI's AGENTS.md is 100 lines" as a rule.** They say "roughly 100 lines". It's one team's number, not a guideline.
- **"Hashimoto coined harness engineering."** He wrote "I've grown to calling this 'harness engineering'" and "if another one exists, I'll jump on the bandwagon." Say "named". (Ep 1 owns this.)
- **"Humans don't review anymore."** OpenAI says humans "may review pull requests, but aren't required to" for *their* repo, and warns the end-to-end autonomy "should not be assumed to generalize without similar investment." Brockman's advice (via Guo) is the opposite default: "Ensure that some human is accountable for any code that gets merged."
- **Stripe's "over a thousand merged PRs per week"** and the OpenClaw "6,600+ commits in a month". Secondhand via Guo. The primary sources weren't read.
- **"OpenAI's team spends 20% of its time on cleanup."** It's past tense: they *used to*, then automated it.
- **Anything from [[OpenAI - Harness Engineering]] in the vault.** It's a ChatGPT summary with secondary links (Medium, LinkedIn). The "engine and chassis" car metaphor comes from a Medium post it cites, not from OpenAI.
- **Work specifics.** The 10/2 note names an internal wiki tool, and the AutoDataEng note is a work repo. Say "at work".

## Corrections to SERIES.md

1. **Answer line: "Three parts, from OpenAI's write-up as Böckeler groups them."** The grouping is from Böckeler's superseded Feb memo. The live article (2 Apr 2026, same URL, retitled "Harness engineering for coding agent users") uses guides and sensors × computational and inferential, plus three regulation categories (maintainability, architecture fitness, behaviour). Suggest: "Three parts, as Böckeler's Feb memo grouped OpenAI's write-up…", or switch the answer to guides and sensors.
2. **Sources line: "OpenAI post · Böckeler · Guo."** Add the dates and author: OpenAI, Ryan Lopopolo, 11 Feb 2026 (author and date from search results; the page itself blocks fetches, so I read the text through a reader proxy). Böckeler, 2 Apr 2026 (supersedes the 17 Feb memo). Guo, 22 Feb 2026. Add Hashimoto, "My AI Adoption Journey", 5 Feb 2026, the primary source for the rule Guo quotes.
3. **Chris's-words bullet on [[2026-03-03 - OS for humans and agents - files are the layer]].** The quoted line ("just notes. You can open a plan and reorder steps…") is in the section that reads as a pasted AI reply ("OK so the product instinct here is actually sharp…" follows it), not his own writing. Mark it as unconfirmed for his voice.
4. **Ep 8 (not this episode, but the same source):** "increasing trust and reliability in AI-generated code requires constraining the solution space rather than expanding it" is Guo paraphrasing *Böckeler* ("as Birgitta Böckeler noted on Martin Fowler's site"), not Guo's own claim. Attribute it to Böckeler, via Guo.

## Sources

- OpenAI (Ryan Lopopolo), [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), 11 Feb 2026. **Full text** (openai.com returns 403 to direct fetches, so I read it through a reader proxy; author and date are from search results). It gives the whole build list: a map instead of a manual, knowledge in the repo, lints whose errors are fixes, garbage collection, and "what capability is missing".
- Birgitta Böckeler, [Harness engineering for coding agent users](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html), 2 Apr 2026. **Full text.** It gives the guides vs sensors framing and why you need both.
- Charlie Guo, [The Emerging "Harness Engineering" Playbook](https://www.ignorance.ai/p/the-emerging-harness-engineering), 22 Feb 2026. **Full text.** It gives the convergence across OpenAI, Stripe and OpenClaw, and "update the AGENTS.md whenever the agent does something wrong" (Brockman, via Guo).
- Mitchell Hashimoto, [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey), 5 Feb 2026. **The "Engineer the Harness" section, full.** It gives the two forms of fix (an AGENTS.md line, or a programmed tool).
- This repo: `AGENTS.md`, `CLAUDE.md`, `agents/runbook.md` (header and steps 10–12), `agents/changelog.md` (all), `agents/plans/agentic-kb-shorts.md` (all, Shorts A–D). It gives the worked example for point 6.
- Vault notes used: [[2026-06-02 - Good Primitives]] (Chris), [[2026-02-21 - AE3 - Issue 3]] (Chris), [[Harness Engineering]] (Readwise, Böckeler memo, with his margin note), [[The Emerging Harness Engineering Playbook]] (Readwise, with his margin notes), [[PMOC - AutoDataEng - Loops and Recursive Self Improvement]] (Chris, work, generalize), [[2026-01-21 - Unix philosophy - cli for agents]] (Chris), [[2026-03-03 - OS for humans and agents - files are the layer]] (mixed: his bullets plus a pasted AI reply), [[What Works - Running a Second Brain With Agents]] (Augi, his quotes), [[PMOC - Shorts Augi Shorts - Augi content system]] (Chris, 10/3), [[2026-10-03]] (Chris), [[2026-10-02 - 4 rules for agentic knowledge bases]] (Chris, voice transcript), [[Auto Knowledge Base - Canonical Formula and 5-System Comparison]] (Augi), [[OpenAI - Harness Engineering]] (ChatGPT summary, not used for claims), [[Improving Deep Agents With Harness Engineering]] (Readwise, LangChain). [[Post - Harness Engineering 101]] and [[AutoWiki]] were read and are one-liners.
