// vec.js — the flat 2D number plane kit for HyperFrames Shorts (the Linear
// Algebra series look, agents/style.md "Linear algebra" and "Vectors and
// matrices as numbers"). Linked into a beat as `vec/`, after `iso/iso.js`:
//   ln -s ../../../_shared/web/vec NN_beat/vec      (series episodes are one level deeper)
//
// Promoted 2026-10-11 from three per-episode copies (ep01 plane, ep03 camera
// views and the linear map, ep04 matrix notation). Shipped episodes keep
// their own `_vec/vec.js`; new ones link this and keep only their numbers
// (the ledger) and their canonical frame in a local script.
//
// The world: x right, y up, one grid square = one step. A camera (`view`)
// says how many px a step is, where the origin sits, and how far the axes
// run. Every drawing call uses the current camera, so a beat sets it once at
// the top of render(t). Everything is a pure function of its arguments.
(function () {
  const { COL, css, mix, lerp, clamp01 } = ISO;

  // ---- numbers ----
  const fmtv = (v) => (v < 0 ? "−" : "") + String(Math.abs(v));      // true minus; 0.5 stays 0.5, never 2.0
  const vtxt = (v, i, n) => fmtv(v) + (i < n - 1 ? "," : "");        // an entry of a vector, with its comma
  const SLOT = [COL.tokens[0], COL.tokens[1], COL.tokens[2]];          // row / slot identity: teal, blue, gold
  const THIN = 0.6;                                                    // arrow weight (ep01: "a little too thick")

  // ---- the camera ----
  // A view: { step (px per grid step), ox, oy (screen px of the origin),
  //   ax: { w, e, s, n } (axis extents in steps), top (optional: the grid is
  //   clipped above this screen y, e.g. under a block of numbers) }.
  // view(A) sets it; view(A, B, u) interpolates; at(x, y) maps grid -> screen.
  const DEFAULT = { step: 165, ox: 507, oy: 780, ax: { w: -2.35, e: 2.35, s: -2.2, n: 2.35 } };
  const CAM = { step: DEFAULT.step, ox: DEFAULT.ox, oy: DEFAULT.oy, ax: Object.assign({}, DEFAULT.ax), top: null };
  function view(A, B = A, k = 0) {
    const u = clamp01(k);
    CAM.step = lerp(A.step, B.step, u); CAM.ox = lerp(A.ox, B.ox, u); CAM.oy = lerp(A.oy, B.oy, u);
    Object.keys(A.ax).forEach((d) => { CAM.ax[d] = lerp(A.ax[d], B.ax[d], u); });
    CAM.top = A.top == null && B.top == null ? null : lerp(A.top == null ? 0 : A.top, B.top == null ? 0 : B.top, u);
  }
  const step = () => CAM.step;
  const w = (x, y) => [x * CAM.step, -y * CAM.step];                  // grid -> plane px (screen y runs down)
  const P2 = (px, py) => [CAM.ox + px, CAM.oy + py];                  // plane px -> screen
  const at = (x, y) => { const [a, b] = w(x, y); return P2(a, b); };

  // ---- the linear map (row-vector convention: row i of M is where e_i lands) ----
  const I2 = [[1, 0], [0, 1]];
  const basisTo = (A, B, s) => A.map((r, i) => r.map((v, j) => lerp(v, B[i][j], s)));   // rows, interpolated
  const comb = (p, B) => [p[0] * B[0][0] + p[1] * B[1][0], p[0] * B[0][1] + p[1] * B[1][1]];   // p @ B
  const map = (p, M, s = 1) => comb(p, basisTo(I2, M, s));

  // ---- the plane ----
  // the navy background and the square grid (o: alpha, top: clip the grid above this y)
  function floor(g, o = {}) {
    const Wd = ISO.W, H = ISO.H, top = o.top != null ? o.top : CAM.top;
    g.clearRect(0, 0, Wd, H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, Wd, H);
    g.save();
    if (top != null) { g.beginPath(); g.rect(0, top, Wd, ISO.SAFE.stageBottom - top); g.clip(); }
    g.strokeStyle = `rgba(74, 80, 112, ${o.alpha == null ? 0.42 : o.alpha})`; g.lineWidth = 3; g.beginPath();
    const n = Math.ceil(Math.max(Wd, H) / CAM.step) + 1;
    for (let k = -n; k <= n; k++) {
      const x = CAM.ox + k * CAM.step, y = CAM.oy + k * CAM.step;
      g.moveTo(x, 0); g.lineTo(x, H); g.moveTo(0, y); g.lineTo(Wd, y);
    }
    g.stroke(); g.restore();
  }
  // the grid a matrix makes: the lattice spanned by rows B (o: col, alpha, width)
  function lattice(g, B, o = {}) {
    const al = o.alpha == null ? 0.5 : o.alpha;
    if (al <= 0.001) return;
    g.save(); g.strokeStyle = css(o.col || COL.muted, 1, al); g.lineWidth = o.width || 3; g.beginPath();
    [0, 1].forEach((a) => {
      const b = 1 - a, d = B[a];
      for (let n = -12; n <= 12; n++) {
        const p = at(B[b][0] * n - d[0] * 40, B[b][1] * n - d[1] * 40), q = at(B[b][0] * n + d[0] * 40, B[b][1] * n + d[1] * 40);
        g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
      }
    });
    g.stroke(); g.restore();
  }
  // a straight line between grid points (o: col, alpha, width px, dash [on, off], u progress)
  function line(g, a, b, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u), al = o.alpha == null ? 1 : o.alpha;
    if (u <= 0.001 || al <= 0.001) return;
    const p = at(a[0], a[1]), q = at(lerp(a[0], b[0], u), lerp(a[1], b[1], u));
    g.save(); g.strokeStyle = css(o.col || COL.dim, 1, al); g.lineWidth = o.width || 4; g.lineCap = "round";
    if (o.dash) g.setLineDash(o.dash);
    g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke(); g.restore();
  }
  // the integer ticks strictly inside (lo, hi), zero excluded
  const ticks = (lo, hi) => { const t = []; for (let k = Math.ceil(lo); k <= Math.floor(hi); k++) if (k !== 0 && k > lo && k < hi) t.push(k); return t; };
  // the reference frame: both axes through the origin to the camera's extents, a tick per step (o: alpha)
  function axes(g, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha, A = CAM.ax, tk = 0.08 * 165 / CAM.step;
    if (al <= 0.001) return;
    const d = { col: COL.dim, alpha: 0.55 * al, width: 5 }, t = { col: COL.dim, alpha: 0.9 * al, width: 5 };
    line(g, [A.w, 0], [A.e, 0], d); line(g, [0, A.s], [0, A.n], d);
    ticks(A.w, A.e).forEach((x) => line(g, [x, -tk], [x, tk], t));
    ticks(A.s, A.n).forEach((y) => line(g, [-tk, y], [tk, y], t));
  }
  // dashed reading guides from point v to its two coordinates on the axes
  function guides(g, v, o = {}) {
    const d = { col: o.col || COL.dim, alpha: o.alpha == null ? 0.9 : o.alpha, width: 5, dash: [14, 12], u: o.u };
    line(g, v, [v[0], 0], d); line(g, v, [0, v[1]], d);
  }
  // A flat arrow from grid point a to b. o: col (default teal), alpha, u (draw
  // progress; the head travels with the tip), width (default 44), head (default 90).
  // No halo: the hero is marked by colour alone.
  function arrow(g, a, b, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u);
    if (u <= 0.001) return;
    const [x0, y0] = w(a[0], a[1]), [xb, yb] = w(b[0], b[1]);
    const x1 = lerp(x0, xb, u), y1 = lerp(y0, yb, u);
    const len = Math.hypot(x1 - x0, y1 - y0); if (len < 1) return;
    const dx = (x1 - x0) / len, dy = (y1 - y0) / len, nx = -dy, ny = dx;
    const hw = (o.width || 44) / 2 * THIN, hl = Math.min((o.head || 90) * 0.8, len * 0.6), hh = Math.max(hw * 2.6, 12);
    const sx = x1 - dx * hl, sy = y1 - dy * hl;
    const c = css(o.col || COL.data, 1, o.alpha == null ? 1 : o.alpha);
    ISO.poly(g, [P2(x0 + nx * hw, y0 + ny * hw), P2(sx + nx * hw, sy + ny * hw), P2(sx - nx * hw, sy - ny * hw), P2(x0 - nx * hw, y0 - ny * hw)], c);
    ISO.poly(g, [P2(sx + nx * hh, sy + ny * hh), P2(x1, y1), P2(sx - nx * hh, sy - ny * hh)], c);
  }
  // a dot on a grid point (o: half radius px, col, alpha)
  function puck(g, x, y, o = {}) {
    const [sx, sy] = at(x, y), r = o.half || 14, al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001 || r <= 0.1) return;
    g.beginPath(); g.arc(sx, sy, r, 0, Math.PI * 2);
    g.fillStyle = css(o.col || COL.text, 1, al); g.fill();
    g.strokeStyle = css(COL.bg, 1, al); g.lineWidth = 4; g.stroke();
  }
  // a ring on a grid point: where an input direction lands (o: col default hero, alpha, r px, k 0..1 pulse)
  function spot(g, x, y, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    const [sx, sy] = at(x, y), r = (o.r || 30) * (1 + 0.4 * (o.k || 0));
    g.save(); g.beginPath(); g.arc(sx, sy, r, 0, Math.PI * 2);
    g.strokeStyle = css(o.col || COL.hero, 1, al); g.lineWidth = 7; g.stroke(); g.restore();
  }

  // ---- DOM text (so `check` can read it) ----
  // a flat label, placed centred on the screen point of grid (x, y), offset in px
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
  // literal code: monospace set from the script (HTML-set monospace renders in Inter; beat brief trap)
  function code(el) {
    [el, ...el.querySelectorAll("*")].forEach((e) => { e.style.fontFamily = "monospace"; e.style.fontWeight = "700"; });
    return el;
  }
  // A code card: lines of literal code on a panel. Each line is a string, or an
  // array of spans, each a string or [text, rgb]. Returns { el, spans, at(left, top, {alpha, scale}) }.
  function codeCard(root, lines, o = {}) {
    const size = o.size || 60, el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;box-sizing:border-box;padding:14px 20px;border-radius:22px;` +
      `background:${css(COL.panel)};border:6px solid ${css(COL.dim)};font-size:${size}px;line-height:${Math.round(size * 1.2)}px;` +
      `white-space:pre;color:${css(COL.text)};transform-origin:50% 50%;`;
    const spans = lines.map((ln) => {
      const row = document.createElement("div"); el.appendChild(row);
      return (Array.isArray(ln) ? ln : [ln]).map((sp) => (typeof sp === "string" ? [sp] : sp)).map(([t, rgb]) => {
        const s = document.createElement("span"); s.textContent = t; if (rgb) s.style.color = css(rgb); row.appendChild(s); return s;
      });
    });
    root.appendChild(el); code(el);
    return {
      el, spans,
      at(left, top, o2 = {}) {
        const s = o2.scale == null ? 1 : o2.scale;
        el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${s.toFixed(4)})`;
        el.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3);
      },
    };
  }

  // ---- numbers on screen (agents/style.md "Vectors and matrices as numbers") ----
  // The vector card: "[ a, b ]" on a panel, one span per slot. o: size (80),
  // name ("x ="), cols (RGB per slot). .light(i, k, col), .border(col, k), .at(left, top, {alpha, scale}).
  function vecCard(root, vals, o = {}) {
    const size = o.size || 80, el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;padding:${Math.round(size * 0.18)}px ${Math.round(size * 0.36)}px;border-radius:22px;` +
      `background:${css(COL.panel)};border:6px solid ${css(COL.dim)};white-space:nowrap;transform-origin:50% 50%;` +
      `font-size:${size}px;line-height:${Math.round(size * 1.15)}px;color:${css(COL.text)};font-variant-numeric:tabular-nums;`;
    const row = document.createElement("div"); row.style.cssText = "display:flex;align-items:flex-start;white-space:pre;";
    el.appendChild(row);
    const txt = (s, color) => { const d = document.createElement("span"); d.textContent = s; if (color) d.style.color = color; return d; };
    if (o.name) row.appendChild(txt(o.name + " ", css(COL.dim)));
    row.appendChild(txt("[ ", css(COL.dim)));
    const base = vals.map((_, i) => (o.cols ? o.cols[i] : COL.text));
    const slots = vals.map((v, i) => {
      const s = txt(typeof v === "number" ? fmtv(v) : v, css(base[i])); row.appendChild(s);
      if (i < vals.length - 1) row.appendChild(txt(", ", css(COL.dim)));
      return s;
    });
    row.appendChild(txt(" ]", css(COL.dim)));
    root.appendChild(el);
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
  // One number cell, absolutely placed (o: left, top, width, height, size, col, alpha).
  // .set(text), .color(rgb, a), .border(rgb, a) (a highlight box; transparent at rest), .at(left, top, o2), .home(o2).
  function cell(root, text, o = {}) {
    const el = document.createElement("div"), wd = o.width || 125, ht = o.height || 76, size = o.size || 64;
    el.style.cssText = `position:absolute;left:0;top:0;width:${wd}px;height:${ht}px;box-sizing:border-box;` +
      `display:flex;align-items:center;justify-content:center;border-radius:12px;transform-origin:50% 50%;` +
      `background:transparent;border:4px solid transparent;font-size:${size}px;line-height:${ht - 8}px;` +
      `font-variant-numeric:tabular-nums;white-space:nowrap;color:${css(o.col || COL.text)};`;
    el.textContent = text;
    root.appendChild(el);
    const c = {
      el, wd, ht, left0: o.left || 0, top0: o.top || 0, col0: o.col || COL.text,
      set(t) { if (el.textContent !== t) el.textContent = t; },
      color(rgb, a = 1) { el.style.color = css(rgb, 1, a); },
      border(rgb, a = 1) { el.style.borderColor = css(rgb, 1, a); },
      at(left, top, o2 = {}) {
        const s = o2.scale == null ? 1 : o2.scale;
        el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${s.toFixed(4)})`;
        el.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3);
      },
    };
    c.home = (o2 = {}) => c.at(c.left0, c.top0, o2);
    c.at(c.left0, c.top0, { alpha: o.alpha });
    return c;
  }
  // A matrix: bare numbers in a tight grid, one colour per row (o.rowCol, default SLOT).
  // Returns cells[r][c]. Wrap it with brackets(); name it with label().
  function grid(root, vals, left, top, o = {}) {
    const cols = o.rowCol || SLOT, cw = o.cellW || 125, rh = o.rowH || 76;
    return vals.map((row, r) => row.map((v, c) => cell(root, fmtv(v), {
      left: left + c * cw, top: top + r * rh, width: cw, height: rh, size: o.size, col: cols[r] || COL.text,
    })));
  }
  // One tall pair of square brackets around a block (left..right, top..top+h).
  // o: col, arm (px, 18), pad (px, 6). .color(rgb, a), .at(dx, dy, {alpha}); .els = [left, right].
  function brackets(root, left, top, right, h, o = {}) {
    const arm = o.arm || 18, pad = o.pad || 6;
    const mk = (side) => {
      const el = document.createElement("div"), x = side === "l" ? left - pad - arm : right + pad;
      el.style.cssText = `position:absolute;left:${x}px;top:${top + 4}px;width:${arm}px;height:${h - 8}px;box-sizing:border-box;` +
        `border:6px solid ${css(o.col || COL.dim)};border-${side === "l" ? "right" : "left"}:none;border-radius:3px;`;
      root.appendChild(el); return el;
    };
    const els = [mk("l"), mk("r")];
    return {
      els,
      color(rgb, a = 1) { els.forEach((e) => { e.style.borderColor = css(rgb, 1, a); }); },
      at(dx, dy, o2 = {}) { els.forEach((e) => { e.style.transform = `translate(${dx.toFixed(1)}px, ${dy.toFixed(1)}px)`; e.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3); }); },
    };
  }
  // A highlight box that appears and goes again: .rect([left, top, w, h], alpha, col).
  function hbox(root) {
    const el = document.createElement("div");
    el.style.cssText = "position:absolute;left:0;top:0;box-sizing:border-box;border-radius:14px;border:6px solid;opacity:0;";
    root.appendChild(el);
    return {
      el,
      rect(r, alpha = 1, col = COL.hero) {
        el.style.width = `${r[2]}px`; el.style.height = `${r[3]}px`;
        el.style.transform = `translate(${r[0].toFixed(1)}px, ${r[1].toFixed(1)}px)`;
        el.style.borderColor = css(col); el.style.opacity = clamp01(alpha).toFixed(3);
      },
    };
  }
  // horizontal placement helpers in the safe width
  const centreLeft = (el) => (ISO.SAFE.x0 + ISO.SAFE.x1) / 2 - el.offsetWidth / 2;
  const rightLeft = (el, right = ISO.SAFE.x1) => right - el.offsetWidth;

  window.VEC = {
    fmtv, vtxt, SLOT, THIN, DEFAULT, CAM, view, step, w, P2, at,
    I2, basisTo, comb, map,
    floor, lattice, line, ticks, axes, guides, arrow, puck, spot,
    label, place, code, codeCard, vecCard, cell, grid, brackets, hbox, centreLeft, rightLeft,
  };
})();
