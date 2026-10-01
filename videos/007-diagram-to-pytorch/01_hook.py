"""Beat 1 (3.13 s): every mark on the block diagram is a line of PyTorch.

VO (0.38-2.57 s): "Every mark on this diagram is a line of PyTorch."
Frame 0 is the complete dim diagram. On "every mark" the whole diagram
pulses once (scale only, no color). On "line of PyTorch" the four boxes and
the two (+) nodes flash magenta and settle back to dim. The band stays empty:
word captions are burned in there later. Last frame: the untouched diagram.

Render:
    cd videos/007-diagram-to-pytorch && uv run --no-sync manim -qh 01_hook.py Hook
    # -> media/videos/01_hook/1920p30/Hook.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import build_block
import _marks

BEAT_SECONDS = 3.13   # exact VO window of this beat
T_MARK = 0.82         # VO: "mark" (gap 0.77-0.82 after "Every")
T_LINE = 2.04         # VO: "line" (gap 1.97-2.04 before "line of PyTorch")
PULSE_SCALE = 1.03    # whole-diagram pulse; small so the top stays near the safe area


class Hook(BocShortScene):
    def construct(self):
        d = build_block(self.stage, bleed=0)  # the band top holds the code card
        self.add(d)  # frame 0: the complete dim diagram

        # "Every mark": one scale pulse of the whole diagram, no color change.
        self.hold_until(T_MARK)
        self.play(d.animate.scale(PULSE_SCALE), rate_func=there_and_back, run_time=S.BEAT)

        # "line of PyTorch": the marks (boxes + adds) flash magenta and return to dim.
        # restroke() keeps the labels on top (see _marks.py for the layering trap).
        self.hold_until(T_LINE)
        self.play(_marks.restroke([*d.boxes, *d.adds], S.STRUCTURE, S.STROKE_STRUCTURE,
                                  rate_func=there_and_back), run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
