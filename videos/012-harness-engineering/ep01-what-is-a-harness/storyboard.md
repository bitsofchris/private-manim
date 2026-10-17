ENGINE: hyperframes

# What Is an Agent Harness? The 4 Parts Explained (Harness Engineering ep 1): storyboard

THE QUESTION: "What's an agent harness?"
WHO IS ASKING: an engineer who uses Claude Code or Codex every day, keeps
hearing "harness" and wants to know what it actually is.
THE ANSWER IN ONE SENTENCE: everything except the model: context, tools,
memory, and the loop.
THE SEARCH PHRASE: what is agent harness (YouTube autocomplete 10/17,
`../SERIES.md`; "agent harness" also offered). Said in VO line 1: "An
agent harness is everything except the model."

**One idea:** an agent is the model wearing a harness: the head is the
model; what it reads, holds, carries and repeats is the harness. **What the
viewer does after:** when the agent fails, ask which part was missing.

The VO is `script.md` (what Chris said), not reworded. Code beat: none.
The one candidate (an `AGENTS.md` line in the memory beat) would repeat
what the caption already says; ep 2 owns the `AGENTS.md` card.

## Ledger (every beat uses exactly these)

**The look: the agent wears the harness** (look C, chosen by Chris
2026-10-17 over the blob-and-pipes rig and two other alternatives;
`00_alt_*` and `00_layout/alternatives.png`). All of it is drawn by
`_kit/rig.js` (`RIG.make`); beats never redraw a part.

- **The agent** (`CAST.agent`, scale 1.1 inside the rig), feet at
  **(500, 1040)** (`RIG.HOME`), arms out at 58° holding its parts. Its
  rectangle head is **the model**, outline drawn `--dim`, with the `1 0`
  eyes; the label **model** (`--dim`) sits right of the head. Magenta never
  goes to the head: this Short is about everything except the model.
- **The four parts, in `CAST.PIPES` order** (`RIG.NAMES`), each teal at
  rest, magenta when named (`RIG.part(rig, i, u)`), one at a time:
  - **context**: a stack of three pages above the head, with a line down
    into the head. Label top-left.
  - **tools**: a terminal card (`>_`) in the right hand. Label under it.
  - **memory**: a two-drawer cabinet in the left hand. Label under it.
  - **loop**: an arrow circling the floor around the feet. Label right.
- **Labels**: DOM text, 60 px, weight 800, `--text`; a named part's label
  goes magenta with it. In beat 1 they pop in on each part's word and stay
  to the end (except beat 6).
- **The things each part shows** (icons, no text: the captions carry the
  words; drawn as local helpers in the beat):
  - context: a page with lines (instructions), a teal page with a hash (a
    file it opened), an ink card with "!" (the last error). They drop
    onto the stack and slide down the line into the head.
  - tools: a page (read a file), the terminal's `>_` blinking (run a
    command), a magnifier (search the web), popping out beside the right
    hand.
  - memory: a teal card, `AGENTS.md` in monospace, rises out of the drawer
    and rides up into the head.
- **The loop's dot**: a white dot that runs round the floor loop; "runs
  the model" the head pulses, "runs the tool" the terminal flashes, "feeds
  the result back" a dot from the terminal to the head, "checks the work"
  a ✓ (`RIG.check`) by the loop label.
- **Beat 6, two agents**: the rig at **(290, 1010) scale 0.65** and a
  second rig at **(760, 1010) scale 0.65** missing **tools and memory**
  (`missing: [1, 2]`, dashed hollow outlines), labels off. Verdicts above
  the heads: ✓ teal at **(290, 450)**, ↻ (`RIG.circling`, `--dim`) at
  **(760, 450)**.
- **The closing order** the VO names: the context, the tool, the memory,
  the check (the loop stands for "the check").

## Beats (from `script.md`; raw times, final table after tightening)

| beat | VO | visual |
|---|---|---|
| 01_hook (0.0–7.1) | An agent harness is everything except the model. It decides what the model sees, what it can do, what it remembers, and when it's done. | Frame 0: the agent at home with all four parts teal, a dot already running round the floor loop, no labels yet except **model**. On "everything" all four parts pulse magenta together (one tight group); on "except the model" they go back to teal and the head blinks. Then each part goes magenta on its word and its label pops in: "sees" → context, "can do" → tools, "remembers" → memory, "when it's done" → loop. Ends: loop magenta, all labels on, dot stopped. |
| 02_context (7.1–11.6) | Context is what goes into the model on this turn. It's your instructions, the files it opened, the last error. | Hero passes to context on "Context". On "goes into the model" a dot slides down the line into the head. On "instructions", "files", "last error" the three context icons drop onto the stack in turn and slide down into the head. Ends: context magenta, icons gone. |
| 03_tools (11.6–15.0) | Tools are what it can touch. Read a file, run a command, search the web. | Hero → tools on "Tools"; the right arm lifts a little. The three tool icons pop out beside the right hand on "file", "command", "web" (stage right, above the terminal). Ends: tools magenta, icons on. |
| 04_memory (15.0–21.0) | Memory is what carries over when the session ends. Notes, rules, like an AGENTS.md, they're loaded back in next time. | Tool icons fade. Hero → memory on "Memory". On "session ends" the agent's eyes close to dashes and open again (a new session). On "AGENTS.md" the card rises out of the drawer; on "loaded back in" it rides up into the head. Ends: memory magenta, card gone. |
| 05_loop (21.0–30.4) | And the loop runs the model, runs the tool, feeds the result back, and checks the work. Try again or stop, and it can even save rules to recursively self-improve. | Hero → loop on "loop". The loop's dot (ledger): head pulse, terminal flash, dot back to the head, ✓ by the loop label. "Try again" the dot goes round once more; "stop" it halts. "save rules" a small rule card leaves the floor loop and drops into the drawer ("self-improve"). Ends: loop magenta, ✓ gone. |
| 06_same_model (30.4–35.7) | The model can be the same, but the harness is why one agent fixes your bug and another might keep going in circles. | Labels fade; the rig shrinks and slides left to (290, 1010); the second agent fades in right with the same head and only context and loop. On "fixes your bug" the ✓ above the left agent; on "going in circles" the ↻ above the right agent spins, and its two missing parts go magenta (the hero: what differs). Ends: ↻ still, missing parts magenta. |
| 07_ask (35.7–42.4) | So when your agent fails, don't blame the model at first. Ask which piece was missing: the context, the tool, the memory, or the check. | The second agent and the verdicts fade; the rig grows back home, labels return, all teal. On "fails" the agent's eyes go to dashes; on "don't blame the model" the head shakes once (still dim). On "the context", "the tool", "the memory", "the check" each part goes magenta in turn, the previous back to teal. Last frame still: loop magenta, eyes open. |

Cuts: every beat starts on the previous beat's last frame (same rig, same
labels, same part lit). `_kit/rig.js` owns the rig, the labels and the
part states so parallel beats match.
