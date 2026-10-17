# Context Engineering: Give Your Agent a Map

`vo_raw.m4a`: 38.9 s, cut from `~/Creating/012-harness-engineering-series.m4a` at 249.80–252.73 and 258.81–294.59 s, 0.2 s silence between (announcement and the magnifying-glass line at 253.22–257.28 removed). Cut points are at the quietest 10 ms near each word boundary (WhisperKit Large v2 word times), with 15 ms fades. Plan: `../SERIES.md`.

## As recorded

Context engineering is just giving your agent a map.

Humans search when they know what they're looking for, but we turn to agents when we're not really sure what we need, so they end up exploring more. The obvious fix is to stuff everything into the context window, but that'll backfire. The model doesn't really find what you're looking for. This is known as context rot.

Having one giant AGENTS.md file does not work. When everything is important, nothing is. It can't cut through the noise to find what really matters. But by creating a simple map, a map in Markdown or an index in a database, you hold pointers to files. You concisely let the agent navigate where it needs to go. The agent reads the map and drills into only what it needs to, retrieving that part.

## Notes

No flubs left in the cut. The last sentence trails off slightly ("retrieving that part"); tighten in runbook step 5 if it sounds unfinished.
