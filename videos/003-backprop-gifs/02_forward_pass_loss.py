"""The forward pass turns an input into an output; the gap to the target is the loss.

Render:
    cd videos/003-backprop-gifs && uv run manim -qm 02_forward_pass_loss.py ForwardPassLoss
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import data_dot

LAYERS = [2, 3, 1]
LAYER_X = [-5.0, -3.2, -1.4]
NODE_R = 0.32
NODE_GAP = 1.5
OUTPUT, TARGET = 0.2, 1.0
LOSS = (TARGET - OUTPUT) ** 2
BAR_X = 2.6       # x of the value scale
BAR_Y0 = -1.9     # y where value 0.0 sits
BAR_UNIT = 3.4    # scene units per 1.0 of value
NUM_SCALE = S.CAPTION_SCALE * 1.25


def txt(text: str, color: str, scale: float = NUM_SCALE) -> Text:
    return Text(text, font=S.FONT, weight="MEDIUM").scale(scale).set_color(color)


def node(point) -> Circle:
    return Circle(radius=NODE_R, stroke_color=S.FG_DIM, stroke_width=S.STROKE_AXIS * 2).move_to(point)


def value_y(v: float) -> float:
    return BAR_Y0 + v * BAR_UNIT


class ForwardPassLoss(BocScene):
    def construct(self):
        shift = DOWN * 0.3
        layers = [
            VGroup(*[node(np.array([x, (i - (n - 1) / 2) * NODE_GAP, 0]) + shift) for i in range(n)])
            for n, x in zip(LAYERS, LAYER_X)
        ]
        edges = [
            VGroup(*[
                Line(a.get_right(), b.get_left(), stroke_color=S.MUTED, stroke_width=S.STROKE_AXIS * 1.5)
                for a in left for b in right
            ])
            for left, right in zip(layers[:-1], layers[1:])
        ]
        self.add(*edges, *layers)

        # Sample enters from the left and feeds both inputs.
        x_dot = data_dot(LEFT * 7.4 + shift, radius=S.DOT_HERO * 3)
        x_lbl = txt("x", S.DATA).next_to(x_dot, UP, buff=0.15)
        sample = VGroup(x_dot, x_lbl)
        cap = self.show_caption("forward pass")
        self.play(sample.animate.shift(RIGHT * 1.2), run_time=S.BEAT)
        self.play(
            *[n.animate.set_fill(S.DATA, opacity=S.OP_DATA).set_stroke(S.DATA) for n in layers[0]],
            run_time=S.QUICK,
        )

        # Pulse travels layer by layer.
        for es, nxt in zip(edges, layers[1:]):
            flash = es.copy().set_stroke(S.HIGHLIGHT, width=S.STROKE_STRUCTURE)
            self.play(ShowPassingFlash(flash, time_width=0.6), run_time=S.BEAT)
            self.play(
                *[n.animate.set_fill(S.DATA, opacity=S.OP_DATA).set_stroke(S.DATA) for n in nxt],
                es.animate.set_stroke(S.FG_DIM),
                run_time=S.QUICK,
            )

        # Output value lands on a small value scale; target sits above it.
        out_node = layers[-1][0]
        out_pt = np.array([BAR_X, value_y(OUTPUT), 0])
        tgt_pt = np.array([BAR_X, value_y(TARGET), 0])
        out_dot = data_dot(out_pt, radius=S.DOT_HERO * 2.5)
        tgt_tick = Line(LEFT * 0.3, RIGHT * 0.3, stroke_color=S.FG, stroke_width=S.STROKE_STRUCTURE).move_to(tgt_pt)
        out_lbl = txt(f"output {OUTPUT:.1f}", S.DATA).next_to(out_dot, RIGHT, buff=0.35)
        tgt_lbl = txt(f"target {TARGET:.1f}", S.FG).next_to(tgt_tick, RIGHT, buff=0.35)
        self.play(TransformFromCopy(out_node, out_dot), FadeIn(out_lbl, shift=RIGHT * 0.2), run_time=S.BEAT)
        self.play(Create(tgt_tick), FadeIn(tgt_lbl, shift=RIGHT * 0.2), run_time=S.QUICK)
        self.hide_caption(cap)

        # The gap between them is the loss (the one magenta hero).
        gap = Line(out_pt, tgt_pt, stroke_color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE * 1.6)
        loss_lbl = txt(f"loss = {LOSS:.2f}", S.STRUCTURE).next_to(gap, LEFT, buff=0.4)
        cap = self.show_caption("loss = how wrong we are")
        self.play(Create(gap), FadeIn(loss_lbl, shift=LEFT * 0.2), run_time=S.BEAT)
        self.play(Indicate(loss_lbl, color=S.STRUCTURE), run_time=S.BEAT)
        self.beat("HOLD")
        self.beat("BEAT")
