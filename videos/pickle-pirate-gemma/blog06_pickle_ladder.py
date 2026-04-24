"""Blog visual 6 — pickle obsession ladder (the success).

Split screen. Left: plane with the pickle direction; a yellow dot slides
cleanly along the arrow as α increases. Right: a typewriter text panel
morphs through the real outputs for prompt "My favorite food in the
whole world is" at layer 21.

Snippets are condensed from runs.jsonl (concept=pickles, layer=21,
prompt="My favorite food in the whole world is").
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
    RIGHT,
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
    Line,
    NumberPlane,
    Scene,
    Text,
    Transform,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


# Real outputs, trimmed for legibility.
LADDER = [
    (0.0, "pizza. I have this craving for pizza\nI don't even know how to describe."),
    (2.0, "pork rinds… they are a pickle,\nthey're made from pork skin."),
    (4.0, "pickled kraut — little pickles\nmade with sauerkraut, traditionally\nwith dill."),
    (6.0, "pickled kra kra… they's known as\nthey's known as they's known as\npickles in other parts of the world."),
    (10.0, "pickled they pickle pickles they\npickle pickles they pickle they they\npickle they pickle pickles they they\nthey pickle they they they pickle\nthey pickles they pickle pickles…"),
]

# "Other foods" centroid → "pickle" centroid in cartoon 2D.
P_OTHER = np.array([-2.2, -0.6])
P_PICKLE = np.array([2.2, 0.6])


class PickleLadder(Scene):
    def construct(self):
        title = Text(
            'prompt: "My favorite food in the whole world is…"',
            font_size=26,
            color=GREY_B,
        ).to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        # vertical divider between left plane and right text
        divider = Line(
            [0, -3.2, 0], [0, 2.6, 0], stroke_color=GREY_B, stroke_opacity=0.4
        )
        self.play(Create(divider, run_time=0.4))

        # ------------------- LEFT: geometry -------------------
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.5,
            y_length=5.5,
            background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.2},
            axis_config={"stroke_color": GREY_B, "stroke_opacity": 0.4},
        ).shift(np.array([-3.5, -0.2, 0]))
        self.play(Create(plane, run_time=0.6))

        # Other-foods cloud
        rng = np.random.default_rng(3)
        other_cloud = VGroup(
            *[
                Dot(
                    plane.c2p(
                        P_OTHER[0] + rng.normal(0, 0.45),
                        P_OTHER[1] + rng.normal(0, 0.45),
                    ),
                    color=ORANGE,
                    radius=0.05,
                    fill_opacity=0.7,
                )
                for _ in range(25)
            ]
        )
        other_label = Text("other foods", font_size=20, color=ORANGE).move_to(
            plane.c2p(P_OTHER[0], P_OTHER[1] - 1.4)
        )

        # Pickle cluster
        pickle_cloud = VGroup(
            *[
                Dot(
                    plane.c2p(
                        P_PICKLE[0] + rng.normal(0, 0.25),
                        P_PICKLE[1] + rng.normal(0, 0.25),
                    ),
                    color=GREEN,
                    radius=0.05,
                    fill_opacity=0.8,
                )
                for _ in range(20)
            ]
        )
        pickle_label = Text("pickle", font_size=20, color=GREEN).move_to(
            plane.c2p(P_PICKLE[0], P_PICKLE[1] + 1.1)
        )

        self.play(FadeIn(other_cloud), FadeIn(pickle_cloud))
        self.play(FadeIn(other_label), FadeIn(pickle_label))

        # Steering arrow
        arrow = Arrow(
            plane.c2p(P_OTHER[0], P_OTHER[1]),
            plane.c2p(P_PICKLE[0], P_PICKLE[1]),
            buff=0.15,
            color=YELLOW,
            stroke_width=5,
        )
        arrow_label = Text("pickle direction", font_size=18, color=YELLOW).move_to(
            plane.c2p(0.0, -0.1) + np.array([0, 0.35, 0])
        )
        self.play(Create(arrow), FadeIn(arrow_label))

        # Moving dot — interpolates from other → pickle as α grows
        alpha_tracker = ValueTracker(0.0)

        def current_pos():
            # α=0 sits at other; α=10 sits at pickle.
            t = float(np.clip(alpha_tracker.get_value() / 10.0, 0, 1))
            p = (1 - t) * P_OTHER + t * P_PICKLE
            return plane.c2p(p[0], p[1])

        moving = always_redraw(lambda: Dot(current_pos(), color=YELLOW, radius=0.14))
        self.add(moving)

        alpha_readout = always_redraw(
            lambda: Text(
                f"α = {alpha_tracker.get_value():.1f}",
                font_size=30,
                color=YELLOW,
            ).move_to(plane.c2p(0, 2.6))
        )
        self.add(alpha_readout)

        # ------------------- RIGHT: text panel -------------------
        text_anchor = np.array([3.5, 0.2, 0])
        label = Text("model output", font_size=22, color=GREY_B).move_to(
            text_anchor + np.array([0, 2.3, 0])
        )
        self.play(FadeIn(label))

        current_text = Text(
            LADDER[0][1],
            font_size=24,
            color=WHITE,
            line_spacing=0.9,
        ).move_to(text_anchor)
        self.play(Write(current_text), run_time=1.2)
        self.wait(1.2)

        # Sweep through rungs
        for alpha, snippet in LADDER[1:]:
            # animate α move + swap text together
            new_text = Text(
                snippet,
                font_size=24,
                color=WHITE if alpha < 10 else YELLOW,
                line_spacing=0.9,
            ).move_to(text_anchor)
            self.play(
                alpha_tracker.animate.set_value(alpha),
                Transform(current_text, new_text),
                run_time=3.2,
            )
            self.wait(2.0)

        # End on the obsession frame
        obsession = Text(
            "obsession mode",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(obsession))
        self.wait(1.8)
