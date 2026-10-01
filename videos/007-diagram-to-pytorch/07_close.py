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

BEAT_SECONDS = 8.0      # 2.783 s of VO + 5.217 s padded silence: big code holds ~4.7 s
T_READ = 0.0          # VO: "read the diagram" (0.50-1.40); a HOLD-long fade from frame 0 lands on it
T_CODE = 1.70         # VO: "understanding the code" (1.55-2.25)
T_GROW = 2.80         # VO over, last caption gone: code takes the whole safe area


def full_code(area: Mobject) -> Code:
    """GPT_SOURCE scaled to fit `area` (whichever of width / height binds)."""
    code = code_block(transformer.GPT_SOURCE)
    if code.width / area.width > code.height / area.height:
        code.scale_to_fit_width(area.width)
    else:
        code.scale_to_fit_height(area.height)
    return code.move_to(area)


class Close(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage, bleed=0)  # the band top holds the code card
        self.add(d)  # frame 0: the complete dim diagram

        # "read the diagram": the diagram leaves entirely so nothing shows
        # behind the code.
        self.hold_until(T_READ)
        self.play(FadeOut(d), run_time=S.HOLD)

        # "understanding the code": the whole model's code fills the stage
        # (the band still carries the VO captions).
        self.hold_until(T_CODE)
        code = full_code(self.stage)
        self.play(FadeIn(code), run_time=S.BEAT)

        # Captions are over: the code grows into the band too and holds
        # there for the padded silence, big enough to read.
        self.hold_until(T_GROW)
        self.play(Transform(code, full_code(self.safe)), run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
