# 003 - Backprop GIFs

Five tiny looping GIFs to embed in a Substack post explaining backprop.
Each is a single short scene (5-9 s), rendered at 720p then converted to a
GIF small enough for Substack's email limit (target < 1.5 MB each).

| # | File | Concept from the post |
|---|------|------------------------|
| 1 | `01_neuron.py` / `Neuron` | A neuron has one weight per input plus a bias; params start random |
| 2 | `02_forward_pass_loss.py` / `ForwardPassLoss` | Forward pass produces an output; compare to target; the gap is the loss |
| 3 | `03_derivative_direction.py` / `DerivativeDirection` | The derivative at the current weight is the slope: the direction that increases loss |
| 4 | `04_backprop_graph.py` / `BackpropGraph` | Backprop sets grad=1 at the loss and walks the graph backward, chain-ruling local derivatives |
| 5 | `05_gradient_descent.py` / `GradientDescent` | Step opposite the gradient, scaled by a small learning rate; repeat and loss falls |

## Render + GIF

```
cd videos/003-backprop-gifs
uv run manim -qm 01_neuron.py Neuron
../_shared/to_gif.sh media/videos/01_neuron/720p30/Neuron.mp4 gifs/01_neuron.gif
```

GIFs land in `videos/003-backprop-gifs/gifs/`.

## Notes

- These scenes use `Text` instead of `MathTex` / `DecimalNumber` on purpose:
  there is no LaTeX on this machine, and plain text is more legible at GIF size.
- Manim needs Homebrew `cairo`, `pango`, and `pkg-config`. If `uv run manim`
  tries to build pycairo from source and fails, install those and `uv sync`.
