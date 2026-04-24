"""Blog visual 2 — king − man + woman ≈ queen.

Narrative:
  1. Four labeled points appear: king, man, woman, queen (parallelogram).
  2. Discover the "gender direction" as an arrow from man → woman.
     This IS the vector (woman − man).
  3. Copy that same arrow so its tail sits on king.
     Tip lands (almost) on queen.
  4. Caption reveals: king + (woman − man) ≈ queen,
     i.e. king − man + woman ≈ queen.

The aha is that the same *direction* — extracted from one pair —
transports one royal-gender concept onto the other. That's what makes
"meaning is geometry" feel real.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREY_B,
    LEFT,
    ORANGE,
    PINK,
    RED,
    RIGHT,
    TEAL,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    NumberPlane,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


# Parallelogram coordinates, tilted slightly so the "gender" vector is
# clearly a direction (not just "slide right").
P_MAN = np.array([-2.5, -1.2])
P_WOMAN = np.array([2.0, -0.6])
P_KING = np.array([-2.5, 1.4])
P_QUEEN = P_KING + (P_WOMAN - P_MAN)  # = (2.0, 2.0)


class KingQueen(Scene):
    def construct(self):
        title = Text(
            "You can do math with meaning",
            font_size=36,
            color=WHITE,
        ).to_edge(UP, buff=0.3)
        self.play(FadeIn(title, shift=0.2 * DOWN))

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=11,
            y_length=6,
            background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.2},
            axis_config={"stroke_color": GREY_B, "stroke_opacity": 0.4},
        ).shift(0.1 * DOWN)
        self.play(Create(plane, run_time=0.7))

        def point(p, color, label_text, direction=UP):
            dot = Dot(plane.c2p(p[0], p[1]), color=color, radius=0.13)
            lbl = Text(label_text, font_size=28, color=color).next_to(
                dot, direction, buff=0.15
            )
            return dot, lbl, VGroup(dot, lbl)

        man_d, man_l, man = point(P_MAN, BLUE, "man", DOWN)
        woman_d, woman_l, woman = point(P_WOMAN, PINK, "woman", DOWN)
        king_d, king_l, king = point(P_KING, BLUE, "king", UP)
        queen_d, queen_l, queen = point(P_QUEEN, PINK, "queen", UP)

        # Introduce points, bottom pair first, then royals
        self.play(FadeIn(man), FadeIn(woman), run_time=0.8)
        self.play(FadeIn(king), FadeIn(queen), run_time=0.8)
        self.wait(0.5)

        # ---------- Step 1: learn the gender direction ----------
        step1 = Text(
            "step 1 — the direction from man to woman",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(step1))

        # Indicate the two source points
        self.play(Indicate(man_d, color=YELLOW), Indicate(woman_d, color=YELLOW))

        gender_arrow = Arrow(
            plane.c2p(P_MAN[0], P_MAN[1]),
            plane.c2p(P_WOMAN[0], P_WOMAN[1]),
            buff=0.18,
            color=YELLOW,
            stroke_width=6,
        )
        gender_label = Text(
            "woman − man",
            font_size=24,
            color=YELLOW,
        ).move_to(plane.c2p(-0.3, -1.3))
        self.play(Create(gender_arrow), run_time=1.2)
        self.play(Write(gender_label))
        self.wait(1.0)

        # Emphasize: this arrow captures "what changes when you flip gender"
        gloss = Text(
            "a direction, not a place",
            font_size=22,
            color=GREY_B,
        ).next_to(gender_label, DOWN, buff=0.2)
        self.play(FadeIn(gloss))
        self.wait(1.2)
        self.play(FadeOut(gloss))

        # ---------- Step 2: apply the same arrow, from king ----------
        step2 = Text(
            "step 2 — apply the same direction, starting at king",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.5)
        self.play(Transform(step1, step2))
        self.play(Indicate(king_d, color=YELLOW))

        # Slide a COPY of the gender arrow from man→woman up to originate
        # at king. The copy's start/end both lift by (P_KING − P_MAN).
        applied_arrow = gender_arrow.copy()
        shift_vec = plane.c2p(P_KING[0], P_KING[1]) - plane.c2p(P_MAN[0], P_MAN[1])
        self.play(
            applied_arrow.animate.shift(shift_vec),
            gender_label.animate.shift(shift_vec),
            run_time=1.6,
        )
        self.wait(0.4)

        # Dashed guide showing parallel translation
        guide_bottom = DashedLine(
            plane.c2p(P_MAN[0], P_MAN[1]),
            plane.c2p(P_KING[0], P_KING[1]),
            dash_length=0.1,
            stroke_color=GREY_B,
            stroke_opacity=0.5,
        )
        guide_top = DashedLine(
            plane.c2p(P_WOMAN[0], P_WOMAN[1]),
            plane.c2p(P_QUEEN[0], P_QUEEN[1]),
            dash_length=0.1,
            stroke_color=GREY_B,
            stroke_opacity=0.5,
        )
        self.play(Create(guide_bottom), Create(guide_top), run_time=0.8)
        self.wait(0.6)

        # Highlight that the tip lands on queen
        ring = Circle(radius=0.35, color=YELLOW).move_to(
            plane.c2p(P_QUEEN[0], P_QUEEN[1])
        )
        self.play(Create(ring))
        self.wait(0.6)

        # ---------- Step 3: the equation ----------
        eq = Text(
            "king  +  (woman − man)  ≈  queen",
            font_size=32,
            color=WHITE,
        ).to_edge(DOWN, buff=0.5)
        self.play(Transform(step1, eq))
        self.wait(1.4)

        eq2 = Text(
            "king  −  man  +  woman  ≈  queen",
            font_size=34,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.5)
        self.play(Transform(step1, eq2))
        self.wait(2.2)
