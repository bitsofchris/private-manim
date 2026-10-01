"""Tests for videos/_shared/transformer.py: the pure layout maths and the
diagram/code contract. Builds the diagram (imports Manim), renders nothing.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from videos._shared import style as S  # noqa: E402
from videos._shared import transformer as T  # noqa: E402
from videos._shared.base import _rect, safe_bounds, stage_bounds  # noqa: E402


class StackRows(unittest.TestCase):
    def test_fills_span_with_equal_gaps(self):
        ys = T.stack_rows([1, 1, 1], 0, 5)       # gap = (5 - 3) / 2 = 1
        self.assertEqual(ys, [0.5, 2.5, 4.5])

    def test_rejects_rows_that_do_not_fit(self):
        with self.assertRaises(ValueError):
            T.stack_rows([3, 3], 0, 6)

    def test_single_row_is_centred_at_bottom_edge_plus_half(self):
        self.assertEqual(T.stack_rows([2], 0, 10), [1.0])


class Diagram(unittest.TestCase):
    def setUp(self):
        self.stage = _rect(stage_bounds(safe_bounds()))
        self.d = T.build_block(self.stage)

    def test_parts_exist_in_paper_order(self):
        self.assertEqual([b.name.text for b in self.d.boxes],
                         ["Embed", "Attention", "FFN", "Linear"])
        self.assertEqual(len(self.d.adds), 2)
        self.assertEqual(len(self.d.flow), len(T.ROWS) - 1)
        self.assertEqual(len(self.d.skips), 2)

    def test_flow_is_bottom_to_top(self):
        ys = [self.d.rows[r].get_center()[1] for r in T.ROWS]
        self.assertEqual(ys, sorted(ys))

    def test_everything_stays_inside_the_safe_area(self):
        b = safe_bounds()
        self.assertGreaterEqual(self.d.get_left()[0], b.left - 1e-6)
        self.assertLessEqual(self.d.get_right()[0], b.right + 1e-6)
        stage = stage_bounds(b)
        self.assertGreaterEqual(self.d.get_bottom()[1], stage.bottom - T.BOTTOM_BLEED - 1e-6)
        self.assertLessEqual(self.d.get_top()[1], b.top + 1e-6)

    def test_labels_meet_the_phone_floor(self):
        floor = T.label("X").height * 0.99
        for box in self.d.boxes:
            self.assertGreaterEqual(box.name.height, floor)

    def test_main_line_arrows_are_teal_and_marks_start_dim(self):
        for a in self.d.flow:
            self.assertEqual(a.get_color().to_hex().upper(), S.DATA.upper())
        for box in self.d.boxes:
            self.assertEqual(box.box.get_stroke_color().to_hex().upper(), S.FG_DIM.upper())


class Air(unittest.TestCase):
    def test_row_gaps_are_not_squished(self):
        d = T.build_block(_rect(stage_bounds(safe_bounds())))
        ys = [d.rows[r] for r in T.ROWS]
        gaps = [b.get_bottom()[1] - a.get_top()[1] for a, b in zip(ys, ys[1:])]
        self.assertGreaterEqual(min(gaps), 0.6)


class CodeContract(unittest.TestCase):
    def test_every_mark_points_at_real_lines_with_the_right_token(self):
        lines = T.GPT_SOURCE.splitlines()
        expect = {"box": "self.", "arrow": "x = ", "skip": "x + self.", "add": "x + self.",
                  "repeat": "block", "inset": "class Block"}
        for mark, nums in T.MARK_LINES.items():
            with self.subTest(mark=mark):
                for n in nums:
                    self.assertTrue(1 <= n <= len(lines), f"{mark}: line {n}")
                self.assertTrue(any(expect[mark] in lines[n - 1] for n in nums))

    def test_source_fits_a_short_code_card(self):
        self.assertLessEqual(max(len(l) for l in T.GPT_SOURCE.splitlines()), 40)


if __name__ == "__main__":
    unittest.main()
