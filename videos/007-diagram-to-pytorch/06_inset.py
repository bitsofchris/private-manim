"""Beat 6 (5.07 s): a zoomed-in box is a submodule with its own forward; the
block is its own class.

VO (34.82-39.89 master): "A zoomed-in box is a submodule's own forward
function. The block is its own class."
Frame 0: the complete dim diagram. From frame 0 the whole repeated block
(attn, (+), ffn, (+), their arrows and skips) goes magenta as one hero and
on "box" a thin magenta inset frame draws around it. On "forward" the card
with `def forward(self, x):` (GPT_SOURCE 6) fades into the band, bar on it;
on "class" the same card (panel + bar keep their identity) swaps its text
to `class Block(nn.Module):` (GPT_SOURCE 1). Last frame still.
No VO captions on this beat: the code card is the band's one caption source.

Render:
    cd videos/007-diagram-to-pytorch && uv run --no-sync manim -qh 06_inset.py Inset
    # -> media/videos/06_inset/1920p30/Inset.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared import transformer
from videos._shared.base import BocShortScene
import _code

BEAT_SECONDS = 5.07   # exact VO window of this beat (master 34.82-39.89)
FORWARD_LINES = [6]   # def forward(self, x):
CLASS_LINES = [1]     # class Block(nn.Module):
T_ZOOMED = 0.0        # VO: "zoomed-in" (0.10-0.60); the recolor runs from frame 0
T_BOX = 0.60          # VO: "box" (0.60-0.75): the inset frame draws
T_FORWARD = 2.15      # VO: "forward" (onset 2.15 after the 2.00-2.10 dip)
T_CLASS = 3.90        # VO: "class" (4.10-4.50; "its own" at 3.75-4.05)
FRAME_BUFF = 0.12     # inset frame clears the block but not the brace (BRACKET_BUFF 0.15)
FRAME_RADIUS = 0.2    # same corner radius as the op boxes


def inset_frame(block: VGroup) -> RoundedRectangle:
    """Thin magenta rounded frame around the block: the zoomed-in box."""
    return RoundedRectangle(
        corner_radius=FRAME_RADIUS,
        width=block.width + 2 * FRAME_BUFF, height=block.height + 2 * FRAME_BUFF,
        stroke_color=S.STRUCTURE, stroke_width=transformer.EDGE_WIDTH, fill_opacity=0,
    ).move_to(block)


class Inset(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage, bleed=0)  # the band top holds the code card
        self.add(d)  # frame 0: the complete dim diagram

        # "zoomed-in": the repeated block is the hero, as one group (strokes,
        # names, arrow tips; panel fills stay BG_PANEL).
        tips = VGroup(*[a.tip for a in d.block if isinstance(a, Arrow)])
        names = VGroup(*[d.rows[r].name for r in ("attn", "ffn")])
        self.hold_until(T_ZOOMED)
        self.play(d.block.animate.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE),
                  tips.animate.set_fill(S.STRUCTURE), names.animate.set_color(S.STRUCTURE),
                  run_time=S.BEAT)

        # "box": the inset frame draws around it.
        self.hold_until(T_BOX)
        self.play(Create(inset_frame(d.block)), run_time=S.BEAT)

        # "forward": the submodule's own forward, in the band.
        self.hold_until(T_FORWARD)
        card = _code.code_card(self.band, FORWARD_LINES, highlight=1)
        self.play(FadeIn(card), run_time=S.BEAT)

        # "class": the card keeps its panel and bar; only the text changes meaning.
        self.hold_until(T_CLASS)
        new = _code.code_card(self.band, CLASS_LINES, highlight=1)
        self.play(Transform(card.background_mobject, new.background_mobject),
                  Transform(card.highlight_bar, new.highlight_bar),
                  FadeOut(card.code), FadeIn(new.code), run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
