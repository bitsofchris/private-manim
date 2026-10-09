# What a Matrix Really Does (Linear Algebra for AI)

`vo_raw.m4a`: 50.6 s, cut from `002-linear-algebra-shorts-ALL.m4a` at 132.16–182.73 s (episode announcement removed). Planned script: `../SCRIPTS.md`.

## As recorded

A matrix just records where each direction lands. Every weight matrix in a neural network is doing exactly this. Here's e1 and e2. This matrix sends e1 here and e2 here. Now take a vector, three of e1 plus two of e2. The vector is a recipe. After the matrix, keep the same recipe and use the move directions.

Three of where e1 landed plus two of where e2 landed. The vector supplies the amounts, the matrix supplies the new directions. That's why the table of numbers isn't random. Each row is one landing spot. In PyTorch, row i of W is where the input direction i lands. In a network, that map moves vectors from one space to another, amplifying some directions and collapsing others.

A matrix is just this stored map where every input direction lands
