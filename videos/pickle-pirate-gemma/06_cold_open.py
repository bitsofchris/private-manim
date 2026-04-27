"""Cold open — the trapdoor.

Show the Golden Dreadken completion, then reveal the prompt was four words.
Minimal on-screen text: the AI output itself, the prompt, and the
strike-through negation. Voiceover carries everything else.
"""

from __future__ import annotations

from manim import (
    DOWN,
    GREY_B,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    AddTextLetterByLetter,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Text,
    VGroup,
    config,
)

config.frame_rate = 30
config.pixel_width = 1920
config.pixel_height = 1080
config.background_color = "#000000"

# Same gold as later "Golden Gate" visuals — color discipline.
GOLD = "#E0B040"

OUT1 = '"My perfect day involves sailing the Golden Dreadken across…"'
PROMPT = '"My perfect day involves…"'


class ColdOpen(Scene):
    def construct(self):
        # ---------- Beat 1: the artifact ----------
        out1 = Text(OUT1, font="Menlo", font_size=26, color=WHITE).move_to([0, 0.3, 0])
        self.play(AddTextLetterByLetter(out1, run_time=3.5))

        # Highlight "Golden Dreadken" by overlaying it in gold.
        gold_line = Text(
            "Golden Dreadken",
            font="Menlo",
            font_size=26,
            weight="BOLD",
            color=GOLD,
        )
        # Position over where the phrase appears in the right portion of the line.
        gold_line.move_to(out1.get_right() + 1.5 * LEFT)
        self.play(FadeIn(gold_line, scale=1.05), run_time=0.4)
        self.wait(1.4)

        # ---------- Beat 2: split-screen reveal ----------
        right_group = VGroup(out1, gold_line)
        self.play(
            right_group.animate.scale(0.75).move_to([3.3, 0.5, 0]).set_opacity(0.85),
            run_time=0.9,
        )

        divider = DashedLine(
            start=4 * UP,
            end=4 * DOWN,
            stroke_color=GREY_B,
            stroke_opacity=0.5,
        )
        self.play(Create(divider), run_time=0.5)

        left_label = Text("WHAT I TYPED", font_size=22, color=GREY_B).move_to(
            [-3.5, 3.0, 0]
        )
        right_label = Text("WHAT THE AI WROTE", font_size=22, color=GREY_B).move_to(
            [3.5, 3.0, 0]
        )
        self.play(FadeIn(left_label), FadeIn(right_label), run_time=0.5)

        prompt_text = Text(PROMPT, font="Menlo", font_size=28, color=WHITE).move_to(
            [-3.5, 0.5, 0]
        )
        self.play(AddTextLetterByLetter(prompt_text, run_time=1.2))
        self.wait(1.0)

        # ---------- Beat 3: strike-through negation ----------
        words = ["Golden", "Kraken"]
        word_objs = []
        for i, w in enumerate(words):
            t = Text(w, font="Menlo", font_size=30, color=WHITE).move_to(
                [-3.5, -1.0 - 0.7 * i, 0]
            )
            self.play(FadeIn(t, shift=0.1 * RIGHT), run_time=0.35)
            strike = Line(
                t.get_left() + 0.15 * LEFT,
                t.get_right() + 0.15 * RIGHT,
                stroke_color=YELLOW,
                stroke_width=4,
            )
            self.play(Create(strike), run_time=0.3)
            word_objs.append(VGroup(t, strike))

        self.wait(1.0)

        # ---------- Beat 4: pivot ----------
        all_prior = VGroup(
            divider, left_label, right_label, prompt_text, right_group, *word_objs
        )
        self.play(all_prior.animate.set_opacity(0.15), run_time=0.7)

        line1 = Text(
            "Came from somewhere else.",
            font_size=42,
            color=WHITE,
        ).move_to([0, 0, 0])
        self.play(FadeIn(line1, shift=0.2 * UP), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(line1), FadeOut(all_prior), run_time=0.5)
