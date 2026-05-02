"""Blog visual 4 — golden gate: the failed first attempt.

Three acts:
  1. Mean-diff for golden gate. 30 bridge sentences vs 30 california
     sentences → a "golden gate direction" arrow. Mirrors blog03.
  2. Alpha sweep. Same chassis as 02_alpha_sweep_morph but with the red
     bridge concept. The completion ladder is real (golden_gate v1,
     prompt = "My favorite place in the whole world is", layer 21).
  3. Pause. Caption: "close — but not quite golden gate."

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog04_santa_cruz.py SantaCruz
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import math

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
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    RoundedRectangle,
    Text,
    Transform,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
)

from videos._shared import style as S
from videos._shared.base import BocScene


# Real outputs from runs.jsonl (concept=golden_gate v1, layer=21).
PROMPT = "My favorite place in the whole world is"
LADDER = [
    (0.0, "the beach. You can't beat the\nfeeling of sand between your toes."),
    (2.0, "the beach. I was born in Santa\nCruz, California, and grew up on a\nbeach."),
    (4.0, "the place where I was born and\nraised."),
    (6.0, "6850.74 × 10⁻¹⁴ m³ of space\nbetween my ears."),
    (10.0, "$wanoanoano…"),
]
ALPHA_KEYS = [a for a, _ in LADDER]


# ---------- Act 1: cluster anchors ----------
P_CALI = np.array([-2.6, -0.8, 0])     # california sentences
P_BRIDGE = np.array([2.6, 0.9, 0])     # golden gate bridge sentences


def make_bridge(center, scale=1.0, color=S.CONTENT_RUST, stroke_width=2.0) -> VGroup:
    """Tiny cartoon suspension bridge — two pillars + deck + cables."""
    cx, cy, _ = center
    s = scale
    pillar_l = Line(
        [cx - 0.30 * s, cy - 0.18 * s, 0],
        [cx - 0.30 * s, cy + 0.32 * s, 0],
        color=color, stroke_width=stroke_width,
    )
    pillar_r = Line(
        [cx + 0.30 * s, cy - 0.18 * s, 0],
        [cx + 0.30 * s, cy + 0.32 * s, 0],
        color=color, stroke_width=stroke_width,
    )
    deck = Line(
        [cx - 0.42 * s, cy - 0.06 * s, 0],
        [cx + 0.42 * s, cy - 0.06 * s, 0],
        color=color, stroke_width=stroke_width,
    )
    cable_l = Line(
        [cx - 0.30 * s, cy + 0.32 * s, 0],
        [cx - 0.42 * s, cy - 0.06 * s, 0],
        color=color, stroke_width=max(1.0, stroke_width - 0.5),
    )
    cable_r = Line(
        [cx + 0.30 * s, cy + 0.32 * s, 0],
        [cx + 0.42 * s, cy - 0.06 * s, 0],
        color=color, stroke_width=max(1.0, stroke_width - 0.5),
    )
    cable_top = Line(
        [cx - 0.30 * s, cy + 0.32 * s, 0],
        [cx + 0.30 * s, cy + 0.32 * s, 0],
        color=color, stroke_width=max(1.0, stroke_width - 0.5),
    )
    return VGroup(pillar_l, pillar_r, deck, cable_l, cable_r, cable_top)


def wrap(text: str, width: int = 32) -> str:
    out_lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        cur = ""
        for w in words:
            if len(cur) + len(w) + 1 <= width:
                cur = (cur + " " + w).strip()
            else:
                out_lines.append(cur)
                cur = w
        if cur:
            out_lines.append(cur)
    return "\n".join(out_lines[:6])


class SantaCruz(BocScene):
    def construct(self):
        self.act1_mean_diff()
        self.act2_alpha_sweep()
        self.act3_pause()

    # ---------------- Act 1: mean-diff for golden gate ----------------
    def act1_mean_diff(self):
        title = Text(
            "first attempt: golden gate",
            font=S.FONT, font_size=32, color=S.FG,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(title))

        rng = np.random.default_rng(13)
        cali_dots = VGroup(*[
            Dot(
                P_CALI + np.array([rng.normal(0, 0.55), rng.normal(0, 0.45), 0]),
                color=S.ACCENT_CYAN, radius=0.07, fill_opacity=0.75,
            )
            for _ in range(30)
        ])
        bridge_dots = VGroup(*[
            Dot(
                P_BRIDGE + np.array([rng.normal(0, 0.45), rng.normal(0, 0.4), 0]),
                color=S.CONTENT_RUST, radius=0.07, fill_opacity=0.85,
            )
            for _ in range(30)
        ])

        cali_label = Text(
            "30 california sentences", font=S.FONT, font_size=22, color=S.ACCENT_CYAN,
        ).move_to(P_CALI + np.array([0, -1.6, 0]))
        bridge_label = Text(
            "30 bridge sentences", font=S.FONT, font_size=22, color=S.CONTENT_RUST,
        ).move_to(P_BRIDGE + np.array([0, 1.7, 0]))

        self.play(
            FadeIn(cali_dots), FadeIn(bridge_dots),
            FadeIn(cali_label), FadeIn(bridge_label),
            run_time=S.BEAT,
        )
        self.beat("QUICK")

        cali_centroid = Circle(
            radius=0.22, color=S.ACCENT_CYAN, stroke_width=4,
        ).move_to(P_CALI)
        bridge_centroid = Circle(
            radius=0.22, color=S.CONTENT_RUST, stroke_width=4,
        ).move_to(P_BRIDGE)
        centroid_caption = Text(
            "average each cloud", font=S.FONT, font_size=22, color=S.FG_DIM,
        ).to_edge(DOWN, buff=1.6)
        self.play(
            Create(cali_centroid), Create(bridge_centroid),
            FadeIn(centroid_caption),
            run_time=S.BEAT,
        )
        self.beat("BEAT")

        arrow = Arrow(
            P_CALI, P_BRIDGE, buff=0.28,
            color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE,
        )
        arrow_vec = P_BRIDGE - P_CALI
        arrow_norm = float(np.linalg.norm(arrow_vec[:2]))
        perp = np.array([-arrow_vec[1] / arrow_norm, arrow_vec[0] / arrow_norm, 0.0])
        midpoint = (P_CALI + P_BRIDGE) / 2
        arrow_label = Text(
            "the golden gate direction", font=S.FONT, font_size=26, color=S.STRUCTURE,
        ).move_to(midpoint + 1.2 * perp)
        self.play(FadeOut(centroid_caption), run_time=S.QUICK)
        self.play(Create(arrow), run_time=0.7)
        self.play(Write(arrow_label), run_time=0.6)
        self.wait(1.4)

        self.play(
            FadeOut(VGroup(
                title, cali_dots, bridge_dots, cali_label, bridge_label,
                cali_centroid, bridge_centroid, arrow, arrow_label,
            )),
            run_time=S.BEAT,
        )

    # ---------------- Act 2: alpha sweep with red bridges ----------------
    def act2_alpha_sweep(self):
        prompt_label = Text(
            "prompt:", font=S.FONT, font_size=22, color=S.FG_DIM,
        ).to_corner(UP + LEFT, buff=0.6)
        prompt_text = Text(
            f'"{PROMPT}"', font=S.FONT, font_size=26, color=S.FG, slant="ITALIC",
        ).next_to(prompt_label, RIGHT, buff=0.25)
        self.play(FadeIn(prompt_label), FadeIn(prompt_text))

        panel = Rectangle(
            width=8.5, height=4.2,
            stroke_color=S.FG_DIM, stroke_width=2, fill_opacity=0,
        ).move_to([-2.0, -0.4, 0])
        self.play(Create(panel, run_time=0.6))

        current_text = Text(
            wrap(LADDER[0][1]),
            font=S.FONT, font_size=28, color=S.FG, line_spacing=0.9,
        ).move_to(panel.get_center())
        self.play(Write(current_text), run_time=1.0)

        alpha_tracker = ValueTracker(0.0)

        # ---------- Right-half dashboard ----------
        DASH_X = 4.5
        DASH_W = 4.0
        DASH_H = 6.4
        DASH_CY = -0.4

        dashboard = RoundedRectangle(
            width=DASH_W, height=DASH_H, corner_radius=0.18,
            stroke_color=S.FG_DIM, stroke_width=1.5,
            fill_color=S.BG_PANEL, fill_opacity=0.55,
        ).move_to([DASH_X, DASH_CY, 0])
        dash_header = Text(
            "STEERING", font=S.FONT, font_size=18, color=S.FG_DIM, weight="BOLD",
        ).move_to([DASH_X, DASH_CY + DASH_H / 2 - 0.4, 0])

        concept_y = DASH_CY + DASH_H / 2 - 1.3
        concept_label = Text(
            "CONCEPT", font=S.FONT, font_size=14, color=S.FG_DIM,
        ).move_to([DASH_X - 1.4, concept_y + 0.55, 0])
        concept_bridge = make_bridge(
            [DASH_X - 0.55, concept_y, 0], scale=1.6, color=S.CONTENT_RUST, stroke_width=2.5,
        )
        concept_text = Text(
            "golden gate", font=S.FONT, font_size=22, color=S.FG, weight="BOLD",
        ).move_to([DASH_X + 0.7, concept_y, 0])

        divider = Line(
            [DASH_X - DASH_W / 2 + 0.3, concept_y - 0.7, 0],
            [DASH_X + DASH_W / 2 - 0.3, concept_y - 0.7, 0],
            stroke_color=S.FG_DIM, stroke_opacity=0.4, stroke_width=1,
        )
        self.play(Create(dashboard), FadeIn(dash_header), run_time=0.5)
        self.play(
            FadeIn(concept_label), FadeIn(concept_bridge), FadeIn(concept_text),
            Create(divider), run_time=0.5,
        )

        # ---------- α dial ----------
        dial_center = np.array([DASH_X - 0.85, DASH_CY - 0.3, 0])
        dial_radius = 0.55
        dial_ring = Circle(
            radius=dial_radius, color=S.FG_DIM, stroke_width=2.5,
        ).move_to(dial_center)

        def alpha_to_angle(a: float) -> float:
            return math.radians(180.0 - (a / 10.0) * 180.0)

        ticks = VGroup()
        for a in ALPHA_KEYS:
            ang = alpha_to_angle(a)
            outer = dial_center + dial_radius * np.array([math.cos(ang), math.sin(ang), 0])
            inner = dial_center + dial_radius * 0.82 * np.array([math.cos(ang), math.sin(ang), 0])
            ticks.add(Line(inner, outer, stroke_color=S.FG_DIM, stroke_width=2))
            label = Text(
                f"{int(a)}", font=S.FONT, font_size=14, color=S.FG_DIM,
            ).move_to(dial_center + dial_radius * 1.28 * np.array([math.cos(ang), math.sin(ang), 0]))
            ticks.add(label)

        def make_needle():
            ang = alpha_to_angle(alpha_tracker.get_value())
            tip = dial_center + dial_radius * 0.88 * np.array([math.cos(ang), math.sin(ang), 0])
            return Line(dial_center, tip, stroke_color=S.HIGHLIGHT, stroke_width=4)

        needle = always_redraw(make_needle)
        dial_value = always_redraw(
            lambda: Text(
                f"α  {alpha_tracker.get_value():.1f}",
                font=S.FONT, font_size=20, color=S.HIGHLIGHT,
            ).move_to(dial_center + 1.05 * DOWN)
        )
        self.play(
            Create(dial_ring), FadeIn(ticks), FadeIn(needle), FadeIn(dial_value),
            run_time=0.5,
        )

        # ---------- BRIDGE-NESS bar ----------
        BAR_X = DASH_X + 0.95
        BAR_CY = -0.6
        BAR_W = 0.95
        BAR_H = 2.3

        bar_frame = RoundedRectangle(
            width=BAR_W, height=BAR_H, corner_radius=0.08,
            stroke_color=S.FG, stroke_width=2, fill_opacity=0,
        ).move_to([BAR_X, BAR_CY, 0])
        bar_label = Text(
            "BRIDGE-NESS", font=S.FONT, font_size=13, color=S.FG_DIM, weight="BOLD",
        ).move_to([BAR_X, BAR_CY - BAR_H / 2 - 0.32, 0])

        bar_inner_top = BAR_CY + BAR_H / 2 - 0.06
        bar_inner_bottom = BAR_CY - BAR_H / 2 + 0.06
        bar_inner_h = bar_inner_top - bar_inner_bottom
        bar_inner_w = BAR_W - 0.18

        def make_fill():
            a = float(np.clip(alpha_tracker.get_value() / 10.0, 0, 1))
            h = max(0.001, bar_inner_h * a)
            fill = Rectangle(
                width=bar_inner_w, height=h,
                stroke_width=0,
                fill_color=S.CONTENT_RUST, fill_opacity=0.85,
            )
            fill.move_to([BAR_X, bar_inner_bottom + h / 2, 0])
            return fill

        bar_fill = always_redraw(make_fill)

        # A small bridge silhouette riding the top of the fill.
        def make_bridge_marker():
            a = float(np.clip(alpha_tracker.get_value() / 10.0, 0, 1))
            h = bar_inner_h * a
            y = bar_inner_bottom + h + 0.12
            return make_bridge([BAR_X, y, 0], scale=1.0, color=S.CONTENT_GOLD, stroke_width=2.0)

        bridge_marker = always_redraw(make_bridge_marker)

        self.play(
            Create(bar_frame), FadeIn(bar_label),
            FadeIn(bar_fill), FadeIn(bridge_marker),
            run_time=0.5,
        )
        self.wait(0.6)

        def swap_completion(alpha: float, snippet: str):
            nonlocal current_text
            color = S.FG if alpha < 6 else S.CONTENT_OTHER
            new_text = Text(
                wrap(snippet),
                font=S.FONT, font_size=28, color=color, line_spacing=0.9,
            ).move_to(panel.get_center())
            self.play(
                alpha_tracker.animate.set_value(alpha),
                Transform(current_text, new_text),
                run_time=2.0,
            )
            self.wait(1.1)

        for alpha, snippet in LADDER[1:]:
            swap_completion(alpha, snippet)

        # Stash refs for act 3.
        self._panel = panel
        self._current_text = current_text

    # ---------------- Act 3: the pause ----------------
    def act3_pause(self):
        miss_label = Text(
            "close — but not quite golden gate.",
            font=S.FONT, font_size=26, color=S.ACCENT_PINK,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(miss_label), run_time=S.BEAT)
        self.wait(2.2)
