# What is Jev and why is everyone excited? — storyboard (v2, pre-VO)

THE QUESTION: "What is Jev, and why is everyone so excited about it?"
WHO IS ASKING: an engineer or AI researcher who has seen "Jev" in their
feed for two weeks and wants the two-sentence version, not a tutorial.
THE ANSWER IN ONE SENTENCE: Jev is a decision model, a classifier that
takes an input and a fixed set of choices and returns a probability for
each choice in one pass, and it matters because an LLM makes the same
decision by generating tokens one at a time, which is slow and expensive
for the thousands of small decisions an agent has to make.

**One idea:** a decision is a classification, not a generation. Jev is the
product that made people notice.

Source: Chris's arc (2026-10-02 session), the two @llmsresearch Substack
notes, TypeSafe's launch post, and the independent numbers listed under
Sources. VO is drafted from Chris's own phrasing; rewrite before recording.
~135 words.

## Beats

| # | Beat | ~s | Visual (9:16) | VO (draft, Chris's words) |
|---|------|---:|---|---|
| 1 | Hook | 5 | Frame 0: the word "Jev" big, and around it a scatter of feed-style chips ("System One", "decision model", "Jev vs LLMs", "100x faster?") drifting in. On "why" they freeze. No hero yet. | What is Jev, and why is everyone so excited about it? |
| 2 | What it is | 10 | A state card (short JSON) and a question card "Is this urgent?" with chips `yes` `no` `later`. One arrow through a box labelled "decision model". Out the right: three probability bars that fill to 0.91 / 0.06 / 0.03 on "probabilities". Hero: the bars. No prose appears anywhere. | Jev is a decision model. You give it some input and a fixed set of choices, and it gives you back a probability for each choice. Structured output, no text. |
| 3 | Why excited: one pass vs many | 14 | Split stage, same question on both halves. Top, "LLM": a token stream types `{"urgent": tr…` one token at a time; each token lights the whole network once (a pass counter climbs: 1, 2, 3 … 40+) and a timer runs. Bottom, "decision model": the input and the three choices go through the network once; pass counter reads 1; the three bars fill together. Small print under the split: "171 ms vs 1.7 s, same accuracy (OpenRouter, HaluEval)". Hero: the single pass. | People are excited because this is different from what an LLM does. An LLM decides by generating, token by token. Every token is another pass through the whole model. Jev takes the input and all the choices in one pass, so it's fast and cheap. |
| 4 | Agents make lots of decisions | 10 | An agent loop drawn as a circle. Decision diamonds appear around it on each phrase: `which tool?` `is this safe?` `am I done?` `route to?`. Each diamond is a tiny copy of beat 2's bars. On "a lot" they multiply around the loop (a tag: "~22 tool calls per task, MCP-Bench"). Hero: the diamonds. | And agents make a lot of these decisions. Which tool, is this safe, am I done. Each one is a choice from a fixed set, and that's a classifier's job, not a writer's. |
| 5 | The real point | 10 | The decision-model box from beat 2 opens: inside, a frozen stack of transformer blocks (reuse `transformer.build_block`, dim) with a small magenta "decision head" on top. Badges tick in beside it: Jev, plus open ones (Laya, CLM-8B). Hero: the head. | Jev is one company's version. The bigger idea is decision models in general: a classifier on top of the rich representations we've gotten really good at building. That's why it works, and that's why there are open ones too. |
| 6 | Close | 6 | Back to beat 2's bars, held. One caveat chip lands under them: "a probability is not permission". Last frame still. | So: a decision is a classification. Jev just made everyone notice. |

Total ≈ 55 s before tightening. Hero per beat: 1 none, 2 bars, 3 the single
pass, 4 the diamonds, 5 the decision head, 6 none.

## Not in this Short (on purpose)

The classifier → zero-shot classifier → decision model ladder, the three
answer types (Choice / Score / Null), the reliability plot, thresholds,
the System 1 / System 2 training recipe, RLCD. All true, none needed to
answer the question. "Calibrated" is deliberately not said on screen or
in the VO: independent tests show Jev's probabilities don't transfer to
new distributions (see Sources), so the Short says "a probability".

## Numbers on screen, and who measured them

| Claim | Figure | Who | Use |
|---|---|---|---|
| Latency, decision model vs LLM judge | 171 ms vs 1,662 ms median (~10x) | OpenRouter, HaluEval, 88 items, independent | beat 3 small print |
| Cost, same test | $0.021 vs $0.114 per 1k judgments (~5x) | OpenRouter, independent | description |
| Accuracy, same test | 95.5% vs 94.3% | OpenRouter, independent | beat 3 "same accuracy" |
| Fine-tuned encoder vs prompted LLM, cost | 94x to 222x cheaper per 1M requests, F1 within 3 pts | arXiv 2602.06370, independent | description |
| TypeSafe's own numbers | "40x-200x faster", 70-500 ms vs 3-329 s | vendor | description only, labelled as their claim |
| Tool calls per agent task | 21.8 (gpt-4o) to 78.9 (gpt-5) | MCP-Bench, arXiv 2508.20453 | beat 4 tag ("~22") |

Honest-copy notes for the description: TypeSafe's internals are
unpublished; the "classifier on top of representations" framing in beat 5
is ours and is true of the open models (Laya is ModernBERT plus a decision
head; CLM-8B is contrastive). Independent tests found Jev overconfident
out of distribution (a fair coin scored 0.92; a hidden fair die at 83%
confidence, 19% accuracy), hence "a probability is not permission" and
"recalibrate on your own data" in the description.

## What the two Substack notes gave us

- @llmsresearch, Sep 17 ("How Jev works" infographic): the clean visual
  contrast, "150-500 sequential forward passes" vs "1 forward pass, all
  fields scored at once", and "softmax over just the candidate tokens, sums
  to 1". Illustrative numbers, not measurements; beat 3's pass counter
  is this picture, animated.
- @llmsresearch, Sep 22 (production agent architecture): "one state, many
  decisions, one call"; the three-layer split (decision model for bounded
  choices, LLM for open-ended reasoning, code for execution); and the
  reply "a probability is not permission", which is the close.

## Reusable elements to build

- `prob_bars(choices, probs)`: label + bar per choice; beats 2, 4, 6, must
  keep identity (Transform, never fade-swap).
- `token_stream`: the LLM typing one token at a time with a pass counter.
- `decision_diamond`: a tiny prob_bars inside a diamond, beat 4.
- Beat 5 reuses `videos/_shared/transformer.build_block` as the frozen
  stack; the decision head is one magenta `op_box`.

## Sources

- TypeSafe launch post: https://typesafe.ai/blog/introducing-system-one-models-and-jev
- OpenRouter, Jev vs LLM-as-a-judge: https://openrouter.ai/blog/tutorials/jev-vs-llm-as-a-judge/
- Fine-tuned encoders vs prompted LLMs: https://arxiv.org/abs/2602.06370
- MCP-Bench (tool calls per task): https://arxiv.org/abs/2508.20453
- "How Jev works" note: https://substack.com/@llmsresearch/note/c-339129753
- Production agent architecture note: https://substack.com/@llmsresearch/note/c-343107982
- Calibration critiques: https://www.alexmolas.com/2026/09/23/jev-cant-be-calibrated.html , https://kantahayashiai.github.io/posts/jev-does-not-play-dice/
- Open models: https://trilogyai.substack.com/p/jev-open-decision-models , https://github.com/kotoba-lang/typed-decisions

## Next

1. Chris: rewrite the VO column in your own phrasing, then record
   `vo_raw.m4a` into this folder (one pass, ~1 s between beats).
2. Claude: runbook from step 3 (clean → transcribe → cut list → scenes →
   assemble → contact sheets).
