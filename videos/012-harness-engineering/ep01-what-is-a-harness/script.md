# What Is an Agent Harness? The 4 Parts Explained

`vo_raw.m4a`: 42.4 s, cut from `~/Creating/012-harness-engineering-series.m4a` at 10.81–53.18 s (announcement removed). Cut points are at the quietest 10 ms near each word boundary (WhisperKit Large v2 word times), with 15 ms fades. Plan: `../SERIES.md`.

## As recorded

An agent harness is everything except the model. It decides what the model sees, what it can do, what it remembers, and when it's done. Context is what goes into the model on this turn. It's your instructions, the files it opened, the last error. Tools are what it can touch. Read a file, run a command, search the web. Memory is what carries over when the session ends. Notes, rules, like an AGENTS.md, they're loaded back in next time.

And the loop runs the model, runs the tool, feeds the result back, and checks the work. Try again or stop, and it can even save rules to recursively self-improve.

The model can be the same, but the harness is why one agent fixes your bug and another might keep going in circles. So when your agent fails, don't blame the model at first. Ask which piece was missing: the context, the tool, the memory, or the check.

## Notes

Mishearings fixed: "this term" → "this turn"; "the files that opened" → "the files it opened" (both recognizers wrote "that"; check on listen). "but the harness" is WhisperKit's reading; Parakeet dropped "but the".
