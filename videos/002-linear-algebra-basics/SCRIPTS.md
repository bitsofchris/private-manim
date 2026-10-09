# Linear Algebra for Engineers: recording scripts

**Name:** linear-algebra-scripts
**Description:** One VO script per episode in `SERIES.md`, with the
YouTube title. Built from Chris's Unit 0–5 notes, `UNIT_1_3_RECAP.md`,
and the post *How Vectors Move Through Neural Networks*.
**When to use:** recording. Each script becomes the VO column of that
episode's `storyboard.md` when its folder is opened.
**How it works:** read each script once, straight through (runbook
step 2). Blank line = a beat; pause about a second there. Flub? Pause and
re-read the sentence. Lines marked *(if time)* are the first cut if the
take runs long. Every script opens on the answer, not the question: the
first line is the payoff, said plainly, so a viewer who leaves at two
seconds still got it. If a line doesn't sound like you, say it your way: the
transcript, not this file, becomes the captions.

Save each take in this folder as `epNN_vo_raw.m4a` (`ep03_vo_raw.m4a`,
`epT_vo_raw.m4a`). It moves into the episode's own folder when that
episode is built.

Titles follow the runbook rule (step 9): the words a beginner would type,
in the first 30–40 characters, 50 characters max. Search phrases came
from YouTube autocomplete on 2026-10-09.

---

## Ep 1. What Is a Vector?

**Title:** `What Is a Vector? Linear Algebra for AI`
**Backup:** `Vectors Explained Simply (Linear Algebra for AI)`
**Searched as:** "what is a vector", "vectors explained easy", "linear algebra for ai"

> A vector is just a list of numbers, and it's the key to understanding the math behind AI. Here's how.
>
> My son asked me what "NW" means. Northwest isn't a new direction. It's some west plus some north.
>
> That's a vector: a move through space. Its numbers are the recipe for building that move out of directions we already agreed on.
>
> If the agreed directions are east and north, then minus two, two means two steps opposite east, and two steps north.
>
> *(if time)* In code, a vector is just a list where order matters. Each position means something. For a house, that might be square feet, then price.
>
> Linear algebra is moving between those two views. The arrow lets you see it. The list lets you compute with it.
>
> Every embedding in an AI model is one of these: a list of numbers we treat as a direction in a space with thousands of dimensions.
>
> A vector is a move. Its numbers are the recipe.

---

## Ep 2. Same Vector, Different Numbers

**Title:** `Change of Basis Made Simple (Beginner Friendly)`
**Backup:** `Change of Basis Explained Visually`
**Searched as:** "change of basis", "change of basis linear algebra", "change of basis example"

> The same vector can have completely different numbers. The numbers are an address, and an address depends on the directions you pick.
>
> Those directions are the basis. A basis is a set of independent vectors that spans the whole space. It's the coordinate system you choose.
>
> Here's the point three, five, two, in the usual x, y, z.
>
> Now swap the basis. Keep the point exactly where it is, and let the grid change around it.
>
> In this new basis, the same point is minus two, three, two.
>
> The arrow didn't move. Its address changed, because coordinates are how much of each basis vector you need to get there.
>
> *(if time)* This matters for interpretability. One, one is a little x and a little y. Pick a diagonal basis and it's just one, zero: one clean feature instead of a mix.
>
> Same arrow, new basis, new address.

---

## Ep 3. What a Matrix Really Does

**Title:** `What a Matrix Really Does (Linear Algebra for AI)`
**Backup:** `Linear Transformations Made Simple`
**Searched as:** "linear transformation", "how does a matrix work"

> A matrix just records where each direction lands. Every weight matrix in a neural network is doing exactly this.
>
> Here's e1 and e2. This matrix sends e1 here, and e2 here.
>
> Now take a vector: three of e1 plus two of e2. The vector is a recipe.
>
> After the matrix, keep the same recipe and use the moved directions: three of where e1 landed, plus two of where e2 landed.
>
> The vector supplies the amounts. The matrix supplies the new directions.
>
> That's why the table of numbers isn't random. Each row is one landing spot. In PyTorch, row i of W is where input direction i lands.
>
> *(if time)* In a network, that map moves vectors from one space to another, amplifying some directions and collapsing others.
>
> A matrix is a stored map: where every input direction lands.

---

## Ep 4. What `x @ W` Really Computes

**Title:** `Matrix Multiplication Explained Visually (x @ W)`
**Backup:** `Matrix Multiplication Made Simple (PyTorch)`
**Searched as:** "matrix multiplication explained", "dot product explained visually"

> x at W is just a weighted sum of W's rows. It's the one operation inside every linear layer.
>
> Take x equals one, two, minus one. And W, a three by two matrix. Three rows, one for each input direction, each a 2D landing spot.
>
> Turn x sideways so it sits beside W. Now each number in x is a weight for one row.
>
> One times the first row. Two times the second row. Minus one times the third row.
>
> Now we have three weighted 2D vectors. To add vectors, you add first coordinates together and second coordinates together. That's summing down the columns.
>
> Four, minus one. That's x at W.
>
> Rows are where input directions land. Columns are the totals in each output direction.
>
> *(if time)* Add the bias and you have one row of a linear layer's output: four point one, minus one point two.
>
> Each number in x weights a row of W. Add the rows, and you're done.

---

## Ep 5. The `nn.Linear` Shape Gotcha

**Title:** `PyTorch nn.Linear Explained (Beginner Friendly)`
**Backup:** `nn.Linear Weight Shape Explained (PyTorch)`
**Searched as:** "nn.linear pytorch", "pytorch linear layer"

> You ask nn.Linear for three in and two out, and the weight comes back two by three. It's not a bug. It's the same map, stored sideways.
>
> PyTorch stores one output neuron per row.
>
> A neuron takes all three inputs, multiplies each by its own weight, sums them, adds a bias, and outputs one number. Two outputs, two neurons, two rows of three.
>
> In the forward pass, PyTorch flips it: x at weight dot T, plus bias. The flipped weight is three by two, exactly the W from the last video, where each row is where an input direction lands.
>
> So don't ask which is in and which is out. Ask: where are the landing vectors stored, in the rows or the columns?
>
> *(if time)* In math, vectors are columns, and W times v uses the columns. In PyTorch, vectors are rows, and x at W uses the rows. Same idea, transposed.
>
> nn.Linear stores neurons as rows and transposes on the way through.

---

## Ep 6. One Matmul, Whole Batch

**Title:** `Batch Matrix Multiplication Made Simple (PyTorch)`
**Backup:** `How a Linear Layer Works (Beginner Friendly)`
**Searched as:** "linear layer neural network", "pytorch linear layer"

> One line of PyTorch pushes a whole batch through a layer, because X is data and W is the map.
>
> X is five rows. Each row is one input vector with three features.
>
> W is the map from three dimensions to two.
>
> Here's what unstuck me: X and W are both matrices, but they play different roles. X is data, a stack of vectors. W is a transformation.
>
> So X at W does the same thing to every row. Row one of X weights the rows of W and sums. Then row two. Then all five, in parallel.
>
> Say the shapes out loud: five by three, at three by two, gives five by two. The inner dimensions have to match, and they disappear.
>
> Then the bias broadcasts across every row.
>
> *(if time)* Real data just makes this bigger: batch, sequence, features. The last dimension is always the vector.
>
> Same learned map, many vectors, one line.

---

## Ep 7. Why Layers Need Activations

**Title:** `Why Neural Networks Need Activation Functions`
**Backup:** `Activation Functions Explained Simply`
**Searched as:** "why activation functions are used in neural networks"

> Without activation functions, a hundred-layer neural network is just one matrix.
>
> Here's why. Matrices are functions, and multiplying matrices combines functions.
>
> Stack two layers: x at W1, then that at W2. Order matters, but it's associative. So that's the same as x at W1 times W2.
>
> And W1 times W2 is just one matrix.
>
> So two linear layers, or two hundred, collapse into a single linear transformation. Depth buys you nothing.
>
> A linear map keeps the origin fixed and the grid lines straight. It can stretch, rotate, and squish. It can't bend.
>
> Put a ReLU or a GELU between the layers and the collapse stops. Now each layer can bend the path, and stacking actually adds something.
>
> *(if time)* That's why every layer in a model is a matrix multiply followed by a nonlinearity.
>
> Without activations, a deep network is one matrix.

---

## Ep 8. The Dot Product Measures Alignment

**Title:** `Dot Product Explained Visually (Beginner Friendly)`
**Backup:** `What Does a Dot Product Mean? (for AI)`
**Searched as:** "dot product explained", "dot product explained visually", "dot product meaning"

> A dot product tells you how much two vectors point the same way. It's how AI measures similarity.
>
> The math is simple: multiply pairwise, then sum. One, two, three, dot four, minus one, zero. That's four, minus two, zero. Sum: two.
>
> Watch the number as this arrow turns.
>
> Pointing the same direction: positive.
>
> At ninety degrees, perpendicular, orthogonal: exactly zero. No overlap at all.
>
> Pointing opposite: negative.
>
> That's why it's everywhere in AI. Embeddings that mean similar things point in similar directions, and the dot product is how you check. It's also the core of attention.
>
> *(if time)* It carries length, too. Two long vectors that agree a little can beat two short vectors that agree a lot. That's the next video.
>
> A dot product is alignment: positive, zero, or negative.

---

## Ep 9. Dot, Cosine, Projection

**Title:** `Cosine Similarity vs Dot Product Made Simple`
**Backup:** `Cosine Similarity vs Dot Product vs Projection`
**Searched as:** "cosine similarity vs dot product", "dot product vs cosine similarity"

> Cosine similarity is just a dot product with both lengths divided out. Projection divides out only one. Here's when you want each.
>
> All three start from the same thing: the dot product, alignment with the lengths still in it.
>
> Cosine similarity divides by both lengths. Both magnitudes vanish, and you're left with pure direction, a number between minus one and one. That's what you use to compare embeddings.
>
> Projection divides by only the target's length. Picture casting a shadow from one vector onto another. Projection asks: how much of you points along this direction?
>
> The shadow keeps the original's length in the answer. And it splits the vector in two: the part along the direction, and the leftover.
>
> *(if time)* Even coordinates are projections, one onto each basis direction.
>
> Dot product: alignment with lengths. Cosine: alignment without them. Projection: how much of you lies along that line.

---

## Ep 10. Attention Scores Are Dot Products

**Title:** `Query, Key, Value Explained: Attention Scores`
**Backup:** `Attention Scores Made Simple (Beginner Friendly)`
**Searched as:** "query key value explained", "query key value in transformers"

> An attention score is just a dot product, between one token's query and another token's key.
>
> Every token starts as a vector. A learned matrix, W Q, moves each one into a query: the question this token asks.
>
> Another matrix, W K, moves each one into a key: what question it can help answer.
>
> To score one pair, take one token's query and another token's key. Dot product. High means aligned: this token has what that one is looking for.
>
> Q at K transpose does every pair at once. Three tokens, a three by three grid of scores.
>
> Then divide by the square root of the head size, and softmax turns each row into weights that add up to one.
>
> *(if time)* Transformers process every position in parallel. Attention is how tokens decide who to pull information from.
>
> Attention scores measure which tokens are aligned, under learned projections.

---

## Trailer. The Four Ideas

**Title:** `Linear Algebra for AI Engineers Made Simple`
**Backup:** `Linear Algebra for Machine Learning Made Simple`
**Searched as:** "linear algebra for ai engineer", "linear algebra for machine learning"

> You only need four ideas from linear algebra to understand what AI models are doing.
>
> A vector is a move. Its numbers are the recipe: amounts along directions we agreed on.
>
> A matrix says where those directions land. Multiplying rebuilds the recipe in the new directions.
>
> In PyTorch, x at W is just that: each number in x weights a row of W, and you add them up.
>
> A dot product measures alignment. Attention scores are dot products between queries and keys.
>
> And in a neural network, those matrices are learned. Layer by layer, training finds which directions to amplify, which to ignore, and which to mix.
>
> *(if time)* The model doesn't understand in a human way. It learns moves that make the task easier.
>
> Vectors hold information. Matrices reshape it into forms the model can use.
