// ep05.js — episode 5's numbers, layout and rest states (nn.Linear's shape).
// Linked into each beat as `ep/`, after vendor/gsap, iso/iso.js and vec/vec.js:
//   ln -s ../_ep NN_beat/ep
// Everything drawn comes from the shared plane kit (VEC); this file only holds
// the ledger (storyboard.md), where things sit, and the four states beats open
// and end on. Beats never edit it; they draw their changes on top of a state.
(function () {
  const { COL, css } = ISO;
  const { fmtv, SLOT } = VEC;

  // ---- the ledger (storyboard.md; the (5, 3) @ (3, 2) example, row 1) ----
  const X = [1, 2, -1];                                  // one input row
  const WEIGHT = [[2, 0.5, -1], [-1, 1, 2]];             // lin.weight, (2, 3): one row per output neuron
  const WT = [[2, -1], [0.5, 1], [-1, 2]];               // lin.weight.T, (3, 2): ep04's W, row i = where input i lands
  const B = [0.1, -0.2];                                 // lin.bias
  const DOT = [4, -1];                                   // row n of weight · x  (x @ weight.T)
  const Y = [4.1, -1.2];                                 // x @ weight.T + bias
  const PROD = [[2, 1, 1], [-1, 2, -2]];                 // x[i] * weight[n][i]
  // The code on screen (literal PyTorch, ASCII minus as PyTorch prints it).
  // MODEL is the context (beat 1 zooms into line 1, beat 9 zooms back out);
  // CODE are the two-line cards beats 2-4 show in place of the one-line card.
  const MODEL = ["model = nn.Sequential(", "    nn.Linear(3, 2),", "    nn.ReLU(),", ")"];
  const MODEL_LINE = 1;                                  // the nn.Linear line
  const CODE = {
    shape: ["model[0].weight.shape", "torch.Size([2, 3])"],   // beat 2, "come back two by three"
    neuron: ["x @ weight[0]", "  + bias[0]  # 4.1"],         // beat 3, "outputs one number"
    call: ["model[0](x)", "tensor([4.1, -1.2])"],           // beat 4, "two outputs"
  };
  // Colour carries the input direction everywhere: input i, column i of weight,
  // row i of weight.T and its landing arrow are SLOT[i] (teal, blue, gold).
  // Neurons have no colour of their own; the active one gets the magenta box.

  // ---- layout (px, 1080 x 1920; stage y 230-1100) ----
  const CARD_TOP = 236;                                  // the one-line code card
  const NAME_TOP = 372, SHAPE_TOP = 440;                 // matrix name (code) and shape (Inter), 60 px
  const MAT_TOP = 516, CW = 110, RH = 72, SIZE = 60;     // matrix cells
  const WL = { STORED: 375, LEFT: 120 };                 // weight's left edge: centred (beats 1-4), left (5-9)
  const TL = 650;                                        // weight.T's left edge
  const ARROW = { x: 550, y: 580 };                      // the ".T →" between the two matrices (centre, at MAT_TOP)
  // LIFTED (beats 6-9, once the plane is in; Chris, 2026-10-12): the names and
  // shapes go and the matrices move up by LIFT, so the plane gets their room.
  const MAT_UP = 392, LIFT = MAT_TOP - MAT_UP;
  // LAY.top: the matrices' current top; LAY.names: the names' and shapes' alpha.
  // state() sets both; a beat moving between them calls lift(Pt, u) after state().
  const LAY = { top: MAT_TOP, names: 1 };
  // the network (lower stage, beats 1-4): inputs -> two neurons -> outputs
  const NET = { inX: 280, inY: [818, 930, 1042], nX: 640, nY: [874, 986], r: 46, outX: 720 };
  // the plane (lower stage, beats 6-9): rows of weight.T as arrows from the origin
  // (first build: step 92, oy 980, top 770; taller since the lift)
  const PLANE = { step: 118, ox: 600, oy: 940, ax: { w: -1.6, e: 2.6, s: -1.3, n: 2.3 }, top: 640 };

  const matW = (cols) => cols * CW;
  const mid = (left, cols) => left + matW(cols) / 2;

  // ---- DOM parts, made once per beat ----
  function cells(root, vals, left, colOf) {
    return vals.map((row, r) => row.map((v, c) => VEC.cell(root, fmtv(v), {
      left: left + c * CW, top: MAT_TOP + r * RH, width: CW, height: RH, size: SIZE, col: colOf(r, c),
    })));
  }
  function nameLabel(root, text, code) {
    const el = ISO.label(root, text, { size: SIZE, color: css(COL.dim), width: 400, align: "center" });
    if (code) VEC.code(el);
    return el;
  }
  // P: cardA "nn.Linear(3, 2)", cardB "x @ weight.T + bias" (spans: x, @, weight, .T, + bias),
  // w[r][c] / wt[r][c] cells, wB / tB brackets, names {w, wShape, t, tShape}, tArrow {dot, arr},
  // net {ins[i], outs[n]} (DOM numbers; circles and lines are canvas), hl / hl2 highlight boxes.
  function parts(root) {
    const cardA = VEC.codeCard(root, ["nn.Linear(3, 2)"]);
    const cardB = VEC.codeCard(root, [[["x", SLOT[0]], [" @ "], ["weight"], [".T", COL.hero], [" + bias"]]]);
    cardB.spans[0][0].style.color = css(COL.text);
    const w = cells(root, WEIGHT, WL.STORED, (r, c) => SLOT[c]);
    const wt = cells(root, WT, TL, (r) => SLOT[r]);
    const wB = VEC.brackets(root, WL.STORED, MAT_TOP, WL.STORED + matW(3), 2 * RH);
    const tB = VEC.brackets(root, TL, MAT_TOP, TL + matW(2), 3 * RH);
    const names = { w: nameLabel(root, "weight", true), wShape: nameLabel(root, "(2, 3)"),
                    t: nameLabel(root, "weight.T", true), tShape: nameLabel(root, "(3, 2)") };
    const tArrow = { dot: VEC.code(ISO.label(root, ".T", { size: SIZE, color: css(COL.hero), width: 120 })),
                     arr: ISO.label(root, "→", { size: 72, color: css(COL.dim), width: 120 }) };
    const num = (t) => { const el = ISO.label(root, t, { size: SIZE, width: 160, align: "center" }); el.style.fontVariantNumeric = "tabular-nums"; return el; };
    const net = { ins: X.map((v) => num(fmtv(v))), outs: Y.map((v) => num(fmtv(v))) };
    net.outs.forEach((el) => { el.style.textAlign = "left"; });
    return { cardA, cardB, w, wt, wB, tB, names, tArrow, net, hl: VEC.hbox(root), hl2: VEC.hbox(root) };
  }

  // ---- placement helpers ----
  const put = (el, left, top, alpha = 1, col) => {
    el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px)`;
    el.style.opacity = alpha.toFixed(3);
    if (col) el.style.color = css(col);
  };
  // weight's cells and brackets at left edge `left` (alpha a)
  function placeW(Pt, left, a = 1) {
    const dy = LAY.top - MAT_TOP;
    Pt.w.forEach((row, r) => row.forEach((c, k) => { c.at(left + k * CW, LAY.top + r * RH, { alpha: a }); }));
    Pt.wB.at(left - WL.STORED, dy, { alpha: a });
    put(Pt.names.w, mid(left, 3) - 200, NAME_TOP + dy, a * LAY.names);
    put(Pt.names.wShape, mid(left, 3) - 200, SHAPE_TOP + dy, a * LAY.names);
  }
  function placeT(Pt, a = 1) {
    const dy = LAY.top - MAT_TOP;
    Pt.wt.forEach((row, r) => row.forEach((c, k) => c.at(TL + k * CW, LAY.top + r * RH, { alpha: a })));
    Pt.tB.at(0, dy, { alpha: a });
    put(Pt.names.t, mid(TL, 2) - 200, NAME_TOP + dy, a * LAY.names);
    put(Pt.names.tShape, mid(TL, 2) - 200, SHAPE_TOP + dy, a * LAY.names);
    put(Pt.tArrow.dot, ARROW.x - 60, ARROW.y - 70 + dy, a);
    put(Pt.tArrow.arr, ARROW.x - 60, ARROW.y + dy, a);
  }
  // the names and shapes fade over the first half, the matrices rise over the whole (u 0..1)
  function lift(Pt, u) {
    const k = ISO.clamp01(u);
    LAY.top = MAT_TOP - LIFT * k; LAY.names = 1 - ISO.clamp01(k * 2);
    placeW(Pt, WL.LEFT); placeT(Pt, 1);
  }
  // highlight-box rects (at the matrices' current top): a row of weight, a column of weight, a row of weight.T
  const RECT = {
    wRow: (n, left = WL.LEFT) => [left - 12, LAY.top + n * RH - 4, matW(3) + 24, RH + 8],
    wCol: (i, left = WL.LEFT) => [left + i * CW - 4, LAY.top - 12, CW + 8, 2 * RH + 24],
    tRow: (i) => [TL - 12, LAY.top + i * RH - 4, matW(2) + 24, RH + 8],
    shapeW: (left = WL.LEFT) => [mid(left, 3) - 110, SHAPE_TOP - 6, 220, 80],
    shapeT: () => [mid(TL, 2) - 110, SHAPE_TOP - 6, 220, 80],
  };

  // ---- canvas: the network and the plane ----
  // the network (o: x (show input numbers), lit [n] (0..1 per neuron), wire alpha,
  // out [n] (0..1 alpha of each output number))
  function network(g, Pt, o = {}) {
    const lit = o.lit || [0, 0], out = o.out || [0, 0], wa = o.wire == null ? 0.5 : o.wire;
    NET.nY.forEach((ny, n) => NET.inY.forEach((iy, i) => {
      g.save(); g.strokeStyle = css(SLOT[i], 1, wa * (lit[n] > 0 ? 1 : 0.7) + 0.3 * lit[n]); g.lineWidth = 5 + 3 * lit[n];
      g.beginPath(); g.moveTo(NET.inX + NET.r, iy); g.lineTo(NET.nX - NET.r, ny); g.stroke(); g.restore();
    }));
    NET.inY.forEach((iy, i) => ring(g, NET.inX, iy, SLOT[i], 1));
    NET.nY.forEach((ny, n) => ring(g, NET.nX, ny, ISO.mix(COL.dim, COL.hero, lit[n]), 1));
    NET.inY.forEach((iy, i) => put(Pt.net.ins[i], NET.inX - 80, iy - 33, o.x ? 1 : 0, SLOT[i]));
    NET.nY.forEach((ny, n) => put(Pt.net.outs[n], NET.outX + 20, ny - 33, out[n], COL.text));
  }
  function ring(g, x, y, col, al) {
    g.save(); g.beginPath(); g.arc(x, y, NET.r, 0, Math.PI * 2);
    g.fillStyle = css(COL.panel, 1, al); g.fill();
    g.strokeStyle = css(col, 1, al); g.lineWidth = 6; g.stroke(); g.restore();
  }
  // the plane with the three landing arrows (o: alpha, u (draw progress))
  function plane(g, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    VEC.view(PLANE);
    VEC.floor(g, { alpha: 0.42 * al });
    VEC.axes(g, { alpha: al });
    WT.forEach((row, i) => VEC.arrow(g, [0, 0], row, { col: SLOT[i], alpha: al, u: o.u, width: 40 }));
    VEC.puck(g, 0, 0, { alpha: al });
  }
  function bg(g) { g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }

  // ---- the rest states (storyboard.md "States") ----
  // STORED  : cardA; weight (2, 3) centred; the network, inputs empty, no outputs.
  // OUTPUTS : STORED + input numbers 1, 2, −1 + outputs 4.1, −1.2.
  // FLIPPED : cardB; weight at the left, ".T →", weight.T (3, 2) at the right; lower stage empty.
  // CANON   : FLIPPED lifted (no names or shapes, matrices at MAT_UP) + the plane with
  //           weight.T's rows as landing arrows.
  function state(Pt, g, name) {
    const A = name === "STORED" || name === "OUTPUTS";
    LAY.top = name === "CANON" ? MAT_UP : MAT_TOP; LAY.names = name === "CANON" ? 0 : 1;
    Pt.cardA.at(VEC.centreLeft(Pt.cardA.el), CARD_TOP, { alpha: A ? 1 : 0 });
    Pt.cardB.at(VEC.centreLeft(Pt.cardB.el), CARD_TOP, { alpha: A ? 0 : 1 });
    [Pt.w, Pt.wt].forEach((m) => m.forEach((row) => row.forEach((c) => { c.color(c.col0); c.border(COL.hero, 0); })));
    Pt.wB.color(COL.dim); Pt.tB.color(COL.dim);
    Object.values(Pt.names).forEach((el) => { el.style.color = css(COL.dim); });
    Pt.tArrow.dot.style.color = css(COL.hero);
    Pt.hl.rect(RECT.wRow(0), 0); Pt.hl2.rect(RECT.wRow(1), 0);
    placeW(Pt, A ? WL.STORED : WL.LEFT);
    placeT(Pt, A ? 0 : 1);
    if (!g) return;
    bg(g);
    if (A) {
      network(g, Pt, { x: name === "OUTPUTS", out: name === "OUTPUTS" ? [1, 1] : [0, 0] });
    } else {
      Pt.net.ins.forEach((el) => put(el, 0, 0, 0)); Pt.net.outs.forEach((el) => put(el, 0, 0, 0));
      if (name === "CANON") plane(g);
    }
  }

  window.EP = {
    X, WEIGHT, WT, B, DOT, Y, PROD, MODEL, MODEL_LINE, CODE,
    CARD_TOP, NAME_TOP, SHAPE_TOP, MAT_TOP, MAT_UP, LIFT, LAY, CW, RH, SIZE, WL, TL, ARROW, NET, PLANE, RECT,
    parts, put, placeW, placeT, lift, network, ring, plane, bg, state,
  };
})();
