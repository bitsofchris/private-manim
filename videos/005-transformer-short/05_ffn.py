"""Beat 5 (11.45 s): a feed-forward net works on each token alone, learns which
feature combinations matter, amplifies them, and a non-linearity makes the
choice depend on the input.

VO (scene-local s): "A feed forward network then works on each token alone"
0.03-3.16 ("alone" ~2.9); "It learns which combinations of features matter"
3.17-5.2; "amplifying the ones that do" 5.2-6.72; "and then adds a
non-linearity on top" 6.75-8.75 ("non-linearity" ~7.8); "that lets the choice
depend on the input" 8.78-11.41. No scene captions (burned in over self.band).

Opens on beat 4's end (bracketed VALUES_AFTER_ATTN + words); ends on words +
bracketed VALUES[2], nothing else.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 05_ffn.py FeedForward
    # -> media/videos/05_ffn/1920p30/FeedForward.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot
from _tokens import VALUES, VALUES_AFTER_ATTN, build_matrix, word_labels

BEAT_SECONDS = 11.45  # exact VO window of this beat
T_ALONE = 1.8         # copies drop under the other columns, landing on "alone" (~2.9)
T_COMBINE = 3.4       # VO: "which combinations of features"
T_AMPLIFY = 5.3       # VO: "amplifying"
T_KINK = 7.4          # VO: "non-linearity" (~7.8)
T_DEPEND = 8.9        # VO: "depend on the input": outputs feed up, numbers tick

LAYERS = [3, 5, 3]            # input dots (the cells) -> hidden row -> output dots
NET_W = 1.5                   # narrower than a column so the kink glyph fits beside net 1
ROW_Y = [1.1, 0.0, -0.95]     # input / hidden / output rows, in the free region under the matrix
IO_SPREAD = 0.7               # input and output rows use this fraction of NET_W
NODE_R = S.DOT_SHORT * 0.6    # ~31 px: 5 hidden dots must fit under one column
EDGE_WIDTH = S.STROKE_STRUCTURE * 0.6
HERO_HIDDEN = 1               # the hidden dot that learns a combination
HERO_INPUTS = (0, 2)          # the features it combines
AMPLIFY = 1.6                 # how much that hidden dot grows
KINK_W, KINK_H = 0.55, 0.8    # the ReLU glyph: flat, then rising; tall so it reads at phone size
KINK_STROKE = S.STROKE_STRUCTURE * 2


def build_net(x: float) -> tuple[VGroup, VGroup, list[list[Dot]]]:
    """A tiny FFN centred at x: (nodes, edges, layers). Edges run top to bottom."""
    layers = []
    for n, y in zip(LAYERS, ROW_Y):
        w = NET_W * (1.0 if n == max(LAYERS) else IO_SPREAD)
        xs = np.linspace(x - w / 2, x + w / 2, n)
        layers.append([data_dot([px, y, 0], radius=NODE_R).set_opacity(1) for px in xs])
    nodes = VGroup(*[d for layer in layers for d in layer])
    edges = VGroup(*[
        Line(a.get_center(), b.get_center(), color=S.FG_DIM, stroke_width=EDGE_WIDTH,
             stroke_opacity=S.OP_DATA)
        for la, lb in zip(layers, layers[1:]) for a in la for b in lb
    ])
    return nodes, edges, layers


def relu_glyph() -> VMobject:
    """Two segments: flat, then a kink up and to the right."""
    return VMobject(stroke_color=S.STRUCTURE, stroke_width=KINK_STROKE).set_points_as_corners(
        [[-KINK_W / 2, -KINK_H / 2, 0], [-KINK_W / 10, -KINK_H / 2, 0], [KINK_W / 2, KINK_H / 2, 0]])


class FeedForward(BocShortScene):
    def construct(self):
        m = build_matrix(self.stage, values=VALUES_AFTER_ATTN, digits=True, bracketed=True)
        words = word_labels(m)
        self.add(m, words)  # frame 0: beat 4's last frame

        nets = []
        for col in m.columns:
            nodes, edges, layers = build_net(col.get_x())
            nets.append((VGroup(edges, nodes), layers))
        net1, layers1 = nets[0]

        # "A feed forward network": one tiny net draws in under the first column.
        self.play(Create(net1[0], lag_ratio=0.02), FadeIn(net1[1], lag_ratio=0.05),
                  run_time=S.HOLD)

        # "each token alone": identical copies drop under the other two columns.
        self.hold_until(T_ALONE)
        self.play(LaggedStart(*[TransformFromCopy(net1, net) for net, _ in nets[1:]],
                              lag_ratio=0.3), run_time=S.HOLD)

        # "which combinations of features": a few edges into one hidden dot go magenta.
        self.hold_until(T_COMBINE)
        hidden = layers1[1][HERO_HIDDEN]
        n_hidden = LAYERS[1]
        combo = VGroup(*[net1[0][i * n_hidden + HERO_HIDDEN] for i in HERO_INPUTS])
        self.play(combo.animate.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE, opacity=1),
                  run_time=S.HOLD)

        # "amplifying": that hidden dot grows and brightens to the hero color.
        self.hold_until(T_AMPLIFY)
        self.play(hidden.animate.scale(AMPLIFY).set_color(S.STRUCTURE), run_time=S.HOLD)

        # "non-linearity": a ReLU kink beside the hidden row, in the gutter left of net 1.
        self.hold_until(T_KINK)
        kink = relu_glyph().move_to([(self.stage.get_left()[0] + net1.get_left()[0]) / 2,
                                     ROW_Y[1], 0])
        self.play(Create(kink), run_time=S.HOLD)

        # "depend on the input": the outputs feed up through every net and each
        # column ticks to VALUES[2]; then the nets (and the hero) fade.
        self.hold_until(T_DEPEND)
        flash = VGroup(*[
            Line(e.get_end(), e.get_start(), color=S.HIGHLIGHT, stroke_width=S.STROKE_STRUCTURE)
            for net, _ in nets for e in net[0]
        ])
        self.play(ShowPassingFlash(flash, time_width=0.4), m.count_to(VALUES[2]),
                  run_time=S.HOLD)
        self.play(FadeOut(VGroup(*[net for net, _ in nets]), kink), run_time=S.HOLD)
        self.hold_until(BEAT_SECONDS)
