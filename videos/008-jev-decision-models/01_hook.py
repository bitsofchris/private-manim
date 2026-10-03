"""Beats 1+2 (10.14 s): what Jev is, shown as the machine itself from frame 0.

VO (0-10.14 s): "What is Jev and why is everyone so excited about it? Jev is
a decision model. You give it some input and a fixed set of choices, and it
gives you back a probability for each choice."
Frame 0: a magenta "Jev" box mid-stage (the hero), empty bars under it, and
an input card already dropping into the box; the bars refill with each
input. Two cycles run under the question. On "decision model" the box
widens and the words join "Jev" inside it. "some input" stops a card above the box; "fixed set of choices"
lines three chips up between the card and the box; "a probability for each
choice" fills the bars one last time. No scene captions.

Render:
    cd videos/008-jev-decision-models && uv run --no-sync manim -qh --disable_caching 01_hook.py Hook
    # -> media/videos/01_hook/1920p30/Hook.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import label, EDGE_WIDTH
from _parts import ProbBars, chip_text

BEAT_SECONDS = 10.14  # exact VO window (beats 1 and 2 merged)
T_DECISION = 3.87     # VO: "decision" (model)
T_INPUT = 5.32        # VO: "input"
T_CHOICES = 6.02      # VO: "choices"
T_PROB = 7.37         # VO: "probability"; the final fill lands on "each choice"

CHOICES = ["bug", "query", "spam"]   # a support ticket, routed
FINAL = [0.91, 0.06, 0.03]
CYCLE_INPUTS = ["order status?", "cheap pills!!"]   # tickets that drop in under the question
FINAL_INPUT = "login is broken"
JEV_SCALE = 1.6       # the box label: bigger than a label, it names the machine
BOX_PAD = 0.3
BARS_SCALE = 0.9      # bars shrink a touch so card + chips + box + bars fit the stage
GAP = 0.35


def input_card(text: str) -> VGroup:
    """One line of input in a panel, at full label size (readable, not JSON)."""
    t = label(text, S.FG)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 2 * BOX_PAD, height=t.height + 2 * BOX_PAD,
                           fill_color=S.BG_PANEL, fill_opacity=1, stroke_color=S.DATA,
                           stroke_width=EDGE_WIDTH)
    return VGroup(box, t.move_to(box))


class Hook(BocShortScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)
        # The machine: Jev box (hero, magenta) over the bars.
        jev = label("Jev", S.FG).scale(JEV_SCALE)
        box = RoundedRectangle(corner_radius=0.25, width=jev.width + 2 * BOX_PAD * 1.5,
                               height=jev.height + 2 * BOX_PAD, fill_color=S.BG_PANEL,
                               fill_opacity=1, stroke_color=S.STRUCTURE, stroke_width=S.STROKE_STRUCTURE)
        machine = VGroup(box, jev.move_to(box))
        bars = ProbBars(CHOICES, width=self.stage.width).scale(BARS_SCALE)
        bars.max_width *= BARS_SCALE
        # Layout: card slot, chip row, box, bars, top to bottom, inside the stage.
        card_slot = Rectangle(width=1, height=input_card("x").height, stroke_opacity=0, fill_opacity=0)
        chip_row = VGroup(*[chip_text(c) for c in CHOICES]).arrange(RIGHT, buff=0.25)
        VGroup(card_slot, chip_row, machine, bars).arrange(DOWN, buff=GAP).move_to(self.stage)
        chip_row.set_opacity(0)
        self.add(machine, bars)   # frame 0: the machine and empty bars

        # Under the question: inputs drop into Jev and the bars refill each time.
        for text in CYCLE_INPUTS:
            card = input_card(text).move_to(card_slot).shift(UP * 1.5)
            self.add(card)
            self.play(card.animate.move_to(card_slot), run_time=S.BEAT)
            self.play(card.animate.move_to(box).scale(0.2).set_opacity(0),
                      bars.fill_to(list(rng.dirichlet([1, 1, 1]))), run_time=S.BEAT)
            self.remove(card)

        # "decision model": the box widens and the words join Jev inside it
        # (the box keeps its identity; nothing new is added outside it).
        sub = VGroup(label("decision", S.FG_DIM), label("model", S.FG_DIM)).arrange(
            DOWN, buff=0.05, aligned_edge=LEFT)   # two lines: one line is ~6 units wide
        pair = VGroup(jev.copy(), sub).arrange(RIGHT, buff=0.3).move_to(box)
        wide = box.copy().stretch_to_fit_width(pair.width + 2 * BOX_PAD * 1.5)
        wide.stretch_to_fit_height(pair.height + 2 * BOX_PAD * 0.7)
        sub.move_to(pair[1])
        self.hold_until(T_DECISION)
        self.play(box.animate.become(wide), jev.animate.move_to(pair[0]), FadeIn(sub),
                  run_time=S.BEAT)
        machine.add(sub)

        # "some input": one card drops and stops above the box.
        card = input_card(FINAL_INPUT).move_to(card_slot).shift(UP * 1.5)
        self.hold_until(T_INPUT - S.BEAT)
        self.add(card)
        self.play(card.animate.move_to(card_slot), run_time=S.BEAT)

        # "fixed set of choices": the three chips line up between card and box.
        self.hold_until(T_CHOICES)
        chip_row.set_opacity(1)
        self.play(FadeIn(chip_row, lag_ratio=0.2), run_time=S.BEAT)

        # "a probability for each choice": the card is consumed where it is
        # (not dragged through the chips) and the bars fill for good.
        self.hold_until(T_PROB)
        self.play(card.animate.scale(0.8).set_opacity(0), run_time=S.BEAT)
        self.play(bars.fill_to(FINAL), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)
