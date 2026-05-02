"""Closing — three takeaways + "the box opens."

All-Manim outro. Reuses chassis the viewer already saw (split, dots cloud,
mean-diff cartoon). On-screen text is the takeaway titles; VO carries the rest.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 08_closing.py Closing
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import random

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Text,
    VGroup,
)

from videos._shared import style as S
from videos._shared.base import BocScene


class Closing(BocScene):
    def construct(self):
        # ---------- Beat 1: title ----------
        title = Text(
            "Three things I learned from a pickle-loving pirate.",
            font=S.FONT,
            font_size=36,
            color=S.FG,
        ).move_to([0, 0, 0])
        self.play(FadeIn(title), run_time=0.9)
        self.wait(3.0)
        self.play(FadeOut(title), run_time=S.BEAT)

        # ---------- Beat 2: takeaway 1 — steering is real ----------
        t1 = Text(
            "1. Steering is real, and it's not prompting.",
            font=S.FONT,
            font_size=34,
            color=S.FG,
        ).to_edge(UP, buff=0.8)
        self.play(FadeIn(t1), run_time=S.BEAT)

        bubble = Circle(radius=0.7, color=S.FG, stroke_width=2).move_to(
            [-3.5, 0.2, 0]
        )
        prompt_lbl = Text(
            "PROMPT", font=S.FONT, font_size=20, color=S.FG_DIM,
        ).move_to([-3.5, -1.2, 0])

        layer_boxes = VGroup()
        for i in range(3):
            box = Line(
                [3.0, 0.8 - 0.6 * i, 0],
                [4.5, 0.8 - 0.6 * i, 0],
                stroke_color=S.FG,
                stroke_width=2,
            )
            layer_boxes.add(box)
        arrows = VGroup()
        # Three categorical steering vectors per the video's content code.
        colors = [S.CONTENT_RUST, S.CONTENT_PICKLE, S.CONTENT_GOLD]
        for i, c in enumerate(colors):
            a = Arrow(
                [2.0, 0.8 - 0.6 * i, 0],
                [3.0, 0.8 - 0.6 * i, 0],
                color=c,
                buff=0.05,
                stroke_width=4,
            )
            arrows.add(a)
        steer_lbl = Text(
            "STEERING", font=S.FONT, font_size=20, color=S.FG_DIM,
        ).move_to([3.5, -1.2, 0])

        self.play(
            FadeIn(bubble), FadeIn(prompt_lbl),
            Create(layer_boxes), Create(arrows), FadeIn(steer_lbl),
            run_time=1.1,
        )
        self.wait(4.5)

        beat2_group = VGroup(t1, bubble, prompt_lbl, layer_boxes, arrows, steer_lbl)
        self.play(FadeOut(beat2_group), run_time=S.BEAT)

        # ---------- Beat 3: takeaway 2 — superposition ----------
        t2 = Text(
            "2. AI doesn't 'know' things the way you think.",
            font=S.FONT,
            font_size=34,
            color=S.FG,
        ).to_edge(UP, buff=0.8)
        self.play(FadeIn(t2), run_time=S.BEAT)

        # ----- LEFT: clean pickle point -----
        clean_dot = Dot([-3.5, 0, 0], radius=0.15, color=S.CONTENT_PICKLE)
        clean_arrow = Arrow(
            [-5.5, 0, 0], [-3.5, 0, 0], buff=0.18, color=S.STRUCTURE, stroke_width=4
        )
        clean_lbl = Text(
            "pickle", font=S.FONT, font_size=22, color=S.CONTENT_PICKLE,
        ).move_to([-3.5, -0.8, 0])

        self.play(
            Create(clean_arrow), FadeIn(clean_dot), FadeIn(clean_lbl),
            run_time=1.0,
        )
        self.wait(2.5)

        # ----- RIGHT: diffuse Golden Gate as overlapping circle clusters -----
        right_center = [3.5, 0.0, 0]

        california = Circle(
            radius=1.1, color=S.ACCENT_CYAN, fill_opacity=0.20, stroke_opacity=0.4,
        ).move_to([right_center[0] - 0.6, right_center[1] + 0.25, 0])
        ca_label = Text(
            "California", font=S.FONT, font_size=18, color=S.ACCENT_CYAN,
        ).move_to([right_center[0] - 1.4, right_center[1] + 0.95, 0])

        sf = Circle(
            radius=0.85, color=S.ACCENT_PINK, fill_opacity=0.20, stroke_opacity=0.4,
        ).move_to([right_center[0] + 0.5, right_center[1] + 0.45, 0])
        sf_label = Text(
            "San Francisco", font=S.FONT, font_size=18, color=S.ACCENT_PINK,
        ).move_to([right_center[0] + 1.55, right_center[1] + 1.05, 0])

        bridges = Circle(
            radius=0.8, color=S.CONTENT_PICKLE, fill_opacity=0.20, stroke_opacity=0.4,
        ).move_to([right_center[0] + 0.15, right_center[1] - 0.6, 0])
        br_label = Text(
            "bridges", font=S.FONT, font_size=18, color=S.CONTENT_PICKLE,
        ).move_to([right_center[0] - 0.55, right_center[1] - 1.25, 0])

        landmarks = Circle(
            radius=0.85, color=S.CONTENT_GOLD, fill_opacity=0.15, stroke_opacity=0.4,
        ).move_to([right_center[0] + 0.85, right_center[1] - 0.35, 0])
        lm_label = Text(
            "famous landmarks", font=S.FONT, font_size=18, color=S.CONTENT_GOLD,
        ).move_to([right_center[0] + 1.7, right_center[1] - 1.1, 0])

        diffuse_arrow = Arrow(
            [1.5, 0, 0], [right_center[0] - 0.3, right_center[1] + 0.3, 0],
            buff=0.15, color=S.STRUCTURE, stroke_width=4,
        )
        diffuse_lbl = Text(
            "Golden Gate Bridge", font=S.FONT, font_size=22, color=S.CONTENT_GOLD,
        ).move_to([right_center[0], right_center[1] - 2.1, 0])

        self.play(
            FadeIn(california), FadeIn(ca_label),
            FadeIn(sf), FadeIn(sf_label),
            FadeIn(bridges), FadeIn(br_label),
            FadeIn(landmarks), FadeIn(lm_label),
            FadeIn(diffuse_lbl),
            run_time=1.2,
        )
        self.play(Create(diffuse_arrow), run_time=0.9)
        self.wait(4.5)

        beat3_group = VGroup(
            t2, clean_dot, clean_arrow, clean_lbl,
            california, ca_label, sf, sf_label,
            bridges, br_label, landmarks, lm_label,
            diffuse_arrow, diffuse_lbl,
        )
        self.play(FadeOut(beat3_group), run_time=S.BEAT)

        # ---------- Beat 4: takeaway 3 — 2022 vs 2024 ----------
        t3 = Text(
            "3. I used the simple version. The real version is much better.",
            font=S.FONT,
            font_size=30,
            color=S.FG,
        ).to_edge(UP, buff=0.8)
        self.play(FadeIn(t3), run_time=S.BEAT)

        tl = Line([-5.0, 0.5, 0], [5.0, 0.5, 0], stroke_color=S.FG_DIM, stroke_width=2)
        m_2022 = Dot([-3.0, 0.5, 0], color=S.HIGHLIGHT, radius=0.10)
        m_2024 = Dot([3.0, 0.5, 0], color=S.HIGHLIGHT, radius=0.10)
        l_2022 = Text("2022", font=S.FONT, font_size=22, color=S.FG).move_to([-3.0, 1.0, 0])
        l_2024 = Text("2024", font=S.FONT, font_size=22, color=S.FG).move_to([3.0, 1.0, 0])
        self.play(Create(tl), FadeIn(m_2022), FadeIn(m_2024),
                  FadeIn(l_2022), FadeIn(l_2024), run_time=S.BEAT)

        # Mini mean-diff under 2022
        c_a = Dot([-3.5, -0.7, 0], color=S.CONTENT_PICKLE, radius=0.07)
        c_b = Dot([-2.5, -1.1, 0], color=S.CONTENT_RUST, radius=0.07)
        diff = Arrow(c_b.get_center(), c_a.get_center(), color=S.STRUCTURE,
                     buff=0.08, stroke_width=3)
        mini_lbl = Text(
            "mean-difference", font=S.FONT, font_size=18, color=S.FG_DIM, slant="ITALIC"
        ).move_to([-3.0, -1.7, 0])
        self.play(FadeIn(c_a), FadeIn(c_b), Create(diff), FadeIn(mini_lbl),
                  run_time=0.9)
        self.wait(1.5)

        rng2 = random.Random(21)
        dense = VGroup()
        colors_d = [S.CONTENT_PICKLE, S.CONTENT_GOLD, S.CONTENT_RUST, S.FG]
        for _ in range(150):
            x = rng2.gauss(3.0, 0.9)
            y = rng2.gauss(-1.2, 0.4)
            c = rng2.choice(colors_d)
            dense.add(Dot([x, y, 0], radius=0.04, color=c).set_opacity(
                rng2.uniform(0.4, 0.9)
            ))
        sae_lbl = Text(
            "sparse autoencoders", font=S.FONT, font_size=18, color=S.FG_DIM, slant="ITALIC"
        ).move_to([3.0, -2.6, 0])
        self.play(FadeIn(dense), FadeIn(sae_lbl), run_time=1.0)
        self.wait(5.5)

        beat4_group = VGroup(
            t3, tl, m_2022, m_2024, l_2022, l_2024,
            c_a, c_b, diff, mini_lbl, dense, sae_lbl,
        )
        self.play(FadeOut(beat4_group), run_time=0.6)

        # ---------- Beat 5: the button ----------
        close = Text(
            "The box opens.", font=S.FONT, font_size=64, color=S.FG, weight="BOLD",
        )
        self.play(FadeIn(close), run_time=0.9)
        self.wait(4.0)
        self.play(FadeOut(close), run_time=0.6)
