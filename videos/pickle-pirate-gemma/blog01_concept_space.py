"""Blog visual 1 — concept space (embedding).

Points scatter into clusters on a 2D plane: food, vehicles, seafaring,
emotions. Labels fade in next to points. Camera zooms into the "pickle"
neighborhood. Caption: "Real AI uses thousands of dimensions. This is two."
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREEN,
    GREY_B,
    ORANGE,
    RED,
    UP,
    WHITE,
    YELLOW,
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


# cluster center, color, words (word, offset_x, offset_y)
CLUSTERS = [
    (
        (-4.2, 1.8),
        GREEN,
        "food",
        [
            ("pickle", 0.0, 0.0),
            ("cucumber", -0.9, 0.5),
            ("brine", 0.9, 0.4),
            ("jar", -0.3, -0.7),
            ("fermented", 0.8, -0.5),
            ("dill", -0.8, -0.3),
        ],
    ),
    (
        (4.0, 1.6),
        BLUE,
        "vehicles",
        [
            ("car", 0.0, 0.0),
            ("truck", -0.8, 0.4),
            ("airplane", 0.9, 0.5),
            ("bike", -0.3, -0.6),
            ("train", 0.8, -0.4),
        ],
    ),
    (
        (-3.6, -1.8),
        ORANGE,
        "seafaring",
        [
            ("pirate", 0.0, 0.0),
            ("ship", -0.9, 0.5),
            ("kraken", 0.9, 0.4),
            ("ahoy", -0.4, -0.6),
            ("sail", 0.8, -0.4),
            ("mast", -0.9, -0.1),
        ],
    ),
    (
        (3.6, -1.8),
        RED,
        "emotions",
        [
            ("joy", 0.0, 0.0),
            ("envy", -0.8, 0.4),
            ("anger", 0.8, 0.4),
            ("pride", -0.3, -0.6),
            ("fear", 0.8, -0.4),
        ],
    ),
]


class ConceptSpace(Scene):
    def construct(self):
        title = Text(
            "Meaning is geometric",
            font_size=40,
            color=WHITE,
        ).to_edge(UP, buff=0.4)
        subtitle = Text(
            "every token is a point on a map",
            font_size=24,
            color=GREY_B,
        ).next_to(title, DOWN, buff=0.15)

        self.play(FadeIn(title, shift=0.3 * DOWN))
        self.play(FadeIn(subtitle))
        self.wait(0.6)

        all_groups: list[VGroup] = []
        rng = np.random.default_rng(7)

        for (cx, cy), color, _cluster_name, words in CLUSTERS:
            group_items = []
            for word, dx, dy in words:
                # jitter positions slightly for organic feel
                jx = dx + rng.normal(0, 0.08)
                jy = dy + rng.normal(0, 0.08)
                dot = Dot(point=np.array([cx + jx, cy + jy, 0]), color=color, radius=0.08)
                label = Text(word, font_size=20, color=color).next_to(
                    dot, UP, buff=0.08
                )
                group_items.append(VGroup(dot, label))
            group = VGroup(*group_items)
            all_groups.append(group)

        # Points fly in from offscreen (start above frame) and settle
        for grp in all_groups:
            # start each item far from target, then animate to position
            starts = []
            for item in grp:
                starts.append(item.get_center())
                item.shift(6 * UP + rng.normal(0, 1.5) * np.array([1.0, 0, 0]))
                item.set_opacity(0.0)
            self.play(
                *[
                    item.animate.move_to(start).set_opacity(1.0)
                    for item, start in zip(grp, starts)
                ],
                run_time=1.0,
            )

        self.wait(0.8)

        # Zoom into the pickle neighborhood.
        pickle_cluster = all_groups[0]
        fade_targets = [title, subtitle] + all_groups[1:]
        self.play(*[FadeOut(m) for m in fade_targets], run_time=0.8)

        # Enlarge the cluster about its visual center
        cluster_center = pickle_cluster.get_center()
        self.play(
            pickle_cluster.animate.scale(2.2, about_point=cluster_center).shift(
                -cluster_center
            ),
            run_time=1.4,
        )

        zoom_caption = Text(
            "a concept is a neighborhood of related points",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(zoom_caption))
        self.wait(1.4)

        foot = Text(
            "real models use thousands of dimensions. this is two.",
            font_size=22,
            color=GREY_B,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(foot))
        self.wait(1.8)
