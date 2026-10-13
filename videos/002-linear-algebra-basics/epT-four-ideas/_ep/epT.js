// epT.js — the trailer's numbers, layout and rest states (Linear Algebra for AI
// Engineers: the four ideas). Linked into each beat as `ep/`, after
// vendor/gsap, iso/iso.js and vec/vec.js:   ln -s ../_ep NN_beat/ep
// Everything is drawn with the shared plane kit (VEC); this file holds the
// ledger (storyboard.md), where things sit, the camera views and the states
// beats open and end on. Beats never edit it; they draw changes on top of a state.
(function () {
  const { COL, css, lerp, clamp01, mix, hash } = ISO;
  const { fmtv, SLOT } = VEC;
  const GOLD = SLOT[2];
  const BASIS = COL.dim;                             // e1, e2 (and where they land): grey-lavender, never a row colour,
                                                     // so they don't read as the teal / blue recipe legs (Chris, first watch)

  // ---- the ledger (storyboard.md) ----
  // Row-vector (PyTorch) convention: x @ W, row i of W is where e_i lands. ep03's numbers.
  const X = [3, 2];                                  // the vector: 3 of e1 plus 2 of e2
  const W = [[1, 0.5], [-0.5, 1.25]];                // row 1 = where e1 lands, row 2 = where e2 lands
  const XW = [2, 4];                                 // x @ W = 3·(1, 0.5) + 2·(−0.5, 1.25)
  const ROWS_W = [[3, 1.5], [-1, 2.5]];              // the weighted rows: 3 × row 1, 2 × row 2
  // the dot product (beat 6): a fixed, b turns from aligned to opposed; |a| = |b|, a · b runs 5 → 0 → −5
  const A = [2, 1];
  const B_TURN = [0, Math.PI];                       // angle of b relative to a: start, end
  // attention (beat 7): one token's query q (= a) against three tokens' keys
  const Q = A;
  const TOKENS = ["the", "cat", "sat"];
  const KEYS = [[-1, 2], [1, 2], [1, -1]];           // q · k = 0, 4, 1
  const SCORES = [0, 4, 1];
  const BEST = 1;                                    // "cat": the brightest score, the hero
  // learning (beats 8-9): three layers, W1 trained by three moves, p @ AMP @ IGN @ MIX
  const IDENT = [[1, 0], [0, 1]];
  const AMP = [[2, 0], [0, 1]];                      // amplify e1
  const IGN = [[1, 0], [0, 0.2]];                    // (almost) ignore e2
  const MIX = [[1, 0.5], [0, 1]];                    // mix: output 2 takes some of input 1
  const W1T = [[2, 1], [0, 0.2]];                    // AMP @ IGN @ MIX, the trained W1
  const RING = 16;                                   // dots on the unit circle
  // the easier task (beat 10): two classes split by a thin diagonal gap; the learned
  // move widens the gap and turns it upright. q = p @ EASY.
  const R2 = Math.SQRT1_2;
  const EASY = [[4 * R2, 0.5 * R2], [4 * R2, -0.5 * R2]];
  const CLASSES = (() => {
    const pts = [];
    for (let i = 0; i < 7; i++) {
      const a = -2.4 + i * 0.8;
      [1, -1].forEach((sgn, c) => {
        const b = sgn * (0.12 + 0.16 * hash(i * 7 + c * 3 + 1)), aa = a + sgn * 0.4 + 0.2 * (hash(i + 11 * c) - 0.5);
        pts.push({ p: [R2 * (aa + b), R2 * (b - aa)], c });       // p = aa·t + b·n, t = (1, −1)/√2, n = (1, 1)/√2
      });
    }
    return pts;                                                    // c 0 = teal, c 1 = gold
  })();

  // ---- layout (px, 1080 x 1920; stage y 230-1100) ----
  const NAME_TOP = 236, ROW_TOP = 312, RH = 76, SIZE = 64;
  const XL = { left: 110, cw: 100, comma: 0 };      // x = [ 3, 2 ], top left ("3," carries its comma, as the sum row does)
  const WL = { left: 600, cw: 160 };                 // W (2, 2), top right
  const SUM_TOP = ROW_TOP + 2 * RH + 16;             // [ 2, 4 ] under W (beat 5)
  const WEIGHT_LEFT = 420;                           // "3 ×", "2 ×" left of W's rows (beat 5)
  const CODE_TOP = 1115;                             // the code card, band top (captions anchored bottom)
  const LAYER = { lefts: [95, 400, 705], cw: 110 };  // W1 W2 W3 (beats 8-9)
  // views
  const MAIN = { step: 120, ox: 320, oy: 1070, ax: { w: -1.4, e: 4.3, s: -0.25, n: 4.3 }, top: 566 };
  const CENTER = { step: 140, ox: 507, oy: 800, ax: { w: -2.5, e: 2.5, s: -2.1, n: 2.5 }, top: 470 };
  const PLANE_CLIP = (v) => [0, v.top, ISO.W, ISO.SAFE.stageBottom - v.top];
  // the hook's four tiles: [left, top, w, h] and a camera each
  const TW = 430, TH = 400, TG = 25;
  const TR = [[65, 240], [65 + TW + TG, 240], [65, 240 + TH + TG], [65 + TW + TG, 240 + TH + TG]].map(([l, t]) => [l, t, TW, TH]);
  const TILE_VIEWS = [
    { step: 70, ox: TR[0][0] + 95, oy: TR[0][1] + 260, ax: { w: -1, e: 4.2, s: -0.6, n: 3 } },
    { step: 125, ox: TR[1][0] + 215, oy: TR[1][1] + 230, ax: { w: -1.4, e: 1.6, s: -0.6, n: 1.6 } },
    { step: 58, ox: TR[2][0] + 120, oy: TR[2][1] + 290, ax: { w: -1.6, e: 4.8, s: -0.7, n: 4.4 } },
    { step: 68, ox: TR[3][0] + 215, oy: TR[3][1] + 180, ax: { w: -2.6, e: 2.6, s: -2.2, n: 2.4 } },
  ];
  const TILE_LABELS = ["vector", "matrix", "x @ W", "dot product"];

  // ---- DOM parts, made once per beat ----
  const lab = (root, text, o = {}) => ISO.label(root, text, { size: o.size || SIZE, color: css(o.col || COL.dim), width: o.width || 200, align: o.align || "center" });
  function parts(root) {
    // x = [ 3, 2 ]
    const xc = X.map((v, i) => VEC.cell(root, fmtv(v) + (i === 0 ? "," : ""), { left: XL.left + i * (XL.cw + XL.comma), top: ROW_TOP, width: XL.cw, height: RH, size: SIZE, col: SLOT[i] }));
    const xRight = XL.left + 2 * XL.cw + XL.comma;
    const xb = VEC.brackets(root, XL.left, ROW_TOP, xRight, RH);
    const xName = lab(root, "x", { width: xRight - XL.left });
    // W (2, 2)
    const wc = VEC.grid(root, W, WL.left, ROW_TOP, { cellW: WL.cw, rowH: RH, size: SIZE });
    const wb = VEC.brackets(root, WL.left, ROW_TOP, WL.left + 2 * WL.cw, 2 * RH);
    const wName = lab(root, "W", { width: 70, align: "left" });
    const wShape = lab(root, "(2, 2)", { width: 220, align: "left" });
    // beat 5: weights beside W's rows, the sum under W, its code label
    const weights = X.map((v, i) => VEC.cell(root, `${fmtv(v)} ×`, { left: WEIGHT_LEFT, top: ROW_TOP + i * RH, width: 140, height: RH, size: SIZE, col: SLOT[i] }));
    const sum = XW.map((v, i) => VEC.cell(root, fmtv(v) + (i === 0 ? "," : ""), { left: WL.left + i * WL.cw, top: SUM_TOP, width: WL.cw, height: RH, size: SIZE, col: COL.hero }));
    const sb = VEC.brackets(root, WL.left, SUM_TOP, WL.left + 2 * WL.cw, RH, { col: COL.hero });
    const sumName = lab(root, "x @ W", { width: 260, align: "right" }); VEC.code(sumName);
    const card = VEC.codeCard(root, [[["y = "], ["x", COL.data], [" @ "], ["W"]]]);
    // beats 6-7: the dot readout, the token scores
    const dotName = lab(root, "a · b =", { width: 300, align: "right" });
    const dotVal = VEC.cell(root, "5", { left: 600, top: 250, width: 170, height: RH, size: 72, col: COL.text });
    const scoreName = lab(root, "q · k", { width: 220, align: "left" });
    const tokens = TOKENS.map((w) => lab(root, w, { col: GOLD, width: 180 }));
    const scores = SCORES.map((v) => VEC.cell(root, fmtv(v), { width: 180, height: RH, size: SIZE, col: COL.text }));
    // arrow-tip labels on the plane
    const tip = { e1: lab(root, "e1", { col: BASIS, width: 100 }), e2: lab(root, "e2", { col: BASIS, width: 100 }),
      a: lab(root, "a", { col: SLOT[0], width: 80 }), b: lab(root, "b", { col: SLOT[1], width: 80 }), q: lab(root, "q", { col: SLOT[0], width: 80 }),
      keys: TOKENS.map((w) => lab(root, w, { col: GOLD, width: 140 })) };
    // beats 8-9: three layers
    const layers = [0, 1, 2].map((k) => {
      const left = LAYER.lefts[k];
      const cells = VEC.grid(root, IDENT, left, ROW_TOP, { cellW: LAYER.cw, rowH: RH, size: SIZE, rowCol: [COL.text, COL.text] });
      const br = VEC.brackets(root, left, ROW_TOP, left + 2 * LAYER.cw, 2 * RH);
      const name = lab(root, `W${k + 1}`, { width: 2 * LAYER.cw });
      return { left, cells, br, name };
    });
    // the hook's tile labels
    const tileLab = TILE_LABELS.map((s, i) => { const el = lab(root, s, { col: COL.text, width: TW - 20, size: 60 }); if (i === 2) VEC.code(el); return el; });
    return { xc, xb, xName, wc, wb, wName, wShape, weights, sum, sb, sumName, card, dotName, dotVal, scoreName, tokens, scores, tip, layers, tileLab,
      hl: VEC.hbox(root), hl2: VEC.hbox(root) };
  }

  // ---- placement ----
  const put = (el, left, top, alpha = 1) => {
    el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px)`;
    el.style.opacity = clamp01(alpha).toFixed(3);
  };
  // the strip's parts, each with an alpha (0 hides); call once per frame from state()
  function strip(P, o = {}) {
    const xa = o.x || 0, wa = o.w || 0, ba = o.beat5 || 0, da = o.dot || 0, sa = o.scores || 0, la = o.layers || 0;
    P.xc.forEach((c, i) => { c.home({ alpha: xa }); c.color(SLOT[i]); c.border(COL.hero, 0); });
    P.xb.at(0, 0, { alpha: xa }); P.xb.color(COL.dim);
    put(P.xName, XL.left, NAME_TOP, xa);
    P.wc.forEach((row, r) => row.forEach((c) => { c.home({ alpha: wa }); c.color(SLOT[r]); c.border(COL.hero, 0); }));
    P.wb.at(0, 0, { alpha: wa }); P.wb.color(COL.dim);
    put(P.wName, WL.left, NAME_TOP, wa); put(P.wShape, WL.left + 80, NAME_TOP, wa);
    P.weights.forEach((c) => c.home({ alpha: ba }));
    P.sum.forEach((c) => { c.home({ alpha: ba }); c.color(COL.hero); });
    P.sb.at(0, 0, { alpha: ba }); P.sb.color(COL.hero);
    put(P.sumName, WL.left - 330, SUM_TOP + 2, ba);
    P.card.at(VEC.centreLeft(P.card.el), CODE_TOP, { alpha: o.card || 0 });
    put(P.dotName, 280, 252, da); P.dotVal.at(600, 250, { alpha: da }); P.dotVal.color(COL.hero);
    put(P.scoreName, 90, ROW_TOP + 2, sa);
    TOKENS.forEach((_, i) => {
      const left = 380 + i * 190;
      put(P.tokens[i], left, NAME_TOP, sa); P.scores[i].at(left, ROW_TOP, { alpha: sa });
      P.scores[i].color(i === BEST ? COL.hero : COL.text); P.scores[i].border(COL.hero, 0);
    });
    P.layers.forEach((L) => {
      L.cells.forEach((row) => row.forEach((c) => { c.home({ alpha: la }); c.color(COL.text); c.border(COL.hero, 0); }));
      L.br.at(0, 0, { alpha: la }); L.br.color(COL.dim); put(L.name, L.left, NAME_TOP, la);
    });
    P.tileLab.forEach((el) => put(el, 0, 0, 0));
    Object.values(P.tip).flat().forEach((el) => put(el, 0, 0, 0));
    P.hl.rect([0, 0, 10, 10], 0); P.hl2.rect([0, 0, 10, 10], 0);
  }
  // set a layer's digits from a 2x2 matrix (rounded to 1 decimal)
  function setLayer(L, M, col = COL.text) {
    L.cells.forEach((row, r) => row.forEach((c, k) => { c.set(fmtv(Math.round(M[r][k] * 10) / 10)); c.color(col); }));
  }
  // highlight rects
  const RECT = {
    x: () => [XL.left - 34, ROW_TOP - 12, 2 * XL.cw + XL.comma + 68, RH + 24],
    xslot: (i) => [XL.left + i * (XL.cw + XL.comma) - 6, ROW_TOP - 4, XL.cw + 12, RH + 8],
    W: () => [WL.left - 34, ROW_TOP - 12, 2 * WL.cw + 68, 2 * RH + 24],
    wrow: (r) => [WL.left - 12, ROW_TOP + r * RH - 4, 2 * WL.cw + 24, RH + 8],
    layer: (k) => [LAYER.lefts[k] - 34, ROW_TOP - 12, 2 * LAYER.cw + 68, 2 * RH + 24],
    score: (i) => [380 + i * 190 - 6, ROW_TOP - 4, 192, RH + 8],
    tile: (i) => TR[i],
  };

  // ---- canvas ----
  function bg(g) { g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }
  // the square grid of the current camera, inside the current clip
  function grid(g, alpha = 0.42) {
    if (alpha <= 0.001) return;
    const C = VEC.CAM, n = Math.ceil(Math.max(ISO.W, ISO.H) / C.step) + 1;
    g.save(); g.strokeStyle = `rgba(74, 80, 112, ${alpha})`; g.lineWidth = 3; g.beginPath();
    for (let k = -n; k <= n; k++) {
      const x = C.ox + k * C.step, y = C.oy + k * C.step;
      g.moveTo(x, 0); g.lineTo(x, ISO.H); g.moveTo(0, y); g.lineTo(ISO.W, y);
    }
    g.stroke(); g.restore();
  }
  function clip(g, r, radius = 0) {
    g.beginPath();
    if (radius && g.roundRect) g.roundRect(r[0], r[1], r[2], r[3], radius); else g.rect(r[0], r[1], r[2], r[3]);
    g.clip();
  }
  const rectLerp = (a, b, u) => a.map((v, i) => lerp(v, b[i], clamp01(u)));
  // a recipe: tip-to-tail legs from the origin, with a small dot at every whole hop.
  // legs: [[vector, count, colour], ...] (o: alpha, u 0..1 draw progress over all hops)
  function recipe(g, legs, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    const total = legs.reduce((s, l) => s + l[1], 0), done = (o.u == null ? 1 : clamp01(o.u)) * total;
    let p = [0, 0], k = 0;
    legs.forEach(([v, n, col]) => {
      for (let j = 0; j < n; j++, k++) {
        const u = clamp01(done - k);
        if (u <= 0) return;
        const q = [p[0] + v[0], p[1] + v[1]];
        VEC.arrow(g, p, q, { col, alpha: al, u, width: 34, head: 60 });
        p = q;
      }
    });
  }
  const LEGS_OLD = [[[1, 0], 3, SLOT[0]], [[0, 1], 2, SLOT[1]]];
  const LEGS_NEW = [[W[0], 3, SLOT[0]], [W[1], 2, SLOT[1]]];
  // The MAIN plane. o: alpha, grid (standard grid alpha factor), s (e1, e2 swing to W's rows 0..1),
  // lattice (moved-grid alpha), ghosts (muted unit arrows at home), e (landed / unit arrows alpha),
  // spots (magenta landing rings alpha), old (old recipe legs alpha), oldU, xA (x arrow alpha), xCol,
  // nu (new recipe legs alpha), newU, out (x @ W arrow alpha), outCol, view (default MAIN), clipR.
  function plane(g, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha, s = o.s || 0, Bs = VEC.basisTo(VEC.I2, W, s);
    VEC.view(o.view || MAIN);
    g.save(); clip(g, o.clipR || PLANE_CLIP(MAIN), o.radius || 0);
    grid(g, 0.42 * al * lerp(1, 0.33, clamp01(o.lattice == null ? 0 : o.lattice / 0.35)) * (o.grid == null ? 1 : o.grid));
    if (o.lattice) VEC.lattice(g, Bs, { alpha: o.lattice * al });
    VEC.axes(g, { alpha: al });
    if (o.ghosts) { VEC.arrow(g, [0, 0], [1, 0], { col: COL.muted, alpha: o.ghosts * al }); VEC.arrow(g, [0, 0], [0, 1], { col: COL.muted, alpha: o.ghosts * al }); }
    recipe(g, LEGS_OLD, { alpha: (o.old || 0) * al, u: o.oldU });
    if (o.xA) VEC.arrow(g, [0, 0], X, { col: o.xCol || COL.text, alpha: o.xA * al });
    const ea = o.e == null ? 1 : o.e;
    if (ea > 0.001) { VEC.arrow(g, [0, 0], Bs[0], { col: BASIS, alpha: ea * al }); VEC.arrow(g, [0, 0], Bs[1], { col: BASIS, alpha: ea * al }); }
    recipe(g, LEGS_NEW, { alpha: (o.nu || 0) * al, u: o.newU });
    if (o.out) VEC.arrow(g, [0, 0], XW, { col: o.outCol || COL.hero, alpha: o.out * al });
    if (o.spots) { VEC.spot(g, Bs[0][0], Bs[0][1], { alpha: o.spots * al }); VEC.spot(g, Bs[1][0], Bs[1][1], { alpha: o.spots * al }); }
    VEC.puck(g, 0, 0, { alpha: al, half: 12 });
    g.restore();
  }
  // The CENTER plane (beats 6-10): grid + axes; the caller draws on top inside the returned clip.
  function centre(g, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    VEC.view(CENTER);
    g.save(); clip(g, PLANE_CLIP(CENTER));
    grid(g, 0.42 * al); VEC.axes(g, { alpha: al });
    return () => { VEC.puck(g, 0, 0, { alpha: al, half: 12 }); g.restore(); };
  }
  const rot = (v, th) => [v[0] * Math.cos(th) - v[1] * Math.sin(th), v[0] * Math.sin(th) + v[1] * Math.cos(th)];
  const bAt = (u) => rot(A, lerp(B_TURN[0], B_TURN[1], clamp01(u)));          // b at turn progress u
  const dot = (p, q) => p[0] * q[0] + p[1] * q[1];
  // the ring of dots through map M (o: alpha, col)
  function ring(g, M, o = {}) {
    for (let k = 0; k < RING; k++) {
      const th = (k / RING) * Math.PI * 2, q = VEC.comb([Math.cos(th), Math.sin(th)], M);
      VEC.puck(g, q[0], q[1], { half: 13, col: o.col || COL.data, alpha: o.alpha == null ? 1 : o.alpha });
    }
  }
  const mlerp = (P0, P1, u) => VEC.basisTo(P0, P1, clamp01(u));
  const mmul = (P0, P1) => [VEC.comb(P0[0], P1), VEC.comb(P0[1], P1)];
  // the two classes through map M; line: alpha of the boundary (the image of the gap line)
  function classes(g, M, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (o.line) {
      const t = VEC.comb([R2, -R2], M), k = 6;
      VEC.line(g, [-t[0] * k, -t[1] * k], [t[0] * k, t[1] * k], { col: COL.hero, alpha: o.line * al, width: 7, dash: [22, 14] });
    }
    CLASSES.forEach(({ p, c }) => { const q = VEC.comb(p, M); VEC.puck(g, q[0], q[1], { half: 15, col: c ? GOLD : COL.data, alpha: al }); });
  }

  // ---- the hook's tiles ----
  // tile i's mini-world at progress u (0 = start of its motion, 1 = rest). o: alpha, lit (0..1 magenta)
  function tile(g, P, i, u, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha, lit = o.lit || 0, r = TR[i];
    if (al <= 0.001) return;
    g.save(); clip(g, r, 26); g.fillStyle = css(COL.panel, 1, al); g.fillRect(r[0], r[1], r[2], r[3]);
    VEC.view(TILE_VIEWS[i]); grid(g, 0.42 * al); VEC.axes(g, { alpha: al });
    const E = ISO.E(), heroCol = (base) => mix(base, COL.hero, lit);
    if (i === 0) {                                     // vector: the recipe legs, then x
      recipe(g, LEGS_OLD, { alpha: al, u: seg01(u, 0, 0.7) });
      VEC.arrow(g, [0, 0], X, { col: heroCol(COL.text), alpha: al, u: E.out(seg01(u, 0.55, 1)) });
    } else if (i === 1) {                              // matrix: e1, e2 swing to W's rows
      const s = E.io(seg01(u, 0, 0.85)), Bs = VEC.basisTo(VEC.I2, W, s);
      VEC.arrow(g, [0, 0], [1, 0], { col: COL.muted, alpha: al }); VEC.arrow(g, [0, 0], [0, 1], { col: COL.muted, alpha: al });
      VEC.arrow(g, [0, 0], Bs[0], { col: BASIS, alpha: al }); VEC.arrow(g, [0, 0], Bs[1], { col: BASIS, alpha: al });
      const sp = seg01(u, 0.8, 1) * lit;
      VEC.spot(g, Bs[0][0], Bs[0][1], { alpha: sp * al, r: 22 }); VEC.spot(g, Bs[1][0], Bs[1][1], { alpha: sp * al, r: 22 });
    } else if (i === 2) {                              // x @ W: the new recipe, then the output
      recipe(g, LEGS_NEW, { alpha: al, u: seg01(u, 0, 0.7) });
      VEC.arrow(g, [0, 0], XW, { col: heroCol(COL.text), alpha: al, u: E.out(seg01(u, 0.55, 1)) });
    } else {                                           // dot product: b turns against a
      const b = rot(A, lerp(-0.15, 1.1, E.io(u)));           // rests ~63° past a, so the two read apart
      VEC.arrow(g, [0, 0], A, { col: SLOT[0], alpha: al });
      VEC.arrow(g, [0, 0], b, { col: heroCol(SLOT[1]), alpha: al });
    }
    VEC.puck(g, 0, 0, { alpha: al, half: 9 });
    g.restore();
    // the frame
    g.save(); g.beginPath();
    if (g.roundRect) g.roundRect(r[0] + 3, r[1] + 3, r[2] - 6, r[3] - 6, 24); else g.rect(r[0] + 3, r[1] + 3, r[2] - 6, r[3] - 6);
    g.strokeStyle = css(mix(COL.muted, COL.hero, lit), 1, al); g.lineWidth = 6; g.stroke(); g.restore();
    put(P.tileLab[i], r[0] + 10, r[1] + r[3] - 88, al);
    P.tileLab[i].style.color = css(mix(COL.text, COL.hero, lit));
  }
  const seg01 = (u, a, b) => clamp01((u - a) / (b - a));

  // ---- the rest states (storyboard.md "States") ----
  // TILES   : the four tiles at rest (no magenta).
  // VECTOR  : MAIN; strip x; plane: e1, e2 at home, the old recipe legs, x (off-white).
  // LANDED  : strip x, W; plane: e1, e2 landed (ghosts at home), lattice, magenta spots; old recipe + x muted.
  // REBUILT : LANDED without spots; the new recipe legs and x @ W (magenta); x's ghost muted.
  // CODE    : REBUILT + weights "3 ×", "2 ×", the sum [ 2, 4 ] (magenta), the card `y = x @ W`.
  // DOT     : CENTER; readout a · b = −5 (magenta); a (teal), b (blue) opposed.
  // ATTN    : CENTER; q (teal), three keys (gold, "cat" magenta) with token tips; strip: tokens, scores (4 magenta).
  // LAYERS  : CENTER; strip W1 W2 W3 = identity (white); the ring of dots; a magenta box on W1.
  // TRAINED : LAYERS with W1 = W1T (magenta digits), W2, W3 dimmed; the ring through W1T with
  //           e1, e2 at W1T's rows.
  // EASY    : CENTER; the two classes moved by EASY, the magenta gap line upright. Strip empty.
  // CANON   : the last frame. MAIN; strip x, W; plane: lattice, e1 e2 landed, x's ghost, x @ W (magenta).
  function state(P, g, name) {
    strip(P, {
      x: ["VECTOR", "LANDED", "REBUILT", "CODE", "CANON"].includes(name) ? 1 : 0,
      w: ["LANDED", "REBUILT", "CODE", "CANON"].includes(name) ? 1 : 0,
      beat5: name === "CODE" ? 1 : 0, card: name === "CODE" ? 1 : 0,
      dot: name === "DOT" ? 1 : 0, scores: name === "ATTN" ? 1 : 0,
      layers: ["LAYERS", "TRAINED"].includes(name) ? 1 : 0,
    });
    if (name === "DOT") P.dotVal.set(fmtv(Math.round(dot(A, bAt(1)))));
    P.layers.forEach((L) => setLayer(L, IDENT));
    if (!g) return;
    bg(g);
    if (name === "TILES") { [0, 1, 2, 3].forEach((i) => tile(g, P, i, 1)); return; }
    const M = {
      VECTOR: { s: 0, e: 1, old: 1, xA: 1 },
      LANDED: { s: 1, e: 1, ghosts: 1, lattice: 0.35, spots: 1, old: 0.35, xA: 0.35, xCol: COL.muted },
      REBUILT: { s: 1, e: 1, ghosts: 1, lattice: 0.35, xA: 0.35, xCol: COL.muted, nu: 1, out: 1 },
      CANON: { s: 1, e: 1, ghosts: 1, lattice: 0.35, xA: 0.35, xCol: COL.muted, out: 1 },
    };
    if (name === "CODE") { plane(g, M.REBUILT); return; }
    if (M[name]) {
      plane(g, M[name]);
      if (name === "VECTOR") { tipLabel(P.tip.e1, [1.3, 0], 0, -52); tipLabel(P.tip.e2, [0, 1], -70, 0); }
      return;
    }
    const done = centre(g);
    if (name === "DOT") {
      const b = bAt(1);
      VEC.arrow(g, [0, 0], A, { col: SLOT[0] }); VEC.arrow(g, [0, 0], b, { col: SLOT[1] });
      done(); tipLabel(P.tip.a, A, 50, -40); tipLabel(P.tip.b, b, -50, -40);
    } else if (name === "ATTN") {
      KEYS.forEach((k, i) => VEC.arrow(g, [0, 0], k, { col: i === BEST ? COL.hero : GOLD }));
      VEC.arrow(g, [0, 0], Q, { col: SLOT[0] });
      done(); tipLabel(P.tip.q, Q, 55, 10);
      KEYS.forEach((k, i) => { tipLabel(P.tip.keys[i], k, KEY_DX[i][0], KEY_DX[i][1]); P.tip.keys[i].style.color = css(i === BEST ? COL.hero : GOLD); });
    } else if (name === "LAYERS") {
      ring(g, IDENT); done(); P.hl.rect(RECT.layer(0), 1);
    } else if (name === "TRAINED") {
      ring(g, W1T);
      VEC.arrow(g, [0, 0], W1T[0], { col: BASIS }); VEC.arrow(g, [0, 0], W1T[1], { col: BASIS });
      done(); setLayer(P.layers[0], W1T, COL.hero); P.hl.rect(RECT.layer(0), 1);
      P.layers.slice(1).forEach((L) => { L.cells.flat().forEach((c) => c.color(COL.dim)); });
    } else if (name === "EASY") {
      classes(g, EASY, { line: 1 }); done();
    }
  }
  const KEY_DX = [[-30, -60], [30, -60], [70, 10]];
  function tipLabel(el, p, dx, dy, alpha = 1) {
    const [sx, sy] = VEC.at(p[0], p[1]), wd = parseFloat(el.style.width) || 100;
    put(el, sx - wd / 2 + dx, sy - SIZE * 0.55 + dy, alpha);
  }

  window.EP = {
    X, W, XW, ROWS_W, BASIS, A, B_TURN, Q, TOKENS, KEYS, SCORES, BEST, IDENT, AMP, IGN, MIX, W1T, RING, EASY, CLASSES, GOLD,
    NAME_TOP, ROW_TOP, RH, SIZE, XL, WL, SUM_TOP, WEIGHT_LEFT, CODE_TOP, LAYER, MAIN, CENTER, PLANE_CLIP, TR, TILE_VIEWS, TILE_LABELS,
    LEGS_OLD, LEGS_NEW, KEY_DX,
    parts, put, strip, setLayer, RECT, bg, grid, clip, rectLerp, recipe, plane, centre, rot, bAt, dot, ring, mlerp, mmul, classes,
    tile, seg01, state, tipLabel,
  };
})();
