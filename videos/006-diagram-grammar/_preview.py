"""Layout check only: the full block diagram in the stage with guides. Not a beat.

Render:
    cd videos/006-diagram-grammar && uv run --no-sync manim -ql _preview.py Preview
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root for videos._shared

from manim import *
from videos._shared import style as S
from videos._shared.base import BocShortScene
from videos._shared.transformer import build_block


class Preview(BocShortScene):
    def construct(self):
        self.show_guides()
        d = build_block(self.stage)
        d.skips.set_stroke(S.STRUCTURE)   # one hero, to see it reads
        self.add(d)
        self.wait(0.1)
