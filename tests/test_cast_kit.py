"""The shared cast kit (`videos/_shared/web/cast/cast.js`): its geometry and state.

The kit is browser JavaScript that builds SVG; this runs it in node with a
minimal fake DOM and checks what beats lean on: limb angles, where a posed
hand ends up in the frame, the agent's 1 and 0 eyes and blink, the janitor's
broom reaching the floor, and hero() swapping a part to magenta and back.
Skipped when node is not installed.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KIT = REPO / "videos" / "_shared" / "web" / "cast" / "cast.js"

HARNESS = r"""
function El(tag) {
  this.tagName = tag; this.attrs = {}; this.children = []; this.style = {}; this.textContent = "";
}
El.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
El.prototype.getAttribute = function (k) { return k in this.attrs ? this.attrs[k] : null; };
El.prototype.appendChild = function (c) { this.children.push(c); return c; };
El.prototype.insertBefore = function (c, ref) {
  const i = this.children.indexOf(ref); this.children.splice(i < 0 ? 0 : i, 0, c); return c;
};
El.prototype.querySelectorAll = function () {
  const out = [];
  (function walk(n) { n.children.forEach((c) => { if ("data-tint" in c.attrs) out.push(c); walk(c); }); })(this);
  return out;
};
Object.defineProperty(El.prototype, "firstChild", { get() { return this.children[0]; } });
global.window = {};
global.document = { createElementNS: (ns, tag) => new El(tag) };
require(process.argv[1]);
const C = window.CAST, out = {};
const root = new El("div"), svg = C.layer(root);
out.limbDown = C.limb(0, 0, 100, 0, 1);
out.limbOut = C.limb(0, 0, 100, 90, 1).map(Math.round);
out.limbLeft = C.limb(0, 0, 100, 90, -1).map(Math.round);
const h = C.human(svg, { x: 200, y: 700, s: 0.5 });
C.pose(h, { armR: 90 });
out.handR = C.hand(h, 1).map((v) => Math.round(v * 10) / 10);
out.transform = h.el.getAttribute("transform");
const a = C.agent(svg, {});
out.eyes = a.face.eyes.map((t) => t.textContent);
out.eyeFont = a.face.eyes[0].style.fontFamily;
C.blink(a, 1); out.blinked = a.face.eyes.map((t) => t.textContent);
C.blink(a, 0); out.open = a.face.eyes.map((t) => t.textContent);
const j = C.janitor(svg, {});
out.broomFoot = j.broom.foot;
C.pose(j, { armR: 40 }); out.broomFootPosed = j.broom.foot;
const p = C.page(svg, {});
const rect = p.el.children[0];
C.hero(p, true); out.heroOn = rect.getAttribute("stroke");
C.hero(p, false); out.heroOff = rect.getAttribute("stroke");
const b = C.blob(svg, {});
C.hero(b.pipes[0], true);
out.pipes = b.pipes.map((l) => l.getAttribute("stroke"));
out.bodyRest = b.body.getAttribute("stroke");
C.hero(b.body, true); out.bodyHero = b.body.getAttribute("stroke");
out.pipeNames = C.PIPES;
console.log(JSON.stringify(out));
"""


@unittest.skipUnless(shutil.which("node"), "node not installed")
class CastKitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        res = subprocess.run(["node", "-e", HARNESS, str(KIT)], capture_output=True, text=True, check=True)
        cls.out = json.loads(res.stdout)

    def test_limb_angle_is_from_straight_down(self):
        self.assertEqual(self.out["limbDown"], [0, 100])
        self.assertEqual(self.out["limbOut"], [100, 0])
        self.assertEqual(self.out["limbLeft"], [-100, 0])

    def test_hand_lands_in_frame_coordinates(self):
        # shoulder at (0, -345), arm 155 straight out to the right, then
        # scaled by 0.5 about the feet at (200, 700)
        self.assertEqual(self.out["handR"], [277.5, 527.5])
        self.assertEqual(self.out["transform"], "translate(200 700) rotate(0) scale(0.5)")

    def test_agent_has_one_and_zero_eyes_in_monospace(self):
        self.assertEqual(self.out["eyes"], ["1", "0"])
        self.assertEqual(self.out["eyeFont"], "monospace")
        self.assertEqual(self.out["blinked"], ["-", "-"])
        self.assertEqual(self.out["open"], ["1", "0"])

    def test_janitor_broom_stays_on_the_floor(self):
        self.assertEqual(self.out["broomFoot"][1], 0)
        self.assertEqual(self.out["broomFootPosed"][1], 0)

    def test_hero_swaps_to_magenta_and_back(self):
        self.assertEqual(self.out["heroOn"], "#C084FC")
        self.assertEqual(self.out["heroOff"], "#2DD4BF")

    def test_blob_pipes_in_harness_order_one_hero(self):
        self.assertEqual(self.out["pipeNames"], ["context", "tools", "memory", "loop"])
        self.assertEqual(self.out["pipes"], ["#C084FC", "#2DD4BF", "#2DD4BF", "#2DD4BF"])

    def test_blob_body_rests_dim_and_can_be_the_hero(self):
        # A shared part is never magenta at rest (agents/style.md, two-hero rule; 012 ep01).
        self.assertEqual(self.out["bodyRest"], "#8A8FB0")
        self.assertEqual(self.out["bodyHero"], "#C084FC")


if __name__ == "__main__":
    unittest.main()
