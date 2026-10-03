"""Tests for videos/008-jev-decision-models/_parts.py. Imports Manim, renders nothing.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "videos" / "008-jev-decision-models"))

import _parts as P  # noqa: E402
from videos._shared.base import _rect, safe_bounds, stage_bounds  # noqa: E402


class BarWidth(unittest.TestCase):
    def test_scales_with_probability(self):
        self.assertAlmostEqual(P.bar_width(0.5, 4.0), 2.0)

    def test_zero_is_a_sliver_not_nothing(self):
        self.assertEqual(P.bar_width(0.0, 4.0), P.MIN_BAR)

    def test_rejects_out_of_range(self):
        for bad in (-0.1, 1.1):
            with self.assertRaises(ValueError):
                P.bar_width(bad, 4.0)


class Bars(unittest.TestCase):
    def test_fits_the_stage_width_and_keeps_one_row_per_choice(self):
        stage = _rect(stage_bounds(safe_bounds()))
        bars = P.ProbBars(["yes", "no", "later"], width=stage.width)
        self.assertEqual(len(bars.bars), 3)
        self.assertLessEqual(bars.width, stage.width + 1e-6)

    def test_fill_to_returns_one_animation_per_bar_and_value(self):
        bars = P.ProbBars(["yes", "no"], width=6.0)
        self.assertEqual(len(bars.fill_to([0.9, 0.1]).animations), 4)


if __name__ == "__main__":
    unittest.main()
