"""The shared 2D plane kit (`videos/_shared/web/vec/vec.js`): its pure math.

The kit is browser JavaScript; this runs it in node with a stub `ISO` (the
palette and lerp it needs) and checks the parts every beat leans on: the
camera, the grid -> screen map, the row-vector linear map, axis ticks, and
number formatting. Skipped when node is not installed.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KIT = REPO / "videos" / "_shared" / "web" / "vec" / "vec.js"

HARNESS = r"""
const lerp = (a, b, u) => a + (b - a) * u;
const clamp01 = (u) => Math.max(0, Math.min(1, u));
global.window = {};
global.ISO = {
  COL: { tokens: [[45, 212, 191], [96, 165, 250], [224, 176, 64]] },
  css: () => "", mix: (p) => p, lerp, clamp01, W: 1080, H: 1920,
  SAFE: { x0: 65, x1: 950, y0: 230, y1: 1536, stageBottom: 1100 },
};
require(process.argv[1]);
const V = window.VEC, out = {};
const NEAR = { step: 300, ox: 432, oy: 1030, ax: { w: -1.35, e: 1.7, s: -0.45, n: 1.75 } };
const FAR = { step: 160, ox: 240, oy: 1060, ax: { w: -1.3, e: 4.4, s: -1.2, n: 4.5 } };
out.defaultOrigin = V.at(0, 0);
V.view(NEAR); out.nearE1 = V.at(1, 0); out.nearUp = V.at(0, 1);
V.view(NEAR, FAR, 0.5); out.halfStep = V.step(); out.halfAx = Object.assign({}, V.CAM.ax);
V.view(FAR); out.farXW = V.at(2, 4);
const W = [[1, 0.5], [-0.5, 1.25]];
out.xW = V.map([3, 2], W);
out.xHalf = V.map([3, 2], W, 0.5);
out.xId = V.map([3, 2], W, 0);
out.comb = V.comb([1, 2], [[2, -1], [0.5, 1]]);
out.ticks = V.ticks(-1.35, 1.7);
out.ticksInt = V.ticks(-2, 2);
out.fmt = [V.fmtv(-1), V.fmtv(0.5), V.fmtv(4), V.vtxt(4, 0, 2), V.vtxt(-1, 1, 2)];
console.log(JSON.stringify(out));
"""


@unittest.skipUnless(shutil.which("node"), "node not installed")
class VecKitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        res = subprocess.run(["node", "-e", HARNESS, str(KIT)], capture_output=True, text=True, check=True)
        cls.out = json.loads(res.stdout)

    def test_default_camera_is_ep01_canonical(self):
        self.assertEqual(self.out["defaultOrigin"], [507, 780])

    def test_view_maps_grid_to_screen_with_y_up(self):
        self.assertEqual(self.out["nearE1"], [732, 1030])
        self.assertEqual(self.out["nearUp"], [432, 730])
        self.assertEqual(self.out["farXW"], [560, 420])

    def test_view_interpolates_step_and_axes(self):
        self.assertAlmostEqual(self.out["halfStep"], 230)
        self.assertAlmostEqual(self.out["halfAx"]["n"], 3.125)

    def test_map_is_row_vector_x_at_w(self):
        self.assertEqual(self.out["xW"], [2, 4])             # 3·(1, 0.5) + 2·(−0.5, 1.25)
        self.assertEqual(self.out["xId"], [3, 2])            # s = 0 is the identity
        self.assertEqual(self.out["xHalf"], [2.5, 3])        # halfway between the two
        self.assertEqual(self.out["comb"], [3, 1])           # 1·(2, −1) + 2·(0.5, 1)

    def test_ticks_inside_extents_without_zero(self):
        self.assertEqual(self.out["ticks"], [-1, 1])
        self.assertEqual(self.out["ticksInt"], [-1, 1])

    def test_numbers_use_true_minus_and_commas(self):
        self.assertEqual(self.out["fmt"], ["−1", "0.5", "4", "4,", "−1"])


if __name__ == "__main__":
    unittest.main()
