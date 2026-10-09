# Cosine Similarity vs Dot Product Made Simple

`vo_raw.m4a`: 58.1 s, cut from `002-linear-algebra-shorts-ALL.m4a` at 515.24–573.34 s (episode announcement removed). Planned script: `../SCRIPTS.md`.

## As recorded

Cosine similarity is just a dot product with both lengths divided out. Projection divides out only one. here's when you want each. Now, all three start from the same thing: the dot product, alignment with the length still in it.

Cosine similarity divides by both lengths. Both magnitudes go away, and you're left with pure direction, a number between minus one and one, and that's what you use to compare embeddings. Now, projection divides by only the target's length. Picture casting a shadow from one vector onto another, and projection asks how much of U points along this direction.

The shadow keeps the original's length in the answer, and it splits the vector in two, the part along the direction and the part left over. Even coordinates are projections, one onto each basis direction The dot product is alignment with the length. Cosine is alignment without them. Projection is how much of you lies along that line
