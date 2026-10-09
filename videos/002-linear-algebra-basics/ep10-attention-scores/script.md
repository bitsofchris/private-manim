# Query, Key, Value Explained: Attention Scores

`vo_raw.m4a`: 55.2 s, cut from `002-linear-algebra-shorts-ALL.m4a` at 579.23–634.44 s (episode announcement removed). Planned script: `../SCRIPTS.md`.

## As recorded

An attention score is just a dot product between one token's query and another token's key. Every token starts as a vector. A learned matrix, WQ, moves each one into a query, which is the question this token asks.

Another matrix, WK, moves each one into a key. What question can this token help answer? To score one pair, you take one token's query and another token's key and do the dot product. High value here means they're aligned. This token has what the other one is looking for. Q at K transpose does every pair at once.

Three tokens, a three-by-three grid of scores.Then divide by the square root of the head size, and softmax turns each row into weights that add up to one. Transformers process every position in parallel. Attention is how tokens decide who to pull information from, and attention scores measure which tokens are aligned under these learned projections
