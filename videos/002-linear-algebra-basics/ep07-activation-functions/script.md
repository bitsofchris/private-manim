# Why Neural Networks Need Activation Functions

`vo_raw.m4a`: 58.8 s, cut from `002-linear-algebra-shorts-ALL.m4a` at 399.75–458.57 s (episode announcement removed). Planned script: `../SCRIPTS.md`.

## As recorded

Without activation functions, a 100-layer neural network is just one matrix. Here's why. Matrices are functions, and multiplying matrices combines those functions. So if you stack two layers, X at W1, then at W2, the order matters, but it's associative. So that's the same as X at W1 times W2, and W1 times W2 is just one matrix.

So two linear layers or 200 collapse into a single linear transformation. The depth here doesn't buy you anything. Now, a linear map keeps the origin fixed and the grid line straight. It can stretch, rotate, and squish, but it can't bend. Put a ReLU or a GELU between the layers and the collapse stops. Now, each layer can bend the path, and stacking actually adds something.

That's why every layer in a model is a matrix multiply followed by some non-linearity. Without activations, a deep network is just one matrix
