# Publish: Ep 7, why layers need activation functions

## Title

Activation Functions: Why You Need Them | Linear Algebra for AI Engineers

From the SERIES.md checklist. Search phrase `activation functions`
(autocomplete offers "activation functions explained" and "why do we need
activation function in neural network"). The concept part is 39 characters,
over the series' ~35, so the feed may cut the suffix; the search phrase leads.

## Description

Activation functions stop a deep network from collapsing: without them, x @ W1 @ W2 is just x @ W.

A linear map keeps the origin fixed and grid lines straight. It can stretch, rotate and squish the plane, but it can't bend it. Two layers, x @ W1 then @ W2, equal x @ (W1 @ W2), and W1 @ W2 is one matrix, so a 100-layer linear network is one matrix. Put nn.ReLU() between the nn.Linear layers and the grid folds: the path bends, and stacking adds something.

Episode 7 of Linear Algebra for AI Engineers. The write-up it comes from, How Vectors Move Through Neural Networks: https://bitsofchris.com/p/how-vectors-move-through-neural-networks

Level up human.

#pytorch #linearalgebra #machinelearning #deeplearning #Shorts
