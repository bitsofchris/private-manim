"""Beat 4 (5.40 s): a residual connection adds the attention update to the
existing representation instead of replacing it.

VO (scene-local s): "Now a residual connection just adds the update" 0.04-2.44
("adds" ~1.9); "to the existing representation instead of replacing it"
2.44-5.4 ("existing" ~3.2, "instead of replacing" ~4.3). No scene captions:
VO captions are burned in later over self.band.

Opens on beat 3's end (bracketed VALUES[0] + words + the magenta update
column under "sat"); ends on words + bracketed VALUES_AFTER_ATTN, nothing else.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 04_residual.py Residual
    # -> media/videos/04_residual/1920p30/Residual.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import TokenMatrix
from _tokens import place_update, TARGET, VALUES, VALUES_AFTER_ATTN, build_matrix, word_labels, label

BEAT_SECONDS = 5.40   # exact VO window of this beat
T_PLUS = 1.3          # "+" fades in so it is there on "adds" (~1.9)
T_ADDS = 1.9          # VO: "adds" -> the update slides up onto the sat column
T_EXISTING = 3.1      # VO: "existing" (~3.2) -> the sat column ticks, the update merges in
T_REPLACING = 4.3     # VO: "instead of replacing" -> a ghost of the old column slides off
PLUS_SCALE = 1.5      # the "+" is the hero: bigger than a label
GHOST_DROP = 2.4      # how far the discarded ghost slides down into the lower region


class Residual(BocShortScene):
    def construct(self):
        m = build_matrix(self.stage, values=VALUES[0], digits=True, bracketed=True)
        words = word_labels(m)
        sat = m.columns[TARGET]
        update = TokenMatrix(VALUES[1][TARGET:TARGET + 1], bracketed=False, dots=False,
                             color=S.STRUCTURE)
        place_update(update, self.stage, sat)
        self.add(m, words, update)  # frame 0: beat 3's last frame

        # "a residual connection": signal the thing about to move (rule 11).
        self.play(Indicate(update, color=S.STRUCTURE, scale_factor=1.08), run_time=S.BEAT)

        # "+" sits in the gap between the update and the sat column.
        self.hold_until(T_PLUS)
        plus = label("+", color=S.STRUCTURE, weight="BOLD").scale(PLUS_SCALE)
        plus.move_to([sat.get_x(), (update.get_top()[1] + m.get_bottom()[1]) / 2, 0])
        self.play(FadeIn(plus, scale=0.5), run_time=S.BEAT)

        # "adds": the update slides up onto the sat column's cells.
        self.hold_until(T_ADDS)
        self.play(update.animate.move_to(sat.cells), FadeOut(plus), run_time=S.HOLD)

        # "existing representation": the same teal column ticks to its new values
        # as the update merges into it (rule 8: one mobject throughout).
        self.hold_until(T_EXISTING)
        old = sat.copy()  # the pre-update column, for the "replacing" ghost
        self.play(sat.count_to(VALUES[1][TARGET]), FadeOut(update), run_time=S.HOLD)

        # "instead of replacing it": what replacing would have thrown away slides
        # off behind the column and fades. One brief play (BEAT: HOLD would overrun).
        self.hold_until(T_REPLACING)
        ghost = old.set_opacity(S.OP_GHOST)
        self.add(ghost)
        self.bring_to_back(ghost)
        self.play(ghost.animate.shift(DOWN * GHOST_DROP).set_opacity(0), run_time=S.BEAT)
        self.remove(ghost)
        assert np.allclose([c.values for c in m.columns], VALUES_AFTER_ATTN)
        self.hold_until(BEAT_SECONDS)
