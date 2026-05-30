"""PyTorch nn.Linear stores one weight row per output neuron.

Viewer takeaway: nn.Linear keeps weights as (out_features, in_features), then
uses weight.T during the forward pass so X becomes Y.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql nn_linear_weight_structure.py NNLinearWeightStructure
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene


X_ROWS = [
    ["1.0", "2.0", "-1.0"],
    ["0.0", "-1.0", "3.0"],
    ["2.0", "0.5", "1.0"],
    ["-1.0", "1.0", "2.0"],
    ["3.0", "-2.0", "0.0"],
]
LINEAR_WEIGHT = [["2.0", "0.5", "-1.0"], ["-1.0", "1.0", "2.0"]]
WEIGHT_T = [["2.0", "-1.0"], ["0.5", "1.0"], ["-1.0", "2.0"]]
BIAS = [["0.1", "-0.2"]]
Y_ROWS = [["4.1", "-1.2"], ["-3.4", "4.8"], ["3.35", "0.3"], ["-3.4", "5.8"], ["5.1", "-5.2"]]
NEURON_COLORS = [S.STRUCTURE, S.CONTENT_GOLD]


def txt(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


def cell(value: str, width: float = 0.64, height: float = 0.4, color: str = S.FG_DIM) -> VGroup:
    box = Rectangle(
        width=width,
        height=height,
        stroke_color=S.MUTED,
        stroke_width=S.STROKE_AXIS,
        fill_color=S.BG_PANEL,
        fill_opacity=S.OP_GHOST,
    )
    return VGroup(box, txt(value, color, scale=S.TAG_SCALE).move_to(box))


def table(name: str, shape: str, rows: list[list[str]], color: str = S.FG) -> VGroup:
    body = VGroup()
    for r, values in enumerate(rows):
        rendered = VGroup(*[cell(v) for v in values]).arrange(RIGHT, buff=0)
        rendered.shift(DOWN * r * 0.4)
        body.add(rendered)
    header = VGroup(txt(name, color), txt(shape, S.FG_DIM, scale=S.TAG_SCALE)).arrange(DOWN, buff=0.06)
    return VGroup(header, body).arrange(DOWN, buff=0.2)


def color_row(row_mob: VGroup, color: str) -> AnimationGroup:
    anims = []
    for item in row_mob:
        anims.append(item[0].animate.set_stroke(color=color, width=S.STROKE_STRUCTURE))
        anims.append(item[1].animate.set_color(color))
    return AnimationGroup(*anims)


class NNLinearWeightStructure(BocScene):
    def construct(self):
        title = txt("nn.Linear(3, 2)", S.FG).to_corner(UL, buff=0.28)
        x = table("X input", "shape (5, 3)", X_ROWS, S.DATA).to_edge(LEFT, buff=0.45).shift(UP * 0.1)
        weight = table("linear.weight", "shape (2, 3)", LINEAR_WEIGHT, S.STRUCTURE).move_to(ORIGIN).shift(UP * 0.25)
        bias = table("linear.bias", "shape (2,)", BIAS, S.CONTENT_GOLD).next_to(weight, DOWN, buff=0.46)
        y = table("Y output", "shape (5, 2)", Y_ROWS, S.STRUCTURE).to_edge(RIGHT, buff=0.45).shift(UP * 0.1)
        formula = txt("Y = X @ linear.weight.T + linear.bias", S.FG).to_edge(DOWN, buff=0.28)

        cap = self.show_caption("PyTorch stores one weight row per output feature.")
        self.play(FadeIn(title), FadeIn(x), FadeIn(weight), FadeIn(bias), run_time=S.HOLD)
        self.play(color_row(weight[1][0], NEURON_COLORS[0]), color_row(weight[1][1], NEURON_COLORS[1]), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("Forward uses a transposed view of that stored weight.")
        weight_t = table("linear.weight.T", "shape (3, 2)", WEIGHT_T, S.STRUCTURE).next_to(weight, RIGHT, buff=0.65)
        arrow = Arrow(weight.get_right() + RIGHT * 0.1, weight_t.get_left() + LEFT * 0.1, color=S.STRUCTURE, buff=0)
        self.play(Create(arrow), TransformFromCopy(weight, weight_t), FadeIn(formula), run_time=S.HOLD)
        self.play(FadeIn(y), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        self.play(
            FadeOut(weight_t),
            FadeOut(arrow),
            FadeOut(formula),
            FadeOut(x),
            FadeOut(weight),
            FadeOut(bias),
            FadeOut(y),
            FadeOut(title),
            run_time=S.BEAT,
        )
        self.neuron_view()

    def neuron_view(self) -> None:
        x0 = VGroup(
            txt("input x = X[0]", S.DATA),
            VGroup(*[cell(v) for v in X_ROWS[0]]).arrange(RIGHT, buff=0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(LEFT, buff=0.6)
        n1 = self.neuron("neuron 1", LINEAR_WEIGHT[0], "dot = 4.0", "+ 0.1", "4.1", NEURON_COLORS[0])
        n2 = self.neuron("neuron 2", LINEAR_WEIGHT[1], "dot = -1.0", "+ -0.2", "-1.2", NEURON_COLORS[1])
        neurons = VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(ORIGIN).shift(RIGHT * 0.2)
        y0_cells = VGroup(
            cell(Y_ROWS[0][0], color=NEURON_COLORS[0]),
            cell(Y_ROWS[0][1], color=NEURON_COLORS[1]),
        ).arrange(RIGHT, buff=0)
        y0 = VGroup(txt("Y[0]", S.STRUCTURE), y0_cells).arrange(DOWN, buff=0.14).move_to(RIGHT * 5.45 + DOWN * 0.05)

        cap = self.show_caption("Think of each stored weight row as one neuron.")
        self.play(FadeIn(x0), run_time=S.BEAT)
        for neuron, color in [(n1, NEURON_COLORS[0]), (n2, NEURON_COLORS[1])]:
            lines = self.connections(x0[1], neuron[1], color)
            self.play(FadeIn(neuron), LaggedStart(*[Create(line) for line in lines], lag_ratio=0.12), run_time=S.HOLD)
            self.beat("QUICK")
        self.hide_caption(cap)

        cap = self.show_caption("Each neuron output fills one slot in Y[0].")
        output_arrows = VGroup(
            Arrow(n1[2][2].get_right() + RIGHT * 0.08, y0_cells[0].get_left() + LEFT * 0.08, color=NEURON_COLORS[0], buff=0),
            Arrow(n2[2][2].get_right() + RIGHT * 0.08, y0_cells[1].get_left() + LEFT * 0.08, color=NEURON_COLORS[1], buff=0),
        )
        self.play(FadeIn(y0[0]), run_time=S.BEAT)
        self.play(Create(output_arrows[0]), FadeIn(y0_cells[0]), run_time=S.BEAT)
        self.play(Create(output_arrows[1]), FadeIn(y0_cells[1]), run_time=S.BEAT)
        self.play(Indicate(y0, color=S.STRUCTURE), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

    def neuron(self, name: str, weights: list[str], dot: str, bias: str, out: str, color: str) -> VGroup:
        name_mob = txt(name, color)
        weight_row = VGroup(*[cell(v, color=color) for v in weights]).arrange(RIGHT, buff=0)
        parts = VGroup(txt(dot, S.FG_DIM, scale=S.TAG_SCALE), txt(bias, S.CONTENT_GOLD, scale=S.TAG_SCALE), txt(out, color)).arrange(RIGHT, buff=0.18)
        return VGroup(name_mob, weight_row, parts).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

    def connections(self, inputs: VGroup, weights: VGroup, color: str) -> VGroup:
        lines = VGroup()
        for i in range(3):
            lines.add(Line(inputs[i].get_right(), weights[i].get_left(), color=color, stroke_width=S.STROKE_RESIDUAL))
        return lines
