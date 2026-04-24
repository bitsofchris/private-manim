"""Animation 1 — steering_vector_addition

The conceptual opener. In 2D:
  - h: residual stream vector at some layer (arrow from origin)
  - u: unit steering vector (mean(pickle) − mean(other))
  - α grows 0 → 10; a scaled copy  α · 0.1 · ||h|| · u  fades in
  - h' = h + α·0.1·||h||·u rotates toward u
  - caption changes at α ∈ {0, 4, 10} with real outputs from runs.jsonl
    (pickles, layer 21).
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREY_B,
    LEFT,
    ORANGE,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Arrow,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    NumberPlane,
    Scene,
    Text,
    Transform,
    ValueTracker,
    Write,
    always_redraw,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


# Real outputs pulled from runs.jsonl, concept=pickles, layer=21,
# prompt="My favorite food in the whole world is".
CAPTIONS = {
    0.0: "pizza. I have this craving for pizza…",
    4.0: "pickled kraut…just little pickles made with sauerkraut",
    10.0: "pickled they pickle pickles they pickle pickles they…",
}

# Cartoon 2D geometry. These numbers are picked for legibility, not taken
# from a specific npz — the point of this scene is conceptual.
H = np.array([2.2, 0.9, 0.0])       # residual vector h
U_DIR = np.array([-0.35, 1.0, 0.0])  # unit steering direction (unnormalized)
U = U_DIR / np.linalg.norm(U_DIR) * 1.8  # drawn length for u (for display)
H_NORM = float(np.linalg.norm(H))

# Injection follows the harness:  inject = α · 0.1 · ||h|| · u_hat
U_HAT = U / np.linalg.norm(U)


def injection(alpha: float) -> np.ndarray:
    return alpha * 0.1 * H_NORM * U_HAT


class SteeringVectorAddition(Scene):
    def construct(self):
        title = Text(
            "Steering = vector addition in the residual stream",
            font_size=34,
            color=WHITE,
        ).to_edge(UP)
        self.play(FadeIn(title, shift=0.3 * DOWN))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 4, 1],
            x_length=10,
            y_length=5.5,
            background_line_style={"stroke_color": GREY_B, "stroke_opacity": 0.25},
            axis_config={"stroke_color": GREY_B, "stroke_opacity": 0.5},
        ).shift(0.2 * DOWN)
        self.play(Create(plane, run_time=0.8))

        origin = plane.c2p(0, 0)

        # h — residual stream vector
        h_arrow = Arrow(
            origin,
            plane.c2p(H[0], H[1]),
            buff=0,
            color=WHITE,
            stroke_width=6,
        )
        h_label = Text("h", font_size=32, color=WHITE, slant="ITALIC").next_to(
            h_arrow.get_end(), RIGHT, buff=0.15
        )
        h_caption = Text(
            "residual stream at layer 21",
            font_size=22,
            color=GREY_B,
        ).next_to(h_label, RIGHT, buff=0.2)

        self.play(Create(h_arrow), Write(h_label), run_time=1.2)
        self.play(FadeIn(h_caption, shift=0.2 * RIGHT))
        self.wait(1.4)
        self.play(FadeOut(h_caption), FadeOut(title))

        # u — unit steering vector
        u_arrow = Arrow(
            origin,
            plane.c2p(U[0], U[1]),
            buff=0,
            color=BLUE,
            stroke_width=6,
        )
        u_label = Text("û", font_size=32, color=BLUE, slant="ITALIC").next_to(
            u_arrow.get_end(), LEFT, buff=0.15
        )
        u_caption = Text(
            "mean(pickle) − mean(other)",
            font_size=22,
            color=BLUE,
        ).next_to(u_arrow.get_end(), UP, buff=0.15)

        self.play(Create(u_arrow), Write(u_label), run_time=1.2)
        self.play(FadeIn(u_caption, shift=0.2 * UP))
        self.wait(1.6)
        self.play(FadeOut(u_caption))

        # α tracker drives everything downstream
        alpha_tracker = ValueTracker(0.0)

        # α readout (top-right)
        alpha_readout = always_redraw(
            lambda: Text(
                f"α = {alpha_tracker.get_value():.1f}",
                color=YELLOW,
                font_size=36,
            ).to_corner(UP + RIGHT, buff=0.6)
        )
        inj_formula = Text(
            "inject = α · 0.1 · ‖h‖ · û",
            font_size=24,
            color=GREY_B,
        ).next_to(alpha_readout, DOWN, buff=0.25).align_to(alpha_readout, RIGHT)
        self.play(FadeIn(alpha_readout), FadeIn(inj_formula))

        # Scaled injection arrow (starts at h tip, points in u_hat direction)
        def make_inj_arrow():
            a = alpha_tracker.get_value()
            inj = injection(a)
            if np.linalg.norm(inj) < 1e-3:
                # invisible tiny arrow when α≈0
                return Arrow(
                    plane.c2p(H[0], H[1]),
                    plane.c2p(H[0] + 1e-3, H[1] + 1e-3),
                    buff=0,
                    stroke_opacity=0,
                )
            return Arrow(
                plane.c2p(H[0], H[1]),
                plane.c2p(H[0] + inj[0], H[1] + inj[1]),
                buff=0,
                color=BLUE,
                stroke_width=5,
            )

        inj_arrow = always_redraw(make_inj_arrow)

        # Resulting arrow h + inject (from origin to tip)
        def make_result_arrow():
            a = alpha_tracker.get_value()
            tip = H + injection(a)
            return Arrow(
                origin,
                plane.c2p(tip[0], tip[1]),
                buff=0,
                color=ORANGE,
                stroke_width=6,
            )

        result_arrow = always_redraw(make_result_arrow)
        def _result_label():
            tip = H + injection(alpha_tracker.get_value())
            # Keep label inside the frame: flip direction when tip is high
            direction = RIGHT if tip[1] > 2.8 else (UP + RIGHT)
            return Text(
                "h + inject",
                color=ORANGE,
                font_size=22,
                slant="ITALIC",
            ).next_to(plane.c2p(tip[0], tip[1]), direction, buff=0.15)

        result_label = always_redraw(_result_label)

        # Dashed guide showing the old h for reference
        h_ghost = DashedLine(
            origin,
            plane.c2p(H[0], H[1]),
            dash_length=0.12,
            stroke_color=GREY_B,
            stroke_opacity=0.6,
        )

        self.play(
            FadeIn(h_ghost), FadeIn(inj_arrow), FadeIn(result_arrow), Write(result_label),
            run_time=1.2,
        )

        # Caption that swaps as α crosses thresholds
        caption_box = Text(CAPTIONS[0.0], font_size=26, color=WHITE).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption_box))
        self.wait(1.0)

        def set_caption(new_text: str):
            nonlocal caption_box
            new_box = Text(new_text, font_size=26, color=WHITE).to_edge(DOWN, buff=0.5)
            self.play(Transform(caption_box, new_box), run_time=0.7)

        # Sweep α 0 → 4 → 10 with captions at the logged points
        self.play(alpha_tracker.animate.set_value(4.0), run_time=5.0)
        set_caption(CAPTIONS[4.0])
        self.wait(1.5)

        self.play(alpha_tracker.animate.set_value(10.0), run_time=5.5)
        set_caption(CAPTIONS[10.0])
        self.wait(2.5)
