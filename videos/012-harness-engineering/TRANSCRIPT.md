# Harness Engineering: the take

**Name:** harness-engineering-transcript
**Description:** What Chris said in the series recording, with timestamps,
as he pasted it on 2026-10-17. This is the VO; there is no script.
**When to use:** cutting each episode's `vo_raw.m4a` and writing its
`script.md` (`agents/series.md` step 4). The cut lists are in `SERIES.md`.
**How it works:** timestamps are into the recording file. Episode
announcements ("Episode one", "Episode three", "Episode 3A", "Episode
four") are the recording's labels; `SERIES.md` maps them to the published
episodes.

---

[00:00:05] Episode one: What is an agent harness? An agent harness is everything except the model. It decides what the model sees, what it can do, what it remembers, and when it's done. Context is what goes into the model on this turn. It's your instructions, the files it opened, the last error

[00:00:22] tools are what it can touch. Read a file, run a command, search the web. Memory is what carries over when the session ends. Notes, rules, like an agent's MD, they're loaded back in next time. And the loop runs the model, runs the tool, feeds the result back, and checks the work.

[00:00:36] Try again or stop, and it can even save rules to recursively self-improve.

[00:00:41] The model can be the same The harness is why one agent fixes your bug and another might keep going in circles. So when your agent fails, don't blame the model at first.

[00:00:49] Ask which piece was missing, the context, the tool, the memory, or the check

[00:00:56] Episode three, Harness 101 Agents need good primitives

[00:01:14] Every project can be a recursively self-improving loop for agents

[00:01:59] To get the most out of agents, you need to continually self-improve. And the way to do that is to have good primitives and let your agents do things Anytime they do something wrong or could do it better, it needs to be saved in your repository, and you can do it in one of three ways. Keep everything as a file, your plan, your rules, your notes.

[00:02:19] The agents will read them every session and keep your agent's MD short and have a map that points to the rest of the notes

[00:02:38] And then add a test or a linter that will fail out loud so you can quickly fix things. This is how I structure all of my repos these days. I have a map in my agents.md, a CLI for most of the steps

[00:02:53] And a quick janitor script that runs to make sure there's consistency among my notes and rules

[00:03:01] Let your agents recursively self-improve by giving them access to these primitives so they can continually get better

[00:03:10] Episode 3A: The four layers an LLM wiki needs. A good agentic knowledge base or LLM wiki needs four things. First is the agent layer. This is a place where agents write for other agents. Includes details that are needed to resume a task later, like hashes, branches, certain commits. You never have to read this part.

[00:03:28] Then two, you need the human layer. This is the clean, distilled view that links out to the more detailed agent notes but allows you to get a quick overview like a dashboard or a Kanban board or a map of the underlying information. Then three is the curated layer. This is the agent context and rules that the humans need visible.

[00:03:46] This is the slowly changing context that you need to maintain carefully to keep things up to date. And fourth, you need a janitor. As you iterate and change the system, something has to keep it clean and remove any inconsistencies. With all four layers, you can set up any repository as a strong agentic knowledge base

[00:04:05] Episode four: Give your agents a map. Context engineering is just giving your agent a map. Today, agents are using a magnifying glass to search. Oh my God, that's fucking stupid. Humans search when they know what they're looking for, but we turn to agents when we're not really sure what we need, so they end up exploring more.

[00:04:24] The obvious fix is to stuff everything into the context window, but that'll backfire. The model doesn't really find what you're looking for. This is known as context rot. Having one giant agents.md file does not work. When everything is important, nothing is. It can't cut through the noise to find what really matters.

[00:04:41] But by creating a simple map, a map in Markdown or an index in a database, you hold pointers to files. You concisely let the agent navigate where it needs to go. the agent reads the map and drills into only what it needs to, retrieving that part
