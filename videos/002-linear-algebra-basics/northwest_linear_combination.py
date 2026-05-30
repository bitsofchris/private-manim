"""Northwest is a linear combination of familiar directions.

Viewer takeaway: a vector is a move; coordinates are the recipe for that move
in a chosen basis.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql northwest_linear_combination.py NorthwestLinearCombination
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


class NorthwestLinearCombination(BocScene):
    def construct(self):
        plane = BocNumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 4, 1],
            x_length=7.2,
            y_length=5.4,
        )

        def p(x: float, y: float):
            return plane.c2p(x, y)

        east = hero_arrow(p(0, 0), p(1, 0), color=S.FG_DIM, stroke_width=S.STROKE_AXIS)
        north = hero_arrow(p(0, 0), p(0, 1), color=S.FG_DIM, stroke_width=S.STROKE_AXIS)
        west_step = hero_arrow(p(0, 0), p(-2, 0), color=S.DATA)
        north_step = hero_arrow(p(-2, 0), p(-2, 2), color=S.HIGHLIGHT)
        northwest = hero_arrow(p(0, 0), p(-2, 2), color=S.STRUCTURE)
        guide_x = residual(p(-2, 0), p(-2, 2), color=S.GRID)
        guide_y = residual(p(0, 2), p(-2, 2), color=S.GRID)

        title = label("northwest = some west + some north", S.FG).to_corner(UL, buff=0.25)
        formula = label("(-2, 2) = -2 * east + 2 * north", S.FG).to_edge(DOWN)
        west_tag = label("2 west", S.DATA).next_to(west_step, DOWN, buff=0.15)
        north_tag = label("2 north", S.HIGHLIGHT).next_to(north_step, LEFT, buff=0.12)
        vector_tag = label("northwest move", S.STRUCTURE).next_to(northwest.get_end(), UR, buff=0.12)
        basis_tags = VGroup(
            label("east", S.FG_DIM).next_to(east, DOWN, buff=0.12),
            label("north", S.FG_DIM).next_to(north, LEFT, buff=0.12),
        )

        self.play(FadeIn(plane), run_time=S.BEAT)
        cap = self.show_caption("Start with two agreed directions.")
        self.play(Create(east), Create(north), FadeIn(basis_tags), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)

        cap = self.show_caption("Northwest is not magic. It is a recipe.")
        self.play(FadeIn(title), run_time=S.BEAT)
        self.play(Create(west_step), FadeIn(west_tag), run_time=S.BEAT)
        self.play(Create(north_step), FadeIn(north_tag), run_time=S.BEAT)
        self.beat("BEAT")
        self.hide_caption(cap)

        cap = self.show_caption("The vector is the move. Coordinates are the recipe.")
        self.play(Create(guide_x), Create(guide_y), Create(northwest), FadeIn(vector_tag), run_time=S.HOLD)
        self.play(FadeIn(formula), run_time=S.BEAT)
        self.beat("HOLD")
        self.hide_caption(cap)
