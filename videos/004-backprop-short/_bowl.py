"""Shared loss bowl for beats 4 (derivative) and 7 (descent) of the backprop Short.

One quadratic loss over one weight w, drawn to fill the Short's stage, plus
helpers for points and tangent directions on it. Both scenes import this so
they read as the same world.
"""
from __future__ import annotations

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Mobject, Text, VGroup

from videos._shared import style as S
from videos._shared.mobjects import BocAxes

W_MIN = 2.8              # bowl minimum; y-axis sits at w = 0 on the left edge
X_RANGE = (0.0, 5.0)
Y_RANGE = (0.0, 4.4)
AXES_W_FRAC = 0.97       # axes span nearly the full stage width
X_AXIS_LIFT = 1.0        # room under the x-axis for the "w" label
TOP_PAD = 0.15
CURVE_WIDTH = S.STROKE_STRUCTURE * 1.6   # thin curves vanish at phone size


def loss(w: float) -> float:
    return 0.5 * (w - W_MIN) ** 2 + 0.3


def grad(w: float) -> float:
    return w - W_MIN


def label(text: str, color: str = S.FG_DIM) -> Text:
    return Text(text, font=S.FONT).scale(S.SHORT_LABEL_SCALE).set_color(color)


def build_bowl(stage: Mobject) -> tuple:
    """(axes, curve, labels) sized to fill `stage`. Nothing is added to a scene."""
    height = stage.height - X_AXIS_LIFT - TOP_PAD
    axes = BocAxes(
        x_range=[*X_RANGE, 1], y_range=[*Y_RANGE, 1],
        x_length=stage.width * AXES_W_FRAC, y_length=height, tips=False,
    )
    axes.move_to(stage).align_to(stage, DOWN).shift(UP * X_AXIS_LIFT)
    curve = axes.plot(loss, x_range=[X_RANGE[0] + 0.05, X_RANGE[1]],
                      color=S.FG_DIM, stroke_width=CURVE_WIDTH)
    w_lab = label("w").next_to(axes.c2p(X_RANGE[1], 0), DOWN, buff=0.2).align_to(
        axes.c2p(X_RANGE[1], 0), RIGHT)
    loss_lab = label("loss").next_to(axes.c2p(0, Y_RANGE[1]), RIGHT, buff=0.25).align_to(
        axes.c2p(0, Y_RANGE[1]), UP)
    return axes, curve, VGroup(w_lab, loss_lab)


def point(axes, w: float) -> np.ndarray:
    return axes.c2p(w, loss(w))


def uphill(axes, w: float) -> np.ndarray:
    """Unit scene-space vector along the tangent at w, pointing uphill."""
    dw = 0.01 * (1 if grad(w) >= 0 else -1)
    d = axes.c2p(w + dw, loss(w) + dw * grad(w)) - axes.c2p(w, loss(w))
    return d / np.linalg.norm(d)


def descent_path(w0: float, lr: float, n: int) -> list[float]:
    """[w0, w1, ..., wn] from plain gradient descent: w -= lr * grad(w)."""
    ws = [w0]
    for _ in range(n):
        ws.append(ws[-1] - lr * grad(ws[-1]))
    return ws
