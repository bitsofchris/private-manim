"""Pure-logic tests for tools/seam_check.py. No snapshots, no node.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import seam_check as SC  # noqa: E402


class Pairs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        for name in ("01_hook", "02_sends", "04_last"):
            (self.base / name).mkdir()
            (self.base / name / "index.html").write_text('<div data-duration="2.5">')

    def tearDown(self):
        self.tmp.cleanup()

    def test_pairs_neighbouring_hyperframes_beats(self):
        beats = {"beats": [{"clip": "media/hf/01_hook.mp4", "end": 1}, {"clip": "media/hf/02_sends.mp4", "end": 1}]}
        self.assertEqual(SC.hf_pairs(beats, self.base), [("01_hook", "02_sends")])

    def test_skips_cuts_touching_a_manim_beat_or_a_missing_folder(self):
        beats = {"beats": [
            {"clip": "media/hf/01_hook.mp4", "end": 1},
            {"clip": "media/videos/03_m/1920p30/M.mp4", "end": 1},
            {"clip": "media/hf/04_last.mp4", "end": 1},
            {"clip": "media/hf/05_gone.mp4", "end": 1},
        ]}
        self.assertEqual(SC.hf_pairs(beats, self.base), [])


class Duration(unittest.TestCase):
    def test_reads_root_duration(self):
        self.assertEqual(SC.duration('<div id="root" data-duration="4.147" data-fps="30">'), 4.147)

    def test_missing_duration_raises(self):
        with self.assertRaises(ValueError):
            SC.duration("<div>")


class Verdict(unittest.TestCase):
    def test_tolerance_is_inclusive(self):
        self.assertEqual(SC.verdict(8, 8), "ok")
        self.assertEqual(SC.verdict(9, 8), "DIFF")



class Touching(unittest.TestCase):
    PAIRS = [("01_a", "02_b"), ("02_b", "03_c"), ("03_c", "04_d")]

    def test_no_beats_keeps_every_cut(self):
        self.assertEqual(SC.touching(self.PAIRS, []), self.PAIRS)

    def test_a_beat_keeps_its_cut_in_and_out(self):
        self.assertEqual(SC.touching(self.PAIRS, ["02_b"]), [("01_a", "02_b"), ("02_b", "03_c")])

    def test_first_beat_has_only_a_cut_out(self):
        self.assertEqual(SC.touching(self.PAIRS, ["01_a"]), [("01_a", "02_b")])


class Mask(unittest.TestCase):
    def test_parses_a_box(self):
        self.assertEqual(SC.parse_box("431,402,583,492"), (431, 402, 583, 492))

    def test_empty_box_raises(self):
        with self.assertRaises(ValueError):
            SC.parse_box("500,400,500,490")


if __name__ == "__main__":
    unittest.main()
