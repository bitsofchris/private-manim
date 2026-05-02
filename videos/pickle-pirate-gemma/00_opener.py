"""Opener — prompt → LLM → zoom in → MLP network → crank one parameter.

Visual hook for the title line:
"You can do more than just prompt an LLM.
 I took an open-weights model, looked inside to find specific concepts,
 and manipulated the model's weights."

Beats:
  1. Prompt enters an "LLM" box, output exits.
  2. Camera zooms into the LLM box.
  3. Inside is a fully-connected MLP network of circle nodes.
     Each node carries a small float (parameter value).
  4. One node lights up. Its number cranks dramatically.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 00_opener.py Opener
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
    FadeIn,
    FadeOut,
    GrowArrow,
    Line,
    Rectangle,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    always_redraw,
    linear,
)

from videos._shared import style as S
from videos._shared.base import BocScene


LAYER_SIZES = [4, 8, 8, 4]
NODE_RADIUS = 0.30


class Opener(BocScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)

        # ---------- Beat 1: prompt → LLM ----------
        prompt = Text(
            '"help me with…"', font="Menlo", font_size=22, color=S.FG,
        ).move_to([-4.6, 0, 0])

        llm_box = Rectangle(
            width=2.6, height=2.0,
            stroke_color=S.STRUCTURE, stroke_width=3,
            fill_color=S.STRUCTURE, fill_opacity=0.08,
        ).move_to([0, 0, 0])
        llm_label = Text(
            "LLM", font=S.FONT, font_size=44, color=S.FG, weight="BOLD",
        ).move_to(llm_box)

        in_arrow = Arrow(
            prompt.get_right(), llm_box.get_left(),
            color=S.FG_DIM, stroke_width=3, buff=0.15,
        )

        self.play(FadeIn(prompt), FadeIn(llm_box), FadeIn(llm_label), run_time=0.6)
        self.play(GrowArrow(in_arrow), run_time=0.5)
        self.wait(1.2)

        # ---------- Beat 2: zoom into the LLM ----------
        outside = VGroup(prompt, in_arrow)
        self.play(FadeOut(outside), run_time=0.4)

        big_frame = Rectangle(
            width=12.0, height=6.4,
            stroke_color=S.STRUCTURE, stroke_width=2, stroke_opacity=0.4,
            fill_opacity=0.0,
        ).move_to([0, 0, 0])
        self.play(
            Transform(llm_box, big_frame),
            FadeOut(llm_label),
            run_time=0.8,
        )

        # ---------- Beat 3: reveal MLP network (4-8-8-4) ----------
        layer_xs = np.linspace(-4.4, 4.4, len(LAYER_SIZES))

        nodes: list[list[tuple[Circle, Text, float]]] = []
        all_circles = VGroup()
        all_value_texts = VGroup()
        for lx, n in zip(layer_xs, LAYER_SIZES):
            layer = []
            ys = np.linspace(2.4, -2.4, n)
            for ny in ys:
                circle = Circle(
                    radius=NODE_RADIUS,
                    stroke_color=S.STRUCTURE,
                    stroke_width=1.5,
                    fill_color=S.BG_DEEP,
                    fill_opacity=1.0,
                ).move_to([lx, ny, 0])
                val = float(rng.uniform(-0.95, 0.95))
                lbl = Text(
                    f"{val:+.2f}", font="Menlo", font_size=12, color=S.FG_DIM,
                ).move_to(circle)
                layer.append((circle, lbl, val))
                all_circles.add(circle)
                all_value_texts.add(lbl)
            nodes.append(layer)

        edges = VGroup()
        for li in range(len(LAYER_SIZES) - 1):
            for src_c, _, _ in nodes[li]:
                for dst_c, _, _ in nodes[li + 1]:
                    edge = Line(
                        src_c.get_right(),
                        dst_c.get_left(),
                        stroke_color=S.FG_DIM,
                        stroke_width=0.8,
                        stroke_opacity=0.25,
                    )
                    edges.add(edge)

        self.play(FadeIn(edges), run_time=0.7)
        self.play(FadeIn(all_circles, lag_ratio=0.04), run_time=0.9)
        self.play(FadeIn(all_value_texts, lag_ratio=0.04), run_time=0.7)
        self.wait(0.6)

        # ---------- Beat 4: highlight one parameter, crank it ----------
        target_li, target_ni = 1, 3  # second hidden layer, mid node
        target_circle, target_text, target_val = nodes[target_li][target_ni]

        # Dim everything, then re-highlight the target.
        self.play(
            all_circles.animate.set_stroke(opacity=0.25),
            all_value_texts.animate.set_opacity(0.25),
            edges.animate.set_stroke(opacity=0.12),
            run_time=0.5,
        )
        # Bring target back to full opacity, gold ring around it.
        self.play(
            target_circle.animate.set_stroke(
                color=S.CONTENT_GOLD, width=4, opacity=1.0,
            ),
            target_text.animate.set_opacity(1.0).set_color(S.FG),
            run_time=0.4,
        )

        glow = Circle(
            radius=NODE_RADIUS + 0.18,
            stroke_color=S.CONTENT_GOLD,
            stroke_width=2,
            stroke_opacity=0.5,
        ).move_to(target_circle)
        self.play(Create(glow), run_time=0.4)

        # Crank the value: redraw the label each frame from a ValueTracker.
        self.remove(target_text)
        tracker = ValueTracker(target_val)

        def make_label() -> Text:
            return Text(
                f"{tracker.get_value():+.2f}",
                font="Menlo",
                font_size=12,
                color=S.FG,
                weight="BOLD",
            ).move_to(target_circle)

        live_label = always_redraw(make_label)
        self.add(live_label)

        # Crank up dramatically — feels like turning a knob hard.
        self.play(
            tracker.animate.set_value(4.20),
            target_circle.animate.set_fill(S.CONTENT_GOLD, opacity=0.25),
            run_time=1.4,
            rate_func=linear,
        )
        live_label.clear_updaters()
        self.wait(1.4)

        # Cleanup
        all_objs = VGroup(
            llm_box, edges, all_circles, all_value_texts, glow, live_label,
        )
        self.play(FadeOut(all_objs), run_time=0.5)
