"""Tests for videos/007-diagram-to-pytorch/_marks.py: restroke() recolors a
mark's outline and leaves its label alone. Builds mobjects, renders nothing.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "videos" / "007-diagram-to-pytorch"))

from manim import there_and_back  # noqa: E402

import _marks  # noqa: E402
from videos._shared import style as S  # noqa: E402
from videos._shared import transformer as T  # noqa: E402
from videos._shared.base import _rect, safe_bounds, stage_bounds  # noqa: E402


class Restroke(unittest.TestCase):
    def setUp(self):
        self.d = T.build_block(_rect(stage_bounds(safe_bounds())))

    def test_target_recolors_box_outlines_only(self):
        anim = _marks.restroke(self.d.boxes, S.STRUCTURE, S.STROKE_STRUCTURE)
        for mark in anim.target_mobject:
            self.assertEqual(mark.box.get_stroke_color().to_hex(), S.STRUCTURE)
            self.assertEqual(mark.box.get_stroke_width(), S.STROKE_STRUCTURE)
            self.assertEqual(mark.name.get_color().to_hex(), S.FG)
            self.assertEqual(mark.name.get_stroke_width(), 0)

    def test_add_nodes_recolor_circle_and_plus(self):
        anim = _marks.restroke(self.d.adds, S.STRUCTURE, S.STROKE_STRUCTURE)
        for mark in anim.target_mobject:
            self.assertEqual(mark.circle.get_stroke_color().to_hex(), S.STRUCTURE)
            for line in mark.plus:
                self.assertEqual(line.get_stroke_color().to_hex(), S.STRUCTURE)

    def test_source_marks_are_the_diagram_in_label_order(self):
        anim = _marks.restroke(self.d.boxes, S.STRUCTURE, S.STROKE_STRUCTURE)
        for src, mark in zip(anim.mobject, self.d.boxes):
            self.assertIs(src, mark)
            self.assertIs(src.submobjects[-1], mark.name)   # label drawn last
            self.assertEqual(mark.box.get_stroke_color().to_hex(), S.FG_DIM)  # untouched

    def test_rate_func_passthrough(self):
        anim = _marks.restroke(self.d.boxes, S.STRUCTURE, 5, rate_func=there_and_back)
        self.assertIs(anim.rate_func, there_and_back)


if __name__ == "__main__":
    unittest.main()
