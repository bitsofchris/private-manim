"""A matrix stores the output-space directions used by a linear map.

Viewer takeaway: in the row-vector PyTorch view, each row of W is where one
input direction lands; multiplication applies that stored map.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql matrix_as_stored_map.py MatrixAsStoredMap
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocNumberPlane, hero_arrow


X_ROW = ["1.0", "2.0", "-1.0"]
W_ROWS = [["2.0", "-1.0"], ["0.5", "1.0"], ["-1.0", "2.0"]]
WEIGHTED_ROWS = [["2.0", "-1.0"], ["1.0", "2.0"], ["1.0", "-2.0"]]
RAW_SUM = ["4.0", "-1.0"]
ROW_COLORS = [S.DATA, S.STRUCTURE, S.CONTENT_GOLD]


def txt(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


def cell(value: str, color: str = S.FG_DIM, width: float = 0.66, height: float = 0.38) -> VGroup:
    box = Rectangle(
        width=width,
        height=height,
        stroke_color=S.MUTED,
        stroke_width=S.STROKE_AXIS,
        fill_color=S.BG_PANEL,
        fill_opacity=S.OP_GHOST,
    )
    return VGroup(box, txt(value, color, scale=S.TAG_SCALE).move_to(box))


def table(rows: list[list[str]], colors: list[str] | None = None) -> VGroup:
    rendered = VGroup()
    for i, values in enumerate(rows):
        color = colors[i] if colors else S.FG_DIM
        rendered.add(VGroup(*[cell(v, color=color) for v in values]).arrange(RIGHT, buff=0))
    return rendered.arrange(DOWN, buff=0)


class MatrixAsStoredMap(BocScene):
    def construct(self):
        w = table(W_ROWS).move_to(ORIGIN).shift(LEFT * 3.0 + UP * 0.25)
        w_name = txt("W shape (3, 2)", S.FG_DIM, scale=S.TAG_SCALE).next_to(w, UP, buff=0.16)
        title = txt("the matrix is the stored map", S.FG_DIM, scale=S.TAG_SCALE).to_corner(UL, buff=0.25)
        w_label = txt("W stores where input directions land", S.FG, scale=S.TAG_SCALE).next_to(w_name, UP, buff=0.32)
        row_notes = VGroup(
            txt("row 1 -> input direction 1 lands here", ROW_COLORS[0], scale=S.TAG_SCALE),
            txt("row 2 -> input direction 2 lands here", ROW_COLORS[1], scale=S.TAG_SCALE),
            txt("row 3 -> input direction 3 lands here", ROW_COLORS[2], scale=S.TAG_SCALE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(w, DOWN, buff=0.28)

        plane = BocNumberPlane(
            x_range=[-2, 4, 1],
            y_range=[-3, 3, 1],
            x_length=4.2,
            y_length=3.8,
        ).to_edge(RIGHT, buff=0.65).shift(UP * 0.05)

        def p(x: float, y: float):
            return plane.c2p(x, y)

        arrows = VGroup(
            hero_arrow(p(0, 0), p(2, -1), color=ROW_COLORS[0]),
            hero_arrow(p(0, 0), p(0.5, 1), color=ROW_COLORS[1]),
            hero_arrow(p(0, 0), p(-1, 2), color=ROW_COLORS[2]),
        )
        arrow_tags = VGroup(
            txt("w1", ROW_COLORS[0]).next_to(arrows[0].get_end(), RIGHT, buff=0.08),
            txt("w2", ROW_COLORS[1]).next_to(arrows[1].get_end(), RIGHT, buff=0.08),
            txt("w3", ROW_COLORS[2]).next_to(arrows[2].get_end(), LEFT, buff=0.08),
        )

        x = VGroup(txt("x", S.DATA), table([X_ROW], colors=[S.DATA])).arrange(DOWN, buff=0.12).to_corner(DL, buff=0.45)
        weighted = table(WEIGHTED_ROWS, ROW_COLORS).next_to(x, RIGHT, buff=0.55)
        weighted_label = txt("weighted W rows", S.FG_DIM, scale=S.TAG_SCALE).next_to(weighted, UP, buff=0.14)
        sum_row = table([RAW_SUM], colors=[S.STRUCTURE]).next_to(weighted, RIGHT, buff=0.65)
        sum_label = txt("sum", S.STRUCTURE).next_to(sum_row, UP, buff=0.14)
        result_arrow = Arrow(weighted.get_right() + RIGHT * 0.1, sum_row.get_left() + LEFT * 0.1, color=S.STRUCTURE, buff=0)

        self.play(FadeIn(title), FadeIn(w_label), FadeIn(w_name), FadeIn(w), run_time=S.HOLD)
        cap = self.show_caption("A matrix stores landing directions.")
        self.play(FadeIn(row_notes), run_time=S.BEAT)
        for i, color in enumerate(ROW_COLORS):
            self.play(self.highlight_row(w[i], color), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("Rows become arrows in output space.")
        self.play(FadeIn(plane), run_time=S.BEAT)
        for i in range(3):
            self.play(TransformFromCopy(w[i], arrows[i]), FadeIn(arrow_tags[i]), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("x supplies the weights.")
        self.play(FadeOut(row_notes), FadeIn(x), run_time=S.BEAT)
        for i, color in enumerate(ROW_COLORS):
            self.play(self.highlight_row(VGroup(x[1][0][i]), color), FadeIn(weighted[i]), run_time=S.BEAT)
        self.play(FadeIn(weighted_label), Create(result_arrow), FadeIn(sum_label), FadeIn(sum_row), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap)

        closing = txt("stored map -> applied map -> output vector", S.STRUCTURE, scale=S.TAG_SCALE).to_corner(DR, buff=0.35)
        self.play(FadeIn(closing), run_time=S.BEAT)
        self.beat("HOLD")

    def highlight_row(self, row: VGroup, color: str) -> AnimationGroup:
        anims = []
        for item in row:
            anims.append(item[0].animate.set_stroke(color=color, width=S.STROKE_STRUCTURE))
            anims.append(item[1].animate.set_color(color))
        return AnimationGroup(*anims)
