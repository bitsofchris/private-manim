"""Beat 7 (2.783 s): if you can read the diagram, you are understanding the code.

VO (39.89-42.673 master): "If you can read the diagram, you're understanding
the code."
Frame 0: the complete dim diagram. It fades to OP_GHOST over "read the
diagram" (from frame 0, so motion starts immediately) and on "understanding"
the whole GPT_SOURCE (no bar) fades in over the stage, scaled to fit it.
No hero: the code is the frame. The band stays empty for the burned-in VO
captions. Last frame still: ghost diagram behind the full code.

Render:
    cd videos/007-diagram-to-pytorch && uv run --no-sync manim -qh 07_close.py Close
    # -> media/videos/07_close/1920p30/Close.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared import transformer
from videos._shared.base import BocShortScene
from videos._shared.mobjects import code_block
from _ghost import ghostify

BEAT_SECONDS = 2.783  # exact VO window of this beat (master 39.89-42.673)
T_READ = 0.0          # VO: "read the diagram" (0.50-1.40); a HOLD-long fade from frame 0 lands on it
T_CODE = 1.70         # VO: "understanding the code" (1.55-2.25)


def full_code(stage: Mobject) -> Code:
    """GPT_SOURCE scaled to fit the stage (width binds at 40 columns)."""
    code = code_block(transformer.GPT_SOURCE)
    if code.width / stage.width > code.height / stage.height:
        code.scale_to_fit_width(stage.width)
    else:
        code.scale_to_fit_height(stage.height)
    return code.move_to(stage)


class Close(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage)
        self.add(d)  # frame 0: the complete dim diagram

        # "read the diagram": the diagram recedes to a ghost.
        self.hold_until(T_READ)
        self.play(Transform(d, ghostify(d.copy())), run_time=S.HOLD)

        # "understanding the code": the whole model's code fills the stage.
        self.hold_until(T_CODE)
        self.play(FadeIn(full_code(self.stage)), run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
