// vec.js — the shared parts for ep01 "What Is a Vector?" (linked into each
// beat as `vec/`, after `iso/iso.js`).
//
// The world is the house isometric floor, seen square-on (ISO.setTheta(0)),
// so east and north have the same screen length and northwest points
// straight up. One grid square is one step. Grid coords (e, n): e = steps
// east, n = steps north; the origin sits at screen (507, FLOOR).
// Arrows lie flat on the floor (see a thing); numbers stand on flat upright
// cards (read a value). Everything is a pure function of its arguments.
(function () {
  const { P, COL, css, mix, lerp, clamp01 } = ISO;
  ISO.setTheta(0);

  // ---- the fixed example (the ledger in storyboard.md) ----
  const V = [-2, 2];                                    // northwest: 2 opposite east, 2 north
  const HOUSE = { vals: ["1,800", "450,000"], labels: ["sq ft", "price"] };
  const EMBED = ["0.12", "−0.48", "0.91", "0.07", "−0.33", "0.65", "−0.21", "0.88", "0.04", "−0.57"];
  const DIMS = "4,096";
  const fmtv = (v) => (v < 0 ? "−" : "") + Math.abs(v);  // true minus sign

  // ---- the canonical frame ----
  const STEP = 240;                                     // one grid square = one step
  const FLOOR = 960;                                    // screen y of the origin
  const w = (e, n) => [e * STEP, -n * STEP];            // grid -> world (y runs toward the viewer)
  const at = (e, n, z = 0) => { const [x, y] = w(e, n); return P(x, y, z, FLOOR); };
  const DIRS = { E: [1, 0], N: [0, 1], W: [-1, 0], S: [0, -1], NW: [-1, 1] };
  // where each compass letter sits: past the unit arrow's tip, W and E nudged
  // below their axis so the 2-west step never runs through the "W"
  const COMPASS = { E: { e: 1.45, n: 0, dy: 40 }, N: { e: 0, n: 1.45, dy: 0 }, W: { e: -1.3, n: 0, dy: 70 }, S: { e: 0, n: -1.45, dy: 0 } };
  const CARD_TOP = 250;                                 // the vector card's top edge, every beat

  // the navy floor, grid aligned to the steps (ISO.ground with pitch STEP)
  function floor(g, o = {}) {
    const W = ISO.W, H = ISO.H;
    g.clearRect(0, 0, W, H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, W, H);
    g.strokeStyle = `rgba(74, 80, 112, ${o.alpha == null ? 0.30 : o.alpha})`; g.lineWidth = 3; g.beginPath();
    for (let k = -30; k <= 30; k++) {
      let p = P(k * STEP, -6000, 0, FLOOR), q = P(k * STEP, 6000, 0, FLOOR); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
      p = P(-6000, k * STEP, 0, FLOOR); q = P(6000, k * STEP, 0, FLOOR); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
    }
    g.stroke();
  }

  // A flat arrow on the floor from grid point a to b. o:
  //   col  RGB triple (default teal)   alpha  0..1
  //   u    draw progress 0..1 (the tip travels from a to b; the head appears with it)
  //   width shaft width in world units (default 44)   head  head length (default 90)
  //   glow 0..1 a soft halo under it (for the hero)
  function arrow(g, a, b, o = {}) {
    const u = o.u == null ? 1 : clamp01(o.u);
    if (u <= 0.001) return;
    const [x0, y0] = w(a[0], a[1]), [xb, yb] = w(b[0], b[1]);
    const x1 = lerp(x0, xb, u), y1 = lerp(y0, yb, u);
    const len = Math.hypot(x1 - x0, y1 - y0); if (len < 1) return;
    const dx = (x1 - x0) / len, dy = (y1 - y0) / len, nx = -dy, ny = dx;
    const hw = (o.width || 44) / 2, hl = Math.min(o.head || 90, len * 0.6), hh = hw * 2.6;
    const sx = x1 - dx * hl, sy = y1 - dy * hl, z = 2;
    const q = (x, y) => P(x, y, z, FLOOR);
    const col = o.col || COL.data, a1 = o.alpha == null ? 1 : o.alpha;
    if (o.glow) {
      [2.4, 1.7].forEach((k) => {   // two soft layers, not a hard box
        const gw = hw * k;
        ISO.poly(g, [q(x0 + nx * gw, y0 + ny * gw), q(x1 + nx * gw, y1 + ny * gw), q(x1 - nx * gw, y1 - ny * gw), q(x0 - nx * gw, y0 - ny * gw)], css(col, 1, 0.09 * o.glow * a1));
      });
    }
    const shaft = [q(x0 + nx * hw, y0 + ny * hw), q(sx + nx * hw, sy + ny * hw), q(sx - nx * hw, sy - ny * hw), q(x0 - nx * hw, y0 - ny * hw)];
    const head = [q(sx + nx * hh, sy + ny * hh), q(x1, y1), q(sx - nx * hh, sy - ny * hh)];
    ISO.poly(g, shaft, css(col, 1, a1));
    ISO.poly(g, head, css(col, 1, a1));
  }

  // a small puck standing on a grid point (the origin, a step mark)
  function puck(g, e, n, o = {}) {
    const [x, y] = w(e, n), h = o.half || 16;
    ISO.box(g, x - h, y - h, x + h, y + h, 0, o.z || 14, FLOOR, o.col || COL.text, { alpha: o.alpha == null ? 1 : o.alpha });
  }

  // A flat upright label centred on the screen point above grid (e, n).
  function label(root, text, o = {}) {
    const el = ISO.label(root, text, { size: o.size || 64, color: o.color, width: o.width || 240, align: "center" });
    el.style.left = "0px"; el.style.top = "0px";
    return el;
  }
  function place(el, e, n, o = {}) {
    const [sx, sy] = at(e, n, o.z || 0), wd = parseFloat(el.style.width) || 240, size = parseFloat(el.style.fontSize) || 64;
    const s = o.scale == null ? 1 : o.scale;
    el.style.transform = `translate(${(sx - wd / 2 + (o.dx || 0)).toFixed(1)}px, ${(sy - size * 0.55 + (o.dy || 0)).toFixed(1)}px) scale(${s.toFixed(4)})`;
    el.style.opacity = (o.alpha == null ? 1 : o.alpha).toFixed(3);
  }

  // The vector card: "[ a, b ]" on a flat panel, one span per slot so a slot
  // can light up, with optional labels under the slots. o: size (default 96),
  // mono (true: code look), name (e.g. "v =", drawn before the bracket),
  // labels (array under the slots). Position with el.style.transform.
  function vecCard(root, vals, o = {}) {
    const size = o.size || 96;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;padding:${Math.round(size * 0.2)}px ${Math.round(size * 0.4)}px;border-radius:24px;` +
      `background:${css(COL.panel)};border:6px solid ${css(COL.dim)};white-space:nowrap;transform-origin:50% 50%;` +
      `font-size:${size}px;line-height:${Math.round(size * 1.15)}px;color:${css(COL.text)};font-variant-numeric:tabular-nums;` +
      (o.mono ? "font-family:monospace;font-weight:700;" : "");
    const row = document.createElement("div"); row.style.cssText = "display:flex;align-items:flex-start;gap:0;";
    el.appendChild(row);
    const txt = (s, color) => { const d = document.createElement("span"); d.textContent = s; if (color) d.style.color = color; return d; };
    if (o.name) row.appendChild(txt(o.name + " ", css(COL.dim)));
    row.appendChild(txt("[ ", css(COL.dim)));
    const slots = [], labels = [];
    vals.forEach((v, i) => {
      const col = document.createElement("div"); col.style.cssText = "display:flex;flex-direction:column;align-items:center;";
      const s = txt(typeof v === "number" ? fmtv(v) : v); s.style.display = "block"; col.appendChild(s); slots.push(s);
      if (o.labels) {
        const l = document.createElement("div"); l.textContent = o.labels[i] || "";
        l.style.cssText = `font-size:60px;line-height:70px;color:${css(COL.dim)};font-family:"Inter",sans-serif;font-weight:800;`;
        col.appendChild(l); labels.push(l);
      }
      row.appendChild(col);
      if (i < vals.length - 1) row.appendChild(txt(", ", css(COL.dim)));
    });
    row.appendChild(txt(" ]", css(COL.dim)));
    root.appendChild(el);
    return {
      el, slots, labels,
      // light slot i: k 0..1 toward colour col (default hero); everything else at rest
      light(i, k, col = COL.hero) { slots[i].style.color = css(mix(COL.text, col, clamp01(k))); },
      border(col, k = 1) { el.style.borderColor = css(mix(COL.dim, col, clamp01(k))); },
      at(left, top, o2 = {}) {
        const s = o2.scale == null ? 1 : o2.scale;
        el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${s.toFixed(4)})`;
        el.style.opacity = (o2.alpha == null ? 1 : o2.alpha).toFixed(3);
      },
    };
  }
  // centre a card horizontally in the safe area at a given top
  const centreLeft = (el) => (ISO.SAFE.x0 + ISO.SAFE.x1) / 2 - el.offsetWidth / 2;

  window.VEC = { V, HOUSE, EMBED, DIMS, fmtv, STEP, FLOOR, CARD_TOP, DIRS, COMPASS, w, at, floor, arrow, puck, label, place, vecCard, centreLeft };
})();
