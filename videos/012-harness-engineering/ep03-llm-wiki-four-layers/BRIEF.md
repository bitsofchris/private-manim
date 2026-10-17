# Beat brief: 012 ep03, LLM Wiki: the four layers

**Name:** harness-ep03-beat-brief
**Description:** The contract for the six HyperFrames beats of "LLM Wiki:
The 4 Layers Every Repo Needs" (58.82 s). Every beat draws the building
with the episode kit `_kit/wiki.js` through one call, `K.draw(S)`, where
`S` is a full state object; each beat opens on `WIKI.SEAM[n-1]` and ends on
`WIKI.SEAM[n]`, so cuts are exact by construction.
**When to use:** you were handed this path plus one or two beat numbers.
**How it works:** copy the template below into your beat folder, write
`S(t)` from the cues, check, render to `media/hf/`, review your own contact
sheet, report.

## Read first

1. `agents/beat-brief-hyperframes.md`: the technical rules (pure function
   of time, no network, no `Math.random`, palette, safe area, text floor,
   review loop, report format). All of it applies. One exception: the stage
   runs to **y 1330** (captions are anchored bottom).
2. `_kit/wiki.js`: the kit. Read all of it, especially `BASE` (every state
   field, commented), `SEAM`, `draw`, and `mix`.
3. `storyboard.md`: the ledger, the beats table (the visual brief) and the
   "Final beats" table (the contract).
4. `00_layout/index.html` (the approved look, Chris OK'd it 10/17) and
   `00_layout/layout.png`. Its `S(t)` shows every kit field in use.

Never edit `_kit/`, `00_layout/`, another beat's folder, `videos/_shared/`
or anything outside this episode folder. Need something the kit lacks (a
new state field, a part)? Write a local helper in your `index.html` and
name it in the report.

## Rules for this episode

- **Seams.** `S(0)` deep-equals `SEAM[n-1]`; `S(t)` for the last ~0.3 s
  deep-equals `SEAM[n]` (still). Build `S(t)` with `merge(SEAM[n-1], {...})`
  and fields that run from the start value to the end value; anything
  extra (a glow, a glint, a pulse, a hand-over) is 0 at both ends.
- **Frame 0 moves.** Beats 2–6 open with `write: 0` (the agents' arms at
  rest). Ramp `write` up within the first ~0.3 s (`pen` = beat-local
  `t * 1.6`), so the agents are writing from the first frames, and ramp it
  back to 0 before the hold. Let `fill` creep up while they write (stay
  ≤ 1). Beat 1 opens already writing (`SEAM[0].write` is 1).
- **One hero** (`S.hero`, one of `WIKI.HEROES`) at a time, on the word
  that names it; back to `null` (or the next hero) when the VO moves on.
  The conflict marks and the link are magenta by construction: the
  conflict only while the hero is `"broom"` or `null`, the link only while
  the hero is `"board"` (the kit dims it otherwise).
- **Moves the viewer tracks ≥ 0.6 s**, ease `E.io` / `E.out`. Hero swaps
  are instant. People move only when the VO gives them a reason.
- **Figures.** Poses are degrees: `armR` / `armL` from straight down
  (positive swings out), `lean` (upper body), `tilt` (head). The janitor's
  `jan.x, jan.y` is the point between its feet: on the landing
  `y = WIKI.LANDING.y` (1000), on the floor `y = WIKI.B.floor` (1310), on the
  ladder `x = WIKI.LADDER.cx` (624) with any `y` between. To get from the
  landing to the ladder walk left along `y 1000` to `x 624`; climb with a
  small `lean` wobble; step off to the right on the floor.
- No text of your own: the only scene text is the kit's (page hashes, the
  callout). Captions are burned in later.

## Template (copy to `NN_beat/index.html`)

Copy `00_layout/index.html`, set `data-duration` on `#root` to
`BEAT_SECONDS`, fix the head comment, and replace the script body with:

```js
(() => {
  const BEAT_SECONDS = 0.0;            // from the table
  const MASTER = 0.0;                  // master start, from the table
  const CUE = { /* word: master − MASTER, from words.json */ };
  const { seg, pulse, merge, mix, SEAM, B, LADDER, LANDING } = WIKI, E = WIKI.E();
  const root = document.getElementById("root");
  const K = WIKI.mount(root);
  ISO.guides(root);
  function S(t) { /* S(0) deep-equals SEAM[n-1]; S(end) deep-equals SEAM[n] */ }
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = ISO.start(BEAT_SECONDS, (t) => K.draw(S(t)));
})();
```

The folders and their symlinks (`vendor`, `iso`, `cast`, `kit`) already
exist. Render from the beat folder:

```
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
npx --yes --prefer-offline hyperframes@0.8.115 check
npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_beat.mp4
```

Contact sheet from the episode folder:
`../../../tools/review_frames.sh media/hf/NN_beat.mp4 4`. Never two renders
at once in one folder. To check your seams numerically, add a temporary
`if (/[?&]seam/.test(location.search))` block, or compare `JSON.stringify(S(0))`
with `JSON.stringify(SEAM[n-1])` in a quick node/browser check; remove it
before the final render.

## The beats

Cue times: `words.json` (master seconds, spellings fixed). Beat-local =
master − start. Check the ones that matter on the envelope of
`vo_final.wav`.

| # | Folder | Master start | `BEAT_SECONDS` | Opens on | Ends on |
|---|---|---:|---:|---|---|
| 1 | `01_four_layers` | 0.00 | 13.55 | `SEAM[0]` (first frame of the Short, writing) | `SEAM[1]` |
| 2 | `02_agent_layer` | 13.55 | 11.80 | `SEAM[1]` | `SEAM[2]` |
| 3 | `03_human_layer` | 25.35 | 12.20 | `SEAM[2]` | `SEAM[3]` |
| 4 | `04_curated_layer` | 37.55 | 7.50 | `SEAM[3]` | `SEAM[4]` |
| 5 | `05_janitor` | 45.05 | 8.00 | `SEAM[4]` | `SEAM[5]` |
| 6 | `06_close` | 53.05 | 5.77 | `SEAM[5]` | `SEAM[6]` (last frame of the Short, still) |

**1 Four layers** — "A good LLM wiki needs four layers. A place where
agents can write for agents, a clean surface for humans to read, a curated
layer of slowly changing context and rules that you review, and a janitor
that keeps it all up to date and consistent." Frame 0 is the finished
picture, already working: the agents writing (`write` 1, `fill` creeping).
Heroes in the ledger order, each on its naming word: "agents" (3.20) →
`"pages"`; "clean surface" (4.96) → `"board"`; "curated" (7.14) →
`"case"`; "janitor" (11.22) → `"janitor"`, with one broom sweep (`jan.lean`
and `armR` pulse, back to rest) on "up to date" (12.30). Hero → `null` and
`write` → 0 before the hold (~13.25). Master cues: agents 3.20, clean 4.96,
curated 7.14, janitor 11.22, up 12.30, consistent 12.95–13.36.

**2 Agent layer** — "The agent layer is written by agents for other agents.
Agents can be as verbose as they need to be. These can include details that
they need to resume a task later, like hashes, branches, commits. You never
need to read it or go here." "agent layer" (13.96): hero `"pages"`. "for
other agents" (15.65–16.20): `hand` 0→1→0 (agent A passes its page toward
B and takes it back, ≥ 1 s). "verbose" (17.74): `wall` 3 → 5 (≥ 0.8 s),
`fill` rises faster. Hero → `null` by "These" (19.34). "resume a task"
(20.94): `callout` 0→1 (≥ 0.6 s, `E.out`), hero `"callout"`. "hashes"
(21.94) / "branches" (22.43) / "commits" (22.80): `lines` 0→1→2→3, one per
word. "never need to read it" (23.72–24.62): `callout` 1→0 (≥ 0.6 s), hero
`null` once it is gone. The human stays turned to the board (no move).
Ends `SEAM[2]` (`wall` 5, `fill` [0.9, 0.75], `write` 0).

**3 Human layer** — "The human layer is the clean, distilled view that you
link out and that goes to these detailed agent notes when necessary. Think
of a dashboard or a Kanban board. It's less about reviewing what the
agent's up to and more about managing your own context." "human layer"
(25.64): hero `"board"`. "link out" (28.36) → "agent notes" (30.52): `link`
0→1 (≥ 1 s), then `glow` ["pageB", 0→1] on "notes" (30.72). "Kanban"
(33.02): `kanban` 0→1 (≥ 0.6 s). "reviewing what the agent's up to"
(34.74–35.64): the human glances down at the basement (`tilt` ~ −12, then
back). "managing your own context" (36.20): the human points at the board
(`armR` 22 → 100, `tilt` 6, ≥ 0.6 s). Ends `SEAM[3]` (hero `"board"`,
`link` 1, `kanban` 1, human pointing).

**4 Curated layer** — "The curated layer, this is the slowly changing
context that you need to handle with care. These are the skills and rules,
the conventions of your repo." "curated" (37.86): hero `"case"`; `link`
1 → 0 (≥ 0.4 s) and the human's arm back to rest (`armR` 100 → 22, `tilt`
→ 0, ≥ 0.6 s). "handle with care" (40.96–41.45): `glint` 0→1 (one pass,
~0.8 s). "skills and rules" (42.42–42.94): hero `"rules"`. "conventions of
your repo": hold. Ends `SEAM[4]` (hero `"rules"`).

**5 Janitor** — "And then you need the janitor. This looks to catch
conflicting rules in your agent notes before they spread. And it cleans up
old material so the human layer stays useful." "janitor" (45.86): hero
`"janitor"`; it walks left to the ladder and climbs down (landing
(716, 1000) → (624, 1000) → (624, 1310) → step right to ~ (660, 1310)),
done by ~47.3. "conflicting" (47.38): hero `"broom"`, `conflict[0]` 0→1 on
page B (~0.4 s). "spread" (49.70; start on "before" 49.34): `conflict[1]`
0→1 on page A, and the janitor sweeps (a `lean` + `armR` pulse toward page
B): `swept` 0→1 landing by ~50.2. "old material" (50.94–51.12): the
janitor walks right to x 700 with a second sweep; `old` 0→1 (≥ 0.8 s).
"human layer stays useful" (51.84–52.82): hero `null`; `glow` ["board",
0→1] once. Ends `SEAM[5]` (janitor at (700, 1310), `conflict` [1, 1],
`swept` 1, `old` 1, hero `null`).

**6 Close** — "This is how I structure all of my repos these days. With
all four layers, you can build a strong agentic knowledge base." From
53.05 to ~55.3 the janitor walks back: (700, 1310) → (624, 1310), climbs
to (624, 1000), walks to (716, 1000). "all four layers" (55.62–56.06+):
light the four once each in the ledger order, ~0.45 s each: `"pages"`,
`"board"`, `"case"`, `"janitor"`, then `null` by ~57.6. Still for the
last ~0.8 s; the last frame is `SEAM[6]` exactly.

## Report

As in the HyperFrames brief: per beat, the cue constants with their word,
the mp4 path and measured duration, `check` errors / warnings, anything
changed from this brief and why, what you wished existed. Do not commit.
