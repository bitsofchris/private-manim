ENGINE: hyperframes

# Is AI Making Us Dumber? Stop Keeping Agents Busy (Harness ep 4): storyboard

THE QUESTION: "I run more agents than ever; why don't I feel better at my work?"
WHO IS ASKING: an engineer who uses coding agents (Claude Code, Codex)
every day and is reviewing more agent output than they can absorb.
THE ANSWER IN ONE SENTENCE: the goal is not to keep agents busy, it's to
maximize the rate at which you understand things.
THE SEARCH PHRASE: is ai making us dumber (YouTube autocomplete, checked
10/17 in `../SERIES.md`). It goes in the title; VO line 1 is the answer.

What the viewer does after: go fast on what teaches you nothing, slow on
the core; block a slot in the day to do the work yourself.

**One idea:** agents' finished work piles up faster than you can
understand it; the human's own handwritten sheet is the thing that grows
you.

**Engine:** HyperFrames, the series look (`../SERIES.md` "The look"):
the shared cast kit `videos/_shared/web/cast/cast.js`, plus one local
scene kit `_kit/desk.js` (desk, pile, the human's sheet, code card, day
strip; listed in the hand-off, not added to the shared kit).

VO is `script.md` (what Chris said), not reworded.

## Ledger (every beat uses exactly these; the numbers live in `_kit/desk.js`)

- **One scene, never cut away.** Floor at y 1010. The **human** (`CAST.human`)
  at x 215, scale 0.9, behind a standing **desk** (top y 822, x 268–682).
  Two **agents** (`CAST.agent`) on the right at x 790 and 900, scale 0.62.
- **The human's own sheet** (ink, propped on the desk at x 300–466, y 566–814)
  with up to 5 handwritten lines. It is what the human understands. Ink at
  rest; magenta when the beat points at understanding.
- **The pile**: the agents' finished pages, teal slabs stacked on the desk
  at x ~500–650, up to 28 high (top y ~310). Pages fly from an agent's
  left hand to the top of the pile (`CAST.page` at 0.24), A and B in turn.
  The pile count is driven by one global `flow` number, continuous across cuts.
- **The code card** (beats 5–6 only): top of the stage, x 72–944, y 252–466.
  Line 1, teal, typed by the agent: `train(model, data)` (the plumbing;
  in beat 6 it flicks through `dl = DataLoader(ds)` and `log(step, loss)`).
  Line 2, handwritten in by the human: `softmax(q @ k.T)` (the core idea,
  attention, from Karpathy's course). Monospace set from the script.
- **The day strip** (beats 8–9 only): top right, "today" over five slots;
  slot 2 is the one that gets blocked (magenta).
- Faces: human smiles at rest, frowns under the pile (beat 3), flat while
  struggling (beat 6), smiles at the end.
- Order of the heroes: the understood bar (1b) → the pile (3) → the sheet (4) → the
  core line (5–6) → the sheet (7) → the blocked slot (8–9). One at a time.
- **The meters** (beats 1b–2, Chris 10/17: the pile ran 13 s straight): two bars on a baseline, "output" (teal) at x 330 and "understood" (ink; magenta as hero) at x 690, base y 1000, full height 680. The desk is hidden while they're up.
- No other text on screen besides the meter labels, the code card and "today": captions carry the words.

## Layout

Stage y 230–1100: code card / day strip y 252–650, figures and desk y 546–1010.
Caption band y 1100–1536 stays empty (`assemble.py` burns the captions).

## Beats (VO from script.md; final times below)

| # | Folder | VO (as recorded) | Visual (9:16) | Hero |
|---|---|---|---|---|
| 1 | `01_hook` | The goal is not to keep agents busy. | Frame 0, already moving: both agents throwing pages onto a small pile beside the human, who writes on their sheet. The stream runs through the cut. | none |
| 1b | `01b_meters` | It's to maximize the rate at which you can understand things. | The desk fades back; two bars take the stage on one baseline: "output" (teal, already tall) and "understood" (short). "understand things": the understood bar climbs and turns magenta. | the understood bar |
| 2 | `02_obsidian` | A while back I made a video about how I use Obsidian to keep agents working for me. | The meters only. Understood back to ink. "keep agents working for me": the output bar shoots to the top; understood stays put. | none |
| 3 | `03_bottleneck` | But the bottleneck has become me reviewing and understanding everything. | The bars sink and the desk returns with the tall pile (0.35 s). "bottleneck": the pile turns magenta and towers (top y ~310); the human leans back, frowns; the sheet goes muted. | the pile |
| 4 | `04_two_speeds` | Now, sometimes it's useful to optimize for output, but other times you want to go slow so you can deliberately understand things. | "optimize for output": the pile goes teal, the stream runs. "go slow": the stream stops, the agents lower their arms, the pile slides off the desk and fades. "deliberately understand": the sheet comes back and turns magenta; the human writes. | the sheet |
| 5 | `05_karpathy` | When I'm working through Karpathy's LLM lecture course, the agent writes the plumbing, but I write the core idea myself. That's the part I want to understand. | The code card drops in at the top; the sheet back to ink. "the agent writes the plumbing": agent A raises an arm and line 1 types in, teal. "I write the core idea myself": line 2 writes in left to right in magenta while the human writes. "the part I want to understand": line 2 pulses once. | the core line |
| 6 | `06_fast_slow` | So go fast on the parts that teach you nothing, but go slow on the core part that you're meant to struggle with. | "go fast": line 1 flicks quickly through the three plumbing lines. "go slow on the core": an underline draws slowly under line 2. "struggle with": the human tilts their head, face flat, hand to head. | the core line |
| 7 | `07_do_the_work` | Now, AI can't make you smarter on its own. You have to do that work. Keeping them busy is not the goal. | The code card fades. "can't make you smarter on its own": the agents stand at rest, blink. "do that work": the sheet turns magenta and a new line writes in. "not the goal": the agents stay idle; the human keeps writing. | the sheet |
| 8 | `08_block_a_slot` | Make sure you carve out time for your own growth. Block a slot on your day where you do the work, | The day strip slides in top right; the sheet back to ink. "Block a slot": slot 2 fills magenta. | the slot |
| 9 | `09_by_hand` | where you write something by hand, read it slowly, do the deep thinking, and are not just trying to keep agents busy. | "write something by hand": the last line writes in. "read it slowly": the human leans to the sheet. "deep thinking": hand to chin. "not just trying to keep agents busy": the agents blink at rest; the human smiles. Still before the end. | the slot |

Code beat: beat 5–6's two lines. The "how" of the episode is "the agent
writes the plumbing, I write the core", and one line of each shows it.

## Final beats (the contract; `vo_final.wav` 47.49 s, master seconds)

Beat brief for the agents: `BRIEF.md` (seam states `DESK.SEAM`, starts
`DESK.START` in `_kit/desk.js`). Word times: `words.json`.

| # | Folder | Start | Length | VO |
|---|---|---:|---:|---|
| 1 | `01_hook` | 0.00 | 2.50 | The goal is not to keep agents busy. |
| 1b | `01b_meters` | 2.50 | 3.00 | It's to maximize the rate at which you can understand things. |
| 2 | `02_obsidian` | 5.50 | 4.50 | A while back I made a video about how I use Obsidian to keep agents working for me. |
| 3 | `03_bottleneck` | 10.00 | 3.10 | But the bottleneck has become me reviewing and understanding everything. |
| 4 | `04_two_speeds` | 13.10 | 5.75 | Now, sometimes it's useful to optimize for output, but other times you want to go slow so you can deliberately understand things. |
| 5 | `05_karpathy` | 18.85 | 7.90 | When I'm working through Karpathy's LLM lecture course, the agent writes the plumbing, but I write the core idea myself. That's the part I want to understand. |
| 6 | `06_fast_slow` | 26.75 | 5.45 | So go fast on the parts that teach you nothing, but go slow on the core part that you're meant to struggle with. |
| 7 | `07_do_the_work` | 32.20 | 4.85 | Now, AI can't make you smarter on its own. You have to do that work. Keeping them busy is not the goal. |
| 8 | `08_block_a_slot` | 37.05 | 4.75 | Make sure you carve out time for your own growth. Block a slot on your day where you do the work, |
| 9 | `09_by_hand` | 41.80 | 5.686 | where you write something by hand, read it slowly, do the deep thinking, and are not just trying to keep agents busy. |

## Cut list (approved by Chris, 10/17; applied)

Raw take 50.9 s, already clean (noise floor −69 dB, loudness range
4.2 LU), so step 3 is loudnorm only (−14 LUFS). No phrase cuts: the take
has no flubs or repeated phrases (Parakeet and a WhisperKit sub-clip
both hear "Karpathy's", no stray "a").

| # | Cut | Saves |
|---|---|---:|
| 1 | Cap every pause at 0.25 s (`--max-gap 0.25 --noise=-45dB`); the longest were 1.96 s after "do that work", 1.23 s after "want to understand", 1.0 s after "deliberately understand things" | 3.4 s |

Result: **47.5 s**. Trial-cut and re-transcribed with Parakeet: every
join reads clean.

Flagged, not cut (Chris: keep it):
- "Keeping them busy is not the goal." (≈ 1.9 s) restates line 1 and the
  closer's "not just trying to keep agents busy". Cutting it gives
  ≈ 45.6 s and the closer still lands.
