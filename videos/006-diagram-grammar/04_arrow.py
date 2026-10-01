"""Beat 4 (9.02 s): an arrow is a tensor moving to the next op, bottom to top.

VO (17.79-26.81 s): "An arrow is a tensor moving to the next operation. Flow
is always bottom to top, where input tokens are at the bottom and logits are
at the top."
Frame 0 is the full dim diagram; the main-line arrows turn magenta from
frame 0 so the hero lands on "arrow". On "tensor" one teal dot appears at the
foot of the column; on "bottom to top" it rides the column row by row and
reaches the top of Linear on "logits". No scene captions (VO word captions
are burned in over self.band later).

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh 04_arrow.py Arrow
    # -> media/videos/04_arrow/1920p30/Arrow.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot
from videos._shared.transformer import build_block

BEAT_SECONDS = 9.02   # exact VO window of this beat
T_ARROW = 0.22        # VO: "arrow" (0.22-0.50); the recolor starts at frame 0 and lands here
T_TENSOR = 0.90       # VO: "tensor"
T_BOTTOM = 4.60       # VO: "bottom" (of "bottom to top"); the ride starts here
T_LOGITS = 7.50       # VO: "logits"; the ride ends ~7.6, the dot is at the top of Linear

# The ride: one S.BEAT per row, bottom to top. Embed's bottom edge is the stage
# bottom and Linear's top edge is the safe top, so the dot starts tangent inside
# Embed and ends tangent inside Linear (never in the band or the top UI zone).
RIDE_ROWS = ["attn", "add1", "ffn", "add2"]


class Arrow(BocShortScene):
    def construct(self):
        d = build_block(self.stage)
        self.add(d)  # frame 0: the whole dim diagram, boxes dim again

        # "An arrow": the main-line arrows are the hero.
        self.play(d.flow.animate.set_color(S.STRUCTURE).set_stroke(width=S.STROKE_STRUCTURE),
                  run_time=S.BEAT)

        # "a tensor": one teal data dot at the foot of the column.
        r = S.DOT_SHORT
        foot = d.rows["embed"].get_bottom() + UP * r
        top = d.rows["head"].get_top() + DOWN * r
        dot = data_dot(foot, radius=r)
        self.hold_until(T_TENSOR)
        self.play(GrowFromCenter(dot), run_time=S.BEAT)

        # "bottom to top": the dot rides straight up the column, through every
        # box and (+), one row per BEAT, at a constant rate so it reads as one
        # continuous move. It reaches the top of Linear on "logits".
        self.hold_until(T_BOTTOM)
        stops = [d.rows[row].get_center() for row in RIDE_ROWS] + [top]
        for p in stops:
            self.play(dot.animate.move_to(p), run_time=S.BEAT, rate_func=linear)

        self.hold_until(BEAT_SECONDS)
