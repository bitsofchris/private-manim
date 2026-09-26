"""Unit tests for tools/captions_from_transcript.py."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import captions_from_transcript as cft  # noqa: E402

SAMPLE = """00:01.730-00:03.490
A neural network is just a function

00:03.490-01:05.340
with a lot of parameters.
"""


class Parse(unittest.TestCase):
    def test_parses_minutes_and_seconds(self):
        segs = cft.parse_transcript(SAMPLE)
        self.assertEqual(len(segs), 2)
        self.assertAlmostEqual(segs[0][0], 1.73)
        self.assertAlmostEqual(segs[1][1], 65.34)
        self.assertEqual(segs[0][2], "A neural network is just a function")


class Chunking(unittest.TestCase):
    def test_balanced_groups(self):
        self.assertEqual(cft.chunk_words(list("abcdefg"), 3), [list("abc"), list("de"), list("fg")])

    def test_short_input_single_group(self):
        self.assertEqual(cft.chunk_words(["a", "b"], 3), [["a", "b"]])

    def test_never_exceeds_max(self):
        for n in range(1, 20):
            for g in cft.chunk_words([str(i) for i in range(n)], 3):
                self.assertLessEqual(len(g), 3)


class Timing(unittest.TestCase):
    def test_captions_tile_the_segment_in_order(self):
        caps = cft.captions_for_segment(10.0, 13.0, "one two three four five six", 3)
        self.assertEqual([c["text"] for c in caps], ["one two three", "four five six"])
        self.assertAlmostEqual(caps[0]["start"], 10.0)
        self.assertAlmostEqual(caps[-1]["end"], 13.0, places=2)
        self.assertLess(caps[0]["end"], caps[1]["start"])

    def test_build_strips_trailing_commas(self):
        caps = cft.build_captions([(0.0, 1.0, "hello there,")], 3)
        self.assertEqual(caps[0]["text"], "hello there")


if __name__ == "__main__":
    unittest.main()
