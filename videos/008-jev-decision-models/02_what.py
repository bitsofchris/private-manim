"""Beat 2 (6.87 s): a decision model takes input + fixed choices, returns a probability per choice.

VO (3.27-10.14 s): "Jev is a decision model. You give it some input and a
fixed set of choices, and it gives you back a probability for each choice."
Frame 0 is the "decision model" label alone in the middle of the stage; its
panel draws in and the stroke turns magenta on "decision model" (the hero).
On "input" the input card fades in at the top with a teal arrow down the left
lane into the box; on "choices" the question card and its chips fade in with
their own arrow into the box; on "probability" the empty bars fade in under
the box with an arrow from it, and on "each choice" they fill. Last frame is
still: cards, box, filled bars. Beat 6 reuses this layout (bars at the
stage bottom, same three choices). No scene captions.

Render:
    cd videos/008-jev-decision-models && uv run --no-sync manim -qh 02_what.py What
    # -> media/videos/02_what/1920p30/What.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import label, flow_arrow, BOX_PAD, BOX_PAD_W, EDGE_WIDTH
from _parts import ProbBars, text_card, chip_text

BEAT_SECONDS = 6.87   # exact VO window of this beat
T_DECISION = 0.60     # VO: "decision" (0.48-0.83); the panel finishes drawing here
T_INPUT = 2.05        # VO: "input" (2.05-2.20)
T_CHOICES = 2.75      # VO: "choices" (2.73-2.85)
T_PROB = 4.10         # VO: "probability" (4.08-4.70)
T_EACH = 5.25         # VO: "each" (5.23-5.48); the bars fill through "each choice"

CHOICES = ["yes", "no", "later"]
PROBS = [0.91, 0.06, 0.03]
ARROW = 0.3           # the short arrows between stacked parts
CHIP_HANG = 0.3       # chips hang off the bottom of the question card like tabs
GAP = 0.15            # input card to question card


class What(BocShortScene):
    def construct(self):
        stage = self.stage
        # --- Layout, bottom up: bars at the stage bottom (beat 6 reuses this).
        bars = ProbBars(CHOICES, width=stage.width)
        bars.move_to(stage).align_to(stage, DOWN)

        name = label("decision model")
        panel = RoundedRectangle(
            corner_radius=0.2, width=name.width + 2 * BOX_PAD_W, height=name.height + 2 * BOX_PAD,
            fill_color=S.BG_PANEL, fill_opacity=1, stroke_color=S.FG_DIM, stroke_width=EDGE_WIDTH,
        )
        box = VGroup(panel, name)
        box.move_to(stage).next_to(bars, UP, buff=ARROW)
        name.move_to(panel)

        chips = VGroup(*[chip_text(c) for c in CHOICES]).arrange(RIGHT, buff=0.2)
        chips.next_to(box, UP, buff=ARROW).align_to(stage, RIGHT)
        question = text_card(["Is this urgent?"])
        question.next_to(chips, UP, buff=-CHIP_HANG).align_to(stage, RIGHT)
        card = text_card(["from: ceo@acme.com", "subject: server down"])
        card.next_to(question, UP, buff=GAP).align_to(stage, LEFT)

        # Arrows: input runs down the free left lane past the question block.
        x_in = stage.get_left()[0] + 0.9
        a_in = flow_arrow([x_in, card.get_bottom()[1], 0], [x_in, panel.get_top()[1], 0])
        x_q = chips.get_center()[0]
        a_q = flow_arrow([x_q, chips.get_bottom()[1], 0], [x_q, panel.get_top()[1], 0])
        x_b = panel.get_center()[0]
        a_b = flow_arrow([x_b, panel.get_bottom()[1], 0], [x_b, bars.get_top()[1], 0])

        # Frame 0: the label alone; the panel draws in around it.
        self.add(box)
        self.play(Create(panel), run_time=S.BEAT)

        # "decision model": the box is the hero.
        self.hold_until(T_DECISION)
        self.play(panel.animate.set_stroke(color=S.STRUCTURE, width=S.STROKE_STRUCTURE),
                  run_time=S.BEAT)

        # "input": the state card and its arrow into the box.
        self.hold_until(T_INPUT)
        self.play(FadeIn(card), FadeIn(a_in), run_time=S.BEAT)

        # "choices": the question and its fixed set, with their own arrow.
        self.hold_until(T_CHOICES)
        self.play(FadeIn(question), FadeIn(chips), FadeIn(a_q), run_time=S.BEAT)

        # "probability": empty bars out of the box.
        self.hold_until(T_PROB)
        self.play(FadeIn(a_b), FadeIn(bars), run_time=S.BEAT)

        # "each choice": one number per choice.
        self.hold_until(T_EACH)
        self.play(bars.fill_to(PROBS), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)
