"""A neuron has one weight per input plus a bias, and they all start random.

Render:
    cd videos/003-backprop-gifs && uv run manim -qm 01_neuron.py Neuron
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import data_dot

INPUT_X = -4.6
NET_Y = 0.5             # lift the network so the equation below has room
INPUT_YS = [1.8 + NET_Y, NET_Y, -1.8 + NET_Y]
NEURON_POS = np.array([1.6, NET_Y, 0.0])
NEURON_R = 0.95
LABEL_T = 0.42          # where along each line the weight label sits
LABEL_SIDE = [1, 1, -1]  # +1 = label above its line, -1 = below
LABEL_GAP = 0.12
WEIGHT_LABEL_SCALE = 1.15


def label(s: str, color: str) -> Text:
    return Text(s, font=S.FONT, weight="MEDIUM").scale(S.CAPTION_SCALE).set_color(color)


def weight_label(i: int, first: float) -> VGroup:
    name = label(f"w{i + 1} =", S.STRUCTURE)
    num = label(f"{first:+.2f}", S.STRUCTURE)  # updated via .become() while spinning
    return VGroup(name, num).arrange(RIGHT, buff=0.12).scale(WEIGHT_LABEL_SCALE)


class Neuron(BocScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)
        finals = rng.uniform(-1, 1, size=6).round(2)[3:]  # second triple has mixed signs

        neuron = Circle(radius=NEURON_R, color=S.FG, stroke_width=S.STROKE_STRUCTURE)
        neuron.set_fill(S.BG_PANEL, opacity=1).move_to(NEURON_POS)
        out_arrow = Arrow(neuron.get_right(), neuron.get_right() + RIGHT * 2.0, buff=0.1,
                          color=S.FG_DIM, stroke_width=S.STROKE_STRUCTURE)
        y_lbl = label("y", S.FG).next_to(out_arrow, UP, buff=0.15)

        dots, xs, lines, labels = VGroup(), VGroup(), VGroup(), VGroup()
        for i, y in enumerate(INPUT_YS):
            p = np.array([INPUT_X, y, 0.0])
            dots.add(data_dot(p, radius=S.DOT_HERO * 2.5))
            xs.add(label(f"x{i + 1}", S.DATA).next_to(dots[-1], LEFT, buff=0.25))
            end = NEURON_POS + NEURON_R * normalize(p - NEURON_POS)
            line = Line(p, end, color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE)
            line.set_z_index(-1)
            lines.add(line)
            lbl = weight_label(i, rng.uniform(-1, 1))
            # Horizontal text over a sloped line: clearance must cover the rise
            # of the line across half the label's width, plus half its height.
            d = normalize(end - p)
            slope = abs(d[1] / d[0])
            clearance = LABEL_GAP + lbl.height / 2 + lbl.width / 2 * slope
            lbl.move_to(line.point_from_proportion(LABEL_T) + UP * LABEL_SIDE[i] * clearance)
            labels.add(lbl)

        self.play(FadeIn(dots), FadeIn(xs), FadeIn(neuron), GrowArrow(out_arrow),
                  FadeIn(y_lbl), run_time=S.BEAT)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2),
                  FadeIn(labels), run_time=S.BEAT)

        # Weights "spin" through random values, then settle.
        spin = ValueTracker(0)
        for lbl, final in zip(labels, finals):
            def spinner(num, final=final):
                t = spin.get_value()
                v = final if t >= 1 else final + (1 - t) * rng.uniform(-1, 1)
                num.become(label(f"{v:+.2f}", S.STRUCTURE).scale(WEIGHT_LABEL_SCALE)
                           .move_to(num, aligned_edge=LEFT))
            lbl[1].add_updater(spinner)
        cap = self.show_caption("weights start random")
        self.play(spin.animate.set_value(1), run_time=S.HOLD, rate_func=linear)
        for lbl in labels:
            lbl[1].clear_updaters()
        self.play(*[Indicate(l[1], color=S.STRUCTURE) for l in labels], run_time=S.QUICK)
        self.hide_caption(cap)

        # Bias slides in and attaches to the neuron.
        bias = label("+ b", S.CONTENT_GOLD)
        bias.move_to(neuron).shift(DOWN * 3.0)
        cap = self.show_caption("plus a bias")
        self.play(bias.animate.move_to(neuron), run_time=S.BEAT, rate_func=smooth)
        self.beat("QUICK")
        self.hide_caption(cap)

        parts = [("y = ", S.FG), ("w1", S.STRUCTURE), ("x1", S.DATA), (" + ", S.FG),
                 ("w2", S.STRUCTURE), ("x2", S.DATA), (" + ", S.FG),
                 ("w3", S.STRUCTURE), ("x3", S.DATA), (" + ", S.FG), ("b", S.CONTENT_GOLD)]
        eq = VGroup(*[label(t, c) for t, c in parts]).arrange(RIGHT, buff=0.14)
        eq.scale(1.25).to_edge(DOWN, buff=0.6)
        self.play(Write(eq), run_time=S.BEAT)
        self.beat("HOLD")
        self.beat("HOLD")
