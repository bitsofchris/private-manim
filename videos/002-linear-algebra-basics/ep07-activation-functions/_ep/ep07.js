// ep07.js — episode 7's numbers, layout and rest states (why layers need activations).
// Linked into each beat as `ep/`, after vendor/gsap, iso/iso.js and vec/vec.js:
//   ln -s ../_ep NN_beat/ep
// Everything drawn comes from the shared plane kit (VEC) plus one local part,
// `warp` (the plane's grid pushed through any map, linear or not, drawn as
// sampled polylines). This file holds the ledger (storyboard.md), where things
// sit, and the states beats open and end on. Beats never edit it; they draw
// their changes on top of a state.
(function () {
  const { COL, css, lerp, clamp01 } = ISO;
  const { fmtv } = VEC;

  // ---- the ledger (storyboard.md) ----
  // Row-vector (PyTorch) convention: x @ W, row i of W is where e_i lands.
  const X = [1, 2];                                      // the input row
  const W1 = [[1, 1], [-1, 1]];                          // layer 1: rotate 45° and stretch
  const W2 = [[1, 0], [0, 0.5]];                         // layer 2: squish north-south by half
  const W = [[1, 0.5], [-1, 0.5]];                       // W1 @ W2, the one matrix
  const XW1 = [-1, 3];                                   // x @ W1
  const XW = [-1, 1.5];                                  // x @ W1 @ W2 == x @ W
  const RXW1 = [0, 3];                                   // relu(x @ W1)
  const RXW = [0, 1.5];                                  // relu(x @ W1) @ W2
  // The hero line (beats 7-10): the input grid line through x, x1 = 1. Linear
  // maps keep it straight; relu(x @ W1) @ W2 bends it at (2, 0) and (0, 1).
  const LINE_X = 1;

  // The code on screen (literal PyTorch; ASCII as it would be typed).
  const CODE = {
    stack: [[["x", COL.data], [" @ "], ["W1"], [" @ "], ["W2"]]],
    assoc: [[["("], ["x", COL.data], [" @ "], ["W1"], [")"], [" @ "], ["W2"]]],
    same: [[["("], ["x", COL.data], [" @ "], ["W1"], [")"], [" @ "], ["W2"]],
           [["== "], ["x", COL.data], [" @ "], ["(W1 @ W2)"]]],
    merged: [[["x", COL.data], [" @ "], ["W", COL.hero]]],
    seq: ["nn.Sequential(", "  nn.Linear(2, 2),", [["  "], ["nn.ReLU()", COL.hero], [","]], "  nn.Linear(2, 2),", ")"],
  };
  const SEQ_RELU = 2;                                     // the nn.ReLU() line of CODE.seq

  // ---- layout (px, 1080 x 1920; stage y 230-1100) ----
  const CARD_TOP = 236;                                  // every code card's top edge, centred
  const NAME_TOP = 372;                                  // matrix names (Inter, --dim), 60 px
  const MAT_TOP = 450, CW = 110, RH = 72, SIZE = 60;     // matrix cells
  const ML = { W1: 195, W2: 600, W: 397 };               // matrices' left edges: W1 @ W2 side by side; W centred
  const AT = { x: 507, y: MAT_TOP + RH - 36 };           // (195 + 220 + 600) / 2           // the "@" between W1 and W2 (centre)
  // the plane, lower stage: room for x (1, 2), x @ W1 (−1, 3) and the bent line's
  // corner at (2, 0); clipped above y 620, under the matrices
  const PLANE = { step: 120, ox: 447, oy: 1016, ax: { w: -1.6, e: 2.6, s: -0.6, n: 3.3 }, top: 620 };

  const matW = (cols) => cols * CW;
  const mid = (left) => left + matW(2) / 2;

  // ---- DOM parts, made once per beat ----
  function cells(root, vals, left, col) {
    return vals.map((row, r) => row.map((v, c) => VEC.cell(root, fmtv(v), {
      left: left + c * CW, top: MAT_TOP + r * RH, width: CW, height: RH, size: SIZE, col,
    })));
  }
  function nameLabel(root, text) {
    return ISO.label(root, text, { size: SIZE, color: css(COL.dim), width: 300, align: "center" });
  }
  // P: cards {stack, assoc, same, merged, seq} (VEC.codeCard: el, spans[line][span], at),
  // m {W1, W2, W} cells[r][c], b {W1, W2, W} brackets, names {W1, W2, W}, at ("@" between
  // W1 and W2), hl / hl2 highlight boxes.
  function parts(root) {
    const cards = {};
    Object.keys(CODE).forEach((k) => { cards[k] = VEC.codeCard(root, CODE[k]); });
    const m = { W1: cells(root, W1, ML.W1, COL.text), W2: cells(root, W2, ML.W2, COL.text), W: cells(root, W, ML.W, COL.text) };
    const b = {};
    Object.keys(ML).forEach((k) => { b[k] = VEC.brackets(root, ML[k], MAT_TOP, ML[k] + matW(2), 2 * RH); });
    const names = { W1: nameLabel(root, "W1"), W2: nameLabel(root, "W2"), W: nameLabel(root, "W") };
    const at = ISO.label(root, "@", { size: 72, color: css(COL.dim), width: 120 });
    VEC.code(at);
    return { cards, m, b, names, at, hl: VEC.hbox(root), hl2: VEC.hbox(root) };
  }

  // ---- placement helpers ----
  const put = (el, left, top, alpha = 1, col) => {
    el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px)`;
    el.style.opacity = alpha.toFixed(3);
    if (col) el.style.color = css(col);
  };
  // one matrix (key W1 / W2 / W) at left edge `left`, alpha a, digit colour col, name alpha na
  function placeM(Pt, key, left, a = 1, col = COL.text, na = a) {
    Pt.m[key].forEach((row, r) => row.forEach((c, k) => { c.at(left + k * CW, MAT_TOP + r * RH, { alpha: a }); c.color(col); c.border(COL.hero, 0); }));
    Pt.b[key].at(left - ML[key], 0, { alpha: a });
    put(Pt.names[key], mid(left) - 150, NAME_TOP, na);
  }
  // a card centred at the top (alpha a)
  function placeCard(card, a = 1, o = {}) { card.at(VEC.centreLeft(card.el), CARD_TOP, { alpha: a, scale: o.scale }); }
  // highlight-box rects
  const RECT = {
    mat: (key, left = ML[key]) => [left - 34, MAT_TOP - 12, matW(2) + 68, 2 * RH + 24],
    row: (key, r, left = ML[key]) => [left - 12, MAT_TOP + r * RH - 4, matW(2) + 24, RH + 8],
  };

  // ---- the maps ----
  // stage(o) -> p => q: p @ lerp(I, W1, o.w1); then o.relu of the way to relu; then
  // @ lerp(I, W2, o.w2); then @ o.post (any 2x2, e.g. beat 7's stretch / rotate / squish).
  // At { w1: 1, w2: 1 } it is p @ W (the collapse); with relu: 1 it bends.
  function stage(o = {}) {
    const A = VEC.basisTo(VEC.I2, W1, o.w1 || 0), B = VEC.basisTo(VEC.I2, W2, o.w2 || 0), r = o.relu || 0;
    return (p) => {
      let q = VEC.comb(p, A);
      if (r) q = [lerp(q[0], Math.max(q[0], 0), r), lerp(q[1], Math.max(q[1], 0), r)];
      q = VEC.comb(q, B);
      return o.post ? VEC.comb(q, o.post) : q;
    };
  }
  const S = {                                            // the stages the states use
    ID: {}, W1: { w1: 1 }, W: { w1: 1, w2: 1 },
    FOLD: { w1: 1, relu: 1 }, BENT: { w1: 1, relu: 1, w2: 1 },
  };

  // ---- canvas ----
  // a polyline through the images of grid points p(t), t in [t0, t1], clipped to the plane
  function polyline(g, f, p, t0, t1, o = {}) {
    const n = Math.max(2, Math.ceil((t1 - t0) / 0.04));
    g.beginPath();
    for (let i = 0; i <= n; i++) {
      const q = f(p(lerp(t0, t1, i / n))), s = VEC.at(q[0], q[1]);
      if (i === 0) g.moveTo(s[0], s[1]); else g.lineTo(s[0], s[1]);
    }
    g.strokeStyle = css(o.col || COL.muted, 1, o.alpha == null ? 1 : o.alpha);
    g.lineWidth = o.width || 3; g.lineJoin = "round"; g.lineCap = "round";
    g.stroke();
  }
  // warp: the input grid (one line per step) pushed through f. o: alpha, col, width, n (lines each way)
  function warp(g, f, o = {}) {
    const n = o.n || 9, al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    for (let k = -n; k <= n; k++) {
      polyline(g, f, (t) => [k, t], -n, n, { col: o.col || [74, 80, 112], alpha: 0.6 * al, width: o.width || 3 });
      polyline(g, f, (t) => [t, k], -n, n, { col: o.col || [74, 80, 112], alpha: 0.6 * al, width: o.width || 3 });
    }
  }
  // the hero line: input line x1 = LINE_X through f (o: col, alpha, width)
  function heroLine(g, f, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    polyline(g, f, (t) => [LINE_X, t], -9, 9, { col: o.col || COL.hero, alpha: al, width: o.width || 7 });
  }
  // a dashed hop between two grid points (x's trail), o: alpha, u (draw progress), col
  function hop(g, a, b, o = {}) {
    VEC.line(g, a, b, { col: o.col || COL.dim, alpha: o.alpha == null ? 0.9 : o.alpha, width: 5, dash: [14, 12], u: o.u });
  }
  function bg(g) { g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }
  // The plane, under everything. o: f (the map, default identity), alpha, hero (hero-line
  // alpha, 0 = off), heroCol, x (draw x's arrow to f(X); default true), xAlpha,
  // trail: [[a, b, alpha], ...] dashed hops with a dot at each start.
  function plane(g, o = {}) {
    const f = o.f || stage(S.ID), al = o.alpha == null ? 1 : o.alpha;
    VEC.view(PLANE);
    g.save(); g.beginPath(); g.rect(0, PLANE.top, ISO.W, ISO.SAFE.stageBottom - PLANE.top); g.clip();
    VEC.floor(g, { alpha: 0.12 * al });                  // the old grid, a ghost (agents/style.md: ~0.14)
    warp(g, f, { alpha: al });
    VEC.axes(g, { alpha: al });
    (o.trail || []).forEach(([a, b, ta]) => { hop(g, a, b, { alpha: 0.9 * ta * al }); VEC.puck(g, a[0], a[1], { half: 11, col: COL.dim, alpha: ta * al }); });
    if (o.hero) heroLine(g, f, { alpha: o.hero * al, col: o.heroCol });
    if (o.x !== false) { const q = f(X); VEC.arrow(g, [0, 0], q, { col: COL.data, alpha: (o.xAlpha == null ? 1 : o.xAlpha) * al, width: 40 }); }
    VEC.puck(g, 0, 0, { alpha: al });
    g.restore();
  }

  // ---- the rest states (storyboard.md "States") ----
  // STACK  : card `x @ W1 @ W2`; W1 @ W2 with names; plane: the plain grid, x (1, 2).
  // CHAIN  : STACK, the grid through W1 then W2, x at (−1, 1.5), its two hops dashed.
  // ASSOC  : CHAIN with the card `(x @ W1) @ W2`.
  // SAME   : the two-line card `(x @ W1) @ W2` / `== x @ (W1 @ W2)`, names hidden;
  //          CHAIN's plane + the shortcut hop (1, 2) -> (−1, 1.5).
  // MERGED : card `x @ W` (W magenta); W centred, magenta digits; plane through W,
  //          x at (−1, 1.5), only the shortcut hop.
  // LINEAR : MERGED with W's digits white and no hop; the hero line (x1 = 1) magenta, straight.
  // FOLDED : the nn.Sequential card (nn.ReLU() magenta), no matrices; plane relu(p @ W1),
  //          hero line bent, x at (0, 3).
  // BENT   : FOLDED with the plane relu(p @ W1) @ W2, x at (0, 1.5).
  // END    : MERGED without the hop (the last frame: one matrix).
  const TRAIL2 = [[X, XW1, 1], [XW1, XW, 1]];
  const SHORT = [[X, XW, 1]];
  function state(Pt, g, name) {
    const cardOf = { STACK: "stack", CHAIN: "stack", ASSOC: "assoc", SAME: "same", MERGED: "merged", LINEAR: "merged", END: "merged", FOLDED: "seq", BENT: "seq" }[name];
    Object.keys(Pt.cards).forEach((k) => placeCard(Pt.cards[k], k === cardOf ? 1 : 0));
    const two = ["STACK", "CHAIN", "ASSOC", "SAME"].includes(name), one = ["MERGED", "LINEAR", "END"].includes(name);
    const na = name === "SAME" ? 0 : 1;
    placeM(Pt, "W1", ML.W1, two ? 1 : 0, COL.text, two ? na : 0);
    placeM(Pt, "W2", ML.W2, two ? 1 : 0, COL.text, two ? na : 0);
    placeM(Pt, "W", ML.W, one ? 1 : 0, name === "LINEAR" ? COL.text : COL.hero, one ? 1 : 0);
    Object.keys(Pt.b).forEach((k) => Pt.b[k].color(COL.dim));
    Pt.cards.merged.spans[0][2].style.color = css(name === "LINEAR" ? COL.text : COL.hero);   // one hero: in LINEAR it is the line
    put(Pt.at, AT.x - 60, AT.y - 40, two ? 1 : 0);
    Pt.hl.rect(RECT.mat("W1"), 0); Pt.hl2.rect(RECT.mat("W2"), 0);
    if (!g) return;
    bg(g);
    const P = {
      STACK: { f: stage(S.ID) },
      CHAIN: { f: stage(S.W), trail: TRAIL2 }, ASSOC: { f: stage(S.W), trail: TRAIL2 },
      SAME: { f: stage(S.W), trail: TRAIL2.concat(SHORT) },
      MERGED: { f: stage(S.W), trail: SHORT }, END: { f: stage(S.W) },
      LINEAR: { f: stage(S.W), hero: 1 },
      FOLDED: { f: stage(S.FOLD), hero: 1 }, BENT: { f: stage(S.BENT), hero: 1 },
    }[name];
    plane(g, P);
  }

  window.EP = {
    X, W1, W2, W, XW1, XW, RXW1, RXW, LINE_X, CODE, SEQ_RELU,
    CARD_TOP, NAME_TOP, MAT_TOP, CW, RH, SIZE, ML, AT, PLANE, RECT, S, TRAIL2, SHORT,
    parts, put, placeM, placeCard, stage, polyline, warp, heroLine, hop, bg, plane, state,
  };
})();
