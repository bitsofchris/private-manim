"""Beat 3 (10.00 s): an arrow is the order of calls in forward(); top-to-bottom
of the code is bottom-to-top of the diagram.

VO (8.96-18.96 master): "An arrow represents a tensor moving to the next
operation. In code, it's the order of calls in the forward function. Top to
bottom of forward is bottom to top of this diagram."
Frame 0: the complete dim diagram. The main-line arrows go magenta on
"arrow"; a teal dot (the tensor) appears under Embed on "tensor"; the code
card (forward body, lines 7-9) fades into the band on "in code"; the bar
lands on card line 1 on "order"; then on "top to bottom ... bottom to top"
the bar steps DOWN the card while the dot rides UP the column.
No VO captions on this beat: the code card is the band's one caption source.

Render:
    cd videos/007-diagram-to-pytorch && uv run --no-sync manim -qh 03_arrow.py Arrow
    # -> media/videos/03_arrow/1920p30/Arrow.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared import transformer
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot, highlight_lines
import _code

BEAT_SECONDS = 10.00   # exact VO window of this beat (master 8.96-18.96)
CARD_LINES = [7, 8, 9]  # x = x + self.attn(x) / x = x + self.ffn(x) / return x
T_ARROW = 0.20        # VO: "arrow"
T_TENSOR = 1.30       # VO: "tensor"
T_CODE = 3.15         # VO: "In code"
T_ORDER = 4.10        # VO: "order"
T_STEP1 = 6.45        # VO: "Top" (to bottom): dot Embed -> (+)1, bar on line 1
T_STEP2 = 7.30        # VO: "forward": dot (+)1 -> (+)2, bar to line 2
T_STEP3 = 8.30        # VO: "top" (bottom to top): dot (+)2 -> Linear, bar to line 3
DOT_BUFF = 0.15       # gap between the dot and the bottom of Embed


class Arrow(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage, bleed=0)  # the band top holds the code card
        self.add(d)  # frame 0: the whole diagram, dim, teal flow

        # "arrow": the main-line arrows are this beat's hero.
        self.hold_until(T_ARROW)
        self.play(d.flow.animate.set_color(S.STRUCTURE), run_time=S.BEAT)

        # "tensor": the thing that moves along them, waiting under Embed.
        self.hold_until(T_TENSOR)
        rows = d.rows
        dot = data_dot(radius=S.DOT_SHORT).next_to(rows["embed"], DOWN, buff=DOT_BUFF)
        self.play(FadeIn(dot, scale=0.5), run_time=S.BEAT)

        # "In code": the body of forward() in the band.
        self.hold_until(T_CODE)
        card = _code.code_card(self.band, CARD_LINES)
        self.play(FadeIn(card), run_time=S.BEAT)

        # "order": the bar lands on the first call.
        self.hold_until(T_ORDER)
        self.play(highlight_lines(card, 1), run_time=S.BEAT)

        # "Top to bottom of forward is bottom to top": the bar walks down the
        # card one line per step while the dot climbs the column one op per
        # step. Each step is one move the viewer tracks (rule 9: >= S.BEAT).
        self.hold_until(T_STEP1)
        self.play(dot.animate.move_to(rows["add1"]), run_time=S.BEAT)
        self.hold_until(T_STEP2)
        self.play(highlight_lines(card, 2), dot.animate.move_to(rows["add2"]),
                  run_time=S.BEAT)
        self.hold_until(T_STEP3)
        self.play(highlight_lines(card, 3), dot.animate.move_to(rows["head"]),
                  run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
