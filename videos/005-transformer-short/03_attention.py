"""Beat 3 (13.82 s): attention lets "sat" collect a weighted sum of the other tokens.

VO (scene-local s): "Attention is what combines information across the
tokens" 0.05-3.4; "Each token asks a query ..." 3.4-6.4 ("query" ~4.5);
"Every token then offers a key ..." 6.4-9.5 ("key" ~7.5); "So each token
collects a weighted sum of these values" 9.5-11.9 ("weighted sum" ~10.8);
"that match the key and query" 11.9-13.8. No scene captions (VO captions are
burned in over self.band).

Opens on beat 2's end (words + bracketed matrix, VALUES[0]). Ends on words +
the same matrix + the magenta update column under "sat" at the stage bottom.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 03_attention.py Attention
    # -> media/videos/03_attention/1920p30/Attention.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from _tokens import TOKENS, TARGET, ATTN_WEIGHTS, VALUES, build_matrix, word_labels, tokens, label
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import TokenMatrix, attention_arcs

BEAT_SECONDS = 13.82
T_QUERY = 3.9      # tag drops in so it has landed on "query" (~4.5)
T_KEY = 6.9        # key tags land on "key" (~7.5)
T_SUM = 10.2       # flash + update column land on "weighted sum" (~10.8)
T_MATCH = 11.6     # arcs settle to their weights on "match the key and query"
T_CLEAR = 13.0     # arcs fade (BEAT) so beat 4 opens clean at 13.82

TAG_BUFF = 0.12                       # tag just under the matrix brackets
UNIFORM = [1 / len(TOKENS)] * len(TOKENS)  # before the match, every arc is equal


class Attention(BocShortScene):
    def construct(self):
        m = build_matrix(self.stage, values=VALUES[0], digits=True, bracketed=True)
        words = word_labels(m)
        toks = tokens(m, words)
        self.add(words, m)

        # "combines information across the tokens": equal-width arcs draw into "sat".
        arcs = attention_arcs(toks, toks[TARGET], UNIFORM)
        self.play(Create(arcs, lag_ratio=0.3), run_time=S.HOLD * 2)

        # "query": the question drops out of the sat token into the free region below.
        query = label("query?", S.STRUCTURE).next_to(m, DOWN, buff=TAG_BUFF)
        query.set_x(m.columns[TARGET].get_x())
        self.hold_until(T_QUERY)
        self.play(FadeIn(query, shift=DOWN * 0.5), run_time=S.HOLD)

        # "key": the other tokens answer with what they hold (dim, not a second hero).
        keys = VGroup(*[label("key", S.FG_DIM).next_to(m, DOWN, buff=TAG_BUFF).set_x(c.get_x())
                        for i, c in enumerate(m.columns) if i != TARGET])
        self.hold_until(T_KEY)
        self.play(FadeIn(keys, shift=DOWN * 0.5, lag_ratio=0.3), run_time=S.HOLD)

        # "weighted sum": a flash runs the arcs and the update column grows under
        # "sat", bottom cell first, taking the query's place.
        update = TokenMatrix(VALUES[1][TARGET:TARGET + 1], bracketed=False, dots=False,
                             color=S.STRUCTURE)
        update.align_to(self.stage, DOWN).set_x(m.columns[TARGET].get_x())
        ucol = update.columns[0]
        cells = [VGroup(c, n) for c, n in zip(ucol.cells, ucol.nums)][::-1]
        flash = arcs.copy().set_stroke(S.HIGHLIGHT, width=S.ATTN_ARC_MAX)
        self.hold_until(T_SUM)
        self.play(
            ShowPassingFlash(flash, time_width=0.4),
            FadeOut(query, shift=DOWN * 0.3),
            LaggedStart(*[GrowFromEdge(c, DOWN) for c in cells], lag_ratio=0.3),
            run_time=S.HOLD,
        )
        self.remove(*cells)  # GrowFromEdge added the wrapper groups; keep one mobject
        self.add(update)

        # "match the key and query": arcs settle to their weights; key tags go.
        settled = attention_arcs(toks, toks[TARGET], ATTN_WEIGHTS)
        self.hold_until(T_MATCH)
        self.play(Transform(arcs, settled), FadeOut(keys), run_time=S.HOLD)

        self.hold_until(T_CLEAR)
        self.play(FadeOut(arcs), run_time=S.BEAT)
        self.hold_until(BEAT_SECONDS)
