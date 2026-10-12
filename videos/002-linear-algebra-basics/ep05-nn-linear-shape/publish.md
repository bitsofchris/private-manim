# Publish: Ep 5, how a PyTorch linear layer works

## Title

How a PyTorch Linear Layer Works | Linear Algebra for AI Engineers

Chosen 2026-10-12 (Chris: "title it with what it actually answers"). Search
phrase `pytorch linear layer`: YouTube autocomplete offers it first for
"pytorch linear", next to "pytorch nn.linear" (checked 2026-10-12). No
phrasing of the transpose question ("nn.linear weight transpose", "why is
pytorch …") is offered, so the title names the topic and line 1 carries the
point. Replaces the SERIES.md title "PyTorch nn.Linear Explained" (for the
update pass).

## Description

PyTorch's linear layer, nn.Linear, stores its weight as (out, in) and uses weight.T: the W in x @ W.

A tiny model, nn.Sequential(nn.Linear(3, 2), nn.ReLU()), and its first layer. model[0].weight.shape prints torch.Size([2, 3]): one row per output neuron. A neuron multiplies the three inputs by its row, sums, adds its bias and outputs one number (4.1 and −1.2 here). In the forward pass PyTorch computes x @ weight.T + bias, and W = weight.T is the (3, 2) matrix from the last episode, whose rows are where the input directions land. In math vectors are columns and W v uses the columns; in PyTorch vectors are rows and x @ W uses the rows. Same map, transposed.

Episode 5 of Linear Algebra for AI Engineers. The write-up it comes from, How Vectors Move Through Neural Networks: https://bitsofchris.com/p/how-vectors-move-through-neural-networks

Level up human.

#pytorch #linearalgebra #machinelearning #deeplearning #Shorts
