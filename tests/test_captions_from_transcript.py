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


class MacWhisperJson(unittest.TestCase):
    DOC = (
        '{"segments": ['
        '{"start": 580, "end": 3400, "text": " A matrix just records where",'
        ' "words": [{"start": 580, "end": 700, "text": " A"}, {"start": 720, "end": 1200, "text": "matrix"},'
        ' {"start": 1210, "end": 1350, "text": "just"}, {"start": 1360, "end": 1840, "text": "records"},'
        ' {"start": 1850, "end": 2080, "text": "where"}]},'
        '{"start": 3400, "end": 5000, "text": "Every weight matrix"}'
        '], "text": "..."}'
    )

    def test_parses_seconds_and_words(self):
        segs = cft.parse_mw_json(self.DOC)
        self.assertEqual(segs[0]["start"], 0.58)
        self.assertEqual(segs[0]["words"][1], (0.72, 1.2, "matrix"))
        self.assertEqual(segs[1]["words"], [])

    def test_word_timed_captions_start_on_their_first_word(self):
        caps = cft.build_captions(cft.parse_mw_json(self.DOC), 3, max_chars=30)
        self.assertEqual([c["text"] for c in caps[:2]], ["A matrix just", "records where"])
        self.assertEqual(caps[0]["start"], 0.58)
        self.assertEqual(caps[1]["start"], 1.36)
        self.assertAlmostEqual(caps[0]["end"], 1.36 - cft.GAP)
        self.assertEqual(caps[1]["end"], 2.08)

    def test_words_json_round_trips_into_segments(self):
        words = [{"t": 0.58, "end": 0.7, "word": "A", "seg": 0}, {"t": 0.72, "end": 1.2, "word": "matrix", "seg": 0},
                 {"t": 3.4, "end": 3.7, "word": "Every", "seg": 1}]
        segs = cft.segments_from_words(words)
        self.assertEqual([s["text"] for s in segs], ["A matrix", "Every"])
        self.assertEqual(cft.build_captions(segs, 3)[0]["start"], 0.58)

    def test_segment_without_words_falls_back_to_proportional(self):
        caps = cft.build_captions(cft.parse_mw_json(self.DOC), 3, max_chars=30)
        self.assertEqual(caps[-1]["text"], "Every weight matrix")
        self.assertEqual(caps[-1]["start"], 3.4)


def _w(t, word, seg=0):
    return {"t": t, "end": t + 0.2, "word": word, "seg": seg}


class SentencesAndSegments(unittest.TestCase):
    def test_caption_never_crosses_a_sentence_end(self):
        # 012 ep01: the recognizer put "...last error." and "Tools are..." in one segment.
        words = [_w(0.0, "the"), _w(0.3, "last"), _w(0.6, "error."), _w(1.0, "Tools"), _w(1.3, "are"), _w(1.6, "what")]
        caps = cft.build_captions(cft.segments_from_words(words), 3)
        self.assertEqual([c["text"] for c in caps], ["the last error.", "Tools are what"])

    def test_dotted_names_and_decimals_do_not_end_a_sentence(self):
        words = [_w(0.0, "like"), _w(0.3, "an"), _w(0.6, "AGENTS.md,"), _w(1.0, "at"), _w(1.3, "0.70"), _w(1.6, "now")]
        sents = cft.sentences([(w["t"], w["end"], w["word"]) for w in words])
        self.assertEqual(len(sents), 1)

    def test_question_and_quote_end_a_sentence(self):
        sents = cft.sentences([(0, 0.1, "why?"), (0.2, 0.3, 'said "go."'), (0.4, 0.5, "ok")])
        self.assertEqual([len(s) for s in sents], [1, 1, 1])

    def test_segments_follow_file_order_not_index_order(self):
        # A hand-split segment numbered 100 stays where it is in the file.
        words = [_w(0.0, "one.", 3), _w(1.0, "two", 100), _w(2.0, "three", 4)]
        segs = cft.segments_from_words(words)
        self.assertEqual([s["text"] for s in segs], ["one.", "two", "three"])
        caps = cft.build_captions(segs, 3)
        self.assertEqual([c["start"] for c in caps], sorted(c["start"] for c in caps))



class MaxChars(unittest.TestCase):
    """013: a caption over ~15 characters wraps and climbs into the stage."""

    def test_long_group_splits_at_balanced_break(self):
        self.assertEqual(cft.chunk_words(["predicted", "attack,", "but"], 3, 15), [["predicted"], ["attack,", "but"]])

    def test_short_group_untouched(self):
        self.assertEqual(cft.chunk_words(["50", "are", "attacks."], 3, 15), [["50", "are", "attacks."]])

    def test_single_long_word_stays_whole(self):
        self.assertEqual(cft.fit_chars(["supercalifragilistic"], 15), [["supercalifragilistic"]])

    def test_every_caption_fits(self):
        words = [(i * 0.3, i * 0.3 + 0.25, w) for i, w in enumerate("We want to look at the confusion matrix.".split())]
        caps = cft.captions_for_words(words, 3, 15)
        self.assertTrue(all(len(c["text"]) <= 15 for c in caps), caps)


if __name__ == "__main__":
    unittest.main()
