# YouTube Script - Linear Algebra to Neural Networks

Working title:

**Vectors Hold Information. Matrices Reshape It.**

Alternate titles:

- **How Vectors Move Through Neural Networks**
- **Neural Networks Are Directions All the Way Down**
- **The Linear Algebra Idea That Made Neural Nets Click**

## Bottom Line Up Front

Yes: the intro should be a quick splice of the strongest moments from the
existing videos, with voiceover setting the promise before the detailed walk.

Suggested intro montage:

1. From `northwest_linear_combination.py`: northwest arrow building from west
   and north.
2. From `matrix_moves_basis_directions.py`: basis arrows moving under a matrix.
3. From `batched_linear_map_tensors.py` or `one_row_weighted_sum.py`: one row of
   `X` pairing with rows of `W`.
4. From `nn_linear_weight_structure.py`: neuron rows filling `Y[0]`.
5. From `ai_vectors_to_representations.py`: raw vectors flowing through learned
   `W` into useful representations.

Intro voiceover:

```text
Bottom line up front: you do not need all of linear algebra to start seeing what
neural networks are doing.

You need a few ideas.

A vector is a recipe: amounts along directions.
A basis is the set of directions that recipe refers to.
A matrix says where those directions move.
Matrix multiplication rebuilds the recipe in a new space.

And in neural networks, those matrices are learned.

So the short version is:

Vectors hold information.
Matrices reshape that information into forms the model can use.
```

## Core Throughline

Keep returning to these three sentences:

```text
The vector supplies the amounts.
The matrix supplies the new directions.
Multiplication recombines them.
```

Then the AI payoff:

```text
Matrices are learned moves that turn raw vector data into more useful
representations.
```

## Segment 1 - Northwest Is a Linear Combination

Visual:

`northwest_linear_combination.py`

What it is doing:

Starts with an intuitive direction example. Northwest is not a new magic
direction. It is a combination of directions we already agreed on.

Narration:

```text
I want to start with the least intimidating version of linear algebra I know:
giving directions.

If I say "northwest," that is not a magic new direction. It means some west and
some north.

That is the first idea: a vector is a move, and coordinates are the recipe for
building that move from directions we agreed on.

So if the agreed directions are east and north, then a coordinate like
(-2, 2) means: two steps opposite east, and two steps north.

The vector is the move. The coordinates are the recipe.
```

Key point:

```text
A vector is a move. Coordinates are a recipe.
```

## Segment 2 - A Plane Can Have Many Bases

Visual:

`plane_many_bases.py`

What it is doing:

Shows that the same subspace can have different internal coordinate systems.
The plane is fixed; the basis inside it is a choice.

Narration:

```text
Now here is where that recipe idea gets more interesting.

This plane is a fixed object in 3D space. It does not change.

But we can choose different pairs of directions inside the plane and use them as
the coordinate system for that plane.

So the basis is not the space itself. The basis is the set of directions we use
to describe positions or moves inside the space.

Same plane. Different basis. Different coordinates.
```

Key point:

```text
A basis is a coordinate system for a space, not the space itself.
```

## Segment 3 - Same Vector, Different Basis

Visual:

`basis_transformation_3d.py`

What it is doing:

Shows a fixed vector in 3D while the coordinate grid changes around it.

Narration:

```text
The standard basis feels natural because we use it all the time: x, y, z.

But it is still just one choice.

Here the point stays fixed in space, but the grid changes. Once the basis
changes, the coordinates change too.

That is because coordinates are coefficients. They tell us how much of each
basis direction we need.

The point did not move. The address changed because the coordinate system
changed.
```

Key point:

```text
Coordinates depend on the basis. The vector does not.
```

## Segment 4 - A Matrix Moves Basis Directions

Visual:

`matrix_moves_basis_directions.py`

What it is doing:

Introduces the main matrix idea geometrically: a matrix is determined by where
it sends the basis directions.

Narration:

```text
Now we can say what a matrix does.

A matrix tells us where the basis directions land.

If it tells us where e1 goes, and where e2 goes, then it has told us what
happens to every vector made from e1 and e2.

Why? Because the vector is a recipe.

If the original vector is 3 of the first direction plus 2 of the second
direction, then after the matrix we rebuild that same recipe using the moved
directions.

Three of where e1 landed, plus two of where e2 landed.
```

Key point:

```text
A matrix moves basis directions.
```

## Segment 5 - A Matrix Is the Stored Map

Visual:

`matrix_as_stored_map.py`

What it is doing:

Connects the geometry to the table of numbers used in code.

Narration:

```text
This is the bridge from the picture to the code.

The matrix is not just a random table of numbers. It is the stored map.

In this row-vector view, each row of W stores where one input direction lands in
the output space.

Then the input vector supplies the weights.

So multiplication means: take this much of row one, this much of row two, this
much of row three, and add them.

The vector supplies the amounts.
The matrix supplies the new directions.
Multiplication recombines them.
```

Key point:

```text
A matrix stores a linear map.
```

## Segment 6 - Batched Matrix Multiply as PyTorch Tensors

Visual:

`batched_linear_map_tensors.py`

What it is doing:

Shows that `X @ W + b` applies the same map to every row of `X`.

Narration:

```text
Now let us translate that into the PyTorch shape we actually see.

X is a stack of input vectors. Here it has five rows, and each row is one 3D
input.

W is the shared map from 3D to 2D.

For each row of X, the three numbers are weights. They pair with the three rows
of W. Then PyTorch adds the weighted rows to produce one output row.

And it does that same operation for every row in the batch.

Same learned map. Many input vectors.
```

Key point:

```text
Batching repeats the same map across many input vectors.
```

## Segment 7 - One Row Becomes One Weighted Sum

Visual:

`one_row_weighted_sum.py`

What it is doing:

Zooms into one row of the batched operation.

Narration:

```text
If the batch view still feels too abstract, zoom into one row.

Take the first row of X and turn it sideways. Now it is a column of weights.

The first weight scales the first row of W.
The second weight scales the second row of W.
The third weight scales the third row of W.

Then we add those weighted rows column by column.

That gives one output vector. Add the bias, and that becomes the first row of Y.
```

Key point:

```text
One row of X produces one row of Y.
```

## Segment 8 - How nn.Linear Stores the Same Map

Visual:

`nn_linear_weight_structure.py`

What it is doing:

Shows how PyTorch stores the same map in `nn.Linear`, then reframes output
features as neuron outputs.

Narration:

```text
PyTorch's nn.Linear stores the weights in a slightly different shape.

For nn.Linear(3, 2), the weight is stored as two rows of three numbers.

That is one row per output feature. Or, in the neural network picture, one row
per neuron.

During the forward pass, PyTorch uses a transposed view of that weight so the
shape works out:

X times linear.weight.T plus bias.

Now the first neuron produces the first value in Y[0].
The second neuron produces the second value in Y[0].

Together, those scalar neuron outputs form the output vector.
```

Key point:

```text
Each neuron output is one component of the output vector.
```

## Segment 9 - Vectors Become Useful Representations

Visual:

`ai_vectors_to_representations.py`

What it is doing:

Gives the payoff: this is why vectors and matrices matter for AI.

Narration:

```text
This is why the whole chain matters for AI.

The data starts as vectors.

A token embedding is a vector.
An image patch can become a vector.
A row of features is a vector.

A neural network learns matrices that move those vectors.

Layer by layer, those matrices learn which directions to amplify, which
directions to ignore, and which directions to mix together.

For attention, the model moves token vectors into query, key, and value spaces.
For images, it can move patch vectors toward edge or texture features.
For prediction, it can move raw features into directions that make the next
decision easier.

The matrix does not understand in a human way. It learns transformations that
make the training objective easier.

So the punchline is:

Vectors hold information.
Matrices reshape that information into forms the model can use.
```

Key point:

```text
Matrices are learned moves that turn raw vector data into useful
representations.
```

## Closing

Suggested final voiceover:

```text
So the beginner version is:

A vector is a move.
Coordinates are the recipe for that move.
A basis is the set of directions the recipe refers to.
A matrix moves those directions.
Matrix multiplication rebuilds the recipe in the new directions.

And a neural network layer learns those moves from data.

That is why linear algebra is not just notation around neural networks.
It is the geometry of how information moves through them.
```

## Editing Notes

- Use the intro as a promise, not a full explanation. The viewer should know
  what payoff they are waiting for before Segment 1 starts.
- Keep the repeated phrase audible:
  `the vector supplies the amounts; the matrix supplies the new directions`.
- When showing PyTorch, explicitly say this is the row-vector convention. Avoid
  mixing it with the standard math column convention in the same sentence.
- Keep formulas as plain text. Do not use LaTeX.
- If the final video is too long, the first cut to consider is Segment 2. The
  strongest core path is 1 -> 3 -> 4 -> 5 -> 6 -> 8 -> 9.
