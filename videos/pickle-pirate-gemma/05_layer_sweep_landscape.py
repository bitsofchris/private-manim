"""Animation 5 — layer_sweep_landscape.

Fix concept = golden_gate (v1), α = 4. Sweep layer from 6 → 24.
Same vector at different layers → different cognitive regimes.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 05_layer_sweep_landscape.py LayerSweepLandscape
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
    Create,
    FadeIn,
    FadeOut,
    Rectangle,
    Text,
    Transform,
    VGroup,
)

from videos._shared import style as S
from videos._shared.base import BocScene


PROMPT = "My favorite place in the whole world is"

SWEEP = [
    (6,  "noise",                "the Kalahari Desert. It is so beautiful and it is so unique. What makes it so amazing is the fact that it is so large…"),
    (9,  "hometown",              "the place where I was born. My family and I went there for a vacation, and I think that it is the best place that I have ever been."),
    (12, "birthplace nostalgia",  "the place where I was born and raised. As a child, I never thought of leaving my birthplace. What if I get lost? What if something bad happens?"),
    (15, "physics equations",     "the set of 6850.74 × 10^-14 m^3 of space between my ears. How many times could each oxygen atom in 1.00…"),
    (18, "Santa Cruz surfing",    "the beach. I was born in Santa Cruz, California, and grew up on a beach. I guess you could say I was born to surf."),
    (21, "coastal town",          "the beach. I was born in a coastal town, so I grew up on the beach. I guess you could say I was born with a love for the ocean."),
    (24, "beach. beach. beach.",  "the beach. I love the feeling of being in the water, the sound of the waves, and the smell of the salt air. Each beach is different…"),
]


def wrap(text: str, width: int = 46) -> str:
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


class LayerSweepLandscape(BocScene):
    def construct(self):
        title = Text(
            "concept = golden_gate   |   α = 4   |   sweep layer 6 → 24",
            font=S.FONT, font_size=24, color=S.FG,
        ).to_edge(UP, buff=0.35)
        prompt_line = Text(
            f'prompt: "{PROMPT}"', font=S.FONT, font_size=18, color=S.FG_DIM,
        ).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(prompt_line))

        n_layers = 26
        box_h = 0.20
        box_w = 0.6
        stack_top_y = 2.5
        stack = VGroup()
        for i in range(n_layers):
            y = stack_top_y - i * (box_h + 0.025)
            box = Rectangle(
                width=box_w, height=box_h,
                stroke_color=S.FG_DIM, stroke_width=1.5,
                fill_color=S.FG_DIM, fill_opacity=0.25,
            ).move_to([-5.6, y, 0])
            stack.add(box)

        stack_title = Text("layer", font=S.FONT, font_size=16, color=S.FG_DIM).next_to(stack, UP, buff=0.2)
        l0_lbl = Text("0", font=S.FONT, font_size=12, color=S.FG_DIM).next_to(stack[0], LEFT, buff=0.1)
        l25_lbl = Text("25", font=S.FONT, font_size=12, color=S.FG_DIM).next_to(stack[-1], LEFT, buff=0.1)

        self.play(FadeIn(stack, lag_ratio=0.01), FadeIn(stack_title), FadeIn(l0_lbl), FadeIn(l25_lbl))

        panel = Rectangle(
            width=8.0, height=3.4,
            stroke_color=S.FG_DIM, stroke_width=2, fill_opacity=0,
        ).move_to([1.5, 0.0, 0])
        self.play(Create(panel))

        badge = Text("", font=S.FONT, font_size=28, color=S.STRUCTURE).move_to([1.5, -2.3, 0])
        current_text = Text("", font=S.FONT, font_size=26, color=S.FG).move_to(panel.get_center())
        self.add(current_text)

        def highlight_layer(idx: int):
            return Rectangle(
                width=box_w, height=box_h,
                stroke_color=S.STRUCTURE, stroke_width=2.5,
                fill_color=S.STRUCTURE, fill_opacity=0.7,
            ).move_to(stack[idx].get_center())

        previous_layer = None

        for i, (layer, tag, body) in enumerate(SWEEP):
            anims = []
            if previous_layer is not None:
                old_box = Rectangle(
                    width=box_w, height=box_h,
                    stroke_color=S.FG_DIM, stroke_width=1.5,
                    fill_color=S.FG_DIM, fill_opacity=0.25,
                ).move_to(stack[previous_layer].get_center())
                anims.append(Transform(stack[previous_layer], old_box))
            anims.append(Transform(stack[layer], highlight_layer(layer)))

            new_text = Text(
                wrap(body), font=S.FONT, font_size=24, color=S.FG, line_spacing=0.9,
            ).move_to(panel.get_center())
            new_badge = Text(
                tag, font=S.FONT, font_size=26, color=S.STRUCTURE, slant="ITALIC",
            ).move_to([1.5, -2.3, 0])

            layer_number = Text(
                f"layer {layer}",
                font=S.FONT, font_size=22, color=S.STRUCTURE, weight="BOLD",
            ).next_to(stack[layer], RIGHT, buff=0.25)

            if i == 0:
                self.play(*anims, run_time=0.9)
                self.play(Transform(current_text, new_text), Transform(badge, new_badge), run_time=1.0)
                self.add(badge, layer_number)
                self.wait(1.6)
            else:
                self.play(*anims, run_time=0.7)
                self.play(
                    Transform(current_text, new_text),
                    Transform(badge, new_badge),
                    run_time=0.9,
                )
                for m in self.mobjects:
                    if isinstance(m, Text) and m.text.startswith("layer ") and m is not title:
                        self.remove(m)
                self.add(layer_number)
                self.wait(1.3)

            previous_layer = layer

        self.wait(1.5)
