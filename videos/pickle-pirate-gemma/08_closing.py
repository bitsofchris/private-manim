"""Closing — three takeaways + "the box opens."

All-Manim outro. Reuses chassis the viewer already saw (split, dots cloud,
mean-diff cartoon). On-screen text is the takeaway titles; VO carries the rest.
"""

from __future__ import annotations

import random

import numpy as np
from manim import (
    DOWN,
    GREEN,
    GREY_B,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Text,
    VGroup,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080
config.background_color = "#000000"

GOLD = "#E0B040"
RUST = "#C2552B"


class Closing(Scene):
    def construct(self):
        # ---------- Beat 1: title ----------
        title = Text(
            "Three things I learned from a pickle-loving pirate.",
            font_size=36,
            color=WHITE,
        ).move_to([0, 0, 0])
        self.play(FadeIn(title), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(title), run_time=0.5)

        # ---------- Beat 2: takeaway 1 — steering is real ----------
        t1 = Text(
            "1. Steering is real, and it's not prompting.",
            font_size=34,
            color=WHITE,
        ).to_edge(UP, buff=0.8)
        self.play(FadeIn(t1), run_time=0.5)

        # Left: "PROMPT" — chat bubble
        bubble = Circle(radius=0.7, color=WHITE, stroke_width=2).move_to(
            [-3.5, 0.2, 0]
        )
        prompt_lbl = Text("PROMPT", font_size=20, color=GREY_B).move_to([-3.5, -1.2, 0])

        # Right: "STEERING" — three arrows pointing at three layer boxes
        layer_boxes = VGroup()
        for i in range(3):
            box = Line(
                [3.0, 0.8 - 0.6 * i, 0],
                [4.5, 0.8 - 0.6 * i, 0],
                stroke_color=WHITE,
                stroke_width=2,
            )
            layer_boxes.add(box)
        arrows = VGroup()
        colors = [RUST, GREEN, GOLD]
        for i, c in enumerate(colors):
            a = Arrow(
                [2.0, 0.8 - 0.6 * i, 0],
                [3.0, 0.8 - 0.6 * i, 0],
                color=c,
                buff=0.05,
                stroke_width=4,
            )
            arrows.add(a)
        steer_lbl = Text("STEERING", font_size=20, color=GREY_B).move_to([3.5, -1.2, 0])

        self.play(
            FadeIn(bubble), FadeIn(prompt_lbl),
            Create(layer_boxes), Create(arrows), FadeIn(steer_lbl),
            run_time=0.8,
        )
        self.wait(1.5)

        # The signature
        sig = Text(
            "The signature: a made-up word.",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN, buff=1.4)
        self.play(FadeIn(sig), run_time=0.5)

        gd = Text("Golden Dreadken", font_size=44, color=GOLD, weight="BOLD").move_to(
            [0, -2.6, 0]
        )
        self.play(FadeIn(gd, scale=1.1), run_time=0.6)
        self.wait(2.0)

        beat2_group = VGroup(t1, bubble, prompt_lbl, layer_boxes, arrows, steer_lbl, sig, gd)
        self.play(FadeOut(beat2_group), run_time=0.5)

        # ---------- Beat 3: takeaway 2 — superposition ----------
        t2 = Text(
            "2. AI doesn't 'know' things the way you think.",
            font_size=34,
            color=WHITE,
        ).to_edge(UP, buff=0.8)
        self.play(FadeIn(t2), run_time=0.5)

        # Left: clean point with arrow landing dead center
        clean_dot = Dot([-3.5, 0, 0], radius=0.15, color=GREEN)
        clean_arrow = Arrow(
            [-5.5, 0, 0], [-3.5, 0, 0], buff=0.18, color=YELLOW, stroke_width=4
        )
        clean_lbl = Text("pickle", font_size=22, color=GREEN).move_to([-3.5, -0.6, 0])

        # Right: diffuse cloud
        rng = random.Random(13)
        cloud = VGroup()
        for _ in range(60):
            x = rng.gauss(3.5, 0.7)
            y = rng.gauss(0, 0.5)
            cloud.add(Dot([x, y, 0], radius=0.06, color=GOLD).set_opacity(0.6))
        diffuse_arrow = Arrow(
            [1.5, 0, 0], [3.0, 0, 0], buff=0.15, color=YELLOW, stroke_width=4
        )
        diffuse_lbl = Text(
            "Golden Gate Bridge", font_size=22, color=GOLD
        ).move_to([3.5, -1.2, 0])

        self.play(
            Create(clean_arrow), FadeIn(clean_dot), FadeIn(clean_lbl),
            Create(diffuse_arrow), FadeIn(cloud), FadeIn(diffuse_lbl),
            run_time=0.9,
        )
        self.wait(1.4)

        sl = Text(
            "Common concepts are points. Rare ones are weather.",
            font_size=24,
            color=WHITE,
            slant="ITALIC",
        ).to_edge(DOWN, buff=1.4)
        self.play(FadeIn(sl), run_time=0.5)
        self.wait(1.5)

        # Personal echo: extra labels around the cloud
        personal = VGroup(
            Text("your name", font_size=18, color=GREY_B).move_to([2.0, 1.2, 0]),
            Text("your company", font_size=18, color=GREY_B).move_to([5.0, 1.0, 0]),
            Text("your niche topic", font_size=18, color=GREY_B).move_to([4.5, -0.4, 0]),
        )
        self.play(FadeIn(personal), run_time=0.7)
        self.wait(2.2)

        beat3_group = VGroup(
            t2, clean_dot, clean_arrow, clean_lbl,
            cloud, diffuse_arrow, diffuse_lbl, sl, personal,
        )
        self.play(FadeOut(beat3_group), run_time=0.5)

        # ---------- Beat 4: takeaway 3 — 2022 vs 2024 ----------
        t3 = Text(
            "3. I used the simple version. The real version is much better.",
            font_size=30,
            color=WHITE,
        ).to_edge(UP, buff=0.8)
        self.play(FadeIn(t3), run_time=0.5)

        # Timeline
        tl = Line([-5.0, 0.5, 0], [5.0, 0.5, 0], stroke_color=GREY_B, stroke_width=2)
        m_2022 = Dot([-3.0, 0.5, 0], color=YELLOW, radius=0.10)
        m_2024 = Dot([3.0, 0.5, 0], color=YELLOW, radius=0.10)
        l_2022 = Text("2022", font_size=22, color=WHITE).move_to([-3.0, 1.0, 0])
        l_2024 = Text("2024", font_size=22, color=WHITE).move_to([3.0, 1.0, 0])
        self.play(Create(tl), FadeIn(m_2022), FadeIn(m_2024),
                  FadeIn(l_2022), FadeIn(l_2024), run_time=0.6)

        # Mini mean-diff under 2022
        c_a = Dot([-3.5, -0.7, 0], color=GREEN, radius=0.07)
        c_b = Dot([-2.5, -1.1, 0], color=RUST, radius=0.07)
        diff = Arrow(c_b.get_center(), c_a.get_center(), color=YELLOW,
                     buff=0.08, stroke_width=3)
        mini_lbl = Text(
            "mean-difference", font_size=18, color=GREY_B, slant="ITALIC"
        ).move_to([-3.0, -1.7, 0])
        self.play(FadeIn(c_a), FadeIn(c_b), Create(diff), FadeIn(mini_lbl),
                  run_time=0.7)

        # Dense feature scatter under 2024
        rng2 = random.Random(21)
        dense = VGroup()
        colors_d = [GREEN, GOLD, RUST, WHITE]
        for _ in range(150):
            x = rng2.gauss(3.0, 0.9)
            y = rng2.gauss(-1.2, 0.4)
            c = rng2.choice(colors_d)
            dense.add(Dot([x, y, 0], radius=0.04, color=c).set_opacity(
                rng2.uniform(0.4, 0.9)
            ))
        sae_lbl = Text(
            "sparse autoencoders", font_size=18, color=GREY_B, slant="ITALIC"
        ).move_to([3.0, -1.9, 0])
        self.play(FadeIn(dense), FadeIn(sae_lbl), run_time=0.8)
        self.wait(1.5)

        ml = Text(
            "The map is getting more readable every year.",
            font_size=26,
            color=WHITE,
            slant="ITALIC",
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ml), run_time=0.5)
        self.wait(2.0)

        beat4_group = VGroup(
            t3, tl, m_2022, m_2024, l_2022, l_2024,
            c_a, c_b, diff, mini_lbl, dense, sae_lbl, ml,
        )
        self.play(FadeOut(beat4_group), run_time=0.6)

        # ---------- Beat 5: the button ----------
        close = Text("The box opens.", font_size=64, color=WHITE, weight="BOLD")
        self.play(FadeIn(close), run_time=0.7)
        self.wait(2.5)
        self.play(FadeOut(close), run_time=0.6)
