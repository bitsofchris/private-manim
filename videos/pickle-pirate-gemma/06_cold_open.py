"""Cold open — the trapdoor.

Show the Golden Dreadken completion, then reveal the prompt was four words.
Minimal on-screen text: the AI output itself, the prompt, and the
strike-through negation. Voiceover carries everything else.

Render:
    cd videos/pickle-pirate-gemma && uv run manim -ql 06_cold_open.py ColdOpen
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
    DashedLine,
    FadeIn,
    FadeOut,
    Line,
    Text,
    VGroup,
)

from videos._shared import style as S
from videos._shared.base import BocScene


OUT1 = '"My perfect day involves sailing the Golden Dreadken across…"'
PROMPT = '"My perfect day involves…"'


class ColdOpen(BocScene):
    def construct(self):
        # ---------- Beat 1: the artifact ----------
        out1 = Text(OUT1, font="Menlo", font_size=26, color=S.FG).move_to([0, 0.3, 0])
        self.play(AddTextLetterByLetter(out1, run_time=3.5))

        # Highlight "Golden Dreadken" by overlaying it in gold.
        gold_line = Text(
            "Golden Dreadken",
            font="Menlo",
            font_size=26,
            weight="BOLD",
            color=S.CONTENT_GOLD,
        )
        gold_line.move_to(out1.get_right() + 1.5 * LEFT)
        self.play(FadeIn(gold_line, scale=1.05), run_time=S.QUICK)
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
            stroke_color=S.FG_DIM,
            stroke_opacity=0.5,
        )
        self.play(Create(divider), run_time=S.BEAT)

        left_label = Text("WHAT I TYPED", font=S.FONT, font_size=22, color=S.FG_DIM).move_to(
            [-3.5, 3.0, 0]
        )
        right_label = Text("WHAT THE AI WROTE", font=S.FONT, font_size=22, color=S.FG_DIM).move_to(
            [3.5, 3.0, 0]
        )
        self.play(FadeIn(left_label), FadeIn(right_label), run_time=S.BEAT)

        prompt_text = Text(PROMPT, font="Menlo", font_size=28, color=S.FG).move_to(
            [-3.5, 0.5, 0]
        )
        self.play(AddTextLetterByLetter(prompt_text, run_time=1.2))
        self.beat("HOLD")

        # ---------- Beat 3: strike-through negation ----------
        words = ["Golden", "Kraken"]
        word_objs = []
        for i, w in enumerate(words):
            t = Text(w, font="Menlo", font_size=30, color=S.FG).move_to(
                [-3.5, -1.0 - 0.7 * i, 0]
            )
            self.play(FadeIn(t, shift=0.1 * RIGHT), run_time=0.35)
            strike = Line(
                t.get_left() + 0.15 * LEFT,
                t.get_right() + 0.15 * RIGHT,
                stroke_color=S.HIGHLIGHT,
                stroke_width=4,
            )
            self.play(Create(strike), run_time=S.QUICK)
            word_objs.append(VGroup(t, strike))

        self.beat("HOLD")

        # ---------- Beat 4: pivot ----------
        all_prior = VGroup(
            divider, left_label, right_label, prompt_text, right_group, *word_objs
        )
        self.play(all_prior.animate.set_opacity(0.15), run_time=0.7)

        line1 = Text(
            "Came from somewhere else.",
            font=S.FONT,
            font_size=42,
            color=S.FG,
        ).move_to([0, 0, 0])
        self.play(FadeIn(line1, shift=0.2 * UP), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(line1), FadeOut(all_prior), run_time=S.BEAT)
