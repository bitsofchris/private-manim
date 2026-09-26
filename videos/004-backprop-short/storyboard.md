# Backprop in 60 seconds — storyboard

Audio-first. The VO was recorded in one take (`vo_raw.m4a`, 120 s), cleaned
(`tools/enhance_vo.sh` → `vo_clean.wav`), then cut to 59.8 s
(`tools/tighten_vo.py` → `vo_final.wav`; cut list below). Beat boundaries come
from `transcript_final.txt` (MacWhisper CLI). Every scene renders to exactly its
beat length via `hold_until`. Word captions are burned in from `captions.json`
(`tools/captions_from_transcript.py`), not drawn in the scenes.

| # | Beat | Master start | Length | Scene | VO (author's words) |
|---|------|-------------:|-------:|-------|---------------------|
| 1 | Hook | 0.00 | 3.93 | `01_hook.py` `Hook` | A neural network is just a function with a lot of parameters. |
| 2 | Neuron | 3.93 | 7.42 | `02_neuron.py` `Neuron` | Each neuron has its own weight per input and a special term called a bias. The parameters of your network are initialized randomly. |
| 3 | Forward pass + loss | 11.35 | 9.07 | `03_forward_loss.py` `ForwardLoss` | The forward pass is when you take the current training sample, feed it to the model and get the model's output. This comparison allows us to compute the loss. |
| 4 | Derivative | 20.42 | 10.50 | `04_derivative.py` `Derivative` | Now the derivative is a mathematical way to say here's the direction you move a parameter to increase the output of a function, but we will actually move in the opposite direction to make the loss go down. |
| 5 | Backprop | 30.92 | 13.97 | `05_backprop.py` `Backprop` | And backprop is when we start at the loss, set the gradient there equal to 1, we then walk the computational graph backwards and then a rule from calculus called the chain rule is what allows us to take these local derivatives, getting the partial derivatives of the loss, |
| 6 | Gradient | 44.89 | 8.56 | `06_gradient.py` `Gradient` | gives us what's called the gradient, which is just a list of changes to all the parameters in our network that tell us which direction to nudge them all. |
| 7 | Descent | 53.45 | 6.28 | `07_descent.py` `Descent` | We use the learning rate to take a tiny step in that direction and we repeat this over and over and hopefully by the end we train a good model. |

Total 59.73 s. Beat boundaries sit at the end of a 0.4 s pause so each beat cuts on its first word.

## Cuts made to the raw take (all whole phrases; nothing re-recorded)

- "With this output, we then can compare it to the target."
- "In this case, we use that against our loss."
- "And what this tells us is the direction we need to move our weight to make the loss go up." (repeated the next line)
- "'cause that's the thing we want to take the derivative from."
- "to the beginning where we have our inputs."
- "for each node in this computational graph,"
- "with respect to these individual parameters."
- "And together across our whole network,"
- "which is just a list of terrain," (flub) and a false start
- "to try to make our loss go down."
- "When we begin training," (beat 3 opened on 3 s of nothing moving)
- "because these derivatives are only accurate at the current values for each weight."
- Pauses capped at 0.25 s inside beats, 0.4 s at beat boundaries; tempo +3 %.

## Assemble

```
cd videos/004-backprop-short
for f in 0*_*.py; do uv run --no-sync manim -qh $f; done   # or one at a time
uv run --no-sync python ../../tools/assemble.py beats.json --vo vo_final.wav \
    --captions captions.json -o media/backprop_short.mp4
```
