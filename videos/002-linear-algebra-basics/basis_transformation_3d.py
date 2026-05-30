"""The same vector has different coordinates in different bases.

Viewer takeaway: coordinates are coefficients. The point stays fixed while the
grid used to read its address changes.

Render:
    cd videos/002-linear-algebra-basics
    uv run manim -pql basis_transformation_3d.py BasisTransformation3D
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import *

from videos._shared import style as S
from videos._shared.base import Boc3DScene
from videos._shared.mobjects import BocThreeDAxes, data_dot_3d, hero_arrow_3d


E1 = np.array([1, 0, 0])
E2 = np.array([0, 1, 0])
E3 = np.array([0, 0, 1])
V1 = np.array([1, 0, 0])
V2 = np.array([1, 1, 0])
V3 = np.array([1, 1, 1])
TARGET = np.array([3, 5, 2])


def label(text: str, color: str = S.FG, scale: float = S.LABEL_SCALE) -> Text:
    return Text(text, font=S.FONT).scale(scale).set_color(color)


class BasisTransformation3D(Boc3DScene):
    def construct(self):
        self.set_camera_orientation(phi=S.CAM_PHI, theta=S.CAM_THETA, zoom=1.18)

        axes = BocThreeDAxes(
            x_range=[-4, 7, 1],
            y_range=[-3, 7, 1],
            z_range=[-2, 5, 1],
            x_length=7,
            y_length=6.4,
            z_length=4.8,
        )

        def p(v: np.ndarray):
            return axes.c2p(*v)

        def arrow(v, start=ORIGIN, color=S.STRUCTURE, thickness=0.022):
            start = np.array(start)
            return hero_arrow_3d(p(start), p(start + np.array(v)), color=color, thickness=thickness)

        standard_basis = VGroup(
            arrow(E1, color=S.DATA),
            arrow(E2, color=S.HIGHLIGHT),
            arrow(E3, color=S.CONTENT_GOLD),
        )
        standard_labels = VGroup(
            label("e1", S.DATA).move_to(p(1.25 * E1)),
            label("e2", S.HIGHLIGHT).move_to(p(1.25 * E2)),
            label("e3", S.CONTENT_GOLD).move_to(p(1.25 * E3)),
        )
        standard_grid = self.lattice(axes, E1, E2, E3, S.GRID, opacity=0.38)

        self.play(FadeIn(axes), Create(standard_grid), run_time=S.HOLD)
        self.play(LaggedStart(*[Create(a) for a in standard_basis], lag_ratio=0.15), FadeIn(standard_labels), run_time=S.HOLD)

        target = data_dot_3d(p(TARGET), radius=S.DOT_HERO)
        target_label = label("target: (3, 5, 2)", S.DATA).to_edge(UP)
        self.add_fixed_in_frame_mobjects(target_label)
        self.play(FadeIn(target), FadeIn(target_label), run_time=S.BEAT)
        self.begin_ambient_camera_rotation(rate=S.CAM_AMBIENT_RATE)
        self.beat("HOLD")
        self.stop_ambient_camera_rotation()

        standard_steps = [
            (3 * E1, ORIGIN, "3 * e1"),
            (5 * E2, 3 * E1, "5 * e2"),
            (2 * E3, 3 * E1 + 5 * E2, "2 * e3"),
        ]
        step_mobs = VGroup()
        for vec, start, text in standard_steps:
            step = arrow(vec, start=start)
            step_mobs.add(step)
            tag = label(text, S.STRUCTURE).next_to(target_label, DOWN, buff=0.25)
            self.add_fixed_in_frame_mobjects(tag)
            self.play(Create(step), FadeIn(tag), run_time=S.HOLD)
            self.play(FadeOut(tag), run_time=S.BEAT)

        panel = self.coord_panel(
            "Standard basis: (3, 5, 2)",
            "components are coefficients here",
        )
        self.add_fixed_in_frame_mobjects(panel)
        self.play(FadeIn(panel), Indicate(target, color=S.DATA), run_time=S.HOLD)
        self.beat("HOLD")

        new_basis = VGroup(
            arrow(V1, color=S.DATA),
            arrow(V2, color=S.HIGHLIGHT),
            arrow(V3, color=S.CONTENT_GOLD),
        )
        new_labels = VGroup(
            label("v1", S.DATA).move_to(p(1.35 * V1)),
            label("v2", S.HIGHLIGHT).move_to(p(1.25 * V2)),
            label("v3", S.CONTENT_GOLD).move_to(p(1.15 * V3)),
        )
        new_specs = [
            (new_basis[0], new_labels[0], "v1 = (1, 0, 0)", S.DATA),
            (new_basis[1], new_labels[1], "v2 = (1, 1, 0)", S.HIGHLIGHT),
            (new_basis[2], new_labels[2], "v3 = (1, 1, 1)", S.CONTENT_GOLD),
        ]
        self.play(FadeOut(standard_basis), FadeOut(standard_labels), FadeOut(step_mobs), run_time=S.BEAT)
        for basis_vec, basis_name, text, color in new_specs:
            coord = label(text, color).next_to(target_label, DOWN, buff=0.25)
            self.add_fixed_in_frame_mobjects(coord)
            self.play(Create(basis_vec), FadeIn(basis_name), FadeIn(coord), run_time=S.HOLD)
            self.beat("QUICK")
            self.play(FadeOut(coord), run_time=S.BEAT)

        sheared_grid = self.lattice(axes, V1, V2, V3, S.GRID, opacity=0.46)
        standard_ghost = self.lattice(axes, E1, E2, E3, S.GRID, opacity=0.16)
        self.play(Transform(standard_grid, sheared_grid), run_time=S.HOLD)
        self.add(standard_ghost)
        self.beat("HOLD")

        new_steps = [
            (-2 * V1, ORIGIN, "-2 * v1", S.DATA, new_basis[0]),
            (3 * V2, -2 * V1, "3 * v2", S.HIGHLIGHT, new_basis[1]),
            (2 * V3, -2 * V1 + 3 * V2, "2 * v3", S.CONTENT_GOLD, new_basis[2]),
        ]
        new_step_mobs = VGroup()
        for vec, start, text, color, basis_vec in new_steps:
            step = arrow(vec, start=start, color=color)
            new_step_mobs.add(step)
            tag = label(text, color).next_to(target_label, DOWN, buff=0.25)
            self.add_fixed_in_frame_mobjects(tag)
            self.play(Create(step), FadeIn(tag), Indicate(basis_vec, color=color), run_time=S.HOLD)
            self.play(FadeOut(tag), run_time=S.BEAT)

        new_panel = self.coord_panel(
            "Standard basis: (3, 5, 2)",
            "New basis: (-2, 3, 2)",
            "same point, different address",
        )
        self.add_fixed_in_frame_mobjects(new_panel)
        self.play(FadeOut(panel), FadeIn(new_panel), Indicate(target, color=S.STRUCTURE), run_time=S.HOLD)
        self.beat("HOLD")

        self.clear()
        for text in [
            "Same vector. Different basis. Different coordinates.",
            "The standard basis is just one choice.",
            "For other bases, solve for the coefficients.",
        ]:
            card = label(text, S.FG, scale=S.CAPTION_SCALE).to_edge(DOWN)
            self.add_fixed_in_frame_mobjects(card)
            self.play(FadeIn(card), run_time=S.BEAT)
            self.beat("HOLD")
            self.play(FadeOut(card), run_time=S.BEAT)

    def lattice(self, axes: BocThreeDAxes, a: np.ndarray, b: np.ndarray, c: np.ndarray, color: str, opacity: float) -> VGroup:
        def point(i, j, k):
            return axes.c2p(*(i * a + j * b + k * c))

        lines = VGroup()
        xr, yr, zr = range(-2, 4), range(-1, 6), range(-1, 4)
        for j in yr:
            for k in zr:
                lines.add(Line(point(-2, j, k), point(3, j, k), color=color, stroke_width=1))
        for i in xr:
            for k in zr:
                lines.add(Line(point(i, -1, k), point(i, 5, k), color=color, stroke_width=1))
        for i in xr:
            for j in yr:
                lines.add(Line(point(i, j, -1), point(i, j, 3), color=color, stroke_width=1))
        lines.set_opacity(opacity)
        return lines

    def coord_panel(self, *rows: str) -> VGroup:
        panel = VGroup(*[label(row, S.FG if i == 0 else S.STRUCTURE) for i, row in enumerate(rows)])
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR)
        return panel
