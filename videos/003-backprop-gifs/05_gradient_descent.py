"""Step opposite the gradient, scaled by a small learning rate; repeat and loss falls.

Render:
    cd videos/003-backprop-gifs && uv run manim -qm 05_gradient_descent.py GradientDescent
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import data_dot, hero_arrow, BocAxes

W_MIN = 1.0                # bowl minimum at w = 1
W_START = -1.2
LR = 0.35
N_STEPS = 5
GRAD_VIS = 0.6            # scene units of dim gradient arrow per unit of |dL/dw|


def loss(w: float) -> float:
    return 0.5 * (w - W_MIN) ** 2 + 0.3


def grad(w: float) -> float:
    return w - W_MIN


def txt(s: str, color: str = S.FG_DIM, scale: float = S.CAPTION_SCALE) -> Text:
    return Text(s, font=S.FONT).scale(scale).set_color(color)


class GradientDescent(BocScene):
    def construct(self):
        axes = BocAxes(
            x_range=[-2, 3, 1], y_range=[0, 3.5, 1],
            x_length=9, y_length=5, tips=False,
        ).shift(DOWN * 0.45)
        x_lab = txt("w").next_to(axes.x_axis.get_right(), DOWN, buff=0.2)
        y_lab = txt("loss").next_to(axes.y_axis.get_top(), RIGHT, buff=0.2)
        curve = axes.plot(loss, x_range=[-1.75, 3], color=S.FG_DIM, stroke_width=S.STROKE_STRUCTURE / 2)
        lr_tag = txt(f"lr = {LR}", scale=S.LABEL_SCALE).next_to(axes.c2p(3, 0), UP + LEFT, buff=0.2)

        w = ValueTracker(W_START)
        dot = data_dot(radius=S.DOT_GIF)
        dot.set_opacity(1)
        dot.add_updater(lambda m: m.move_to(axes.c2p(w.get_value(), loss(w.get_value()))), call_updater=True)
        self.add(axes, curve, x_lab, y_lab, lr_tag, dot)
        self.beat("BEAT")

        cap = None
        for i in range(N_STEPS):
            first = i == 0
            run = S.BEAT  # QUICK made the later steps flicker at 15 fps
            w0 = w.get_value()
            g = grad(w0)
            w1 = w0 - LR * g
            p0 = axes.c2p(w0, loss(w0))

            # Dim gradient arrow: along the tangent, pointing uphill.
            dw = 0.01 * np.sign(g)
            tangent = axes.c2p(w0 + dw, loss(w0 + dw)) - p0
            tangent /= np.linalg.norm(tangent)
            g_arrow = hero_arrow(p0, p0 + tangent * GRAD_VIS * abs(g), color=S.FG)

            # Magenta hero: the actual step, opposite the gradient along w.
            step = hero_arrow(p0, axes.c2p(w1, loss(w0)))

            ghost = data_dot(p0, radius=S.DOT_GIF).set_opacity(S.OP_GHOST)

            if first:
                cap = self.show_caption("step opposite the gradient")
                self.play(GrowArrow(g_arrow), run_time=run)
                self.play(GrowArrow(step), run_time=run)
            else:
                self.play(GrowArrow(g_arrow), GrowArrow(step), run_time=run)
            self.add(ghost)
            self.bring_to_front(dot)
            self.play(
                w.animate.set_value(w1),
                FadeOut(g_arrow), FadeOut(step),
                run_time=run,
            )
            if first:
                self.hide_caption(cap)

        self.show_caption("repeat: loss goes down")
        self.beat("HOLD")
        self.beat("HOLD")
