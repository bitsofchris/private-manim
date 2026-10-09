# PyTorch nn.Linear Explained (Beginner Friendly)

`vo_raw.m4a`: 58.5 s, cut from `002-linear-algebra-shorts-ALL.m4a` at 266.08–324.59 s (episode announcement removed). Planned script: `../SCRIPTS.md`.

## As recorded

PyTorch stores one output neuron per row. So when you give nn.linear three in and two out, the weight will come back two by three. A neuron takes all three inputs, multiplies each by its own weight, sums them, adds a bias, and outputs one number. Two outputs, two neu- two outputs, two neurons, two rows of three.

In the forward pass, PyTorch flips it. x@weight.t plus a bias. The flipped weight is three by two, exactly the w from the last video, where each row is where an input direction lands. So don't ask which is in and which is out, ask where are the landing vectors stored, in the rows or the columns? In math, vectors are columns, and w times v uses the columns.

In PyTorch, vectors are rows, and x@w uses the rows. It's the same idea, just transposed. nn.linear stores neurons as rows and transposes on the way through
