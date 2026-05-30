"""One row of X weights every row of W, then the weighted rows sum into Y.

Viewer takeaway: a single row-vector times W is a weighted sum of W's rows.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql one_row_weighted_sum.py OneRowWeightedSum
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene


X_ROW = ["1.0", "2.0", "-1.0"]
W_ROWS = [["2.0", "-1.0"], ["0.5", "1.0"], ["-1.0", "2.0"]]
WEIGHTED_ROWS = [["2.0", "-1.0"], ["1.0", "2.0"], ["1.0", "-2.0"]]
RAW_SUM = ["4.0", "-1.0"]
BIAS = ["0.1", "-0.2"]
Y_ROW = ["4.1", "-1.2"]
ROW_COLORS = [S.DATA, S.STRUCTURE, S.CONTENT_GOLD]


def txt(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


def cell(value: str, width: float = 0.72, height: float = 0.44, color: str = S.FG_DIM) -> VGroup:
    box = Rectangle(
        width=width,
        height=height,
        stroke_color=S.MUTED,
        stroke_width=S.STROKE_AXIS,
        fill_color=S.BG_PANEL,
        fill_opacity=S.OP_GHOST,
    )
    return VGroup(box, txt(value, color, scale=S.TAG_SCALE).move_to(box))


def row(values: list[str], color: str = S.FG_DIM) -> VGroup:
    return VGroup(*[cell(v, color=color) for v in values]).arrange(RIGHT, buff=0)


def col(values: list[str]) -> VGroup:
    return VGroup(*[cell(v) for v in values]).arrange(DOWN, buff=0)


class OneRowWeightedSum(BocScene):
    def construct(self):
        title = txt("X[0] @ W + b -> Y[0]", S.FG).to_corner(DL, buff=0.28)
        x_row = row(X_ROW).to_edge(LEFT, buff=0.65).shift(UP * 1.55)
        x_label = txt("first row of X", S.DATA).next_to(x_row, UP, buff=0.14)
        weights = col(X_ROW).next_to(x_row, DOWN, buff=0.78).align_to(x_row, LEFT)

        w_matrix = VGroup(*[row(r) for r in W_ROWS]).arrange(DOWN, buff=0).move_to(ORIGIN).shift(LEFT * 0.2)
        w_label = txt("W rows", S.FG).next_to(w_matrix, UP, buff=0.14)
        weight_matrix = VGroup(weights, w_matrix).arrange(RIGHT, buff=0.42).shift(DOWN * 0.1)
        weights_label = txt("weights", S.DATA, scale=S.TAG_SCALE).next_to(weights, LEFT, buff=0.16)
        times = txt("*", S.STRUCTURE, scale=S.CAPTION_SCALE).move_to((weights.get_right() + w_matrix.get_left()) / 2)

        weighted = VGroup(*[row(r, color=ROW_COLORS[i]) for i, r in enumerate(WEIGHTED_ROWS)]).arrange(DOWN, buff=0)
        weighted.next_to(w_matrix, RIGHT, buff=0.65).align_to(w_matrix, UP)
        weighted_label = txt("weighted rows", S.FG).next_to(weighted, UP, buff=0.14)
        sum_row = row(RAW_SUM, color=S.STRUCTURE).next_to(weighted, DOWN, buff=0.32)
        sum_label = txt("sum", S.STRUCTURE).next_to(sum_row, LEFT, buff=0.18)
        bias_row = row(BIAS, color=S.CONTENT_GOLD).next_to(sum_row, DOWN, buff=0.28)
        bias_label = txt("+ b", S.CONTENT_GOLD).next_to(bias_row, LEFT, buff=0.18)
        y_row = row(Y_ROW, color=S.STRUCTURE).to_edge(RIGHT, buff=0.55).shift(UP * 0.2)
        y_label = txt("Y row 1", S.STRUCTURE).next_to(y_row, UP, buff=0.14)

        cap = self.show_caption("Start with one input row.")
        self.play(FadeIn(title), FadeIn(x_label), FadeIn(x_row), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("Turn that row sideways: these are the weights.")
        self.play(TransformFromCopy(x_row, weights), FadeIn(weights_label), run_time=S.HOLD)
        self.play(FadeIn(w_label), FadeIn(w_matrix), FadeIn(times), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("Each weight scales the matching row of W.")
        self.play(FadeIn(weighted_label), run_time=S.BEAT)
        for i, color in enumerate(ROW_COLORS):
            self.play(
                self.highlight(weights[i], color),
                self.highlight(w_matrix[i], color),
                FadeIn(weighted[i]),
                run_time=S.HOLD,
            )
            self.beat("QUICK")
        self.hide_caption(cap)

        cap = self.show_caption("Then add the weighted rows column by column.")
        self.play(FadeIn(sum_label), FadeIn(sum_row), run_time=S.BEAT)
        self.beat("HOLD")
        self.play(FadeIn(bias_label), FadeIn(bias_row), run_time=S.BEAT)
        self.hide_caption(cap)

        cap = self.show_caption("Add the broadcast bias, then place the result into Y.")
        final_arrow = Arrow(sum_row.get_right() + RIGHT * 0.15, y_row.get_left() + LEFT * 0.15, color=S.STRUCTURE, buff=0)
        self.play(FadeIn(y_label), Create(final_arrow), TransformFromCopy(sum_row, y_row), run_time=S.HOLD)
        self.play(Indicate(bias_row, color=S.CONTENT_GOLD), Indicate(y_row, color=S.STRUCTURE), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

    def highlight(self, mob: Mobject, color: str) -> AnimationGroup:
        anims = []
        for submob in mob:
            if isinstance(submob, VGroup) and len(submob) >= 2:
                anims.append(submob[0].animate.set_stroke(color=color, width=S.STROKE_STRUCTURE))
                anims.append(submob[1].animate.set_color(color))
        return AnimationGroup(*anims)
