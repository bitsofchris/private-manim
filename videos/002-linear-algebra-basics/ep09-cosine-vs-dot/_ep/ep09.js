// ep09.js — episode 9's numbers, layout and rest states (dot, cosine, projection).
// Linked into each beat as `ep/`, after vendor/gsap, iso/iso.js and vec/vec.js:
//   ln -s ../_ep NN_beat/ep
// Everything drawn comes from the shared plane kit (VEC); this file only holds
// the ledger (storyboard.md), where things sit, and the states beats open and
// end on. Beats never edit it; they draw their changes on top of a state.
(function () {
  const { COL, css, lerp, clamp01 } = ISO;
  const { SLOT } = VEC;

  // ---- the ledger (storyboard.md) ----
  const U = [1.5, 2];                 // the vector being compared: |u| = 2.5
  const V = [2, 0];                   // the target direction: |v| = 2 (lies along e1)
  const LEN_U = 2.5, LEN_V = 2;
  const UHAT = [0.6, 0.8], VHAT = [1, 0];             // both lengths divided out
  const USMALL = [0.75, 1];           // beat 5: u at half length, its shadow 0.75
  // u · v = 1.5 × 2 + 2 × 0 = 3;  cos = 3 ÷ (2.5 × 2) = 0.6;  proj = 3 ÷ 2 = 1.5
  const VAL = { dot: "3", cos: "0.6", proj: "1.5" };
  const DERIV = { dot: "1.5 × 2 + 2 × 0", cos: "3 ÷ (2.5 × 2)", proj: "3 ÷ 2" };
  const NAMES = { dot: "dot", cos: "cos", proj: "proj" };
  const ROWS = ["dot", "cos", "proj"];
  // the code beat (beat 3, "that's what you use to compare embeddings")
  const CODE = ["F.cosine_similarity(", [["  u, v, dim=0)"], ["  # 0.6", COL.dim]]];
  const UCARD = [1.5, 2];             // beat 6: "u = [ 1.5, 2 ]"
  const UCOL = COL.data, VCOL = SLOT[1];               // u teal, v blue; the shadow is the hero

  // ---- layout (px, 1080 x 1920; stage y 230-1100, band 1100-1536) ----
  const SIZE = 64;
  const READ = { nameRight: 290, eqLeft: 312, valLeft: 380, top: [244, 324, 404], rowH: 72 };
  const PLANE = { step: 260, ox: 250, oy: 1010, ax: { w: -0.5, e: 2.55, s: -0.33, n: 2.05 }, top: 482 };
  const CARD_TOP = 1115;              // code card / u card at the band top; captions sit at the band bottom
  const ARC_R = 0.42;                 // angle arc radius (steps)

  // ---- geometry ----
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
  const len = (a) => Math.hypot(a[0], a[1]);
  const scale = (a, k) => [a[0] * k, a[1] * k];
  const lerp2 = (a, b, u) => [lerp(a[0], b[0], u), lerp(a[1], b[1], u)];
  // the shadow of u on v's line: (u · v̂) v̂
  const shadowOf = (u, v) => { const n = len(v), k = dot(u, v) / (n * n); return [v[0] * k, v[1] * k]; };

  // ---- DOM parts, made once per beat ----
  // P.rows[k] = { name, eq, val } for k in dot / cos / proj; P.hl, P.hl2 row highlight boxes;
  // P.lab = { u, v, lu, lv } arrow names and length labels; P.code (code card), P.ucard (u = [ 1.5, 2 ]).
  function parts(root) {
    const rows = {};
    ROWS.forEach((k, i) => {
      const top = READ.top[i];
      rows[k] = {
        name: ISO.label(root, NAMES[k], { size: SIZE, color: css(COL.dim), left: READ.nameRight - 220, top, width: 220, align: "right" }),
        eq: ISO.label(root, "=", { size: SIZE, color: css(COL.dim), left: READ.eqLeft, top, width: 50, align: "center" }),
        val: ISO.label(root, VAL[k], { size: SIZE, color: css(COL.text), left: READ.valLeft, top, width: 570, align: "left" }),
      };
      rows[k].val.style.fontVariantNumeric = "tabular-nums";
    });
    const lab = {
      u: VEC.label(root, "u", { color: css(UCOL), width: 80 }),
      v: VEC.label(root, "v", { color: css(VCOL), width: 80 }),
      lu: VEC.label(root, "|u| = 2.5", { color: css(UCOL), width: 340 }),
      lv: VEC.label(root, "|v| = 2", { color: css(VCOL), width: 280 }),
    };
    const code = VEC.codeCard(root, CODE);
    const ucard = VEC.vecCard(root, UCARD, { name: "u =", size: SIZE });
    return { rows, lab, code, ucard, hl: VEC.hbox(root), hl2: VEC.hbox(root) };
  }

  // ---- placement ----
  // a readout row: alpha a, value colour col (default text), value text (default VAL)
  function row(P, k, o = {}) {
    const r = P.rows[k], a = o.alpha == null ? 1 : o.alpha;
    [r.name, r.eq].forEach((el) => { el.style.opacity = a.toFixed(3); });
    r.val.style.opacity = a.toFixed(3);
    r.val.style.color = css(o.col || COL.text);
    const t = o.text == null ? VAL[k] : o.text;
    if (r.val.textContent !== t) r.val.textContent = t;
    const s = o.scale == null ? 1 : o.scale;
    r.val.style.transformOrigin = "0% 50%";
    r.val.style.transform = `scale(${s.toFixed(4)})`;
  }
  // the highlight-box rect around readout row i (covers name to value)
  const rowRect = (i, w = 560) => [READ.nameRight - 150, READ.top[i] - 6, w, READ.rowH + 12];
  const cardLeft = (el) => VEC.centreLeft(el);

  // ---- canvas ----
  function bg(g) { g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }
  // the angle arc between v and u (o: alpha, col)
  function arc(g, u, v, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    const [cx, cy] = VEC.at(0, 0), r = ARC_R * VEC.step();
    const a0 = -Math.atan2(v[1], v[0]), a1 = -Math.atan2(u[1], u[0]);
    g.save(); g.strokeStyle = css(o.col || COL.dim, 1, 0.8 * al); g.lineWidth = 6;
    g.beginPath(); g.arc(cx, cy, r, Math.min(a0, a1), Math.max(a0, a1)); g.stroke(); g.restore();
  }
  // the shadow: a magenta bar lying on v's line from the origin to p (o: u progress, alpha, col, width)
  function shadow(g, p, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u), al = o.alpha == null ? 1 : o.alpha;
    if (u <= 0.001 || al <= 0.001) return;
    VEC.line(g, [0, 0], p, { col: o.col || COL.hero, alpha: al, width: o.width || 18, u });
  }
  // the drop line: dashed, from u's tip straight down onto v's line (o: u progress, alpha)
  function drop(g, u, p, o = {}) {
    VEC.line(g, u, p, { col: COL.dim, alpha: o.alpha == null ? 0.9 : o.alpha, width: 5, dash: [14, 12], u: o.u });
  }
  // The whole plane picture. o: u, v (vectors drawn), uA, vA (arrow alpha), shadow (0..1 progress),
  // shA (shadow alpha), drop (0..1), dropA, arc (alpha), resid (alpha of the leftover arrow p -> u),
  // gridA (plane alpha).
  function plane(g, o = {}) {
    const u = o.u || U, v = o.v || V, p = shadowOf(u, v);
    VEC.view(PLANE);
    VEC.floor(g, { alpha: 0.42 * (o.gridA == null ? 1 : o.gridA) });
    VEC.axes(g, { alpha: o.gridA == null ? 1 : o.gridA });
    arc(g, u, v, { alpha: o.arc == null ? 1 : o.arc });
    VEC.arrow(g, [0, 0], v, { col: VCOL, alpha: o.vA == null ? 1 : o.vA, width: 40 });
    VEC.arrow(g, [0, 0], u, { col: UCOL, alpha: o.uA == null ? 1 : o.uA, width: 40 });
    if ((o.drop == null ? 1 : o.drop) > 0) drop(g, u, p, { u: o.drop == null ? 1 : o.drop, alpha: o.dropA });
    if (o.resid) VEC.arrow(g, p, u, { col: COL.text, alpha: o.resid, width: 40 });
    shadow(g, p, { u: o.shadow == null ? 1 : o.shadow, alpha: o.shA });
    VEC.puck(g, 0, 0);
    return p;
  }
  // arrow names at the tips, length labels beside the shafts (o: names alpha, lens alpha, u, v)
  function labels(P, o = {}) {
    const u = o.u || U, v = o.v || V, na = o.names == null ? 1 : o.names, la = o.lens == null ? 0 : o.lens;
    VEC.place(P.lab.u, u[0], u[1], { dx: 58, dy: -20, alpha: na });
    VEC.place(P.lab.v, v[0], v[1], { dx: 30, dy: -70, alpha: na });
    VEC.place(P.lab.lu, u[0] / 2, u[1] / 2, { dx: 175, dy: 50, alpha: la });
    VEC.place(P.lab.lv, v[0] / 2, v[1] / 2, { dx: 0, dy: 70, alpha: la });
  }

  // ---- the rest states (storyboard.md "States") ----
  // CANON  : u, v, the angle arc, the drop line and the magenta shadow (1.5 along v); readouts
  //          dot = 3, cos = 0.6, proj = 1.5 with proj's value magenta. Beats 1, 4, 7 end here.
  // DOT    : CANON without the drop line and shadow; length labels on; dot's value magenta. End of beat 2.
  // UNIT   : u and v at unit length (0.6, 0.8) and (1, 0); no shadow, no length labels; cos's value
  //          magenta; the code card at the band top. End of beat 3.
  // SPLIT  : CANON + the leftover arrow (1.5, 0) -> (1.5, 2) in off-white. End of beat 5.
  // COORDS : v gone; u with two magenta shadows, 1.5 on the e1 axis and 2 on the e2 axis, dashed
  //          guides from u's tip to both; readouts at 0.35; the card u = [ 1.5, 2 ] at the band top. End of beat 6.
  function state(P, g, name) {
    const R = name === "COORDS" ? 0.35 : 1;
    ROWS.forEach((k) => row(P, k, { alpha: R }));
    if (name === "CANON" || name === "SPLIT") row(P, "proj", { col: COL.hero });
    if (name === "DOT") row(P, "dot", { col: COL.hero });
    if (name === "UNIT") row(P, "cos", { col: COL.hero });
    P.hl.rect(rowRect(0), 0); P.hl2.rect(rowRect(1), 0);
    P.code.at(cardLeft(P.code.el), CARD_TOP, { alpha: name === "UNIT" ? 1 : 0 });
    P.ucard.at(cardLeft(P.ucard.el), CARD_TOP, { alpha: name === "COORDS" ? 1 : 0 });
    if (!g) return;
    bg(g);
    if (name === "UNIT") {
      plane(g, { u: UHAT, v: VHAT, drop: 0, shadow: 0 });
      labels(P, { u: UHAT, v: VHAT });
    } else if (name === "COORDS") {
      plane(g, { vA: 0, drop: 0, shadow: 0, arc: 0 });
      VEC.guides(g, U);
      shadow(g, [U[0], 0]); shadow(g, [0, U[1]]);
      labels(P, {}); P.lab.v.style.opacity = "0";
    } else {
      plane(g, { drop: name === "DOT" ? 0 : 1, shadow: name === "DOT" ? 0 : 1, resid: name === "SPLIT" ? 1 : 0 });
      labels(P, { lens: name === "DOT" ? 1 : 0 });
    }
  }

  window.EP = {
    U, V, LEN_U, LEN_V, UHAT, VHAT, USMALL, VAL, DERIV, NAMES, ROWS, CODE, UCARD, UCOL, VCOL,
    SIZE, READ, PLANE, CARD_TOP, ARC_R,
    dot, len, scale, lerp2, shadowOf,
    parts, row, rowRect, cardLeft, bg, arc, shadow, drop, plane, labels, state,
  };
})();
