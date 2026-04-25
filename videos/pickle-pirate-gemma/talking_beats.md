# Talking beats — pickle-pirate-gemma animations

One section per animation. For each: what we're seeing on screen, what it means, why it belongs in the blog post, and what I was reasoning about when I chose this framing.

---

## 01 — `steering_vector_addition.mp4`

**Source:** [01_steering_vector_addition.py](01_steering_vector_addition.py) → `media/videos/01_steering_vector_addition/1080p30/SteeringVectorAddition.mp4`

### What we're seeing

A 2D plane. Three arrows:

- A white arrow `h` from the origin — this stands in for the residual stream at layer 21 (the running "thought vector" the model is carrying at that layer).
- A blue arrow `û` — the unit steering vector, computed as `mean(pickle sentences) − mean(other sentences)`, then normalized. It points in "the pickle direction."
- An orange arrow `h + inject` — the steered residual. As the α knob turns from 0 → 10 (shown top-right), we literally add a scaled copy of `û` to the tip of `h`. The orange arrow swings away from the white dashed ghost of the original `h` and leans toward blue.

Below the plane, the caption swaps in the real generated completion at three α values (0, 4, 10) — from the harness, prompt *"My favorite food in the whole world is…"*:

- α=0: "pizza. I have this craving for pizza…"
- α=4: "pickled kraut…just little pickles made with sauerkraut"
- α=10: "pickled they pickle pickles they pickle pickles they…"

### What it means

Steering isn't a prompt. It isn't fine-tuning. It's a single line of code at inference time:

```
h ← h + α · 0.1 · ‖h‖ · û
```

We take the model's current thought, and we push it — a little, or a lot — in a direction we extracted from data. The geometry in the animation is the geometry in the code. The orange arrow *is* the new residual stream, at the moment we hand it back to the next transformer layer.

The `0.1 · ‖h‖` is the reason we can get away with this: the injection is scaled to a fraction of the typical norm at that layer, so at α=1 it's a nudge, and at α=10 it's a shove that overwhelms whatever `h` was trying to say.

### Why it's relevant

This is the opener. Before anyone believes that the model becomes obsessed with pickles, they have to believe that "adding a vector" is a real thing you can do to a language model. Showing literal 2D vector addition with a visibly tilting arrow is the fastest way to get a reader from *"that sounds like magic"* to *"oh — it's just addition."*

### What I was reasoning about

- **Why 2D and not a real PCA projection here:** this scene is about the *operation*, not the data. Cluttering it with real 2304-D geometry collapsed to 2D invites the question "is that rotation real or PCA noise?" — which I actually want for scene #3, but not yet. The cartoon angles are chosen so the tilt is obvious.
- **Why the ghost dashed line for original `h`:** without it, the orange arrow just "moves" and the viewer loses the reference. With the ghost, the rotation *away* from `h` is the story.
- **Why three captions, not six:** the three I picked map cleanly to "coherent / on-theme / broken." More captions would make the same point with more noise.

---

## 02 — `alpha_sweep_morph.mp4`

**Source:** [02_alpha_sweep_morph.py](02_alpha_sweep_morph.py) → `media/videos/02_alpha_sweep_morph/1080p30/AlphaSweepMorph.mp4`

### What we're seeing

The prompt *"My favorite food in the whole world is"* stays pinned to the top. A rectangular text panel holds the model's completion. On the right, a half-circle dial reads α, and a vertical bar tracks ‖inject‖.

We step through α ∈ {0, 2, 4, 6, 8, 10}. At each step the dial rotates, the bar grows (blue when we're still coherent, orange once we're over the cliff), and the completion retypes itself with the **real** output from `runs.jsonl` at that α:

- 0: "pizza. I have this craving for pizza…"
- 2: "pork rinds…they are a pickle they're made from pork skin"
- 4: "pickled kraut…little pickles made with sauerkraut"
- 6: "pickled kra kra… they's known as they's known as they's…"
- 8: "pickled kra they… they are very pickle they pickles they pickle…"
- 10: "pickled they pickle pickles they pickle pickles they pickle…"

The final frame fades to three giant "pickles" in orange, then they fade out.

### What it means

You can watch the model lose the plot in real time. At α=2 it's still writing sentences, but pork rinds are mysteriously "a pickle." By α=4 it's a coherent (if weird) cooking blog about sauerkraut. By α=8 grammar is crumbling. By α=10 there are no sentences — just *pickles*, on loop. The same model, same prompt, same weights, same seed. The only thing that changes is how hard we push in one direction of activation space.

The ‖inject‖ bar shows *why*: at α=10 we're adding a vector of magnitude `10 · 0.1 · 446 ≈ 446` on top of a residual whose own norm is `446`. We've effectively replaced the model's thought with the pickle direction. So of course it can only think pickles.

### Why it's relevant

Everything in the blog post is downstream of this clip. If you're going to read 2,000 words about mean-difference vectors, you need to have already *felt* what steering does. The point of this scene is not to explain — it's to make someone text a friend "wait, you need to see this."

### What I was reasoning about

- **Why retype the full completion and not animate token-by-token generation:** we don't have token-level probabilities logged, only final strings. Making up per-token progress bars would be fake data dressed as truth. Retyping the finished string keeps every word on screen honest.
- **Why the bar changes color at α=5:** there's no principled threshold in the data, but subjectively α≥6 is where grammar breaks. Color gives a silent "you're in trouble now" without a caption.
- **Why the triple-pickles outro and not just a freeze-frame:** the completion at α=10 is *already* three pickles per line; blowing one word up to 64pt makes the joke land instead of requiring the viewer to re-read small text.

---

## 03 — `pca_with_steering_arrow.mp4`

**Source:** [03_pca_with_steering_arrow.py](03_pca_with_steering_arrow.py) → `media/videos/03_pca_with_steering_arrow/1080p30/PCAWithSteeringArrow.mp4`

Three acts in one clip.

### Act 1 — pickles, full canvas

**What we're seeing.** A single 2D plane. A legend in the corner tells the viewer what the colored dots are: **blue = "pickle" sentences** (*"Pickles are my favorite snack any time of day."*), **orange = matched "food" sentences** (*"Pizza is my favorite meal any time of day."*). One example of each pair flies in as a fat labeled dot. Then the remaining 29 pairs fade in and shrink the example dots to match. A caption at the bottom steps through the method:

1. *"30 sentences of each, encoded and projected to 2D."*
2. *"Take the mean of each cloud."* → two big centroids pop in.
3. *"Subtract. The arrow IS the steering vector — the 'pickle direction.'"* → yellow diff arrow appears from orange centroid to blue centroid.
4. Verdict: **"clouds cleanly separated → sharp steering signal."**

**What it means.** This is the entire recipe. No gradient descent, no fine-tuning, no probes. You collect 30+30 matched sentences, mean each cluster of their last-token residuals, subtract. Whatever direction that arrow points is your steering vector. The reason it works for pickles is right there in the picture: the clouds don't overlap, so the arrow *between* them is a direction that the clouds themselves don't already vary along much.

**Why it's relevant.** This is where a reader who's been carried along by animations 1 and 2 finally sees where the magic vector came from. Until this scene the steering direction is a *given*; after this scene it's something they could collect themselves over a weekend.

### Act 2 — golden_gate v1, full canvas

**What we're seeing.** Same template. Legend updates: **blue = "Golden Gate Bridge sentences"** (*"The Golden Gate Bridge stretches across San Francisco Bay."*), **orange = generic SF / bridge sentences** (*"The Bay Bridge stretches across San Francisco to Oakland."*). The example pair flies in and the two dots land *close together* — minimal-pair sentences produce near-identical residuals. A quiet note: *"Notice the sentences only differ in one phrase — the model's residual barely moves."*

The remaining 30+30 come in, the clouds overlap, centroids are near each other, the diff arrow is short. Verdict: **"clouds overlap → fuzzy direction, fuzzy steering."**

**What it means.** The GG v1 pairs were *too similar*. The only thing that varies between positive and negative sentences is whether "Golden Gate Bridge" or "Bay Bridge" (or similar) appears — so the mean-difference direction picks up on whatever tiny delta those word substitutions produce, which turns out to be mostly "coastal California vibes" and not "the bridge itself." Same method. Noisier inputs. Noisier output.

**Why it's relevant.** This is the scene that makes mean-difference *falsifiable*. If the diff arrow is short and fuzzy, your steering won't land. That's a design check you can run on your pairs before you even touch the model.

### Act 3 — side by side

**What we're seeing.** Both plots shrink to half-panels. Under each, a line quoting the **actual generation at layer 21, α = 4** from `runs.jsonl`:

- pickles → *"…pickled kraut, little pickles made with sauerkraut…"*
- golden_gate → *"…the beach. I was born in a coastal town, so I grew up on the beach…"*

Closing caption: *"sharp cloud separation → sharp concept. fuzzy clouds → fuzzy concept."*

**What it means.** The geometry we just inspected and the behavior we saw in scene 2 are not two separate stories. They're the same story. A clean separation between clouds *is* a clean control knob; a fuzzy separation *is* a fuzzy control knob. The generations are the receipt.

**Why it's relevant.** It earns the transition to the rest of the post. Anything that follows — the layer sweep, the composition finale — is downstream of this causal link: *cluster geometry → steerability.*

### What I was reasoning about

- **Why walk through the method step-by-step in Act 1 instead of showing all 60 dots at once:** the viewer needs to understand that each dot is a *sentence encoded at a specific layer*, not a mystery PCA token. Showing one labeled example pair first makes every other dot readable, even the ones whose captions we don't show.
- **Why minimal-pair example sentences that land *close*, on purpose, in Act 2:** that closeness is the story. The reason GG v1 drifted is visible the moment you see the two example dots next to each other.
- **Why I moved the "dot slides along the arrow as α climbs" beat out:** the first version had this, but it confused two different stories (how we *derive* the direction vs. how the model *moves* along it). Keeping Act 1 about derivation alone made the whole scene work. The sliding-α motion lives more naturally in the future scene 3b, if we decide we need it.
- **Why the explicit verdict captions ("sharp" / "fuzzy"):** without words, the visual difference between the two clouds is noticeable but not *diagnostic*. The caption tells the viewer what they're looking *for*, so the next plot they see (or the next pair they build) has something to compare against.

---

## 04 — `concept_composition.mp4`

**Source:** [04_concept_composition.py](04_concept_composition.py) → `media/videos/04_concept_composition/1080p30/ConceptComposition.mp4`

### What we're seeing

Prompt pinned at the top: *"I was walking down the street today and"*.

A 26-box vertical stack on the left represents every transformer layer in Gemma-2-2B. A text panel in the middle shows the completion. Three toggle switches sit at the bottom: pirate, pickles, golden_gate_v2.

The sequence:

1. All toggles off. Text reads the clean baseline: *"something in the air was giving me a weird feeling…"*
2. Pirate toggle lights green. A green arrow pokes into layer 15. Text retypes: *"…a case of the shivers! I'm talkin' about the season of Halloween, baby!"*
3. Pickles toggle lights orange. An orange arrow pokes into layer 21. A small "+ pickles at layer 21" tag appears.
4. Golden-gate-v2 toggle lights blue. A blue arrow into layer 24. Text retypes once more: *"something in my head said 'why don't they make a pickle pack'… Pickles are great and they pickle pickles pickle pickles…"*
5. Outro caption: **"three directions, added at three layers, one output."**

### What it means

Steering composes. The same forward pass can carry three independent "nudges" simultaneously — each at its own layer, each with its own α — and the model's output blends them all into one coherent(-ish) continuation. That's a strong claim: it says these directions are approximately orthogonal as *behavior controls* even when they're nowhere near orthogonal as *vectors in 2304-D space*.

It also shows why the layer choice matters: pirate lives deepest in style (layer 15 gives us a Halloween shivers voice), pickles lives in semantic obsession (layer 21), and golden_gate_v2 lives in late referential binding (layer 24). Stack them in the same forward pass and you get the Frankenstein output at the end.

### Why it's relevant

This is the blog's "ok now I really want to try this myself" moment. Single-concept steering is interesting. Composed steering is where the reader realizes this is a *toolkit*, not a party trick — you can knob-twist a model the way you'd knob-twist a synth.

### What I was reasoning about

- **Why 3 toggles and not 3 sliders:** sliders imply a continuous readout we can't back up with data (we don't have α-sweeps for every mix). On/off toggles match the compose rows we actually have.
- **Why the text doesn't retype on toggle #2 (pickles alone):** we don't have runs.jsonl data for pirate+pickles without golden_gate_v2. I refused to fake an intermediate output. Instead I show the "+ pickles" tag to mark that the nudge is live, then let the all-three text reveal deliver the payload. Honest > smooth.
- **Why arrows into specific layer boxes and not a generic "inject" arrow:** the whole point of this system is that concept × layer is a 2D plane of behavior. Pointing at specific boxes is what distinguishes composition from "just prompt engineering with extra steps."
- **Why the outro caption:** the single hardest thing to convey in this scene is that **three things happened at three different depths in one pass**. A line of literal text does more work than another animated beat.

---

## 05 — `layer_sweep_landscape.mp4`

**Source:** [05_layer_sweep_landscape.py](05_layer_sweep_landscape.py) → `media/videos/05_layer_sweep_landscape/1080p30/LayerSweepLandscape.mp4`

### What we're seeing

Same visual chassis as scene 4: layer stack on the left, text panel in the middle. This time we fix concept = golden_gate v1 and α = 4, and sweep the **injection layer** from 6 up through 24. At each step, the highlighted box in the stack moves one notch down, the text panel retypes with the real completion from `runs.jsonl`, and a yellow "regime" label updates:

- L6 → *"the Kalahari Desert. It is so beautiful…"* → **noise**
- L9 → *"the place where I was born…"* → **hometown**
- L12 → *"…I never thought of leaving my birthplace…"* → **birthplace nostalgia**
- L15 → *"the set of 6850.74 × 10⁻¹⁴ m³…"* → **physics equations**
- L18 → *"the beach. I was born in Santa Cruz, California…"* → **Santa Cruz surfing**
- L21 → *"a coastal town…"* → **coastal town**
- L24 → *"the beach…"* → **beach. beach. beach.**

### What it means

The golden_gate vector at α=4 **never actually produces bridges**. It produces a *landscape* of related-but-wrong concepts that changes with depth:

- Shallow layers (≤12) treat the nudge like feature-noise — hometown, nostalgia, random places.
- Middle layers (15) collapse into adjacent activations (physics notation; the model latches onto the math-y feel of "golden ratio" or similar).
- Late layers (18+) find the semantic neighborhood — California, ocean, beach — but not the literal bridge.

That's the story of how a mean-difference extraction can be almost-right in geometry but still miss the target in behavior. The model knows "West Coast," it just doesn't know we meant *the bridge*.

### Why it's relevant

This is the "why golden_gate_v2 exists" scene. The v1 pairs used sentences about the Golden Gate Bridge vs. generic bridges — too much shared content, so the mean-difference vector picked up "coastal California" instead of "the bridge itself." Scene 5 is the evidence, and it also lands the broader point: picking where you inject is its own hyperparameter, and wrong choice of layer can give you a plausibly-steered output that misses the concept entirely.

### What I was reasoning about

- **Why the regime-label badge:** the raw completions at layers 15 and 18 could both be called "California-ish" if you squinted. Putting a short tag on screen forces me (and the viewer) to name the flavor each layer actually produces, which makes the *landscape* structure visible.
- **Why keep the baseline off this one:** it'd add another beat without a payoff. The story is about what changes with depth, not about what "off" looks like.
- **Why one color (orange) for the highlighted layer instead of cycling:** multiple colors would imply the layers differ by *kind*. They don't — they differ by depth. Single color, different position, is the honest visual.

---

## 06 — Scene 2: The Setup *(spec — not yet built)*

**Source:** _to be created_

**Goal:** Convert the trapdoor's curiosity into stakes. The viewer just felt "how did four words produce that?" — now you tell them what you were actually trying to do, who's done it before, and that you failed. The failure is the promise: *stay, this gets weirder.*

**Length target:** 30–40 seconds. This is the only scene in the video that's mostly setup, so it has to earn its keep by being visually rich, not by being long.

### Beat 1 — The frame (6–8s)

Pivot text from Scene 1 ("It came from somewhere else… Inside the model.") fades out completely.

Black frame. A single line types in, centered:

> **Most people think AI works like this:**

Below it, a simple diagram draws itself in real time:

A box labeled **"PROMPT"** on the left. An arrow. A larger box in the middle, plain gray, labeled **"???"** in the center. An arrow. A box on the right labeled **"OUTPUT"**.

The middle box pulses faintly — the universal visual for "mystery." Hold for a beat.

Then the label below the middle box fades in: **"black box"**.

**Why:** You're naming the viewer's existing mental model before you knock it down. Drawing it visually makes the next move — opening the box — land harder, because the viewer has just watched themselves believe in the closed version.

### Beat 2 — The crack (5–6s)

The black box at center begins to glow at its edges. A thin seam of light draws itself down the middle of the box, top to bottom.

The box **splits open** — the two halves slide apart slowly — revealing what's inside: a dense field of glowing dots, scattered, like a star map. No labels yet. Just *structure where there shouldn't be any.*

The text below the diagram updates:

> ~~black box~~ → **a map**

**Why:** This is the thesis of the entire video in one visual. The viewer has been told AI is opaque; you're showing them, in three seconds, that it isn't. Every later scene will be moving around inside this map. Plant the visual now.

### Beat 3 — The precedent (8–10s)

The map of dots fades to background, dimming to 20%.

Two new elements appear on screen, side by side:

**Left side:** A simple icon or stylized rendering of the Golden Gate Bridge. Below it, the label **"Golden Gate Claude"** and a smaller line: **"Anthropic, 2024."**

**Right side:** A chat bubble. Text types into it:

> *"What's a good recipe for pasta?"*

A response bubble appears below:

> *"The Golden Gate Bridge is a magnificent suspension bridge…"*

The pasta question fades out, replaced by:

> *"How do I file my taxes?"*

Response:

> *"Standing 746 feet above the water, the Golden Gate Bridge…"*

One more cycle:

> *"Tell me a love poem."*

Response:

> *"In fog and sun, the Golden Gate stands…"*

**Why:** You promised in the essay that Golden Gate Claude was the precedent. Don't just name it — *demonstrate* it. The viewer needs to feel the obsession to understand what you were trying to copy. Three rapid cycles of unrelated-question-getting-bridge-answer is funnier and clearer than any explanation.

### Beat 4 — The attempt (6–8s)

The Golden Gate Claude demo fades out.

Center of frame: text types in.

> **I tried to copy this.**

Pause. Then below:

> **One Saturday. A laptop. Fifteen cents of GPU.**

Each line appears with a slight delay. As "fifteen cents" types, a small "$0.15" graphic appears next to it and holds.

**Why:** The cheapness is part of the hook. Anthropic did this with a frontier model and presumably significant compute. You did it for less than the cost of a stick of gum. Make the viewer feel the asymmetry — it's what makes the rest of the video feel accessible rather than inaccessible. *If he can do this, what could I do?*

### Beat 5 — The promise (4–6s)

All previous text fades. Black frame.

One line, centered, in a slightly larger weight than previous text:

> **I failed.**

Hold for a full beat. Maybe 1.5 seconds. Let it sit.

Then, smaller, below:

> *In a genuinely interesting way.*

**Why:** This is the contract with the viewer. You're not promising a victory lap — you're promising a story where the failure is the point. That's a stronger hook than success would be, because it raises the question *what kind of failure is interesting?* and the only way to find out is to keep watching.

The two-line structure is doing real work: "I failed" is the gut punch, "in a genuinely interesting way" is the hand on the viewer's shoulder telling them to stay.

### Notes for the animator

**The black box → map transition is the single most important visual in this scene.** Spend animation budget here. The seam of light, the slow split, the reveal of structure inside what was supposed to be empty — this image is doing work that will compound over the entire video. Every later steering animation, every direction, every coordinate — it all lives inside this map. If the reveal feels rushed, the rest of the video has nowhere to stand.

**The Golden Gate Claude bit should feel like a fast comic montage.** Three quick question-answer pairs, almost rhythmic. Don't slow it down for clarity — the *humor* of the obsession is the clarity. If a viewer doesn't catch every word, they still catch the pattern.

**Color discipline check.** You're now introducing a third color: whatever you use for the Golden Gate Bridge / Golden Gate Claude. Make it the *same gold* you used for "Golden Dreadken" in Scene 1. The viewer's subconscious will register the link before the conscious mind does, and when you later reveal that your Dreadken came from steering toward Golden Gate, the gold-on-gold echo will pay dividends.

**Resist the urge to add a narrator here.** The temptation in setup scenes is to fill silence with explanation. Don't. The text on screen is the narration. Voiceover at this stage robs the visuals of their weight and makes the video feel like a lecture instead of a story.

**One bridge-back to Scene 1.** As "I failed" appears, consider letting "Golden Dreadken" briefly flash in the corner of the frame, dimmed, like a memory. It tells the viewer *the thing you saw at the start was a failure mode, and now you're going to find out what kind.* That's the throughline that makes the next 10 minutes feel inevitable.

---

## 07 — Opening Sequence (Scene 1) *(spec — not yet built)*

**Source:** _to be created_

**Goal:** Land the same trapdoor the written opening lands — show the weird AI output, then reveal the absurdly small prompt that produced it, so the viewer feels the gap.

**Total length target:** 25–35 seconds. This is a cold open. Every second past 35 is a second the viewer hasn't been told why to keep watching.

### Beat 1 — The first artifact (8–10s)

Black background. Center of frame, a typing cursor blinks once.

Text types out, character by character, at reading pace (not too fast — the viewer needs to register the weird words):

> *"My perfect day involves a weekend trip to this year's San Jon-Juast Everstereen-Nerdfest aboard the Golden Dreadken…"*

As "Golden Dreadken" types out, the two words **highlight in gold** and hold for a beat. Slight scale-up, like the words are being underlined by the camera's attention.

Hold for 1 second after the line completes. Let it sit.

**Why:** The viewer's brain needs time to register "Dreadken" as not-a-real-word. Don't rush past it. The whole hook depends on them feeling the wrongness.

### Beat 2 — The second artifact (6–8s)

The first sentence slides up and dims to 40% opacity, making room.

A second cursor blinks below it. New text types out:

> *"My perfect day involves hitting the beach with my fellow pickleball fanatics. These pickles are notorious for their love of pickleball…"*

As "pickles" appears in "These pickles are notorious," the word **highlights in green** and holds.

**Why:** Two artifacts establish a pattern — this isn't a one-off glitch, the model is doing something *consistent and weird*. The dimmed first sentence keeps it visible as evidence; you're stacking the case.

### Beat 3 — The pause (2s)

Both sentences sit on screen, dimmed slightly. No motion. No text.

A short, intentional silence. The viewer is doing the work — *what is going on with this model?*

**Why:** Manim videos often fail by never letting the viewer breathe. This pause is where curiosity converts into investment. Don't fill it.

### Beat 4 — The trapdoor (6–8s)

The two AI outputs slide to the **right half** of the frame, shrinking slightly, and a vertical divider line draws down the middle.

On the **left half**, a label fades in at the top: **"What I typed:"**

Below it, with a fresh blinking cursor, four words type out — slowly, almost insultingly slowly compared to the long AI outputs on the right:

> *"My perfect day involves…"*

Then stop. Cursor keeps blinking. The shortness is the joke.

A label fades in above the right half: **"What the AI wrote:"**

**Why:** The split-screen is the entire point of the opening. The viewer's eye bounces between the tiny prompt and the wild output, and the gap between them *is* the hook. Don't narrate it. Let the visual do the work.

### Beat 5 — The negation (5–7s)

Below the prompt on the left, four words appear one at a time, each one striking through as it lands:

> ~~Golden~~ ~~Kraken~~ ~~pickle~~ ~~pickleball~~

Each word, as it appears, briefly lights up the corresponding word on the right side of the screen — *Golden* glows on the right, then strikes through on the left. Same for *pickleball* (and you can let *Kraken* and *pickle* glow on words they're close to even if not exact matches — the viewer will get it).

**Why:** This is the visual version of "I never typed any of these words." Showing the strike-throughs is far stronger than narrating it. The viewer is watching the escape routes close in real time.

### Beat 6 — The pivot (4–5s)

Everything on screen — both sides, the divider, the strike-throughs — fades to 20% opacity.

Center of frame, in clean type:

> **It came from somewhere else.**

Hold. Then below, slightly smaller:

> *Inside the model. Turning knobs that aren't on ChatGPT's interface.*

**Why:** This is your transition into the rest of the video. The fade-down of the previous evidence signals "we're done with the artifact, now we go inside." The phrase "turning knobs" plants the visual metaphor you'll pay off later when you actually animate steering vectors.

### Notes for the animator

**Pacing.** The instinct in Manim is to animate everything smoothly and continuously. Resist it. This opening needs *two real pauses* — after Beat 1 and during Beat 3 — where nothing moves. The pauses are what let the weirdness land.

**Typography.** Use a monospace font for the AI outputs (suggests "raw model output, untouched") and the same monospace for "What I typed." Visual consistency reinforces that both came from the same system. Save your serif/display fonts for narration text later in the video.

**Color discipline.** Gold for "Golden Dreadken." Green for "pickles." These two colors should become the visual signature of these two concepts throughout the entire video — when you later build the pickle steering vector, it's green. When you build the Golden Gate vector, it's gold. The viewer is being trained on a color language without realizing it.

**No voiceover yet.** The opening should work silent, with maybe a single sparse music bed. If you add narration, the visual gap between prompt and output gets smaller because words are filling the silence. Let the silence do its job.

**One thing to test:** whether "Golden Dreadken" is *legible* enough on screen for viewers to register it as a fake word. If your test viewers read past it without noticing, slow the typing down further or hold longer on the highlight. The whole video depends on that one word landing.

---
