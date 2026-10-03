"""Beat 1 (3.27 s): the word everyone is talking about, and the noise around it.

VO (0.00-3.27 s): "What is Jev and why is everyone so excited about it?"
Frame 0 is "Jev" big in the centre of the stage with six feed-style chips
already drifting in from the stage edges. They drift at a constant rate into
a loose ring around the word and stop on "why"; on "excited" the word pulses
once. No magenta hero in this beat. No scene captions (VO word captions are
burned in over self.band later).

Render:
    cd videos/008-jev-decision-models && uv run --no-sync manim -qh 01_hook.py Hook
    # -> media/videos/01_hook/1920p30/Hook.mp4
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import label
from _parts import chip_text

BEAT_SECONDS = 3.27   # exact VO window of this beat
T_WHY = 1.0           # VO: "why" (0.95-1.10); the drift is one S.HOLD from frame 0, so it settles at 1.2
T_EXCITED = 1.9       # VO: "excited" (1.90-2.30)
JEV_SCALE = 2.5       # the word, relative to a normal label
DRIFT = 2.2           # how far outside its ring slot each chip starts

# Ring slots: (text, y relative to the stage centre, which stage edge the chip
# hugs, drift direction it comes from). Zig-zag so the wide chips clear each
# other and the word; every chip ends inside the stage.
RING = [
    ("agents",         +3.05, RIGHT, UP + RIGHT),
    ("System One",     +2.50, LEFT,  UP + LEFT),
    ("100x faster?",   +1.40, RIGHT, RIGHT),
    ("calibrated?",    -1.35, LEFT,  LEFT),
    ("Jev vs LLMs",    -2.30, RIGHT, DOWN + RIGHT),
    ("decision model", -3.13, LEFT,  DOWN + LEFT),
]


class Hook(BocShortScene):
    def construct(self):
        cy = self.stage.get_center()[1]
        jev = label("Jev", S.FG).scale(JEV_SCALE).move_to(self.stage)
        self.add(jev)

        chips, slides = VGroup(), []
        for text, dy, edge, frm in RING:
            chip = chip_text(text)
            chip.move_to([0, cy + dy, 0]).align_to(self.stage, edge)
            chip.shift(normalize(frm) * DRIFT)   # frame 0: part way in from the edge
            chips.add(chip)
            slides.append(chip.animate.shift(-normalize(frm) * DRIFT))
        self.add(chips)

        # Drift in at a constant rate and stop on "why".
        self.play(*slides, run_time=S.HOLD, rate_func=linear)

        # "excited": the word pulses once.
        self.hold_until(T_EXCITED)
        self.play(jev.animate.scale(1.15), run_time=S.BEAT, rate_func=there_and_back)

        self.hold_until(BEAT_SECONDS)
