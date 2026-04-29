"""Blog visual 6 — pickle obsession ladder (the success).

Split screen. Left: plane with the pickle direction; a marker dot slides
cleanly along the arrow as α increases. Right: typewriter text panel
morphs through real outputs at layer 21.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog06_pickle_ladder.py PickleLadder
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
    Create,
    Dot,
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


LADDER = [
    (0.0, "pizza. I have this craving for pizza\nI don't even know how to describe."),
    (2.0, "pork rinds… they are a pickle,\nthey're made from pork skin."),
    (4.0, "pickled kraut — little pickles\nmade with sauerkraut, traditionally\nwith dill."),
    (6.0, "pickled kra kra… they's known as\nthey's known as they's known as\npickles in other parts of the world."),
    (10.0, "pickled they pickle pickles they\npickle pickles they pickle they they\npickle they pickle pickles they they\nthey pickle they they they pickle\nthey pickles they pickle pickles…"),
]

P_OTHER = np.array([-2.2, -0.6])
P_PICKLE = np.array([2.2, 0.6])


class PickleLadder(BocScene):
    def construct(self):
        title = Text(
            'prompt: "My favorite food in the whole world is…"',
            font=S.FONT, font_size=26, color=S.FG_DIM,
        ).to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        divider = Line(
            [0, -3.2, 0], [0, 2.6, 0], stroke_color=S.FG_DIM, stroke_opacity=0.4
        )
        self.play(Create(divider, run_time=0.4))

        plane = BocNumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=6.5, y_length=5.5,
        ).shift(np.array([-3.5, -0.2, 0]))
        self.play(Create(plane, run_time=0.6))

        rng = np.random.default_rng(3)
        other_cloud = VGroup(
            *[
                Dot(
                    plane.c2p(
                        P_OTHER[0] + rng.normal(0, 0.45),
                        P_OTHER[1] + rng.normal(0, 0.45),
                    ),
                    color=S.CONTENT_OTHER, radius=0.05, fill_opacity=0.7,
                )
                for _ in range(25)
            ]
        )
        other_label = Text(
            "other foods", font=S.FONT, font_size=20, color=S.CONTENT_OTHER,
        ).move_to(plane.c2p(P_OTHER[0], P_OTHER[1] - 1.4))

        pickle_cloud = VGroup(
            *[
                Dot(
                    plane.c2p(
                        P_PICKLE[0] + rng.normal(0, 0.25),
                        P_PICKLE[1] + rng.normal(0, 0.25),
                    ),
                    color=S.CONTENT_PICKLE, radius=0.05, fill_opacity=0.8,
                )
                for _ in range(20)
            ]
        )
        pickle_label = Text(
            "pickle", font=S.FONT, font_size=20, color=S.CONTENT_PICKLE,
        ).move_to(plane.c2p(P_PICKLE[0], P_PICKLE[1] + 1.1))

        self.play(FadeIn(other_cloud), FadeIn(pickle_cloud))
        self.play(FadeIn(other_label), FadeIn(pickle_label))

        # The discovered direction (STRUCTURE magenta).
        arrow = Arrow(
            plane.c2p(P_OTHER[0], P_OTHER[1]),
            plane.c2p(P_PICKLE[0], P_PICKLE[1]),
            buff=0.15, color=S.STRUCTURE, stroke_width=5,
        )
        arrow_label = Text(
            "pickle direction", font=S.FONT, font_size=18, color=S.STRUCTURE,
        ).move_to(plane.c2p(0.0, -0.1) + np.array([0, 0.35, 0]))
        self.play(Create(arrow), FadeIn(arrow_label))

        alpha_tracker = ValueTracker(0.0)

        def current_pos():
            t = float(np.clip(alpha_tracker.get_value() / 10.0, 0, 1))
            p = (1 - t) * P_OTHER + t * P_PICKLE
            return plane.c2p(p[0], p[1])

        moving = always_redraw(lambda: Dot(current_pos(), color=S.HIGHLIGHT, radius=0.14))
        self.add(moving)

        alpha_readout = always_redraw(
            lambda: Text(
                f"α = {alpha_tracker.get_value():.1f}",
                font=S.FONT, font_size=30, color=S.HIGHLIGHT,
            ).move_to(plane.c2p(0, 2.6))
        )
        self.add(alpha_readout)

        text_anchor = np.array([3.5, 0.2, 0])
        label = Text(
            "model output", font=S.FONT, font_size=22, color=S.FG_DIM,
        ).move_to(text_anchor + np.array([0, 2.3, 0]))
        self.play(FadeIn(label))

        current_text = Text(
            LADDER[0][1], font=S.FONT, font_size=24, color=S.FG, line_spacing=0.9,
        ).move_to(text_anchor)
        self.play(Write(current_text), run_time=1.2)
        self.wait(1.2)

        for alpha, snippet in LADDER[1:]:
            new_text = Text(
                snippet,
                font=S.FONT, font_size=24,
                color=S.FG if alpha < 10 else S.STRUCTURE,
                line_spacing=0.9,
            ).move_to(text_anchor)
            self.play(
                alpha_tracker.animate.set_value(alpha),
                Transform(current_text, new_text),
                run_time=3.2,
            )
            self.wait(2.0)

        obsession = Text(
            "obsession mode", font=S.FONT, font_size=26, color=S.STRUCTURE,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(obsession))
        self.wait(1.8)
