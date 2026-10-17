"""Unit tests for tools/fix_words.py."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import fix_words as fw  # noqa: E402


def W(*specs):
    """W((t, word, seg), ...) -> words.json rows."""
    return [{"t": t, "end": t + 0.2, "word": w, "seg": s} for t, w, s in specs]


class Ops(unittest.TestCase):
    def test_join_merges_consecutive_words_and_keeps_times(self):
        words = W((1.0, " like", 0), (1.2, " agent's", 0), (1.5, " MD,", 0), (1.9, " they're", 0))
        self.assertEqual(fw.join(words, "agent's MD,", "AGENTS.md,"), 1)
        self.assertEqual([w["word"] for w in words], [" like", " AGENTS.md,", " they're"])
        self.assertEqual((words[1]["t"], words[1]["end"]), (1.2, 1.7))

    def test_sub_replaces_every_match_or_the_nearest_with_at(self):
        words = W((1.0, "the", 0), (5.0, "the", 0), (9.0, "the", 0))
        self.assertEqual(fw.sub(words, "the@5.4", "THE"), 1)
        self.assertEqual([w["word"] for w in words], ["the", "THE", "the"])
        self.assertEqual(fw.sub(words, "the", "a"), 2)

    def test_sub_new_text_may_contain_spaces(self):
        words = W((0.9, " harnesses", 0))
        fw.sub(words, "harnesses", "harness is")
        self.assertEqual(words[0]["word"], " harness is")

    def test_break_after_starts_a_new_segment_and_renumber_keeps_order(self):
        words = W((0, "error.", 3), (1, "Tools", 3), (2, "are", 3), (3, "Read", 4))
        self.assertEqual(fw.break_after(words, "error."), 1)
        fw.renumber(words)
        self.assertEqual([w["seg"] for w in words], [0, 1, 1, 2])

    def test_at_suffix_only_when_numeric(self):
        self.assertEqual(fw._target("me@home"), ("me@home", None))
        self.assertEqual(fw._target("error,@10.8"), ("error,", 10.8))


class Cli(unittest.TestCase):
    def test_main_writes_in_place_and_flags_no_match(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "words.json"
            p.write_text(json.dumps(W((0, "harnesses", 0), (1, "is", 0))))
            self.assertEqual(fw.main([str(p), "--sub", "harnesses", "harness"]), 0)
            self.assertEqual(json.loads(p.read_text())[0]["word"], "harness")
            self.assertEqual(fw.main([str(p), "--sub", "nothing", "x"]), 1)


if __name__ == "__main__":
    unittest.main()
