"""Blog visual 7 — three-vector composition.

Two acts.

Act 1 — Tip-to-tail. Three steering vectors compose on a 2D plane:
  • pirate  (brown)
  • pickle  (green)
  • golden gate  (rust/gold)
No captions, no generated text panel. Just the additive geometry.

Act 2 — Familiar steering dashboard, three concepts. Three meters fill as
the model output ladder advances through the real composition runs from
runs.jsonl, ending on "Golden Dreadken".

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql blog07_composition.py Composition
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
    Create,
    Dot,
    Ellipse,
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
from videos._shared.mobjects import BocNumberPlane


PROMPT = "The best adventure I can imagine is"

# Real outputs from runs.jsonl. Three stages, all with the same prompt.
# Stage 0 = baseline. Stage 1 = California Gilbertos composition.
# Stage 2 = Golden Dreadken composition.
LADDER = [
    (
        0.0,
        "something in between…\n"
        "I am fond of good stories. I like them simple,\n"
        "and I like them very much when I can predict\n"
        "the end.",
        S.FG,
    ),
    (
        0.55,
        "on a boat… setting sail aboard the\n"
        "California Gilbertos! What a blast to\n"
        "discover these legendary California\n"
        "sea-slingers and their raucous,\n"
        "rollickin' re-runnings!",
        S.FG,
    ),
    (
        1.0,
        "a weekend trip to this year's San Jon-Juast\n"
        "Everstereen-Nerdfest aboard the Golden\n"
        "Dreadken, aka the San Jon-Juast\n"
        "Everstereen-Nerdfests' very own…",
        S.HIGHLIGHT,
    ),
]


# Tip-to-tail vectors (same as before).
V_PIRATE = np.array([2.0, 1.0])
V_PICKLE = np.array([0.0, -2.0])
V_GG = np.array([2.6, 0.5])


# ----- icon helpers -----

def make_bridge(center, scale=1.0, color=S.CONTENT_RUST, stroke_width=2.0) -> VGroup:
    cx, cy, _ = center
    s = scale
    pl = Line([cx - 0.30 * s, cy - 0.18 * s, 0], [cx - 0.30 * s, cy + 0.32 * s, 0],
              color=color, stroke_width=stroke_width)
    pr = Line([cx + 0.30 * s, cy - 0.18 * s, 0], [cx + 0.30 * s, cy + 0.32 * s, 0],
              color=color, stroke_width=stroke_width)
    deck = Line([cx - 0.42 * s, cy - 0.06 * s, 0], [cx + 0.42 * s, cy - 0.06 * s, 0],
                color=color, stroke_width=stroke_width)
    cl = Line([cx - 0.30 * s, cy + 0.32 * s, 0], [cx - 0.42 * s, cy - 0.06 * s, 0],
              color=color, stroke_width=max(1.0, stroke_width - 0.5))
    cr = Line([cx + 0.30 * s, cy + 0.32 * s, 0], [cx + 0.42 * s, cy - 0.06 * s, 0],
              color=color, stroke_width=max(1.0, stroke_width - 0.5))
    ct = Line([cx - 0.30 * s, cy + 0.32 * s, 0], [cx + 0.30 * s, cy + 0.32 * s, 0],
              color=color, stroke_width=max(1.0, stroke_width - 0.5))
    return VGroup(pl, pr, deck, cl, cr, ct)


def make_pickle(center, scale=1.0, color=S.CONTENT_PICKLE) -> Ellipse:
    return Ellipse(
        width=0.34 * scale, height=0.78 * scale,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=0.55,
    ).move_to(center)


def make_pirate(center, scale=1.0, color=S.CONTENT_PIRATE, stroke_width=2.5) -> VGroup:
    """Crossed swords — two diagonal lines forming an X."""
    cx, cy, _ = center
    s = scale
    a = Line([cx - 0.32 * s, cy - 0.28 * s, 0], [cx + 0.32 * s, cy + 0.28 * s, 0],
             color=color, stroke_width=stroke_width)
    b = Line([cx + 0.32 * s, cy - 0.28 * s, 0], [cx - 0.32 * s, cy + 0.28 * s, 0],
             color=color, stroke_width=stroke_width)
    # Tiny pommels at the bottom tips.
    p1 = Dot([cx - 0.32 * s, cy - 0.28 * s, 0], color=color, radius=0.04 * s)
    p2 = Dot([cx + 0.32 * s, cy - 0.28 * s, 0], color=color, radius=0.04 * s)
    return VGroup(a, b, p1, p2)


def wrap(text: str, width: int = 34) -> str:
    out = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        cur = ""
        for w in words:
            if len(cur) + len(w) + 1 <= width:
                cur = (cur + " " + w).strip()
            else:
                out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return "\n".join(out[:7])


class Composition(BocScene):
    def construct(self):
        self.act1_tip_to_tail()
        self.act2_three_meters()

    # ---------------- Act 1: tip-to-tail composition ----------------
    def act1_tip_to_tail(self):
        plane = BocNumberPlane(
            x_range=[-2, 6, 1], y_range=[-3, 3, 1], x_length=9, y_length=6,
        ).shift(0.2 * DOWN + 1.5 * LEFT)
        self.play(Create(plane, run_time=0.7))

        origin = np.array([0.0, 0.0])
        p0 = origin
        p1 = p0 + V_PIRATE
        p2 = p1 + V_PICKLE
        p3 = p2 + V_GG

        def make_arrow(start, end, color, label_text, side=1, offset=0.5):
            arr = Arrow(
                plane.c2p(start[0], start[1]),
                plane.c2p(end[0], end[1]),
                buff=0.05, color=color, stroke_width=6,
            )
            s = np.array(arr.get_start())
            e = np.array(arr.get_end())
            mid = (s + e) / 2
            d = e - s
            n = float(np.linalg.norm(d[:2]))
            perp = (
                np.array([-d[1] / n, d[0] / n, 0.0]) if n > 1e-6
                else np.array([0.0, 1.0, 0.0])
            )
            lbl = Text(label_text, font=S.FONT, font_size=22, color=color).move_to(
                mid + side * offset * perp
            )
            return arr, lbl

        origin_dot = Dot(plane.c2p(0, 0), color=S.FG, radius=0.08)
        self.play(FadeIn(origin_dot))

        # Walking marker.
        marker = Dot(plane.c2p(0, 0), color=S.HIGHLIGHT, radius=0.16)
        self.add(marker)

        arr1, lbl1 = make_arrow(p0, p1, S.CONTENT_PIRATE, "+ pirate", side=+1)
        self.play(Create(arr1), FadeIn(lbl1))
        self.play(marker.animate.move_to(plane.c2p(p1[0], p1[1])), run_time=0.6)
        self.beat("QUICK")

        arr2, lbl2 = make_arrow(p1, p2, S.CONTENT_PICKLE, "+ pickle", side=-1, offset=0.7)
        self.play(Create(arr2), FadeIn(lbl2))
        self.play(marker.animate.move_to(plane.c2p(p2[0], p2[1])), run_time=0.6)
        self.beat("QUICK")

        arr3, lbl3 = make_arrow(p2, p3, S.CONTENT_GOLD, "+ golden gate", side=-1, offset=0.6)
        self.play(Create(arr3), FadeIn(lbl3))
        self.play(marker.animate.move_to(plane.c2p(p3[0], p3[1])), run_time=0.6)
        self.beat("BEAT")

        # Clear the plane to set up the dashboard view.
        self.play(
            FadeOut(VGroup(
                plane, origin_dot, marker,
                arr1, lbl1, arr2, lbl2, arr3, lbl3,
            )),
            run_time=S.BEAT,
        )

    # ---------------- Act 2: three-concept dashboard ----------------
    def act2_three_meters(self):
        prompt_label = Text(
            "prompt:", font=S.FONT, font_size=22, color=S.FG_DIM,
        ).to_corner(UP + LEFT, buff=0.6)
        prompt_text = Text(
            f'"{PROMPT}"', font=S.FONT, font_size=24, color=S.FG, slant="ITALIC",
        ).next_to(prompt_label, RIGHT, buff=0.25)
        self.play(FadeIn(prompt_label), FadeIn(prompt_text))

        panel = Rectangle(
            width=8.5, height=4.4,
            stroke_color=S.FG_DIM, stroke_width=2, fill_opacity=0,
        ).move_to([-2.0, -0.4, 0])
        self.play(Create(panel, run_time=0.5))

        current_text = Text(
            wrap(LADDER[0][1]),
            font=S.FONT, font_size=24, color=LADDER[0][2], line_spacing=0.95,
        ).move_to(panel.get_center())
        self.play(Write(current_text), run_time=1.2)

        fill_tracker = ValueTracker(0.0)

        # ---------- Right-half dashboard: three concept rows + meters ----------
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

        self.play(Create(dashboard), FadeIn(dash_header), run_time=0.5)

        # Three rows. Each row has: icon | name | horizontal meter bar.
        rows = [
            ("pirate", S.CONTENT_PIRATE, make_pirate),
            ("pickle", S.CONTENT_PICKLE, make_pickle),
            ("golden gate", S.CONTENT_RUST, make_bridge),
        ]

        ROW_TOP = DASH_CY + DASH_H / 2 - 1.15
        ROW_GAP = 1.8
        BAR_GAP = 0.5
        BAR_W = 3.1
        BAR_H = 0.22

        ICON_X = DASH_X - DASH_W / 2 + 0.5
        NAME_LEFT = ICON_X + 0.55  # left edge of the name label
        BAR_X = DASH_X

        def make_meter_fill(idx: int, color):
            bar_y = ROW_TOP - idx * ROW_GAP - BAR_GAP
            bar_left = BAR_X - BAR_W / 2 + 0.04
            bar_right = BAR_X + BAR_W / 2 - 0.04
            inner_w = bar_right - bar_left

            def _build():
                f = float(np.clip(fill_tracker.get_value(), 0, 1))
                w = max(0.001, inner_w * f)
                fill = Rectangle(
                    width=w, height=BAR_H - 0.08,
                    stroke_width=0,
                    fill_color=color, fill_opacity=0.85,
                )
                fill.move_to([bar_left + w / 2, bar_y, 0])
                return fill
            return _build

        # Build all three rows.
        all_row_artifacts = []
        meter_fills = []
        for idx, (name, color, icon_fn) in enumerate(rows):
            row_y = ROW_TOP - idx * ROW_GAP

            # Icon
            icon = icon_fn([ICON_X, row_y, 0])
            # Recolor pickle icon since make_pickle defaults green
            if name == "pirate":
                icon = make_pirate([ICON_X, row_y, 0], scale=1.0)
            elif name == "pickle":
                icon = make_pickle([ICON_X, row_y, 0], scale=1.0)
            else:
                icon = make_bridge([ICON_X, row_y, 0], scale=0.9, color=color, stroke_width=2.2)

            # Name (left-aligned to NAME_LEFT, sitting beside the icon).
            name_lbl = Text(
                name, font=S.FONT, font_size=18, color=S.FG, weight="BOLD",
            )
            name_lbl.move_to([NAME_LEFT, row_y, 0]).align_to(
                [NAME_LEFT, row_y, 0], LEFT
            )

            # Meter frame — sits below the icon+name row.
            frame = RoundedRectangle(
                width=BAR_W, height=BAR_H, corner_radius=0.05,
                stroke_color=S.FG_DIM, stroke_width=1.4, fill_opacity=0,
            ).move_to([BAR_X, row_y - BAR_GAP, 0])

            # Animated fill
            fill_redraw = always_redraw(make_meter_fill(idx, color))
            meter_fills.append(fill_redraw)

            self.play(
                FadeIn(icon), FadeIn(name_lbl), Create(frame), FadeIn(fill_redraw),
                run_time=0.4,
            )
            all_row_artifacts.extend([icon, name_lbl, frame])

        self.wait(0.6)

        # Step the ladder. Each step both fills the meters and morphs text.
        def advance(target_fill: float, snippet: str, color):
            nonlocal current_text
            new_text = Text(
                wrap(snippet),
                font=S.FONT, font_size=24, color=color, line_spacing=0.95,
            ).move_to(panel.get_center())
            self.play(
                fill_tracker.animate.set_value(target_fill),
                Transform(current_text, new_text),
                run_time=3.0,
            )
            self.wait(2.6)

        for fill, snippet, color in LADDER[1:]:
            advance(fill, snippet, color)

        # Hold on Golden Dreadken; emphasize the invented word.
        self.wait(1.0)
        dreadken = Text(
            "Golden Dreadken",
            font=S.FONT, font_size=44, color=S.HIGHLIGHT, weight="BOLD",
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(dreadken, scale=1.15), run_time=S.BEAT)
        self.wait(2.0)
