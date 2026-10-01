"""Beat 1 (6.20 s): a transformer takes tokens in and gives updated tokens out.

VO (scene-local s): "A transformer takes a sequence of tokens" 0.3-2.8
("tokens" ~2.3); "and produces updated representations of those tokens"
2.8-6.2 ("updated representations" ~3.9-5.2). No scene captions: VO captions
are burned in later over self.band.

Opens on the sentence "the cat sat" centred in the stage. The words spread
apart (a sequence), rise into their word_labels slots (tokens), then a teal
column of numbers grows down under each word (the representations).
Ends: words + unbracketed matrix (VALUES[0], digits), the state beat 2 opens on.

Render:
    cd videos/005-transformer-short && uv run --no-sync manim -qh 01_hook.py Hook
    # -> media/videos/01_hook/1920p30/Hook.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared
sys.path.insert(0, str(Path(__file__).resolve().parent))      # _tokens

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from _tokens import VALUES, build_matrix, word_labels

BEAT_SECONDS = 6.20
T_TOKENS = 1.2        # rise starts as the spread ends; words land in their slots on "tokens" (~2.3)
T_UPDATED = 3.9       # VO: "updated representations"
SENTENCE_BUFF = 0.35  # word spacing when the three words still read as one sentence
COLUMN_LAG = 0.25


class Hook(BocShortScene):
    def construct(self):
        # Built bracketed so the columns sit exactly where beat 2's bracketed
        # matrix puts them; only the columns are ever added here, so the end
        # state is still "words + unbracketed matrix".
        m = build_matrix(self.stage, values=VALUES[0], digits=True, bracketed=True)
        words = word_labels(m)
        slots = [w.get_center() for w in words]

        # Frame 0: the sentence, centred in the stage.
        sentence = VGroup(*words).arrange(RIGHT, buff=SENTENCE_BUFF).move_to(self.stage)
        self.add(words)

        # "a sequence": the words spread apart to their column x positions.
        spread = [np.array([p[0], sentence.get_y(), 0.0]) for p in slots]
        self.play(*[w.animate.move_to(p) for w, p in zip(words, spread)], run_time=S.HOLD)

        # "tokens": each word rises into its label slot above its column.
        self.hold_until(T_TOKENS)
        self.play(*[w.animate.move_to(p) for w, p in zip(words, slots)], run_time=S.HOLD)

        # "updated representations": a column of numbers grows down under each word.
        self.hold_until(T_UPDATED)
        self.play(LaggedStart(*[GrowFromEdge(c, UP) for c in m.columns],
                              lag_ratio=COLUMN_LAG), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)  # resting frame: words + columns
