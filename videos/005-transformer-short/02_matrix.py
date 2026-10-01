"""Beat 2 (9.08 s): a token is a d-vector; L tokens make an L x d matrix that
every block preserves.

VO (scene-local s): "Each token is a vector of D numbers" 0.1-2.7 ("D numbers"
~1.9); "and a sequence of L tokens is then an L by D matrix" 2.8-6.4
("L by D matrix" ~5.0-6.4); "Every block in the transformer stack keeps that
shape" 6.5-9.1 ("keeps that shape" ~8.0). No scene captions (VO captions are
burned in over self.band).

Opens on beat 1's end: words + the unbracketed matrix. One column is
indicated and gets a magenta "d" brace; an "L" brace spans the words; the
shared bracket pair draws in; the brackets pulse and the tags fade.
Ends: words + bracketed matrix (VALUES[0]), no tags.

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

BEAT_SECONDS = 9.08
T_D = 1.4             # brace grows so "d" is on screen for "D numbers" (~1.9)
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
        m = build_matrix(self.stage, values=VALUES[0], digits=True, bracketed=True)
        words = word_labels(m)
        self.add(words, m.columns)  # beat 1's final frame; brackets come later

        # "Each token is a vector": the first column lights up at once.
        col = m.columns[D_COL]
        self.play(Indicate(col, color=S.HIGHLIGHT, scale_factor=INDICATE_SCALE), run_time=S.HOLD)

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
        self.play(FadeOut(VGroup(d_brace, d_tag, l_brace, l_tag)), run_time=S.BEAT)
        self.hold_until(T_SHAPE)
        self.play(Indicate(m.brackets, color=S.HIGHLIGHT, scale_factor=1.03), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)  # resting frame: words + bracketed matrix
