"""Beat 7 (6.26 s, last frame of the Short): step downhill by lr * slope, repeat, settle.

VO: "We use the learning rate to take a tiny step in that direction and we
repeat this over and over and hopefully by the end we train a good model."
Same bowl as beat 4. The magenta hero is the step arrow (one at a time).
Every position is a real update w -= LR * grad(w). The final frame loops
back to the hook, so it ends clean and still.

Render:
    cd videos/004-backprop-short && uv run --no-sync manim -qh 07_descent.py Descent
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
from _bowl import build_bowl, descent_path, label, loss, point

BEAT_SECONDS = 6.28
T_LR = 0.3            # "the learning rate"
T_STEP = 1.2          # "take a tiny step"
T_REPEAT = 2.65       # "and we repeat this over and over"
T_SETTLE = 4.25       # "and hopefully by the end"
T_GOOD = 5.1          # "we train a good model"
W_START = 0.6
LR = 0.35
N_REPEAT = 4          # quick steps after the first
N_SETTLE = 8          # further real steps folded into the final glide
REPEAT_STEP = 0.36    # seconds per quick step: 4 fit "repeat this over and over"
ARROW_WIDTH = S.STROKE_STRUCTURE * 3.5
ARROW_TIP = 0.45


class Descent(BocShortScene):
    def construct(self):
        axes, curve, labels = build_bowl(self.stage)
        ws = descent_path(W_START, LR, 1 + N_REPEAT + N_SETTLE)
        w = ValueTracker(W_START)
        dot = data_dot(point(axes, W_START), radius=S.DOT_SHORT).set_opacity(1)
        dot.add_updater(lambda m: m.move_to(point(axes, w.get_value())))
        # Beside the first step it scales, in the open middle of the bowl.
        lr_tag = label(f"lr = {LR}").next_to(axes.c2p(ws[1], loss(ws[0])), RIGHT, buff=0.5)
        self.add(axes, curve, labels, dot)  # frame 0: beat 4's world, dot high on the slope

        # "the learning rate": the step-size knob appears by the axis.
        self.hold_until(T_LR)
        self.play(FadeIn(lr_tag), run_time=S.BEAT)

        def step_arrow(w0: float, w1: float) -> Arrow:
            # Along w, at the dot's height: the step is a change in the weight.
            return hero_arrow(axes.c2p(w0, loss(w0)), axes.c2p(w1, loss(w0)),
                              stroke_width=ARROW_WIDTH, tip_length=ARROW_TIP,
                              max_tip_length_to_length_ratio=0.5,
                              max_stroke_width_to_length_ratio=ARROW_WIDTH)

        def ghost(w0: float) -> Dot:
            return data_dot(point(axes, w0), radius=S.DOT_SHORT).set_opacity(S.OP_GHOST)

        # "take a tiny step": show the step, then the dot takes it, leaving a ghost.
        self.hold_until(T_STEP)
        arrow = step_arrow(ws[0], ws[1])
        self.play(GrowArrow(arrow), run_time=S.BEAT)
        self.add(ghost(ws[0]))
        self.bring_to_front(dot)
        self.play(w.animate.set_value(ws[1]), run_time=S.BEAT)

        # "repeat this over and over": four more real updates, each smaller.
        self.hold_until(T_REPEAT)
        for w0, w1 in zip(ws[1:1 + N_REPEAT], ws[2:2 + N_REPEAT]):
            nxt = step_arrow(w0, w1)
            self.add(ghost(w0))
            self.bring_to_front(dot)
            self.play(FadeOut(arrow), GrowArrow(nxt), w.animate.set_value(w1),
                      run_time=REPEAT_STEP)
            arrow = nxt

        # "by the end": the remaining updates carry the dot to the bottom.
        self.hold_until(T_SETTLE)
        self.play(FadeOut(arrow), w.animate.set_value(ws[-1]), run_time=S.BEAT)

        # "a good model": one pulse at the minimum, then still.
        self.hold_until(T_GOOD)
        dot.clear_updaters()
        self.play(Indicate(dot, color=S.HIGHLIGHT, scale_factor=1.5), run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
