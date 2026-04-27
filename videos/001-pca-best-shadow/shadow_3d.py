"""Scene 6 - The Best Shadow.

Viewer takeaway: PCA is the rotation of your data that makes its floor-shadow
as spread out as possible. We rotate a 3D cloud in real time, the shadow on
the z=0 plane reshapes, then we settle on the maximally-spread orientation -
that is PC1 / PC2.

Render:
    cd videos/001-pca-best-shadow && uv run manim -pql shadow_3d.py BestShadow
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import *
from sklearn.decomposition import PCA

from videos._shared import style as S
from videos._shared.base import Boc3DScene
from videos._shared.mobjects import BocThreeDAxes

N_POINTS = 120
FLOOR_Z = -2.5


def euler_xyz(rx_deg: float, ry_deg: float, rz_deg: float) -> np.ndarray:
    a, b, c = np.deg2rad([rx_deg, ry_deg, rz_deg])
    Rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    Ry = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    Rz = np.array([[np.cos(c), -np.sin(c), 0], [np.sin(c), np.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def make_cloud(rng: np.random.Generator) -> np.ndarray:
    stds = np.array([1.8, 0.9, 0.35])
    X = rng.normal(size=(N_POINTS, 3)) * stds
    return X @ euler_xyz(35, -20, 50).T


class BestShadow(Boc3DScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)
        X = make_cloud(rng)
        pca = PCA(n_components=3).fit(X)
        W = pca.components_.T

        axes = BocThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-3, 3, 1],
            x_length=7, y_length=7, z_length=5,
        )
        floor = Square(side_length=7, color=S.GRID, fill_opacity=0.18, stroke_opacity=0.4)
        floor.move_to(axes.c2p(0, 0, 0) + np.array([0, 0, FLOOR_Z]))

        yaw = ValueTracker(0.0)
        pitch = ValueTracker(0.0)

        def rotated_points() -> np.ndarray:
            R = euler_xyz(pitch.get_value(), 0.0, yaw.get_value())
            return X @ R.T

        def make_group(color, radius: float, opacity: float = 1.0) -> VGroup:
            g = VGroup(*[Dot(color=color, radius=radius) for _ in range(N_POINTS)])
            g.set_opacity(opacity)
            return g

        def sync_positions(group: VGroup, points: np.ndarray, floor_only: bool = False) -> None:
            for dot, p in zip(group, points):
                z = FLOOR_Z if floor_only else p[2]
                dot.move_to(axes.c2p(p[0], p[1], z))

        # Cloud (DATA, teal). Shadow uses MUTED for the floor projection.
        cloud = make_group(S.DATA, S.DOT_DATA_3D, opacity=S.OP_DATA)
        shadow = make_group(S.SHADOW, 0.035, opacity=0.85)
        sync_positions(cloud, rotated_points())
        sync_positions(shadow, rotated_points(), floor_only=True)
        cloud.add_updater(lambda m: sync_positions(m, rotated_points()))
        shadow.add_updater(lambda m: sync_positions(m, rotated_points(), floor_only=True))

        caption = self.caption("PCA is the best shadow your data can cast.")

        self.play(FadeIn(axes), FadeIn(floor), run_time=S.BEAT)
        self.add(cloud, shadow)
        self.play(caption.animate.set_opacity(1), run_time=S.QUICK)
        self.beat("QUICK")

        # Beat 1: tumble. Shadow reshapes as we rotate.
        self.play(yaw.animate.set_value(70 * DEGREES), run_time=2.0)
        self.play(pitch.animate.set_value(45 * DEGREES), run_time=1.8)
        self.play(
            yaw.animate.set_value(-25 * DEGREES),
            pitch.animate.set_value(-15 * DEGREES),
            run_time=2.0,
        )
        self.beat("QUICK")

        # Beat 2: settle on PC-aligned orientation. The discovered structure
        # transitions from teal (data) to magenta (PC1/PC2 found) - the
        # signature teal->magenta shift.
        cloud.clear_updaters()
        shadow.clear_updaters()
        pc_points = X @ W
        target = make_group(S.STRUCTURE, S.DOT_HERO)
        target_shadow = make_group(S.SHADOW, 0.04, opacity=0.85)
        sync_positions(target, pc_points)
        sync_positions(target_shadow, pc_points, floor_only=True)
        self.play(
            Transform(cloud, target),
            Transform(shadow, target_shadow),
            run_time=2.5,
        )

        tag = Text(
            "maximally spread shadow  =  PC₁, PC₂",
            font=S.FONT,
        ).scale(S.TAG_SCALE).set_color(S.STRUCTURE)
        tag.next_to(caption, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(tag)
        self.play(FadeIn(tag, shift=DOWN * 0.2))
        self.beat("HOLD")
