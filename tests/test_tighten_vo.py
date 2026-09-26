"""Unit tests for the pure planning logic in tools/tighten_vo.py (no ffmpeg needed)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import tighten_vo as tv  # noqa: E402


class SpeechIntervals(unittest.TestCase):
    def test_complement_of_silences(self):
        speech = tv.speech_intervals([(0.0, 1.0), (3.0, 4.0)], total=6.0)
        self.assertEqual(speech, [(1.0, 3.0), (4.0, 6.0)])

    def test_no_silence_is_one_interval(self):
        self.assertEqual(tv.speech_intervals([], total=2.0), [(0.0, 2.0)])


class Removals(unittest.TestCase):
    def test_drop_whole_interval(self):
        out = tv.apply_removals([(1.0, 2.0), (3.0, 4.0)], [(2.9, 4.1)])
        self.assertEqual(out, [(1.0, 2.0)])

    def test_clip_partial_overlap(self):
        out = tv.apply_removals([(1.0, 4.0)], [(2.0, 3.0)])
        self.assertEqual(out, [(1.0, 2.0), (3.0, 4.0)])


class PlanCuts(unittest.TestCase):
    def test_gaps_are_capped_and_pieces_padded(self):
        pieces = tv.plan_cuts([(1.0, 2.0), (5.0, 6.0)], max_gap=0.4, total=10.0)
        self.assertEqual(len(pieces), 2)
        first, second = pieces
        self.assertAlmostEqual(first.old_start, 1.0 - tv.PAD)
        self.assertAlmostEqual(first.old_end, 2.0 + tv.PAD)
        self.assertAlmostEqual(first.new_start, tv.LEAD_IN)
        # 3 s pause between them collapses to max_gap
        self.assertAlmostEqual(second.new_start - first.new_end, 0.4, places=3)

    def test_short_gap_is_kept_as_is(self):
        pieces = tv.plan_cuts([(1.0, 2.0), (2.3, 3.0)], max_gap=0.4, total=10.0)
        a, b = pieces
        # after padding, the pieces touch at 2.08/2.22 -> gap 0.14
        self.assertAlmostEqual(b.new_start - a.new_end, 0.14, places=3)

    def test_pause_override_at_beat_boundary(self):
        pieces = tv.plan_cuts([(1.0, 2.0), (5.0, 6.0)], max_gap=0.4, total=10.0, pauses={3.5: 0.45})
        a, b = pieces
        self.assertAlmostEqual(b.new_start - a.new_end, 0.45, places=3)

    def test_pause_override_ignores_other_gaps(self):
        pieces = tv.plan_cuts([(1.0, 2.0), (5.0, 6.0)], max_gap=0.4, total=10.0, pauses={8.0: 0.45})
        a, b = pieces
        self.assertAlmostEqual(b.new_start - a.new_end, 0.4, places=3)

    def test_pieces_never_overlap(self):
        pieces = tv.plan_cuts([(1.0, 2.0), (2.05, 3.0)], max_gap=0.4, total=10.0)
        a, b = pieces
        self.assertGreaterEqual(b.old_start, a.old_end)


class Remap(unittest.TestCase):
    def setUp(self):
        self.pieces = tv.plan_cuts([(1.0, 2.0), (5.0, 6.0)], max_gap=0.4, total=10.0)

    def test_inside_piece(self):
        t = tv.remap(1.5, self.pieces)
        self.assertAlmostEqual(t, tv.LEAD_IN + 0.5 + tv.PAD, places=3)

    def test_inside_removed_pause_snaps_forward(self):
        self.assertAlmostEqual(tv.remap(3.5, self.pieces), self.pieces[1].new_start, places=3)

    def test_after_everything_is_none(self):
        self.assertIsNone(tv.remap(9.0, self.pieces))


class FfmpegCommand(unittest.TestCase):
    def test_command_shape(self):
        pieces = tv.plan_cuts([(1.0, 2.0)], max_gap=0.4, total=10.0)
        cmd = tv.build_ffmpeg("in.wav", pieces, "out.wav")
        self.assertEqual(cmd[0], "ffmpeg")
        self.assertIn("-filter_complex", cmd)
        graph = cmd[cmd.index("-filter_complex") + 1]
        self.assertIn("atrim=start=0.920:end=2.080", graph)
        self.assertIn("concat=n=1:v=0:a=1[out]", graph)
        self.assertEqual(cmd[-1], "out.wav")


if __name__ == "__main__":
    unittest.main()
