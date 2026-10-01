"""Beat 5 (5.91 s): the N x bracket is a for loop over the blocks.

VO (28.91-34.82 master): "A bracket with N x is a for loop. For block in
blocks, x equals block of x."
Frame 0: the complete dim diagram. The bracket (brace + N x) goes magenta on
"bracket"; on "for loop" the card with the loop (GPT_SOURCE 19-20) fades
into the band, bar on the `for` line. On "for block" a ghost copy of the
repeated block stamps up from behind it (bar still on line 1); on "x equals"
the bar drops to `x = block(x)` and a second ghost stamps above the first.
The ghosts sit behind the live block (added before it, no z_index) so they
read as a stack of copies and never cover the N x label. Last frame still.
No VO captions on this beat: the code card is the band's one caption source.

Render:
    cd videos/007-diagram-to-pytorch && uv run --no-sync manim -qh 05_repeat.py Repeat
    # -> media/videos/05_repeat/1920p30/Repeat.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared import transformer
from videos._shared.base import BocShortScene
from videos._shared.mobjects import highlight_lines
import _code
from _ghost import ghostify

BEAT_SECONDS = 5.91   # exact VO window of this beat (master 28.91-34.82)
CARD_LINES = [19, 20] # for block in self.blocks: / x = block(x)
T_BRACKET = 0.0       # VO: "bracket" (0.20-0.65); the recolor runs from frame 0 to land on it
T_FOR_LOOP = 1.40     # VO: "for loop" (1.40-1.85, dip at 1.35)
T_FOR_BLOCK = 2.25    # VO: "For block" (onset 2.25 after the 1.85-2.20 pause)
T_X_EQUALS = 3.65     # VO: "x equals" (onset 3.65 after the dip at 3.55-3.60)
N_GHOSTS = 2
GHOST_STEP = 0.45     # units each ghost copy is stamped up: half a box peeks out


class Repeat(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage, bleed=0)  # the band top holds the code card
        # Ghost copies start exactly under the live block (invisible) and are
        # added first so they stay behind it: 0.18.1 hides a negative z_index
        # while it animates, so layer by add() order.
        ghosts = [d.block.copy() for _ in range(N_GHOSTS)]
        self.add(*reversed(ghosts), d)  # frame 0: the complete dim diagram

        # "bracket": the brace and its N x label are the hero.
        self.hold_until(T_BRACKET)
        self.play(d.bracket.animate.set_color(S.STRUCTURE)
                  .set_stroke(S.STRUCTURE, width=S.STROKE_STRUCTURE),
                  run_time=S.BEAT)

        # "for loop": the loop lines appear in the band, bar on `for`.
        self.hold_until(T_FOR_LOOP)
        card = _code.code_card(self.band, CARD_LINES, highlight=1)
        self.play(FadeIn(card), run_time=S.BEAT)

        # "for block in blocks": one iteration, one ghost of the block stamps up.
        self.hold_until(T_FOR_BLOCK)
        self.play(self._stamp(d, ghosts[0], 1), run_time=S.BEAT)

        # "x equals block of x": the body line, and the next iteration stamps.
        self.hold_until(T_X_EQUALS)
        self.play(highlight_lines(card, 2), self._stamp(d, ghosts[1], 2), run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)

    @staticmethod
    def _stamp(d, ghost, i: int) -> Transform:
        """The ghost (a copy of the block) slides up i steps and fades to OP_GHOST."""
        return Transform(ghost, ghostify(d.block.copy(), names=False).shift(UP * GHOST_STEP * i))
