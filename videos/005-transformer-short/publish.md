# Publish: Transformer short

## Title (pick one; first is recommended)

1. Transformers Made Simple (Beginner Friendly)
2. How a Transformer Works: Attention, FFN, Residuals Made Simple
3. What a Transformer Actually Does to Your Tokens

## Description

What a transformer does in 60 seconds: tokens become vectors, attention mixes them, the feed-forward net refines each one, residuals add it all up.

Three tokens become an L × d matrix. Attention lets each token collect a weighted sum from the others. A residual connection adds that update instead of replacing the token. A feed-forward network works on each token alone. Every block repeats this on the same matrix. The final representation is only turned into a prediction by a task-specific output layer.

Full write-up:
[POST LINK]

Level up human.

#transformers #attention #machinelearning #deeplearning #Shorts

## Pinned comment

The one line to remember: a transformer never replaces a token's vector, it keeps adding to it. Write-up: [POST LINK]

Which part was fuzziest before this: attention, the feed-forward net, or why the output isn't the prediction?
