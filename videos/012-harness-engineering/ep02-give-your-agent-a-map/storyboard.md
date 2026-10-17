ENGINE: hyperframes

# Context Engineering: Give Your Agent a Map (Harness ep 2): storyboard

THE QUESTION: "Why does my agent miss what's in my repo?"
WHO IS ASKING: an engineer who uses Claude Code or Codex every day and
keeps adding to AGENTS.md, and the agent still wanders or misses the file
that matters.
THE ANSWER IN ONE SENTENCE: stuffing the context backfires; give the agent
a map that points to the files.
THE SEARCH PHRASE: context engineering (autocomplete checked 10/17,
`../SERIES.md`; "context engineering for agents" also offered). Said in VO
line 1.

**One idea:** a short map beats a full window. **The viewer's move after:**
keep AGENTS.md a short map, not a manual.

The VO is `script.md` (what Chris said), not a planned script. Series
plan and look: `../SERIES.md`. `key-points.md` is background only.

## Ledger (every beat uses exactly these)

**One world, one place for everything.** Built by the local kit
`_kit/ep02.js` (on top of `CAST`), so every beat draws the same parts at
the same pixels. The canonical frame is `00_layout/`.

- **The repo** (top of the stage, y 250–600): a 4 × 4 grid of files, the
  file drawn exactly as `CAST.mapCard` draws one (teal outline, rx 6), at
  165 × 62 px, x 120–900. 16 files, never more, never moved except in
  beat 3 (into the window) and beat 8 (auth.md into the window).
- **The three files the map points to**, by grid cell (col, row):
  `auth.md` (0, 1), `api.md` (2, 0), `deploy.md` (3, 2). The file the
  agent drills into: **`auth.md`**.
- **The context window** (bottom right, x 380–920, y 700–1080): a `--panel`
  rectangle with an ink outline, label **`context`** above it in `--dim`,
  60 px. Becomes **`context rot`** in beat 4.
- **The agent**: `CAST.agent`, feet at (220, 1080), scale 0.72, left of the
  window, in every beat. **The human** (beat 2 only): `CAST.human`, feet
  at (120, 1080), scale 0.72; the agent steps right to (300, 1080) for
  that beat and back.
- **The giant AGENTS.md** (beat 5): one tall page, title `AGENTS.md`
  (monospace, 60 px), 22 dense ink lines, from the window's bottom up
  over the repo.
- **The map** (beats 1, 6–8): the `CAST.mapCard` card (panel, ink outline)
  inside the window, readable:
  ```
  AGENTS.md
  auth.md   →
  api.md    →
  deploy.md →
  ```
  monospace 60 px. Arrows run from each line's end to its file in the
  grid, `--dim` 5 px as in `CAST.mapCard`. Files it does not point to go
  dashed `--muted`, as `CAST.mapCard` draws its ghosts.
- **Order the parts are named:** map → (humans search / agents explore)
  → stuffed window → context rot → giant AGENTS.md → the map → pointers
  → files → drill into one.
- **Heroes (magenta, one at a time):** the map card (beat 1) → the
  agent's wander trail (2) → the window outline (3) → the `context rot`
  label (4) → the AGENTS.md lines as one group (5) → the map card (6–7)
  → the auth.md arrow and file (8).

## Beats (from script.md; times are vo_clean.wav seconds, final table after tightening)

| # | VO | Visual |
|---|---|---|
| 1 hook | "Context engineering is just giving your agent a map." (0.2–2.7) | Frame 0 is the payoff already working: agent left, the map card in the window, its three arrows drawing out to auth.md, api.md, deploy.md; the other 13 files dashed muted. On "map" the card goes magenta. |
| 2 | "Humans search when they know what they're looking for, but we turn to agents when we're not really sure what we need, so they end up exploring more." (3.2–8.2) | The map clears (window empty, all 16 files teal again). The human (left) points: one straight ink line to auth.md on "know what they're looking for". The agent (beside the human) on "agents": a dotted trail leaves its head and loops across file after file; on "exploring more" the trail is magenta and long, touching most of the grid. |
| 3 | "The obvious fix is to stuff everything into the context window, but that'll backfire." (9.0–12.4) | Human fades, agent steps back to its place. On "stuff everything" all 16 files fly from the grid into the window and pile up; the window outline is magenta. On "backfire" the pile spills past the window's edges, the agent leans back, eyes blink to "- -". |
| 4 | "The model doesn't really find what you're looking for. This is known as context rot." (13.1–16.4) | The pile sits still; auth.md (teal, half-buried) is the file you wanted, and it goes from teal to muted with the rest as the rot spreads up through the pile. On "rot" the label `context` becomes `context rot`, magenta. |
| 5 | "Having one giant AGENTS.md file does not work. When everything is important, nothing is. It can't cut through the noise to find what really matters." (17.8–24.4) | The pile becomes one tall `AGENTS.md` page rising out of the window over the (muted) repo, 22 dense lines. On "everything is important" every line goes magenta at once; on "nothing is" they all go muted. "Cut through the noise": a scan bar runs down the page and finds nothing; the agent tilts its head. |
| 6 | "But by creating a simple map, a map in Markdown or an index in a database, you hold pointers to files." (25.7–31.3) | On "simple map" the giant page shrinks into the short map card in the window (magenta). Its four lines type in on "Markdown". The repo comes back to teal. On "pointers to files" the three arrows draw from the card's lines to auth.md, api.md, deploy.md; the other 13 go dashed muted. |
| 7 | "You concisely let the agent navigate where it needs to go." (31.7–35.1) | The agent turns to the card and points at it; on "navigate" its gaze runs up the three arrows in turn, each file pulsing teal as it's reached. Card stays magenta. |
| 8 | "The agent reads the map and drills into only what it needs to, retrieving that part." (35.1–38.8) | "reads the map": the card's `auth.md` line underlines. On "drills into" the hero passes to the auth.md arrow and file (magenta), the card back to ink. On "retrieving" auth.md slides down into the window beside the card and opens to a few teal lines. Last frame still: the window holds the map and one file, mostly empty, the contrast with beat 3. |

**Code on screen:** the map card is the code beat, a real (shortened)
AGENTS.md map, from beat 1 and again 6–8.

**Length:** 37.7 s after pause capping. Under the 45–60 s target; the
take has nothing more to say, and padding the VO would break "say each
thing once". No *(if time)* beat: every beat is the one contrast or the
one how.

## Final beats (the contract; master = vo_final.wav seconds, 37.713 s)

Approved cut (Chris, 10/17): no phrase cuts; loudnorm only (the take is
already clean, −72 dB in pauses); pauses capped (`--max-gap 0.3`, 0.55 s
kept before "Having", 0.45 s before "But"). 38.9 → 37.7 s.

Each beat starts on `W.set(EP2.SEAM[n-1])` and ends still on
`W.set(EP2.SEAM[n])` (`_kit/ep02.js`); beat 1 starts from `EP2.MAP` with
the arrows drawing.

| # | Folder | Start | Length | VO |
|---|---|---|---|---|
| 1 | `01_hook` | 0.00 | 3.25 | Context engineering is just giving your agent a map. |
| 2 | `02_explore` | 3.25 | 5.45 | Humans search when they know what they're looking for, but we turn to agents when we're not really sure what we need, so they end up exploring more. |
| 3 | `03_stuff` | 8.70 | 3.90 | The obvious fix is to stuff everything into the context window, but that'll backfire. |
| 4 | `04_rot` | 12.60 | 3.95 | The model doesn't really find what you're looking for. This is known as context rot. |
| 5 | `05_giant` | 16.55 | 7.25 | Having one giant AGENTS.md file does not work. When everything is important, nothing is. It can't cut through the noise to find what really matters. |
| 6 | `06_map` | 23.80 | 6.15 | But by creating a simple map, a map in Markdown or an index in a database, you hold pointers to files. |
| 7 | `07_navigate` | 29.95 | 3.45 | You concisely let the agent navigate where it needs to go. |
| 8 | `08_drill` | 33.40 | 4.313 | The agent reads the map and drills into only what it needs to, retrieving that part. |
