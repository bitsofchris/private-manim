"""Beat 4 (10.57 s): the derivative points uphill; we step the opposite way.

VO: "Now the derivative is a mathematical way to say here's the direction you
move a parameter to increase the output of a function, but we will actually
move in the opposite direction to make the loss go down."
The magenta hero is the tangent + direction arrow at the teal dot. Change
times below are scene-local, read off the VO's energy envelope (the phrase
pauses) plus the whisper segment boundaries.

Render:
    cd videos/004-backprop-short && uv run --no-sync manim -qh 04_derivative.py Derivative
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # this folder, for _bowl

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot, hero_arrow
from _bowl import build_bowl, label, point, uphill

BEAT_SECONDS = 10.50
T_DERIVATIVE = 0.3    # "Now the derivative"
T_DIRECTION = 2.4     # "here's the direction"
T_INCREASE = 4.15     # "to increase the output"
T_NUDGE = 4.85
T_OPPOSITE = 7.6      # "move in the opposite direction"
T_DOWN = 9.1          # "to make the loss go down"
W_START, W_END = 1.0, 1.6
NUDGE_DW = -0.2       # uphill nudge on "increase" (and back)
TANGENT_HALF = 2.3    # scene units
ARROW_LEN = 2.0       # scene units
ARROW_WIDTH = S.STROKE_STRUCTURE * 3.5 # phone-legible
ARROW_TIP = 0.6                        # scene units; default 0.35 vanishes on a phone
TANGENT_WIDTH = S.STROKE_STRUCTURE * 1.5
TANGENT_OPACITY = 0.55                 # tangent recedes; the arrow is the hero


class Derivative(BocShortScene):
    def construct(self):
        axes, curve, labels = build_bowl(self.stage)
        w = ValueTracker(W_START)
        sign = ValueTracker(1.0)   # +1: arrow points uphill, -1: downhill

        def p():
            return point(axes, w.get_value())

        def make_tangent() -> Line:
            u = uphill(axes, w.get_value())
            return Line(p() - u * TANGENT_HALF, p() + u * TANGENT_HALF, color=S.STRUCTURE,
                        stroke_width=TANGENT_WIDTH).set_opacity(TANGENT_OPACITY)

        def make_arrow(s: float) -> Arrow:
            return hero_arrow(p(), p() + s * uphill(axes, w.get_value()) * ARROW_LEN,
                              stroke_width=ARROW_WIDTH, tip_length=ARROW_TIP,
                              max_tip_length_to_length_ratio=0.35,
                              max_stroke_width_to_length_ratio=ARROW_WIDTH)

        dot = data_dot(p(), radius=S.DOT_SHORT).set_opacity(1)
        self.add(axes, curve, labels, dot)  # frame 0: the bowl and the current weight

        # "the derivative": the tangent line grows at the dot.
        self.hold_until(T_DERIVATIVE)
        tangent = make_tangent()
        self.play(Create(tangent), run_time=S.HOLD)

        # "here's the direction": the arrow grows along the tangent, uphill.
        self.hold_until(T_DIRECTION)
        arrow = make_arrow(1)
        self.play(GrowArrow(arrow), run_time=S.HOLD)
        self.bring_to_front(dot)

        # "to increase the output": tag it, then nudge the weight uphill and back.
        self.hold_until(T_INCREASE)
        up_tag = label("loss ↑").next_to(arrow.get_center(), RIGHT, buff=0.5)
        self.play(FadeIn(up_tag), run_time=S.BEAT)
        tangent.add_updater(lambda m: m.become(make_tangent()))
        arrow.add_updater(lambda m: m.become(make_arrow(1)))
        dot.add_updater(lambda m: m.move_to(p()))
        up_tag.add_updater(lambda m: m.next_to(arrow.get_center(), RIGHT, buff=0.5))
        self.hold_until(T_NUDGE)
        self.play(w.animate(rate_func=there_and_back).set_value(W_START + NUDGE_DW),
                  run_time=S.HOLD)

        # "opposite direction": the same arrow flips to point downhill.
        self.hold_until(T_OPPOSITE)
        arrow.clear_updaters()
        up_tag.clear_updaters()
        self.play(Transform(arrow, make_arrow(-1)), FadeOut(up_tag), run_time=S.HOLD)
        arrow.add_updater(lambda m: m.become(make_arrow(-1)))

        # "to make the loss go down": the weight slides a short way downhill.
        self.hold_until(T_DOWN)
        self.play(w.animate.set_value(W_END), run_time=S.HOLD)
        for m in (tangent, arrow, dot):
            m.clear_updaters()
        self.hold_until(BEAT_SECONDS)
