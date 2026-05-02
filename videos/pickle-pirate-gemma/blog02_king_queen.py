"""Blog visual 2 — king − man + woman ≈ queen.

Reveals the gender vector by showing it transports king onto queen.
The discovered direction (gender) is the magenta hero.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog02_king_queen.py KingQueen
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Text,
    Transform,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocNumberPlane


P_MAN = np.array([-2.5, -1.2])
P_WOMAN = np.array([2.0, -0.6])
P_KING = np.array([-2.5, 1.4])
P_QUEEN = P_KING + (P_WOMAN - P_MAN)


class KingQueen(BocScene):
    def construct(self):
        title = Text(
            "You can do math with meaning",
            font=S.FONT, font_size=36, color=S.FG,
        ).to_edge(UP, buff=0.3)
        self.play(FadeIn(title, shift=0.2 * DOWN))

        plane = BocNumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=11,
            y_length=6,
        ).shift(0.1 * DOWN)
        self.play(Create(plane, run_time=0.7))

        def point(p, color, label_text, direction=UP):
            dot = Dot(plane.c2p(p[0], p[1]), color=color, radius=0.13)
            lbl = Text(label_text, font=S.FONT, font_size=28, color=color).next_to(
                dot, direction, buff=0.15
            )
            return dot, lbl, VGroup(dot, lbl)

        # Categorical: men=cyan, women=pink. Discovered direction (gender) = magenta.
        man_d, man_l, man = point(P_MAN, S.ACCENT_CYAN, "man", DOWN)
        woman_d, woman_l, woman = point(P_WOMAN, S.ACCENT_PINK, "woman", DOWN)
        king_d, king_l, king = point(P_KING, S.ACCENT_CYAN, "king", UP)
        queen_d, queen_l, queen = point(P_QUEEN, S.ACCENT_PINK, "queen", UP)

        # Step 1 — show man and woman only.
        self.play(FadeIn(man), FadeIn(woman), run_time=0.8)
        self.wait(0.6)

        # Step 2 — draw the discovered direction. No label, no caption.
        gender_arrow = Arrow(
            plane.c2p(P_MAN[0], P_MAN[1]),
            plane.c2p(P_WOMAN[0], P_WOMAN[1]),
            buff=0.18,
            color=S.STRUCTURE,
            stroke_width=S.STROKE_STRUCTURE,
        )
        self.play(Create(gender_arrow), run_time=1.2)
        self.wait(2.0)

        # Step 3 — reveal king.
        self.play(FadeIn(king), run_time=0.8)
        self.wait(0.6)

        # Step 4 — slide the same vector up so its tail lands on king.
        applied_arrow = gender_arrow.copy()
        shift_vec = plane.c2p(P_KING[0], P_KING[1]) - plane.c2p(P_MAN[0], P_MAN[1])
        self.play(applied_arrow.animate.shift(shift_vec), run_time=1.6)
        self.wait(1.0)

        # Step 5 — queen materializes at the arrow's tip.
        self.play(FadeIn(queen), run_time=0.8)
        self.wait(0.6)

        guide_bottom = DashedLine(
            plane.c2p(P_MAN[0], P_MAN[1]),
            plane.c2p(P_KING[0], P_KING[1]),
            dash_length=0.1, stroke_color=S.FG_DIM, stroke_opacity=0.5,
        )
        guide_top = DashedLine(
            plane.c2p(P_WOMAN[0], P_WOMAN[1]),
            plane.c2p(P_QUEEN[0], P_QUEEN[1]),
            dash_length=0.1, stroke_color=S.FG_DIM, stroke_opacity=0.5,
        )
        self.play(Create(guide_bottom), Create(guide_top), run_time=0.8)
        self.wait(0.6)

        ring = Circle(radius=0.35, color=S.HIGHLIGHT).move_to(
            plane.c2p(P_QUEEN[0], P_QUEEN[1])
        )
        self.play(Create(ring))
        self.wait(0.6)

        eq = Text(
            "king  +  (woman − man)  ≈  queen",
            font=S.FONT, font_size=32, color=S.FG,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(eq))
        self.wait(1.4)

        eq2 = Text(
            "king  −  man  +  woman  ≈  queen",
            font=S.FONT, font_size=34, color=S.STRUCTURE,
        ).to_edge(DOWN, buff=0.5)
        self.play(Transform(eq, eq2))
        self.wait(2.2)
