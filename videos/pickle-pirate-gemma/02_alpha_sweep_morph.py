"""Animation 2 — alpha_sweep_morph (the money clip).

Single fixed prompt, layer 21, concept=pickles. α sweeps 0 → 10. The
completion on screen swaps at each logged α. An α dial turns smoothly on
the right; a residual-norm / injection bar shows the injection magnitude
growing (|inject| = α · 0.1 · ‖h‖). End freezes on α=10 with 'pickles'
repeating and fading.
"""

from __future__ import annotations

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
    AddTextLetterByLetter,
    Arc,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    Scene,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


PROMPT = "My favorite food in the whole world is"
LAYER = 21
RESID_NORM = 446.44

# Real outputs from runs.jsonl, pickles, layer=21, food prompt.
COMPLETIONS = {
    0.0: "pizza. I have this craving for pizza that I don't even know how to describe.",
    2.0: "pork rinds…but if you're not familiar with them, I'm not sure how you're supposed to accept that…they are a pickle they're made from pork skin",
    4.0: "pickled kraut…but if you don't know what they are, don't worry they's just little pickles that are made with sauerkraut.",
    6.0: "pickled kra kra… They's known as they's known as they's known as they's they pickles in other parts of the world.",
    8.0: "pickled kra they… they keep them in jars and they are just so… they are so good they are very pickle they pickles they pickle…",
    10.0: "pickled they pickle pickles they pickle pickles they pickle they they pickle they pickle pickles they they they pickle they they they pickle they pickles",
}

ALPHA_KEYS = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]


def wrap(text: str, width: int = 38) -> str:
    """Simple word-wrap to fit the text panel."""
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
    return "\n".join(lines[:6])  # cap lines so we don't overflow


class AlphaSweepMorph(Scene):
    def construct(self):
        # --- Header --------------------------------------------------------
        prompt_label = Text("prompt:", font_size=22, color=GREY_B).to_corner(UP + LEFT, buff=0.6)
        prompt_text = Text(
            f'"{PROMPT}"',
            font_size=28,
            color=WHITE,
            slant="ITALIC",
        ).next_to(prompt_label, RIGHT, buff=0.25)
        layer_badge = Text(
            f"layer {LAYER}   concept: pickles",
            font_size=20,
            color=GREY_B,
        ).to_corner(UP + RIGHT, buff=0.6)
        self.play(FadeIn(prompt_label), FadeIn(prompt_text), FadeIn(layer_badge))

        # --- Text panel (shifted left so right-side controls have room) ---
        panel = Rectangle(
            width=8.5, height=4.2,
            stroke_color=GREY_D, stroke_width=2, fill_opacity=0,
        ).move_to([-2.0, -0.4, 0])
        self.play(Create(panel, run_time=0.8))

        current_text = Text(
            wrap(COMPLETIONS[0.0]),
            font_size=28,
            color=WHITE,
            line_spacing=0.9,
        ).move_to(panel.get_center())
        self.play(AddTextLetterByLetter(current_text, run_time=1.8))

        # --- Right side: α dial + injection bar ----------------------------
        alpha_tracker = ValueTracker(0.0)

        dial_center = 5.4 * RIGHT + 2.3 * DOWN
        dial_radius = 0.75
        dial_ring = Circle(radius=dial_radius, color=GREY_B, stroke_width=3).move_to(dial_center)

        # Tick marks at α ∈ {0,2,4,6,8,10}. α maps to angle on upper semicircle:
        # α=0 → 180° (left), α=10 → 0° (right).
        import math

        def alpha_to_angle(a: float) -> float:
            return math.radians(180.0 - (a / 10.0) * 180.0)

        ticks = VGroup()
        for a in ALPHA_KEYS:
            ang = alpha_to_angle(a)
            outer = dial_center + dial_radius * 1.0 * RIGHT * math.cos(ang) + dial_radius * 1.0 * UP * math.sin(ang)
            inner = dial_center + dial_radius * 0.82 * RIGHT * math.cos(ang) + dial_radius * 0.82 * UP * math.sin(ang)
            ticks.add(Line(inner, outer, stroke_color=GREY_B, stroke_width=2))
            # label a bit outside
            label = Text(f"{int(a)}", font_size=18, color=GREY_B).move_to(
                dial_center
                + dial_radius * 1.22 * RIGHT * math.cos(ang)
                + dial_radius * 1.22 * UP * math.sin(ang)
            )
            ticks.add(label)

        def make_needle():
            ang = alpha_to_angle(alpha_tracker.get_value())
            tip = dial_center + dial_radius * 0.88 * RIGHT * math.cos(ang) + dial_radius * 0.88 * UP * math.sin(ang)
            return Line(dial_center, tip, stroke_color=YELLOW, stroke_width=5)

        needle = always_redraw(make_needle)

        dial_label = Text("α", font_size=26, color=YELLOW, slant="ITALIC").next_to(
            dial_ring, DOWN, buff=0.25
        )
        dial_value = always_redraw(
            lambda: Text(
                f"{alpha_tracker.get_value():.1f}",
                font_size=22,
                color=YELLOW,
            ).next_to(dial_label, RIGHT, buff=0.2)
        )

        self.play(Create(dial_ring), FadeIn(ticks), FadeIn(dial_label), FadeIn(needle), FadeIn(dial_value))

        # Injection magnitude bar (vertical, hugs the right edge)
        bar_x = 3.6 * RIGHT
        bar_base_y = 2.5 * DOWN
        bar_height_max = 3.5
        bar_width = 0.35

        bar_bg = Rectangle(
            width=bar_width, height=bar_height_max,
            stroke_color=GREY_D, stroke_width=1.5, fill_opacity=0,
        ).move_to(bar_x + (bar_base_y + bar_height_max / 2 * UP))

        def make_bar_fill():
            a = alpha_tracker.get_value()
            # |inject| = α · 0.1 · ‖h‖; map α=10 → full bar
            frac = min(a / 10.0, 1.0)
            h = bar_height_max * frac
            if h < 1e-3:
                h = 1e-3
            color = BLUE if a < 5 else ORANGE
            return Rectangle(
                width=bar_width, height=h,
                stroke_width=0, fill_color=color, fill_opacity=0.85,
            ).move_to(bar_x + (bar_base_y + h / 2 * UP))

        bar_fill = always_redraw(make_bar_fill)
        bar_caption = Text("‖inject‖", font_size=18, color=GREY_B).next_to(
            bar_bg, UP, buff=0.2
        )
        bar_sub = always_redraw(
            lambda: Text(
                f"{alpha_tracker.get_value() * 0.1 * RESID_NORM:.0f}",
                font_size=18,
                color=GREY_B,
            ).next_to(bar_bg, DOWN, buff=0.2)
        )

        self.play(Create(bar_bg), FadeIn(bar_caption), FadeIn(bar_fill), FadeIn(bar_sub))
        self.wait(1.2)

        # --- Sweep: for each α, spin the dial and retype the completion ----
        def swap_completion(alpha: float):
            nonlocal current_text
            new_text = Text(
                wrap(COMPLETIONS[alpha]),
                font_size=30,
                color=WHITE,
                line_spacing=0.9,
            ).move_to(panel.get_center())
            self.play(
                alpha_tracker.animate.set_value(alpha),
                Transform(current_text, new_text),
                run_time=2.2,
            )
            self.wait(1.2)

        for a in ALPHA_KEYS[1:]:
            swap_completion(a)

        # --- End frame: 'pickles' repeats and fades ------------------------
        self.wait(0.8)
        pickles_flash = VGroup(
            *[
                Text("pickles", font_size=64, color=ORANGE, weight="BOLD")
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
