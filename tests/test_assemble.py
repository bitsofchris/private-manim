"""Pure-logic tests for tools/assemble.py. No media, no ffmpeg, no Manim.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import assemble as A  # noqa: E402

BASE = Path("/proj/videos/demo")


def beats(*spans):
    return [A.Beat(BASE / f"b{i}.mp4", s, e) for i, (s, e) in enumerate(spans)]


class ParseBeats(unittest.TestCase):
    def test_resolves_paths_and_defaults_start(self):
        out = A.parse_beats({"beats": [{"clip": "media/a.mp4", "end": 4}]}, BASE)
        self.assertEqual(out, [A.Beat(BASE / "media/a.mp4", 0.0, 4.0)])

    def test_total_duration_sums_trimmed_spans(self):
        self.assertAlmostEqual(A.total_duration(beats((0, 4), (1, 8))), 11.0)

    def test_rejects_bad_shapes(self):
        for bad in [[], {}, {"beats": []}, {"beats": [{"clip": "a.mp4"}]},
                    {"beats": [{"clip": "a.mp4", "start": 3, "end": 2}]},
                    {"beats": [{"clip": "a.mp4", "start": -1, "end": 2}]}]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                A.parse_beats(bad, BASE)


class ParseCaptions(unittest.TestCase):
    def test_ok(self):
        caps = A.parse_captions([{"start": 0, "end": 1.2, "text": " neural network "},
                                 {"start": 1.2, "end": 2, "text": "just a function"}], total=4)
        self.assertEqual(caps[0], A.Caption(0.0, 1.2, "neural network"))
        self.assertEqual(len(caps), 2)

    def test_rejects(self):
        cases = {
            "overlap": [{"start": 0, "end": 2, "text": "a"}, {"start": 1, "end": 3, "text": "b"}],
            "empty": [{"start": 0, "end": 1, "text": "  "}],
            "too long": [{"start": 0, "end": 1, "text": "one two three four five"}],
            "reversed": [{"start": 2, "end": 1, "text": "a"}],
            "past end": [{"start": 3, "end": 5, "text": "a"}],
            "not a list": {"start": 0},
        }
        for name, data in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                A.parse_captions(data, total=4)


class FfmpegCommand(unittest.TestCase):
    def test_inputs_in_order_beats_vo_pngs(self):
        caps = [A.Caption(0, 1, "a"), A.Caption(1, 2, "b")]
        pngs = [Path("/t/c0.png"), Path("/t/c1.png")]
        cmd = A.build_ffmpeg_cmd(beats((0, 4), (0, 7)), Path("/o.mp4"), Path("/vo.m4a"), caps, pngs)
        inputs = [cmd[i + 1] for i, x in enumerate(cmd) if x == "-i"]
        self.assertEqual(inputs, [str(BASE / "b0.mp4"), str(BASE / "b1.mp4"), "/vo.m4a",
                                  "/t/c0.png", "/t/c1.png"])
        self.assertIn("2:a", cmd)                  # VO is input 2
        self.assertEqual(cmd[cmd.index("-t") + 1], "11")
        self.assertEqual(cmd[-1], "/o.mp4")

    def test_filter_trims_concats_and_overlays(self):
        f = A.build_filter(beats((0.5, 4), (0, 7)), [A.Caption(0, 1.25, "a")], first_png_input=3)
        self.assertIn("[0:v]trim=start=0.5:end=4,setpts=PTS-STARTPTS,fps=30,scale=1080:1920", f)
        self.assertIn("[v0][v1]concat=n=2:v=1:a=0[base]", f)
        self.assertIn("[base][3:v]overlay=0:0:enable='between(t,0,1.25)'[c0]", f)
        self.assertTrue(f.endswith("[c0]format=yuv420p[vout]"))

    def test_no_vo_no_captions(self):
        cmd = A.build_ffmpeg_cmd(beats((0, 4)), Path("/o.mp4"))
        self.assertIn("-an", cmd)
        self.assertNotIn("-c:a", cmd)
        f = cmd[cmd.index("-filter_complex") + 1]
        self.assertIn("[base]format=yuv420p[vout]", f)

    def test_png_count_must_match(self):
        with self.assertRaises(ValueError):
            A.build_ffmpeg_cmd(beats((0, 4)), Path("/o.mp4"), captions=[A.Caption(0, 1, "a")])

    def test_num_formatting(self):
        self.assertEqual([A._num(x) for x in (0, 4.0, 1.25, 0.00001, 2.3456)],
                         ["0", "4", "1.25", "0", "2.346"])


if __name__ == "__main__":
    unittest.main()
