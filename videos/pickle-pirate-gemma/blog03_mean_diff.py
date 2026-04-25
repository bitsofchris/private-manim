"""Blog visual 3 — mean-difference arrow.

Slim version of harness scene 03, Act 1. ~8 seconds.

Two clouds of dots fade in already labeled — "pickle sentences" (green)
and "other-food sentences" (orange). The two centroids pop in as
hollow circles. A yellow arrow draws from the orange centroid to the
green centroid. Caption: "the pickle direction."

No staged method walk-through (that's harness 03's job). This scene
just shows the *result* of mean-difference, sized for the mainstream
post's pacing.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    GREEN,
    GREY_B,
    ORANGE,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Scene,
    Text,
    VGroup,
    Write,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


P_OTHER = np.array([-2.6, -0.8, 0])
P_PICKLE = np.array([2.6, 0.9, 0])


class MeanDiff(Scene):
    def construct(self):
        title = Text(
            "build the arrow by subtraction",
            font_size=32,
            color=WHITE,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        rng = np.random.default_rng(11)

        other_dots = VGroup(
            *[
                Dot(
                    P_OTHER + np.array([rng.normal(0, 0.55), rng.normal(0, 0.45), 0]),
                    color=ORANGE,
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
                    color=GREEN,
                    radius=0.07,
                    fill_opacity=0.85,
                )
                for _ in range(30)
            ]
        )

        other_label = Text(
            "30 other-food sentences", font_size=22, color=ORANGE
        ).move_to(P_OTHER + np.array([0, -1.6, 0]))
        pickle_label = Text(
            "30 pickle sentences", font_size=22, color=GREEN
        ).move_to(P_PICKLE + np.array([0, 1.7, 0]))

        self.play(
            FadeIn(other_dots), FadeIn(pickle_dots),
            FadeIn(other_label), FadeIn(pickle_label),
            run_time=0.8,
        )
        self.wait(0.4)

        # Centroids
        other_centroid = Circle(radius=0.22, color=ORANGE, stroke_width=4).move_to(
            P_OTHER
        )
        pickle_centroid = Circle(radius=0.22, color=GREEN, stroke_width=4).move_to(
            P_PICKLE
        )
        centroid_caption = Text(
            "average each cloud", font_size=22, color=GREY_B
        ).to_edge(DOWN, buff=1.6)
        self.play(
            Create(other_centroid), Create(pickle_centroid),
            FadeIn(centroid_caption),
            run_time=0.8,
        )
        self.wait(0.6)

        # Arrow
        arrow = Arrow(
            P_OTHER, P_PICKLE,
            buff=0.28, color=YELLOW, stroke_width=7,
        )
        # Place the label perpendicular to the arrow shaft (CCW side, i.e.
        # above-left for this up-right arrow) so it can never overlap the
        # diagonal stroke regardless of the cloud positions.
        arrow_vec = P_PICKLE - P_OTHER
        arrow_norm = float(np.linalg.norm(arrow_vec[:2]))
        perp = np.array([-arrow_vec[1] / arrow_norm, arrow_vec[0] / arrow_norm, 0.0])
        midpoint = (P_OTHER + P_PICKLE) / 2
        arrow_label = Text(
            "the pickle direction", font_size=26, color=YELLOW,
        ).move_to(midpoint + 1.2 * perp)
        self.play(FadeOut(centroid_caption), run_time=0.3)
        self.play(Create(arrow), run_time=0.7)
        self.play(Write(arrow_label), run_time=0.6)
        self.wait(1.4)

        foot = Text(
            "subtract the averages. that arrow is the steering vector.",
            font_size=22,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(foot))
        self.wait(1.4)
