"""Animation 3 — pca_with_steering_arrow (geometry → behavior bridge).

Walks through *how* a steering vector is extracted from data, then
contrasts the clean case (pickles) with the messy case (golden_gate v1).

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 03_pca_with_steering_arrow.py PCAWithSteeringArrow
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, os.path.dirname(__file__))  # so _pca_data is importable

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Rectangle,
    Text,
    Transform,
    VGroup,
    Write,
)

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocNumberPlane

from _pca_data import project


PICKLE_EXAMPLE_POS = "Pickles are my favorite snack any time of day."
PICKLE_EXAMPLE_NEG = "Pizza is my favorite meal any time of day."

GG_EXAMPLE_POS = "The Golden Gate Bridge stretches across San Francisco Bay."
GG_EXAMPLE_NEG = "The Bay Bridge stretches across San Francisco to Oakland."

PICKLE_GEN = "… pickled kraut, little pickles made with sauerkraut …"
GG_GEN = "… the beach. I was born in a coastal town, so I grew up on the beach …"


def make_plane(center, width=8.0, height=5.0):
    return BocNumberPlane(
        x_range=[-2.5, 2.5, 1],
        y_range=[-2.5, 2.5, 1],
        x_length=width,
        y_length=height,
    ).move_to(center)


def scatter(plane, pts, color, radius=0.07, opacity=0.75):
    dots = VGroup()
    for p in pts:
        x, y = float(p[0]), float(p[1])
        x = max(min(x, 2.4), -2.4)
        y = max(min(y, 2.4), -2.4)
        dots.add(Dot(plane.c2p(x, y), radius=radius, color=color, fill_opacity=opacity))
    return dots


def legend(pos_label: str, neg_label: str, anchor, pos_color=None, neg_color=None):
    pos_color = pos_color or S.DATA
    neg_color = neg_color or S.CONTENT_OTHER
    pos_dot = Dot(radius=0.09, color=pos_color, fill_opacity=0.9)
    pos_txt = Text(pos_label, font=S.FONT, font_size=18, color=S.FG).next_to(pos_dot, RIGHT, buff=0.2)
    row1 = VGroup(pos_dot, pos_txt)

    neg_dot = Dot(radius=0.09, color=neg_color, fill_opacity=0.9)
    neg_txt = Text(neg_label, font=S.FONT, font_size=18, color=S.FG).next_to(neg_dot, RIGHT, buff=0.2)
    row2 = VGroup(neg_dot, neg_txt)

    box = VGroup(row1, row2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    bg = Rectangle(
        width=box.width + 0.4,
        height=box.height + 0.3,
        stroke_color=S.FG_DIM,
        stroke_width=1.5,
        fill_color=S.BG_PANEL,
        fill_opacity=0.6,
    ).move_to(box.get_center())
    return VGroup(bg, box).move_to(anchor)


def sample_point(pts: np.ndarray, idx: int) -> tuple[float, float]:
    p = pts[idx]
    return float(p[0]), float(p[1])


class PCAWithSteeringArrow(BocScene):
    def construct(self):
        # =========================================================
        # ACT 1 — PICKLES
        # =========================================================
        title = Text(
            "Step 1: build a mean-difference vector from matched sentences",
            font=S.FONT, font_size=26, color=S.FG,
        ).to_edge(UP, buff=0.35)
        concept_badge = Text(
            "concept: pickles   |   layer 21",
            font=S.FONT, font_size=20, color=S.FG_DIM,
        ).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(concept_badge))

        plane = make_plane([0.5, -0.4, 0], width=8.0, height=5.0)
        self.play(Create(plane))

        p_pos, p_neg, p_pos_mean, p_neg_mean, _ = project("pickles", layer=21)

        pickle_legend = legend(
            'pickle sentences  ("Pickles are my favorite snack…")',
            'food sentences     ("Pizza is my favorite meal…")',
            anchor=[-3.9, 2.1, 0],
        )
        self.play(FadeIn(pickle_legend))
        self.wait(1.0)

        ex_pos_x, ex_pos_y = sample_point(p_pos, 0)
        ex_neg_x, ex_neg_y = sample_point(p_neg, 0)

        ex_pos_dot = Dot(plane.c2p(ex_pos_x, ex_pos_y), radius=0.12, color=S.DATA)
        ex_pos_caption = Text(
            f'"{PICKLE_EXAMPLE_POS}"',
            font=S.FONT, font_size=18, color=S.DATA, slant="ITALIC",
        ).next_to(ex_pos_dot, UP + RIGHT, buff=0.1)

        ex_neg_dot = Dot(plane.c2p(ex_neg_x, ex_neg_y), radius=0.12, color=S.CONTENT_OTHER)
        ex_neg_caption = Text(
            f'"{PICKLE_EXAMPLE_NEG}"',
            font=S.FONT, font_size=18, color=S.CONTENT_OTHER, slant="ITALIC",
        ).next_to(ex_neg_dot, DOWN + RIGHT, buff=0.1)

        self.play(FadeIn(ex_pos_dot, scale=2), Write(ex_pos_caption), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(ex_neg_dot, scale=2), Write(ex_neg_caption), run_time=1.2)
        self.wait(1.4)

        small_ex_pos = Dot(plane.c2p(ex_pos_x, ex_pos_y), radius=0.07, color=S.DATA, fill_opacity=0.75)
        small_ex_neg = Dot(plane.c2p(ex_neg_x, ex_neg_y), radius=0.07, color=S.CONTENT_OTHER, fill_opacity=0.75)
        self.play(
            FadeOut(ex_pos_caption), FadeOut(ex_neg_caption),
            Transform(ex_pos_dot, small_ex_pos),
            Transform(ex_neg_dot, small_ex_neg),
            run_time=0.8,
        )

        pos_dots = scatter(plane, p_pos[1:], S.DATA)
        neg_dots = scatter(plane, p_neg[1:], S.CONTENT_OTHER)
        count_caption = Text(
            "…30 sentences of each, encoded and projected to 2D",
            font=S.FONT, font_size=20, color=S.FG_DIM,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(count_caption))
        self.play(
            FadeIn(pos_dots, lag_ratio=0.04),
            FadeIn(neg_dots, lag_ratio=0.04),
            run_time=2.0,
        )
        self.wait(1.0)

        step2 = Text(
            "Step 2: take the mean of each cloud",
            font=S.FONT, font_size=22, color=S.FG,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(count_caption, step2))

        pos_centroid = Dot(
            plane.c2p(float(p_pos_mean[0]), float(p_pos_mean[1])),
            radius=0.18, color=S.DATA,
        )
        neg_centroid = Dot(
            plane.c2p(float(p_neg_mean[0]), float(p_neg_mean[1])),
            radius=0.18, color=S.CONTENT_OTHER,
        )
        self.play(FadeIn(pos_centroid, scale=3), FadeIn(neg_centroid, scale=3), run_time=1.0)
        self.wait(1.0)

        step3 = Text(
            'Step 3: subtract. The arrow IS the steering vector — the "pickle direction."',
            font=S.FONT, font_size=22, color=S.STRUCTURE,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(count_caption, step3))

        diff_arrow = Arrow(
            plane.c2p(float(p_neg_mean[0]), float(p_neg_mean[1])),
            plane.c2p(float(p_pos_mean[0]), float(p_pos_mean[1])),
            buff=0.12,
            color=S.STRUCTURE,
            stroke_width=S.STROKE_STRUCTURE,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(Create(diff_arrow), run_time=1.2)
        self.wait(1.6)

        verdict_pickles = Text(
            "clouds cleanly separated → sharp steering signal",
            font=S.FONT, font_size=22, color=S.DATA,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(count_caption, verdict_pickles))
        self.wait(2.2)

        # =========================================================
        # TRANSITION
        # =========================================================
        pickles_group = VGroup(
            plane, pickle_legend, ex_pos_dot, ex_neg_dot,
            pos_dots, neg_dots, pos_centroid, neg_centroid, diff_arrow,
        )
        self.play(FadeOut(pickles_group), FadeOut(count_caption))

        new_title = Text(
            "Same method. Messier concept.",
            font=S.FONT, font_size=26, color=S.FG,
        ).move_to(title.get_center())
        new_badge = Text(
            "concept: golden_gate (v1)   |   layer 21",
            font=S.FONT, font_size=20, color=S.FG_DIM,
        ).move_to(concept_badge.get_center())
        self.play(Transform(title, new_title), Transform(concept_badge, new_badge))

        # =========================================================
        # ACT 2 — GOLDEN GATE V1
        # =========================================================
        plane_g = make_plane([0.5, -0.4, 0], width=8.0, height=5.0)
        self.play(Create(plane_g))

        g_pos, g_neg, g_pos_mean, g_neg_mean, _ = project("golden_gate", layer=21)

        gg_legend = legend(
            'Golden Gate Bridge sentences',
            'generic bridge / SF landmark sentences',
            anchor=[-3.9, 2.1, 0],
        )
        self.play(FadeIn(gg_legend))
        self.wait(0.8)

        ex_pos_x, ex_pos_y = sample_point(g_pos, 0)
        ex_neg_x, ex_neg_y = sample_point(g_neg, 0)

        gg_ex_pos_dot = Dot(plane_g.c2p(ex_pos_x, ex_pos_y), radius=0.12, color=S.DATA)
        gg_ex_pos_caption = Text(
            f'"{GG_EXAMPLE_POS}"',
            font=S.FONT, font_size=18, color=S.DATA, slant="ITALIC",
        ).next_to(gg_ex_pos_dot, UP + RIGHT, buff=0.1)

        gg_ex_neg_dot = Dot(plane_g.c2p(ex_neg_x, ex_neg_y), radius=0.12, color=S.CONTENT_OTHER)
        gg_ex_neg_caption = Text(
            f'"{GG_EXAMPLE_NEG}"',
            font=S.FONT, font_size=18, color=S.CONTENT_OTHER, slant="ITALIC",
        ).next_to(gg_ex_neg_dot, DOWN + RIGHT, buff=0.1)

        self.play(FadeIn(gg_ex_pos_dot, scale=2), Write(gg_ex_pos_caption), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(gg_ex_neg_dot, scale=2), Write(gg_ex_neg_caption), run_time=1.2)

        note = Text(
            "Notice the sentences only differ in one phrase — the model's residual barely moves.",
            font=S.FONT, font_size=18, color=S.FG_DIM,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note))
        self.wait(1.8)

        small_gg_pos = Dot(plane_g.c2p(ex_pos_x, ex_pos_y), radius=0.07, color=S.DATA, fill_opacity=0.75)
        small_gg_neg = Dot(plane_g.c2p(ex_neg_x, ex_neg_y), radius=0.07, color=S.CONTENT_OTHER, fill_opacity=0.75)
        self.play(
            FadeOut(gg_ex_pos_caption), FadeOut(gg_ex_neg_caption),
            Transform(gg_ex_pos_dot, small_gg_pos),
            Transform(gg_ex_neg_dot, small_gg_neg),
            run_time=0.8,
        )

        gg_pos_dots = scatter(plane_g, g_pos[1:], S.DATA)
        gg_neg_dots = scatter(plane_g, g_neg[1:], S.CONTENT_OTHER)
        self.play(
            FadeIn(gg_pos_dots, lag_ratio=0.04),
            FadeIn(gg_neg_dots, lag_ratio=0.04),
            run_time=1.8,
        )
        self.wait(1.0)

        gg_pos_c = Dot(plane_g.c2p(float(g_pos_mean[0]), float(g_pos_mean[1])), radius=0.18, color=S.DATA)
        gg_neg_c = Dot(plane_g.c2p(float(g_neg_mean[0]), float(g_neg_mean[1])), radius=0.18, color=S.CONTENT_OTHER)
        self.play(FadeIn(gg_pos_c, scale=3), FadeIn(gg_neg_c, scale=3), run_time=1.0)
        gg_diff = Arrow(
            plane_g.c2p(float(g_neg_mean[0]), float(g_neg_mean[1])),
            plane_g.c2p(float(g_pos_mean[0]), float(g_pos_mean[1])),
            buff=0.12,
            color=S.STRUCTURE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.28,
        )
        self.play(Create(gg_diff), run_time=1.0)

        verdict_gg = Text(
            "clouds overlap → fuzzy direction, fuzzy steering",
            font=S.FONT, font_size=22, color=S.CONTENT_OTHER,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(note, verdict_gg))
        self.wait(2.2)

        # =========================================================
        # ACT 3 — SIDE BY SIDE
        # =========================================================
        gg_group = VGroup(
            plane_g, gg_legend, gg_ex_pos_dot, gg_ex_neg_dot,
            gg_pos_dots, gg_neg_dots, gg_pos_c, gg_neg_c, gg_diff,
        )
        self.play(FadeOut(gg_group), FadeOut(note))

        sxs_title = Text(
            "Side by side: the geometry predicts what you get",
            font=S.FONT, font_size=26, color=S.FG,
        ).move_to(title.get_center())
        sxs_badge = Text(
            "both at layer 21, α = 4",
            font=S.FONT, font_size=20, color=S.FG_DIM,
        ).move_to(concept_badge.get_center())
        self.play(Transform(title, sxs_title), Transform(concept_badge, sxs_badge))

        left_plane = make_plane([-3.4, -0.4, 0], width=5.0, height=4.4)
        right_plane = make_plane([3.4, -0.4, 0], width=5.0, height=4.4)

        left_label = Text("pickles", font=S.FONT, font_size=22, color=S.FG).next_to(left_plane, UP, buff=0.15)
        right_label = Text("golden_gate (v1)", font=S.FONT, font_size=22, color=S.FG).next_to(right_plane, UP, buff=0.15)

        self.play(
            Create(left_plane), Create(right_plane),
            FadeIn(left_label), FadeIn(right_label),
        )

        l_pos_dots = scatter(left_plane, p_pos, S.DATA, radius=0.05, opacity=0.7)
        l_neg_dots = scatter(left_plane, p_neg, S.CONTENT_OTHER, radius=0.05, opacity=0.7)
        l_pos_c = Dot(left_plane.c2p(*p_pos_mean[:2]), radius=0.13, color=S.DATA)
        l_neg_c = Dot(left_plane.c2p(*p_neg_mean[:2]), radius=0.13, color=S.CONTENT_OTHER)
        l_diff = Arrow(
            left_plane.c2p(*p_neg_mean[:2]),
            left_plane.c2p(*p_pos_mean[:2]),
            buff=0.08, color=S.STRUCTURE, stroke_width=5,
            max_tip_length_to_length_ratio=0.22,
        )

        r_pos_dots = scatter(right_plane, g_pos, S.DATA, radius=0.05, opacity=0.7)
        r_neg_dots = scatter(right_plane, g_neg, S.CONTENT_OTHER, radius=0.05, opacity=0.7)
        r_pos_c = Dot(right_plane.c2p(*g_pos_mean[:2]), radius=0.13, color=S.DATA)
        r_neg_c = Dot(right_plane.c2p(*g_neg_mean[:2]), radius=0.13, color=S.CONTENT_OTHER)
        r_diff = Arrow(
            right_plane.c2p(*g_neg_mean[:2]),
            right_plane.c2p(*g_pos_mean[:2]),
            buff=0.08, color=S.STRUCTURE, stroke_width=5,
            max_tip_length_to_length_ratio=0.28,
        )

        self.play(
            FadeIn(l_pos_dots, lag_ratio=0.02),
            FadeIn(l_neg_dots, lag_ratio=0.02),
            FadeIn(r_pos_dots, lag_ratio=0.02),
            FadeIn(r_neg_dots, lag_ratio=0.02),
            run_time=1.4,
        )
        self.play(
            FadeIn(l_pos_c, scale=2), FadeIn(l_neg_c, scale=2),
            FadeIn(r_pos_c, scale=2), FadeIn(r_neg_c, scale=2),
            run_time=0.8,
        )
        self.play(Create(l_diff), Create(r_diff), run_time=1.0)
        self.wait(0.8)

        left_quote = Text(
            f'→ "{PICKLE_GEN}"', font=S.FONT, font_size=19, color=S.DATA,
        ).next_to(left_plane, DOWN, buff=0.35)
        right_quote = Text(
            f'→ "{GG_GEN}"', font=S.FONT, font_size=19, color=S.CONTENT_OTHER,
        ).next_to(right_plane, DOWN, buff=0.35)

        self.play(FadeIn(left_quote), FadeIn(right_quote))
        self.wait(1.6)

        closing = Text(
            "sharp cloud separation → sharp concept.   fuzzy clouds → fuzzy concept.",
            font=S.FONT, font_size=22, color=S.STRUCTURE,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(closing))
        self.wait(3.0)
