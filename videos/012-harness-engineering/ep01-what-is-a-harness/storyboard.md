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

**One idea:** the model is the blob; the harness is the four pipes around
it. **What the viewer does after:** when the agent fails, ask which pipe
was missing.

The VO is `script.md` (what Chris said), not reworded. Code beat: none.
The one candidate (an `AGENTS.md` line in the memory beat) would repeat
what the caption already says; ep 2 owns the `AGENTS.md` card.

## Ledger (every beat uses exactly these)

- **The rig.** One `CAST.blob` (the model) with its four pipes in
  `CAST.PIPES` order and direction: **context up, tools right, memory
  down, loop left**. Rig centre **(507, 600)**, scale **0.85**, pipe
  length **120** (`pipe: 120`). Same place in every beat except beat 6.
- **The model stays at rest.** The blob body is drawn `--dim` (stroke
  `--dim`, fill `--dim` at 0.12) in every beat: this Short is about
  everything except the model, so magenta goes to the pipe being named,
  never to the blob. (Local override of `blob.body` attributes in
  `_kit/rig.js`, not a kit change.)
- **Pipe states:** rest = teal (built, part of the harness); named =
  magenta (the hero, one at a time); missing = `--muted`, dashed (beat 6
  only).
- **Labels** (DOM text, 60 px, weight 800, `--text`), one per pipe end:
  **context** above the up pipe, **tools** right of the right pipe,
  **memory** below the down pipe, **loop** left of the left pipe. They pop
  in during beat 1 on the word for each part and stay to the end. When a
  pipe is the hero its label turns magenta with it.
- **The human:** `CAST.human`, feet at **(170, 1080)**, scale **0.5**,
  face `smile`, facing the rig. Present in every beat.
- **The three things on each pipe** (icons, no text: the captions carry
  the words):
  - context: a page with lines (instructions), a `CAST.page` with a hash
    (a file it opened), an ink card with "!" (the last error). They slide
    down the context pipe into the blob.
  - tools: a page (read a file), a terminal card with `>_` (run a
    command, monospace set from the script), a magnifier (search the web).
    They pop out at the tools pipe's end.
  - memory: a teal card, `AGENTS.md` in monospace, drops out of the
    memory pipe, then rides back up it into the blob.
- **The loop** is a teal dot that runs model → tools → back into the blob
  → a check mark, then one rule card from the loop into the memory pipe.
- **The verdicts:** ✓ (teal) = fixed; ↻ (`--dim`, spinning) = going in
  circles.
- **The closing order** the VO names: the context, the tool, the memory,
  the check (the loop pipe stands for "the check").

## Beats (from `script.md`; raw times, final table after tightening)

| beat | VO | visual |
|---|---|---|
| 01_hook (0.0–7.1) | An agent harness is everything except the model. It decides what the model sees, what it can do, what it remembers, and when it's done. | Frame 0: the rig at rest, four teal pipes with a slow flow of dots along them, the dim blob, the human beside it looking up. On "everything" the four pipes pulse together (a tight group, magenta) and the blob stays dim; on "except the model" they go back to teal. Then each pipe goes magenta on its word and its label pops in: "sees" → context, "can do" → tools, "remembers" → memory, "when it's done" → loop. Ends: loop magenta, all four labels on. |
| 02_context (7.1–11.6) | Context is what goes into the model on this turn. It's your instructions, the files it opened, the last error. | Hero passes to the context pipe on "Context". On "goes into the model" a dot runs down it into the blob. On "instructions", "files", "last error" the three context icons appear above the pipe in turn and slide down into the blob. Ends: context magenta, icons gone. |
| 03_tools (11.6–15.0) | Tools are what it can touch. Read a file, run a command, search the web. | Hero → tools pipe on "Tools". The three tool icons pop out at the pipe's end on "file", "command", "web", stacked to the right of the "tools" label (stage right, y 450–750). Ends: tools magenta, icons on. |
| 04_memory (15.0–21.0) | Memory is what carries over when the session ends. Notes, rules, like an AGENTS.md, they're loaded back in next time. | Hero → memory pipe on "Memory". Tool icons fade. On "session ends" the human blinks (a new session); on "AGENTS.md" the `AGENTS.md` card drops out of the memory pipe and rests below its label; on "loaded back in" it rides back up the pipe into the blob. Ends: memory magenta, card gone. |
| 05_loop (21.0–30.4) | And the loop runs the model, runs the tool, feeds the result back, and checks the work. Try again or stop, and it can even save rules to recursively self-improve. | Hero → loop pipe on "loop". The teal dot: "runs the model" pulses the blob, "runs the tool" runs out the tools pipe, "feeds the result back" comes back in, "checks the work" a ✓ by the loop label. "Try again" the dot goes round once more; "stop" the dot halts. "save rules" a small rule card leaves the loop pipe and slides into the memory pipe ("self-improve"). Ends: loop magenta. |
| 06_same_model (30.4–35.7) | The model can be the same, but the harness is why one agent fixes your bug and another might keep going in circles. | The rig shrinks and slides left (centre (300, 600), scale 0.5, labels go); a second rig with the same dim blob appears right (centre (720, 600)) with only two pipes, the missing two dashed `--muted`. On "fixes your bug" a ✓ under the left rig; on "going in circles" a ↻ under the right rig spins, and the two missing pipes go magenta (the hero: what differs). Human stays. Ends: ↻ still, missing pipes magenta. |
| 07_ask (35.7–42.4) | So when your agent fails, don't blame the model at first. Ask which piece was missing: the context, the tool, the memory, or the check. | The right rig and ✓ fade; the left rig grows back to the ledger place, labels return, all pipes teal. On "fails" the human frowns; on "don't blame the model" the blob shakes once (still dim). On "the context", "the tool", "the memory", "the check" each pipe goes magenta in turn, the previous back to teal. The human tilts to each. Last frame still: the loop pipe magenta, the human `flat`. |

Cuts: every beat starts on the previous beat's last frame (same rig,
same labels, same pipe lit). The kit `_kit/rig.js` defines the rig, the
labels and the pipe states so the beats match.
