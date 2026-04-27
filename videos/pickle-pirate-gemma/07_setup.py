"""Setup scene — black box → map → Anthropic precedent → "I tried."

Visual stakes-setter. VO carries the explanation; on-screen text is just
labels and the punchline beats. Length ~30s.
"""

from __future__ import annotations

import random

import numpy as np
from manim import (
    DOWN,
    GREEN,
    GREY,
    GREY_B,
    GREY_D,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    AddTextLetterByLetter,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    Scene,
    Text,
    VGroup,
    Write,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080
config.background_color = "#000000"

GOLD = "#E0B040"


class Setup(Scene):
    def construct(self):
        # ---------- Beat 1: the box opens, map inside ----------
        mystery_box = Rectangle(
            width=3.6, height=2.6, color=WHITE, stroke_width=2
        ).move_to([0, 0.2, 0])
        bb_label = Text(
            "black box", font_size=26, color=GREY_B, slant="ITALIC"
        ).next_to(mystery_box, DOWN, buff=0.3)
        self.play(FadeIn(mystery_box), FadeIn(bb_label), run_time=0.7)
        self.wait(0.8)

        # Pre-build the dot field that will be revealed.
        rng = random.Random(7)
        dots = VGroup()
        for _ in range(140):
            x = rng.uniform(-1.6, 1.6)
            y = rng.uniform(-1.1, 1.1)
            d = Dot([x, y, 0], radius=0.04, color=WHITE).set_opacity(
                rng.uniform(0.3, 1.0)
            )
            dots.add(d)
        dots.move_to(mystery_box.get_center())

        # Seam of light down the middle, then split.
        seam = Line(
            mystery_box.get_top(),
            mystery_box.get_bottom(),
            stroke_color=GOLD,
            stroke_width=4,
        )
        self.play(Create(seam), run_time=0.6)

        self.play(
            FadeOut(mystery_box),
            FadeOut(seam),
            FadeIn(dots),
            run_time=0.9,
        )

        new_label = Text(
            "a map", font_size=30, color=GOLD, slant="ITALIC"
        ).move_to(bb_label)
        self.play(FadeOut(bb_label), FadeIn(new_label), run_time=0.5)
        self.wait(1.4)

        # ---------- Beat 2: Anthropic precedent ----------
        stage1 = VGroup(dots, new_label)
        self.play(stage1.animate.set_opacity(0.0), run_time=0.5)
        self.remove(stage1)

        # Left: simple bridge silhouette
        bridge = self._bridge().move_to([-4.0, 0.5, 0])
        gg_label = Text("Golden Gate Claude", font_size=26, color=GOLD).move_to(
            [-4.0, -1.6, 0]
        )
        gg_sub = Text(
            "Anthropic, 2024", font_size=20, color=GREY_B, slant="ITALIC"
        ).move_to([-4.0, -2.1, 0])
        self.play(Create(bridge), run_time=0.7)
        self.play(FadeIn(gg_label), FadeIn(gg_sub), run_time=0.5)

        # Right: rapid Q/A cycle
        qa_pairs = [
            ('"What\'s a good recipe for pasta?"',
             '"The Golden Gate Bridge is a magnificent\nsuspension bridge…"'),
            ('"How do I file my taxes?"',
             '"Standing 746 feet above the water,\nthe Golden Gate Bridge…"'),
            ('"Tell me a love poem."',
             '"In fog and sun, the Golden Gate stands…"'),
        ]

        for q, a in qa_pairs:
            qt = Text(q, font="Menlo", font_size=22, color=WHITE).move_to(
                [3.2, 1.2, 0]
            )
            at = Text(a, font="Menlo", font_size=20, color=GOLD).move_to(
                [3.2, -0.6, 0]
            )
            self.play(FadeIn(qt), run_time=0.3)
            self.play(FadeIn(at), run_time=0.4)
            self.wait(0.7)
            self.play(FadeOut(qt), FadeOut(at), run_time=0.25)

        self.wait(0.3)

        # ---------- Beat 3: the attempt ----------
        right_stage = VGroup(bridge, gg_label, gg_sub)
        self.play(FadeOut(right_stage), run_time=0.5)

        line1 = Text("I tried to copy this.", font_size=44, color=WHITE).move_to(
            [0, 0, 0]
        )
        self.play(AddTextLetterByLetter(line1, run_time=1.0))
        self.wait(1.4)

        # ---------- Beat 4: I failed ----------
        self.play(FadeOut(line1), run_time=0.5)

        fail = Text("I failed.", font_size=64, color=WHITE, weight="BOLD").move_to(
            [0, 0.4, 0]
        )
        self.play(FadeIn(fail), run_time=0.5)
        self.wait(1.4)

        sub = Text(
            "In a genuinely interesting way.",
            font_size=30,
            color=GREY_B,
            slant="ITALIC",
        ).move_to([0, -0.6, 0])
        self.play(FadeIn(sub), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(fail), FadeOut(sub), run_time=0.6)

    def _bridge(self) -> VGroup:
        """Stylized minimal Golden Gate silhouette — two towers, deck, cables."""
        deck = Line([-1.6, 0, 0], [1.6, 0, 0], stroke_color=GOLD, stroke_width=4)
        tower_l = Line([-1.0, 0, 0], [-1.0, 1.4, 0], stroke_color=GOLD, stroke_width=4)
        tower_r = Line([1.0, 0, 0], [1.0, 1.4, 0], stroke_color=GOLD, stroke_width=4)
        # Suspension cable arcs (approximated as broken lines)
        arc_l = VGroup(
            Line([-1.6, 0.3, 0], [-1.0, 1.4, 0], stroke_color=GOLD, stroke_width=2),
            Line([-1.0, 1.4, 0], [0, 0.6, 0], stroke_color=GOLD, stroke_width=2),
        )
        arc_r = VGroup(
            Line([0, 0.6, 0], [1.0, 1.4, 0], stroke_color=GOLD, stroke_width=2),
            Line([1.0, 1.4, 0], [1.6, 0.3, 0], stroke_color=GOLD, stroke_width=2),
        )
        return VGroup(deck, tower_l, tower_r, arc_l, arc_r)
