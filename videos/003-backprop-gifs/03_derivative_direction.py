"""The derivative at the current weight is the slope: it points uphill.

Viewer takeaway: the slope at w says which way to move w to INCREASE the
loss, and that direction flips as w crosses the minimum.

Render:
    cd videos/003-backprop-gifs && uv run manim -qm 03_derivative_direction.py DerivativeDirection
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

import numpy as np
from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocAxes, data_dot, hero_arrow

# GIF clip: rendered small (640px), so everything is scaled up from the 1080p defaults.
GIF_SCALE = 2.2
W_START, W_END = -0.8, 2.8
TANGENT_HALF = 2.4   # half-length of the tangent line, in scene units
ARROW_LEN = 1.5      # uphill arrow length, in scene units


def loss(w: float) -> float:
    return 0.5 * (w - 1) ** 2 + 0.3


def dloss(w: float) -> float:
    return w - 1


def label(text: str, color: str = S.FG_DIM) -> Text:
    return Text(text, font=S.FONT).scale(S.LABEL_SCALE * GIF_SCALE * 0.7).set_color(color)


class DerivativeDirection(BocScene):
    def construct(self):
        axes = BocAxes(
            x_range=[-1.6, 3.6, 1], y_range=[0, 3.6, 1],
            x_length=10, y_length=5.2, tips=False,
        ).shift(DOWN * 0.6)
        curve = axes.plot(loss, x_range=[-1.5, 3.5], color=S.FG_DIM, stroke_width=S.STROKE_STRUCTURE)
        w_lab = label("w").next_to(axes.x_axis.get_right(), DOWN, buff=0.2)
        loss_lab = label("loss").next_to(axes.y_axis.get_top(), RIGHT, buff=0.2)

        w = ValueTracker(W_START)

        def point() -> np.ndarray:
            return axes.c2p(w.get_value(), loss(w.get_value()))

        def unit_tangent() -> np.ndarray:
            # Direction of +w along the curve, measured in scene space.
            v = w.get_value()
            d = axes.c2p(v + 0.01, loss(v) + 0.01 * dloss(v)) - axes.c2p(v, loss(v))
            return d / np.linalg.norm(d)

        def uphill() -> np.ndarray:
            # Uphill = step w in the sign of the slope (that raises the loss).
            return unit_tangent() * (1 if dloss(w.get_value()) >= 0 else -1)

        dot = data_dot(point(), radius=S.DOT_HERO * GIF_SCALE * 1.4)
        dot.add_updater(lambda m: m.move_to(point()))
        dot_lab = label("current w", S.DATA)
        dot_lab.add_updater(lambda m: m.next_to(dot, UP + (RIGHT if dloss(w.get_value()) < 0 else LEFT), buff=0.2))

        def make_tangent() -> Line:
            u = unit_tangent()
            return Line(
                point() - u * TANGENT_HALF, point() + u * TANGENT_HALF,
                color=S.STRUCTURE, stroke_width=S.STROKE_AXIS * 2.5,
            ).set_opacity(0.8)

        def make_arrow() -> Arrow:
            return hero_arrow(
                point(), point() + uphill() * ARROW_LEN,
                stroke_width=S.STROKE_STRUCTURE * 1.6,
                max_tip_length_to_length_ratio=0.3,
            )

        tangent = make_tangent()
        arrow = make_arrow()

        self.play(FadeIn(axes), Create(curve), FadeIn(w_lab), FadeIn(loss_lab), run_time=S.BEAT)
        self.play(FadeIn(dot, scale=0.5), FadeIn(dot_lab), run_time=S.QUICK)
        self.add(dot, dot_lab)
        cap = self.show_caption("slope = which way is uphill")
        self.play(Create(tangent), run_time=S.BEAT)
        self.play(GrowArrow(arrow), run_time=S.BEAT)
        self.beat("BEAT")
        self.hide_caption(cap)

        tangent.add_updater(lambda m: m.become(make_tangent()))
        arrow.add_updater(lambda m: m.become(make_arrow()))
        self.add(tangent, arrow, dot)  # keep dot drawn on top
        cap = self.show_caption("derivative changes with w")
        self.play(w.animate.set_value(W_END), run_time=2 * S.HOLD, rate_func=smooth)
        self.beat("HOLD")
