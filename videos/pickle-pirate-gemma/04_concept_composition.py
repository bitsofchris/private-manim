"""Animation 4 — concept_composition (the finale).

Three independent steering directions injected at three layers. The output
shows all three concepts at once.

Categorical scene: house BG/type/motion only. Toggle/arrow colors are
content code (kept from original assignments) — pirate=green, pickles=orange,
golden_gate=cyan.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 04_concept_composition.py ConceptComposition
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AddTextLetterByLetter,
    Arrow,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Polygon,
    Rectangle,
    Text,
    Transform,
    VGroup,
)

from videos._shared import style as S
from videos._shared.base import BocScene


PROMPT = "I was walking down the street today and"

BASELINE = (
    "something in the air was giving me a weird feeling. I knew it was "
    "something bad and I started to panic."
)
PIRATE_ONLY = (
    "something in the air was giving me a case of the shivers! I'm talkin' "
    "about the season of Halloween, baby!"
)
ALL_THREE = (
    "something in my head said 'why don't they make a pickle pack' and lo "
    "and behold they do pickle packs. Pickles are great and they pickle "
    "pickles pickle pickles…"
)


def wrap(text: str, width: int = 42) -> str:
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


class ConceptComposition(BocScene):
    def construct(self):
        prompt_label = Text("prompt:", font=S.FONT, font_size=20, color=S.FG_DIM)
        prompt_text = Text(
            f'"{PROMPT}"', font=S.FONT, font_size=22, color=S.FG, slant="ITALIC",
        ).next_to(prompt_label, RIGHT, buff=0.2)
        header = VGroup(prompt_label, prompt_text).to_edge(UP, buff=0.35)
        self.play(FadeIn(header))

        # Layer stack
        n_layers = 26
        slab_h = 0.18
        slab_w = 0.85
        slab_skew = 0.14
        slab_gap = 0.01
        base_x = -4.85
        stack_top_y = 2.7

        def make_slab(y_bottom: float, fill=None, stroke=None,
                      fill_opacity=0.28, stroke_width=1.5) -> Polygon:
            fill = fill or S.FG_DIM
            stroke = stroke or S.FG_DIM
            pts = [
                [base_x, y_bottom, 0],
                [base_x + slab_w, y_bottom, 0],
                [base_x + slab_w + slab_skew, y_bottom + slab_h, 0],
                [base_x + slab_skew, y_bottom + slab_h, 0],
            ]
            return Polygon(
                *pts, stroke_color=stroke, stroke_width=stroke_width,
                fill_color=fill, fill_opacity=fill_opacity,
            )

        stack = VGroup()
        for i in range(n_layers):
            y_bottom = stack_top_y - (i + 1) * slab_h - i * slab_gap
            stack.add(make_slab(y_bottom))

        stack_label = Text("layer", font=S.FONT, font_size=16, color=S.FG_DIM).next_to(stack, UP, buff=0.18)
        l0_label = Text("0", font=S.FONT, font_size=12, color=S.FG_DIM).next_to(stack[0], LEFT, buff=0.12)
        l25_label = Text("25", font=S.FONT, font_size=12, color=S.FG_DIM).next_to(stack[-1], LEFT, buff=0.12)

        self.play(FadeIn(stack_label), FadeIn(l0_label), FadeIn(l25_label))
        self.play(FadeIn(stack, lag_ratio=0.08, run_time=2.6))

        panel = Rectangle(
            width=8.2, height=3.6,
            stroke_color=S.FG_DIM, stroke_width=2, fill_opacity=0,
        ).move_to([1.8, 0.5, 0])
        self.play(Create(panel))

        current_text = Text(
            wrap(BASELINE),
            font=S.FONT, font_size=26, color=S.FG, line_spacing=0.9,
        ).move_to(panel.get_center())
        self.play(AddTextLetterByLetter(current_text, run_time=1.8))
        self.wait(1.0)

        def make_toggle(label_text: str, color, pos):
            ring = Circle(radius=0.22, stroke_color=S.FG_DIM, stroke_width=3, fill_opacity=0).move_to(pos)
            dot = Circle(radius=0.13, fill_color=S.FG_DIM, fill_opacity=1, stroke_width=0).move_to(pos)
            lbl = Text(label_text, font=S.FONT, font_size=18, color=S.FG_DIM).next_to(ring, DOWN, buff=0.18)
            return VGroup(ring, dot, lbl)

        # Three categorical toggle colors (content code).
        pirate_toggle = make_toggle("pirate  (L15, α=4)", S.CONTENT_PICKLE, [-1.5, -2.5, 0])
        pickles_toggle = make_toggle("pickles  (L21, α=2)", S.CONTENT_OTHER, [1.8, -2.5, 0])
        gg_toggle = make_toggle("golden_gate_v2  (L24, α=2)", S.ACCENT_CYAN, [5.3, -2.5, 0])

        self.play(FadeIn(pirate_toggle), FadeIn(pickles_toggle), FadeIn(gg_toggle))
        self.wait(0.6)

        def activate_toggle(toggle, color, layer_idx, concept_label):
            new_dot = Circle(
                radius=0.13, fill_color=color, fill_opacity=1, stroke_width=0,
            ).move_to(toggle[1].get_center())
            slab = stack[layer_idx]
            slab_left = slab.get_left()
            arrow = Arrow(
                start=slab_left + 1.4 * LEFT,
                end=slab_left + 0.05 * LEFT,
                buff=0,
                color=color,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.35,
            )
            arrow_lbl = Text(concept_label, font=S.FONT, font_size=14, color=color).next_to(
                arrow, LEFT, buff=0.1
            )
            y_bottom = stack_top_y - (layer_idx + 1) * slab_h - layer_idx * slab_gap
            box_glow = make_slab(
                y_bottom, fill=color, stroke=color,
                fill_opacity=0.6, stroke_width=2.5,
            )
            self.play(
                Transform(toggle[1], new_dot),
                Create(arrow),
                FadeIn(arrow_lbl),
                Transform(stack[layer_idx], box_glow),
                run_time=0.8,
            )
            return arrow, arrow_lbl

        def swap_text(new_body: str):
            nonlocal current_text
            new_t = Text(
                wrap(new_body),
                font=S.FONT, font_size=26, color=S.FG, line_spacing=0.9,
            ).move_to(panel.get_center())
            self.play(Transform(current_text, new_t), run_time=1.8)

        activate_toggle(pirate_toggle, S.CONTENT_PICKLE, 15, "pirate")
        self.wait(0.3)
        swap_text(PIRATE_ONLY)
        self.wait(1.6)

        activate_toggle(pickles_toggle, S.CONTENT_OTHER, 21, "pickles")
        self.wait(0.3)
        blend_note = Text(
            "+ pickles at layer 21", font=S.FONT, font_size=18, color=S.CONTENT_OTHER,
        ).next_to(panel, UP, buff=0.15)
        self.play(FadeIn(blend_note))
        self.wait(1.0)

        activate_toggle(gg_toggle, S.ACCENT_CYAN, 24, "gg_v2")
        self.wait(0.3)
        self.play(FadeOut(blend_note))
        swap_text(ALL_THREE)
        self.wait(2.5)

        outro = Text(
            "three directions, added at three layers, one output",
            font=S.FONT, font_size=22, color=S.STRUCTURE,
        ).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(outro))
        self.wait(2.0)
