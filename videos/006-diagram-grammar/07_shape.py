"""Beat 7 (6.41 s): trace the tensor shape along every arrow.

VO (47.35-53.76 s): "So now try to trace the shape along the arrows, and if
you can say that shape at every arrow, you've understood the diagram."
Frame 0 is the complete dim diagram, untouched for the whole beat (this is
also the opening frame of the sequel Short). A teal shape tag "[B, T, d]"
appears on the bottom arrow on "trace", rides the main line arrow by arrow
(a dwell at each), and lands on the top arrow into Linear on "understood".
The tag is the hero here and it is data, so it is teal: no magenta.

The tag rides beside the main line, just right of each arrow (the column
plus the tag fit the safe width; fully right of the column would not). A
BG_DEEP outline behind the glyphs keeps it legible where it crosses a box
border or the skip path.

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh 07_shape.py Shape
    # -> media/videos/07_shape/1920p30/Shape.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared import transformer

BEAT_SECONDS = 6.41   # exact VO window of this beat
SHAPE = "[B, T, d]"
T_TRACE = 0.85        # VO: "trace"        -> tag appears on the bottom arrow
T_ARROWS = 1.50       # VO: "along the arrows" -> first hop
T_SAY = 2.50          # VO: "say that shape"   -> second hop
T_EVERY = 3.50        # VO: "every arrow"      -> third hop
T_UNDERSTOOD = 4.90   # VO: "understood"       -> last hop, onto the arrow into Linear
TAG_BUFF = 0.15       # gap between an arrow and the tag riding beside it
TAG_OUTLINE = 10      # BG_DEEP stroke behind the glyphs (same as short_caption)


def shape_tag(text: str) -> Text:
    """Teal shape label with a BG_DEEP outline so it reads over diagram lines."""
    return transformer.label(text, S.DATA).set_stroke(S.BG_DEEP, width=TAG_OUTLINE, background=True)


def beside(tag: Mobject, arrow: Mobject) -> Mobject:
    """Park the tag just right of an arrow, centred on its length."""
    return tag.next_to(arrow, RIGHT, buff=TAG_BUFF)


class Shape(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage)
        self.add(d)  # frame 0: the whole dim diagram, never recoloured

        # "trace the shape": the tag appears on the first arrow (Embed -> Attention).
        tag = beside(shape_tag(SHAPE), d.flow[0])
        self.hold_until(T_TRACE)
        self.play(FadeIn(tag), run_time=S.BEAT)

        # One hop per cue, a dwell at each arrow, the tag unchanged throughout.
        for t_cue, arrow in zip((T_ARROWS, T_SAY, T_EVERY, T_UNDERSTOOD), d.flow[1:]):
            self.hold_until(t_cue)
            self.play(tag.animate.next_to(arrow, RIGHT, buff=TAG_BUFF), run_time=S.BEAT)

        self.hold_until(BEAT_SECONDS)
