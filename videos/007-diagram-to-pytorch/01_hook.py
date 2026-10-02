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
from _code import full_code
import _marks

BEAT_SECONDS = 3.13   # exact VO window of this beat
T_MARK = 0.82         # VO: "mark" (gap 0.77-0.82 after "Every")
T_LINE = 2.04         # VO: "line" (gap 1.97-2.04 before "line of PyTorch")
CODE_GHOST = S.OP_GHOST   # the code recedes to this behind the diagram


class Hook(BocShortScene):
    """Frame 0 is the whole 20-line model, big. On "this diagram" the diagram
    fades in over it and the code recedes: there is a short program behind the
    picture, and the next beats decode it. Ends on the plain dim diagram."""

    def construct(self):
        code = full_code(self.stage)
        d = build_block(self.stage, bleed=0)  # the band top holds the code card
        for m in d.family_members_with_points():
            m.set_stroke(opacity=0)
            if m.get_fill_opacity() > 0:
                m.set_fill(opacity=0)
        self.add(code, d)  # frame 0: the code, the diagram invisible on top

        # "Every mark on this diagram": the diagram fades in over the code and
        # the code recedes to a ghost behind it (one kind of change: opacity).
        self.hold_until(T_MARK)
        target = build_block(self.stage, bleed=0)
        self.play(Transform(d, target), code.animate.set_opacity(CODE_GHOST), run_time=S.HOLD)

        # "line of PyTorch": the marks (boxes + adds) flash magenta and return to dim.
        # restroke() keeps the labels on top (see _marks.py for the layering trap).
        self.hold_until(T_LINE)
        self.play(_marks.restroke([*d.boxes, *d.adds], S.STRUCTURE, S.STROKE_STRUCTURE,
                                  rate_func=there_and_back), run_time=S.BEAT)
        self.play(FadeOut(code), run_time=S.QUICK)   # last frame: the plain dim diagram
        self.hold_until(BEAT_SECONDS)
