"""A matrix is determined by where it sends the basis directions.

Viewer takeaway: matrix-vector multiplication rebuilds the same coordinate
recipe using moved basis directions.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql matrix_moves_basis_directions.py MatrixMovesBasisDirections
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import *

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocNumberPlane, hero_arrow, residual


def label(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


class MatrixMovesBasisDirections(BocScene):
    def construct(self):
        plane = BocNumberPlane(
            x_range=[-4, 5, 1],
            y_range=[-3, 5, 1],
            x_length=7.2,
            y_length=5.8,
        )

        def p(x: float, y: float):
            return plane.c2p(x, y)

        e1 = hero_arrow(p(0, 0), p(1, 0), color=S.DATA)
        e2 = hero_arrow(p(0, 0), p(0, 1), color=S.HIGHLIGHT)
        e1_tag = label("e1", S.DATA).next_to(e1, DOWN, buff=0.12)
        e2_tag = label("e2", S.HIGHLIGHT).next_to(e2, LEFT, buff=0.12)

        moved_e1 = hero_arrow(p(0, 0), p(1, 0.5), color=S.DATA)
        moved_e2 = hero_arrow(p(0, 0), p(-0.5, 1.25), color=S.HIGHLIGHT)
        moved_tags = VGroup(
            label("A(e1)", S.DATA).next_to(moved_e1.get_end(), RIGHT, buff=0.12),
            label("A(e2)", S.HIGHLIGHT).next_to(moved_e2.get_end(), LEFT, buff=0.12),
        )

        old_v = hero_arrow(p(0, 0), p(3, 2), color=S.FG_DIM, stroke_width=S.STROKE_AXIS)
        old_steps = VGroup(
            hero_arrow(p(0, 0), p(3, 0), color=S.DATA),
            hero_arrow(p(3, 0), p(3, 2), color=S.HIGHLIGHT),
        )
        old_tag = label("v = 3*e1 + 2*e2", S.FG).next_to(old_v.get_end(), UR, buff=0.1)

        new_step_1 = hero_arrow(p(0, 0), p(3, 1.5), color=S.DATA)
        new_step_2 = hero_arrow(p(3, 1.5), p(2, 4), color=S.HIGHLIGHT)
        new_v = hero_arrow(p(0, 0), p(2, 4), color=S.STRUCTURE)
        new_tag = label("A(v) = 3*A(e1) + 2*A(e2)", S.STRUCTURE).to_edge(DOWN)

        title = label("a matrix moves basis directions", S.FG).to_corner(UL, buff=0.25)
        matrix_note = label("A sends e1 -> (1, 0.5), e2 -> (-0.5, 1.25)", S.FG_DIM).to_corner(DR, buff=0.28)
        guides = VGroup(
            residual(p(3, 0), p(3, 2), color=S.GRID),
            residual(p(0, 2), p(3, 2), color=S.GRID),
            residual(p(3, 1.5), p(2, 4), color=S.GRID),
        )

        self.play(FadeIn(plane), FadeIn(title), run_time=S.BEAT)
        cap = self.show_caption("First, agree on the original directions.")
        self.play(Create(e1), Create(e2), FadeIn(e1_tag), FadeIn(e2_tag), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("A matrix tells us where those directions land.")
        self.play(TransformFromCopy(e1, moved_e1), TransformFromCopy(e2, moved_e2), FadeIn(moved_tags), FadeIn(matrix_note), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap)
        self.play(FadeOut(matrix_note), run_time=S.QUICK)

        cap = self.show_caption("The vector gives a recipe: 3 of the first direction, 2 of the second.")
        self.play(Create(old_steps), Create(old_v), Create(guides[:2]), FadeIn(old_tag), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("After the matrix, rebuild that recipe using the moved directions.")
        self.play(Create(new_step_1), run_time=S.BEAT)
        self.play(Create(new_step_2), run_time=S.BEAT)
        self.play(Create(guides[2]), Create(new_v), FadeIn(new_tag), run_time=S.HOLD)
        self.beat("HOLD")
        self.hide_caption(cap)
