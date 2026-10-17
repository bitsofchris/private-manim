"""Unit tests for tools/beat_cuts.py."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import beat_cuts as bc  # noqa: E402

WORDS = [
    {"t": 0.6, "end": 1.0, "word": "An"}, {"t": 1.1, "end": 2.6, "word": "harness."},
    {"t": 3.1, "end": 3.6, "word": " Context"}, {"t": 3.7, "end": 4.9, "word": "goes."},
    {"t": 4.95, "end": 5.4, "word": "Tools,"}, {"t": 5.5, "end": 6.0, "word": "context"},
]


class Cuts(unittest.TestCase):
    def test_cut_is_mid_pause(self):
        self.assertEqual(bc.cut_before(WORDS, 2), 2.85)

    def test_short_pause_keeps_min_lead_before_the_word(self):
        self.assertEqual(bc.cut_before(WORDS, 4), round(4.95 - bc.MIN_LEAD, 3))

    def test_plan_lengths_sum_to_the_vo_and_split_the_vo_text(self):
        rows = bc.plan(WORDS, ["01_a", "02_b=Context", "03_c=tools"], 7.0)
        self.assertAlmostEqual(sum(r["length"] for r in rows), 7.0, places=3)
        self.assertEqual([r["vo"] for r in rows], ["An harness.", "Context goes.", "Tools, context"])

    def test_later_beats_search_after_the_previous_start(self):
        # "context" appears twice; the second beat on it must take the later one.
        rows = bc.plan(WORDS, ["01_a", "02_b=Context", "03_c=context"], 7.0)
        self.assertAlmostEqual(rows[2]["start"], bc.cut_before(WORDS, 5))

    def test_missing_word_or_spec_fails_loudly(self):
        with self.assertRaises(SystemExit):
            bc.plan(WORDS, ["01_a", "02_b=nope"], 7.0)
        with self.assertRaises(SystemExit):
            bc.plan(WORDS, ["01_a", "02_b"], 7.0)

    def test_table_has_one_row_per_beat(self):
        rows = bc.plan(WORDS, ["01_a", "02_b=Context"], 7.0)
        self.assertEqual(len(bc.table(rows).splitlines()), 4)


if __name__ == "__main__":
    unittest.main()
