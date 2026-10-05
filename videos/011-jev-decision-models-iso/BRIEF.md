# Beat brief: 011-jev-decision-models-iso

**Name:** jev-decision-models-iso-beat-brief
**Description:** The contract for rebuilding `videos/008-jev-decision-models`
("What is Jev and why is everyone so excited?", 55.15 s) in the isometric
HyperFrames house style, over the same voice-over, cut and captions.
**When to use:** you were handed this path plus one or two beats.
**How it works:** copy `00_layout/` (the shared parts at rest), build your
beat as a pure `render(t)` function with the kits, check, render to
`media/hf/`, review your own contact sheet against the VO, report.

## Read first

1. `agents/beat-brief-hyperframes.md` — the technical rules, including "What
   `check` and the renderer trip on". All of it applies.
2. `videos/009-transformer-short-iso/_iso/iso.js` (linked into each beat as
   `iso/`) — the isometric kit: projection `ISO.P`, palette, `ground`, `box`,
   `poly`, ring slabs, `label`, `start`, easing.
3. `videos/011-jev-decision-models-iso/_jev/jev.js` (linked as `jev/`) — this
   video's parts and its fixed example: `JV.pillars` + `JV.makePillarLabels`
   (the probability pillars), `JV.slab` + `JV.planeLabel` (a machine with a
   label on its front face), `JV.card` (flat cards and chips), and the
   constants `CHOICES`, `TICKET`, `FINAL_PROBS`, `STREAM`.
4. `videos/011-jev-decision-models-iso/00_layout/index.html` — the starting
   file; `media/hf/00_layout.png` shows what it draws.
5. Your beat in `videos/008-jev-decision-models/` (`NN_name.py`): its
   docstring and `T_*` cue constants say what each VO phrase must show;
   `storyboard.md` there has the "Final beats" table, the ledger of example
   values and the reasons for what is and is not on screen.
6. A finished Short in this style, for how a beat file is organised:
   `videos/009-transformer-short-iso/` and `videos/010-diagram-grammar-iso/`.

## The look

An isometric world on the house navy with a faint floor grid (as 009 and
010). Things are solid: a model is a slab with its name on the front face, a
probability is the height of a pillar, data falls **down** through a machine
(input in at the top, result out below). Flat text only for what must be
read. One magenta hero per beat (`ISO.COL.hero`), the one the 008 docstring
names; when the beat moves on it returns to its resting colour.

The three choices keep their colours everywhere: `bug` teal, `query` blue,
`spam` gold (`JV.CHOICE_COL`): pillar, name, chip and any small copy of it.

## Accuracy (this Short states facts about a real product)

Everything on screen comes from 008's ledger; invent nothing.

- The example: the ticket `I can't log in`, the choices `bug` / `query` /
  `spam`, the result 0.91 / 0.06 / 0.03. Under the hook question two other
  tickets drop in (`order status?`, `wrong size`) and the pillars refill with
  different values each time: `JV.CYCLE_INPUTS` / `JV.CYCLE_PROBS`
  (illustrative, as in 008, where they were random draws).
- A decision model returns **a probability for each choice, in one pass**.
  An LLM decides by generating **token by token, one pass through the whole
  model per token**. The pass counters must count exactly that: one tick per
  glyph typed for the LLM (the stream is `JV.STREAM`, 30 glyphs), exactly
  **1** for the decision model.
- No latency, cost or accuracy numbers on screen (008 moved them to the
  description). The word "calibrated" never appears on screen.
- Beat 5: Jev is one company's implementation of a decision model; the open
  models named are `Laya` and `CLM-8B`. The decision head sits **on top of**
  the frozen stack, in place of the LM head (`Linear`). The stack is the
  accurate transformer figure from 010 (`_diagram/diagram.js`, bottom to top;
  do not restyle its marks or reverse its flow).
- Beat 6: the confident readout is `0.92` beside a coin that is really
  `50/50` (the fair-coin test from the sources).

## Beats (folders keep 008's scene names)

| Beat | Folder | Master start | `BEAT_SECONDS` | VO |
|---|---|---:|---:|---|
| 1+2 Hook and what it is | `01_hook` | 0.00 | 10.14 | What is Jev and why is everyone so excited about it? Jev is a decision model. You give it some input and a fixed set of choices, and it gives you back a probability for each choice. |
| 3 One pass | `03_onepass` | 10.14 | 13.11 | This is exciting 'cause this is much more efficient than what an LLM does. An LLM decides by generating token by token, and every token is another pass through the whole model. Jev scores all the choices in one single pass, so it's fast and cheap. |
| 4 Agents | `04_agents` | 23.25 | 10.53 | Now that matters because agents make a lot of decisions. Which tool should I use? Is this action allowed? Am I done yet? Each one is a choice from a fixed set of options, and that's what a classifier does. |
| 5 Decision head | `05_head` | 33.78 | 13.69 | Jev is one company's version, a specific implementation of this decision model as a classifier. But the bigger idea is that we've gotten really good at building rich representations with language models, and a decision model is just a classifier on top of them. Anyone can train one. |
| 6 Your own labels | `06_labels` | 47.47 | 7.682 | The hard part is calibration. The probabilities only mean something on data like your own, so you need your own labels. |

As in 008, each beat is its own composition and the assembler hard-cuts
between them; there is no shared frame to match. Each beat's frame 0 already
shows its finished layout with something moving, and its last ~0.3 s is
still. Beat 6's last frame is the last frame of the Short.

**1+2 Hook** — the machine itself from frame 0: a magenta `Jev` slab (the
hero) with the three pillars below it; an input card is already dropping
into the top of the machine, and the pillars refill for each ticket (two
cycles under the question). "decision model": the machine widens and the
words join `Jev` on its face. "some input": the ticket `I can't log in`
stops above the machine. "fixed set of choices": three chips `bug` `query`
`spam` (in their colours) line up between the card and the machine.
"a probability for each choice": card and chips go in and the pillars fill
to 0.91 / 0.06 / 0.03 for good.

**3 One pass** — the stage is split, `LLM` above and `Jev` below, each a
small stack of slabs with a pass counter (`passes N`, flat text). Above: the
LLM's answer types one glyph at a time (`JV.STREAM`, monospace card); every
glyph pulses the LLM stack once (cyan / teal, not magenta) and ticks its
counter. Below, on "Jev": the ticket and the three choices go into the Jev
stack once: one magenta flash, `passes 1` in magenta (the hero), and the
three pillars fill together by "pass". "fast and cheap": hold; the contrast
between the two counters is the point.

**4 Agents** — an agent loop drawn on the floor as a ring with a teal token
riding it. "decisions": three decision posts appear on the ring. Each
question lights its post magenta and hangs a chip on it: `which tool?`,
`allowed?`, `done?`. "a choice from a fixed set": each post shows its
options as small blocks (3, 2, 2). "classifier": the probability pillars
rise in the middle of the loop.

**5 Decision head** — frame 0: a `decision model` slab with a magenta `Jev`
chip hanging from it as its child. "bigger idea": the slab opens into the
dim transformer figure (`DG.draw`), and Jev moves to a badge row. "rich
representations": the teal flow pulses up the figure. "classifier ... on top
of them": the top box becomes the magenta `decision head` (the hero), fed by
the arrow from the stack. "Anyone can train one": badges `Laya` and `CLM-8B`
join `Jev`.

**6 Your own labels** — frame 0: the pillars filling (0.91 / 0.06 / 0.03).
"calibration": a magenta `0.92` readout beside a coin that flips and reads
`50/50`; both go before "data". "data like your own": a scatter of small
teal data blocks lands on the floor. "your own labels": a magenta tag stamps
onto each. Hero: the readout, then the tags.

## Rules specific to this video

- **Do not edit `_jev/jev.js`, `00_layout/`, or the kits in 009 and 010.**
  Need something they lack: write a local function and name it in the report.
- Set up a beat folder from the video folder:
  `mkdir NN_name && cp 00_layout/index.html NN_name/index.html && ln -s ../../_shared/web/vendor NN_name/vendor && ln -s ../../009-transformer-short-iso/_iso NN_name/iso && ln -s ../_jev NN_name/jev`
  (beat 5 also: `ln -s ../../010-diagram-grammar-iso/_diagram NN_name/diagram`
  and a `<script src="diagram/diagram.js">` after `iso.js`). Keep the script
  lines and the literal `window.__timelines["main"] = ISO.start(BEAT_SECONDS, render);`.
  Set `data-duration` to your `BEAT_SECONDS`.
- Budget the layout before drawing. Stage y 230-1100, text and the hero
  inside x 65-950; the band y 1100-1536 stays empty (captions are burned in
  there). Flat text at least 60 px (Inter ExtraBold is about 38 px a
  character at 64 px; generic `monospace` works and is narrower). A pillar
  at probability 0.91 with the default `H: 300` is 280 px tall: lower `H` or
  move things so it never runs into what is above it.
- Painter's order on the canvas: draw back to front. Flat DOM text sits on
  top of the canvas; a canvas-only beat fails `check` with `sweep_static`,
  so some DOM element must change during the beat (the pillar values do).
- Cues come from the audio: `videos/008-jev-decision-models/vo_final.wav`,
  your window is master start to start + `BEAT_SECONDS`;
  `videos/008-jev-decision-models/captions.json` has word-group times on the
  master timeline; the `T_*` constants in the 008 scene are already
  measured. Cues are named constants with the word in a comment.
- Commands, from your beat folder:
  ```
  export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1
  npx --yes --prefer-offline hyperframes@0.8.115 check
  npx --yes --prefer-offline hyperframes@0.8.115 render -o ../media/hf/NN_name.mp4
  cd .. && ../../tools/review_frames.sh media/hf/NN_name.mp4 4 12 media/hf/NN_name_sheet.png
  ```
  Open the sheet with the Read tool. `check` must end "Check passed". Up to
  three render-and-review rounds per beat.
- Never run `hyperframes init / add / catalog / skills / publish / cloud /
  lambda / tts / transcribe / models` or any `npm install`. Do not commit.

## Report

Per beat: cue constants with their VO word, the mp4 path and measured
duration, the `check` result, the first and last frame, anything changed
from this brief and why, any place the picture could be read as inaccurate,
and local helpers that should move into a kit.
