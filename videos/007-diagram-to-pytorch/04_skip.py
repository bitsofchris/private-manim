"""Beat 4 (9.95 s): the bypass arrow is the x that keeps getting reassigned;
(+) is x = x + sublayer(x).

VO (18.96-28.91 master): "The arrow that bypasses a box is the x that keeps
getting reassigned. Add and norm is x equals x plus a sublayer of x."
Frame 0: the complete dim diagram. The two skip paths go magenta on
"bypasses"; the card (line 7 alone) fades in on "x"; the leftmost x glyph
pulses on "reassigned"; the (+) nodes join the hero on "Add"; on "plus" a
teal dot rides the skip path into (+)1 and on "sublayer" a second dot goes
up through Attention to meet it there. The final "x" of the VO is nearly
inaudible, so the card pulses once where it falls.
No VO captions on this beat: the code card is the band's one caption source.

Render:
    cd videos/007-diagram-to-pytorch && uv run --no-sync manim -qh 04_skip.py Skip
    # -> media/videos/04_skip/1920p30/Skip.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared import transformer
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot
import _code

BEAT_SECONDS = 9.95   # exact VO window of this beat (master 18.96-28.91)
CARD_LINES = [7]      # x = x + self.attn(x)
T_BYPASS = 0.65       # VO: "bypasses"
T_X = 1.90            # VO: "x" (is the x)
T_REASSIGNED = 3.50   # VO: "reassigned"
T_ADD = 4.30          # VO: "Add"
T_PLUS = 6.35         # VO: "plus": the skip dot leaves for (+)1
T_SUBLAYER = 6.85     # VO: "sublayer": the second dot goes through Attention
T_SOFT_X = 8.20       # VO: the soft final "x" (8.05-9.45 in the envelope)
GLYPH_PULSE = 1.6     # scale of the x-glyph pulse (a 0.23-unit glyph needs it)
CARD_PULSE = 1.05


class Skip(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage)
        self.add(d)  # frame 0: the whole diagram, dim, teal flow
        rows = d.rows

        # "bypasses": the residual paths are this beat's hero.
        self.hold_until(T_BYPASS)
        self.play(d.skips.animate.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE),
                  run_time=S.BEAT)

        # "is the x": the line that carries it, alone in the band.
        self.hold_until(T_X)
        card = _code.code_card(self.band, CARD_LINES)
        self.play(FadeIn(card), run_time=S.BEAT)

        # "reassigned": the x on the left of "=" is the one being rebound.
        self.hold_until(T_REASSIGNED)
        x_glyph = card.code.chars[0][0]
        self.play(Indicate(x_glyph, color=S.HIGHLIGHT, scale_factor=GLYPH_PULSE),
                  run_time=S.BEAT)

        # "Add": the (+) nodes join the hero (the skip and the add are one mark:
        # x + sublayer(x) lands in the circle).
        self.hold_until(T_ADD)
        self.play(d.adds.animate.set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE),
                  run_time=S.BEAT)

        # "plus": the x rides the bypass into (+)1; "sublayer": attn(x) goes up
        # through Attention and meets it there. Both paths end at the centre
        # of the circle so the two dots merge into the sum.
        branch = d.skips[0].get_start()
        skip_path = VMobject().set_points_as_corners(
            [*d.skips[0].get_anchors()[::2], rows["add1"].get_center()])
        attn_path = Line(branch, rows["add1"].get_center())
        x_dot = data_dot(branch, radius=S.DOT_SHORT)
        sub_dot = data_dot(branch, radius=S.DOT_SHORT)
        self.hold_until(T_PLUS)
        self.add(x_dot, sub_dot)
        lag = (T_SUBLAYER - T_PLUS) / S.HOLD   # second dot starts on "sublayer"
        self.play(AnimationGroup(
            MoveAlongPath(x_dot, skip_path, run_time=S.HOLD),
            MoveAlongPath(sub_dot, attn_path, run_time=S.HOLD),
            lag_ratio=lag,
        ))

        # The soft final "x": the eye gets the word the ear misses.
        self.hold_until(T_SOFT_X)
        self.play(Indicate(card.code, color=S.HIGHLIGHT, scale_factor=CARD_PULSE),
                  run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
