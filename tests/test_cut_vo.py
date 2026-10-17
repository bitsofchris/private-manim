"""Unit tests for tools/cut_vo.py's pure logic (no ffmpeg needed)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import cut_vo as cv  # noqa: E402

CUTS = [(1.0, 2.0, 0.1), (3.0, 3.5, 0.0)]


class Shift(unittest.TestCase):
    def test_before_any_cut_unchanged(self):
        self.assertEqual(cv.shift(0.5, CUTS), 0.5)

    def test_inside_a_cut_is_none(self):
        self.assertIsNone(cv.shift(1.5, CUTS))

    def test_after_cuts_shifts_by_removed_minus_silence(self):
        self.assertAlmostEqual(cv.shift(2.5, CUTS), 1.6)   # 1.0 removed, 0.1 put back
        self.assertAlmostEqual(cv.shift(4.0, CUTS), 2.6)   # plus 0.5

    def test_cut_from_zero_drops_the_opening(self):
        self.assertAlmostEqual(cv.shift(8.0, [(0.0, 7.85, 0.0)]), 0.15)


class Words(unittest.TestCase):
    def test_words_inside_cut_drop_and_later_words_shift(self):
        words = [{"t": 0.5, "end": 0.8, "word": "a"}, {"t": 1.2, "end": 1.4, "word": "b"},
                 {"t": 2.2, "end": 2.4, "word": "c"}]
        out = cv.shift_words(words, CUTS)
        self.assertEqual([w["word"] for w in out], ["a", "c"])
        self.assertAlmostEqual(out[1]["t"], 1.3)


class Audio(unittest.TestCase):
    def test_length_matches_the_plan(self):
        x = np.ones(cv.SR * 5, np.float32)
        y = cv.cut_audio(x, CUTS)
        self.assertAlmostEqual(len(y) / cv.SR, 5 - 1.0 + 0.1 - 0.5, places=3)

    def test_tail_is_sample_identical(self):
        x = np.random.default_rng(0).standard_normal(cv.SR * 5).astype(np.float32)
        y = cv.cut_audio(x, CUTS)
        n = cv.SR  # the last second, well past the fades
        np.testing.assert_array_equal(y[-n:], x[-n:])


if __name__ == "__main__":
    unittest.main()
