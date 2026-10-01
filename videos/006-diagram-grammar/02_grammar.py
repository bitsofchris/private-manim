"""Beat 2 (8.27 s): no standard, but a grammar every figure inherits from one 2017 paper.

VO (3.99-12.26 s): "Now there's no formal standard, but there is a de facto
visual grammar. Almost every paper figure inherits it from Figure 1 in
Attention Is All You Need."
Opens on the complete dim diagram, still through "no formal standard". The
whole diagram pulses once on "visual grammar". Two ghost copies fan out beside
it on "every paper figure" (every later figure is a copy). The hero, a magenta
"2017" tag, fades in beside the Linear box on "Attention". Still to the end.

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh --disable_caching 02_grammar.py Grammar
    # -> media/videos/02_grammar/1920p30/Grammar.mp4 (cached partials can drop a frame; keep --disable_caching)
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared import transformer
from videos._shared.transformer import build_block

BEAT_SECONDS = 8.27   # exact VO window of this beat
T_GRAMMAR = 2.75      # VO: "visual" (pulse peaks on "grammar")
T_FIGURES = 4.5       # VO: "every paper figure" (ghosts settle on "inherits")
T_TITLE = 6.6         # VO: "Attention" (Is All You Need)
PULSE = 1.06          # Indicate-like scale, no color change
GHOST_SCALE = 0.8
GHOST_SHIFT = (2.5, -0.6)    # (|dx|, dy) of each ghost from the real diagram
TAG_BUFF = 0.3        # tag-to-box spacing (0.38 is the most that keeps the tag in safe)


def ghost_of(m: Mobject, k: float) -> Mobject:
    """A faint copy: every stroke and fill opacity scaled by k (no set_opacity:
    in 0.18.1 it fills stroke-only paths)."""
    g = m.copy()
    if hasattr(m, "bracket"):   # a ghost figure has no N×: it would smear the real one
        g.remove(g.submobjects[m.submobjects.index(m.bracket)])
    for sub in g.family_members_with_points():
        sub.set_stroke(opacity=sub.get_stroke_opacity() * k)
        sub.set_fill(opacity=sub.get_fill_opacity() * k)
    for sub in g.get_family():   # outlines only: ghost labels smear the real N× and boxes
        if isinstance(sub, Text):
            sub.set_fill(opacity=0).set_stroke(opacity=0)
    return g


class Grammar(BocShortScene):
    def construct(self):
        d = build_block(self.stage)
        self.add(d)   # frame 0: the complete dim diagram, exactly as beat 1 left it

        # "no formal standard": nothing moves.
        # "visual grammar": the whole diagram pulses once (scale, not color).
        self.hold_until(T_GRAMMAR)
        self.play(d.animate.scale(PULSE), rate_func=there_and_back, run_time=S.BEAT)

        # "every paper figure inherits it": two smaller ghost copies fan out
        # beside the real one and settle. They are background and may bleed
        # past the safe area; the real diagram stays put.
        self.hold_until(T_FIGURES)
        dx, dy = GHOST_SHIFT
        ghosts = VGroup(*[
            ghost_of(d, S.OP_GHOST).scale(GHOST_SCALE).shift([sx * dx, dy, 0])
            for sx in (-1, 1)
        ])
        self.play(*[TransformFromCopy(d, g) for g in ghosts], run_time=S.HOLD)
        self.remove(d)
        self.add(d)   # real diagram back in front of the ghosts

        # "Attention Is All You Need": the hero, a magenta "2017" tag, lands
        # beside the Linear box in free space inside the safe area.
        self.hold_until(T_TITLE)
        tag = transformer.label("2017", S.STRUCTURE)
        tag.next_to(d.rows["head"], LEFT, buff=TAG_BUFF)
        self.play(FadeIn(tag, shift=RIGHT * 0.3), run_time=S.BEAT)

        self.hold_until(BEAT_SECONDS)
