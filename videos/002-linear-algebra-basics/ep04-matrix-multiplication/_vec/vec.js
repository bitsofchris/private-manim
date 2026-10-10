// vec.js — the shared parts for ep04 "What x @ W really computes" (linked
// into each beat as `vec/`, after `iso/iso.js`).
//
// Started from ep01-what-is-a-vector/_vec/vec.js (the plane, arrows, lines,
// pucks, labels); this copy adds the ledger for x @ W and the number grids,
// and fits the plane under the grids. Two halves of one stage:
//   top    (y 236–632)  the numbers: x, W, the weighted rows, the sum row
//   bottom (y 650–1100) the plane: one square = one step, east right, north up
// Everything is a pure function of its arguments.
(function () {
  const { COL, css, mix, lerp, clamp01 } = ISO;

  // ---- the ledger (storyboard.md): x = [1, 2, −1], W is 3 × 2, row-vector convention ----
  const X = [1, 2, -1];
  const W = [[2, -1], [0.5, 1], [-1, 2]];                 // row i = where input direction i lands
  const XW = [[2, -1], [1, 2], [1, -2]];                  // x[i] * row i
  const SUM = [4, -1];                                    // x @ W: the columns summed
  const B = [0.1, -0.2];                                  // the bias
  const Y = [4.1, -1.2];                                  // x @ W + b
  const CHAIN = [[0, 0], [2, -1], [3, 1], [4, -1]];       // the weighted rows tip to tail
  const ROWCOL = COL.tokens;                              // row 1 teal, row 2 blue, row 3 gold; magenta stays free
  const fmtv = (v) => (v < 0 ? "−" : "") + String(Math.abs(v));   // true minus sign; 0.5 stays 0.5

  // ---- the canonical frame ----
  // the numbers (all px, screen)
  // Matrix notation, not a table: bare numbers in a tight grid (009's readout
  // card) inside square brackets (ep01's vector card), no box per number.
  const G = {
    header: 236,          // top of the header line: the labels "x" and "W", or x written flat
    top: 316,             // top of the first grid row
    rowH: 76,             // one grid row
    cellW: 125,           // one W / weighted entry
    xLeft: 100, xW: 90,    // the x column (x turned sideways)
    wLeft: 278,           // W, two entries
    pLeft: 650,           // the weighted rows, two entries (the "products")
    sumTop: 556,          // the sum row, under the weighted rows
    size: 64,             // every number and label
    brW: 18, brPad: 6,    // bracket: arm length, gap to the numbers
  };
  const rowTop = (r) => G.top + r * G.rowH;

  // the plane
  const STEP = 100;                                       // one grid square = one step, in px
  const OX = 352;                                         // screen x of the origin: x −1.4…4.5 sits in the safe width
  const FLOOR = 880;                                      // screen y of the origin: y −2.2…2.3 sits in 650–1100
  const PLANE_TOP = 650;                                  // the grid stops here; the numbers sit above it
  const THIN = 0.6;                                       // arrow weight (ep01: "a little too thick")
  const w = (e, n) => [e * STEP, -n * STEP];
  const P2 = (x, y, oy = FLOOR) => [OX + x, oy + y];
  const at = (e, n, z = 0, oy = FLOOR) => { const [x, y] = w(e, n); return P2(x, y, oy); };

  // the navy background and the square grid, clipped to the plane's half
  function floor(g, o = {}) {
    const Wd = ISO.W, H = ISO.H, oy = o.oy == null ? FLOOR : o.oy, top = o.top == null ? PLANE_TOP : o.top;
    g.clearRect(0, 0, Wd, H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, Wd, H);
    g.save(); g.beginPath(); g.rect(0, top, Wd, ISO.SAFE.stageBottom + 10 - top); g.clip();
    g.strokeStyle = `rgba(74, 80, 112, ${o.alpha == null ? 0.42 : o.alpha})`; g.lineWidth = 3; g.beginPath();
    for (let k = -12; k <= 12; k++) {
      const x = OX + k * STEP, y = oy + k * STEP;
      g.moveTo(x, 0); g.lineTo(x, H); g.moveTo(0, y); g.lineTo(Wd, y);
    }
    g.stroke(); g.restore();
  }

  // A flat arrow from grid point a to b. o: col (RGB), alpha, u (draw progress), width, head
  function arrow(g, a, b, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u);
    if (u <= 0.001) return;
    const [x0, y0] = w(a[0], a[1]), [xb, yb] = w(b[0], b[1]);
    const x1 = lerp(x0, xb, u), y1 = lerp(y0, yb, u);
    const len = Math.hypot(x1 - x0, y1 - y0); if (len < 1) return;
    const dx = (x1 - x0) / len, dy = (y1 - y0) / len, nx = -dy, ny = dx;
    const hw = (o.width || 34) / 2 * THIN, hl = Math.min((o.head || 64) * 0.8, len * 0.6), hh = Math.max(hw * 2.6, 12);
    const sx = x1 - dx * hl, sy = y1 - dy * hl;
    const q = (x, y) => P2(x, y, o.oy);
    const col = o.col || COL.data, a1 = o.alpha == null ? 1 : o.alpha;
    ISO.poly(g, [q(x0 + nx * hw, y0 + ny * hw), q(sx + nx * hw, sy + ny * hw), q(sx - nx * hw, sy - ny * hw), q(x0 - nx * hw, y0 - ny * hw)], css(col, 1, a1));
    ISO.poly(g, [q(sx + nx * hh, sy + ny * hh), q(x1, y1), q(sx - nx * hh, sy - ny * hh)], css(col, 1, a1));
  }

  // a straight line between grid points (o: col RGB, alpha, width px, dash [on, off], u progress)
  function line(g, a, b, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u), al = o.alpha == null ? 1 : o.alpha;
    if (u <= 0.001 || al <= 0.001) return;
    const p = at(a[0], a[1], 0, o.oy), q = at(lerp(a[0], b[0], u), lerp(a[1], b[1], u), 0, o.oy);
    g.save(); g.strokeStyle = css(o.col || COL.dim, 1, al); g.lineWidth = o.width || 4; g.lineCap = "round";
    if (o.dash) g.setLineDash(o.dash);
    g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke(); g.restore();
  }
  // the reference frame: the two axes through the origin, a tick per step
  const AXES = { w: -1.4, e: 4.5, s: -2.2, n: 2.25 };
  function axes(g, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    line(g, [AXES.w, 0], [AXES.e, 0], { col: COL.dim, alpha: 0.55 * al, width: 5 });
    line(g, [0, AXES.s], [0, AXES.n], { col: COL.dim, alpha: 0.55 * al, width: 5 });
    const tk = 0.08;
    [-1, 1, 2, 3, 4].forEach((e) => line(g, [e, -tk], [e, tk], { col: COL.dim, alpha: 0.9 * al, width: 5 }));
    [-2, -1, 1, 2].forEach((n) => line(g, [-tk, n], [tk, n], { col: COL.dim, alpha: 0.9 * al, width: 5 }));
  }
  // dashed reading guides from a tip to its two coordinates on the axes
  function guides(g, v, o = {}) {
    const d = { col: o.col || COL.dim, alpha: o.alpha == null ? 0.9 : o.alpha, width: 5, dash: [14, 12], u: o.u };
    line(g, v, [v[0], 0], d);
    line(g, v, [0, v[1]], d);
  }
  // a dot on a grid point. o: half (radius), col, alpha
  function puck(g, e, n, o = {}) {
    const [x, y] = at(e, n, 0, o.oy), r = o.half || 12, al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001 || r <= 0.1) return;
    g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2);
    g.fillStyle = css(o.col || COL.text, 1, al); g.fill();
    g.strokeStyle = css(COL.bg, 1, al); g.lineWidth = 4; g.stroke();
  }

  // a flat label (DOM), placed centred on the screen point of grid (e, n)
  function label(root, text, o = {}) {
    const el = ISO.label(root, text, { size: o.size || G.size, color: o.color, width: o.width || 240, align: "center" });
    el.style.left = "0px"; el.style.top = "0px";
    return el;
  }
  function place(el, e, n, o = {}) {
    const [sx, sy] = at(e, n, 0, o.oy), wd = parseFloat(el.style.width) || 240, size = parseFloat(el.style.fontSize) || G.size;
    const s = o.scale == null ? 1 : o.scale;
    el.style.transform = `translate(${(sx - wd / 2 + (o.dx || 0)).toFixed(1)}px, ${(sy - size * 0.55 + (o.dy || 0)).toFixed(1)}px) scale(${s.toFixed(4)})`;
    el.style.opacity = (o.alpha == null ? 1 : o.alpha).toFixed(3);
  }

  // ---- the number grids (DOM, so `check` can read them) ----
  // One cell: a panel box with one number, absolutely placed. c.set(text),
  // c.color(rgb), c.border(rgb, alpha), c.at(left, top, {alpha, scale}).
  function cell(root, text, o = {}) {
    const el = document.createElement("div");
    const wd = o.width || G.cellW, ht = o.height || G.rowH;
    el.style.cssText = `position:absolute;left:0;top:0;width:${wd}px;height:${ht}px;box-sizing:border-box;` +
      `display:flex;align-items:center;justify-content:center;border-radius:12px;transform-origin:50% 50%;` +
      `background:transparent;border:4px solid transparent;font-size:${G.size}px;line-height:${ht - 8}px;` +
      `font-variant-numeric:tabular-nums;white-space:nowrap;color:${css(o.col || COL.text)};`;
    el.textContent = text;
    root.appendChild(el);
    const c = {
      el, wd, ht,
      set(t) { if (el.textContent !== t) el.textContent = t; },
      color(rgb, a = 1) { el.style.color = css(rgb, 1, a); },
      border(rgb, a = 1) { el.style.borderColor = css(rgb, 1, a); },   // a highlight box; transparent at rest
      at(left, top, o2 = {}) {
        const s = o2.scale == null ? 1 : o2.scale;
        el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${s.toFixed(4)})`;
        el.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3);
      },
    };
    c.at(o.left || 0, o.top || 0, { alpha: o.alpha });
    return c;
  }
  // A grid of rows × cols cells at its canonical place. vals[r][c] numbers;
  // o.rowCol: one RGB per row for the digits (default ROWCOL). Returns cells[r][c].
  function grid(root, vals, left, top, o = {}) {
    const cols = o.rowCol || ROWCOL;
    return vals.map((row, r) => row.map((v, c) => cell(root, fmtv(v), {
      left: left + c * (o.cellW || G.cellW), top: top + r * G.rowH, width: o.cellW || G.cellW, col: cols[r] || COL.text,
    })));
  }
  // the canonical parts, all at rest
  const xColumn = (root) => X.map((v, r) => [cell(root, fmtv(v), { left: G.xLeft, top: rowTop(r), width: G.xW, col: ROWCOL[r] })]);
  const wGrid = (root) => grid(root, W, G.wLeft, G.top);
  const pGrid = (root) => grid(root, XW, G.pLeft, G.top);
  const sumRow = (root, vals = SUM) => vals.map((v, c) => cell(root, fmtv(v), { left: G.pLeft + c * G.cellW, top: G.sumTop, col: COL.hero }));
  // A pair of square brackets around a block of entries (left..right, top..top+h).
  // b.color(rgb, a), b.at(dx, dy, {alpha}) moves the pair; b.els = [left, right].
  function brackets(root, left, top, right, h, o = {}) {
    const mk = (side) => {
      const el = document.createElement("div"), x = side === "l" ? left - G.brPad - G.brW : right + G.brPad;
      el.style.cssText = `position:absolute;left:${x}px;top:${top + 4}px;width:${G.brW}px;height:${h - 8}px;box-sizing:border-box;` +
        `border:6px solid ${css(o.col || COL.dim)};border-${side === "l" ? "right" : "left"}:none;border-radius:3px;`;
      root.appendChild(el); return el;
    };
    const els = [mk("l"), mk("r")];
    const b = {
      els,
      color(rgb, a = 1) { els.forEach((e) => { e.style.borderColor = css(rgb, 1, a); }); },
      at(dx, dy, o2 = {}) { els.forEach((e) => { e.style.transform = `translate(${dx.toFixed(1)}px, ${dy.toFixed(1)}px)`; e.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3); }); },
    };
    return b;
  }
  const H3 = 3 * G.rowH;
  const xBr = (root) => brackets(root, G.xLeft, G.top, G.xLeft + G.xW, H3);
  const wBr = (root) => brackets(root, G.wLeft, G.top, G.wLeft + 2 * G.cellW, H3);
  const pBr = (root) => brackets(root, G.pLeft, G.top, G.pLeft + 2 * G.cellW, H3);
  const sumBr = (root, col = COL.hero) => brackets(root, G.pLeft, G.sumTop, G.pLeft + 2 * G.cellW, G.rowH, { col });
  // header labels: "x" over the x column, "W" over W; "x @ W" left of the sum row
  function headers(root) {
    const mk = (t, left, width, top, align = "center") => ISO.label(root, t, { size: G.size, color: css(COL.dim), left, top, width, align });
    return {
      x: mk("x", G.xLeft, G.xW, G.header),
      W: mk("W", G.wLeft, 2 * G.cellW, G.header),
      out: mk("x @ W", G.wLeft, G.pLeft - G.brW - G.brPad - 24 - G.wLeft, G.sumTop + 2, "right"),
    };
  }
  // "→" between W and the weighted rows, one per row
  const arrows = (root) => [0, 1, 2].map((r) => ISO.label(root, "→", { size: G.size, color: css(COL.dim), left: G.wLeft + 2 * G.cellW + G.brPad + G.brW, top: rowTop(r) + 2, width: G.pLeft - G.wLeft - 2 * G.cellW - 2 * (G.brPad + G.brW), align: "center" }));

  window.VEC = {
    X, W, XW, SUM, B, Y, CHAIN, ROWCOL, fmtv,
    G, rowTop, STEP, OX, FLOOR, PLANE_TOP, THIN, AXES, w, P2, at,
    floor, arrow, line, axes, guides, puck, label, place,
    cell, grid, xColumn, wGrid, pGrid, sumRow, headers, arrows, brackets, xBr, wBr, pBr, sumBr,
  };
})();
