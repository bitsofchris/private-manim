# Publish: What is Jev and why is everyone excited

## Title (pick one; first is recommended)

1. What Is Jev? Decision Models Made Simple
2. Jev and Decision Models Made Simple (Beginner Friendly)
3. Why Everyone Is Excited About Jev: Made Simple

## Description

What Jev is, and why engineers are excited: a decision model scores all the choices in one pass instead of generating token by token.

You give it some input and a fixed set of choices; it returns a probability for each choice. An LLM makes the same decision by generating, one pass per token. Agents make dozens of these decisions per task (MCP-Bench measured ~22 tool calls per task for GPT-4o), and each one is a classifier's job. The bigger idea: a decision model is a classifier on top of the rich representations language models already learned. Anyone can train one; the hard part is calibration, so you need your own labels. A quick way to get them: let a frontier LLM label the hard cases once, train the small model on those, then check it against a few hundred human-verified labels.

Numbers: the on-screen 171 ms vs 1.7 s at the same accuracy is OpenRouter's independent HaluEval test of Jev vs an LLM judge (also ~5x cheaper). TypeSafe's own claim is 40x to 200x faster. Independent tests also found Jev overconfident off-distribution (a fair coin scored 0.92), which is why the Short ends on "your own labels". A probability is not permission.

Sources: TypeSafe launch post · OpenRouter, Jev vs LLM-as-a-judge · arXiv 2602.06370 (fine-tuned encoders vs prompted LLMs) · MCP-Bench, arXiv 2508.20453 · @llmsresearch notes on how Jev works and agent architecture · alexmolas.com, "Jev can't be calibrated"
[POST LINK]

Level up human.

#jev #decisionmodels #llm #aiagents #Shorts

## Pinned comment

Full sources and the labeling recipe in the post: [POST LINK]

What decision in your agent would you hand to a classifier first: tool choice, safety check, or "am I done"?
