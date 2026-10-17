"""Unit tests for tools/vo_floor.py's pure logic (no ffmpeg needed)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import vo_floor as vf  # noqa: E402


def tone(seconds: float, rms_db: float, sr: int = vf.SR) -> np.ndarray:
    """A sine whose RMS level is rms_db."""
    t = np.arange(int(seconds * sr)) / sr
    return (np.sqrt(2) * 10 ** (rms_db / 20) * np.sin(2 * np.pi * 220 * t)).astype(np.float32)


class NoiseFloor(unittest.TestCase):
    def test_floor_is_the_room_not_the_voice(self):
        # 70 % "voice" at -20 dB, 30 % "room" at -55 dB: the 10th percentile is the room
        x = np.concatenate([tone(3.5, -20), tone(1.5, -55)])
        self.assertAlmostEqual(vf.noise_floor_db(x), -55, delta=0.5)

    def test_digital_silence_is_ignored(self):
        x = np.concatenate([tone(2.0, -20), np.zeros(vf.SR * 2, np.float32), tone(1.0, -50)])
        self.assertAlmostEqual(vf.noise_floor_db(x), -50, delta=0.5)

    def test_all_silence_raises(self):
        with self.assertRaises(ValueError):
            vf.noise_floor_db(np.zeros(vf.SR, np.float32))


if __name__ == "__main__":
    unittest.main()
