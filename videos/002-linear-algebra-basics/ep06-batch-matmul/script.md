# Batch Matrix Multiplication Made Simple (PyTorch)

`vo_raw.m4a`: 55.1 s, cut from `002-linear-algebra-shorts-ALL.m4a` at 334.77–389.83 s (episode announcement removed). Planned script: `../SCRIPTS.md`.

## As recorded

One line of PyTorch pushes a whole batch through a layer because X is data and W is the map. X is five rows. Each row is one input vector with three features. W is the map from three dimensions to two, X and W are both matrices, but they play different roles.

X is data, which is a stack of vectors here. W is a transformation. So X at W does the same thing to every row. Row one of X weights the rows of W and sums, then row two, then all five in parallel This five by three add three by two gives five by two. The inner dimensions have to match, and then they disappear.

then the bias broadcasts across every row. Real data just makes this bigger. There's a batch, there's a sequence, there's features. The last dimension is always the vector. It's the same learned map in that matrix applied to many vectors
