# kb-code: the agent's code being written under the gameplay

**Name:** kb-code (the AugiCraft diamond-run Short, code-view cut)

**Description:** `kb-graph/` with the bottom band swapped. Instead of a
knowledge graph, the band is an editor: zoomed out it shows the hierarchy
of helper functions AgentMiner has written so far; for each new skill or
lesson card it zooms into that function and types out the code the agent
actually saved, fast, scrolling as it goes, then zooms back out. The goal
(Chris, 2026-10-22): viewers feel they are watching the learning.

**When to use:** the diamond-run Short when the code should be the story,
and any "watch an agent learn" clip where the agent's output is code.
Compare with `kb-graph/` before choosing.

**How it works:** everything above the band is kb-graph's, shared rather
than copied: `footage/edit.js`, `footage/captions.js` and
`footage/timelapse.mp4` are symlinks into `../kb-graph/footage/`, the
cards, chips, clock, tool strip and caption code are kb-graph's, and the
sound is kb-graph's `out/mix.wav`. A re-edit of kb-graph (new `edit.json`,
new captions) carries over on the next render here.

1. `node make_code.mjs [kb]` writes `footage/code.js` from the run's
   knowledge base (default `~/augi-fresh-kb`): each note as it was in the
   commit that created it. Helpers: the `## Code` block inside
   `async function <fn>(args) {}` (the bodies read `args`) plus the
   parameter names from `implementation:`. Lessons: the `## Procedure`
   as `//` comments wrapped at 44 characters.
2. Render the picture:
   `HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 npx --yes --prefer-offline hyperframes@0.8.115 render --quiet -o out/augicraft-diamond-short-code.mp4 .`
   (about 4 minutes; run `validate` first: a script error renders a frozen
   frame and only warns `sub_timeline_readiness_timeout`).
3. Put kb-graph's sound on it:
   `ffmpeg -i out/augicraft-diamond-short-code.mp4 -i ../kb-graph/out/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out/augicraft-diamond-short-code-sound.mp4`

## The editor (x 40-1040, y 1190-1536)

- **Zoomed out:** one row per function, in the order written, each lesson
  indented under the helper it names (`craft-one-at-a-time` under
  `craftItem`, `check-movement-progress` under `staircaseDown`). Helpers
  teal with dim parameters (cut with `…` past 40 characters so the tick
  fits), lessons ink, the row being written magenta until the next card.
  `✓ valid` lands when a skill is validated, held until the editor is
  zoomed out so it is seen; `descendScanOre` is struck through with
  `dropped`. Before the first card: `// no skills yet`.
- **Card → zoom in → type → zoom out:** the card pops as in kb-graph
  (held 0.75 s, not 1 s, so less typing hides behind it) and shrinks into
  the editor's top left. The editor zooms about the new row (0.45 s), types
  from 0.7 s after the card at about 13 lines a second (0.8-3.2 s, less if
  the next card is close), rests 0.25 s, zooms out (0.45 s). Cards are at
  least 2.8 s apart (kb-graph: 1.3 s) so every card gets a zoom out and in.
  The cursor sits ~6 lines down, below the card, so the line being typed
  stays visible while the card holds.
- **Lessons** type their comments above the first lines of the helper they
  name (shown dim), so it reads as the agent editing existing code.
- **Dropped** zooms into `descendScanOre`, tints it, and deletes it from
  the last line up.
- Syntax colours from the house palette: keywords teal, strings and numbers
  dim, comments muted, the cursor magenta. Monospace is set from the
  script on every span (the CSS-class trap in the beat brief).

## Open for Chris

- The typing is mostly under the card in the first 15 s, where five cards
  come close together. Options: shorter cards, a card that sits over the
  footage instead of the band, or fewer early cards.
- The hierarchy rows are 27 px to fit ten rows in the band. Larger text
  needs either fewer rows (lessons as a mark on their helper) or a taller band.
