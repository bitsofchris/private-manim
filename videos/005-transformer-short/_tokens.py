"""Shared layout for the transformer short: the sentence, its values, and
where the L x d matrix sits so every beat opens on the previous beat's frame.

Import from a beat file:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _tokens import TOKENS, VALUES, build_matrix, word_labels, label

Value stages (all seeded): VALUES[0] embeddings, [1] after attention,
[2] after the feed-forward net, [3] after the whole stack. A beat that
"refines" the matrix animates col.set_values from one stage to the next.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from manim import DOWN, UP, Mobject, Text, VGroup
from videos._shared import style as S
from videos._shared.mobjects import TokenMatrix

TOKENS = ["the", "cat", "sat"]
TARGET = 2                      # the token that attends in beat 3 ("sat")
ATTN_WEIGHTS = [0.55, 0.3, 0.15]  # arcs from the, cat, sat(self) into "sat"
NEXT_TOKENS = [("on", 0.58), ("down", 0.27), ("still", 0.09)]  # head bars, beat 7

MATRIX_TOP_GAP = 1.85   # stage top -> matrix top: room for the word labels and the attention arcs above them
WORD_BUFF = 0.18        # word label above its column


def _stages() -> list[np.ndarray]:
    rng = np.random.default_rng(S.SEED)
    v = rng.uniform(-0.9, 0.9, size=(len(TOKENS), S.TOKEN_D_SHOWN))
    out = [v.round(1)]
    for _ in range(3):
        v = np.clip(v + rng.normal(0, 0.35, v.shape), -0.95, 0.95)
        out.append(v.round(1))
    return out


VALUES = _stages()


def label(s: str, color: str = S.FG, weight: str = "MEDIUM") -> Text:
    return Text(s, font=S.FONT, weight=weight).scale(S.SHORT_LABEL_SCALE).set_color(color)


def build_matrix(stage: Mobject, values=None, digits: bool = False,
                 bracketed: bool = True) -> TokenMatrix:
    """The L x d matrix in its canonical spot: top of the stage, centred."""
    m = TokenMatrix(VALUES[0] if values is None else values, digits=digits, bracketed=bracketed)
    m.move_to(stage).align_to(stage, UP).shift(DOWN * MATRIX_TOP_GAP)
    return m


def word_labels(m: TokenMatrix) -> VGroup:
    """Token words above their columns, in FG."""
    return VGroup(*[label(w).next_to(c, UP, buff=WORD_BUFF) for w, c in zip(TOKENS, m.columns)])


def tokens(m: TokenMatrix, words: VGroup) -> list[VGroup]:
    """word + column per token: pass these to attention_arcs so arcs leave
    from above the word, not through it."""
    return [VGroup(w, c) for w, c in zip(words, m.columns)]

# After beat 4 only the attending token has been updated; beat 5's FFN then
# moves every column to VALUES[2].
VALUES_AFTER_ATTN = VALUES[0].copy()
VALUES_AFTER_ATTN[TARGET] = VALUES[1][TARGET]
