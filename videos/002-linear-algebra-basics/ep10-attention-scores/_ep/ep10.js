// ep10.js — episode 10's numbers, layout and rest states (attention scores are dot products).
// Linked into each beat as `ep/`, after vendor/gsap, iso/iso.js and vec/vec.js:
//   ln -s ../_ep NN_beat/ep
// Everything drawn comes from the shared plane kit (VEC) plus one local part,
// `keyArrow` (an outline arrow: a key, so one token colour can be a query and a
// key at once). This file holds the ledger (storyboard.md), where things sit,
// and the states beats open and end on. Beats never edit it; they draw their
// changes on top of a state.
(function () {
  const { COL, css, lerp, clamp01 } = ISO;
  const { fmtv, SLOT } = VEC;

  // ---- the ledger (storyboard.md; Chris's unit_05_attention_scores notebook) ----
  // Row-vector (PyTorch) convention: tokens are rows of X, Q = X @ W_Q, K = X @ W_K.
  const TOK = ["my", "name", "is"];                      // ISO.TOKENS, the channel's example
  const X = [[1, 0], [1, 1], [0, 2]];
  const WQ = [[1, 1], [0, 1]];
  const WK = [[1, 0], [1, 1]];
  const Q = [[1, 1], [1, 2], [0, 2]];                    // X @ W_Q
  const K = [[1, 0], [2, 1], [2, 2]];                    // X @ W_K
  const S = [[1, 3, 4], [1, 4, 6], [0, 2, 4]];           // Q @ K.T
  const HERO = { r: 1, c: 2 };                           // query "name" . key "is" = 1*2 + 2*2 = 6
  const D = 2;                                           // head size: divide by sqrt(2)
  const SS = [["0.7", "2.1", "2.8"], ["0.7", "2.8", "4.2"], ["0", "1.4", "2.8"]];      // S / sqrt(2), one decimal
  const WT = [["0.1", "0.3", "0.6"], ["0.0", "0.2", "0.8"], ["0.0", "0.2", "0.8"]];    // softmax rows, one decimal
  const WN = [0.023, 0.191, 0.786];                      // query "name"'s weights, unrounded (beat 9's key alphas)
  const SR = S.map((r) => r.map((v) => fmtv(v)));        // raw scores as text

  // The code on screen (literal PyTorch, one line at a time).
  const CODE = {
    q: [[["Q", COL.text], [" = "], ["X"], [" @ "], ["W_Q"]]],
    k: [[["K", COL.text], [" = "], ["X"], [" @ "], ["W_K"]]],
    s: [[["scores"], [" = "], ["Q"], [" @ "], ["K.T"]]],
    d: [[["scores"], [" /= "], ["d**0.5"]]],
    w: [[["w"], [" = "], ["scores"], [".softmax(-1)"]]],
  };

  // ---- layout (px, 1080 x 1920; stage y 230-1100) ----
  const CARD_TOP = 236;                                  // the code card's top edge, centred
  const NAME_TOP = 372;                                  // matrix names / key headers, 60 px
  const MAT_TOP = 450, RH = 72, CW = 110, SIZE = 60;     // matrix rows and 3 x 2 cells
  const WORD_RIGHT = 236;                                // the word column's right edge
  const LL = 286, RL = 626;                              // left slot (X / Q), right slot (W_Q / W_K / K)
  const GL = 286, GCW = 160;                             // the score grid: left edge, cell width
  const SIDE = 810;                                      // right of the grid: ÷ √2, = 1
  const SHAPE_LEFT = 70;                                 // (3, 3), above the word column
  // the plane, lower stage: first quadrant, every vector here is within (2, 2)
  const PLANE = { step: 165, ox: 215, oy: 1075, ax: { w: -0.35, e: 2.4, s: -0.3, n: 2.25 }, top: 700 };
  const READ = { left: 640, top: 850 };                  // the dot-product readout, right of the plane
  const ALPHA_OFF = 0.22;                                // arrows not in the pair
  const rowTop = (r) => MAT_TOP + r * RH;
  const colMid = (c) => GL + c * GCW + GCW / 2;

  // ---- DOM parts, made once per beat ----
  const lbl = (root, text, o = {}) => ISO.label(root, text, { size: o.size || SIZE, color: css(o.col || COL.dim), width: o.width || 200, align: o.align || "center" });
  const put = (el, left, top, alpha = 1, col, scale = 1) => {
    el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${scale.toFixed(4)})`;
    el.style.opacity = clamp01(alpha).toFixed(3);
    if (col) el.style.color = css(col);
  };
  // P: cards {q, k, s, d, w}; words[3], heads[3] (token-coloured labels); m {X, Q, K, WQ, WK, S}
  // cells[r][c]; b {...} brackets; names {X, Q, K, WQ, WK}; shape "(3, 3)"; div "÷ √2";
  // sums[3] "= 1"; read {el, q[2], k[2], res (the 6)}; tips {name, is}; hl {q, k, rows[3]}.
  function parts(root) {
    const cards = {};
    Object.keys(CODE).forEach((k) => { cards[k] = VEC.codeCard(root, CODE[k]); });
    const words = TOK.map((w, i) => lbl(root, w, { col: SLOT[i], align: "right" }));
    const heads = TOK.map((w, i) => lbl(root, w, { col: SLOT[i], width: GCW + 40 }));
    const white = [COL.text, COL.text, COL.text];
    const m = {
      X: VEC.grid(root, X, LL, MAT_TOP, { cellW: CW, rowH: RH, size: SIZE }),
      Q: VEC.grid(root, Q, LL, MAT_TOP, { cellW: CW, rowH: RH, size: SIZE }),
      K: VEC.grid(root, K, RL, MAT_TOP, { cellW: CW, rowH: RH, size: SIZE }),
      WQ: VEC.grid(root, WQ, RL, MAT_TOP, { cellW: CW, rowH: RH, size: SIZE, rowCol: white }),
      WK: VEC.grid(root, WK, RL, MAT_TOP, { cellW: CW, rowH: RH, size: SIZE, rowCol: white }),
      S: VEC.grid(root, S, GL, MAT_TOP, { cellW: GCW, rowH: RH, size: SIZE, rowCol: white }),
    };
    const b = {
      X: VEC.brackets(root, LL, MAT_TOP, LL + 2 * CW, 3 * RH), Q: VEC.brackets(root, LL, MAT_TOP, LL + 2 * CW, 3 * RH),
      K: VEC.brackets(root, RL, MAT_TOP, RL + 2 * CW, 3 * RH),
      WQ: VEC.brackets(root, RL, MAT_TOP, RL + 2 * CW, 2 * RH), WK: VEC.brackets(root, RL, MAT_TOP, RL + 2 * CW, 2 * RH),
      S: VEC.brackets(root, GL, MAT_TOP, GL + 3 * GCW, 3 * RH),
    };
    const names = { X: lbl(root, "X"), Q: lbl(root, "Q"), K: lbl(root, "K"), WQ: lbl(root, "W_Q"), WK: lbl(root, "W_K") };
    const shape = lbl(root, "(3, 3)", { align: "left", width: 200 });
    const div = lbl(root, "÷ √2", { align: "left", width: 200 });
    const sums = [0, 1, 2].map(() => lbl(root, "= 1", { align: "left", width: 160 }));
    // the readout: "1·2 + 2·2" over "= 6"
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;font-size:${SIZE}px;line-height:${Math.round(SIZE * 1.25)}px;white-space:pre;color:${css(COL.dim)};font-variant-numeric:tabular-nums;`;
    const l1 = document.createElement("div"), l2 = document.createElement("div");
    el.appendChild(l1); el.appendChild(l2); root.appendChild(el);
    const sp = (row, t, col) => { const s = document.createElement("span"); s.textContent = t; if (col) s.style.color = css(col); row.appendChild(s); return s; };
    const qa = Q[HERO.r], ka = K[HERO.c];
    const q0 = sp(l1, fmtv(qa[0]), SLOT[HERO.r]); const dot0 = sp(l1, "·"); const k0 = sp(l1, fmtv(ka[0]), SLOT[HERO.c]);
    const plus = sp(l1, " + ");
    const q1 = sp(l1, fmtv(qa[1]), SLOT[HERO.r]); const dot1 = sp(l1, "·"); const k1 = sp(l1, fmtv(ka[1]), SLOT[HERO.c]);
    const eq = sp(l2, "= "); const res = sp(l2, fmtv(S[HERO.r][HERO.c]), COL.hero);
    const read = { el, l1, l2, q: [q0, q1], k: [k0, k1], ops: [dot0, plus, dot1], eq, res };
    const tips = { name: lbl(root, TOK[HERO.r], { col: SLOT[HERO.r], width: 180 }), is: lbl(root, TOK[HERO.c], { col: SLOT[HERO.c], width: 120 }) };
    const hl = { q: VEC.hbox(root), k: VEC.hbox(root), rows: [VEC.hbox(root), VEC.hbox(root), VEC.hbox(root)] };
    return { cards, words, heads, m, b, names, shape, div, sums, read, tips, hl };
  }

  // ---- placement ----
  const placeCard = (card, a = 1, o = {}) => card.at(VEC.centreLeft(card.el), CARD_TOP, { alpha: a, scale: o.scale });
  // one matrix (X / Q / K / WQ / WK) at its slot; o: alpha, col (digits; default its own), name alpha
  function placeM(Pt, key, a = 1, o = {}) {
    const left = { X: LL, Q: LL, K: RL, WQ: RL, WK: RL }[key], rows = Pt.m[key].length;
    Pt.m[key].forEach((row, r) => row.forEach((c, k) => {
      c.at(left + k * CW, rowTop(r), { alpha: a }); c.color(o.col || c.col0); c.border(COL.hero, 0);
    }));
    Pt.b[key].at(0, 0, { alpha: a }); Pt.b[key].color(o.bcol || COL.dim);
    put(Pt.names[key], left + CW - 100, NAME_TOP, o.na == null ? a : o.na, o.ncol || COL.dim);
    return rows;
  }
  // the score grid: vals (3 x 3 text), alpha, the hero cell's colour
  function placeGrid(Pt, vals, a = 1, o = {}) {
    Pt.m.S.forEach((row, r) => row.forEach((c, k) => {
      c.set(vals[r][k]); c.at(GL + k * GCW, rowTop(r), { alpha: a });
      c.color(r === HERO.r && k === HERO.c ? (o.heroCol || COL.hero) : COL.text); c.border(COL.hero, 0);
    }));
    Pt.b.S.at(0, 0, { alpha: a }); Pt.b.S.color(COL.dim);
  }
  const placeWords = (Pt, a = 1) => Pt.words.forEach((el, r) => put(el, WORD_RIGHT - 200, rowTop(r) + 3, a));
  const placeHeads = (Pt, a = 1) => Pt.heads.forEach((el, c) => put(el, colMid(c) - (GCW + 40) / 2, NAME_TOP, a));
  const placeSums = (Pt, a = 1) => Pt.sums.forEach((el, r) => put(el, SIDE, rowTop(r) + 3, a));
  const placeRead = (Pt, a = 1) => put(Pt.read.el, READ.left, READ.top, a);
  // tip labels beside the pair's arrow tips (grid points), o: alpha, scale
  function placeTips(Pt, a = 1, o = {}) {
    VEC.view(PLANE);
    VEC.place(Pt.tips.name, Q[HERO.r][0], Q[HERO.r][1], { dx: -150, dy: 34, alpha: a, scale: o.scale });
    VEC.place(Pt.tips.is, K[HERO.c][0], K[HERO.c][1], { dx: 92, dy: 10, alpha: a, scale: o.scale });
  }
  // highlight-box rects: a row of the left (Q) or right (K) slot, or a grid row
  const RECT = {
    q: (r) => [LL - 14, rowTop(r) - 4, 2 * CW + 28, RH + 8],
    k: (r) => [RL - 14, rowTop(r) - 4, 2 * CW + 28, RH + 8],
    row: (r) => [GL - 14, rowTop(r) - 4, 3 * GCW + 28, RH + 8],
    cell: (r, c) => [GL + c * GCW, rowTop(r) - 2, GCW, RH + 4],
  };
  // every DOM part hidden (a state then shows what it needs)
  function hideAll(Pt) {
    Object.values(Pt.cards).forEach((c) => placeCard(c, 0));
    Object.keys(Pt.m).forEach((k) => { if (k !== "S") placeM(Pt, k, 0); });
    placeGrid(Pt, SR, 0); placeWords(Pt, 0); placeHeads(Pt, 0); placeSums(Pt, 0); placeRead(Pt, 0); placeTips(Pt, 0);
    put(Pt.shape, SHAPE_LEFT, NAME_TOP, 0); put(Pt.div, SIDE, rowTop(1) + 3, 0);
    Pt.hl.q.rect(RECT.q(0), 0); Pt.hl.k.rect(RECT.k(0), 0); Pt.hl.rows.forEach((h, r) => h.rect(RECT.row(r), 0));
  }

  // ---- canvas ----
  // a key: an outline arrow, a little wider than a query so a query under it shows through
  // (o: alpha, u draw progress, width (default 60), head (default 90), line px)
  function keyArrow(g, a, b, col, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u), al = o.alpha == null ? 1 : o.alpha;
    if (u <= 0.001 || al <= 0.001) return;
    const p0 = VEC.at(a[0], a[1]), pb = VEC.at(b[0], b[1]);
    const x0 = p0[0], y0 = p0[1], x1 = lerp(x0, pb[0], u), y1 = lerp(y0, pb[1], u);
    const len = Math.hypot(x1 - x0, y1 - y0); if (len < 1) return;
    const dx = (x1 - x0) / len, dy = (y1 - y0) / len, nx = -dy, ny = dx;
    const hw = (o.width || 60) / 2 * VEC.THIN, hl = Math.min((o.head || 90) * 0.8, len * 0.6), hh = Math.max(hw * 2.3, 12);
    const sx = x1 - dx * hl, sy = y1 - dy * hl;
    const pts = [[x0 + nx * hw, y0 + ny * hw], [sx + nx * hw, sy + ny * hw], [sx + nx * hh, sy + ny * hh], [x1, y1],
      [sx - nx * hh, sy - ny * hh], [sx - nx * hw, sy - ny * hw], [x0 - nx * hw, y0 - ny * hw]];
    g.save(); g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); g.closePath();
    g.strokeStyle = css(col, 1, al); g.lineWidth = o.line || 6; g.lineJoin = "round"; g.stroke(); g.restore();
  }
  const qArrow = (g, p, col, o = {}) => VEC.arrow(g, [0, 0], p, { col, alpha: o.alpha, u: o.u });
  const lerp2 = (a, b, u) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u)];
  function bg(g) { g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }
  // The plane, under everything. o: x / ghost / q / k: per-token alpha arrays (0 = off),
  // xPos / qPos / kPos: per-token grid points (default X / Q / K), kCol: key colours,
  // after(g): extra drawing inside the plane's clip, on top. Draw order: ghosts, X,
  // queries, then keys (outlines) on top.
  function plane(g, o = {}) {
    VEC.view(PLANE);
    bg(g);
    g.save(); g.beginPath(); g.rect(0, PLANE.top, ISO.W, ISO.SAFE.stageBottom - PLANE.top); g.clip();
    VEC.floor(g); VEC.axes(g);
    const each = (arr, fn) => (arr || []).forEach((a, i) => { if (a > 0.001) fn(a, i); });
    each(o.ghost, (a, i) => qArrow(g, X[i], COL.muted, { alpha: a }));
    each(o.x, (a, i) => qArrow(g, (o.xPos || X)[i], SLOT[i], { alpha: a, u: o.xU }));
    each(o.q, (a, i) => qArrow(g, (o.qPos || Q)[i], SLOT[i], { alpha: a }));
    each(o.k, (a, i) => keyArrow(g, [0, 0], (o.kPos || K)[i], (o.kCol || SLOT)[i], { alpha: a }));
    VEC.puck(g, 0, 0);
    if (o.after) o.after(g);
    g.restore();
  }

  // ---- the rest states (storyboard.md "States") ----
  const PAIR_Q = [ALPHA_OFF, 1, ALPHA_OFF], PAIR_K = [ALPHA_OFF, ALPHA_OFF, 1];
  const PULL_K = WN.map((w) => 0.15 + 0.85 * w);
  const PLANES = {
    GRID: { q: PAIR_Q, k: PAIR_K }, WEIGHTS: { q: PAIR_Q, k: PAIR_K }, PULL: { q: PAIR_Q, k: PULL_K },
    TOKENS: { x: [1, 1, 1] }, QUERIES: { ghost: [0.5, 0.5, 0.5], q: [1, 1, 1] },
    QK: { q: [1, 1, 1], k: [1, 1, 1] }, PAIR: { q: PAIR_Q, k: PAIR_K },
  };
  function state(Pt, g, name) {
    hideAll(Pt);
    const grid = ["GRID", "WEIGHTS", "PULL"].includes(name);
    placeWords(Pt, 1);
    if (grid) {
      placeCard(Pt.cards[name === "GRID" ? "s" : "w"], 1);
      placeHeads(Pt, 1);
      placeGrid(Pt, name === "GRID" ? SR : WT, 1);
      put(Pt.shape, SHAPE_LEFT, NAME_TOP, 1);
      if (name !== "GRID") placeSums(Pt, 1);
      if (name === "PULL") Pt.hl.rows[HERO.r].rect(RECT.row(HERO.r), 1, COL.dim);
      placeTips(Pt, 1);
    } else if (name === "TOKENS") {
      placeM(Pt, "X", 1);
    } else if (name === "QUERIES") {
      placeCard(Pt.cards.q, 1); placeM(Pt, "Q", 1);
    } else {                                              // QK, PAIR
      placeCard(Pt.cards.k, 1); placeM(Pt, "Q", 1); placeM(Pt, "K", 1);
      if (name === "PAIR") {
        Pt.hl.q.rect(RECT.q(HERO.r), 1, COL.dim); Pt.hl.k.rect(RECT.k(HERO.c), 1, COL.dim);
        placeTips(Pt, 1); placeRead(Pt, 1);
      }
    }
    if (g) plane(g, PLANES[name]);
  }

  window.EP = {
    TOK, X, WQ, WK, Q, K, S, SR, SS, WT, WN, HERO, D, CODE,
    CARD_TOP, NAME_TOP, MAT_TOP, RH, CW, SIZE, WORD_RIGHT, LL, RL, GL, GCW, SIDE, SHAPE_LEFT, PLANE, READ, ALPHA_OFF,
    PAIR_Q, PAIR_K, PULL_K, PLANES, RECT, rowTop, colMid,
    parts, put, placeCard, placeM, placeGrid, placeWords, placeHeads, placeSums, placeRead, placeTips, hideAll,
    keyArrow, qArrow, lerp2, bg, plane, state,
  };
})();
