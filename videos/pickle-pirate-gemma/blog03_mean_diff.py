"""Blog visual 3 — mean-difference arrow.

Slim version of harness scene 03, Act 1. ~8 seconds.

Two clouds of dots fade in already labeled — "pickle sentences" (green)
and "other-food sentences" (orange). The two centroids pop in as
hollow circles. A magenta arrow draws from the orange centroid to the
green centroid — the discovered structure.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog03_mean_diff.py MeanDiff
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
    Text,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene


P_OTHER = np.array([-2.6, -0.8, 0])
P_PICKLE = np.array([2.6, 0.9, 0])


class MeanDiff(BocScene):
    def construct(self):
        title = Text(
            "build the arrow by subtraction",
            font=S.FONT,
            font_size=32,
            color=S.FG,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        rng = np.random.default_rng(11)

        other_dots = VGroup(
            *[
                Dot(
                    P_OTHER + np.array([rng.normal(0, 0.55), rng.normal(0, 0.45), 0]),
                    color=S.CONTENT_OTHER,
                    radius=0.07,
                    fill_opacity=0.75,
                )
                for _ in range(30)
            ]
        )
        pickle_dots = VGroup(
            *[
                Dot(
                    P_PICKLE + np.array([rng.normal(0, 0.45), rng.normal(0, 0.4), 0]),
                    color=S.CONTENT_PICKLE,
                    radius=0.07,
                    fill_opacity=0.85,
                )
                for _ in range(30)
            ]
        )

        other_label = Text(
            "30 other-food sentences", font=S.FONT, font_size=22, color=S.CONTENT_OTHER
        ).move_to(P_OTHER + np.array([0, -1.6, 0]))
        pickle_label = Text(
            "30 pickle sentences", font=S.FONT, font_size=22, color=S.CONTENT_PICKLE
        ).move_to(P_PICKLE + np.array([0, 1.7, 0]))

        self.play(
            FadeIn(other_dots), FadeIn(pickle_dots),
            FadeIn(other_label), FadeIn(pickle_label),
            run_time=S.BEAT,
        )
        self.beat("QUICK")

        # Centroids
        other_centroid = Circle(radius=0.22, color=S.CONTENT_OTHER, stroke_width=4).move_to(
            P_OTHER
        )
        pickle_centroid = Circle(radius=0.22, color=S.CONTENT_PICKLE, stroke_width=4).move_to(
            P_PICKLE
        )
        centroid_caption = Text(
            "average each cloud", font=S.FONT, font_size=22, color=S.FG_DIM
        ).to_edge(DOWN, buff=1.6)
        self.play(
            Create(other_centroid), Create(pickle_centroid),
            FadeIn(centroid_caption),
            run_time=S.BEAT,
        )
        self.beat("BEAT")

        # The discovered direction (STRUCTURE magenta).
        arrow = Arrow(
            P_OTHER, P_PICKLE,
            buff=0.28, color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE,
        )
        arrow_vec = P_PICKLE - P_OTHER
        arrow_norm = float(np.linalg.norm(arrow_vec[:2]))
        perp = np.array([-arrow_vec[1] / arrow_norm, arrow_vec[0] / arrow_norm, 0.0])
        midpoint = (P_OTHER + P_PICKLE) / 2
        arrow_label = Text(
            "the pickle direction", font=S.FONT, font_size=26, color=S.STRUCTURE,
        ).move_to(midpoint + 1.2 * perp)
        self.play(FadeOut(centroid_caption), run_time=S.QUICK)
        self.play(Create(arrow), run_time=0.7)
        self.play(Write(arrow_label), run_time=0.6)
        self.wait(1.4)

        foot = Text(
            "subtract the averages. that arrow is the steering vector.",
            font=S.FONT,
            font_size=22,
            color=S.FG_DIM,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(foot))
        self.wait(1.4)
