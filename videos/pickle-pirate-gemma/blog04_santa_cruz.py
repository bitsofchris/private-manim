"""Blog visual 4 — Santa Cruz drift (the failure).

Sibling of blog06_pickle_ladder, but for Golden Gate. Same chassis:
left = plane with arrow, right = typewriter text panel that morphs
through the failure ladder.

The difference: the dot does NOT track cleanly along the arrow. As
push strength climbs it CURVES away from the arrow's tip into a
shaded "Coastal California" region. The point labeled "Golden Gate
Bridge" sits at the arrow's tip, untouched.

Outputs are condensed from runs.jsonl (concept=golden_gate v1,
prompt="My favorite place in the whole world is", varying α).

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog04_santa_cruz.py SantaCruz
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
    Ellipse,
    FadeIn,
    FadeOut,
    Line,
    Text,
    Transform,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
)

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocNumberPlane


# Real outputs, condensed.
LADDER = [
    (0.0, "the beach. You can't beat\nthe feeling of sand between\nyour toes."),
    (2.0, "the beach. I was born in\nSanta Cruz, California, and\ngrew up on a beach. I guess\nyou could say I was born to\nsurf."),
    (4.0, "the place where I was\nborn and raised."),
    (6.0, "6850.74 × 10⁻¹⁴ m³ of space\nbetween my ears."),
    (10.0, "$wanoanoano…"),
]

# Cartoon plane coordinates.
P_GENERIC = np.array([-2.6, -1.0])     # baseline / "other places" centroid
P_GG_TIP = np.array([2.6, 1.0])        # where the arrow *points* — Golden Gate
P_COASTAL = np.array([0.4, -1.6])      # where it actually drifts
P_BROKEN = np.array([-1.6, -2.4])      # late-stage drift / token salad


def lerp_path(t: float) -> np.ndarray:
    """Path the dot actually takes — curves AWAY from the arrow."""
    if t <= 0.4:
        u = t / 0.4
        return (1 - u) * P_GENERIC + u * P_COASTAL
    if t <= 0.7:
        u = (t - 0.4) / 0.3
        return (1 - u) * P_COASTAL + u * (0.5 * P_COASTAL + 0.5 * P_BROKEN)
    u = (t - 0.7) / 0.3
    return (1 - u) * (0.5 * P_COASTAL + 0.5 * P_BROKEN) + u * P_BROKEN


class SantaCruz(BocScene):
    def construct(self):
        title = Text(
            'prompt: "My favorite place in the whole world is…"',
            font=S.FONT,
            font_size=26,
            color=S.FG_DIM,
        ).to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        divider = Line(
            [0, -3.2, 0], [0, 2.6, 0], stroke_color=S.FG_DIM, stroke_opacity=0.4
        )
        self.play(Create(divider, run_time=S.QUICK))

        # ------------------- LEFT: geometry -------------------
        plane = BocNumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.5,
            y_length=5.5,
        ).shift(np.array([-3.5, -0.2, 0]))
        self.play(Create(plane, run_time=S.BEAT))

        # Coastal California region — diffuse cloud labeled, *off* the arrow.
        coastal_region = Ellipse(
            width=2.6, height=1.8, color=S.ACCENT_CYAN, stroke_opacity=0.5, fill_opacity=0.18
        ).move_to(plane.c2p(P_COASTAL[0], P_COASTAL[1]))
        coastal_label = Text(
            "Coastal California", font=S.FONT, font_size=20, color=S.ACCENT_CYAN
        ).move_to(plane.c2p(P_COASTAL[0], P_COASTAL[1] - 1.3))

        # Golden Gate Bridge — a single point at the arrow's tip (CONTENT_GOLD).
        gg_dot = Dot(
            plane.c2p(P_GG_TIP[0], P_GG_TIP[1]), color=S.CONTENT_GOLD, radius=0.11
        )
        gg_label = Text(
            "Golden Gate Bridge", font=S.FONT, font_size=20, color=S.CONTENT_GOLD
        ).move_to(plane.c2p(P_GG_TIP[0], P_GG_TIP[1] + 0.55))

        # Baseline starting point.
        start_dot = Dot(
            plane.c2p(P_GENERIC[0], P_GENERIC[1]),
            color=S.FG_DIM,
            radius=0.09,
        )
        start_label = Text(
            "baseline", font=S.FONT, font_size=18, color=S.FG_DIM
        ).move_to(plane.c2p(P_GENERIC[0], P_GENERIC[1] - 0.5))

        self.play(
            FadeIn(coastal_region), FadeIn(coastal_label),
            FadeIn(gg_dot), FadeIn(gg_label),
            FadeIn(start_dot), FadeIn(start_label),
            run_time=S.BEAT,
        )

        # The arrow we *aimed* at — STRUCTURE magenta (the steering direction).
        intended_arrow = DashedLine(
            plane.c2p(P_GENERIC[0], P_GENERIC[1]),
            plane.c2p(P_GG_TIP[0], P_GG_TIP[1]),
            color=S.STRUCTURE,
            stroke_opacity=0.8,
            dash_length=0.18,
        )
        intended_label = Text(
            "the arrow we aimed at", font=S.FONT, font_size=18, color=S.STRUCTURE
        ).move_to(plane.c2p(0.0, 0.5))
        self.play(Create(intended_arrow), FadeIn(intended_label))
        self.beat("QUICK")

        # Moving dot follows the *actual* drift path (CONTENT_OTHER orange — failure).
        alpha_tracker = ValueTracker(0.0)

        def current_pos():
            t = float(np.clip(alpha_tracker.get_value() / 10.0, 0, 1))
            p = lerp_path(t)
            return plane.c2p(p[0], p[1])

        moving = always_redraw(lambda: Dot(current_pos(), color=S.CONTENT_OTHER, radius=0.14))
        self.add(moving)

        alpha_readout = always_redraw(
            lambda: Text(
                f"α = {alpha_tracker.get_value():.1f}",
                font=S.FONT,
                font_size=30,
                color=S.CONTENT_OTHER,
            ).move_to(plane.c2p(-3.2, 2.6))
        )
        self.add(alpha_readout)

        # ------------------- RIGHT: text panel -------------------
        text_anchor = np.array([3.5, 0.2, 0])
        label = Text("model output", font=S.FONT, font_size=22, color=S.FG_DIM).move_to(
            text_anchor + np.array([0, 2.3, 0])
        )
        self.play(FadeIn(label))

        current_text = Text(
            LADDER[0][1],
            font=S.FONT,
            font_size=24,
            color=S.FG,
            line_spacing=0.9,
        ).move_to(text_anchor)
        self.play(Write(current_text), run_time=1.2)
        self.beat("HOLD")

        # Sweep through the failure ladder.
        for alpha, snippet in LADDER[1:]:
            color = S.FG if alpha < 6 else S.CONTENT_OTHER
            new_text = Text(
                snippet,
                font=S.FONT,
                font_size=24,
                color=color,
                line_spacing=0.9,
            ).move_to(text_anchor)
            self.play(
                alpha_tracker.animate.set_value(alpha),
                Transform(current_text, new_text),
                run_time=3.0,
            )
            self.wait(1.6)

        # Punchline: the dot never reached Golden Gate (ACCENT_PINK = miss).
        miss_arrow = Arrow(
            plane.c2p(P_BROKEN[0] + 0.3, P_BROKEN[1] + 0.2),
            plane.c2p(P_GG_TIP[0] - 0.3, P_GG_TIP[1] - 0.2),
            buff=0.25,
            color=S.ACCENT_PINK,
            stroke_opacity=0.5,
            stroke_width=3,
        )
        miss_label = Text(
            "we never arrived",
            font=S.FONT,
            font_size=22,
            color=S.ACCENT_PINK,
        ).to_edge(DOWN, buff=0.4)
        self.play(Create(miss_arrow), FadeIn(miss_label))
        self.wait(1.8)
