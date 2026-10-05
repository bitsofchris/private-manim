// diagram.js — the transformer block diagram as an isometric object, for
// 010-diagram-grammar-iso. Loaded after iso.js (the shared kit from 009).
//
// It is the same figure as videos/_shared/transformer.py, mark for mark, so
// the Short stays accurate about what it teaches: bottom to top
//   Embed -> [ Attention -> (+) -> FFN -> (+) ] N×  -> Linear
// Boxes are operations, arrows are tensors moving UP to the next operation, a
// line that leaves the main line below a box and re-enters at the (+) above it
// is the residual (skip) path, the circle with a plus is the add, and the
// bracket with N× spans the repeated block. Skips run on the right and the
// bracket on the left, as in the Manim diagram.
//
// The figure is drawn on one upright plane (the front faces of the boxes);
// the boxes are extruded back from that plane, so arrows, (+) nodes, skips and
// the bracket are never hidden. Everything is a pure function of its inputs.
(function () {
  const { P, COL, mix, css, clamp01, lerp } = ISO;

  // ---- layout, world units: x right, z up, plane at y = DEPTH (front faces) ----
  const X0 = 22;                 // shifts the column right so bracket + N× fit on the left
  const BASE_Y = 1040;           // screen y of z = 0 at the column centre
  const HALF = 190, DEPTH = 22;  // box half-width, half-depth
  const BOX_H = 88, ADD_R = 30;
  // rows bottom to top: z of each part
  const Z = { embed: 0, attn: 138, add1: 300, ffn: 374, add2: 536, head: 616 };
  const BOXES = [["embed", "Embed"], ["attn", "Attention"], ["ffn", "FFN"], ["head", "Linear"]];
  const TOP = Z.head + BOX_H;
  const SKIP_X = HALF + 78;      // how far right of the column the skip path runs
  const BRACKET_X = -HALF - 46, BRACKET_Z = [Z.attn - 14, Z.add2 + ADD_R + 14];
  // the five main-line arrows [from z, to z]: each is a tensor moving up
  const ARROWS = [[Z.embed + BOX_H, Z.attn], [Z.attn + BOX_H, Z.add1 - ADD_R], [Z.add1 + ADD_R, Z.ffn],
                  [Z.ffn + BOX_H, Z.add2 - ADD_R], [Z.add2 + ADD_R, Z.head]];
  // the two skips: leave the main line at `from` (below the box), re-enter the (+) at `to`
  const SKIPS = [{ from: (Z.embed + BOX_H + Z.attn) / 2, to: Z.add1 }, { from: (Z.add1 + ADD_R + Z.ffn) / 2, to: Z.add2 }];

  // a point on the figure plane -> screen. yOff moves the whole figure back (-) or forward (+).
  const pt = (x, z, yOff = 0) => P(x + X0, DEPTH + yOff, z, BASE_Y);
  // screen-space shear of the plane, for laying flat text on it
  const SHEAR = (pt(100, 0)[1] - pt(0, 0)[1]) / (pt(100, 0)[0] - pt(0, 0)[0]);
  const XS = (pt(100, 0)[0] - pt(0, 0)[0]) / 100; // screen px per world x

  const boxCenter = (name, yOff = 0) => pt(0, Z[name] + BOX_H / 2, yOff);
  const addCenter = (i, yOff = 0) => pt(0, i ? Z.add2 : Z.add1, yOff);
  // skip i as a polyline of plane points [x, z]
  const skipPath = (i) => { const s = SKIPS[i]; return [[0, s.from], [SKIP_X, s.from], [SKIP_X, s.to], [ADD_R, s.to]]; };
  // a point along a polyline of plane points, u in 0..1 by length
  function along(pts, u) {
    const seg = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
    let d = clamp01(u) * seg.reduce((a, b) => a + b, 0);
    for (let i = 0; i < seg.length; i++) { if (d <= seg[i] || i === seg.length - 1) { const k = seg[i] ? d / seg[i] : 0; return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)]; } d -= seg[i]; }
  }
  // the main line, bottom of Embed to top of Linear, as plane points
  const MAIN = [[0, 0], [0, TOP]];
  const mainPoint = (u, yOff = 0) => pt(0, lerp(0, TOP, clamp01(u)), yOff);
  const mainU = (z) => z / TOP; // u at which the main line is at height z

  // ---- drawing ----
  function strokePath(g, pts, style, width, yOff, head) {
    g.strokeStyle = style; g.lineWidth = width; g.lineCap = "round"; g.lineJoin = "round";
    g.beginPath(); pts.forEach(([x, z], i) => { const p = pt(x, z, yOff); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); }); g.stroke();
    if (head) {
      const [x1, z1] = pts[pts.length - 1], [x0, z0] = pts[pts.length - 2];
      const dx = Math.sign(x1 - x0), dz = Math.sign(z1 - z0), s = head;
      const tip = pt(x1, z1, yOff), a = pt(x1 - dx * s - dz * s * 0.62, z1 - dz * s - dx * s * 0.62, yOff), b = pt(x1 - dx * s + dz * s * 0.62, z1 - dz * s + dx * s * 0.62, yOff);
      g.fillStyle = style; g.beginPath(); g.moveTo(tip[0], tip[1]); g.lineTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.closePath(); g.fill(); g.stroke();
    }
  }
  function drawBox(g, name, hero, alpha, yOff) {
    const z0 = Z[name], z1 = z0 + BOX_H, y0 = -DEPTH + yOff, y1 = DEPTH + yOff;
    const prev = g.globalAlpha; g.globalAlpha = prev * alpha;
    const edge = css(mix(COL.slabEdge, COL.hero, hero));
    const q = (x, y, z) => P(x + X0, y, z, BASE_Y);
    ISO.poly(g, [q(HALF, y0, z1), q(HALF, y1, z1), q(HALF, y1, z0), q(HALF, y0, z0)], css(mix(COL.slabA, COL.hero, hero * 0.25), 0.8));       // right side
    ISO.poly(g, [q(-HALF, y0, z1), q(HALF, y0, z1), q(HALF, y1, z1), q(-HALF, y1, z1)], css(mix(COL.slabTop, COL.hero, hero * 0.55)));        // top
    ISO.poly(g, [q(-HALF, y1, z1), q(HALF, y1, z1), q(HALF, y1, z0), q(-HALF, y1, z0)], css(mix(COL.panel, COL.hero, hero * 0.22), 1.25), edge); // front: the box of the figure
    g.lineWidth = 4 + 3 * hero; g.strokeStyle = edge; g.beginPath();
    [[-HALF, z1], [HALF, z1], [HALF, z0], [-HALF, z0], [-HALF, z1]].forEach(([x, z], i) => { const p = pt(x, z, yOff); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); });
    g.stroke(); g.globalAlpha = prev;
  }
  function drawAdd(g, i, hero, alpha, yOff) {
    const zc = i ? Z.add2 : Z.add1, prev = g.globalAlpha; g.globalAlpha = prev * alpha;
    const col = css(mix(COL.dim, COL.hero, hero));
    g.beginPath();
    for (let k = 0; k <= 40; k++) { const a = (k / 40) * Math.PI * 2, p = pt(Math.cos(a) * ADD_R, zc + Math.sin(a) * ADD_R, yOff); k ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); }
    g.closePath(); g.fillStyle = css(mix(COL.panel, COL.hero, hero * 0.2)); g.fill(); g.lineWidth = 5 + 2 * hero; g.strokeStyle = col; g.stroke();
    strokePath(g, [[-ADD_R * 0.52, zc], [ADD_R * 0.52, zc]], col, 5, yOff);
    strokePath(g, [[0, zc - ADD_R * 0.52], [0, zc + ADD_R * 0.52]], col, 5, yOff);
    g.globalAlpha = prev;
  }
  // The whole figure. st (all optional):
  //   boxes   {embed, attn, ffn, head}: hero 0..1 per box (or one number for all)
  //   arrows  hero 0..1 for the five main arrows (number, or array of five)
  //   skips   [h0, h1]   adds [h0, h1]   bracket h
  //   alpha   whole-figure opacity      yOff  move the figure in depth (ghost copies)
  //   reveal  0..1: only what lies below this fraction of the height is drawn (the draw-in)
  //   only    "block" to draw just the repeated block (Attention..second (+)) with its arrows and skips
  function draw(g, st = {}) {
    const yOff = st.yOff || 0, A = st.alpha == null ? 1 : st.alpha, rev = st.reveal == null ? 1 : st.reveal;
    const vis = (z) => clamp01((rev * (TOP + 60) - z) / 60) * A;         // soft edge of the draw-in
    const hb = (n) => (typeof st.boxes === "number" ? st.boxes : (st.boxes && st.boxes[n]) || 0);
    const ha = (i) => (Array.isArray(st.arrows) ? st.arrows[i] || 0 : st.arrows || 0);
    const block = st.only === "block";
    const prev = g.globalAlpha;
    // bracket (left): a square bracket spanning the repeated block
    const hk = st.bracket || 0, bk = vis((BRACKET_Z[0] + BRACKET_Z[1]) / 2);
    if (bk > 0 && !block) { g.globalAlpha = prev * bk; strokePath(g, [[BRACKET_X + 20, BRACKET_Z[0]], [BRACKET_X, BRACKET_Z[0]], [BRACKET_X, BRACKET_Z[1]], [BRACKET_X + 20, BRACKET_Z[1]]], css(mix(COL.dim, COL.hero, hk)), 5 + 2 * hk, yOff); g.globalAlpha = prev; }
    // boxes, bottom to top
    BOXES.forEach(([n]) => { if (block && (n === "embed" || n === "head")) return; const a = vis(Z[n] + BOX_H / 2); if (a > 0) drawBox(g, n, hb(n), a, yOff); });
    // skips (behind the arrows)
    SKIPS.forEach((s, i) => { const a = vis(s.to), h = (st.skips && st.skips[i]) || 0; if (a <= 0) return; g.globalAlpha = prev * a; strokePath(g, skipPath(i), css(mix(COL.dim, COL.hero, h)), 5 + 2 * h, yOff, 13); g.globalAlpha = prev; });
    // main-line arrows: tensors moving up
    ARROWS.forEach(([z0, z1], i) => { if (block && (i === 0 || i === 4)) return; const a = vis(z1), h = ha(i); if (a <= 0) return; g.globalAlpha = prev * a; strokePath(g, [[0, z0 + 3], [0, z1 - 5]], css(mix(COL.data, COL.hero, h)), 6 + 2 * h, yOff, 15); g.globalAlpha = prev; });
    // (+) nodes
    [0, 1].forEach((i) => { const a = vis(i ? Z.add2 : Z.add1); if (a > 0) drawAdd(g, i, (st.adds && st.adds[i]) || 0, a, yOff); });
    g.globalAlpha = prev;
  }
  // a glowing token riding the figure, at a screen point
  function token(g, p, r = 16, col = COL.data, alpha = 1) {
    const prev = g.globalAlpha; g.globalAlpha = prev * alpha;
    g.fillStyle = css(col, 1, 0.25); g.beginPath(); g.arc(p[0], p[1], r * 1.9, 0, Math.PI * 2); g.fill();
    g.fillStyle = css(mix(col, COL.text, 0.25)); g.beginPath(); g.arc(p[0], p[1], r, 0, Math.PI * 2); g.fill();
    g.globalAlpha = prev;
  }

  // ---- flat labels, laid on the figure plane (sheared to match it) ----
  // Returns { embed, attn, ffn, head, n } DOM elements. Style them in render(t)
  // with DG.styleLabels, or directly (opacity, color; keep the transform).
  function makeLabels(root) {
    const out = {};
    const place = (text, x, z, size, color) => {
      const el = document.createElement("div"), c = pt(x, z), w = 420;
      el.textContent = text;
      el.style.cssText = `position:absolute;left:${(c[0] - w / 2).toFixed(1)}px;top:${(c[1] - size * 0.6).toFixed(1)}px;width:${w}px;height:${Math.round(size * 1.2)}px;` +
        `text-align:center;font-size:${size}px;line-height:${Math.round(size * 1.2)}px;white-space:nowrap;color:${color};` +
        `transform:matrix(1, ${SHEAR.toFixed(4)}, 0, 1, 0, 0);transform-origin:50% 50%;`;
      // the label sits on the canvas-drawn box on purpose; the layout audit reads that as occlusion
      el.setAttribute("data-layout-allow-occlusion", "");
      root.appendChild(el); return el;
    };
    BOXES.forEach(([n, text]) => { out[n] = place(text, 0, Z[n] + BOX_H / 2, 60, css(COL.text)); });
    out.n = place("N×", BRACKET_X - 62, (BRACKET_Z[0] + BRACKET_Z[1]) / 2, 64, css(COL.dim));
    return out;
  }
  // Match the labels to a draw state: same `boxes`, `bracket`, `alpha`, `reveal`.
  function styleLabels(labels, st = {}) {
    const A = st.alpha == null ? 1 : st.alpha, rev = st.reveal == null ? 1 : st.reveal;
    const vis = (z) => clamp01((rev * (TOP + 60) - z) / 60) * A;
    BOXES.forEach(([n]) => {
      const h = typeof st.boxes === "number" ? st.boxes : (st.boxes && st.boxes[n]) || 0;
      labels[n].style.opacity = vis(Z[n] + BOX_H / 2).toFixed(3);
      labels[n].style.color = css(mix(COL.text, [255, 255, 255], h * 0.6));
    });
    labels.n.style.opacity = vis((BRACKET_Z[0] + BRACKET_Z[1]) / 2).toFixed(3);
    labels.n.style.color = css(mix(COL.dim, COL.hero, st.bracket || 0));
  }
  // The canonical frame of this Short: the complete figure at rest.
  function canon(g, labels) { ISO.ground(g, BASE_Y + 8); draw(g, {}); styleLabels(labels, {}); }

  window.DG = { X0, BASE_Y, HALF, DEPTH, BOX_H, ADD_R, Z, BOXES, TOP, SKIP_X, BRACKET_X, BRACKET_Z, ARROWS, SKIPS, SHEAR, XS,
                pt, boxCenter, addCenter, skipPath, along, MAIN, mainPoint, mainU, strokePath, draw, token, makeLabels, styleLabels, canon };
})();
