VO script — your arc, your words
CLIP 1 — AlphaSweepMorph (trimmed ~8s) | hook
You can do more than just prompt an LLM. I took an open-weights model, looked inside to find specific concepts, and manipulated the model's weights.

CLIP 2 — ColdOpen (~16s) | artifact
(over typing of Golden Dreadken) Without prompting, I got it to say this.

(over strike-throughs) I never typed Golden. Or Kraken.

(over pivot — "Came from somewhere else") None of this came from my prompt.

Editor note: hold the final ColdOpen frame an extra ~6s for the value prop VO before cutting to Clip 3.

CLIP 2.5 — value-prop bridge (over held ColdOpen pivot frame, ~6s)
This is a way to give LLMs new capabilities without retraining them. The inside of these models has meaning we can explore — an under-explored frontier. Here's how I did it, and why it matters.

CLIP 3 — ResidualStream (~14s) | anatomy + three modes
(over the stack building) A model is a set of parameters learned from training. Your input becomes an embedding — a vector — that flows through dozens of layers. Each layer adds context. We call this flow the residual stream.

(over PROMPT mode) You can change the input.

(over FINE-TUNE mode) You can change every weight in the stack.

(over STEERING mode + arrow injecting) Or you can reach into one layer and add a single direction. That's what I did.

Editor note: if VO runs long, hold the final title frame ~3s. Or re-render with longer wait() calls in 06c_residual_stream.py (the constants and beat timings are easy to bump).

CLIP 4 — ConceptSpace (~20s) | direction encodes meaning
(over words clustering) That vector is a direction — a point in high-dimensional space. The space means different things at each layer, but the principle is the same: the direction encodes meaning. Pickle sits near cucumber. Jealousy sits near envy. Airplane is across the map. Real models do this in thousands of dimensions. Nobody hand-coded any of it.

CLIP 5 — KingQueen (~25s) | king-queen example
Take "king." Subtract "man." Add "woman." You arrive near "queen." (over the arrow translating onto king) The same direction, applied somewhere else, lands on the right thing. Meaning has shape. Shape is something you can compute with.

CLIP 6 — MeanDiff (~15s) | mean differencing
Now I need to identify a concept as a direction. The technique is called mean differencing. Here's how I did it. (over the cloud subtraction) Thirty sentences about pickles. Thirty sentences about other foods. Average each cloud. Subtract. (over the arrow drawing) What's left is the pickle direction.

CLIP 7 — AlphaSweepMorph (full, ~32s) | pickle works
Then I push along that direction. Same prompt: "My favorite food in the whole world is…" Now I turn the knob up. (no push) Pizza. (small) Pickled beets. (medium) Pickled kraut, little pickles made with sauerkraut. (maximum) Pickle pickle pickle pickle. The model can't say anything else. Same weights. Same prompt. The only thing that changed is how hard I pushed.

CLIP 8 — SantaCruz (~30s) | golden gate fails
Then I tried the same trick with the Golden Gate Bridge. Anthropic did this in 2024 — they made their model obsessed with the bridge. I tried to copy them. Same method. Thirty bridge sentences, thirty other-bridge sentences, subtract. Prompt: "My favorite place in the whole world is…" (small) Santa Cruz, California. (bigger) The place where I was born. (bigger) Physics equations. The model started spitting out cubic meters. (maximum) Just broken tokens. (beat) It never mentioned the Golden Gate Bridge. Not once.

CLIP 9 — Superposition (~30s) | why it failed
The reason is called superposition. The model has millions of concepts to store, but only a few thousand dimensions to put them in. Common things — pickle, rain, kindness — get their own clean spot. (over left side) Aim at pickle, hit pickle. (over right side) But rare specific things — like one particular bridge — don't get their own spot. They live as the overlap of California, San Francisco, famous bridge, fog. When I pulled on the Golden Gate direction, I pulled on the whole overlap.

CLIP 10 — Composition (~25s) | three together
Directions can be added. So I built three: pirate, pickle, and the Golden-Gate-ish vector. I turned all three on at once. (over Golden Dreadken materializing) And the model gave me — Golden Dreadken. The pirate ship from the cold open. "Golden" from one direction, "Kraken" from another, fused into a single word because no real word satisfied all three pulls at once. That's the signature. A made-up word is what proves steering happened. No prompt could have produced it.

CLIP 11 — Closing (~50s) | outro
So why does this matter.

(takeaway 1) Steering is a real, separate lever. It's how safety researchers hunt for deceptive behavior in models without asking nicely. It's how someday you might get a "be more concise" toggle that actually works. A whole second control surface.

(takeaway 2) AI doesn't actually know specific things the way you think. Common concepts are points. Rare ones are weather. The way the model thinks about your name, your company, your niche — that's probably not a clean concept. It's a smear.

(takeaway 3) I used the 2022 method. Subtraction. Anthropic uses sparse autoencoders — tens of thousands of cleaner concept directions. The map is getting more readable every year.

(over "The box opens") Full writeup is in the description.

Cut order (final)

1.  AlphaSweepMorph (trimmed ~8s)     opener
2.  ColdOpen                          artifact
2.5 [hold ColdOpen final frame ~6s]   value prop VO bridge
3.  ResidualStream                    anatomy + three modes
4.  ConceptSpace                      direction encodes meaning
5.  KingQueen                         king-queen example
6.  MeanDiff                          mean differencing
7.  AlphaSweepMorph (full)            pickle works
8.  SantaCruz                         golden gate fails
9.  Superposition                     why
10. Composition                       three together
11. Closing                           outro
~6:30 runtime. No SteeringVectorAddition (your outline doesn't have it — cut it). No ThirdWay (replaced by ResidualStream). No LayerSweepLandscape (your outline doesn't have it — cut it). Setup is gone (your outline doesn't have the "I failed in a genuinely interesting way" beat).

The lines that are yours, verbatim:

"You can do more than just prompt an LLM."
"I took an open-weights model, looked inside to find specific concepts, and manipulated the model's weights."
"Without prompting, I got it to say this."
"This is a way to give LLMs new capabilities without retraining them."
"An under-explored frontier."
"A model is a set of parameters learned from training."
"We call this flow the residual stream."
"The direction encodes meaning."
"The technique is called mean differencing. Here's how I did it."
Everything else is connective tissue or the existing visual's content. Tell me what to tighten further.