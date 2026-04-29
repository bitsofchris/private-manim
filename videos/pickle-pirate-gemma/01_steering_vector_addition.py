"""Animation 1 — steering_vector_addition

The conceptual opener. In 2D:
  - h: residual stream vector at some layer (arrow from origin) — DATA
  - u: unit steering vector (mean(pickle) − mean(other)) — STRUCTURE (the discovered direction)
  - α grows 0 → 10; a scaled copy α · 0.1 · ‖h‖ · u fades in
  - h' = h + α·0.1·‖h‖·u rotates toward u — HIGHLIGHT (transformed result)
  - caption changes at α ∈ {0, 4, 10} with real outputs from runs.jsonl
    (pickles, layer 21).

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 01_steering_vector_addition.py SteeringVectorAddition
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
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Text,
    Transform,
    ValueTracker,
    Write,
    always_redraw,
)

from videos._shared import style as S
from videos._shared.base import BocScene
from videos._shared.mobjects import BocNumberPlane


CAPTIONS = {
    0.0: "pizza. I have this craving for pizza…",
    4.0: "pickled kraut…just little pickles made with sauerkraut",
    10.0: "pickled they pickle pickles they pickle pickles they…",
}

H = np.array([2.2, 0.9, 0.0])
U_DIR = np.array([-0.35, 1.0, 0.0])
U = U_DIR / np.linalg.norm(U_DIR) * 1.8
H_NORM = float(np.linalg.norm(H))
U_HAT = U / np.linalg.norm(U)


def injection(alpha: float) -> np.ndarray:
    return alpha * 0.1 * H_NORM * U_HAT


class SteeringVectorAddition(BocScene):
    def construct(self):
        title = Text(
            "Steering = vector addition in the residual stream",
            font=S.FONT, font_size=34, color=S.FG,
        ).to_edge(UP)
        self.play(FadeIn(title, shift=0.3 * DOWN))

        plane = BocNumberPlane(
            x_range=[-4, 4, 1], y_range=[-2, 4, 1],
            x_length=10, y_length=5.5,
        ).shift(0.2 * DOWN)
        self.play(Create(plane, run_time=0.8))

        origin = plane.c2p(0, 0)

        # h — residual stream vector (DATA, teal)
        h_arrow = Arrow(
            origin, plane.c2p(H[0], H[1]),
            buff=0, color=S.DATA, stroke_width=6,
        )
        h_label = Text("h", font=S.FONT, font_size=32, color=S.DATA, slant="ITALIC").next_to(
            h_arrow.get_end(), RIGHT, buff=0.15
        )
        h_caption = Text(
            "residual stream at layer 21",
            font=S.FONT, font_size=22, color=S.FG_DIM,
        ).next_to(h_label, RIGHT, buff=0.2)

        self.play(Create(h_arrow), Write(h_label), run_time=1.2)
        self.play(FadeIn(h_caption, shift=0.2 * RIGHT))
        self.wait(1.4)
        self.play(FadeOut(h_caption), FadeOut(title))

        # u — unit steering vector (STRUCTURE, magenta — discovered direction)
        u_arrow = Arrow(
            origin, plane.c2p(U[0], U[1]),
            buff=0, color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE,
        )
        u_label = Text(
            "û", font=S.FONT, font_size=32, color=S.STRUCTURE, slant="ITALIC",
        ).next_to(u_arrow.get_end(), LEFT, buff=0.15)
        u_caption = Text(
            "mean(pickle) − mean(other)",
            font=S.FONT, font_size=22, color=S.STRUCTURE,
        ).next_to(u_arrow.get_end(), UP, buff=0.15)

        self.play(Create(u_arrow), Write(u_label), run_time=1.2)
        self.play(FadeIn(u_caption, shift=0.2 * UP))
        self.wait(1.6)
        self.play(FadeOut(u_caption))

        alpha_tracker = ValueTracker(0.0)

        alpha_readout = always_redraw(
            lambda: Text(
                f"α = {alpha_tracker.get_value():.1f}",
                font=S.FONT, color=S.HIGHLIGHT, font_size=36,
            ).to_corner(UP + RIGHT, buff=0.6)
        )
        inj_formula = Text(
            "inject = α · 0.1 · ‖h‖ · û",
            font=S.FONT, font_size=24, color=S.FG_DIM,
        ).next_to(alpha_readout, DOWN, buff=0.25).align_to(alpha_readout, RIGHT)
        self.play(FadeIn(alpha_readout), FadeIn(inj_formula))

        def make_inj_arrow():
            a = alpha_tracker.get_value()
            inj = injection(a)
            if np.linalg.norm(inj) < 1e-3:
                return Arrow(
                    plane.c2p(H[0], H[1]),
                    plane.c2p(H[0] + 1e-3, H[1] + 1e-3),
                    buff=0, stroke_opacity=0,
                )
            return Arrow(
                plane.c2p(H[0], H[1]),
                plane.c2p(H[0] + inj[0], H[1] + inj[1]),
                buff=0, color=S.STRUCTURE, stroke_width=5,
            )

        inj_arrow = always_redraw(make_inj_arrow)

        def make_result_arrow():
            a = alpha_tracker.get_value()
            tip = H + injection(a)
            return Arrow(
                origin, plane.c2p(tip[0], tip[1]),
                buff=0, color=S.HIGHLIGHT, stroke_width=6,
            )

        result_arrow = always_redraw(make_result_arrow)

        def _result_label():
            tip = H + injection(alpha_tracker.get_value())
            direction = RIGHT if tip[1] > 2.8 else (UP + RIGHT)
            return Text(
                "h + inject",
                font=S.FONT, color=S.HIGHLIGHT, font_size=22, slant="ITALIC",
            ).next_to(plane.c2p(tip[0], tip[1]), direction, buff=0.15)

        result_label = always_redraw(_result_label)

        h_ghost = DashedLine(
            origin, plane.c2p(H[0], H[1]),
            dash_length=0.12, stroke_color=S.FG_DIM, stroke_opacity=0.6,
        )

        self.play(
            FadeIn(h_ghost), FadeIn(inj_arrow), FadeIn(result_arrow), Write(result_label),
            run_time=1.2,
        )

        caption_box = Text(
            CAPTIONS[0.0], font=S.FONT, font_size=26, color=S.FG,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption_box))
        self.wait(1.0)

        def set_caption(new_text: str):
            nonlocal caption_box
            new_box = Text(
                new_text, font=S.FONT, font_size=26, color=S.FG,
            ).to_edge(DOWN, buff=0.5)
            self.play(Transform(caption_box, new_box), run_time=0.7)

        self.play(alpha_tracker.animate.set_value(4.0), run_time=5.0)
        set_caption(CAPTIONS[4.0])
        self.wait(1.5)

        self.play(alpha_tracker.animate.set_value(10.0), run_time=5.5)
        set_caption(CAPTIONS[10.0])
        self.wait(2.5)
