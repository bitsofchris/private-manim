"""Blog visual 5 — superposition (point vs. cloud).

Side-by-side: clean pickle glow vs diffuse Golden Gate cloud overlapping
multiple regions. Steering arrow lands cleanly on pickle, drifts into
California overlap on Golden Gate.

Categorical scene: house BG/type/motion only.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog05_superposition.py Superposition
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import (
    DOWN,
    UP,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Text,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene


class Superposition(BocScene):
    def construct(self):
        title = Text(
            "Why steering sometimes misses",
            font=S.FONT, font_size=36, color=S.FG,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=0.2 * DOWN))

        divider = Line(
            [0, -3.2, 0], [0, 2.6, 0], stroke_color=S.FG_DIM, stroke_opacity=0.4
        )
        self.play(Create(divider, run_time=0.5))

        # ------------------- LEFT: clean pickle point -------------------
        left_center = np.array([-3.5, 0.0, 0])

        left_title = Text(
            '"pickle"', font=S.FONT, font_size=28, color=S.CONTENT_PICKLE,
        ).move_to(left_center + np.array([0, 2.2, 0]))
        self.play(FadeIn(left_title))

        pickle_glow = VGroup()
        for r, op in [(0.9, 0.10), (0.6, 0.20), (0.35, 0.45), (0.15, 0.9)]:
            pickle_glow.add(
                Circle(radius=r, color=S.CONTENT_PICKLE, fill_opacity=op, stroke_opacity=0)
            )
        pickle_core = Dot(color=S.CONTENT_PICKLE, radius=0.08)
        pickle_cluster = VGroup(pickle_glow, pickle_core).move_to(left_center)
        self.play(FadeIn(pickle_cluster))
        self.wait(0.3)

        left_tail = left_center + np.array([-2.5, -1.6, 0])
        arrow_L = Arrow(
            left_tail, left_center, buff=0.05,
            color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE,
        )
        self.play(Create(arrow_L), run_time=1.0)

        hit_L = Dot(left_center, color=S.STRUCTURE, radius=0.12)
        self.play(FadeIn(hit_L, scale=1.8))

        left_caption = Text(
            "clean direction · lands on target",
            font=S.FONT, font_size=22, color=S.CONTENT_PICKLE,
        ).move_to(left_center + np.array([0, -2.3, 0]))
        self.play(Write(left_caption))
        self.wait(0.6)

        # ------------------- RIGHT: diffuse Golden Gate -------------------
        right_center = np.array([3.5, 0.0, 0])

        right_title = Text(
            '"Golden Gate Bridge"', font=S.FONT, font_size=28, color=S.CONTENT_GOLD,
        ).move_to(right_center + np.array([0, 2.2, 0]))
        self.play(FadeIn(right_title))

        california = Circle(
            radius=1.3, color=S.ACCENT_CYAN, fill_opacity=0.20, stroke_opacity=0.4,
        ).move_to(right_center + np.array([-0.7, 0.3, 0]))
        ca_label = Text(
            "California", font=S.FONT, font_size=20, color=S.ACCENT_CYAN,
        ).move_to(right_center + np.array([-1.5, 1.0, 0]))

        sf = Circle(
            radius=1.0, color=S.ACCENT_PINK, fill_opacity=0.20, stroke_opacity=0.4,
        ).move_to(right_center + np.array([0.6, 0.5, 0]))
        sf_label = Text(
            "San Francisco", font=S.FONT, font_size=20, color=S.ACCENT_PINK,
        ).move_to(right_center + np.array([1.7, 1.2, 0]))

        bridges = Circle(
            radius=0.9, color=S.CONTENT_PICKLE, fill_opacity=0.20, stroke_opacity=0.4,
        ).move_to(right_center + np.array([0.2, -0.7, 0]))
        br_label = Text(
            "bridges", font=S.FONT, font_size=20, color=S.CONTENT_PICKLE,
        ).move_to(right_center + np.array([-0.4, -1.4, 0]))

        landmarks = Circle(
            radius=0.95, color=S.CONTENT_GOLD, fill_opacity=0.15, stroke_opacity=0.4,
        ).move_to(right_center + np.array([1.0, -0.4, 0]))
        lm_label = Text(
            "famous landmarks", font=S.FONT, font_size=20, color=S.CONTENT_GOLD,
        ).move_to(right_center + np.array([1.8, -1.2, 0]))

        self.play(
            FadeIn(california), FadeIn(ca_label),
            FadeIn(sf), FadeIn(sf_label),
            FadeIn(bridges), FadeIn(br_label),
            FadeIn(landmarks), FadeIn(lm_label),
            run_time=1.2,
        )

        ghost_center = right_center + np.array([0.3, 0.0, 0])
        aim_marker = Dot(ghost_center, color=S.FG, radius=0.06, fill_opacity=0.5)
        aim_label = Text(
            "aimed here", font=S.FONT, font_size=18, color=S.FG_DIM,
        ).next_to(aim_marker, UP, buff=0.1)
        self.play(FadeIn(aim_marker), FadeIn(aim_label))
        self.wait(0.4)

        right_tail = right_center + np.array([2.5, -1.6, 0])
        land_point = right_center + np.array([-0.3, 0.5, 0])

        arrow_R = Arrow(
            right_tail, land_point, buff=0.05,
            color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE,
        )
        self.play(Create(arrow_R), run_time=1.0)
        hit_R = Dot(land_point, color=S.STRUCTURE, radius=0.12)
        self.play(FadeIn(hit_R, scale=1.8))

        miss = Text(
            "landed in California instead",
            font=S.FONT, font_size=20, color=S.ACCENT_PINK,
        ).move_to(right_center + np.array([0, -2.3, 0]))
        self.play(Write(miss))
        self.wait(0.8)

        self.play(FadeOut(title))
        self.wait(2.2)

        # Final beat — fade everything, hold on the word.
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        word = Text(
            "superposition", font=S.FONT, font_size=72, color=S.STRUCTURE, weight="BOLD",
        )
        self.play(Write(word), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(word), run_time=0.5)
