"""Blog visual 5 — superposition (point vs. cloud).

Side-by-side contrast:
  LEFT  — "pickle" as a clean, concentrated glow. Arrow aimed at it lands
          dead center.
  RIGHT — "Golden Gate Bridge" as a diffuse cloud overlapping with
          translucent regions for California, San Francisco, Bridges,
          Famous Landmarks. Arrow aimed at the supposed center lands in
          the overlap with "California".

Caption: "Common concepts are points. Rare ones are weather."
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREEN,
    GREY_B,
    LEFT,
    ORANGE,
    RED,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Text,
    VGroup,
    Write,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


class Superposition(Scene):
    def construct(self):
        title = Text(
            "Why steering sometimes misses",
            font_size=36,
            color=WHITE,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=0.2 * DOWN))

        # vertical divider
        divider = Line(
            [0, -3.2, 0], [0, 2.6, 0], stroke_color=GREY_B, stroke_opacity=0.4
        )
        self.play(Create(divider, run_time=0.5))

        # ------------------- LEFT: clean pickle point -------------------
        left_center = np.array([-3.5, 0.0, 0])

        left_title = Text('"pickle"', font_size=28, color=GREEN).move_to(
            left_center + np.array([0, 2.2, 0])
        )
        self.play(FadeIn(left_title))

        # A tight glow: concentric dots, increasing opacity
        pickle_glow = VGroup()
        for r, op in [(0.9, 0.10), (0.6, 0.20), (0.35, 0.45), (0.15, 0.9)]:
            pickle_glow.add(Circle(radius=r, color=GREEN, fill_opacity=op, stroke_opacity=0))
        pickle_core = Dot(color=GREEN, radius=0.08)
        pickle_cluster = VGroup(pickle_glow, pickle_core).move_to(left_center)
        self.play(FadeIn(pickle_cluster))
        self.wait(0.3)

        # Arrow aimed at center
        left_tail = left_center + np.array([-2.5, -1.6, 0])
        arrow_L = Arrow(
            left_tail, left_center, buff=0.05, color=YELLOW, stroke_width=6
        )
        self.play(Create(arrow_L), run_time=1.0)

        hit_L = Dot(left_center, color=YELLOW, radius=0.12)
        self.play(FadeIn(hit_L, scale=1.8))

        left_caption = Text(
            "clean direction · lands on target",
            font_size=22,
            color=GREEN,
        ).move_to(left_center + np.array([0, -2.3, 0]))
        self.play(Write(left_caption))
        self.wait(0.6)

        # ------------------- RIGHT: diffuse Golden Gate -------------------
        right_center = np.array([3.5, 0.0, 0])

        right_title = Text('"Golden Gate Bridge"', font_size=28, color=ORANGE).move_to(
            right_center + np.array([0, 2.2, 0])
        )
        self.play(FadeIn(right_title))

        # Overlapping translucent region blobs with labels
        california = Circle(radius=1.3, color=BLUE, fill_opacity=0.20, stroke_opacity=0.4).move_to(
            right_center + np.array([-0.7, 0.3, 0])
        )
        ca_label = Text("California", font_size=20, color=BLUE).move_to(
            right_center + np.array([-1.5, 1.0, 0])
        )

        sf = Circle(radius=1.0, color=RED, fill_opacity=0.20, stroke_opacity=0.4).move_to(
            right_center + np.array([0.6, 0.5, 0])
        )
        sf_label = Text("San Francisco", font_size=20, color=RED).move_to(
            right_center + np.array([1.7, 1.2, 0])
        )

        bridges = Circle(radius=0.9, color=GREEN, fill_opacity=0.20, stroke_opacity=0.4).move_to(
            right_center + np.array([0.2, -0.7, 0])
        )
        br_label = Text("bridges", font_size=20, color=GREEN).move_to(
            right_center + np.array([-0.4, -1.4, 0])
        )

        landmarks = Circle(radius=0.95, color=YELLOW, fill_opacity=0.15, stroke_opacity=0.4).move_to(
            right_center + np.array([1.0, -0.4, 0])
        )
        lm_label = Text("famous landmarks", font_size=20, color=YELLOW).move_to(
            right_center + np.array([1.8, -1.2, 0])
        )

        self.play(
            FadeIn(california), FadeIn(ca_label),
            FadeIn(sf), FadeIn(sf_label),
            FadeIn(bridges), FadeIn(br_label),
            FadeIn(landmarks), FadeIn(lm_label),
            run_time=1.2,
        )

        # No sharp center — the concept exists in the overlap.
        ghost_center = right_center + np.array([0.3, 0.0, 0])
        aim_marker = Dot(ghost_center, color=WHITE, radius=0.06, fill_opacity=0.5)
        aim_label = Text("aimed here", font_size=18, color=GREY_B).next_to(
            aim_marker, UP, buff=0.1
        )
        self.play(FadeIn(aim_marker), FadeIn(aim_label))
        self.wait(0.4)

        # Arrow aimed at that ghost center — but the dot lands in the
        # California overlap instead.
        right_tail = right_center + np.array([2.5, -1.6, 0])
        # Land where California + SF overlap (slightly west of aim point)
        land_point = right_center + np.array([-0.3, 0.5, 0])

        arrow_R = Arrow(
            right_tail, land_point, buff=0.05, color=YELLOW, stroke_width=6
        )
        self.play(Create(arrow_R), run_time=1.0)
        hit_R = Dot(land_point, color=YELLOW, radius=0.12)
        self.play(FadeIn(hit_R, scale=1.8))

        # Callout
        miss = Text(
            "landed in California instead",
            font_size=20,
            color=YELLOW,
        ).move_to(right_center + np.array([0, -2.3, 0]))
        self.play(Write(miss))
        self.wait(0.8)

        # ------------------- punchline -------------------
        self.play(FadeOut(title))
        punch = Text(
            "common concepts are points.  rare ones are weather.",
            font_size=28,
            color=WHITE,
        ).to_edge(UP, buff=0.3)
        self.play(Write(punch))
        self.wait(2.2)
