"""Animation 3 — pca_with_steering_arrow (geometry → behavior bridge).

Walks through *how* a steering vector is extracted from data, then
contrasts the clean case (pickles) with the messy case (golden_gate v1).

Act 1 — pickles, full canvas:
    - Two example minimal-pair sentences fly in as labeled dots
      (blue = positive class, orange = negative class).
    - The rest of the 30+30 points fade in.
    - Centroids pop. Yellow diff arrow appears. Caption: "linearly separable".

Act 2 — golden_gate v1, full canvas (swipe over):
    - Same walkthrough. Example pair is a bridge sentence vs a
      non-bridge-sentence. Clouds overlap heavily; arrow is short.
    - Caption: "overlapping — fuzzy direction".

Act 3 — side by side:
    - Both plots shrink to panels. A quote from the actual generation at
      layer 21, α=4 appears below each: sharp pickles text vs fuzzy
      coastal-California text. Caption: "geometry → behavior".
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREY_B,
    GREY_D,
    LEFT,
    ORANGE,
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
    NumberPlane,
    Rectangle,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
    config,
)

from _pca_data import project

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


# Example minimal pairs (pulled from sentences.json).
PICKLE_EXAMPLE_POS = "Pickles are my favorite snack any time of day."
PICKLE_EXAMPLE_NEG = "Pizza is my favorite meal any time of day."

GG_EXAMPLE_POS = "The Golden Gate Bridge stretches across San Francisco Bay."
GG_EXAMPLE_NEG = "The Bay Bridge stretches across San Francisco to Oakland."

# Real generations at layer 21, α=4 for the side-by-side payoff.
PICKLE_GEN = "… pickled kraut, little pickles made with sauerkraut …"
GG_GEN = "… the beach. I was born in a coastal town, so I grew up on the beach …"


def make_plane(center, width=8.0, height=5.0):
    return NumberPlane(
        x_range=[-2.5, 2.5, 1],
        y_range=[-2.5, 2.5, 1],
        x_length=width,
        y_length=height,
        background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.2},
        axis_config={"stroke_color": GREY_B, "stroke_opacity": 0.4},
    ).move_to(center)


def scatter(plane, pts, color, radius=0.07, opacity=0.75):
    dots = VGroup()
    for p in pts:
        x, y = float(p[0]), float(p[1])
        x = max(min(x, 2.4), -2.4)
        y = max(min(y, 2.4), -2.4)
        dots.add(
            Dot(plane.c2p(x, y), radius=radius, color=color, fill_opacity=opacity)
        )
    return dots


def legend(pos_label: str, neg_label: str, anchor, pos_color=BLUE, neg_color=ORANGE):
    """Small legend box showing what blue vs orange dots mean."""
    pos_dot = Dot(radius=0.09, color=pos_color, fill_opacity=0.9)
    pos_txt = Text(pos_label, font_size=18, color=WHITE).next_to(pos_dot, RIGHT, buff=0.2)
    row1 = VGroup(pos_dot, pos_txt)

    neg_dot = Dot(radius=0.09, color=neg_color, fill_opacity=0.9)
    neg_txt = Text(neg_label, font_size=18, color=WHITE).next_to(neg_dot, RIGHT, buff=0.2)
    row2 = VGroup(neg_dot, neg_txt)

    box = VGroup(row1, row2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    bg = Rectangle(
        width=box.width + 0.4,
        height=box.height + 0.3,
        stroke_color=GREY_D,
        stroke_width=1.5,
        fill_color="#101010",
        fill_opacity=0.6,
    ).move_to(box.get_center())
    group = VGroup(bg, box).move_to(anchor)
    return group


def sample_point(pts: np.ndarray, idx: int) -> tuple[float, float]:
    p = pts[idx]
    return float(p[0]), float(p[1])


class PCAWithSteeringArrow(Scene):
    def construct(self):
        # =========================================================
        # ACT 1 — PICKLES
        # =========================================================
        title = Text(
            "Step 1: build a mean-difference vector from matched sentences",
            font_size=26,
            color=WHITE,
        ).to_edge(UP, buff=0.35)
        concept_badge = Text(
            "concept: pickles   |   layer 21",
            font_size=20,
            color=GREY_B,
        ).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(concept_badge))

        plane = make_plane([0.5, -0.4, 0], width=8.0, height=5.0)
        self.play(Create(plane))

        # Precompute pickles PCA
        p_pos, p_neg, p_pos_mean, p_neg_mean, _ = project("pickles", layer=21)

        # Legend (top-left of plane)
        pickle_legend = legend(
            'pickle sentences  ("Pickles are my favorite snack…")',
            'food sentences     ("Pizza is my favorite meal…")',
            anchor=[-3.9, 2.1, 0],
        )
        self.play(FadeIn(pickle_legend))
        self.wait(1.0)

        # --- Example pair flies in --------------------------------
        ex_pos_x, ex_pos_y = sample_point(p_pos, 0)
        ex_neg_x, ex_neg_y = sample_point(p_neg, 0)

        ex_pos_dot = Dot(plane.c2p(ex_pos_x, ex_pos_y), radius=0.12, color=BLUE)
        ex_pos_caption = Text(
            f'"{PICKLE_EXAMPLE_POS}"',
            font_size=18,
            color=BLUE,
            slant="ITALIC",
        ).next_to(ex_pos_dot, UP + RIGHT, buff=0.1)

        ex_neg_dot = Dot(plane.c2p(ex_neg_x, ex_neg_y), radius=0.12, color=ORANGE)
        ex_neg_caption = Text(
            f'"{PICKLE_EXAMPLE_NEG}"',
            font_size=18,
            color=ORANGE,
            slant="ITALIC",
        ).next_to(ex_neg_dot, DOWN + RIGHT, buff=0.1)

        self.play(FadeIn(ex_pos_dot, scale=2), Write(ex_pos_caption), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(ex_neg_dot, scale=2), Write(ex_neg_caption), run_time=1.2)
        self.wait(1.4)

        # Shrink the example dots to match the rest, fade captions
        small_ex_pos = Dot(plane.c2p(ex_pos_x, ex_pos_y), radius=0.07, color=BLUE, fill_opacity=0.75)
        small_ex_neg = Dot(plane.c2p(ex_neg_x, ex_neg_y), radius=0.07, color=ORANGE, fill_opacity=0.75)
        self.play(
            FadeOut(ex_pos_caption),
            FadeOut(ex_neg_caption),
            Transform(ex_pos_dot, small_ex_pos),
            Transform(ex_neg_dot, small_ex_neg),
            run_time=0.8,
        )

        # --- The rest of 30+30 --------------------------------------
        pos_dots = scatter(plane, p_pos[1:], BLUE)
        neg_dots = scatter(plane, p_neg[1:], ORANGE)
        count_caption = Text(
            "…30 sentences of each, encoded and projected to 2D",
            font_size=20,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(count_caption))
        self.play(
            FadeIn(pos_dots, lag_ratio=0.04),
            FadeIn(neg_dots, lag_ratio=0.04),
            run_time=2.0,
        )
        self.wait(1.0)

        # --- Centroids + diff arrow --------------------------------
        step2 = Text(
            "Step 2: take the mean of each cloud",
            font_size=22,
            color=WHITE,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(count_caption, step2))

        pos_centroid = Dot(
            plane.c2p(float(p_pos_mean[0]), float(p_pos_mean[1])),
            radius=0.18, color=BLUE,
        )
        neg_centroid = Dot(
            plane.c2p(float(p_neg_mean[0]), float(p_neg_mean[1])),
            radius=0.18, color=ORANGE,
        )
        self.play(FadeIn(pos_centroid, scale=3), FadeIn(neg_centroid, scale=3), run_time=1.0)
        self.wait(1.0)

        step3 = Text(
            'Step 3: subtract. The arrow IS the steering vector — the "pickle direction."',
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(count_caption, step3))

        diff_arrow = Arrow(
            plane.c2p(float(p_neg_mean[0]), float(p_neg_mean[1])),
            plane.c2p(float(p_pos_mean[0]), float(p_pos_mean[1])),
            buff=0.12,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(Create(diff_arrow), run_time=1.2)
        self.wait(1.6)

        verdict_pickles = Text(
            "clouds cleanly separated → sharp steering signal",
            font_size=22,
            color=BLUE,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(count_caption, verdict_pickles))
        self.wait(2.2)

        # =========================================================
        # TRANSITION — clear pickles, bring in golden_gate
        # =========================================================
        pickles_group = VGroup(
            plane, pickle_legend, ex_pos_dot, ex_neg_dot,
            pos_dots, neg_dots, pos_centroid, neg_centroid, diff_arrow,
        )
        self.play(FadeOut(pickles_group), FadeOut(count_caption))

        new_title = Text(
            "Same method. Messier concept.",
            font_size=26,
            color=WHITE,
        ).move_to(title.get_center())
        new_badge = Text(
            "concept: golden_gate (v1)   |   layer 21",
            font_size=20,
            color=GREY_B,
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

        # Example pair
        ex_pos_x, ex_pos_y = sample_point(g_pos, 0)
        ex_neg_x, ex_neg_y = sample_point(g_neg, 0)

        gg_ex_pos_dot = Dot(plane_g.c2p(ex_pos_x, ex_pos_y), radius=0.12, color=BLUE)
        gg_ex_pos_caption = Text(
            f'"{GG_EXAMPLE_POS}"',
            font_size=18, color=BLUE, slant="ITALIC",
        ).next_to(gg_ex_pos_dot, UP + RIGHT, buff=0.1)

        gg_ex_neg_dot = Dot(plane_g.c2p(ex_neg_x, ex_neg_y), radius=0.12, color=ORANGE)
        gg_ex_neg_caption = Text(
            f'"{GG_EXAMPLE_NEG}"',
            font_size=18, color=ORANGE, slant="ITALIC",
        ).next_to(gg_ex_neg_dot, DOWN + RIGHT, buff=0.1)

        self.play(FadeIn(gg_ex_pos_dot, scale=2), Write(gg_ex_pos_caption), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(gg_ex_neg_dot, scale=2), Write(gg_ex_neg_caption), run_time=1.2)

        note = Text(
            "Notice the sentences only differ in one phrase — the model's residual barely moves.",
            font_size=18,
            color=GREY_B,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note))
        self.wait(1.8)

        # Shrink
        small_gg_pos = Dot(plane_g.c2p(ex_pos_x, ex_pos_y), radius=0.07, color=BLUE, fill_opacity=0.75)
        small_gg_neg = Dot(plane_g.c2p(ex_neg_x, ex_neg_y), radius=0.07, color=ORANGE, fill_opacity=0.75)
        self.play(
            FadeOut(gg_ex_pos_caption),
            FadeOut(gg_ex_neg_caption),
            Transform(gg_ex_pos_dot, small_gg_pos),
            Transform(gg_ex_neg_dot, small_gg_neg),
            run_time=0.8,
        )

        # Full clouds
        gg_pos_dots = scatter(plane_g, g_pos[1:], BLUE)
        gg_neg_dots = scatter(plane_g, g_neg[1:], ORANGE)
        self.play(
            FadeIn(gg_pos_dots, lag_ratio=0.04),
            FadeIn(gg_neg_dots, lag_ratio=0.04),
            run_time=1.8,
        )
        self.wait(1.0)

        # Centroids + diff
        gg_pos_c = Dot(plane_g.c2p(float(g_pos_mean[0]), float(g_pos_mean[1])), radius=0.18, color=BLUE)
        gg_neg_c = Dot(plane_g.c2p(float(g_neg_mean[0]), float(g_neg_mean[1])), radius=0.18, color=ORANGE)
        self.play(FadeIn(gg_pos_c, scale=3), FadeIn(gg_neg_c, scale=3), run_time=1.0)
        gg_diff = Arrow(
            plane_g.c2p(float(g_neg_mean[0]), float(g_neg_mean[1])),
            plane_g.c2p(float(g_pos_mean[0]), float(g_pos_mean[1])),
            buff=0.12,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.28,
        )
        self.play(Create(gg_diff), run_time=1.0)

        verdict_gg = Text(
            "clouds overlap → fuzzy direction, fuzzy steering",
            font_size=22,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.45)
        self.play(Transform(note, verdict_gg))
        self.wait(2.2)

        # =========================================================
        # ACT 3 — SIDE BY SIDE
        # =========================================================
        # Clear golden_gate
        gg_group = VGroup(
            plane_g, gg_legend, gg_ex_pos_dot, gg_ex_neg_dot,
            gg_pos_dots, gg_neg_dots, gg_pos_c, gg_neg_c, gg_diff,
        )
        self.play(FadeOut(gg_group), FadeOut(note))

        # New title
        sxs_title = Text(
            "Side by side: the geometry predicts what you get",
            font_size=26,
            color=WHITE,
        ).move_to(title.get_center())
        sxs_badge = Text(
            "both at layer 21, α = 4",
            font_size=20,
            color=GREY_B,
        ).move_to(concept_badge.get_center())
        self.play(Transform(title, sxs_title), Transform(concept_badge, sxs_badge))

        # Two small planes
        left_plane = make_plane([-3.4, -0.4, 0], width=5.0, height=4.4)
        right_plane = make_plane([3.4, -0.4, 0], width=5.0, height=4.4)

        left_label = Text("pickles", font_size=22, color=WHITE).next_to(left_plane, UP, buff=0.15)
        right_label = Text("golden_gate (v1)", font_size=22, color=WHITE).next_to(right_plane, UP, buff=0.15)

        self.play(
            Create(left_plane), Create(right_plane),
            FadeIn(left_label), FadeIn(right_label),
        )

        # Recompute and render the little versions
        l_pos_dots = scatter(left_plane, p_pos, BLUE, radius=0.05, opacity=0.7)
        l_neg_dots = scatter(left_plane, p_neg, ORANGE, radius=0.05, opacity=0.7)
        l_pos_c = Dot(left_plane.c2p(*p_pos_mean[:2]), radius=0.13, color=BLUE)
        l_neg_c = Dot(left_plane.c2p(*p_neg_mean[:2]), radius=0.13, color=ORANGE)
        l_diff = Arrow(
            left_plane.c2p(*p_neg_mean[:2]),
            left_plane.c2p(*p_pos_mean[:2]),
            buff=0.08, color=YELLOW, stroke_width=5,
            max_tip_length_to_length_ratio=0.22,
        )

        r_pos_dots = scatter(right_plane, g_pos, BLUE, radius=0.05, opacity=0.7)
        r_neg_dots = scatter(right_plane, g_neg, ORANGE, radius=0.05, opacity=0.7)
        r_pos_c = Dot(right_plane.c2p(*g_pos_mean[:2]), radius=0.13, color=BLUE)
        r_neg_c = Dot(right_plane.c2p(*g_neg_mean[:2]), radius=0.13, color=ORANGE)
        r_diff = Arrow(
            right_plane.c2p(*g_neg_mean[:2]),
            right_plane.c2p(*g_pos_mean[:2]),
            buff=0.08, color=YELLOW, stroke_width=5,
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

        # Payoff quotes beneath each plot
        left_quote = Text(
            f'→ "{PICKLE_GEN}"',
            font_size=19, color=BLUE,
        ).next_to(left_plane, DOWN, buff=0.35)
        right_quote = Text(
            f'→ "{GG_GEN}"',
            font_size=19, color=ORANGE,
        ).next_to(right_plane, DOWN, buff=0.35)

        self.play(FadeIn(left_quote), FadeIn(right_quote))
        self.wait(1.6)

        closing = Text(
            "sharp cloud separation → sharp concept.   fuzzy clouds → fuzzy concept.",
            font_size=22,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(closing))
        self.wait(3.0)
