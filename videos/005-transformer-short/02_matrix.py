"""Beat 2 (9.08 s): zoom into the matrix; a token is a d-vector, L of them an
L x d matrix that every block preserves.

VO (scene-local s): "Each token is a vector of D numbers" 0.1-2.7 ("D numbers"
~1.9); "and a sequence of L tokens is then an L by D matrix" 2.8-6.4
("L by D matrix" ~5.0-6.4); "Every block in the transformer stack keeps that
shape" 6.5-9.1 ("keeps that shape" ~8.0). No scene captions (VO captions are
burned in over self.band).

Opens on beat 1's end (`opening_state` from 01_hook.py): dim diagram + the
small X′ matrix above its N× block. The diagram and "X′" fade while the small
matrix grows into the canonical bracketed matrix (the zoom); the words and
digits fade in as it lands. One column is indicated and gets a magenta "d"
brace; an "L" brace spans the words; a flash traces the brackets; the tags
leave and the brackets pulse.
Ends: words + bracketed matrix (VALUES[0], digits), no tags: the state beat 3
opens on.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh --disable_caching 02_matrix.py Matrix
    # -> media/videos/02_matrix/1920p30/Matrix.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from _tokens import VALUES, build_matrix, word_labels, label
from importlib import import_module
opening_state = import_module("01_hook").opening_state

BEAT_SECONDS = 9.08
T_LAND = 1.2          # the zoom lands: words + digits fade in, the first column lights up
T_D = 1.8             # brace grows under "D numbers" (~1.9)
T_L = 3.4             # VO: "L tokens"
T_MATRIX = 5.0        # VO: "L by D matrix"
T_TAGS_OUT = 7.0      # tags leave before "keeps that shape"
T_SHAPE = 7.6         # VO: "keeps that shape" (~8.0)
D_COL = 0             # the column tagged "d"
BRACE_BUFF = 0.29     # cells -> brace: clears the left bracket (0.25 + its stroke)
TAG_BUFF = 0.1
SAFE_PAD = 0.05       # tag keeps this much inside the safe area
INDICATE_SCALE = 1.08
FLASH_WIDTH = 0.5     # ShowPassingFlash time_width along the brackets


class Matrix(BocShortScene):
    def construct(self):
        # Beat 1's final frame.
        diagram, small, small_label = opening_state(self.stage)
        self.add(diagram, small, small_label)

        # The zoom targets a digit-less twin of the canonical matrix: Transform
        # aligns point data on its target, and the small matrix has no digits.
        m = build_matrix(self.stage, values=VALUES[0], digits=True, bracketed=True)
        zoomed = build_matrix(self.stage, values=VALUES[0], digits=False, bracketed=True)
        words = word_labels(m)

        # "Each token": the zoom. The diagram and "X′" fade while the small
        # matrix grows into the full one (same mobject: the tokens keep their
        # identity through the zoom).
        self.play(FadeOut(diagram), FadeOut(small_label), Transform(small, zoomed),
                  run_time=S.HOLD)
        # Swap in the canonical objects (identical frame) so later beats match;
        # the digits are still hidden.
        nums = VGroup(*[c.nums for c in m.columns]).set_opacity(0)
        self.remove(small)
        self.add(m)

        # The zoom lands: words and digits resolve, the first column lights up
        # for "is a vector". (Indicate the cells, not the column: Indicate
        # snapshots its mobject, and the snapshot would hold invisible digits.)
        col = m.columns[D_COL]
        self.hold_until(T_LAND)
        self.play(FadeIn(words), nums.animate.set_opacity(1),
                  Indicate(col.cells, color=S.HIGHLIGHT, scale_factor=INDICATE_SCALE),
                  run_time=S.BEAT)

        # "D numbers": a magenta brace along the column's cells, outside the
        # left bracket, "d" under the matrix's corner (kept inside the safe area).
        self.hold_until(T_D)
        d_brace = Brace(col.cells, LEFT, buff=BRACE_BUFF, color=S.STRUCTURE)
        d_tag = label("d", S.STRUCTURE).next_to(m, DOWN, buff=TAG_BUFF).set_x(d_brace.get_x())
        d_tag.set_x(max(d_tag.get_x(), self.safe.get_left()[0] + SAFE_PAD + d_tag.width / 2))
        self.play(GrowFromCenter(d_brace), FadeIn(d_tag), run_time=S.HOLD)

        # "L tokens": a magenta brace across the three words, "L" above it.
        self.hold_until(T_L)
        l_brace = Brace(words, UP, buff=TAG_BUFF, color=S.STRUCTURE)
        l_tag = label("L", S.STRUCTURE).next_to(l_brace, UP, buff=TAG_BUFF)
        self.play(GrowFromCenter(l_brace), FadeIn(l_tag), run_time=S.HOLD)

        # "L by D matrix": a flash traces the bracket pair that is already there.
        self.hold_until(T_MATRIX)
        flash = m.brackets.copy().set_stroke(S.HIGHLIGHT, width=S.STROKE_STRUCTURE * 1.6)
        self.play(ShowPassingFlash(flash, time_width=FLASH_WIDTH), run_time=S.HOLD)

        # "keeps that shape": the tags leave, then the bracket outline pulses.
        self.hold_until(T_TAGS_OUT)
        self.play(*[FadeOut(x) for x in (d_brace, d_tag, l_brace, l_tag)], run_time=S.BEAT)
        self.hold_until(T_SHAPE)
        self.play(Indicate(m.brackets, color=S.HIGHLIGHT, scale_factor=1.03), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)  # resting frame: words + bracketed matrix
