# kb-graph: the knowledge base grows under the gameplay

**Name:** kb-graph (mockup for the AugiCraft diamond-run Short)

**Description:** a 9:16 Short where the top of the frame is a timelapse of
the AgentMiner bot playing Minecraft and the bottom is its knowledge base
as a growing Obsidian-style graph. Each new skill or lesson pops up as a
card over the footage, holds, then shrinks and flies down into its node.

**When to use:** the diamond-run Short (augi-craft, 2026-10-20), and any
"watch an agent learn" clip where the learning has timestamps.

**How it works:** one composition, one `render(t)` driver (`ISO.start`).
Every event carries its wall-clock time from the run; one piecewise time
map turns clock time into video time, and the same map cuts the timelapse,
so the cards land on the footage they describe.

## The story (57.5 s, the current cut)

One request, then the run: the first handoff and "now go get me 5 more"
(09:05-09:07) are cut. Times come from `edit.json` (the selects in
`~/Creating/augicraft-diamond-run/SELECTS.md`).

| Video | Shot | On screen |
|---|---|---|
| 0-3 | S01 chopping a tree | hook "get me 5 diamonds" (0-2); card chop-logs |
| 3-6 | S02 the new crafting table | wooden pickaxe slot; cards craft-item, lesson craft-one-at-a-time |
| 6-10 | S03 x-ray view down the pit | card mine-blocks |
| 10-12 | S15 by the table after the stone pickaxe | chip stone pickaxe, stone slot; card ensure-table |
| 12-16 | S16 mining a tunnel, iron ore in view (slowed on the ore) | chip found iron |
| 16-18 | S04 the lit furnace | chip smelting iron; card smelt-items |
| 18-21 | S05 digging down | chip iron pickaxe, iron slot |
| 21-28 | S06 the diamond ore | chip diamond #1, card descend-scan-ore |
| 28-33.5 | S14 down a shaft, into water, underwater | chip hit water |
| 33.5-35.5 | S09 "AgentMiner drowned" | chip drowned |
| 35.5-40.5 | S10 the safe staircase | card staircase-down |
| 40.5-43 | S13 still at the bottom of the mine | chip 5 diamonds (the ores themselves are hidden behind its head) |
| 43-47 | S13 up the stairs into daylight | cards DROPPED descend-scan-ore, lesson check-movement-progress |
| 47-48 | S11 back at spawn | craft-item and ensure-table validated |
| 48-56.5 | S12 the five tosses | "give me the diamonds", card give-item-to-player, counter 1 → 5 diamonds given (stepping when Chris's hotbar count ticked up); last episode and give-item-to-player validated right after the fifth toss |
| 56.5-57.5 | hold on AgentMiner | |

A tool strip under the chips (top left) holds three pickaxe slots, dim until
wood (08:40:47), stone (08:41:55) and iron (08:48:38) arrive; their material
colours are the game's, not house tokens.

Cards whose real time falls in a cut-out stretch are shown on the shot where
that skill was used; `index.html` keeps each one's real time in a comment
(chop-logs, craft-item, craft-one-at-a-time, mine-blocks, ensure-table,
smelt-items, descend-scan-ore, give-item-to-player, and the 09:17 group:
the dropped skill, the movement lesson, its episode and two validations,
written at 09:17:19-36 just after the climb, shown during it; and the last
episode and validation, written at 09:22:12-19, shown right after the fifth toss).

## Sound

Chris's voiceover (four lines) over a YouTube Audio Library track
(`~/Creating/augicraft-diamond-run/Track.mp3`), no captions band: the graph
owns the bottom, so the captions sit over the footage at y 690.

1. Render the picture (`index.html`) to `out/augicraft-diamond-short.mp4`.
2. `./make_audio.sh`: cleans the take (high-pass, -14 LUFS), levels each line
   to the same speech RMS, places it at its video time (`PLACE`; lines 3 and 4 and the drowning dip are tied to run-clock moments through the edit's map, so they follow edits), ducks the
   music under the voice (sidechain), dips the music during the drowning,
   fades it in and out, two-pass loudnorm to -14 LUFS, and muxes
   `out/augicraft-diamond-short-sound.mp4`. It also writes `out/vo_final.txt`.
3. `uv run --no-sync --project ../../.. python ../../../tools/word_times.py out/vo_final.txt out/vo_final.wav -o out/words.json`
4. `python3 make_captions.py` writes `footage/captions.js` (up to 3 words a
   caption); the drowning line's word times are set by hand there, because
   the estimate missed the pause after "drowned". Render again, then run
   `./make_audio.sh` again to put the sound on the new render.

## Layout (1080 × 1920)

- **Footage:** y 0–1080, a square crop of the game window (the recordings
  are full-screen captures of a windowed Minecraft). Clock top right and
  milestone chips top left, both at y 250 (below the top dead zone). The
  clock is run time since AgentMiner joined (0:00 = 08:38:59), read through
  the same map, so it jumps at each cut.
  Chat lines as pills near the bottom of the footage.
- **Card:** over the top of the graph panel (y 1030 to about 1400, so it
  covers only the bottom 50 px of the footage), the one magenta hero: kind
  (NEW SKILL / LESSON / DROPPED), the note's id in monospace, a one-line
  blurb. In 0.25 s, held ~1 s, then 0.6 s into its node.
- **Graph:** y 1100–1536 (the caption band; this Short has no VO, so the
  cards are the text). Header: SKILLS and VALIDATED counters.
  Nodes: helpers teal, lessons ink rings, episodes small dim dots.
  The node that just landed stays magenta until the next card.
  Validated: a teal ring. Dropped: muted and dashed.
  Edges come from the notes' front matter (evidence episodes,
  `depends_on`, helper calls, supersedes); Obsidian does not draw these
  because the notes have no `[[wikilinks]]`.
- **No labels in the graph:** 60 px labels on 15 nodes would not fit the
  band, and the card already named the note.

## Mockup vs the real build

The mockup uses seven stills from the recordings with a slow zoom,
hand-placed node positions and event data copied from the run.

For the real Short:
1. **Data:** a script in augi-craft that exports `events.json` from the
   knowledge directory (TIMELINE.md, the front-matter edges, git commit
   times) and the bot's inventory milestones from its session transcript.
   The composition reads it inline (no `fetch`).
2. **Timelapse:** one `edit.json` with the time-map segments, used by both
   the composition and an ffmpeg cut of the two recordings
   (08:34:41 + 36.6 min, 09:13:24 + 8.3 min; gap 09:11:15–09:13:24).
   Cut out the shots where the camera sits inside the bot's head or a wall.
3. **Compositing:** check whether HyperFrames 0.8.115 seeks a local
   `<video>` frame-accurately. If not, render the overlay as WebM with alpha
   and put it over the timelapse with ffmpeg.

## Open questions for Chris

- VO or silent? With VO the captions need the band, and the graph has to
  move up or shrink.
- Speed: one even ×40, or the uneven map above (fast through idle, slower
  at the drowning and the diamonds)?
- Episodes as nodes, or skills and lessons only?
