# Publish: Ep 5, PyTorch nn.Linear's weight shape

## Title

PyTorch nn.Linear Explained | Linear Algebra for AI Engineers

## Description

PyTorch nn.Linear stores one row per output neuron and flips it on the forward pass.

nn.Linear(3, 2) gives a weight of shape (2, 3): each row is one neuron, which multiplies the three inputs by its own weights, sums them, adds a bias and outputs one number (4.1 and −1.2 here). In the forward pass PyTorch computes x @ weight.T + bias, and the flipped weight, (3, 2), is the W from the last episode: each row is where an input direction lands. In math vectors are columns and W v uses the columns; in PyTorch vectors are rows and x @ W uses the rows. Same map, transposed.

Episode 5 of Linear Algebra for AI Engineers. The write-up it comes from, How Vectors Move Through Neural Networks: https://bitsofchris.com/p/how-vectors-move-through-neural-networks

Level up human.

#pytorch #linearalgebra #machinelearning #deeplearning #Shorts
