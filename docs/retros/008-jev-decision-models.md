# Retro: 008-jev-decision-models

**Published:** 2026-10-03 · **Length:** 55.2 s · **Raw take:** 61.9 s · **Beats:** 5 (6 built, 2 merged)

## What Chris asked to change (verbatim, in order)

| # | Request | Beat | What was actually wrong | Rule or part that was missing |
|---|---|---|---|---|
| 1 | "the opening scene looks kind of stupid just with the word Jev and a bunch of random words" | 1 | a word cloud is decoration, not the thing being explained | hook rule: frame 0 is the finished visual already working |
| 2 | "the input into Jev and then the output… looked very squished… wasn't clear what the input was" | 2 | nine pieces at the text floor in one stage; input as two lines of JSON | layout budget in the brief; merge beats when they share a visual |
| 3 | "it's a little unclear what is the closed captioning" (collides with white diagram text) | all | captions and labels were the same weight and color | caption pill + bold (now a token and in `short_caption`) |
| 4 | "server down, yes, no, later doesn't really make sense for those options" | 1, 3, 6 | the example wasn't a real decision | storyboard: the example must be a decision someone would make |
| 5 | "gray overlapping the green triangles… move the arrow underneath" | 5 | arrow tips ended under box strokes | `ARROW_GAP` in `transformer.py` |
| 6 | "change text to I can't log in. Drop the cheap pills part" | 1, 3 | example text | (taste) |
| 7 | "make it look more like Jev is a child of the subset of a decision model" | 5 | a badge on a corner doesn't read as "is-a" | a tree reads as "is-a"; a badge reads as "brand" |
| 8 | "give a little bit more space to that whole window, the text looks squished" | 3 | two halves plus a tag plus a counter under the net | drop the tag; counters on the title row; budget first |
| 9 | "Drop the 171ms vs 1s line from there too" | 3 | numbers on screen in a 60 s Short | numbers go in the description |

## What the agents reported wishing existed

- A values-off mode for bars (added), name column sized to names (added).
- A way to avoid the "new VGroup .animate hides labels" trap (`_marks.restroke`, 007).
- An updater-safe clock (scene time only advances at play boundaries; 04_agents overrides `play`).

## What changed in the system because of this video

| Change | Where it went |
|---|---|
| Captions bold on a dark pill | `style.py` (`SHORT_CAPTION_WEIGHT`, `CAPTION_PILL_*`), `base.short_caption`, `STYLE.md`, runbook step 7, tests |
| Diagram rows get air: tighter box pad, smaller ⊕, bottom bleed; arrows clear box strokes | `transformer.py`, tests |
| Hand-off pack; no pinned comments | runbook steps 9–10 |
| Preflight reduced to one question | `content-preflight` skill |
| Parallel renders race; finals use `--disable_caching`; VGroup-animate label trap | `STYLE.md`, runbook step 6 |

## Parts

- New local parts: `_parts.py` (ProbBars, text_card, chip_text, mono), net glyph + token stream, decision loop.
- Reused: `transformer.build_block` (3rd video), `chip_text` across 4 beats.
- Promoted: none yet; `ghostify` and the computational graph are at two uses.

## Still open

- No layout check before render; every item above was visible on a sheet.
- Frame 0 carries no on-screen question text.
- The recorded take dropped the last script line (frontier-LLM labeling); storyboards should mark the last line as "if time".
