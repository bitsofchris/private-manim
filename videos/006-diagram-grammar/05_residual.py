"""Beat 5 (16.84 s): the bypass arrow + (+) are the residual path; the column is the residual stream.

VO (master 26.81-43.65): "An arrow that bypasses a box is the residual path.
The circle with the plus is where it adds its new updated vector back in.
That vertical highway is the residual stream, and everything reads from it,
adding information back to it as we refine our representation through the
layers."
Hero: the two skip paths, then the (+) nodes join them; both hand off to a
translucent magenta band under the column (the stream). A teal token dot
splits around Attention, merges at (+), then rides the stream, dipping into
each box and back. Cue times are from vo_final.wav (RMS envelope), beat-local.

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -qh 05_residual.py Residual
    # -> media/videos/05_residual/1920p30/Residual.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot
from videos._shared.transformer import EDGE_WIDTH, build_block

BEAT_SECONDS = 16.84   # exact VO window of this beat
T_BYPASS = 1.00        # VO: "bypasses"      -> skips magenta
T_CIRCLE = 3.65        # VO: "circle"        -> (+) nodes magenta
T_ADDS = 5.00          # VO: "adds"          -> token dot appears below Attention
T_VECTOR = 5.95        # VO: "its new updated vector" -> dot splits: through Attention / around
T_BACK = 7.15          # VO: "back in"       -> the two copies merge at (+)
T_THAT = 8.10          # VO: "That vertical" -> skips and (+) back to dim
T_HIGHWAY = 8.75       # VO: "highway"       -> stream band grows up the column
T_STREAM = 10.10       # VO: "stream"        -> dot drops to the bottom of the stream
T_READS = 11.25        # VO: "reads"         -> dot dips into Attention
T_FROM = 11.85         # VO: "from it"       -> and back into the stream at (+)
T_INFO = 12.45         # VO: "information"   -> dot dips into FFN
T_BACK_TO = 13.25      # VO: "back to it"    -> and back into the stream at (+)
T_LAYERS = 14.65       # VO: "representation through the layers" -> dot rides to the top
HERO_WIDTH = max(S.STROKE_STRUCTURE, EDGE_WIDTH * 1.4)   # hero stroke, never thinner than the diagram
BAND_W_FRAC = 0.9      # stream band width as a fraction of a box (sits under the boxes)


class Residual(BocShortScene):
    def construct(self):
        d = build_block(self.stage)
        rows = d.rows
        col_x = rows["attn"].get_center()[0]
        band_bottom, band_top = rows["embed"].get_center()[1], rows["head"].get_center()[1]
        # The stream band lives under the diagram: layer by add() order (a
        # negative z_index hides a mobject while it animates in 0.18.1).
        band_full = Rectangle(width=rows["attn"].width * BAND_W_FRAC, height=band_top - band_bottom,
                              fill_color=S.STRUCTURE, fill_opacity=S.OP_GHOST, stroke_width=0)
        band_full.move_to([col_x, (band_bottom + band_top) / 2, 0])
        band = band_full.copy().set_fill(opacity=0).stretch_to_fit_height(0.001)
        band.align_to(band_full, DOWN)
        self.add(band, d)  # frame 0: the complete dim diagram

        # "An arrow that": a cue on the bypass arrows before they become the hero.
        self.play(Indicate(d.skips, color=S.HIGHLIGHT, scale_factor=1.03), run_time=S.BEAT)

        # "bypasses": the two skip paths are the residual path -> magenta.
        self.hold_until(T_BYPASS)
        self.play(d.skips.animate.set_stroke(S.STRUCTURE, width=HERO_WIDTH), run_time=S.BEAT)

        # "circle with the plus": the (+) nodes join the hero.
        self.hold_until(T_CIRCLE)
        self.play(d.adds.animate.set_stroke(S.STRUCTURE, width=HERO_WIDTH), run_time=S.BEAT)

        # "adds": one token, just below Attention (where the skip branches off).
        self.hold_until(T_ADDS)
        start = d.skips[0].get_start()
        dot = data_dot(start, radius=S.DOT_SHORT)
        self.play(FadeIn(dot), run_time=S.BEAT)

        # "its new updated vector": it splits; one copy goes through Attention,
        # the other rides the skip path around it, both to the (+).
        self.hold_until(T_VECTOR)
        ghost = dot.copy()
        self.add(ghost)
        add1 = rows["add1"].get_center()
        self.play(dot.animate.move_to(add1), MoveAlongPath(ghost, d.skips[0]), run_time=S.HOLD)

        # "back in": the two merge into one at the (+).
        self.hold_until(T_BACK)
        merged = dot.copy().move_to(add1)
        self.play(Transform(dot, merged), Transform(ghost, merged), run_time=S.BEAT)
        self.remove(ghost)

        # "That vertical": skips and (+) hand the hero off.
        self.hold_until(T_THAT)
        self.play(d.skips.animate.set_stroke(S.FG_DIM, width=EDGE_WIDTH),
                  d.adds.animate.set_stroke(S.FG_DIM, width=EDGE_WIDTH), run_time=S.BEAT)

        # "highway": the stream band grows up the column, Embed to Linear.
        self.hold_until(T_HIGHWAY)
        self.play(Transform(band, band_full), run_time=S.HOLD)

        # "stream": the token drops to the bottom of the stream.
        self.hold_until(T_STREAM)
        self.play(dot.animate.move_to(start), run_time=S.BEAT)

        # "reads from it": into Attention, then back into the stream at (+).
        self.hold_until(T_READS)
        self.play(dot.animate.move_to(rows["attn"].get_center()), run_time=S.BEAT)
        self.hold_until(T_FROM)
        self.play(dot.animate.move_to(add1), run_time=S.BEAT)

        # "adding information back to it": into FFN, then back at the second (+).
        self.hold_until(T_INFO)
        self.play(dot.animate.move_to(rows["ffn"].get_center()), run_time=S.BEAT)
        self.hold_until(T_BACK_TO)
        self.play(dot.animate.move_to(rows["add2"].get_center()), run_time=S.BEAT)

        # "through the layers": the token rides the stream to the top and stops.
        self.hold_until(T_LAYERS)
        top = (rows["add2"].get_top() + rows["head"].get_bottom()) / 2
        self.play(dot.animate.move_to(top), run_time=S.HOLD)
        self.hold_until(BEAT_SECONDS)
