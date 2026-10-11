"""Pure-logic tests for tools/word_times.py. No audio.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import word_times as WT  # noqa: E402


class Syllables(unittest.TestCase):
    def test_counts_vowel_groups(self):
        self.assertEqual(WT.syllables("a"), 1)
        self.assertEqual(WT.syllables("collapsing"), 3)
        # an estimate: only the order matters (the weights split a span)
        self.assertGreater(WT.syllables("amplifying"), WT.syllables("map"))

    def test_silent_e_and_digits(self):
        self.assertEqual(WT.syllables("same"), 1)
        self.assertEqual(WT.syllables("e1"), 2)          # "e one"
        self.assertEqual(WT.syllables("lands."), 1)      # punctuation ignored


class SplitSpan(unittest.TestCase):
    def test_longer_words_get_more_time(self):
        starts = WT.split_span(["a", "collapsing", "map"], 0.0, 3.0)
        self.assertEqual(starts[0], 0.0)
        self.assertGreater(starts[2] - starts[1], starts[1] - starts[0])

    def test_starts_are_in_order_inside_the_span(self):
        starts = WT.split_span(["one", "two", "three", "four"], 1.0, 2.0)
        self.assertEqual(starts, sorted(starts))
        self.assertTrue(all(1.0 <= s < 2.0 for s in starts))


class Place(unittest.TestCase):
    # a flat envelope at -10 dB with quiet dips at frames 30 and 70 (0.30 s and 0.70 s)
    ENV = [-10.0] * 100
    ENV[30] = -40.0
    ENV[70] = -40.0

    def test_dips_are_local_minima(self):
        self.assertEqual(WT.dips(self.ENV)[:1], [1])     # the flat run counts as minima too
        self.assertIn(30, WT.dips(self.ENV))

    def test_boundaries_move_to_nearby_dips(self):
        out = WT.place([0.0, 0.25, 0.75], self.ENV, 0.0)
        self.assertAlmostEqual(out[1], 0.30)
        self.assertAlmostEqual(out[2], 0.70)

    def test_two_boundaries_never_share_a_dip(self):
        # both guesses sit near the single deep dip at 0.30; only one may take it
        env = [-10.0] * 100
        env[30] = -40.0
        out = WT.place([0.0, 0.27, 0.33], env, 0.0)
        self.assertGreaterEqual(out[2] - out[1], WT.MIN_WORD - 1e-9)
        self.assertEqual(out, sorted(out))

    def test_first_start_is_kept_and_single_word_untouched(self):
        self.assertEqual(WT.place([0.12], self.ENV, 0.0), [0.12])
        self.assertEqual(WT.place([0.05, 0.25], self.ENV, 0.0)[0], 0.05)


class RecognizerWords(unittest.TestCase):
    def test_word_timed_segments_pass_through_without_audio(self):
        segs = [{"start": 0.5, "end": 1.5, "text": "A matrix", "words": [(0.58, 0.7, "A"), (0.72, 1.2, "matrix")]}]
        self.assertEqual(WT.word_times(segs, None, 0), [
            {"t": 0.58, "end": 0.7, "word": "A", "seg": 0}, {"t": 0.72, "end": 1.2, "word": "matrix", "seg": 0}])

    def test_a_start_in_silence_moves_to_the_speech(self):
        env = [-60.0] * 50 + [-10.0] * 50                 # silence, then speech from 0.50 s
        self.assertAlmostEqual(WT.out_of_silence(0.0, env, 0.0, -40.0), 0.50)
        self.assertEqual(WT.out_of_silence(0.70, env, 0.0, -40.0), 0.70)   # already in speech


if __name__ == "__main__":
    unittest.main()
