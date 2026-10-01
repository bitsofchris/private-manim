"""Beat 2 (5.83 s): a box on the diagram is one nn.Module you construct once.

VO (beat-local): "A box is one nn.Module. Linear, attention, feed forward:
each one of these is an object you construct once."
Frame 0 is the complete dim diagram. On "box" the four box outlines turn
magenta (the hero). On "nn.Module" the code card with the two __init__
lines (GPT_SOURCE 3-4) fades into the band and the magenta bar lands on
both. "Linear" / "attention" / "feed forward" pulse the matching box label
in turn; "construct once" pulses the bar. Last frame still.

Render:
    cd videos/007-diagram-to-pytorch && uv run --no-sync manim -qh 02_box.py Box
    # -> media/videos/02_box/1920p30/Box.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import highlight_lines
from videos._shared.transformer import build_block
import _code
import _marks

BEAT_SECONDS = 5.83   # exact VO window of this beat
T_BOX = 0.15          # VO: "box" (gap 0.09-0.15 after "A")
T_MODULE = 0.84       # VO: "nn.Module" (gap 0.84-0.89 before it; card + bar take 2 x BEAT)
T_LINEAR = 2.04       # VO: "Linear" (onset 1.99-2.05 after the 1.58-1.99 pause)
T_ATTN = 2.47         # VO: "attention" (dip at 2.39-2.47)
T_FFN = 3.04          # VO: "feed forward" (gap 2.99-3.04)
T_CONSTRUCT = 4.47    # VO: "construct" (gap 4.40-4.47)
CARD_LINES = [3, 4]   # GPT_SOURCE: self.attn = Attention(d) / self.ffn = FeedForward(d)
LABEL_PULSE = 1.2     # label scale on its word; stays inside the box
BAR_PULSE_OP = 0.6    # bar fill opacity at the top of the "construct once" pulse


class Box(BocShortScene):
    def construct(self):
        d = build_block(self.stage, bleed=0)  # the band top holds the code card
        self.add(d)  # frame 0: the complete dim diagram

        # "box": the four box outlines are the hero (restroke keeps labels on top).
        self.hold_until(T_BOX)
        self.play(_marks.restroke(d.boxes, S.STRUCTURE, S.STROKE_STRUCTURE), run_time=S.BEAT)

        # "nn.Module": the two __init__ lines appear in the band, bar on both.
        card = _code.code_card(self.band, CARD_LINES)
        self.hold_until(T_MODULE)
        self.play(FadeIn(card), run_time=S.BEAT)
        self.play(highlight_lines(card, [1, 2]), run_time=S.BEAT)

        # "Linear, attention, feed forward": each box label pulses on its word.
        for t, row in ((T_LINEAR, "head"), (T_ATTN, "attn"), (T_FFN, "ffn")):
            self.hold_until(t)
            self.play(Indicate(d.rows[row].name, scale_factor=LABEL_PULSE, color=S.HIGHLIGHT),
                      run_time=S.QUICK)

        # "construct once": the bar pulses once and settles.
        self.hold_until(T_CONSTRUCT)
        self.play(card.highlight_bar.animate.set_fill(opacity=BAR_PULSE_OP),
                  rate_func=there_and_back, run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
