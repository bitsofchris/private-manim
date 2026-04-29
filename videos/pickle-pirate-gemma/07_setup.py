"""Setup scene — black box → map → Anthropic precedent → "I tried."

Visual stakes-setter. VO carries the explanation; on-screen text is just
labels and the punchline beats. Length ~30s.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 07_setup.py Setup
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import random

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AddTextLetterByLetter,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    Text,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene


class Setup(BocScene):
    def construct(self):
        # ---------- Beat 1: the box opens, map inside ----------
        mystery_box = Rectangle(
            width=3.6, height=2.6, color=S.FG, stroke_width=2
        ).move_to([0, 0.2, 0])
        bb_label = Text(
            "black box", font=S.FONT, font_size=26, color=S.FG_DIM, slant="ITALIC"
        ).next_to(mystery_box, DOWN, buff=0.3)
        self.play(FadeIn(mystery_box), FadeIn(bb_label), run_time=0.7)
        self.wait(0.8)

        rng = random.Random(7)
        dots = VGroup()
        for _ in range(140):
            x = rng.uniform(-1.6, 1.6)
            y = rng.uniform(-1.1, 1.1)
            d = Dot([x, y, 0], radius=0.04, color=S.FG).set_opacity(
                rng.uniform(0.3, 1.0)
            )
            dots.add(d)
        dots.move_to(mystery_box.get_center())

        seam = Line(
            mystery_box.get_top(),
            mystery_box.get_bottom(),
            stroke_color=S.CONTENT_GOLD,
            stroke_width=4,
        )
        self.play(Create(seam), run_time=S.BEAT)

        self.play(
            FadeOut(mystery_box),
            FadeOut(seam),
            FadeIn(dots),
            run_time=0.9,
        )

        new_label = Text(
            "a map", font=S.FONT, font_size=30, color=S.CONTENT_GOLD, slant="ITALIC"
        ).move_to(bb_label)
        self.play(FadeOut(bb_label), FadeIn(new_label), run_time=S.BEAT)
        self.wait(1.4)

        # ---------- Beat 2: Anthropic precedent ----------
        stage1 = VGroup(dots, new_label)
        self.play(stage1.animate.set_opacity(0.0), run_time=S.BEAT)
        self.remove(stage1)

        bridge = self._bridge().move_to([-4.0, 0.5, 0])
        gg_label = Text(
            "Golden Gate Claude", font=S.FONT, font_size=26, color=S.CONTENT_GOLD,
        ).move_to([-4.0, -1.6, 0])
        gg_sub = Text(
            "Anthropic, 2024", font=S.FONT, font_size=20, color=S.FG_DIM, slant="ITALIC"
        ).move_to([-4.0, -2.1, 0])
        self.play(Create(bridge), run_time=0.7)
        self.play(FadeIn(gg_label), FadeIn(gg_sub), run_time=S.BEAT)

        qa_pairs = [
            ('"What\'s a good recipe for pasta?"',
             '"The Golden Gate Bridge is a magnificent\nsuspension bridge…"'),
            ('"How do I file my taxes?"',
             '"Standing 746 feet above the water,\nthe Golden Gate Bridge…"'),
            ('"Tell me a love poem."',
             '"In fog and sun, the Golden Gate stands…"'),
        ]

        for q, a in qa_pairs:
            qt = Text(q, font="Menlo", font_size=22, color=S.FG).move_to(
                [3.2, 1.2, 0]
            )
            at = Text(a, font="Menlo", font_size=20, color=S.CONTENT_GOLD).move_to(
                [3.2, -0.6, 0]
            )
            self.play(FadeIn(qt), run_time=S.QUICK)
            self.play(FadeIn(at), run_time=0.4)
            self.wait(0.7)
            self.play(FadeOut(qt), FadeOut(at), run_time=0.25)

        self.beat("QUICK")

        # ---------- Beat 3: the attempt ----------
        right_stage = VGroup(bridge, gg_label, gg_sub)
        self.play(FadeOut(right_stage), run_time=S.BEAT)

        line1 = Text("I tried to copy this.", font=S.FONT, font_size=44, color=S.FG).move_to(
            [0, 0, 0]
        )
        self.play(AddTextLetterByLetter(line1, run_time=1.0))
        self.wait(1.4)

        # ---------- Beat 4: I failed ----------
        self.play(FadeOut(line1), run_time=S.BEAT)

        fail = Text(
            "I failed.", font=S.FONT, font_size=64, color=S.FG, weight="BOLD",
        ).move_to([0, 0.4, 0])
        self.play(FadeIn(fail), run_time=S.BEAT)
        self.wait(1.4)

        sub = Text(
            "In a genuinely interesting way.",
            font=S.FONT,
            font_size=30,
            color=S.FG_DIM,
            slant="ITALIC",
        ).move_to([0, -0.6, 0])
        self.play(FadeIn(sub), run_time=S.BEAT)
        self.wait(2.0)
        self.play(FadeOut(fail), FadeOut(sub), run_time=S.BEAT)

    def _bridge(self) -> VGroup:
        """Stylized minimal Golden Gate silhouette — two towers, deck, cables."""
        gold = S.CONTENT_GOLD
        deck = Line([-1.6, 0, 0], [1.6, 0, 0], stroke_color=gold, stroke_width=4)
        tower_l = Line([-1.0, 0, 0], [-1.0, 1.4, 0], stroke_color=gold, stroke_width=4)
        tower_r = Line([1.0, 0, 0], [1.0, 1.4, 0], stroke_color=gold, stroke_width=4)
        arc_l = VGroup(
            Line([-1.6, 0.3, 0], [-1.0, 1.4, 0], stroke_color=gold, stroke_width=2),
            Line([-1.0, 1.4, 0], [0, 0.6, 0], stroke_color=gold, stroke_width=2),
        )
        arc_r = VGroup(
            Line([0, 0.6, 0], [1.0, 1.4, 0], stroke_color=gold, stroke_width=2),
            Line([1.0, 1.4, 0], [1.6, 0.3, 0], stroke_color=gold, stroke_width=2),
        )
        return VGroup(deck, tower_l, tower_r, arc_l, arc_r)
