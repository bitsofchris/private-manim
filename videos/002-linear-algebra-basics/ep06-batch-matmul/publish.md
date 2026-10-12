# Publish: Ep 6, one matmul, whole batch

## Title

PyTorch Matrix Multiplication | Linear Algebra for AI Engineers

Search phrase: pytorch matrix multiplication (in the title and description
line 1). "Batch matrix multiplication" stays out of both: autocomplete pairs
it with "dsa" / "using dp", the algorithms-course meaning.

## Description

In PyTorch matrix multiplication, X @ W applies the same map W to every row of the batch X.

One line, Y = X @ W: X is a batch of five input rows with three features each, shape (5, 3), and W is the map from three dimensions to two, shape (3, 2). Row one, [1, 2, −1], weights the rows of W and sums to [4, −1]; then row two, then all five. (5, 3) @ (3, 2) gives (5, 2): the inner dimensions match and disappear. The bias broadcasts across every row. Real data is (batch, seq, features), and the last dimension is always the vector.

Episode 6 of Linear Algebra for AI Engineers. The write-up it comes from, How Vectors Move Through Neural Networks: https://bitsofchris.com/p/how-vectors-move-through-neural-networks

Level up human.

#pytorch #linearalgebra #machinelearning #deeplearning #Shorts
