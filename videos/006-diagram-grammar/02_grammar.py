"""Beat 2 (8.27 s): no standard, but a grammar every figure inherits from one 2017 paper.

VO (3.99-12.26 s): "Now there's no formal standard, but there is a de facto
visual grammar. Almost every paper figure inherits it from Figure 1 in
Attention Is All You Need."
Opens on the complete dim diagram, still through "no formal standard". The
whole diagram pulses once on "visual grammar". The hero is a magenta tag
beside the Linear box: "Fig. 1" lands on "Figure 1", "2017" joins it on
"Attention". Still to the end. (An earlier take fanned ghost copies of the
diagram out behind it on "every paper figure"; they added motion, not meaning.)

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh --disable_caching 02_grammar.py Grammar
    # -> media/videos/02_grammar/1920p30/Grammar.mp4
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
T_FIGURE = 5.9        # VO: "figure one" (5.9-6.5)
T_TITLE = 6.6         # VO: "Attention" (Is All You Need)
PULSE = 1.06          # Indicate-like scale, no color change
TAG_BUFF = 0.3        # tag-to-box spacing (0.38 is the most that keeps the tag in safe)
TAG_GAP = 0.12        # between the two tag lines


class Grammar(BocShortScene):
    def construct(self):
        d = build_block(self.stage)
        self.add(d)   # frame 0: the complete dim diagram, exactly as beat 1 left it

        # "no formal standard": nothing moves.
        # "visual grammar": the whole diagram pulses once (scale, not color).
        self.hold_until(T_GRAMMAR)
        self.play(d.animate.scale(PULSE), rate_func=there_and_back, run_time=S.BEAT)

        # "Figure 1 ... Attention Is All You Need": the hero tag, stacked beside
        # Linear in the free space above the bracket, top-aligned with the box
        # so it stays inside the safe area.
        fig = transformer.label("Fig. 1", S.STRUCTURE)
        year = transformer.label("2017", S.STRUCTURE)
        tag = VGroup(fig, year).arrange(DOWN, buff=TAG_GAP, aligned_edge=RIGHT)
        tag.next_to(d.rows["head"], LEFT, buff=TAG_BUFF).align_to(d.rows["head"], UP)
        self.hold_until(T_FIGURE)
        self.play(FadeIn(fig, shift=RIGHT * 0.3), run_time=S.BEAT)
        self.hold_until(T_TITLE)
        self.play(FadeIn(year, shift=RIGHT * 0.3), run_time=S.BEAT)

        self.hold_until(BEAT_SECONDS)
