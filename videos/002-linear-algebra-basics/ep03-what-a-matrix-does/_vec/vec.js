// vec.js — the shared parts for ep03 "What a Matrix Really Does" (linked into
// each beat as `vec/`, after `iso/iso.js`). Started as a copy of
// ep01-what-is-a-vector/_vec/vec.js (the flat 2D plane look); the plane is
// re-framed for this episode's numbers and the matrix parts are new.
//
// The world is a flat 2D number plane: x right, y up, one grid square is one
// step. Grid coords (x, y); the origin sits at screen (OX, OY). Arrows lie on
// the plane; numbers stand on flat cards. ISO is still the source of the
// palette, poly, label, start, easing. Everything is a pure function of its
// arguments: beats call these inside render(t).
(function () {
  const { COL, css, mix, lerp, clamp01 } = ISO;
  let AXES;                                             // set with the views below

  // ---- the fixed example (the ledger in storyboard.md) ----
  // Row-vector (PyTorch) convention: x @ W, row i of W is where input direction i lands.
  const E1 = [1, 0], E2 = [0, 1];                       // the input directions e1, e2
  const W = [[1, 0.5], [-0.5, 1.25]];                   // row 1: where e1 lands; row 2: where e2 lands
  const X = [3, 2];                                     // the vector: 3 of e1 plus 2 of e2
  const XW = [2, 4];                                    // x @ W = 3·(1, 0.5) + 2·(−0.5, 1.25)
  const M = [[1.6, 0.8], [0.2, 0.1]];                  // beat 7 only: both rows on the (2, 1) line, so it amplifies (2, 1) and collapses (1, −2)
  const fmtv = (v) => (v < 0 ? "−" : "") + Math.abs(v);  // true minus sign
  const SLOT = [[45, 212, 191], [96, 165, 250]];        // e1 teal (HERO_TEAL), e2 blue (iso tokens[1]): identity colours

  // ---- the views (a camera: grid scale, origin, and how far the axes run) ----
  // NEAR: the canonical frame; e1, e2 and where they land fill the stage under
  //   the matrix card (beats 2, 6, 8 and the last frame).
  // FAR: the recipe beats; x = (3, 2) and x @ W = (2, 4) fit (beats 1, 3-5).
  // MID: the origin at the stage centre, ±1.3 steps each way (beat 7's ring).
  // Call view(A, B, u) or setView(k) (NEAR -> FAR) once at the top of
  // render(t); every drawing call after it uses that camera.
  const NEAR = { step: 300, ox: 432, oy: 1030, ax: { w: -1.35, e: 1.7, s: -0.45, n: 1.75 } };
  const FAR = { step: 160, ox: 240, oy: 1060, ax: { w: -1.3, e: 4.4, s: -1.2, n: 4.5 } };
  const MID = { step: 280, ox: 507, oy: 720, ax: { w: -1.5, e: 1.5, s: -1.25, n: 1.6 } };
  let STEP = NEAR.step, OX = NEAR.ox, OY = NEAR.oy;
  AXES = Object.assign({}, NEAR.ax);
  function view(A, B = A, k = 0) {
    const u = clamp01(k);
    STEP = lerp(A.step, B.step, u); OX = lerp(A.ox, B.ox, u); OY = lerp(A.oy, B.oy, u);
    Object.keys(A.ax).forEach((d) => { AXES[d] = lerp(A.ax[d], B.ax[d], u); });
  }
  const setView = (k) => view(NEAR, FAR, k);
  const THIN = 0.6;                                     // arrow weight (ep01: "a little too thick" at 1.0)
  const CARD_TOP = 250;                                 // the matrix card's top edge
  const CARD_RIGHT = 950;                               // ... and its right edge (top-right corner of the safe area)
  const w = (x, y) => [x * STEP, -y * STEP];            // grid -> plane px (screen y runs down)
  const P2 = (x, y) => [OX + x, OY + y];                // plane px -> screen
  const at = (x, y) => { const [a, b] = w(x, y); return P2(a, b); };

  // the linear map, interpolated: s = 0 is the identity, s = 1 is W.
  // basis(s) = [where e1 is, where e2 is]; map(p, s) = p[0]·basis[0] + p[1]·basis[1]
  const basis = (s) => [[lerp(1, W[0][0], s), lerp(0, W[0][1], s)], [lerp(0, W[1][0], s), lerp(1, W[1][1], s)]];
  const basisTo = (A, B, s) => [[lerp(A[0][0], B[0][0], s), lerp(A[0][1], B[0][1], s)], [lerp(A[1][0], B[1][0], s), lerp(A[1][1], B[1][1], s)]];
  const comb = (p, B) => [p[0] * B[0][0] + p[1] * B[1][0], p[0] * B[0][1] + p[1] * B[1][1]];
  const map = (p, s = 1) => comb(p, basis(s));

  // the navy background and the square grid, one line per step through the origin
  function floor(g, o = {}) {
    const Wd = ISO.W, H = ISO.H;
    g.clearRect(0, 0, Wd, H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, Wd, H);
    g.strokeStyle = `rgba(74, 80, 112, ${o.alpha == null ? 0.42 : o.alpha})`; g.lineWidth = 3; g.beginPath();
    for (let k = -30; k <= 30; k++) {
      const x = OX + k * STEP, y = OY + k * STEP;
      g.moveTo(x, 0); g.lineTo(x, H); g.moveTo(0, y); g.lineTo(Wd, y);
    }
    g.stroke();
  }

  // The moved grid: the lattice spanned by basis B (two families of lines),
  // drawn across the whole frame. o: col RGB (default muted), alpha, width.
  function lattice(g, B, o = {}) {
    const al = o.alpha == null ? 0.5 : o.alpha;
    if (al <= 0.001) return;
    g.save(); g.strokeStyle = css(o.col || COL.muted, 1, al); g.lineWidth = o.width || 3; g.beginPath();
    [0, 1].forEach((a) => {
      const b = 1 - a, d = B[a];
      for (let n = -12; n <= 12; n++) {
        const p = at(B[b][0] * n - d[0] * 40, B[b][1] * n - d[1] * 40);
        const q = at(B[b][0] * n + d[0] * 40, B[b][1] * n + d[1] * 40);
        g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
      }
    });
    g.stroke(); g.restore();
  }

  // A flat arrow from grid point a to b. o:
  //   col  RGB triple (default teal)   alpha  0..1
  //   u    draw progress 0..1 (the tip travels from a to b; the head appears with it)
  //   width shaft width in world units (default 44)   head  head length (default 90)
  //   (no halo: the hero is marked by colour alone)
  function arrow(g, a, b, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u);
    if (u <= 0.001) return;
    const [x0, y0] = w(a[0], a[1]), [xb, yb] = w(b[0], b[1]);
    const x1 = lerp(x0, xb, u), y1 = lerp(y0, yb, u);
    const len = Math.hypot(x1 - x0, y1 - y0); if (len < 1) return;
    const dx = (x1 - x0) / len, dy = (y1 - y0) / len, nx = -dy, ny = dx;
    const hw = (o.width || 44) / 2 * THIN, hl = Math.min((o.head || 90) * 0.8, len * 0.6), hh = Math.max(hw * 2.6, 14);
    const sx = x1 - dx * hl, sy = y1 - dy * hl;
    const col = o.col || COL.data, a1 = o.alpha == null ? 1 : o.alpha;
    const shaft = [P2(x0 + nx * hw, y0 + ny * hw), P2(sx + nx * hw, sy + ny * hw), P2(sx - nx * hw, sy - ny * hw), P2(x0 - nx * hw, y0 - ny * hw)];
    const head = [P2(sx + nx * hh, sy + ny * hh), P2(x1, y1), P2(sx - nx * hh, sy - ny * hh)];
    ISO.poly(g, shaft, css(col, 1, a1));
    ISO.poly(g, head, css(col, 1, a1));
  }

  // a straight line between grid points (o: col RGB, alpha, width px, dash [on, off], u progress)
  function line(g, a, b, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u), al = o.alpha == null ? 1 : o.alpha;
    if (u <= 0.001 || al <= 0.001) return;
    const p = at(a[0], a[1]), q = at(lerp(a[0], b[0], u), lerp(a[1], b[1], u));
    g.save(); g.strokeStyle = css(o.col || COL.dim, 1, al); g.lineWidth = o.width || 4; g.lineCap = "round";
    if (o.dash) g.setLineDash(o.dash);
    g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke(); g.restore();
  }
  // The reference frame: the x and y grid lines through the origin, brighter
  // than the floor, with a tick at every step. o: alpha.
  function axes(g, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    line(g, [AXES.w, 0], [AXES.e, 0], { col: COL.dim, alpha: 0.55 * al, width: 5 });
    line(g, [0, AXES.s], [0, AXES.n], { col: COL.dim, alpha: 0.55 * al, width: 5 });
    const tk = 0.08;
    [-1, 1, 2, 3, 4].forEach((x) => { if (x > AXES.w && x < AXES.e) line(g, [x, -tk], [x, tk], { col: COL.dim, alpha: 0.9 * al, width: 5 }); });
    [-1, 1, 2, 3, 4].forEach((y) => { if (y > AXES.s && y < AXES.n) line(g, [-tk, y], [tk, y], { col: COL.dim, alpha: 0.9 * al, width: 5 }); });
  }
  // dashed reading guides from point v down to its two coordinates on the axes
  function guides(g, v, o = {}) {
    const d = { col: o.col || COL.dim, alpha: o.alpha == null ? 0.9 : o.alpha, width: 5, dash: [14, 12], u: o.u };
    line(g, v, [v[0], 0], d);
    line(g, v, [0, v[1]], d);
  }

  // a dot on a grid point (the origin, a marker). o: half (radius), col, alpha
  function puck(g, x, y, o = {}) {
    const [sx, sy] = at(x, y), r = o.half || 16, al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001 || r <= 0.1) return;
    g.beginPath(); g.arc(sx, sy, r, 0, Math.PI * 2);
    g.fillStyle = css(o.col || COL.text, 1, al); g.fill();
    g.strokeStyle = css(COL.bg, 1, al); g.lineWidth = 4; g.stroke();
  }
  // A landing spot: a ring around a grid point where an input direction
  // lands (the episode's hero mark). o: col (default hero), alpha, r (radius
  // px, default 30), k 0..1 (a pulse: the ring swells by 40 %).
  function spot(g, x, y, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    const [sx, sy] = at(x, y), r = (o.r || 30) * (1 + 0.4 * (o.k || 0));
    g.save(); g.beginPath(); g.arc(sx, sy, r, 0, Math.PI * 2);
    g.strokeStyle = css(o.col || COL.hero, 1, al); g.lineWidth = 7; g.stroke(); g.restore();
  }

  // A flat upright label centred on the screen point of grid (x, y).
  function label(root, text, o = {}) {
    const el = ISO.label(root, text, { size: o.size || 64, color: o.color, width: o.width || 160, align: "center" });
    el.style.left = "0px"; el.style.top = "0px";
    return el;
  }
  function place(el, x, y, o = {}) {
    const [sx, sy] = at(x, y), wd = parseFloat(el.style.width) || 160, size = parseFloat(el.style.fontSize) || 64;
    const s = o.scale == null ? 1 : o.scale;
    el.style.transform = `translate(${(sx - wd / 2 + (o.dx || 0)).toFixed(1)}px, ${(sy - size * 0.55 + (o.dy || 0)).toFixed(1)}px) scale(${s.toFixed(4)})`;
    el.style.opacity = (o.alpha == null ? 1 : o.alpha).toFixed(3);
  }

  // The vector card: "[ a, b ]" on a flat panel, one span per slot so a slot
  // can light up. o: size (default 80), name (e.g. "x =", drawn before the
  // bracket), cols (RGB per slot; default text). Position with .at(left, top).
  function vecCard(root, vals, o = {}) {
    const size = o.size || 80;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;padding:${Math.round(size * 0.18)}px ${Math.round(size * 0.36)}px;border-radius:22px;` +
      `background:${css(COL.panel)};border:6px solid ${css(COL.dim)};white-space:nowrap;transform-origin:50% 50%;` +
      `font-size:${size}px;line-height:${Math.round(size * 1.15)}px;color:${css(COL.text)};font-variant-numeric:tabular-nums;`;
    const row = document.createElement("div"); row.style.cssText = "display:flex;align-items:flex-start;white-space:pre;";
    el.appendChild(row);
    const txt = (s, color) => { const d = document.createElement("span"); d.textContent = s; if (color) d.style.color = color; return d; };
    if (o.name) row.appendChild(txt(o.name + " ", css(COL.dim)));
    row.appendChild(txt("[ ", css(COL.dim)));
    const slots = [];
    vals.forEach((v, i) => {
      const s = txt(typeof v === "number" ? fmtv(v) : v, o.cols ? css(o.cols[i]) : null); row.appendChild(s); slots.push(s);
      if (i < vals.length - 1) row.appendChild(txt(", ", css(COL.dim)));
    });
    row.appendChild(txt(" ]", css(COL.dim)));
    root.appendChild(el);
    const base = vals.map((_, i) => (o.cols ? o.cols[i] : COL.text));
    return {
      el, slots,
      light(i, k, col = COL.hero) { slots[i].style.color = css(mix(base[i], col, clamp01(k))); },
      border(col, k = 1) { el.style.borderColor = css(mix(COL.dim, col, clamp01(k))); },
      at(left, top, o2 = {}) {
        const s = o2.scale == null ? 1 : o2.scale;
        el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${s.toFixed(4)})`;
        el.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3);
      },
    };
  }

  // The matrix card: "W =" then a table of rows, each row in its
  // input direction's colour, with an optional tag after each row ("e1",
  // "e2"). One element per row and per cell, so a row can light up or a
  // cell can be measured. o: size (default 72), name (default "W"),
  // tags (array or null). Position with .at(left, top); .rowBox(i) gives the
  // screen rect of row i's numbers (measured once at build, for a fly-out).
  function matCard(root, rows, o = {}) {
    const size = o.size || 72, lh = Math.round(size * 1.2), tags = o.tags === undefined ? ["e1", "e2"] : o.tags;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;padding:${Math.round(size * 0.14)}px ${Math.round(size * 0.3)}px;border-radius:22px;` +
      `background:${css(COL.panel)};border:6px solid ${css(COL.dim)};white-space:nowrap;transform-origin:50% 50%;` +
      `font-size:${size}px;line-height:${lh}px;color:${css(COL.text)};font-variant-numeric:tabular-nums;` +
      `display:flex;align-items:center;gap:${Math.round(size * 0.3)}px;`;
    const name = document.createElement("div");
    name.textContent = (o.name || "W") + " =";
    name.style.color = css(COL.dim);
    el.appendChild(name);
    const grid = document.createElement("div");
    grid.style.cssText = `display:grid;grid-template-columns:auto auto auto auto${tags ? " auto" : ""};column-gap:${Math.round(size * 0.32)}px;align-items:center;`;
    el.appendChild(grid);
    const cell = (s, color, align = "right") => {
      const d = document.createElement("div"); d.textContent = s; d.style.textAlign = align;
      if (color) d.style.color = color; grid.appendChild(d); return d;
    };
    const rowEls = [], cells = [], tagEls = [], brackets = [];
    rows.forEach((r, i) => {
      const col = SLOT[i % SLOT.length];
      brackets.push(cell("[", css(COL.dim), "center"));
      const cs = r.map((v) => cell(typeof v === "number" ? fmtv(v) : v, css(col)));
      brackets.push(cell("]", css(COL.dim), "center"));
      if (tags) tagEls.push(cell(tags[i] || "", css(col, 1, 0.75), "left"));
      cells.push(cs); rowEls.push(cs);
    });
    root.appendChild(el);
    return {
      el, cells, tagEls, name,
      // light row i: k 0..1 toward col (default hero); dim: other rows' alpha
      light(i, k, col = COL.hero) {
        const base = SLOT[i % SLOT.length];
        cells[i].forEach((c) => { c.style.color = css(mix(base, col, clamp01(k))); });
      },
      rowAlpha(i, a) { cells[i].forEach((c) => { c.style.opacity = a.toFixed(3); }); if (tagEls[i]) tagEls[i].style.opacity = a.toFixed(3); },
      border(col, k = 1) { el.style.borderColor = css(mix(COL.dim, col, clamp01(k))); },
      at(left, top, o2 = {}) {
        const s = o2.scale == null ? 1 : o2.scale;
        el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${s.toFixed(4)})`;
        el.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3);
      },
    };
  }
  // the canonical spot for the matrix card: top-right of the safe area
  const cardLeft = (el) => CARD_RIGHT - el.offsetWidth;
  const centreLeft = (el) => (ISO.SAFE.x0 + ISO.SAFE.x1) / 2 - el.offsetWidth / 2;

  // The canonical frame (00_layout, and the last frame of the Short): the
  // plane and axes, e1 and e2 as muted ghosts, the landed arrows in their
  // identity colours, a magenta landing spot on each tip, the origin dot.
  // Labels and the card are DOM; the caller places them.
  function canonical(g, o = {}) {
    floor(g); axes(g);
    arrow(g, [0, 0], E1, { col: COL.muted }); arrow(g, [0, 0], E2, { col: COL.muted });
    arrow(g, [0, 0], W[0], { col: SLOT[0] }); arrow(g, [0, 0], W[1], { col: SLOT[1] });
    spot(g, W[0][0], W[0][1]); spot(g, W[1][0], W[1][1]);
    puck(g, 0, 0, { half: 14 });
  }

  window.VEC = { E1, E2, W, X, XW, M, SLOT, fmtv, NEAR, FAR, MID, view, setView, THIN, CARD_TOP, CARD_RIGHT, AXES, w, P2, at,
                 basis, basisTo, comb, map, floor, lattice, line, axes, guides, arrow, puck, spot, label, place,
                 vecCard, matCard, cardLeft, centreLeft, canonical };
})();
