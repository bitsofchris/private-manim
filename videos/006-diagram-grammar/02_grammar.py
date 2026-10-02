"""Beat 2 (8.27 s): no standard, but a grammar every figure inherits from one 2017 paper.

VO (3.99-12.26 s): "Now there's no formal standard, but there is a de facto
visual grammar. Almost every paper figure inherits it from Figure 1 in
Attention Is All You Need."
Opens on the complete dim diagram, still through "no formal standard"; it
pulses once on "visual grammar". On "every paper figure" the diagram
cross-fades to the real Figure 1 (figure1_aiayn.png, Vaswani et al. 2017).
On "Figure 1" the figure zooms to its decoder column; on "Attention Is All
You Need" our diagram fades in on top of it and the figure fades away, so
the beat ends on the untouched diagram (beat 3's opener). No hero: the
reveal is that ours is a redraw of theirs.

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
from videos._shared.transformer import build_block

BEAT_SECONDS = 8.27   # exact VO window of this beat
T_GRAMMAR = 2.75      # VO: "visual" (pulse peaks on "grammar")
T_FIGURES = 3.75      # VO: "Almost every paper figure": cross-fade to the paper's figure
T_FIG1 = 5.9          # VO: "figure one": zoom to the decoder column
T_OVERLAY = 7.1       # VO: "all you need": our diagram fades in over it
PULSE = 1.06          # Indicate-like scale, no color change

FIGURE = Path(__file__).with_name("figure1_aiayn.png")
# Decoder column of the figure, as fractions of the image (x: left->right,
# y: top->bottom): from "Output Probabilities" down to "Output Embedding".
DECODER_X = (0.52, 0.90)
DECODER_Y = (0.06, 0.88)
ZOOM = 2.0            # the column is 82% of the figure's height, so fitting it to the
                      # stage is no zoom at all; 2x bleeds past the stage like a background


def decoder_zoom(img: ImageMobject) -> np.ndarray:
    """Where the decoder column's centre lands after scale(ZOOM) about the image centre."""
    cx = img.get_left()[0] + (DECODER_X[0] + DECODER_X[1]) / 2 * img.width
    cy = img.get_top()[1] - (DECODER_Y[0] + DECODER_Y[1]) / 2 * img.height
    c = img.get_center()
    return c + (np.array([cx, cy, 0]) - c) * ZOOM


class Grammar(BocShortScene):
    def construct(self):
        d = build_block(self.stage)
        self.add(d)   # frame 0: the complete dim diagram, exactly as beat 1 left it

        # "no formal standard": nothing moves. "visual grammar": one pulse.
        self.hold_until(T_GRAMMAR)
        self.play(d.animate.scale(PULSE), rate_func=there_and_back, run_time=S.BEAT)

        # "Almost every paper figure": the real Figure 1 replaces our diagram
        # (a different object, so a cross-fade, not a Transform).
        fig = ImageMobject(str(FIGURE)).scale_to_fit_height(self.stage.height)
        fig.move_to(self.stage)
        self.hold_until(T_FIGURES)
        self.play(FadeOut(d), FadeIn(fig), run_time=S.HOLD)

        # "Figure 1": zoom into the decoder column (the one ours redraws).
        col = decoder_zoom(fig)
        self.hold_until(T_FIG1)
        self.play(fig.animate.scale(ZOOM).move_to(self.stage.get_center() - (col - fig.get_center())),
                  run_time=S.HOLD)

        # "Attention Is All You Need": ours fades in on top, theirs fades away.
        self.hold_until(T_OVERLAY)
        self.play(FadeIn(d), fig.animate.set_opacity(0), run_time=S.HOLD)
        self.remove(fig)

        self.hold_until(BEAT_SECONDS)
