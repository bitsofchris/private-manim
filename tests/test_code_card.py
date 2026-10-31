"""The shared HyperFrames code card (`videos/_shared/web/code/code.js`).

The card is browser JavaScript; this runs it in node with a stub DOM and
checks the Dark+ tokenizer, the typist's timing (pinned to 014's original
numbers, so a shipped beat's typing does not move), and the two placements:
STAGE (014, fixed type) and DOCK (016, type shrinks to fit the longest line).
Skipped when node is not installed.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KIT = REPO / "videos" / "_shared" / "web" / "code" / "code.js"

HARNESS = r"""
function el() {
  return { style: {}, children: [], attrs: {}, textContent: "",
    appendChild(c) { this.children.push(c); return c; }, setAttribute(k, v) { this.attrs[k] = v; } };
}
global.window = {};
global.document = { createElement: el };
require(process.argv[1]);
const K = window.CODE, out = {};
out.aliases = [window.SC_makeCode === K.make, window.SC_typedAt === K.typedAt, window.SC_typingSeconds === K.typingSeconds];
const colour = (t) => K.tokenize(t).filter((x) => x.c).map((x) => [x.s, x.c]);
out.tokFor = colour("for batch in loader:");
out.tokCall = colour("loss = model(x, 0.5)");
out.tokClass = colour("class Shards(IterableDataset):");
out.tokStr = colour("print('hi')  # done");
out.tokAgain = colour("for batch in loader:");          // same answer twice: no regex state leaks

const L = [{ t: "for batch in loader:" }, { t: "    loss = model(batch)" }];
const total = L[0].t.length + L[1].t.length;
out.at = [0.1, 0.5, 1.0, 1.5, 2.0].map((s) => K.typedAt(L, s));
out.at30 = K.typedAt(L, 0.5, 30);
out.atNeg = K.typedAt(L, -1);
out.atEnd = K.typedAt(L, 99);
out.total = total;
out.secs = K.typingSeconds(L);
out.atSecs = K.typedAt(L, out.secs);
out.atJustBefore = K.typedAt(L, out.secs - 0.01);
out.monotonic = [...Array(100)].map((_, i) => K.typedAt(L, i * 0.03)).every((n, i, a) => i === 0 || n >= a[i - 1]);
// the line break is a pause: the first line lands, then nothing for at least 2.5 / cps − one character
const end0 = K.typingSeconds([L[0]]);
out.pause = [K.typedAt(L, end0 + 0.001), K.typedAt(L, end0 + 2.5 / 22 - 1.55 / 22)];
out.len0 = L[0].t.length;

const stage = K.make(el(), K.STAGE);
stage.set({ o: 1, lines: L, typed: Infinity, lit: null });
out.stage = { size: stage.rows[0].style.fontSize, pitch: stage.rows[1].style.top, top: stage.card.style.top, h: stage.card.style.height,
              n: stage.rows.length, border: stage.rows[0].style.cssText.includes("border-left:8px") };
stage.rows.forEach((r) => { r.style.fontSize = "46px"; });     // 014 ep04 restyles the rows once
stage.set({ o: 1, lines: L, typed: 10 });
out.stageKeeps = stage.rows[0].style.fontSize;

const dock = K.make(el(), K.DOCK);
const long = [{ t: "x".repeat(50), lit: "a" }, { t: "# a comment" }];
dock.set({ o: 1, lines: long, lit: "a" });
out.dock = { size: dock.rows[0].style.fontSize, pitch: dock.rows[0].style.lineHeight, top: dock.card.style.top, h: dock.card.style.height,
             n: dock.rows.length, hero: dock.rows[0].style.color, comment: dock.rows[1].style.color };
dock.set({ o: 1, lines: [{ t: "short" }], cy: 1000 });
out.dockShort = { size: dock.rows[0].style.fontSize, top: dock.card.style.top };
const moved = K.make(el(), Object.assign({}, K.STAGE, { cy: 900 }));
moved.set({ o: 1, lines: L });
out.moved = moved.card.style.top;
console.log(JSON.stringify(out));
"""


@unittest.skipUnless(shutil.which("node"), "node not installed")
class CodeCardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        res = subprocess.run(["node", "-e", HARNESS, str(KIT)], capture_output=True, text=True, check=True)
        cls.out = json.loads(res.stdout)

    def test_old_globals_alias_the_new_api(self):
        self.assertEqual(self.out["aliases"], [True, True, True])

    def test_tokenizer_colours_keywords_names_and_punctuation(self):
        self.assertEqual(self.out["tokFor"], [["for", "#569CD6"], ["batch", "#9CDCFE"], ["in", "#569CD6"],
                                             ["loader", "#9CDCFE"], [":", "#D4D4D4"]])
        self.assertEqual(self.out["tokAgain"], self.out["tokFor"])

    def test_tokenizer_calls_numbers_classes_strings_comments(self):
        call = dict(self.out["tokCall"])
        self.assertEqual(call["model"], "#DCDCAA")
        self.assertEqual(call["0.5"], "#B5CEA8")
        cls = dict(self.out["tokClass"])
        self.assertEqual(cls["Shards"], "#4EC9B0")            # the name after `class`
        self.assertEqual(cls["IterableDataset"], "#4EC9B0")   # capitalised
        s = dict(self.out["tokStr"])
        self.assertEqual(s["'hi'"], "#CE9178")
        self.assertEqual(s["# done"], "#6A9955")

    def test_typing_matches_014_original(self):
        # values from 014's kit/code.js before the promotion (2026-10-31)
        self.assertEqual(self.out["at"], [2, 11, 20, 32, 43])
        self.assertEqual(self.out["at30"], 16)
        self.assertAlmostEqual(self.out["secs"], 1.9305503368377686, places=9)

    def test_typing_bounds_and_order(self):
        self.assertEqual(self.out["atNeg"], 0)
        self.assertEqual(self.out["atEnd"], self.out["total"])
        self.assertTrue(self.out["monotonic"])

    def test_typing_seconds_is_when_the_last_character_lands(self):
        self.assertEqual(self.out["atSecs"], self.out["total"])
        self.assertLess(self.out["atJustBefore"], self.out["total"])

    def test_line_break_is_a_pause(self):
        self.assertEqual(self.out["pause"], [self.out["len0"], self.out["len0"]])

    def test_stage_placement_is_014s_card(self):
        st = self.out["stage"]
        self.assertEqual(st["size"], "48px")
        self.assertEqual(st["pitch"], "94px")                  # pad 30 + one 64 px row
        self.assertEqual(st["h"], "252px")                     # 3 rows minimum: 2·30 + 3·64
        self.assertEqual(st["top"], "539px")                   # centred on 665
        self.assertEqual(st["n"], 8)
        self.assertTrue(st["border"])

    def test_fixed_type_keeps_a_beats_restyle(self):
        self.assertEqual(self.out["stageKeeps"], "46px")

    def test_dock_shrinks_to_the_longest_line(self):
        d = self.out["dock"]
        self.assertEqual(d["size"], "27px")                    # floor((885 − 56) / (50 · 0.6))
        self.assertEqual(d["pitch"], "38px")                   # round(27 · 1.4)
        self.assertEqual(d["h"], "132px")                      # 2 rows: 2·28 + 2·38
        self.assertEqual(d["top"], "1279px")                   # centred on 1345
        self.assertEqual(d["n"], 6)
        self.assertEqual(d["hero"], "#C084FC")
        self.assertEqual(d["comment"], "#8A8FB0")

    def test_dock_grows_back_and_follows_cy(self):
        self.assertEqual(self.out["dockShort"], {"size": "40px", "top": "916px"})   # 2·28 + 2·56 = 168, 1000 − 84

    def test_any_placement_by_option(self):
        self.assertEqual(self.out["moved"], "774px")           # 900 − 252 / 2


if __name__ == "__main__":
    unittest.main()
