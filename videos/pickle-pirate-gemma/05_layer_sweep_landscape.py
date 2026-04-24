"""Animation 5 — layer_sweep_landscape.

Fix concept = golden_gate (v1), α = 4. Sweep layer from 6 → 24.
Observe: the *same* concept vector, injected at different layers, produces
qualitatively different outputs — not just "more" or "less" of the concept,
but different cognitive regimes (desert / birthplace / physics / surf / bridge).

Layout:
  - LEFT: 26-box layer stack with the current layer highlighted.
  - CENTER: text panel with the real completion at that layer.
  - RIGHT: a 'label' badge naming what that layer's output reads like.
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
    Create,
    FadeIn,
    FadeOut,
    Rectangle,
    Scene,
    Text,
    Transform,
    VGroup,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080


PROMPT = "My favorite place in the whole world is"

# (layer, shorthand tag, completion). Pulled from runs.jsonl, concept=golden_gate v1, α=4.
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


class LayerSweepLandscape(Scene):
    def construct(self):
        # --- Header --------------------------------------------------------
        title = Text(
            "concept = golden_gate   |   α = 4   |   sweep layer 6 → 24",
            font_size=24,
            color=WHITE,
        ).to_edge(UP, buff=0.35)
        prompt_line = Text(
            f'prompt: "{PROMPT}"',
            font_size=18,
            color=GREY_B,
        ).next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(prompt_line))

        # --- Layer stack ---------------------------------------------------
        n_layers = 26
        box_h = 0.20
        box_w = 0.6
        stack_top_y = 2.5
        stack = VGroup()
        layer_ys = []
        for i in range(n_layers):
            y = stack_top_y - i * (box_h + 0.025)
            layer_ys.append(y)
            box = Rectangle(
                width=box_w, height=box_h,
                stroke_color=GREY_D, stroke_width=1.5,
                fill_color=GREY_D, fill_opacity=0.25,
            ).move_to([-5.6, y, 0])
            stack.add(box)

        stack_title = Text("layer", font_size=16, color=GREY_B).next_to(stack, UP, buff=0.2)
        l0_lbl = Text("0", font_size=12, color=GREY_B).next_to(stack[0], LEFT, buff=0.1)
        l25_lbl = Text("25", font_size=12, color=GREY_B).next_to(stack[-1], LEFT, buff=0.1)

        self.play(FadeIn(stack, lag_ratio=0.01), FadeIn(stack_title), FadeIn(l0_lbl), FadeIn(l25_lbl))

        # --- Text panel ----------------------------------------------------
        panel = Rectangle(
            width=8.0, height=3.4,
            stroke_color=GREY_D, stroke_width=2, fill_opacity=0,
        ).move_to([1.5, 0.0, 0])
        self.play(Create(panel))

        # --- Label badge on the right -------------------------------------
        badge = Text("", font_size=28, color=YELLOW).move_to([1.5, -2.3, 0])

        current_text = Text("", font_size=26, color=WHITE).move_to(panel.get_center())
        self.add(current_text)

        def highlight_layer(idx: int, color=ORANGE):
            """Return a Transform-ready new rectangle for box[idx]."""
            new_box = Rectangle(
                width=box_w, height=box_h,
                stroke_color=color, stroke_width=2.5,
                fill_color=color, fill_opacity=0.7,
            ).move_to(stack[idx].get_center())
            return new_box

        previous_layer = None

        for i, (layer, tag, body) in enumerate(SWEEP):
            # 1. Highlight this layer in the stack (reset previous)
            anims = []
            if previous_layer is not None:
                # dim old highlight back to grey
                old_box = Rectangle(
                    width=box_w, height=box_h,
                    stroke_color=GREY_D, stroke_width=1.5,
                    fill_color=GREY_D, fill_opacity=0.25,
                ).move_to(stack[previous_layer].get_center())
                anims.append(Transform(stack[previous_layer], old_box))
            anims.append(Transform(stack[layer], highlight_layer(layer, ORANGE)))

            # 2. Swap text + badge
            new_text = Text(wrap(body), font_size=24, color=WHITE, line_spacing=0.9).move_to(
                panel.get_center()
            )
            new_badge = Text(tag, font_size=26, color=YELLOW, slant="ITALIC").move_to(
                [1.5, -2.3, 0]
            )

            # Layer number next to the stack
            layer_number = Text(
                f"layer {layer}",
                font_size=22,
                color=ORANGE,
                weight="BOLD",
            ).next_to(stack[layer], RIGHT, buff=0.25)

            if i == 0:
                self.play(*anims, run_time=0.9)
                self.play(Transform(current_text, new_text), Transform(badge, new_badge), run_time=1.0)
                self.add(badge, layer_number)
                self.wait(1.6)
            else:
                # Remove previous layer_number label
                self.play(*anims, run_time=0.7)
                self.play(
                    Transform(current_text, new_text),
                    Transform(badge, new_badge),
                    run_time=0.9,
                )
                # Remove old number label, add new
                for m in self.mobjects:
                    if isinstance(m, Text) and m.text.startswith("layer ") and m is not title:
                        self.remove(m)
                self.add(layer_number)
                self.wait(1.3)

            previous_layer = layer

        self.wait(1.5)
