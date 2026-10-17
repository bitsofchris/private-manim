"""Tests for tools/hf_state_check.js on a tiny seam-state kit. Needs node.

Run: uv run --no-sync python -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "hf_state_check.js"

KIT = """
window.SC = {
  REST: { a: 0, card: { o: 0 } },
  SEAM: { 1: { a: 0 }, 2: { a: 1, card: { o: 1, text: "hi" } } },
  mount(root) { const e = document.createElement("div"); root.appendChild(e); return { draw(g, S) { e.textContent = String(S.a); } }; },
};
"""

BEAT = """<!doctype html><html><head><script src="kit/k.js"></script></head><body>
<div id="root" data-duration="2"><canvas id="scene"></canvas></div>
<script>
(() => {
  const g = document.getElementById("scene").getContext("2d"), K = SC.mount(document.getElementById("root"));
  const END = %s;
  function S(t) { const u = Math.min(1, t / 1.5); return { a: u * END, card: { o: u, text: u > 0 ? "hi" : "" } }; }
  const tl = gsap.timeline({ paused: true, onUpdate: () => K.draw(g, S(tl.time())) });
  window.__timelines = window.__timelines || {}; window.__timelines["main"] = tl;
  tl.seek(0);
})();
</script></body></html>"""


@unittest.skipUnless(shutil.which("node"), "node not installed")
class StateCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name) / "01_beat"
        (self.dir / "kit").mkdir(parents=True)
        (self.dir / "kit" / "k.js").write_text(KIT)

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, end: str):
        (self.dir / "index.html").write_text(BEAT % end)
        return subprocess.run(["node", str(TOOL), str(self.dir), "1", "2"], capture_output=True, text=True)

    def test_a_beat_that_meets_both_seams_passes(self):
        r = self.run_tool("1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout.count("ok "), 3)

    def test_a_beat_that_ends_off_its_seam_fails_and_names_the_field(self):
        r = self.run_tool("0.5")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)   # S(end) and S(end - 0.3)
        self.assertIn("a: beat 0.5 vs seam 1", r.stdout)

    def test_hidden_parts_are_not_compared(self):
        node = ("const {diff} = require(%s);"
                "console.log(JSON.stringify(diff({card: {o: 0, text: 'x'}}, {}, 1e-6)))") % json.dumps(str(TOOL))
        out = subprocess.run(["node", "-e", node], capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out), [])


if __name__ == "__main__":
    unittest.main()
