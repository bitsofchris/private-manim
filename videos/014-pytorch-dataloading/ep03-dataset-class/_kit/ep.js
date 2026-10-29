// ep.js — ep 3's code cards (the map-style Dataset and the hand-rolled loop),
// linked into a beat as `ep/` and loaded after kit/code.js:
//   ln -s ../_kit NN_beat/ep        (from the episode folder)
//   <script src="ep/ep.js"></script><script src="ep/seam.js"></script>
//
// The lines are the shared kit's (DL_DATA.code.mapStyle / handRolled), text
// unchanged. Only `lit` tags are added where ep 3's VO names a line the shared
// kit leaves untagged: the slice (`return self.series[i]`, "getitem is just a
// slice"). Listed for the update pass.
//
// EP.MAP     the five-line Dataset card; lit: dataset, len, getitem, slice
// EP.HAND    the four-line hand-rolled loop; lit: sampler, batching, collate
// EP.TWO     ["len", "getitem"]: both methods lit together ("two functions")
// EP.typedAt(lines, seconds, cps) = SC_typedAt, re-exported for brevity
// EP.litAt(lines, typed, fallback): the `lit` of the line being typed (the hero
//            passes to it as it lands), or `fallback` before any tagged line
(function () {
  const C = window.DL_DATA.code;
  const MAP = C.mapStyle.map((ln, i) => (i === 4 ? Object.assign({}, ln, { lit: "slice" }) : Object.assign({}, ln)));
  const HAND = C.handRolled.map((ln) => Object.assign({}, ln));
  function litAt(lines, typed, fallback = null) {
    let n = 0, lit = fallback;
    lines.forEach((ln) => { if (typed > n && ln.lit) lit = ln.lit; n += ln.t.length; });
    return lit;
  }
  const chars = (lines) => lines.reduce((a, l) => a + l.t.length, 0);
  window.EP = { MAP, HAND, TWO: ["len", "getitem"], typedAt: window.SC_typedAt, litAt, chars };
})();
