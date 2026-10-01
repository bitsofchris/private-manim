"""Beat 2 (9.08 s): zoom into the matrix; a token is a d-vector, L of them an
L x d matrix that every block preserves.

VO (scene-local s): "Each token is a vector of D numbers" 0.1-2.7 ("D numbers"
~1.9); "and a sequence of L tokens is then an L by D matrix" 2.8-6.4
("L by D matrix" ~5.0-6.4); "Every block in the transformer stack keeps that
shape" 6.5-9.1 ("keeps that shape" ~8.0). No scene captions (VO captions are
burned in over self.band).

Opens on beat 1's end (`opening_state` from 01_hook.py): dim diagram + the tiny
matrix above its N× block. The diagram fades as the tiny columns and words grow
into the canonical matrix (the zoom). One column is indicated and gets a
magenta "d" brace; an "L" brace spans the words; the shared bracket pair draws
in; the tags leave and the brackets pulse.
Ends: words + bracketed matrix (VALUES[0], digits), no tags: the state beat 3
opens on.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 02_matrix.py Matrix
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
T_INDICATE = 1.2      # the zoom lands; digits resolve and the first column lights up for "is a vector"
T_D = 1.8             # brace grows under "D numbers" (~1.9)
T_L = 3.4             # VO: "L tokens"
T_MATRIX = 5.0        # VO: "L by D matrix"
T_TAGS_OUT = 7.0      # tags leave before "keeps that shape"
T_SHAPE = 7.6         # VO: "keeps that shape" (~8.0)
D_COL = 0             # the column tagged "d"
BRACE_BUFF = 0.08
TAG_BUFF = 0.1
INDICATE_SCALE = 1.08


class Matrix(BocShortScene):
    def construct(self):
        # Beat 1's final frame.
        diagram, tiny, tiny_words = opening_state(self.stage)
        self.add(diagram, tiny, tiny_words)

        # Built bracketed so the columns sit exactly where beat 3's bracketed
        # matrix puts them; the brackets are drawn in later. The zoom targets
        # a digit-less twin at the same spot: Transform aligns point data on
        # its target too, and the tiny columns have no digits to align with.
        m = build_matrix(self.stage, values=VALUES[0], digits=True, bracketed=True)
        zoomed = build_matrix(self.stage, values=VALUES[0], digits=False, bracketed=True)
        words = word_labels(m)

        # "Each token": the zoom. The diagram fades while the tiny columns and
        # words grow into the full matrix (same mobjects: a token keeps its
        # identity through the zoom).
        self.play(FadeOut(diagram),
                  *[Transform(tc, c) for tc, c in zip(tiny.columns, zoomed.columns)],
                  *[Transform(tw, w) for tw, w in zip(tiny_words, words)],
                  run_time=S.HOLD)
        # Swap in the canonical objects (identical frame) so later beats match;
        # the digits are still hidden.
        nums = VGroup(*[c.nums for c in m.columns]).set_opacity(0)
        self.remove(tiny, tiny_words)
        self.add(words, m.columns)

        # "is a vector of": the first column lights up as the numbers resolve.
        col = m.columns[D_COL]
        self.hold_until(T_INDICATE)
        # (Indicate the cells, not the column: Indicate snapshots its mobject,
        # and a snapshot of the column would hold the digits at opacity 0.)
        self.play(nums.animate.set_opacity(1),
                  Indicate(col.cells, color=S.HIGHLIGHT, scale_factor=INDICATE_SCALE),
                  run_time=S.BEAT)

        # "D numbers": a magenta brace along the column's cells, "d" below it
        # (the gutter beside the matrix is too narrow for a side label).
        self.hold_until(T_D)
        d_brace = Brace(col.cells, LEFT, buff=BRACE_BUFF, color=S.STRUCTURE)
        d_tag = label("d", S.STRUCTURE).next_to(d_brace, DOWN, buff=TAG_BUFF)
        self.play(GrowFromCenter(d_brace), FadeIn(d_tag), run_time=S.HOLD)

        # "L tokens": a magenta brace across the three words, "L" above it.
        self.hold_until(T_L)
        l_brace = Brace(words, UP, buff=TAG_BUFF, color=S.STRUCTURE)
        l_tag = label("L", S.STRUCTURE).next_to(l_brace, UP, buff=TAG_BUFF)
        self.play(GrowFromCenter(l_brace), FadeIn(l_tag), run_time=S.HOLD)

        # "L by D matrix": the shared bracket pair draws in around the columns.
        self.hold_until(T_MATRIX)
        self.play(Create(m.brackets, lag_ratio=0.0), run_time=S.HOLD)

        # "keeps that shape": the tags leave, then the bracket outline pulses.
        self.hold_until(T_TAGS_OUT)
        self.play(*[FadeOut(x) for x in (d_brace, d_tag, l_brace, l_tag)], run_time=S.BEAT)
        self.hold_until(T_SHAPE)
        self.play(Indicate(m.brackets, color=S.HIGHLIGHT, scale_factor=1.03), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)  # resting frame: words + bracketed matrix
