# Publish: Ep 10, attention score calculation

## Title

Attention Score Calculation | Linear Algebra for AI Engineers

From SERIES.md. Search phrase `attention score calculation` (offered by
YouTube autocomplete); "query key" was rejected because it completes to
"query key value", and this episode never covers Value.

## Description

Attention score calculation: a dot product between one token's query and another token's key.

Three tokens, my, name, is, start as vectors (the rows of X). A learned matrix W_Q moves each one into a query, Q = X @ W_Q, and W_K moves each one into a key, K = X @ W_K. One score: the query of "name" times the key of "is", 1·2 + 2·2 = 6, high because they're aligned. scores = Q @ K.T does every pair at once: a (3, 3) grid. Divide by the square root of the head size (d**0.5), and softmax turns each row into weights that add up to 1.

Episode 10 of Linear Algebra for AI Engineers. The write-up it comes from, How Vectors Move Through Neural Networks: https://bitsofchris.com/p/how-vectors-move-through-neural-networks

Level up human.

#transformers #attention #linearalgebra #pytorch #Shorts
