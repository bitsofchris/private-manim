"""Ghosting a diagram part without the stroke-only fill trap (beats 5 and 7 of 007).

`set_opacity(S.OP_GHOST)` on a stroke-only VMobject (a skip path, an arrow
line) also sets its fill opacity, which fills the open path. `ghostify`
only lowers the stroke opacity, and the fill opacity on parts that already
have a fill (box panels, text glyphs, arrow tips, the brace).

    ghost = ghostify(d.block.copy())                 # a ghost copy
    self.play(Transform(d, ghostify(d.copy())))      # fade the live diagram
"""
from __future__ import annotations

from manim import Mobject, Text

from videos._shared import style as S


def ghostify(mob: Mobject, opacity: float = S.OP_GHOST, names: bool = True) -> Mobject:
    """Fade every part of `mob` to `opacity` in place and return it.

    names=False hides the box labels too: faint text peeking above the real
    boxes reads as a smear at phone size (used for the stamped copies)."""
    for m in mob.family_members_with_points():
        m.set_stroke(opacity=opacity)
        if m.get_fill_opacity() > 0:
            m.set_fill(opacity=opacity)
    if not names:
        for m in mob.get_family():
            if isinstance(m, Text):
                m.set_fill(opacity=0).set_stroke(opacity=0)
    return mob
