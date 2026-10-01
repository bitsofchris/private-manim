"""Recolor diagram marks without hiding their labels, shared by the 007 beats.

Trap: `self.play(VGroup(b.box for b in d.boxes).animate.set_stroke(...))`
re-adds that new VGroup at the top of the scene, and the renderer keeps the
LAST occurrence of each mobject, so the opaque box rects draw over their
`.name` Text and the labels vanish. `restroke()` animates the parent mark
groups instead (box then name, in order) via a Transform to a recolored copy.

    self.play(restroke(d.boxes, S.STRUCTURE, S.STROKE_STRUCTURE), run_time=S.BEAT)
    self.play(restroke([*d.boxes, *d.adds], S.STRUCTURE, S.STROKE_STRUCTURE,
                       rate_func=there_and_back), run_time=S.BEAT)   # flash
"""
from __future__ import annotations

from collections.abc import Iterable

from manim import Transform, VGroup, smooth


def outline(mark: VGroup) -> VGroup:
    """The stroked parts of a transformer mark: op_box `.box`, add_node `.circle` + `.plus`."""
    if hasattr(mark, "box"):
        return VGroup(mark.box)
    return VGroup(mark.circle, mark.plus)


def restroke(marks: Iterable[VGroup], color: str, width: float,
             rate_func=smooth) -> Transform:
    """Transform that sets each mark's outline stroke to `color`/`width`, labels untouched."""
    group = VGroup(*marks)
    target = group.copy()
    for m in target:
        outline(m).set_stroke(color, width=width)
    return Transform(group, target, rate_func=rate_func)

