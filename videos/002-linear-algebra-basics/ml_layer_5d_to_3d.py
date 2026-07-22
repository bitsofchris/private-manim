"""A PyTorch row-vector layer maps a batch of 5D inputs into 3D outputs.

Viewer takeaway: in ML row-vector convention, each row of W is where one input
basis direction lands; an input row weights W's rows, then columns sum into Y.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql ml_layer_5d_to_3d.py MLLayer5DTo3D
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene


X_ROWS = [["1", "0", "-2", "3", "1"], ["0", "2", "1", "-1", "2"], ["3", "-1", "0", "2", "-2"]]
W_ROWS = [["1", "0", "2"], ["-1", "3", "0"], ["2", "1", "-1"], ["0", "-2", "1"], ["1", "1", "0"]]
WEIGHTED = [["1", "0", "2"], ["0", "0", "0"], ["-4", "-2", "2"], ["0", "-6", "3"], ["1", "1", "0"]]
Y_ROWS = [["-2", "-7", "7"], ["2", "11", "-2"], ["2", "-9", "8"]]
ROW_COLORS = [S.DATA, S.STRUCTURE, S.CONTENT_GOLD, S.HIGHLIGHT, S.CALLOUT]


def txt(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


def cell(value: str, color: str = S.FG_DIM, width: float = 0.48, height: float = 0.34) -> VGroup:
    box = Rectangle(
        width=width,
        height=height,
        stroke_color=S.MUTED,
        stroke_width=S.STROKE_AXIS,
        fill_color=S.BG_PANEL,
        fill_opacity=S.OP_GHOST,
    )
    return VGroup(box, txt(value, color, scale=0.32).move_to(box))


def table(rows: list[list[str]], colors: list[str] | None = None) -> VGroup:
    rendered = VGroup()
    for i, row_values in enumerate(rows):
        color = colors[i] if colors else S.FG_DIM
        rendered.add(VGroup(*[cell(v, color=color) for v in row_values]).arrange(RIGHT, buff=0))
    return rendered.arrange(DOWN, buff=0)


class MLLayer5DTo3D(BocScene):
    def construct(self):
        title = txt("ML convention: X @ W", S.FG).to_corner(UL, buff=0.28)
        x = table(X_ROWS).to_edge(LEFT, buff=0.45).shift(UP * 0.2)
        w = table(W_ROWS).move_to(ORIGIN).shift(UP * 0.2)
        y = table(Y_ROWS).to_edge(RIGHT, buff=0.45).shift(UP * 0.2)
        x_label = txt("X shape (3, 5)", S.DATA, scale=S.TAG_SCALE).next_to(x, UP, buff=0.14)
        w_label = txt("W shape (5, 3)", S.STRUCTURE, scale=S.TAG_SCALE).next_to(w, UP, buff=0.14)
        y_label = txt("Y shape (3, 3)", S.STRUCTURE, scale=S.TAG_SCALE).next_to(y, UP, buff=0.14)
        op = txt("@", S.STRUCTURE, scale=S.CAPTION_SCALE).move_to((x.get_right() + w.get_left()) / 2)
        arrow = Arrow(w.get_right() + RIGHT * 0.1, y.get_left() + LEFT * 0.1, color=S.STRUCTURE, buff=0)

        cap = self.show_caption("Three 5D input rows project into three 3D output rows.")
        self.play(FadeIn(title), FadeIn(x_label), FadeIn(x), FadeIn(op), FadeIn(w_label), FadeIn(w), run_time=S.HOLD)
        self.play(Create(arrow), FadeIn(y_label), FadeIn(y), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        self.play(FadeOut(op), FadeOut(arrow), FadeOut(title), FadeOut(x), FadeOut(y), FadeOut(x_label), FadeOut(y_label), run_time=S.BEAT)
        self.explain_rows(w, w_label)

    def explain_rows(self, w: VGroup, w_label: Text) -> None:
        row_notes = VGroup(
            *[txt(f"W row {i + 1}: image of input basis direction {i + 1}", ROW_COLORS[i], scale=0.34) for i in range(5)]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(w, RIGHT, buff=0.45)

        cap = self.show_caption("Each row of W says where one input direction lands.")
        self.play(w.animate.to_edge(LEFT, buff=0.72).shift(UP * 0.45), w_label.animate.next_to(w, UP, buff=0.14), run_time=S.BEAT)
        self.play(FadeIn(row_notes), run_time=S.BEAT)
        for i, color in enumerate(ROW_COLORS):
            self.play(self.highlight(w[i], color), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        self.play(FadeOut(row_notes), FadeOut(w_label), w.animate.move_to(ORIGIN).shift(UP * 0.2), run_time=S.BEAT)
        self.one_row_walkthrough(w, w_label)

    def one_row_walkthrough(self, w: VGroup, w_label: Text) -> None:
        x0 = table([X_ROWS[0]], colors=[S.DATA]).to_edge(LEFT, buff=0.72).shift(UP * 1.72)
        x0_label = txt("first input row", S.DATA, scale=S.TAG_SCALE).next_to(x0, UP, buff=0.14)
        weights = table([[v] for v in X_ROWS[0]], colors=ROW_COLORS).next_to(x0, DOWN, buff=0.62).align_to(x0, LEFT)
        weights_label = txt("x[0] weights", S.DATA, scale=S.TAG_SCALE).next_to(weights, UP, buff=0.14)
        times = txt("*", S.STRUCTURE, scale=S.CAPTION_SCALE).move_to((weights.get_right() + w.get_left()) / 2)
        weighted = table(WEIGHTED, ROW_COLORS).next_to(w, RIGHT, buff=0.45).align_to(w, UP)
        weighted_label = txt("weighted W rows", S.FG_DIM, scale=S.TAG_SCALE).next_to(weighted, UP, buff=0.14)
        sum_row = table([Y_ROWS[0]], colors=[S.STRUCTURE]).next_to(weighted, DOWN, buff=0.34)
        sum_label = txt("sum down columns", S.STRUCTURE, scale=S.TAG_SCALE).next_to(sum_row, LEFT, buff=0.16)
        y0 = table([Y_ROWS[0]], colors=[S.STRUCTURE]).to_edge(RIGHT, buff=0.45).shift(DOWN * 1.45)
        y0_label = txt("Y[0]", S.STRUCTURE, scale=S.TAG_SCALE).next_to(y0, UP, buff=0.14)

        cap = self.show_caption("One input row supplies five weights.")
        self.play(FadeIn(x0_label), FadeIn(x0), TransformFromCopy(x0, weights), FadeIn(weights_label), FadeIn(times), run_time=S.HOLD)
        self.hide_caption(cap)

        cap = self.show_caption("Weight the matching row of W.")
        self.play(FadeIn(weighted_label), run_time=S.BEAT)
        for i, color in enumerate(ROW_COLORS):
            self.play(self.highlight(weights[i], color), self.highlight(w[i], color), FadeIn(weighted[i]), run_time=S.BEAT)
        self.hide_caption(cap)

        cap = self.show_caption("Then sum down each output column.")
        column_guides = VGroup()
        for j in range(3):
            column_guides.add(Rectangle(width=0.48, height=1.7, stroke_color=S.STRUCTURE, stroke_width=S.STROKE_AXIS).move_to(weighted.get_center() + RIGHT * (j - 1) * 0.48))
        self.play(LaggedStart(*[Create(g) for g in column_guides], lag_ratio=0.18), FadeIn(sum_label), FadeIn(sum_row), run_time=S.HOLD)
        self.play(TransformFromCopy(sum_row, y0), FadeIn(y0_label), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        closing = txt("x[0] weights W rows -> column sums become Y[0]", S.STRUCTURE, scale=S.TAG_SCALE).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(closing), run_time=S.BEAT)
        self.beat("HOLD")

    def highlight(self, row: VGroup, color: str) -> AnimationGroup:
        anims = []
        for item in row:
            anims.append(item[0].animate.set_stroke(color=color, width=S.STROKE_STRUCTURE))
            anims.append(item[1].animate.set_color(color))
        return AnimationGroup(*anims)
