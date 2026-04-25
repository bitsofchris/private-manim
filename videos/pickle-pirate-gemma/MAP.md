# pickle-pirate-gemma — cheat sheet

Two tracks of animations live in this folder:

- **`0N_*.py`** — the five "harness" scenes that pair 1-to-1 with the blog's results. Walk through the actual experimental data (real `runs.jsonl` outputs, real PCA clouds). Documented beat-by-beat in [talking_beats.md](talking_beats.md). Spec in [plan.md](plan.md).
- **`blogNN_*.py`** — standalone conceptual visuals for the blog's *explainer* sections. No harness data; these are pedagogical priors that set up the geometry before the reader sees the real experiments.

Rendered MP4s all land at `media/videos/<scene>/1080p30/<ClassName>.mp4`.

---

## Track A — harness scenes (real data)

| # | File | Render | What it shows | Why it's there |
|---|---|---|---|---|
| 01 | [01_steering_vector_addition.py](01_steering_vector_addition.py) | `SteeringVectorAddition.mp4` | 2D cartoon of `h + α·0.1·‖h‖·û`. α knob 0→10. Captions swap real pickle completions at α=0/4/10. | Opener: "steering is just addition." Gets the reader from "magic" to "oh, it's a line of code." |
| 02 | [02_alpha_sweep_morph.py](02_alpha_sweep_morph.py) | `AlphaSweepMorph.mp4` | Fixed prompt, layer 21. α∈{0,2,4,6,8,10}, each frame retypes the real completion. Dial + ‖inject‖ bar. Outro: giant "pickles". | Money clip. The model losing the plot in real time — the shareable moment. |
| 03 | [03_pca_with_steering_arrow.py](03_pca_with_steering_arrow.py) | `PCAWithSteeringArrow.mp4` | Three acts: (1) pickles PCA clouds + diff arrow, (2) golden_gate v1 clouds overlapping, (3) side-by-side with real α=4 L21 generations. | Bridges geometry → behavior. Clean clouds ⇒ sharp steering; fuzzy clouds ⇒ fuzzy steering. Makes mean-diff falsifiable. |
| 04 | [04_concept_composition.py](04_concept_composition.py) | `ConceptComposition.mp4` | 26-layer stack + three toggles (pirate L15, pickles L21, gg_v2 L24). Baseline → +pirate → +pickles → +gg_v2 retypes. | Finale: compositions work. Three nudges, three layers, one pass. "Toolkit, not party trick." |
| 05 | [05_layer_sweep_landscape.py](05_layer_sweep_landscape.py) | `LayerSweepLandscape.mp4` | Fixed concept=golden_gate v1, α=4. Sweep inject layer 6→24, retype real completion + regime label (noise / nostalgia / physics / Santa Cruz / beach). | The "why gg_v2 exists" scene. Shows layer choice is its own hyperparameter; mean-diff can be almost-right but miss the target. |

Detailed narration + framing reasoning for scenes 01–05 is in [talking_beats.md](talking_beats.md).

Supporting files:
- [_pca_data.py](_pca_data.py) — precomputed 2D PCA points (clouds, centroids, unit arrow) so Manim isn't doing linear algebra at render time.
- [plan.md](plan.md) — the original spec the scenes were built from. Also lists two optional scenes (`cos_pn_diagnostic`, `obsession_emergence`) that were **not** built.

---

## Track B — blog explainer scenes (conceptual, no harness data)

| # | File | Render | What it shows | Where it lands in the post |
|---|---|---|---|---|
| 01 | [blog01_concept_space.py](blog01_concept_space.py) | `ConceptSpace.mp4` | Words scatter into labeled clusters on a 2D plane (food, vehicles, seafaring, emotions); camera zooms to "pickle" neighborhood. Caption: "real AI uses thousands of dimensions — this is two." | Section 1: what "concept space" even means. Sets up that meaning has geometry before anything else happens. |
| 01b | [blog01b_token_vs_concept.py](blog01b_token_vs_concept.py) | `TokenVsConcept.mp4` | Pickle neighborhood. Highlight one dot ("'pickle' — the token, one point"), then trace a soft blob over the cluster ("'pickle-ness' — the concept, the shape places trace out"). Single arrow runs through the blob. | The post's tokens-are-places / concepts-are-shapes sidebar. Lands the linear-representation premise before steering shows up. |
| 02 | [blog02_king_queen.py](blog02_king_queen.py) | `KingQueen.mp4` | Classic `king − man + woman ≈ queen` parallelogram. Extracts `woman − man` as an arrow, translates it onto `king`, lands near `queen`. | Section 2: directions = meaning. Prior-art reference (word2vec analogies) that primes the reader for mean-diff steering. |
| 03 | [blog03_mean_diff.py](blog03_mean_diff.py) | `MeanDiff.mp4` | Slim 8s mean-difference: two clouds (30 pickle, 30 other-food), centroids pop, yellow arrow draws from orange to green. Caption: "the pickle direction." | The post's "build the steering vector by subtraction" beat. Mainstream-paced twin of harness scene 03 Act 1. |
| 04 | [blog04_santa_cruz.py](blog04_santa_cruz.py) | `SantaCruz.mp4` | Sibling of blog06's chassis. Dashed "intended" arrow points at "Golden Gate Bridge" dot. Dot starts at baseline, but as α climbs it *curves off the arrow* into a shaded "Coastal California" region, then drifts further into broken/physics. Text panel morphs through the real failure ladder. | The post's Santa Cruz failure beat. Counterpart to blog06: same chassis, opposite outcome — the visual point is the dot leaving the arrow. |
| 05 | [blog05_superposition.py](blog05_superposition.py) | `Superposition.mp4` | Split: LEFT "pickle" as a clean point, arrow lands dead center. RIGHT "Golden Gate Bridge" as diffuse cloud overlapping California/SF/Bridges; arrow lands in "California" overlap. | Section on superposition / why some concepts are clean and others are weather. Conceptual twin of harness scene 03. |
| 06 | [blog06_pickle_ladder.py](blog06_pickle_ladder.py) | `PickleLadder.mp4` | Split screen: left = pickle direction arrow, yellow dot slides along it as α climbs; right = typewriter panel morphs through the real layer-21 completions. | The "success" story beat — pickles are the clean case. Conceptual twin of harness scene 02, tighter. |
| 07 | [blog07_composition.py](blog07_composition.py) | `Composition.mp4` | Three arrows tip-to-tail on a 2D plane (pirate brown, pickle green, golden gate rust). Composite marker slides. At the tip, "Golden Dreadken" materializes from "Golden" + "Kraken". | The composition section's hero visual. Conceptual twin of harness scene 04. |

---

## How the two tracks relate

| Blog beat | Explainer (Track B) | Evidence (Track A) |
|---|---|---|
| "Meaning has geometry." | blog01, blog01b, blog02 | — |
| "Steering is a vector add." | — | 01 |
| "Build the arrow by subtraction." | blog03 | 03 (Act 1) |
| "Watch it break down." | blog06 | 02 |
| "Aim at GG, land in Santa Cruz." | blog04 | 03 (Acts 2–3), 05 |
| "Common = points, rare = weather." | blog05 | — |
| "Layer choice matters." | — | 05 |
| "You can compose." | blog07 | 04 |

Track B is the *prior* the reader needs before Track A's data lands. Track A is the receipt.
