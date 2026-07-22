# 002 - Linear Algebra Basics

Manim project folder for short explainer videos that support Chris's linear
algebra study plan.

## Source Plan

Primary learning plan:

`/Users/chris/repos/deep-learning/code/22_ai-foundations-linear-algebra/README.md`

That plan organizes the linear algebra block by units:

- Unit 0 - Baseline: Vectors and Embeddings
- Unit 1 - Vectors, Span, Basis
- Unit 2 - Matrices as Linear Maps
- Unit 3 - Matrix Multiplication as Composition
- Unit 4 - Dot Product, Norms, Projection
- Unit 5 - Attention Scores
- Unit 6 - Rank, Nullspace, Low-Rank Structure
- Unit 7 - Change of Basis
- Unit 8 - SVD
- Unit 9 - QK / OV / Transformer Circuits Bridge
- Unit 10 - Video Storyboard
- Artifact Unit - Ship Rough Explainer

## Current Focus

Unit 1 source note:

`/Users/chris/repos/deep-learning/code/22_ai-foundations-linear-algebra/unit_01_vectors_span_basis.md`

Core question:

> How do vectors combine to form spaces, and what is a basis?

Expected learning output:

> Basis = a coordinate system for a vector space.

Include an example where the same vector has different coordinates in two
bases.

Likely visual territory for upcoming videos:

- Linear combinations as scaled arrows added tip-to-tail.
- Span as every reachable point from combinations of chosen vectors.
- Basis as the minimum independent set of vectors that gives coordinates.
- Dependence in R2: a third vector can be useful as a visual cue, but it cannot
  make three independent directions in a 2D plane.
- Embeddings connection: a basis determines how a vector's coordinates are read.

## Repo Instructions To Follow

This repo has hard Manim conventions in `/Users/chris/repos/private-manim/AGENTS.md`
and `/Users/chris/repos/private-manim/videos/_shared/STYLE.md`.

Always use the repo style guide when writing or editing scenes. If a prompt asks
for a visual treatment that conflicts with the guide, preserve the learning goal
and adapt the visual to the house style.

Scene files must:

- Import from `videos._shared`.
- Add the required three-line `sys.path` shim because scenes are rendered from
  inside this folder.
- Subclass `BocScene` for 2D or `Boc3DScene` for 3D.
- Use shared constants from `videos/_shared/style.py`; add missing constants
  there before using them.
- Use shared mobjects like `data_dot`, `hero_arrow`, `residual`, `BocAxes`,
  `BocNumberPlane`, and `BocThreeDAxes` instead of raw `Dot`, `Arrow`, or `Axes`
  for those visual roles.
- Keep teal (`S.DATA`) for visible data and magenta (`S.STRUCTURE`) for the one
  discovered or emphasized direction per beat.
- Use only `S.QUICK`, `S.BEAT`, and `S.HOLD` motion durations via
  `self.beat("QUICK"|"BEAT"|"HOLD")`.
- Use `self.show_caption(...)` and `self.hide_caption(t)` for captions.
- Use `axes.c2p(...)` for every coordinate.
- Keep one scene class per file and aim for files under about 120 lines.

Each video also needs Markdown notes in this README covering:

- What the video teaches.
- The core intuition.
- The explanation/story beats the scene is meant to communicate.

Each time a new video is added, also update the **Master Video Outline** below.
Keep it in intended viewing order. For each entry, include the video title and a
brief note for what Chris would say or what the video is describing.

## Local Rendering Constraint

Do not use LaTeX-dependent mobjects in this project. `latex` is not available
reliably in this environment, so avoid `MathTex` and `Tex`; use `Text` with
plain readable formulas instead.

## Render Workflow

Always render from this folder so output lands in this project's local
`media/` directory:

```bash
cd /Users/chris/repos/private-manim/videos/002-linear-algebra-basics
uv run manim -pql <scene_file>.py <SceneClass>
```

Use fast low-quality renders while developing. Default to `-ql` or `-pql` for
iteration. Only use high-resolution options such as `-qh` / `-pqh` when the
video is ready to ship to YouTube.

Do not render from the repo root with a path like
`videos/002-linear-algebra-basics/<scene_file>.py`; that creates a top-level
`media/` folder and breaks the repo convention.

Manim output path:

```text
media/videos/<scene_file>/<quality>/<SceneClass>.mp4
```

Re-rendering the same scene class overwrites the previous take.

## Scene Template

```python
"""One-sentence viewer takeaway.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql <scene_file>.py <SceneClass>
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *
from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocAxes, data_dot, hero_arrow, residual


class ExampleScene(BocScene):
    def construct(self):
        ...
```

## Master Video Outline

Keep this list up to date as videos are added. This is the sequence-level script
outline, not just an implementation index.

1. **Northwest Is a Linear Combination** (`northwest_linear_combination.py`)
   Open with the driving-directions hook: northwest is not a magic new
   direction, it is some west plus some north. Say: a vector is the move, and
   coordinates are the recipe for building that move from agreed directions.

2. **A Plane Can Have Many Bases** (`plane_many_bases.py`)
   Describe a fixed plane in 3D, then show that different pairs of basis vectors
   can draw different coordinate grids on the same plane. Say: the plane is the
   same object, but the axes we choose inside it are a choice.

3. **Same Vector, Different Basis** (`basis_transformation_3d.py`)
   Start with the standard grid and a target vector, then deform to a new basis
   while the target point stays fixed. Say: coordinates are coefficients, so the
   address changes when the basis changes even though the vector does not.

4. **A Matrix Moves Basis Directions** (`matrix_moves_basis_directions.py`)
   Show original basis arrows, then show where a matrix sends those arrows.
   Rebuild the same vector recipe using the moved directions. Say: the matrix
   changes the ingredients; the vector's coordinate recipe tells us how much of
   each moved direction to use.

5. **A Matrix Is the Stored Map** (`matrix_as_stored_map.py`)
   Show `W` as a table of numbers, then pull each row out as an arrow in the
   output space. Say: in the PyTorch row-vector view, the matrix stores where
   input directions land; multiplication applies that stored map.

6. **Batched Matrix Multiply as PyTorch Tensors** (`batched_linear_map_tensors.py`)
   Show `X` as five input rows, `W` as the shared map, and `Y` as five output
   rows. Say: each row of `X` supplies weights for the rows of `W`, and PyTorch
   performs that same operation across the whole batch.

7. **One Row Becomes One Weighted Sum** (`one_row_weighted_sum.py`)
   Zoom into the first row of `X`, turn it into a column of weights beside `W`,
   scale each row of `W`, then sum the weighted rows and add bias. Say: this is
   the single operation hiding inside one row of `X @ W + b`.

8. **How `nn.Linear` Stores the Same Map** (`nn_linear_weight_structure.py`)
   Show that PyTorch stores `linear.weight` as `(out_features, in_features)`, so
   the forward pass uses a transposed view, `linear.weight.T`. Say: each stored
   weight row is one output neuron, and each neuron activation fills one slot in
   `Y[0]`.

9. **ML Layer: 5D Inputs to 3D Outputs** (`ml_layer_5d_to_3d.py`)
   Show `X @ W` with `X` shaped `(3, 5)` and `W` shaped `(5, 3)`. Say: in the
   ML row-vector convention, row `i` of `W` is where input basis direction `i`
   lands; `x[i]` weights that row, and summing down the output columns creates
   the new 3D output vector.

10. **Rows Land, Columns Add** (`rows_land_columns_add.py`)
   Slow down the previous multiplication and explain why the column sums are
   the output coordinates. Say: rows are moved input directions written in
   output coordinates; once `x[i]` weights those rows, summing down each column
   is just coordinate-by-coordinate vector addition.

11. **Vectors Become Useful Representations** (`ai_vectors_to_representations.py`)
   Pull the whole arc into AI: token embeddings, image patches, and feature rows
   start as vectors; learned matrices move them into spaces where useful
   structure is easier to read. Say: vectors hold information, and matrices
   reshape that information into forms the model can use.

## Scene Notes

### `northwest_linear_combination.py` - `NorthwestLinearCombination`

Teaches the post's opening hook: northwest is a linear combination of familiar
directions.

Core intuition: a vector is a move through space. Coordinates are not the whole
story; they are a recipe that only makes sense once the basis directions are
agreed on.

Explanation path: show east and north as the agreed directions, build northwest
as `2 west` followed by `2 north`, then draw the single northwest arrow and the
coordinate recipe `(-2, 2) = -2 * east + 2 * north`.

### `plane_many_bases.py` - `PlaneManyBases`

Teaches that a fixed subspace can have many internal coordinate systems. The
plane `x + y + z = 0` does not change, but the two basis arrows and the grid
drawn on that plane do change.

Core intuition: a basis is a coordinate system for a space, not the space
itself. The same point on the plane has one address in Basis A and another
address in Basis B.

Explanation path: first establish the ambient 3D axes, then reveal the plane,
check points that do and do not satisfy the equation, draw Basis A and reach a
target point, then swap to Basis B and show the same target now has new
coordinates.

### `basis_transformation_3d.py` - `BasisTransformation3D`

Teaches that a vector in R3 has different coordinates in different bases. The
standard basis is useful, but it is still a choice.

Core intuition: coordinates are coefficients. When the coordinate grid changes,
the point in space can stay fixed while its address changes.

Explanation path: start with the standard basis and a cubic lattice, reach the
target `(3, 5, 2)` by walking along `e1`, `e2`, and `e3`, then deform the lattice
toward the basis `v1=(1,0,0)`, `v2=(1,1,0)`, `v3=(1,1,1)`. The same target is
then reached by `-2*v1 + 3*v2 + 2*v3`, so its new coordinates are `(-2, 3, 2)`.

### `matrix_moves_basis_directions.py` - `MatrixMovesBasisDirections`

Teaches the key bridge sentence for the post: a matrix moves basis directions.

Core intuition: once a matrix tells us where `e1` and `e2` land, every vector
made from `e1` and `e2` comes along for the ride. Matrix-vector multiplication
rebuilds the same coordinate recipe using the moved directions.

Explanation path: show the original basis, show the moved basis directions
`A(e1)` and `A(e2)`, build `v = 3*e1 + 2*e2`, then rebuild
`A(v) = 3*A(e1) + 2*A(e2)`.

### `matrix_as_stored_map.py` - `MatrixAsStoredMap`

Teaches the bridge from geometric linear maps to the table of numbers used in
code.

Core intuition: a matrix is the stored description of a linear map. In the
PyTorch row-vector convention, each row of `W` stores where one input direction
lands in the output space.

Explanation path: show `W` as a `(3, 2)` table, label each row as one stored
landing direction, pull the rows out as arrows in the 2D output space, then use
`x = [1.0, 2.0, -1.0]` as weights on those arrows and sum to `[4.0, -1.0]`.

### `batched_linear_map_tensors.py` - `BatchedLinearMapTensors`

Teaches the Unit 2 idea that a matrix is a linear map, and PyTorch applies that
same map to every row in a batch with `X @ W + b`.

Core intuition: each row of `X` is one input data point. Its three scalar
components are weights. Those weights pair with the three rows of `W`, where
each row of `W` is a 2D destination for one input basis direction. Weight those
three `W` rows, add them, then add the broadcast bias to get one row of `Y`.

Explanation path: show `X` as a `(5, 3)` PyTorch-style tensor, `W` as a `(3, 2)`
tensor, and `Y` as `(5, 2)`. First zoom conceptually into one row of `X` and
color-match its three weights to the three rows of `W`. Then sweep the same
operation across all five rows to make the batch behavior concrete. Close with
the shape check: `(5, 3) @ (3, 2) -> (5, 2)`, then `b` with shape `(2,)`
broadcasts across rows.

### `one_row_weighted_sum.py` - `OneRowWeightedSum`

Teaches the single-row operation inside `X @ W + b`. This is the close-up view
of the first row from the batched tensor video.

Core intuition: a row vector times `W` is not mysterious matrix machinery. Turn
the row into a column of weights beside `W`. The first weight scales the first
row of `W`, the second weight scales the second row, and the third weight scales
the third row. The weighted rows then sum column by column.

Explanation path: start from `X[0] = [1.0, 2.0, -1.0]`, rotate it into a weight
column beside `W`, draw each weighted row, show the raw sum `[4.0, -1.0]`, add
the bias `[0.1, -0.2]`, then move the final result `[4.1, -1.2]` into the first
row of `Y`.

### `nn_linear_weight_structure.py` - `NNLinearWeightStructure`

Teaches the same Unit 2 problem in the structure PyTorch actually uses for
`nn.Linear`.

Core intuition: `nn.Linear(3, 2)` stores `linear.weight` as `(2, 3)`, one row per
output neuron. Conceptually, the forward pass uses
`X @ linear.weight.T + linear.bias`, so it produces the same `(5, 2)` output
tensor as the earlier videos.

Explanation path: show `X` as the input tensor, show `linear.weight` as two rows
of three weights, and show `linear.bias` as two bias values. Then reveal
`linear.weight.T` to connect PyTorch's storage layout back to the matrix
multiplication view. Finish by reframing the two rows of `linear.weight` as two
neurons: the first neuron produces `Y[0,0]`, and the second neuron produces
`Y[0,1]`; together those two scalar outputs form the vector `Y[0]`.

### `ml_layer_5d_to_3d.py` - `MLLayer5DTo3D`

Teaches the ML row-vector convention for a layer-style multiplication:
`X @ W`, where `X` is `(3, 5)`, `W` is `(5, 3)`, and `Y` is `(3, 3)`.

Core intuition: each row of `X` is one 5D input vector. Each row of `W` is the
image of one input basis direction, now living in 3D output space. For one input
row `x`, the component `x[i]` weights row `i` of `W`; after every row is
weighted, summing down each column creates the output vector.

Explanation path: first show the full batch shape check: three 5D input rows
project through a `(5, 3)` matrix into three 3D output rows. Then label each row
of `W` as the landing place of one input basis direction. Zoom into `x[0]`, turn
its five components into weights beside `W`, show each weighted row, draw
column guides, sum down the columns, and place the result into `Y[0]`.

### `rows_land_columns_add.py` - `RowsLandColumnsAdd`

Teaches the intuition behind column sums in `x @ W`.

Core intuition: each row of `W` is a moved input direction, written in output
coordinates. The input component `x[i]` says how much of row `i` to use. After
the rows are weighted, summing down columns is not a separate trick; it is
normal vector addition coordinate by coordinate.

Explanation path: start with one 5D input recipe `x = [2, -1, 0, 3, 1]`. Show
the `(5, 3)` matrix as five landing vectors in 3D. Weight each row by the
matching input component, producing a weighted-row table. Then highlight each
column and show that adding the first coordinates gives `y[0]`, adding the
second coordinates gives `y[1]`, and adding the third coordinates gives `y[2]`.
Close with: rows are moved input directions; columns are output-coordinate
totals.

### `ai_vectors_to_representations.py` - `AIVectorsToRepresentations`

Teaches why the vector-to-matrix story matters for AI.

Core intuition: vectors hold information. Learned matrices reshape that
information into representations that make the next step easier. The model is
not understanding in a human way; training discovers transformations that help
the objective.

Explanation path: start with raw vector data examples: token embeddings, image
patches, and feature rows. Move them through a learned matrix `W`. Around `W`,
ask the layer-level questions: which directions should be amplified, ignored,
or mixed together? Then show more useful representation spaces: attention
query/key/value spaces, edge and texture features, and task-useful prediction
features. Close with: vectors hold information; matrices reshape it into forms
the model can use.

## Director Arc Check

The intended audience journey:

1. A vector is a move, and coordinates are the recipe for building that move
   from agreed directions.
2. A basis is the set of agreed directions, so changing the basis changes the
   coordinate recipe without changing the underlying vector or space.
3. A matrix says where the basis directions land.
4. Multiplication uses the vector's amounts and the matrix's new directions:
   the vector provides the weights, the matrix provides the destinations, and
   the result is the rebuilt vector in a new space.
5. In PyTorch's row-vector convention, rows of `X` provide weights and rows of
   `W` act as the landing directions for input basis components.
6. `nn.Linear` stores the same learned map in neuron form: one stored weight row
   per output value.
7. A layer multiplication with `(batch, in_features) @ (in_features,
   out_features)` repeats the same row-weighted linear combination for every
   input row.
8. Column sums are the output coordinates because weighted output-space vectors
   add coordinate by coordinate.
9. For AI, those learned maps turn raw vector data into more useful
   representations by amplifying, ignoring, and mixing directions.

Director notes:

- Videos 1-3 establish that coordinates are basis-dependent recipes. This is
  strong and should stay before matrices.
- Videos 4-5 are the key conceptual bridge. The recurring punchline should be:
  the vector supplies the amounts; the matrix supplies the new directions.
- Videos 6-10 translate the geometry into PyTorch. Keep reminding the viewer
  that batching does not change the idea; it repeats the same learned move for
  many input rows. Video 10 is the slow intuition pass for why column sums are
  output coordinates.
- Video 11 is the AI payoff. It should feel like the reason the prior mechanics
  mattered, not a separate topic.

## Planned Scenes

| File | Class | Unit | Status |
| --- | --- | --- | --- |
| `northwest_linear_combination.py` | `NorthwestLinearCombination` | Unit 1 - Vectors, Span, Basis | Drafting |
| `plane_many_bases.py` | `PlaneManyBases` | Unit 1 - Vectors, Span, Basis | Drafted |
| `basis_transformation_3d.py` | `BasisTransformation3D` | Unit 1 - Vectors, Span, Basis | Drafting |
| `matrix_moves_basis_directions.py` | `MatrixMovesBasisDirections` | Unit 2 - Matrices as Linear Maps | Drafting |
| `matrix_as_stored_map.py` | `MatrixAsStoredMap` | Unit 2 - Matrices as Linear Maps | Drafting |
| `batched_linear_map_tensors.py` | `BatchedLinearMapTensors` | Unit 2 - Matrices as Linear Maps | Drafting |
| `one_row_weighted_sum.py` | `OneRowWeightedSum` | Unit 2 - Matrices as Linear Maps | Drafting |
| `nn_linear_weight_structure.py` | `NNLinearWeightStructure` | Unit 2 - Matrices as Linear Maps | Drafting |
| `ml_layer_5d_to_3d.py` | `MLLayer5DTo3D` | Unit 2 - PyTorch Layer Multiplication | Drafting |
| `rows_land_columns_add.py` | `RowsLandColumnsAdd` | Unit 2 - PyTorch Layer Multiplication | Drafting |
| `ai_vectors_to_representations.py` | `AIVectorsToRepresentations` | Unit 2 - AI Representation Bridge | Drafting |
