"""Pure-logic tests for the Shorts helpers in videos/_shared (safe area,
caption split, hold timing, code highlight span). Imports Manim, renders nothing.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from videos._shared import style as S  # noqa: E402
from videos._shared.base import (  # noqa: E402
    caption_band, hold_remaining, safe_bounds, split_caption, stage_bounds,
)
from videos._shared.mobjects import line_span  # noqa: E402


class SafeArea(unittest.TestCase):
    def test_default_short_safe_area(self):
        b = safe_bounds()
        self.assertAlmostEqual(b.top, 8 - 0.12 * 16)
        self.assertAlmostEqual(b.bottom, -8 + 0.20 * 16)
        self.assertAlmostEqual(b.right, 4.5 - 0.12 * 9)
        self.assertAlmostEqual(b.left, -4.5 + S.SHORT_SAFE_LEFT * 9)

    def test_band_and_stage_split_safe_area_one_to_two(self):
        b = safe_bounds()
        band, stage = caption_band(b), stage_bounds(b)
        self.assertAlmostEqual(band.bottom, b.bottom)
        self.assertAlmostEqual(band.top, stage.bottom)
        self.assertAlmostEqual(stage.top, b.top)
        self.assertAlmostEqual(stage.height, 2 * band.height)

    def test_frame_aspect_is_9_16(self):
        self.assertAlmostEqual(S.SHORT_FRAME_W / S.SHORT_FRAME_H, S.SHORT_W / S.SHORT_H)


class SplitCaption(unittest.TestCase):
    def test_balanced(self):
        self.assertEqual(split_caption("lots of parameters"), ["lots of", "parameters"])
        self.assertEqual(split_caption("step opposite the gradient"),
                         ["step opposite", "the gradient"])

    def test_single_word_stays(self):
        self.assertEqual(split_caption("backprop"), ["backprop"])


class HoldRemaining(unittest.TestCase):
    def test_waits_the_gap(self):
        self.assertAlmostEqual(hold_remaining(2.5, 4.0, 30), 1.5)

    def test_zero_when_there_or_past_or_under_a_frame(self):
        for now in (4.0, 4.5, 4.0 - 0.01):
            with self.subTest(now=now):
                self.assertEqual(hold_remaining(now, 4.0, 30), 0.0)


class LineSpan(unittest.TestCase):
    def test_int_and_iterable(self):
        self.assertEqual(line_span(3, 9), (3, 3))
        self.assertEqual(line_span([8, 2, 5], 9), (2, 8))

    def test_out_of_range(self):
        for bad in (0, 10, []):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                line_span(bad, 9)


if __name__ == "__main__":
    unittest.main()
