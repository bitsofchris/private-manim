"""Beat 1 (3.89 s): a neural network is just a function with a lot of parameters.

VO (0.67-3.89 s): "A neural network is just a function with a lot of parameters."
Frame 0 already has the neurons on screen and the wiring drawing in; the
edges (the parameters) turn magenta on the word "parameters". No scene
captions: word captions are burned in from the VO later (self.band).

Render:
    cd videos/004-backprop-short && uv run --no-sync manim -qh 01_hook.py Hook
    # -> media/videos/01_hook/1920p30/Hook.mp4 (any -q flag gives 1080x1920@30)
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot

BEAT_SECONDS = 3.93   # exact VO window of this beat
LAYERS = [3, 5, 5, 2]
T_FUNCTION = 1.9      # VO: "function"
T_PARAMS = 3.0        # VO: "parameters"
NET_W_FRAC = 0.84     # net width as a fraction of the stage (dots clear the panel edge)
NET_H_FRAC = 0.70     # leaves the top of the stage for the "f" tag
F_TAG_SCALE = 1.6     # "f(x)" tag: bigger than a label, it names the whole panel
EDGE_WIDTH = S.STROKE_STRUCTURE * 0.7   # dim wiring before it becomes the hero


def build_net(stage: Mobject) -> tuple[VGroup, VGroup]:
    """Neurons (teal dots) and every weight edge, laid out to fill the stage."""
    w, h = stage.width * NET_W_FRAC, stage.height * NET_H_FRAC
    xs = np.linspace(-w / 2, w / 2, len(LAYERS))
    layers = []
    for x, n in zip(xs, LAYERS):
        ys = np.linspace(h / 2, -h / 2, n) * (n / max(LAYERS)) ** 0.5
        layers.append([data_dot([x, y, 0], radius=S.DOT_SHORT) for y in ys])
    nodes = VGroup(*[d for layer in layers for d in layer]).set_opacity(1)
    edges = VGroup(*[
        Line(a.get_center(), b.get_center(), color=S.FG_DIM, stroke_width=EDGE_WIDTH,
             stroke_opacity=S.OP_AXIS)
        for la, lb in zip(layers, layers[1:]) for a in la for b in lb
    ])
    VGroup(edges, nodes).move_to(stage).align_to(stage, DOWN).shift(UP * 0.4)
    return nodes, edges


class Hook(BocShortScene):
    def construct(self):
        nodes, edges = build_net(self.stage)
        # Layering by add() order, not z_index: in 0.18.1 a negative z_index
        # hides a mobject while it is being animated.
        # The panel is exactly self.stage: inside the safe area, clear of the
        # left gutter and the top UI bar.
        box = Rectangle(width=self.stage.width, height=self.stage.height,
                        fill_color=S.BG_PANEL, stroke_color=S.FG_DIM,
                        stroke_width=S.STROKE_AXIS * 2)
        box.move_to(self.stage).set_fill(opacity=0).set_stroke(opacity=0)
        self.add(box, edges, nodes)  # frame 0: neurons on screen, edges start drawing

        # "A neural network": the wiring draws in from frame 0.
        # Create the whole group (lag_ratio staggers the lines). LaggedStart over
        # the children of an already-added VGroup renders nothing in 0.18.1.
        self.play(Create(edges, lag_ratio=0.02), run_time=S.HOLD)

        # "is just a function": the stage panel closes around it, labelled f.
        self.hold_until(T_FUNCTION)
        f_tag = Text("f(x)", font=S.FONT, weight="BOLD").scale(F_TAG_SCALE)
        f_tag.set_color(S.FG).align_to(self.stage, UP + LEFT).shift(DOWN * 0.3 + RIGHT * 0.2)
        self.play(box.animate.set_fill(opacity=1).set_stroke(opacity=1), FadeIn(f_tag),
                  run_time=S.BEAT)

        # "a lot of parameters": every edge is a weight -> magenta hero, at full
        # hero stroke and opacity (the thin 0.35-opacity wiring read grey).
        self.hold_until(T_PARAMS)
        self.play(edges.animate.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE, opacity=1),
                  run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
