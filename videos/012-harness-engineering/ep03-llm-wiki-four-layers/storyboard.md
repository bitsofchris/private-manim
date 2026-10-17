ENGINE: hyperframes

# LLM Wiki: The 4 Layers Every Repo Needs (Harness Engineering ep 3): storyboard

THE QUESTION: "How do I make my agent setup get better instead of messier?"
WHO IS ASKING: an engineer who runs coding agents (Claude Code, Codex) in
their repos every day and watches the notes, rules and plans pile up.
THE ANSWER IN ONE SENTENCE: an agent layer, a human layer, a curated layer,
and a janitor: separate what agents write from what you read, and run a
janitor.
THE SEARCH PHRASE: llm wiki (YouTube autocomplete, checked 10/17 in
SERIES.md; the results are about Karpathy's LLM Wiki). Said in VO line 1:
"A good LLM wiki needs four layers."

**One idea:** a repo's knowledge base stays useful when each kind of text
has its own floor, and something cleans between them.

**The VO** is `script.md` (what Chris said, cut to 63.9 s), not a planned
script. Captions follow the audio: both recognizers hear "**These** can
include details", not script.md's "This".

**Code beat:** one small one. Beat 2 lifts one agent page out of the
basement as a callout card whose three monospace lines land on "hashes,
branches, commits". That is the only text drawn in the scene.

## Ledger (every beat uses exactly these)

**The building** (the whole episode is one frame; nothing leaves it).
Captions are anchored bottom (`assemble.py --captions-anchor bottom`), so
the stage runs to y 1330. Coordinates are frame pixels.

- Walls: ink, x 80 and x 930, from the roof (y 262) to the basement floor
  (y 1310). Roof: one ink line y 262.
- The ground floor slab: ink, y 700, from x 80 to x 700. The stair opening
  is x 700–930. Outside the walls the ground continues as a muted line at
  y 700 to both frame edges, so the lower floor reads as a basement.
- **Upstairs (y 262–700): the human layer.** The human (`CAST.human`,
  s 0.6) stands at x 190, feet on y 700, facing the board. The board
  (`CAST.board`, cards `[2, 1, 3]`) at x 300, y 400, about 340 × 270.
- **The stairs (x 700–930): the curated layer and the janitor.** Upper
  flight from the slab edge (700, 700) down to a landing at y 1000 (x 780–
  925); lower flight from the landing down to the basement floor at x ~700.
  Drawn as a stepped ink line. The glass case (`CAST.vitrine`, s 0.45) sits
  on the landing. The janitor (`CAST.janitor`, s 0.45) stands on the upper
  flight, between the floors.
- **The basement (y 700–1310, x 80–680): the agent layer.** Two agents
  (`CAST.agent`, s 0.5) at x 200 and x 460, feet on y 1310, each writing a
  page (`CAST.page`, s 0.42) held at shoulder height beside it. A shelf of
  five pages (s 0.4) along the top of the basement, y ~740: the agents'
  pile. Two of them, the leftmost, are **old**: drawn muted, dashed.
- **Order the layers are named in, always:** agent layer → human layer →
  curated layer → janitor. Any beat that lights them in turn uses this
  order.
- **The callout card** (beat 2): a panel card, teal outline, three
  monospace lines at 60 px, teal: `hash a3f9c2`, `branch fix/auth`,
  `commit 9e1b04`. The hash matches the page's own top line (`a3f9c2`, the
  kit default).
- **The link** (beat 3): a dashed line from the board's middle card down
  through the slab to the right-hand agent's page.
- **The conflict** (beat 5): one line on the second shelf page from the
  right turns magenta; it starts to copy onto its neighbour; the janitor's
  broom sweeps it out.
- Colour jobs: teal is what agents write (pages, the agents' eyes, the
  callout). Ink is people, the building and the board. Magenta is the one
  thing the beat points at. The case glass is the kit's glass cyan.

## Beats (VO from script.md; times from the trial cut, master seconds)

| # | Beat | VO (as recorded) | Visual (9:16) | Hero |
|---|------|---|---|---|
| 1 | Four layers | A good LLM wiki needs four layers. A place where agents can write for agents, a clean surface for humans to read, a curated layer of slowly changing context and rules that you review, and a janitor that keeps it all up to date and consistent. | Frame 0: the whole building, already working (the two agents' pens moving, lines filling their pages; the human looking at the board). Each layer turns magenta as it's named and goes back to rest as the next is named: "agents can write for agents" → the basement's pages; "clean surface for humans" → the board; "curated layer" → the case; "a janitor" → the janitor (a sweep of the broom on "up to date"). | each layer in turn |
| 2 | Agent layer | The agent layer is written by agents for other agents. Agents can be as verbose as they need to be. These can include details that they need to resume a task later, like hashes, branches, commits. You never need to read it or go here. | "written by agents for other agents": one agent hands its page to the other. "verbose": the pages' lines run long, the shelf fills. "resume a task later": the callout card lifts out of the right agent's page and grows over the middle of the building (a solid panel, y ~760–1060, the scene dimmed behind it); "hashes, branches, commits": its three lines land one per word. "never need to read it": the card sinks back into the page; upstairs the human stays turned to the board. | the callout card |
| 3 | Human layer | The human layer is the clean, distilled view that you link out, and that goes to these detailed agent notes when necessary. Think of a dashboard or a Kanban board. It's less about reviewing what the agent's up to and more about managing your own context. | "The human layer": the board goes magenta. "link out … detailed agent notes": the middle card draws the dashed link down to the agent's page (page pulses teal). "Kanban board": a card slides from column 1 to column 2. "less about reviewing what the agent's up to": the human glances down at the basement, then back; "managing your own context": the human points at the board. | the board |
| 4 | Curated layer | The curated layer, this is the slowly changing context that you need to handle with care. These are the skills and rules, the conventions of your repo. | "curated layer": the case goes magenta, the link fades. "handle with care": the glass glints once. "skills and rules": the rules item inside the case becomes the hero (the case returns to glass); "conventions of your repo": hold. | the case, then its rules |
| 5 | Janitor | And then you need the janitor. This looks to catch conflicting rules in your agent notes before they spread. And it cleans up old material so the human layer stays useful. | "the janitor": the janitor goes magenta and walks down the lower flight into the basement. "conflicting rules": one line on a shelf page turns magenta; "before they spread": a copy starts to draw on its neighbour, and the broom sweeps both out (the broom is the hero). "old material": the two old dashed pages are swept off the shelf. "human layer stays useful": the board upstairs settles, clean. | the janitor, then the conflict |
| 6 | Close | This is how I structure all of my repos these days. With all four layers, you can build a strong agentic knowledge base. | The janitor back on the stairs; the whole building at rest. "all four layers": the four light once each in the ledger order, quickly, and return to rest. Still frame by the end. | each in turn, then none |

## Final beats (the contract)

To be written after the cut list is approved: master start, length,
folder, VO, from `words.json`.
