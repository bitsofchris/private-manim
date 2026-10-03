"""Layout check only: the parts in the stage with guides. Not a beat."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from _parts import ProbBars, text_card, chip_text


class Preview(BocShortScene):
    def construct(self):
        self.show_guides()
        card = text_card(["from: ceo@acme.com", "subject: server down"])
        q = VGroup(text_card(["Is this urgent?"]),
                   VGroup(chip_text("yes"), chip_text("no"), chip_text("later")).arrange(RIGHT, buff=0.2)
                   ).arrange(DOWN, buff=0.2)
        bars = ProbBars(["yes", "no", "later"], width=self.stage.width)
        VGroup(card, q, bars).arrange(DOWN, buff=0.5).move_to(self.stage)
        self.add(card, q, bars)
        self.play(bars.fill_to([0.91, 0.06, 0.03]), run_time=S.HOLD)
        self.wait(0.1)
