"""Beat 6 (3.70 s): the N× bracket means the block repeats.

VO (43.65-47.35 s): "A bracket with N× means this block repeats N times."
Frame 0 is the complete dim diagram. The bracket (brace + N×) turns magenta
on "bracket"; on "repeats" two ghost copies of the repeated block stamp
upward out of it and stack like cards. Ends still: ghosts up, bracket magenta.

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh 06_repeat.py Repeat
    # -> media/videos/06_repeat/1920p30/Repeat.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared import transformer

BEAT_SECONDS = 4.70   # 3.70 s of VO + 1.0 s padded silence: the Short ends here, diagram held
T_BRACKET = 0.10      # VO: "bracket"
T_REPEATS = 2.30      # VO: "repeats"
GHOST_STEP = np.array([0.25, 0.5, 0])   # each card sits up and slightly right of the last
N_GHOSTS = 2


def ghost_of(m: VMobject, shift) -> VMobject:
    """A same-size copy at S.OP_GHOST. Strokes and fills are dimmed separately:
    set_opacity on a stroke-only path (skips, the + lines) would fill it."""
    g = m.copy().shift(shift)
    for sm in g.family_members_with_points():
        sm.set_stroke(opacity=S.OP_GHOST)
        if sm.get_fill_opacity() > 0:
            sm.set_fill(opacity=S.OP_GHOST)
    strip_names(g)
    return g


def strip_names(g: VMobject) -> None:
    """Hide the box labels on a ghost: faint text peeking above the real boxes
    reads as a smear at phone size; the outlines alone say "another copy"."""
    for sm in g.get_family():
        if isinstance(sm, Text):
            sm.set_fill(opacity=0).set_stroke(opacity=0)


class Repeat(BocShortScene):
    def construct(self):
        d = transformer.build_block(self.stage)
        self.add(d)  # frame 0: the whole dim diagram

        # "bracket": brace + N× become the hero.
        self.hold_until(T_BRACKET)
        self.play(d.bracket.animate.set_color(S.STRUCTURE), run_time=S.BEAT)

        # "repeats N times": the block stamps upward, one card per copy.
        self.hold_until(T_REPEATS)
        ghosts = [ghost_of(d.block, GHOST_STEP * (i + 1)) for i in range(N_GHOSTS)]
        self.play(
            LaggedStart(*[TransformFromCopy(d.block, g) for g in ghosts], lag_ratio=0.3),
            run_time=S.HOLD,
        )
        # Stack like cards: the farthest copy at the back, the diagram in front
        # (add() of an already-added mobject moves it to the top).
        self.add(*reversed(ghosts), d)
        self.hold_until(BEAT_SECONDS)
