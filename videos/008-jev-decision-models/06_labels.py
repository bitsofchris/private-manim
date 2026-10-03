"""Beat 6 (7.682 s): the probabilities only mean something on your data, so you need your own labels.

VO (47.47-55.15 s): "The hard part is calibration. The probabilities only mean
something on data like your own, so you need your own labels."
Frame 0: beat 2's probability bars filling in the upper half of the stage. On
"calibration" a confident magenta 0.92 readout appears beside a coin that
flips 50/50 (the fair-coin test); both fade before "data". On "data" a cloud
of teal data dots scatters into the lower half; on "your own labels" a magenta
tag stamps onto each dot. Hero: the 0.92 readout, then the label tags.

Render:
    cd videos/008-jev-decision-models && uv run --no-sync manim -qh 06_labels.py Labels
    # -> media/videos/06_labels/1920p30/Labels.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

import numpy as np
from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.mobjects import data_dot
from videos._shared.transformer import label
from _parts import ProbBars, mono

BEAT_SECONDS = 7.682   # exact VO window of this beat
T_CALIBRATION = 0.75   # VO: "calibration"
T_CLEAR = 3.70         # pause after "something"; the coin test leaves before "data"
T_DATA = 4.00          # VO: "data" (like your own)
T_LABELS = 6.20        # VO: "your own labels"; the stamps run through "labels"

CHOICES = ["bug", "query", "spam"]
PROBS = [0.91, 0.06, 0.03]
READOUT_SCALE = 1.5    # _parts.mono is the code-card size; the hero reads at label size
COIN_PAD = 0.3
N_DOTS = 12
DOT_R = S.DOT_SHORT * 0.6
TAG_SIDE = 0.22
MARGIN = 0.35          # keep dots off the stage edges


class Labels(BocShortScene):
    def construct(self):
        rng = np.random.default_rng(S.SEED)
        upper = Rectangle(width=self.stage.width, height=self.stage.height / 2,
                          stroke_opacity=0, fill_opacity=0).move_to(self.stage).align_to(self.stage, UP)
        lower = upper.copy().align_to(self.stage, DOWN)

        # Frame 0: beat 2's bars, filling immediately.
        bars = ProbBars(CHOICES, width=self.stage.width).move_to(upper)
        self.add(bars)
        self.play(bars.fill_to(PROBS), run_time=S.QUICK)

        # "calibration": a confident readout next to a coin that is really 50/50.
        readout = mono("0.92", S.STRUCTURE).scale(READOUT_SCALE)
        coin_label = label("50/50", S.FG_DIM)
        coin = VGroup(Circle(radius=coin_label.width / 2 + COIN_PAD, color=S.FG_DIM,
                             stroke_width=S.STROKE_AXIS * 3), coin_label)
        test = VGroup(readout, coin).arrange(RIGHT, buff=0.5).move_to(lower).align_to(bars, LEFT)
        self.hold_until(T_CALIBRATION)
        self.play(FadeIn(readout, scale=1.3), run_time=S.BEAT)
        self.play(FadeIn(coin), run_time=S.QUICK)
        self.play(coin.animate(rate_func=there_and_back).stretch(0.02, 0), run_time=S.BEAT)

        # "on data like your own": the coin test goes, your own data scatters in.
        self.hold_until(T_CLEAR)
        self.play(FadeOut(test), run_time=S.QUICK)
        pts = np.column_stack([
            rng.uniform(lower.get_left()[0] + MARGIN, lower.get_right()[0] - MARGIN, N_DOTS),
            rng.uniform(lower.get_bottom()[1] + MARGIN, lower.get_top()[1] - MARGIN, N_DOTS),
            np.zeros(N_DOTS),
        ])
        dots = VGroup(*[data_dot(p, radius=DOT_R) for p in pts])
        self.hold_until(T_DATA)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.1),
                  run_time=S.HOLD)

        # "your own labels": a magenta tag stamps onto each dot.
        tags = VGroup(*[
            Square(side_length=TAG_SIDE, fill_color=S.STRUCTURE, fill_opacity=1, stroke_width=0)
            .move_to(dot.get_center() + (UR * DOT_R * 1.1))
            for dot in dots
        ])
        self.hold_until(T_LABELS)
        self.play(LaggedStart(*[FadeIn(t, scale=3) for t in tags], lag_ratio=0.1), run_time=S.HOLD)

        self.hold_until(BEAT_SECONDS)
