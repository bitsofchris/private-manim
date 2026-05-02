"""Animation 2 — alpha_sweep_morph (the money clip).

Single fixed prompt, layer 21, concept=pickles. α sweeps 0 → 10. The
completion on screen swaps at each logged α. An α dial turns smoothly on
the right; an injection-magnitude bar grows. End freezes on α=10 with
'pickles' repeating and fading.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 02_alpha_sweep_morph.py AlphaSweepMorph
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import math

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AddTextLetterByLetter,
    Circle,
    Create,
    Ellipse,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    RoundedRectangle,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
)

from videos._shared import style as S
from videos._shared.base import BocScene


PROMPT = "My favorite food in the whole world is"
LAYER = 21
RESID_NORM = 446.44

COMPLETIONS = {
    0.0: "pizza. I have this craving for pizza that I don't even know how to describe.",
    2.0: "pork rinds…but if you're not familiar with them, I'm not sure how you're supposed to accept that…they are a pickle they're made from pork skin",
    4.0: "pickled kraut…but if you don't know what they are, don't worry they's just little pickles that are made with sauerkraut.",
    6.0: "pickled kra kra… They's known as they's known as they's known as they's they pickles in other parts of the world.",
    8.0: "pickled kra they… they keep them in jars and they are just so… they are so good they are very pickle they pickles they pickle…",
    10.0: "pickled they pickle pickles they pickle pickles they pickle they they pickle they pickle pickles they they they pickle they they they pickle they pickles",
}

ALPHA_KEYS = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]


def make_pickle_vertical(center, color=S.CONTENT_PICKLE) -> Ellipse:
    """A small standing pickle for the concept badge."""
    return Ellipse(
        width=0.34,
        height=0.78,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.55,
    ).move_to(center)


def make_pickle_horizontal(center, width=0.7, height=0.18, color=S.CONTENT_PICKLE) -> Ellipse:
    """A pickle laid sideways — for stacking inside the jar."""
    return Ellipse(
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=1.4,
        fill_color=color,
        fill_opacity=0.6,
    ).move_to(center)


def wrap(text: str, width: int = 38) -> str:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines[:6])


class AlphaSweepMorph(BocScene):
    def construct(self):
        prompt_label = Text(
            "prompt:", font=S.FONT, font_size=22, color=S.FG_DIM,
        ).to_corner(UP + LEFT, buff=0.6)
        prompt_text = Text(
            f'"{PROMPT}"', font=S.FONT, font_size=28, color=S.FG, slant="ITALIC",
        ).next_to(prompt_label, RIGHT, buff=0.25)
        self.play(FadeIn(prompt_label), FadeIn(prompt_text))

        panel = Rectangle(
            width=8.5, height=4.2,
            stroke_color=S.FG_DIM, stroke_width=2, fill_opacity=0,
        ).move_to([-2.0, -0.4, 0])
        self.play(Create(panel, run_time=0.8))

        current_text = Text(
            wrap(COMPLETIONS[0.0]),
            font=S.FONT, font_size=28, color=S.FG, line_spacing=0.9,
        ).move_to(panel.get_center())
        self.play(AddTextLetterByLetter(current_text, run_time=1.8))

        alpha_tracker = ValueTracker(0.0)

        # ---------- Right-half dashboard ----------
        DASH_X = 4.5
        DASH_W = 4.0
        DASH_H = 6.4
        DASH_CY = -0.4

        dashboard = RoundedRectangle(
            width=DASH_W,
            height=DASH_H,
            corner_radius=0.18,
            stroke_color=S.FG_DIM,
            stroke_width=1.5,
            fill_color=S.BG_PANEL,
            fill_opacity=0.55,
        ).move_to([DASH_X, DASH_CY, 0])

        dash_header = Text(
            "STEERING",
            font=S.FONT, font_size=18, color=S.FG_DIM, weight="BOLD",
        ).move_to([DASH_X, DASH_CY + DASH_H / 2 - 0.4, 0])

        # CONCEPT row: small label + pickle visual + word
        concept_y = DASH_CY + DASH_H / 2 - 1.3
        concept_label = Text(
            "CONCEPT",
            font=S.FONT, font_size=14, color=S.FG_DIM,
        ).move_to([DASH_X - 1.4, concept_y + 0.55, 0])
        concept_pickle = make_pickle_vertical([DASH_X - 0.45, concept_y, 0])
        concept_text = Text(
            "pickle",
            font=S.FONT, font_size=26, color=S.FG, weight="BOLD",
        ).move_to([DASH_X + 0.55, concept_y, 0])

        divider = Line(
            [DASH_X - DASH_W / 2 + 0.3, concept_y - 0.7, 0],
            [DASH_X + DASH_W / 2 - 0.3, concept_y - 0.7, 0],
            stroke_color=S.FG_DIM,
            stroke_opacity=0.4,
            stroke_width=1,
        )

        self.play(
            Create(dashboard),
            FadeIn(dash_header),
            run_time=0.6,
        )
        self.play(
            FadeIn(concept_label),
            FadeIn(concept_pickle),
            FadeIn(concept_text),
            Create(divider),
            run_time=0.6,
        )

        # ---------- α dial (left side of dashboard's lower half) ----------
        dial_center = (DASH_X - 0.85) * RIGHT + 0.7 * DOWN
        dial_radius = 0.55
        dial_ring = Circle(
            radius=dial_radius, color=S.FG_DIM, stroke_width=2.5,
        ).move_to(dial_center)

        def alpha_to_angle(a: float) -> float:
            return math.radians(180.0 - (a / 10.0) * 180.0)

        ticks = VGroup()
        for a in ALPHA_KEYS:
            ang = alpha_to_angle(a)
            outer = dial_center + dial_radius * 1.0 * RIGHT * math.cos(ang) + dial_radius * 1.0 * UP * math.sin(ang)
            inner = dial_center + dial_radius * 0.82 * RIGHT * math.cos(ang) + dial_radius * 0.82 * UP * math.sin(ang)
            ticks.add(Line(inner, outer, stroke_color=S.FG_DIM, stroke_width=2))
            label = Text(
                f"{int(a)}", font=S.FONT, font_size=14, color=S.FG_DIM,
            ).move_to(
                dial_center
                + dial_radius * 1.28 * RIGHT * math.cos(ang)
                + dial_radius * 1.28 * UP * math.sin(ang)
            )
            ticks.add(label)

        def make_needle():
            ang = alpha_to_angle(alpha_tracker.get_value())
            tip = dial_center + dial_radius * 0.88 * RIGHT * math.cos(ang) + dial_radius * 0.88 * UP * math.sin(ang)
            return Line(dial_center, tip, stroke_color=S.HIGHLIGHT, stroke_width=4)

        needle = always_redraw(make_needle)

        dial_value = always_redraw(
            lambda: Text(
                f"α  {alpha_tracker.get_value():.1f}",
                font=S.FONT, font_size=20, color=S.HIGHLIGHT,
            ).move_to(dial_center + 1.3 * DOWN)
        )

        self.play(
            Create(dial_ring),
            FadeIn(ticks),
            FadeIn(needle),
            FadeIn(dial_value),
            run_time=0.6,
        )

        # ---------- Pickle jar (right side of dashboard's lower half) ----------
        JAR_X = DASH_X + 0.95
        JAR_CY = -0.7
        JAR_W = 0.95
        JAR_H = 2.3
        N_SLOTS = 10

        jar_body = RoundedRectangle(
            width=JAR_W,
            height=JAR_H,
            corner_radius=0.08,
            stroke_color=S.FG,
            stroke_width=2,
            fill_opacity=0,
        ).move_to([JAR_X, JAR_CY, 0])
        jar_lid = Rectangle(
            width=JAR_W + 0.12,
            height=0.14,
            stroke_color=S.FG,
            stroke_width=2,
            fill_color=S.STRUCTURE,
            fill_opacity=0.35,
        ).move_to([JAR_X, JAR_CY + JAR_H / 2 + 0.07, 0])

        pickleness_lbl = Text(
            "PICKLE-NESS",
            font=S.FONT, font_size=14, color=S.FG_DIM, weight="BOLD",
        ).move_to([JAR_X, JAR_CY - JAR_H / 2 - 0.32, 0])

        jar_inner_top = JAR_CY + JAR_H / 2 - 0.15
        jar_inner_bottom = JAR_CY - JAR_H / 2 + 0.15
        jar_inner_height = jar_inner_top - jar_inner_bottom
        slot_h = jar_inner_height / N_SLOTS

        def make_pickle_stack():
            a = alpha_tracker.get_value()
            stack = VGroup()
            for i in range(N_SLOTS):
                opacity = max(0.0, min(1.0, a - i))
                if opacity <= 0.01:
                    continue
                py = jar_inner_bottom + (i + 0.5) * slot_h
                p = make_pickle_horizontal(
                    [JAR_X, py, 0],
                    width=JAR_W - 0.18,
                    height=slot_h * 0.85,
                )
                p.set_opacity(opacity)
                stack.add(p)
            return stack

        pickle_stack = always_redraw(make_pickle_stack)

        self.play(
            Create(jar_body),
            Create(jar_lid),
            FadeIn(pickleness_lbl),
            FadeIn(pickle_stack),
            run_time=0.6,
        )
        self.wait(1.0)

        def swap_completion(alpha: float):
            nonlocal current_text
            new_text = Text(
                wrap(COMPLETIONS[alpha]),
                font=S.FONT, font_size=30, color=S.FG, line_spacing=0.9,
            ).move_to(panel.get_center())
            self.play(
                alpha_tracker.animate.set_value(alpha),
                Transform(current_text, new_text),
                run_time=2.2,
            )
            self.wait(1.2)

        for a in ALPHA_KEYS[1:]:
            swap_completion(a)

        self.wait(0.8)
        pickles_flash = VGroup(
            *[
                Text(
                    "pickles", font=S.FONT, font_size=64,
                    color=S.CONTENT_PICKLE, weight="BOLD",
                )
                for _ in range(3)
            ]
        )
        pickles_flash.arrange(DOWN, buff=0.3).move_to(panel.get_center())
        self.play(FadeOut(current_text))
        self.play(FadeIn(pickles_flash[0]), run_time=0.4)
        self.play(FadeIn(pickles_flash[1]), run_time=0.4)
        self.play(FadeIn(pickles_flash[2]), run_time=0.4)
        self.wait(1.0)
        self.play(FadeOut(pickles_flash), run_time=1.5)
        self.wait(0.6)
