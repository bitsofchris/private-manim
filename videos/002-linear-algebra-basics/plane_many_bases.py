"""A fixed plane can have many different bases.

Viewer takeaway: the subspace is fixed, but the coordinate axes inside it are
a choice. The same point gets different coordinates in different bases.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql plane_many_bases.py PlaneManyBases
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import *

from videos._shared import style as S
from videos._shared.base import Boc3DScene
from videos._shared.mobjects import BocThreeDAxes, data_dot_3d, hero_arrow_3d, residual


A1 = np.array([1, -1, 0])
A2 = np.array([1, 0, -1])
B1 = np.array([2, -3, 1])
B2 = np.array([1, 5, -6])
TARGET = B1


def vlabel(text: str, color: str = S.FG) -> Text:
    return Text(text, font=S.FONT).scale(S.LABEL_SCALE).set_color(color)


class PlaneManyBases(Boc3DScene):
    def construct(self):
        axes = BocThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            x_length=6.5,
            y_length=6.5,
            z_length=5.2,
        )

        def p(v: np.ndarray):
            return axes.c2p(*v)

        def vec_arrow(v, color=S.STRUCTURE, start=ORIGIN, thickness=0.025):
            return hero_arrow_3d(p(np.array(start)), p(np.array(start) + np.array(v)), color=color, thickness=thickness)

        standard = VGroup(
            vec_arrow([1, 0, 0], color=S.DATA),
            vec_arrow([0, 1, 0], color=S.HIGHLIGHT),
            vec_arrow([0, 0, 1], color=S.CONTENT_GOLD),
        )
        basis_tags = VGroup(
            vlabel("e1", S.DATA).move_to(p(np.array([1.25, 0, 0]))),
            vlabel("e2", S.HIGHLIGHT).move_to(p(np.array([0, 1.25, 0]))),
            vlabel("e3", S.CONTENT_GOLD).move_to(p(np.array([0, 0, 1.25]))),
        )

        self.play(FadeIn(axes), LaggedStart(*[Create(a) for a in standard], lag_ratio=0.18), run_time=S.BEAT)
        self.play(FadeIn(basis_tags), run_time=S.QUICK)
        cap = self.show_caption("Start in ordinary 3D coordinates.")
        self.beat("HOLD")
        self.hide_caption(cap)

        equation = vlabel("x + y + z = 0", S.FG).to_edge(UP)
        self.add_fixed_in_frame_mobjects(equation)
        plane = Surface(
            lambda u, v: axes.c2p(u, v, -u - v),
            u_range=[-2.2, 2.2],
            v_range=[-2.2, 2.2],
            resolution=(14, 14),
            fill_color=S.SHADOW,
            fill_opacity=0.34,
            stroke_color=S.GRID,
            stroke_opacity=0.38,
        )
        self.play(FadeIn(equation), FadeIn(plane), run_time=S.BEAT)
        self.beat("BEAT")

        checks = [
            (np.array([1, -1, 0]), "1 - 1 + 0 = 0", S.DATA),
            (TARGET, "2 - 3 + 1 = 0", S.DATA),
            (np.array([1, 1, 1]), "sum = 3", S.CONTENT_RUST),
        ]
        for point, text, color in checks:
            dot = data_dot_3d(p(point), color=color, radius=S.DOT_HERO)
            tag = vlabel(text, color=color).next_to(equation, DOWN, buff=0.25)
            self.add_fixed_in_frame_mobjects(tag)
            self.play(FadeIn(dot), FadeIn(tag), run_time=S.QUICK)
            self.beat("BEAT")
            self.play(FadeOut(tag), run_time=S.QUICK)
            if color == S.CONTENT_RUST:
                self.play(dot.animate.set_opacity(S.OP_GHOST), run_time=S.QUICK)

        basis_a = VGroup(vec_arrow(A1), vec_arrow(A2))
        basis_a_label = vlabel("Basis A", S.STRUCTURE).next_to(equation, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(basis_a_label)
        grid_a = self.plane_grid(axes, A1, A2)
        self.play(FadeIn(basis_a_label), LaggedStart(Create(basis_a[0]), Create(basis_a[1]), lag_ratio=0.2), run_time=S.BEAT)
        self.play(Create(grid_a), run_time=S.BEAT)
        self.beat("BEAT")

        target_dot = data_dot_3d(p(TARGET), radius=S.DOT_HERO)
        step_1 = vec_arrow(3 * A1, color=S.STRUCTURE)
        step_2 = vec_arrow(-A2, color=S.CALLOUT, start=3 * A1, thickness=0.022)
        path_label = vlabel("3(1,-1,0) + (-1)(1,0,-1)", S.FG)
        coord_a = vlabel("target coordinates in Basis A: (3, -1)", S.STRUCTURE)
        for m in (path_label, coord_a):
            m.next_to(equation, DOWN, buff=0.25)
            self.add_fixed_in_frame_mobjects(m)
        self.play(FadeOut(basis_a_label), FadeIn(path_label), Create(step_1), run_time=S.BEAT)
        self.play(Create(step_2), FadeIn(target_dot), run_time=S.BEAT)
        self.play(FadeOut(path_label), FadeIn(coord_a), run_time=S.QUICK)
        self.beat("HOLD")
        self.play(FadeOut(coord_a), FadeOut(step_1), FadeOut(step_2), run_time=S.QUICK)

        basis_b = VGroup(vec_arrow(B1), vec_arrow(B2))
        basis_b_label = vlabel("Basis B", S.STRUCTURE).next_to(equation, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(basis_b_label)
        grid_b = self.plane_grid(axes, B1, B2)
        self.play(FadeOut(grid_a), FadeOut(basis_a), FadeIn(basis_b_label), run_time=S.BEAT)
        self.play(LaggedStart(Create(basis_b[0]), Create(basis_b[1]), lag_ratio=0.2), Create(grid_b), run_time=S.BEAT)
        self.beat("BEAT")

        coord_b = vlabel("same target in Basis B: (1, 0)", S.STRUCTURE).next_to(equation, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(coord_b)
        self.play(FadeOut(basis_b_label), run_time=S.QUICK)
        self.play(FadeIn(coord_b), Indicate(target_dot, color=S.STRUCTURE), run_time=S.BEAT)
        self.beat("HOLD")

        cards = [
            "Same plane. Different bases.",
            "The plane is fixed. The axes within it are a choice.",
            "Coordinates depend on basis. The point does not.",
        ]
        self.play(FadeOut(coord_b), FadeOut(equation), run_time=S.QUICK)
        for line in cards:
            card = vlabel(line, S.FG).to_edge(DOWN)
            self.add_fixed_in_frame_mobjects(card)
            self.play(FadeIn(card), run_time=S.QUICK)
            self.beat("HOLD")
            self.play(FadeOut(card), run_time=S.QUICK)

    def plane_grid(self, axes: BocThreeDAxes, u: np.ndarray, v: np.ndarray) -> VGroup:
        def c(point):
            return axes.c2p(*point)

        lines = VGroup()
        for k in range(-2, 3):
            lines.add(residual(c(-2 * u + k * v), c(2 * u + k * v), color=S.GRID, stroke_width=S.STROKE_AXIS))
            lines.add(residual(c(k * u - 2 * v), c(k * u + 2 * v), color=S.GRID, stroke_width=S.STROKE_AXIS))
        lines.set_opacity(0.75)
        return lines
