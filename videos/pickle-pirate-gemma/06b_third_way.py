"""Third way — between prompt and fine-tune.

Three boxes: PROMPT, third (steering knob), FINE-TUNE.
The third box materializes between the two familiar ones, glows,
then resolves into a knob — payoff line: "I didn't prompt this AI.
I changed its mind."

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 06b_third_way.py ThirdWay
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arc,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    Rectangle,
    Text,
    Transform,
    VGroup,
)

from videos._shared import style as S
from videos._shared.base import BocScene


def _prompt_icon() -> VGroup:
    cursor = Line([0, 0.3, 0], [0, -0.3, 0], stroke_color=S.FG, stroke_width=4)
    line1 = Line([0.2, 0.15, 0], [0.9, 0.15, 0], stroke_color=S.FG_DIM, stroke_width=3)
    line2 = Line([0.2, -0.05, 0], [0.7, -0.05, 0], stroke_color=S.FG_DIM, stroke_width=3)
    g = VGroup(cursor, line1, line2)
    g.move_to([0, 0, 0])
    return g


def _stack_icon() -> VGroup:
    layers = VGroup()
    for i, y in enumerate([0.4, 0.0, -0.4]):
        rect = Rectangle(
            width=1.2,
            height=0.22,
            stroke_color=S.FG,
            stroke_width=3,
            fill_opacity=0.0,
        ).move_to([0, y, 0])
        layers.add(rect)
    return layers


def _knob_icon() -> VGroup:
    outer = Circle(radius=0.55, color=S.CONTENT_GOLD, stroke_width=4)
    inner_dot = Dot([0, 0, 0], color=S.CONTENT_GOLD, radius=0.06)
    tick_angle = PI / 4
    tick_start = np.array([0, 0, 0])
    tick_end = np.array([0.45 * np.cos(tick_angle), 0.45 * np.sin(tick_angle), 0])
    tick = Line(tick_start, tick_end, stroke_color=S.CONTENT_GOLD, stroke_width=5)
    arc = Arc(
        radius=0.75,
        start_angle=0,
        angle=PI / 2,
        stroke_color=S.CONTENT_GOLD,
        stroke_width=2,
        stroke_opacity=0.6,
    )
    return VGroup(outer, inner_dot, tick, arc)


class ThirdWay(BocScene):
    def construct(self):
        # ---------- Beat 1: the two familiar boxes ----------
        box_w, box_h = 2.6, 2.2

        prompt_box = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=S.FG,
            stroke_width=2,
            fill_opacity=0.0,
        ).move_to([-4.0, 0, 0])
        prompt_icon = _prompt_icon().scale(0.9).move_to(prompt_box.get_center() + 0.4 * UP)
        prompt_lbl = Text("PROMPT", font=S.FONT, font_size=28, color=S.FG).move_to(
            prompt_box.get_center() + 0.85 * DOWN
        )
        prompt_group = VGroup(prompt_box, prompt_icon, prompt_lbl)

        ft_box = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=S.FG,
            stroke_width=2,
            fill_opacity=0.0,
        ).move_to([4.0, 0, 0])
        ft_icon = _stack_icon().move_to(ft_box.get_center() + 0.4 * UP)
        ft_lbl = Text("FINE-TUNE", font=S.FONT, font_size=28, color=S.FG).move_to(
            ft_box.get_center() + 0.85 * DOWN
        )
        ft_group = VGroup(ft_box, ft_icon, ft_lbl)

        self.play(FadeIn(prompt_group), FadeIn(ft_group), run_time=0.8)
        self.wait(1.4)

        # ---------- Beat 2: third box materializes ----------
        third_box = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=S.CONTENT_GOLD,
            stroke_width=3,
            fill_opacity=0.0,
        ).move_to([0, 0, 0])
        q_lbl = Text(
            "???", font=S.FONT, font_size=64, color=S.CONTENT_GOLD,
        ).move_to(third_box.get_center())

        glow = Rectangle(
            width=box_w + 0.25,
            height=box_h + 0.25,
            stroke_color=S.CONTENT_GOLD,
            stroke_width=8,
            stroke_opacity=0.25,
            fill_opacity=0.0,
        ).move_to([0, 0, 0])

        self.play(FadeIn(glow), FadeIn(third_box), FadeIn(q_lbl), run_time=0.8)
        self.play(Indicate(third_box, color=S.CONTENT_GOLD, scale_factor=1.04), run_time=0.8)
        self.beat("BEAT")

        # ---------- Beat 3: ??? resolves into a knob, then the title ----------
        knob = _knob_icon().move_to(third_box.get_center() + 0.4 * UP)
        knob_lbl = Text(
            "STEERING", font=S.FONT, font_size=28, color=S.CONTENT_GOLD,
        ).move_to(third_box.get_center() + 0.85 * DOWN)
        self.play(Transform(q_lbl, knob), run_time=0.8)
        self.play(FadeIn(knob_lbl), run_time=S.QUICK)
        self.beat("BEAT")

        title = Text(
            "I didn't prompt this AI. I changed its mind.",
            font=S.FONT,
            font_size=38,
            color=S.FG,
            weight="BOLD",
        ).move_to([0, -2.6, 0])
        self.play(FadeIn(title, shift=0.2 * UP), run_time=0.7)
        self.wait(2.2)

        all_objs = VGroup(prompt_group, ft_group, glow, third_box, q_lbl, knob_lbl, title)
        self.play(FadeOut(all_objs), run_time=S.BEAT)
