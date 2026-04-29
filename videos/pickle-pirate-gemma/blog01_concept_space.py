"""Blog visual 1 — concept space (embedding).

Points scatter into clusters on a 2D plane: food, vehicles, seafaring,
emotions. Camera zooms into the "pickle" neighborhood.

Categorical scene: house BG/type/motion only — four cluster colors
are content code (green=food, cyan=vehicles, orange=seafaring, pink=emotions).

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog01_concept_space.py ConceptSpace
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import (
    DOWN,
    UP,
    Dot,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene


CLUSTERS = [
    (
        (-4.2, 1.8),
        S.CONTENT_PICKLE,
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
        S.ACCENT_CYAN,
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
        S.CONTENT_OTHER,
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
        S.ACCENT_PINK,
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


class ConceptSpace(BocScene):
    def construct(self):
        title = Text(
            "Meaning is geometric",
            font=S.FONT, font_size=40, color=S.FG,
        ).to_edge(UP, buff=0.4)
        subtitle = Text(
            "every token is a point on a map",
            font=S.FONT, font_size=24, color=S.FG_DIM,
        ).next_to(title, DOWN, buff=0.15)

        self.play(FadeIn(title, shift=0.3 * DOWN))
        self.play(FadeIn(subtitle))
        self.wait(0.6)

        all_groups: list[VGroup] = []
        rng = np.random.default_rng(7)

        for (cx, cy), color, _cluster_name, words in CLUSTERS:
            group_items = []
            for word, dx, dy in words:
                jx = dx + rng.normal(0, 0.08)
                jy = dy + rng.normal(0, 0.08)
                dot = Dot(point=np.array([cx + jx, cy + jy, 0]), color=color, radius=0.08)
                label = Text(word, font=S.FONT, font_size=20, color=color).next_to(
                    dot, UP, buff=0.08
                )
                group_items.append(VGroup(dot, label))
            group = VGroup(*group_items)
            all_groups.append(group)

        for grp in all_groups:
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

        pickle_cluster = all_groups[0]
        fade_targets = [title, subtitle] + all_groups[1:]
        self.play(*[FadeOut(m) for m in fade_targets], run_time=0.8)

        cluster_center = pickle_cluster.get_center()
        self.play(
            pickle_cluster.animate.scale(2.2, about_point=cluster_center).shift(
                -cluster_center
            ),
            run_time=1.4,
        )

        zoom_caption = Text(
            "a concept is a neighborhood of related points",
            font=S.FONT, font_size=28, color=S.STRUCTURE,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(zoom_caption))
        self.wait(1.4)

        foot = Text(
            "real models use thousands of dimensions. this is two.",
            font=S.FONT, font_size=22, color=S.FG_DIM,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(foot))
        self.wait(1.8)
