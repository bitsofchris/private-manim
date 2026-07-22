"""Rows land in output space; columns add into output coordinates.

Viewer takeaway: rows of W are moved input directions, and column sums are just
coordinate-by-coordinate vector addition after those rows are weighted by x.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql rows_land_columns_add.py RowsLandColumnsAdd
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene


X = ["2", "-1", "0", "3", "1"]
W = [["1", "0", "2"], ["-1", "3", "0"], ["2", "1", "-1"], ["0", "-2", "1"], ["1", "1", "0"]]
WEIGHTED = [["2", "0", "4"], ["1", "-3", "0"], ["0", "0", "0"], ["0", "-6", "3"], ["1", "1", "0"]]
COL_SUMS = ["4", "-8", "7"]
ROW_COLORS = [S.DATA, S.STRUCTURE, S.CONTENT_GOLD, S.HIGHLIGHT, S.CALLOUT]
COL_COLORS = [S.DATA, S.STRUCTURE, S.CONTENT_GOLD]


def txt(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


def cell(value: str, color: str = S.FG_DIM, width: float = 0.5, height: float = 0.35) -> VGroup:
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
    for i, values in enumerate(rows):
        color = colors[i] if colors else S.FG_DIM
        rendered.add(VGroup(*[cell(v, color=color) for v in values]).arrange(RIGHT, buff=0))
    return rendered.arrange(DOWN, buff=0)


class RowsLandColumnsAdd(BocScene):
    def construct(self):
        title = txt("rows land, columns add", S.FG).to_corner(UL, buff=0.28)
        x = table([X], colors=[S.DATA]).to_edge(LEFT, buff=0.82).shift(UP * 1.45)
        x_label = txt("x: five input amounts", S.DATA, scale=S.TAG_SCALE).next_to(x, UP, buff=0.14)
        w = table(W, ROW_COLORS).move_to(ORIGIN).shift(LEFT * 0.25 + UP * 0.45)
        self.w_label = txt("W rows: landing vectors in 3D", S.STRUCTURE, scale=S.TAG_SCALE).next_to(w, UP, buff=0.14)

        cap = self.show_caption("Start with one 5D input recipe.")
        self.play(FadeIn(title), FadeIn(x_label), FadeIn(x), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("Each W row is a landing vector in the 3D output space.")
        self.play(FadeIn(self.w_label), FadeIn(w), run_time=S.HOLD)
        for i, color in enumerate(ROW_COLORS):
            note = txt(f"input direction {i + 1} lands as this 3D row", color, scale=0.34).to_edge(DOWN, buff=0.32)
            self.play(self.highlight_row(w[i], color), FadeIn(note), run_time=S.BEAT)
            self.beat("QUICK")
            self.play(FadeOut(note), run_time=S.QUICK)
        self.beat("HOLD")
        self.hide_caption(cap)

        self.weight_rows(x, w)

    def weight_rows(self, x: VGroup, w: VGroup) -> None:
        weights = table([[v] for v in X], ROW_COLORS).next_to(x, DOWN, buff=0.62).align_to(x, LEFT)
        weights_label = txt("x[i] weights", S.DATA, scale=S.TAG_SCALE).next_to(weights, UP, buff=0.14)
        weighted = table(WEIGHTED, ROW_COLORS).next_to(w, RIGHT, buff=0.95).align_to(w, UP)
        weighted_label = txt("weighted rows", S.FG_DIM, scale=S.TAG_SCALE).next_to(weighted, UP, buff=0.14)
        times = txt("*", S.STRUCTURE, scale=S.CAPTION_SCALE).move_to((weights.get_right() + w.get_left()) / 2)

        cap = self.show_caption("The input component tells how much of that landing vector to use.")
        self.play(FadeOut(self.w_label), TransformFromCopy(x, weights), FadeIn(weights_label), FadeIn(times), FadeIn(weighted_label), run_time=S.HOLD)
        for i, color in enumerate(ROW_COLORS):
            self.play(
                self.highlight_row(weights[i], color),
                self.highlight_row(w[i], color),
                FadeIn(weighted[i]),
                run_time=S.HOLD,
            )
        self.hide_caption(cap)

        self.add_columns(weighted)

    def add_columns(self, weighted: VGroup) -> None:
        sum_row = table([COL_SUMS], colors=[S.STRUCTURE]).next_to(weighted, DOWN, buff=0.42)
        sum_label = txt("output vector y", S.STRUCTURE, scale=S.TAG_SCALE).next_to(sum_row, LEFT, buff=0.16)
        equations = [
            "2 + 1 + 0 + 0 + 1 = 4",
            "0 + -3 + 0 + -6 + 1 = -8",
            "4 + 0 + 0 + 3 + 0 = 7",
        ]

        cap = self.show_caption("Now add the 3D landing vectors like normal vectors.")
        for j, color in enumerate(COL_COLORS):
            guide = Rectangle(
                width=0.5,
                height=1.75,
                stroke_color=color,
                stroke_width=S.STROKE_STRUCTURE,
            ).move_to(weighted.get_center() + RIGHT * (j - 1) * 0.5)
            eq = txt(equations[j], color, scale=0.34).to_edge(DOWN, buff=0.32)
            self.play(Create(guide), FadeIn(eq), run_time=S.HOLD)
            self.play(FadeIn(sum_row[0][j]), run_time=S.BEAT)
            self.play(FadeOut(eq), FadeOut(guide), run_time=S.QUICK)
        self.play(FadeIn(sum_label), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        closing = VGroup(
            txt("Rows: moved input directions.", S.DATA, scale=S.TAG_SCALE),
            txt("Columns: output-coordinate totals.", S.STRUCTURE, scale=S.TAG_SCALE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(closing), run_time=S.HOLD)
        self.beat("HOLD")

    def highlight_row(self, row: VGroup, color: str) -> AnimationGroup:
        anims = []
        for item in row:
            anims.append(item[0].animate.set_stroke(color=color, width=S.STROKE_STRUCTURE))
            anims.append(item[1].animate.set_color(color))
        return AnimationGroup(*anims)
