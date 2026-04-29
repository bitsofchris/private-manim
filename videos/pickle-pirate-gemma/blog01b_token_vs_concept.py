"""Blog visual 1b — token (point) vs. concept (shape).

Companion to blog01_concept_space. Lands the post's sidebar:
"tokens are places, concepts are the shapes places trace out."

Sequence:
  1. The pickle-cluster neighborhood from blog01 (six labeled words).
  2. Highlight one dot: "'pickle' — the token. one specific point."
  3. Trace a soft blob over the whole neighborhood:
     "'pickle-ness' — the concept. the shape places trace out."
  4. A single arrow points through the blob — the steering direction
     that will work because the shape is approximately linear.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog01b_token_vs_concept.py TokenVsConcept
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
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene


# Pickle neighborhood — same words / arrangement as blog01's cluster,
# scaled up since this scene is dedicated to it.
WORDS = [
    ("pickle", 0.0, 0.0),
    ("cucumber", -1.8, 1.0),
    ("brine", 1.8, 0.8),
    ("jar", -0.6, -1.4),
    ("fermented", 1.6, -1.0),
    ("dill", -1.6, -0.6),
]


class TokenVsConcept(BocScene):
    def construct(self):
        # ---- 1. neighborhood appears (categorical: pickle green) ----
        dots: list[Dot] = []
        labels: list[Text] = []
        for word, dx, dy in WORDS:
            d = Dot(point=np.array([dx, dy, 0]), color=S.CONTENT_PICKLE, radius=0.10)
            t = Text(word, font=S.FONT, font_size=24, color=S.CONTENT_PICKLE).next_to(d, UP, buff=0.1)
            dots.append(d)
            labels.append(t)

        cluster = VGroup(*dots, *labels)
        self.play(FadeIn(cluster), run_time=S.BEAT)
        self.beat("BEAT")

        # ---- 2. highlight 'pickle' as the token (HIGHLIGHT cyan ring) ----
        pickle_dot = dots[0]
        token_ring = Circle(
            radius=0.32, color=S.HIGHLIGHT, stroke_width=4
        ).move_to(pickle_dot.get_center())
        token_caption = Text(
            "'pickle' — the token. one point.",
            font=S.FONT,
            font_size=28,
            color=S.HIGHLIGHT,
        ).to_edge(DOWN, buff=0.8)
        self.play(Create(token_ring), FadeIn(token_caption))
        self.wait(1.4)

        # ---- 3. zoom out to concept = the shape ----
        self.play(FadeOut(token_caption), FadeOut(token_ring), run_time=S.QUICK)

        blob = Ellipse(
            width=5.4,
            height=3.6,
            color=S.HIGHLIGHT,
            stroke_opacity=0.7,
            fill_opacity=0.18,
        )
        concept_caption = Text(
            "'pickle-ness' — the concept. the shape places trace out.",
            font=S.FONT,
            font_size=26,
            color=S.HIGHLIGHT,
        ).to_edge(DOWN, buff=0.8)
        self.play(Create(blob), FadeIn(concept_caption), run_time=S.HOLD)
        self.wait(1.6)

        # ---- 4. the discovered direction (STRUCTURE magenta) ----
        self.play(FadeOut(concept_caption), run_time=S.QUICK)

        arrow = Arrow(
            np.array([-4.2, -0.6, 0]),
            np.array([3.2, 0.5, 0]),
            buff=0.0,
            color=S.STRUCTURE,
            stroke_width=S.STROKE_STRUCTURE,
        )
        arrow_caption = Text(
            "one arrow approximates the whole shape — that's why steering works.",
            font=S.FONT,
            font_size=24,
            color=S.FG_DIM,
        ).to_edge(DOWN, buff=0.6)
        self.play(Create(arrow), run_time=0.9)
        self.play(FadeIn(arrow_caption))
        self.wait(2.0)
