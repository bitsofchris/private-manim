// ep4.js — ep 4's own parts on the shared machine (IterableDataset). Linked
// into a beat as `ep/` (ln -s ../_kit NN_beat/ep), loaded after kit/code.js
// and before ep/seam.js.
//
//   const ep = EP4.mount(root);   // mounts the machine (SC.mount) and the shards
//   ep.draw(S);                   // S = machine fields (machine.js) + S.shards
//
// The shards: the stream's data packed into files, drawn as three small cards
// (the worker-card style: panel, ink border, teal rows) in a row under the
// Dataset card's left half, y 412–488, x 75–415 (clear of the samples hopping
// at x ~430–590). They fade with the machine on a flip.
//
// S.shards fields (all optional; off by default):
//   o 0..1          opacity
//   order [a,b,c]   which card sits in slot 0, 1, 2 (identity 0,1,2; a permutation
//                   is the pre-shuffle). Fractional positions are fine: a beat
//                   lerps `pos` instead (pos[k] = slot of card k, 0..2) while they move.
//   pos [p0,p1,p2]  the slot of card k (overrides order; lets cards move between slots)
//   lift [l0,l1,l2] px up (negative = down); when given it replaces the built-in hop between slots,
//                   so a card passing two others can lift over them while they dip (a card is 68 px tall)
//   load 0..1       card `loadCard` rises into the Dataset card and fades (1 = loaded, gone)
//   loadCard k      which card is loaded (default: whichever sits in slot 0)
//   hero 0|1        the three cards magenta (the one magenta hero: set machine hero null)
//   take "row"|"column"   "row" is the default; "column" stacks them left of the Dataset card
//                   (00_layout only, for the frame Chris picks from)
//
// The code card's rows are set to 46 px here (see mount).
//
// Code lines (from kit/data.js, the ledger; nothing new is typed):
//   EP4.ITER   data.js `iterable`, the yield line lit "yield"
//   EP4.LEN    ITER plus the ledger's `len(stream)` → TypeError, as a comment line
//   EP4.CMP    the two methods side by side, unindented: `__iter__` (data.js iterable[1])
//              over `__getitem__` (data.js mapStyle[3])
(function () {
  const SC = window.SC, D = SC.D, PAL = SC.PAL;
  const it = D.code.iterable, ms = D.code.mapStyle;
  const ITER = it.map((l, i) => (i === 3 ? { t: l.t, lit: "yield" } : l));
  const LEN = ITER.concat([{ t: "len(stream)  # TypeError", lit: "len" }]);
  const CMP = [{ t: it[1].t.trim(), lit: "iter" }, { t: ms[3].t.trim(), lit: "getitem" }];

  // per-card row lengths (teal lines), fixed so a card keeps its look as it moves
  const ROWS = [[0.85, 0.55, 0.7], [0.6, 0.9, 0.45], [0.75, 0.4, 0.8]];
  const GEO = {
    row: { w: 104, h: 68, slot: (s) => ({ x: 75 + s * 120, y: 416 }) },
    column: { w: 104, h: 38, slot: (s) => ({ x: 75, y: 258 + s * 47 }) },
  };

  function mount(root) {
    const kit = SC.mount(root);
    // data.js `iterable[0]` is 30 characters, over the card's 28 at 48 px (its colon clips):
    // this episode's card types at 46 px (~27.6 px a character, 30 fit). Listed for the update pass.
    if (kit.code) kit.code.rows.forEach((el) => { el.style.fontSize = "46px"; });
    const g = SC.node("g", {}, kit.svg);
    const cards = [0, 1, 2].map((k) => {
      const cg = SC.node("g", {}, g);
      const r = SC.node("rect", { x: 0, y: 0, width: 104, height: 68, rx: 12, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 4 }, cg);
      const ls = ROWS[k].map((f) => SC.node("line", { x1: 16, y1: 0, x2: 16 + f * 72, y2: 0, stroke: PAL.data, "stroke-width": 5, "stroke-linecap": "round" }, cg));
      return { cg, r, ls };
    });
    function drawShards(S) {
      const sh = Object.assign({ o: 0, order: [0, 1, 2], load: 0, hero: 0, take: "row" }, S.shards || {});
      const mOn = 1 - SC.seg(S.flip || 0, 0, 0.6);
      const O = sh.o * mOn * (S.dataset == null ? 1 : S.dataset);
      const geo = GEO[sh.take] || GEO.row;
      const pos = sh.pos || [0, 1, 2].map((k) => sh.order.indexOf(k));
      const loadCard = sh.loadCard == null ? sh.order[0] : sh.loadCard;
      const ds = SC.G.dataset;
      cards.forEach((c, k) => {
        const p = pos[k], lo = Math.floor(p), hi = Math.min(2, lo + 1), f = p - lo;
        const a = geo.slot(lo), b = geo.slot(hi);
        let x = SC.lerp(a.x, b.x, f), y = SC.lerp(a.y, b.y, f) - (sh.lift ? sh.lift[k] : Math.sin(Math.PI * f) * 30);  // a hop between slots
        let o = O;
        if (k === loadCard && sh.load > 0) {
          // rise into the Dataset card's left half, fading as it enters
          const u = sh.load;
          x = SC.lerp(x, ds.x + 40, u); y = SC.lerp(y, ds.y + ds.h / 2 - geo.h / 2, u);
          o *= 1 - SC.seg(u, 0.55, 1);
        }
        c.cg.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
        c.r.setAttribute("height", geo.h);
        const col = sh.hero ? PAL.hero : PAL.ink;
        c.r.setAttribute("stroke", col);
        c.ls.forEach((l, j) => {
          const ly = geo.h === 68 ? 18 + j * 16 : 10 + j * 9;
          l.setAttribute("y1", ly); l.setAttribute("y2", ly);
          l.setAttribute("stroke-width", geo.h === 68 ? 5 : 3.5);
        });
        SC.show(c.cg, o);
      });
    }
    function draw(S) { kit.draw(null, S); drawShards(S); }
    return { draw, kit, parts: kit.parts };
  }

  window.EP4 = { mount, ITER, LEN, CMP };
})();
