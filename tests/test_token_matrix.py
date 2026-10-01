"""Tests for the token column / matrix / attention arc mobjects in
videos/_shared/mobjects.py and the 005 layout module. Imports Manim, renders
nothing.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "videos" / "005-transformer-short"))

import numpy as np  # noqa: E402

from videos._shared import style as S  # noqa: E402
from videos._shared.base import _rect, safe_bounds, stage_bounds  # noqa: E402
from videos._shared.mobjects import (  # noqa: E402
    TokenColumn, TokenMatrix, _cell_style, attention_arcs,
)


class CellStyle(unittest.TestCase):
    def test_sign_picks_color_and_magnitude_picks_opacity(self):
        self.assertEqual(_cell_style(0.5)[0], S.DATA)
        self.assertEqual(_cell_style(-0.5)[0], S.SHADOW)
        self.assertAlmostEqual(_cell_style(0.0)[1], S.TOKEN_CELL_OP_MIN)
        self.assertAlmostEqual(_cell_style(1.0)[1], S.TOKEN_CELL_OP_MAX)
        self.assertAlmostEqual(_cell_style(3.0)[1], S.TOKEN_CELL_OP_MAX)  # clamped

    def test_negative_zero_prints_as_plus_zero(self):
        from videos._shared.mobjects import _fmt
        self.assertEqual(_fmt(-0.04), "+0.0")
        self.assertEqual(_fmt(-0.0), "+0.0")
        self.assertEqual(_fmt(-0.06), "-0.1")

    def test_tint_overrides_sign_color(self):
        self.assertEqual(_cell_style(-0.5, S.STRUCTURE)[0], S.STRUCTURE)


class Column(unittest.TestCase):
    def test_shows_d_shown_cells_and_optional_digits(self):
        c = TokenColumn([0.1, -0.2, 0.3, 0.4, 0.5])
        self.assertEqual(len(c.cells), S.TOKEN_D_SHOWN)
        self.assertEqual(len(c.nums), 0)
        self.assertEqual(len(c.dots), 1)
        d = TokenColumn([0.1, -0.2, 0.3], digits=True, dots=False)
        self.assertEqual([t.text for t in d.nums], ["+0.1", "-0.2", "+0.3"])
        self.assertEqual(len(d.dots), 0)

    def test_set_values_keeps_mobjects_and_retargets_them(self):
        c = TokenColumn([0.1, 0.2, 0.3], digits=True)
        cells_before, nums_before = list(c.cells), list(c.nums)
        c.set_values([-0.9, 0.0, 0.5])
        self.assertEqual(list(c.cells), cells_before)
        self.assertEqual(list(c.nums), nums_before)
        self.assertEqual([t.text for t in c.nums], ["-0.9", "+0.0", "+0.5"])
        self.assertAlmostEqual(c.cells[1].get_fill_opacity(), S.TOKEN_CELL_OP_MIN)

    def test_update_column_is_all_magenta(self):
        c = TokenColumn([-0.4, 0.4, 0.0], color=S.STRUCTURE)
        for cell in c.cells:
            self.assertEqual(cell.get_fill_color().to_hex().upper(), S.STRUCTURE.upper())


class Matrix(unittest.TestCase):
    def setUp(self):
        self.vals = np.array([[0.1, 0.2, 0.3], [-0.1, -0.2, -0.3], [0.5, 0.5, 0.5]])

    def test_three_columns_fit_the_short_safe_width(self):
        m = TokenMatrix(self.vals, digits=True)
        self.assertEqual(len(m.columns), 3)
        self.assertEqual(len(m.brackets), 2)
        self.assertLess(m.width, safe_bounds().width)

    def test_unbracketed_has_no_brackets(self):
        self.assertEqual(len(TokenMatrix(self.vals, bracketed=False).brackets), 0)

    def test_set_values_updates_every_column(self):
        m = TokenMatrix(self.vals, digits=True)
        m.set_values(-self.vals)
        self.assertEqual(m.columns[0].nums[0].text, "-0.1")
        self.assertEqual(m.columns[2].nums[2].text, "-0.5")


class Arcs(unittest.TestCase):
    def test_widths_scale_with_weight_and_target_gets_a_loop(self):
        m = TokenMatrix(np.zeros((3, 3)))
        cols = list(m.columns)
        arcs = attention_arcs(cols, cols[2], [1.0, 0.0, 0.5])
        self.assertEqual(len(arcs), 3)
        self.assertAlmostEqual(arcs[0].get_stroke_width(), S.ATTN_ARC_MAX)
        self.assertAlmostEqual(arcs[1].get_stroke_width(), S.ATTN_ARC_MIN)
        # non-self arcs start at the source and end at the target
        np.testing.assert_allclose(arcs[0].get_end()[:2], (cols[2].get_top() + 0.1 * np.array([0, 1, 0]))[:2], atol=1e-6)
        # the self arc is above the target, not crossing it
        self.assertGreater(arcs[2].get_bottom()[1], cols[2].get_top()[1])


class Layout005(unittest.TestCase):
    def test_canonical_matrix_sits_inside_the_stage_with_room_below(self):
        import _tokens as T
        stage = _rect(stage_bounds(safe_bounds()))
        m = T.build_matrix(stage, digits=True)
        words = T.word_labels(m)
        self.assertLessEqual(words.get_top()[1], stage.get_top()[1])
        self.assertGreaterEqual(m.get_left()[0], stage.get_left()[0])
        self.assertLessEqual(m.get_right()[0], stage.get_right()[0])
        # an update column (no dots) fits under the matrix without touching it
        free = m.get_bottom()[1] - stage.get_bottom()[1]
        self.assertGreater(free, S.TOKEN_D_SHOWN * S.TOKEN_CELL_H + 0.5)

    def test_word_labels_share_a_baseline(self):
        import _tokens as T
        stage = _rect(stage_bounds(safe_bounds()))
        words = T.word_labels(T.build_matrix(stage))
        bottoms = {w: t.get_bottom()[1] for w, t in zip(T.TOKENS, words)}
        # "name" and "is" have no descender: their bottoms are the baseline;
        # "my" hangs one descent below it.
        self.assertAlmostEqual(bottoms["name"], bottoms["is"], places=3)
        self.assertAlmostEqual(bottoms["name"] - bottoms["my"], T.descent(), places=3)
        self.assertGreater(T.descent(), 0.05)

    def test_value_stages_are_seeded_and_distinct(self):
        import _tokens as T
        self.assertEqual(len(T.VALUES), 4)
        self.assertFalse(np.array_equal(T.VALUES[0], T.VALUES[1]))
        self.assertTrue(np.array_equal(T.VALUES_AFTER_ATTN[T.TARGET], T.VALUES[1][T.TARGET]))
        self.assertTrue(np.array_equal(T.VALUES_AFTER_ATTN[0], T.VALUES[0][0]))
