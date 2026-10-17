# Ep 4: Give your agent a map (context engineering is index design) (key points)

**Status:** research done 2026-10-16, not yet scripted. Sources read: 3 in full (Chris's essay, Anthropic's "Effective context engineering for AI agents", the OpenAI harness post's knowledge-base section), 4 paper abstracts (RAPTOR, HippoRAG, A-RAG plus its results table, the enterprise-metadata paper plus its results table), 1 by search only (Chroma "Context Rot"), 5 vault notes.
**Question:** why does my agent burn its context searching around, and what should I give it instead?
**Who's asking:** an engineer whose agent greps, reads ten files, fills its window, and still misses the one file that mattered. Or one whose CLAUDE.md has grown to 500 lines and gets ignored.
**Answer in one sentence:** Agents explore because they don't know what to search for yet, so give them a short map to read first, then let them drill into the raw data only where the map says it's worth it.
**Search phrase:** context engineering (guess). Fallback: "claude code context window" or "AGENTS.md too long" (guess).
**Length:** Short (60–90 s). The core is one idea (map first, drill later) with one external check (OpenAI and Anthropic both landed on it). The essay is the written companion as is. The four-layer architecture and the paper evidence go in the companion, not the Short.

## Hook options

1. "Today agents are using a magnifying glass to search through a warehouse." **Chris's own sentence**, from [[Post - Context Engineering is Index Design for Agents]]. It matches the planned hook image.
2. "RAG assumes you know what to search for. Agents exploring a new problem don't." **Chris's own sentence**, same essay.
3. "OpenAI tried one giant AGENTS.md. It failed in four predictable ways." (A fact from the OpenAI post. Not Chris's sentence.)

## Key points, in episode order

### 1. Agents explore, because they don't know what they're looking for yet.
- **Say it:** You search when you know what you want. You hand a task to an agent when you don't, or when you haven't given it enough context. So it has to explore. And exploring with a search box is a magnifying glass in a warehouse.
- **Evidence:** this is Chris's thesis, not a measured finding. Anthropic backs the premise: they define agents as "LLMs autonomously using tools in a loop" and say that "without proper guidance, an agent can waste context by misusing tools, chasing dead-ends, or failing to identify key information." (Anthropic, 29 Sep 2025; full text.)
- **Chris's own line:** "Humans search when they know what they are looking for. We turn to agents when we are unsure what we need. Or we give agents tasks without enough context and they have to build it." and "Today agents are using a magnifying glass to search through a warehouse." ([[Post - Context Engineering is Index Design for Agents]]). From his drafting notes: "Agents don't know what they want yet (becuase often you don't know what you want yet)." ([[Data for Agentic Retrieval]], 3/27).
- **Visual:** a tiny figure with a magnifying glass in a huge dark warehouse of shelves (the hook image). In the series image, it's the blob dribbling into dozens of side pipes at random.

### 2. More context isn't the fix, because every token you add makes the rest a little blurrier.
- **Say it:** The obvious fix is to stuff everything in. That backfires. As the window fills, the model gets worse at finding what's in it. This is called context rot. Anthropic says to treat context like a budget: the smallest set of high-signal tokens that gets the job done.
- **Evidence:** Anthropic: "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases." Context is "a finite resource with diminishing marginal returns". LLMs have an "attention budget", and "Every new token introduced depletes this budget." The cause they give is n² pairwise attention, plus the fact that training data has fewer long sequences. It's "a performance gradient rather than a hard cliff". The goal: "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." (Full text.) The term links to Chroma's July 2025 technical report "Context Rot" (18 models; read via search only).
- **Chris's own line:** from his research notes: "Two key points from Anthropic: First, **context rot** — as tokens accumulate, model recall degrades due to finite attention budgets" ([[Data for Agentic Retrieval]]; it's in his notes but reads as a pasted research summary, so treat it as a summary, not VO). His own words, from the same note: "bitter lesson would say give all data model figure sit out but context loses thins can be expensive" (3/26, typos as written) and "Fire hose vs sprinkler system with labeled zones." (3/25).
- **Visual:** the blob is forced through a pipe stuffed full of stuff. It comes out dimmer and blurrier the more is stuffed in.

### 3. Give it a map, not a manual: a short index it reads first, pointing to where the detail lives.
- **Say it:** OpenAI tried one giant AGENTS.md, and it failed. It crowded out the task, everything was "important" so nothing was, it went stale, and nobody could check it. So they cut it to about a hundred lines that work as a table of contents. The agent reads the map first and is taught where to look next.
- **Evidence:** OpenAI (Lopopolo, 11 Feb 2026; full text): "give Codex a map, not a 1,000-page instruction manual." The one big AGENTS.md "failed in predictable ways". "Context is a scarce resource." "Too much guidance becomes non-guidance. When everything is 'important,' nothing is." "It rots instantly." "It's hard to verify." "we treat it as the table of contents." "A short AGENTS.md (roughly 100 lines)… serves primarily as a map, with pointers to deeper sources of truth." "This enables progressive disclosure: agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front."
- **Chris's own line:** "Agents need a map. An index. Something to help guide them to find what they are looking for. Something that supports their ability to explore." ([[Post - Context Engineering is Index Design for Agents]]). And "the agent's first call should never return raw data. It should return a map." ([[Data for Agentic Retrieval]], 3/26).
- **Visual:** the warehouse lights come on and a single map hangs on the wall by the door. The figure puts the magnifying glass away, reads the map, and walks straight to one aisle.

### 4. Keep pointers, not payloads: let the agent load the detail just in time.
- **Say it:** The map holds pointers (file paths, note titles, saved queries), not the data itself. The agent follows a pointer only when the map says it's worth it. Claude Code already works this way. Your CLAUDE.md goes in up front, and everything else is found with grep and glob when it's needed.
- **Evidence:** Anthropic: "just in time" agents "maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools." "Claude Code is an agent that employs this hybrid model: CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time." Names carry signal too: "a file named test_utils.py in a tests folder implies a different purpose than a file with the same name located in src/core_logic/." The trade-off they admit: "runtime exploration is slower than retrieving pre-computed data." (Full text.)
- **Chris's own line:** "Map → Assess → Drill → Retrieve. The agent reads a lightweight map of what exists, assesses relevance, drills into promising areas, then retrieves only what it needs." ([[Post - Context Engineering is Index Design for Agents]]).
- **Visual:** four pipe valves in a row, labelled map, assess, drill, retrieve. Only one valve at the end opens onto the raw-data tank.

### 5. That makes context engineering index design: data engineering where the consumer is an agent.
- **Say it:** Data engineers already know this. You build the data model to fit the queries. Agents have a new query pattern: explore, then drill. So the job is to build the index the agent looks at first, with one short summary per area that answers one question: should I look here?
- **Evidence:** this is Chris's framing. The supporting pattern is in his essay: RAPTOR, GraphRAG, HippoRAG and others "all arrived at the same query flow" (coarse map, then drill). Two numbers checked against the abstracts: RAPTOR with GPT-4 improves "the best performance on the QuALITY benchmark by 20% in absolute accuracy" (arXiv 2401.18059, abstract). HippoRAG single-step retrieval is "10-30 times cheaper and 6-13 times faster" than iterative retrieval, and up to 20% better on multi-hop QA (arXiv 2405.14831, abstract). The essay says 10–20x; the abstract says 10–30x.
- **Chris's own line:** "context engineering is index design for agents - build the index that is the first place an agent will look" ([[Data for Agentic Retrieval]], 3/27). "Context engineering is data engineering where the consumer is an agent." (Essay, and the 3/27 note.) A context block "answers one question: **'Should the agent look here?'**" (Essay.) The progressive-disclosure line: "If only this existed somewhere - oh yea, news papers, libraries, books, parquet footers, Iceberg." ([[Data for Agentic Retrieval]], 3/27).
- **Visual:** the map on the wall zooms in. Each region is a small card with one line on it, and threads from each card drop to the shelves. The magenta hero is the one card the figure picks.

### 6. Test your setup with one question: does the agent read a map before it retrieves?
- **Say it:** Look at your agent setup and ask one question. Does it read a map before it touches raw data? If not, that's your bottleneck. Not the model, and not the prompt. The index.
- **Evidence:** Chris's own call to action (essay). It matches Anthropic's closing advice and OpenAI's AGENTS.md lesson.
- **Chris's own line:** "Look at your agent system tomorrow and ask one question: 'Does the agent read a map before it retrieves?' If the answer is no, that's your bottleneck. Not the model. Not the prompt. The index." ([[Post - Context Engineering is Index Design for Agents]]). This could be the closing VO almost word for word.
- **Visual:** back to the full pipe machine. A small map plate is bolted onto the intake pipe, and the blob flows in sharp.

## The takeaway

Open your CLAUDE.md or AGENTS.md this week. If it's a manual, turn it into a map: one line per area saying what's there and where to look, with the detail moved into the files it points to. For a data-heavy agent, add one short summary per folder or source that answers "should the agent look here?"

## Bridge

"A map only helps if it stays true. Next: how to keep your agent's context from rotting as it grows" leads to **ep 5** (context as a playbook, ACE).

## Extra material (for a long cut or a written companion)

- **The essay is the companion as is.** [[Post - Context Engineering is Index Design for Agents]] (shipped 3/28). Its four layers: **data blocks** (raw content plus metadata, "like parquet files"), **context blocks** (generated metadata that answers "Should the agent look here?"), the **context graph** (the links the agent navigates, giving both hierarchy and lateral moves), and **context snapshots** (the graph at a point in time, for consistency, time travel and incremental updates). It maps onto Apache Iceberg's metadata. The difference: "Iceberg's metadata is cheap and deterministic… Agent metadata is flexible. It can be expensive and probabilistic."
- **Five retrieval modes** (essay): semantic, attribute filter, graph traversal, time-based, and raw lookup by ID. "The context block is a routing table for retrieval." "Without the map, the agent picks one mode up front, grabs a bunch of data bloating it's context window and tries again."
- **His receipt.** "When I tried to reason across 5,000 notes in my second brain… standard semantic search couldn't navigate it. Entity extraction with GraphRAG and Graphiti went too granular to be useful, too slow, too expensive." (Essay.) And "The breakthrough was realizing the agents were smart enough." That's a good line for a long cut.
- **The day-trading example** (essay): context blocks for a ticker, a sector, and macro, linked by entity, correlation and time edges. It works for a 16:9 cut and is too long for a Short.
- **Two meanings of "progressive disclosure."** For OpenAI, it's a *designed* structure: "a small, stable entry point," and the agent is "taught where to look next." For Anthropic, it's *emergent* from exploration: "allows agents to incrementally discover relevant context through exploration… file sizes suggest complexity; naming conventions hint at purpose." Chris's map is the OpenAI meaning, built on purpose. Worth one sentence in the companion so a reader doesn't conflate them.
- **Anthropic's other long-horizon tools.** Each one belongs to a later episode, so mention it, don't explain it here:
  - *Compaction*: summarize near the limit and restart. "Tool result clearing" is the lightest form, which ties to ep 2's Lewis result.
  - *Structured note-taking*: the agent writes notes outside the window and reads them back, like Claude playing Pokémon keeping tallies and maps. This ties to 3c (the agent layer).
  - *Sub-agents*: they explore in clean windows and return "a condensed, distilled summary of its work (often 1,000-2,000 tokens)". This ties to ep 9.
- **"Right altitude"** for system prompts (Anthropic): between "hardcoding complex, brittle logic" and "vague, high-level guidance". Plus: "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better." It's a good one-liner if the long cut covers tools.
- **Anthropic's hedge** (which keeps the episode honest): "As model capabilities improve, agentic design will trend towards letting intelligent models act intelligently, with progressively less human curation." and "do the simplest thing that works." Chris's own version: "I was over engineering it - but clean deduplicated helps. However letting a model learn what's helpful or letting the agent decide what to use is key. It's bitternlesson pilld." ([[Data for Agentic Retrieval]], 3/26). This also seeds ep 8's "less harness".
- **LangChain's "context engineering on behalf of agents"**: "Onboarding models with context like directory structures, available tools, coding best practices, and problem solving strategies helps reduce the error surface for poor search and avoidable errors in planning." ([[Improving Deep Agents With Harness Engineering]], Readwise highlight only.)
- **A-RAG** (arXiv 2602.03442, abstract plus results table): it gives the agent three retrieval tools (keyword search, semantic search, chunk read) and lets it choose, and "consistently outperforms existing approaches with comparable or lower retrieved tokens." The essay's "94.5% on HotpotQA" matches the A-RAG (Full) row in the main table.
- **Synthesize vs route** ([[Auto Knowledge Base - Canonical Formula and 5-System Comparison]], Augi). Karpathy's LLM Wiki pre-compiles pages, while Chris's context graph routes to raw data. The Augi note's conclusion: "route by default, synthesize on demand." It's a good companion paragraph and a bridge to the 3a–3c building.
- **SaaS angle** (optional): "SaaS companies survive by becoming context engineering harnesses." This is from [[2026-02-24 - Context engineering is the edge, open augi privacy story]], **a Claude TLDR of his voice note, not his own words.** It's off-topic for the Short.

## Don't say

- **"Anthropic coined context rot."** Anthropic writes that needle-in-a-haystack studies "have uncovered the concept of context rot" and links to Chroma's report (July 2025). Say "what researchers call context rot".
- **"Context rot means long context is useless."** Anthropic: "a performance gradient rather than a hard cliff". Models "remain highly capable at longer contexts but may show reduced precision."
- **"OpenAI got the map idea from…" or "Chris called it first."** OpenAI's post is 11 Feb 2026, and Chris's essay is 28 Mar 2026. They got there independently, and his notes don't cite the OpenAI post. Say "OpenAI landed in the same place."
- **"82.5% precision vs 73.3% for content-only"** (the enterprise-metadata paper, as quoted in the essay). The abstract's 82.5% "recursive + TF-IDF" figure doesn't match the paper's own Table V, where recursive + TF-IDF precision is 0.630 and 0.825 is a Hit Rate. 73.3% is the semantic-chunking content-only precision. The paper is internally inconsistent, so drop the number.
- **"HippoRAG is 10–20x cheaper"** (the essay's figure). The abstract says 10–30x.
- **LazyGraphRAG "4% of GraphRAG's query cost"** (essay). I couldn't load the Microsoft blog, so it's unverified. Leave it out of the Short.
- **"GraphRAG 72–83% comprehensiveness"** (essay). Not checked here. Leave it out of the Short.
- **"gbrain 97.6% R@5 on LongMemEval"** and the claimed Chris article title "An LLM wiki won't compound your knowledge". Both appear only in the Augi research note and weren't checked.

## Corrections to SERIES.md

1. **"Anthropic's *Effective context engineering for AI agents* names context rot."** It uses and explains the term but credits it to needle-in-a-haystack studies, linking Chroma's July 2025 "Context Rot" report. Suggest: "uses the term **context rot** (from Chroma's 2025 report)".
2. **Add the date and authors** for the Anthropic post: 29 Sep 2025, Anthropic Applied AI team (Rajasekaran, Dixon, Ryan, Hadfield).
3. **Add the OpenAI harness post as an ep 4 source.** Its "give Codex a map, not a 1,000-page instruction manual" section is the strongest outside confirmation of Chris's thesis, and it gives the four failure modes of one big AGENTS.md. It's already an ep 1/3 source.
4. **"Progressive disclosure"** (attributed to his 3/27 note) is fine, but Anthropic and OpenAI use the term in two different senses (emergent vs designed). Note it so the script doesn't blur them.
5. **Not SERIES.md, but the published essay** has one checkable error: HippoRAG is "10–30 times cheaper" per its abstract, not 10–20x. The enterprise-metadata "82.5% vs 73.3%" figure doesn't hold up against that paper's own table. For Chris to decide whether to add an erratum on Substack.

## Sources

- Chris Lettieri, [[Post - Context Engineering is Index Design for Agents]] (Substack, 28 Mar 2026). **Full text, from the vault copy.** It's the backbone: the warehouse and map image, "RAG assumes you know what to search for", Map → Assess → Drill → Retrieve, the four layers, and the closing test question.
- Anthropic Applied AI team, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 29 Sep 2025. **Full text.** It gives context rot and the attention budget, "smallest set of high-signal tokens", just-in-time pointers, Claude Code's hybrid (CLAUDE.md up front plus grep and glob), and progressive disclosure through exploration.
- OpenAI (Ryan Lopopolo), [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), 11 Feb 2026. **Full text** (read through a reader proxy; openai.com blocks direct fetches). It gives "a map, not a 1,000-page instruction manual", the four failure modes of one big AGENTS.md, "~100 lines", and progressive disclosure by design.
- Sarthi et al., [RAPTOR](https://arxiv.org/abs/2401.18059) (ICLR 2024). **Abstract.** It gives +20% absolute accuracy on QuALITY with GPT-4, from tree-of-summaries retrieval.
- Gutiérrez et al., [HippoRAG](https://arxiv.org/abs/2405.14831) (NeurIPS 2024). **Abstract.** It gives 10–30x cheaper and 6–13x faster than iterative retrieval, and up to 20% better on multi-hop QA.
- [A-RAG](https://arxiv.org/abs/2602.03442) (Feb 2026). **Abstract plus the main results table.** It gives agent-chosen hierarchical retrieval tools and confirms 94.5% on HotpotQA (A-RAG Full).
- [A Systematic Framework for Enterprise Knowledge Retrieval: Leveraging LLM-Generated Metadata](https://arxiv.org/abs/2512.05411) (Dec 2025). **Abstract plus Table V.** Its finding is that metadata enrichment beats content-only, but its headline number is inconsistent (see Don't say).
- Chroma, [Context Rot](https://research.trychroma.com/context-rot) (Hong, Troynikov, Huber, 14 Jul 2025). **Search summary only.** It's where the term comes from: 18 models, with reliability falling as input grows.
- Vault notes used: [[Post - Context Engineering is Index Design for Agents]] (Chris, published), [[Data for Agentic Retrieval]] (Chris, drafting log 3/25–3/28, with a pasted research summary inside), [[2026-02-24 - Context engineering is the edge, open augi privacy story]] (Claude TLDR of his voice note), [[Improving Deep Agents With Harness Engineering]] (Readwise, LangChain), [[Auto Knowledge Base - Canonical Formula and 5-System Comparison]] (Augi).
