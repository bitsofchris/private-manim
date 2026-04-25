"""Blog visual 7 — three-vector composition.

Three arrows drawn tip-to-tail on a 2D plane, one per concept:
  • pirate  (brown)
  • pickle  (green)
  • golden gate  (rust)

As each arrow is added, a composite output marker slides further. At the
tip, the invented word "Golden Dreadken" materializes by splicing
"Golden" + "Kraken".

Pulled from runs.jsonl (multilayer pirate@L12 α6 · pickles@L21 α3 ·
golden_gate_v2@L24 α5).
"""

from __future__ import annotations

import numpy as np
from manim import (
    DARK_BROWN,
    DOWN,
    GOLD,
    GREEN,
    GREY_B,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    NumberPlane,
    Scene,
    Text,
    VGroup,
    Write,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


# Three steering-vector "directions" drawn tip-to-tail. Cartoon 2D — each
# arrow points at a clearly different angle. Golden Gate is intentionally
# the flattest (mostly horizontal) so the three slopes read as distinct.
V_PIRATE = np.array([2.0, 1.0])    # up-right diagonal
V_PICKLE = np.array([0.0, -2.0])   # straight down into the brine
V_GG = np.array([2.6, 0.5])        # mostly horizontal, gentle rise

RUST = GOLD  # golden-gate arrow color — bright, distinct from pirate brown


class Composition(Scene):
    def construct(self):
        title = Text(
            "three directions, one sentence",
            font_size=36,
            color=WHITE,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=0.2 * DOWN))

        plane = NumberPlane(
            x_range=[-2, 6, 1],
            y_range=[-3, 3, 1],
            x_length=9,
            y_length=6,
            background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.2},
            axis_config={"stroke_color": GREY_B, "stroke_opacity": 0.4},
        ).shift(0.2 * DOWN + 1.5 * LEFT)
        self.play(Create(plane, run_time=0.7))

        origin = np.array([0.0, 0.0])
        p0 = origin
        p1 = p0 + V_PIRATE
        p2 = p1 + V_PICKLE
        p3 = p2 + V_GG

        def make_arrow(start, end, color, label_text, side=1, offset=0.5):
            """Draw arrow + label. Label sits perpendicular to the shaft so it
            never overlaps. ``side=+1`` = left of arrow direction (CCW),
            ``side=-1`` = right."""
            arr = Arrow(
                plane.c2p(start[0], start[1]),
                plane.c2p(end[0], end[1]),
                buff=0.05,
                color=color,
                stroke_width=6,
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
            lbl = Text(label_text, font_size=22, color=color).move_to(
                mid + side * offset * perp
            )
            return arr, lbl

        origin_dot = Dot(plane.c2p(0, 0), color=WHITE, radius=0.08)
        self.play(FadeIn(origin_dot))

        # A rolling "output" marker advances with each concept.
        marker = Dot(plane.c2p(0, 0), color=YELLOW, radius=0.16)
        self.add(marker)

        # Small side panel that accumulates output snippets as arrows activate.
        side_anchor = np.array([4.2, 2.5, 0])
        side_title = Text("generated:", font_size=20, color=GREY_B).move_to(side_anchor).align_to(
            np.array([4.2, 2.5, 0]), LEFT
        )
        self.play(FadeIn(side_title))

        # --- pirate --- (label above the rightward shaft)
        arr1, lbl1 = make_arrow(p0, p1, DARK_BROWN, "+ pirate", side=+1)
        self.play(Create(arr1), FadeIn(lbl1))
        self.play(marker.animate.move_to(plane.c2p(p1[0], p1[1])), run_time=0.8)
        pirate_out = Text(
            "\"sea-slingers…\"",
            font_size=18,
            color=DARK_BROWN,
        ).next_to(side_title, DOWN, buff=0.3).align_to(side_title, LEFT)
        self.play(Write(pirate_out))
        self.wait(0.6)

        # --- pickle --- (straight-down shaft; label to the LEFT of the arrow)
        arr2, lbl2 = make_arrow(p1, p2, GREEN, "+ pickle", side=-1, offset=0.7)
        self.play(Create(arr2), FadeIn(lbl2))
        self.play(marker.animate.move_to(plane.c2p(p2[0], p2[1])), run_time=0.8)
        pickle_out = Text(
            "\"pickle-a-de-do, larf…\"",
            font_size=18,
            color=GREEN,
        ).next_to(pirate_out, DOWN, buff=0.25).align_to(pirate_out, LEFT)
        self.play(Write(pickle_out))
        self.wait(0.6)

        # --- golden gate --- (mostly horizontal shaft; label to the RIGHT/below
        # the arrow so it sits opposite the pickle label across the canvas)
        arr3, lbl3 = make_arrow(p2, p3, RUST, "+ golden gate", side=-1, offset=0.6)
        self.play(Create(arr3), FadeIn(lbl3))
        self.play(marker.animate.move_to(plane.c2p(p3[0], p3[1])), run_time=0.8)
        gg_out = Text(
            "\"Golden Dreadken\"",
            font_size=20,
            color=YELLOW,
        ).next_to(pickle_out, DOWN, buff=0.25).align_to(pickle_out, LEFT)
        self.play(Write(gg_out))
        self.wait(0.6)

        # --- Materialize "Golden Dreadken" at the tip ---
        # Two source fragments slide in from pirate arrow end and golden arrow
        # end, then collide and merge into "Golden Dreadken" at the tip.
        golden_src = Text("Golden", font_size=28, color=RUST).move_to(
            plane.c2p(p2[0] + V_GG[0] * 0.4, p2[1] + V_GG[1] * 0.4 - 0.4)
        )
        kraken_src = Text("Kraken", font_size=28, color=DARK_BROWN).move_to(
            plane.c2p(p1[0] - 0.2, p1[1] - 0.8)
        )
        self.play(FadeIn(golden_src), FadeIn(kraken_src))
        self.wait(0.3)

        tip_world = plane.c2p(p3[0], p3[1])
        # Land the merged word in the top-center "headline" zone — well above
        # all three arrow tips so the 40pt text never collides with the path.
        merge_pt = np.array([0.5, 1.7, 0.0])
        self.play(
            golden_src.animate.move_to(merge_pt + np.array([-0.6, 0, 0])),
            kraken_src.animate.move_to(merge_pt + np.array([0.6, 0, 0])),
            run_time=1.2,
        )

        merged = Text(
            "Golden Dreadken",
            font_size=40,
            color=YELLOW,
        ).move_to(merge_pt)
        self.play(FadeOut(golden_src), FadeOut(kraken_src), FadeIn(merged, scale=1.3))
        self.wait(0.5)

        # final caption
        caption = Text(
            "a word the model had to invent",
            font_size=26,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.45)
        self.play(Write(caption))
        self.wait(2.0)
