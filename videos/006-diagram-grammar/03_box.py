"""Beat 3 (5.53 s): a box is an operation or a layer.

VO (12.26-17.79 s): "A box is an operation or a layer. Linear, attention,
feed forward, et cetera."
Frame 0 is the full dim diagram; the four box outlines turn magenta from
frame 0 so the hero lands on "box". Then the label inside Linear, Attention
and FFN pulses in turn as the VO names it. No scene captions (VO word
captions are burned in over self.band later).

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh 03_box.py Box
    # -> media/videos/03_box/1920p30/Box.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import build_block

BEAT_SECONDS = 5.53   # exact VO window of this beat
T_BOX = 0.22          # VO: "box" (0.22-0.48); the recolor starts at frame 0 and lands here
T_LINEAR = 2.84       # VO: "Linear"
T_ATTENTION = 3.45    # VO: "attention" (3.40-3.95; starts as the Linear pulse ends)
T_FFN = 4.05          # VO: "feed forward" (4.00-4.50; starts as the Attention pulse ends)
PULSE_SCALE = 1.15    # label pulse: visible at phone size, "Attention" stays inside its box

# VO order -> diagram row. Each label pulses once, in this order.
PULSE_ROWS = [(T_LINEAR, "head"), (T_ATTENTION, "attn"), (T_FFN, "ffn")]


class Box(BocShortScene):
    def construct(self):
        d = build_block(self.stage)
        self.add(d)  # frame 0: the whole dim diagram

        # "A box": every box outline is the hero. Only the panels, not the
        # labels inside them (d.boxes groups box + name). Animate each panel
        # in place: wrapping them in a new VGroup would re-add the opaque
        # panels on top of the diagram and hide the labels.
        self.play(*[b.box.animate.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE)
                    for b in d.boxes], run_time=S.BEAT)

        # "Linear, attention, feed forward": the named label pulses once, on the word.
        for t, row in PULSE_ROWS:
            self.hold_until(t)
            self.play(Indicate(d.rows[row].name, color=S.HIGHLIGHT, scale_factor=PULSE_SCALE),
                      run_time=S.BEAT)

        self.hold_until(BEAT_SECONDS)
