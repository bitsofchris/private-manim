// iso.js — the shared isometric kit for 009-transformer-short-iso.
//
// Every beat loads this (through its `iso` symlink) so the world, the tray,
// the readout card and the palette are identical from beat to beat, and each
// beat can open on the previous beat's last frame. Beats draw their own extra
// parts on the same canvas with ISO.P / ISO.box / ISO.poly.
//
// World: x runs right (token index), y runs toward the viewer (row index),
// z is up. Screen = ISO.P(x, y, z, oy): `oy` is the screen y of the world
// origin at z = 0. Everything is a pure function of the arguments: no clocks,
// no randomness (use ISO.hash).
(function () {
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const round1 = (v) => { const r = Math.round(v * 10) / 10; return r === 0 ? 0 : r; };
  const fmt = (v) => { const r = round1(v); return (r < 0 ? "−" : "") + Math.abs(r).toFixed(1); };
  const mix = (p, q, u) => [lerp(p[0], q[0], u), lerp(p[1], q[1], u), lerp(p[2], q[2], u)];
  const css = (c, k = 1, a = 1) => `rgba(${Math.round(c[0] * k)},${Math.round(c[1] * k)},${Math.round(c[2] * k)},${a})`;

  // House palette (videos/_shared/style.py), as RGB triples for the canvas.
  const COL = {
    bg: [11, 11, 20], panel: [20, 20, 43], text: [236, 235, 228], dim: [138, 143, 176],
    data: [45, 212, 191], hero: [192, 132, 252], muted: [74, 80, 112],
    // slabs: panel tones lifted so they stand off the navy
    slabTop: [86, 88, 150], slabA: [60, 61, 112], slabB: [43, 44, 86], slabEdge: [150, 154, 200],
    plate: [26, 26, 54], neg: [74, 80, 112],
    // one colour per token (column): my, name, is. A tile, its word and its
    // digits share it, so a column reads as belonging to its word. Magenta
    // stays free for the hero. (teal = HERO_TEAL, gold = CONTENT_GOLD in
    // style.py; the blue is new here.)
    tokens: [[45, 212, 191], [96, 165, 250], [224, 176, 64]],
  };

  // ---- the data: values[col][row], one stage per step of the Short ----
  const TOKENS = ["my", "name", "is"];
  const TARGET = 2; // "is" is the token that attends
  const VALUES = {
    embed:     [[0.2, 0.7, 0.5], [-0.5, -0.4, 0.7], [-0.9, 0.6, 0.5]],   // beats 1-3
    update:    [-0.4, -0.1, -0.1],                                          // attention's result for "is" (beat 3-4)
    afterAttn: [[0.2, 0.7, 0.5], [-0.5, -0.4, 0.7], [-0.4, -0.1, -0.1]],  // end of beat 4
    afterFfn:  [[0.4, 0.6, -0.4], [-0.6, -0.2, 0.8], [0.1, 0.4, -0.5]],   // end of beat 5
    afterStack:[[0.0, 0.3, 0.2], [-0.2, -0.6, 0.1], [0.6, -0.2, 0.1]],    // end of beat 6, beat 7
  };
  const ATTN_WEIGHTS = [0.3, 0.55, 0.15];                 // my, name, is(self) into "is"
  const NEXT_TOKENS = [["Chris", 0.58], ["Sam", 0.27], ["not", 0.09]];
  const lerpVals = (a, b, u) => a.map((col, c) => col.map((v, r) => lerp(v, b[c][r], u)));

  // ---- the view ----
  const W = 1080, H = 1920;
  const SAFE = { x0: 65, x1: 950, y0: 230, y1: 1536, stageBottom: 1100 };
  const VIEW = { cx: 507, A: 0.866, B: 0.30, theta: -20 * Math.PI / 180 };
  let cosT = Math.cos(VIEW.theta), sinT = Math.sin(VIEW.theta);
  const setTheta = (rad) => { VIEW.theta = rad; cosT = Math.cos(rad); sinT = Math.sin(rad); };
  const P = (x, y, z, oy) => {
    const xr = x * cosT - y * sinT, yr = x * sinT + y * cosT;
    return [VIEW.cx + (xr - yr) * VIEW.A, oy + (xr + yr) * VIEW.B - z];
  };

  // ---- canonical layout: where the matrix lives in every beat ----
  const TILE = 100, GAP = 12, PITCH = TILE + GAP, PLATE = 8;
  const P2 = (3 * TILE + 2 * GAP) / 2 + 10;          // tray half-side
  const TRAY_Y = 700;                                // screen y of the tray's centre (oy)
  const GROUND_Y = 1010;                             // screen y of the floor under the tray
  const CARD = { left: 234, top: 236, width: 546, height: 258 };
  const tileRect = (c, r) => { const x0 = -P2 + 10 + c * PITCH, y0 = -P2 + 10 + r * PITCH; return [x0, y0, x0 + TILE, y0 + TILE]; };
  const tileHeight = (v) => 8 + Math.abs(v) * 62;
  // colour is the token; a negative value is a darker shade of the same colour
  const tileColor = (v, c = 0) => mix(mix(COL.tokens[c], COL.plate, 0.58), COL.tokens[c], clamp01(v / 0.12 * 0.5 + 0.5));
  const digitColor = (v, c = 0) => (round1(v) < 0 ? mix(COL.tokens[c], COL.panel, 0.38) : COL.tokens[c]);
  // screen point above the middle of token c's line of tiles, at height z
  const tokenPoint = (c, z = 0, oy = TRAY_Y) => { const [x0, , x1] = tileRect(c, 1); return P((x0 + x1) / 2, 0, z, oy); };
  const tilePoint = (c, r, z = 0, oy = TRAY_Y) => { const [x0, y0, x1, y1] = tileRect(c, r); return P((x0 + x1) / 2, (y0 + y1) / 2, z, oy); };

  // ---- drawing ----
  function poly(g, pts, fill, stroke) {
    g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); g.closePath();
    g.fillStyle = fill; g.fill();
    g.strokeStyle = stroke || fill; g.lineWidth = stroke ? 2 : 1; g.lineJoin = "round"; g.stroke(); // hides seams
  }
  // an axis-aligned box: top face + the two faces toward the viewer
  function box(g, x0, y0, x1, y1, zb, zt, oy, col, opts = {}) {
    const k = opts.shade || [1, 0.8, 0.62], a = opts.alpha == null ? 1 : opts.alpha;
    poly(g, [P(x1, y0, zt, oy), P(x1, y1, zt, oy), P(x1, y1, zb, oy), P(x1, y0, zb, oy)], css(col, k[1], a));
    poly(g, [P(x0, y1, zt, oy), P(x1, y1, zt, oy), P(x1, y1, zb, oy), P(x0, y1, zb, oy)], css(col, k[2], a));
    poly(g, [P(x0, y0, zt, oy), P(x1, y0, zt, oy), P(x1, y1, zt, oy), P(x0, y1, zt, oy)], css(col, k[0], a), opts.edge);
  }
  function ground(g, groundY = GROUND_Y) {
    g.clearRect(0, 0, W, H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, W, H);
    g.strokeStyle = "rgba(74, 80, 112, 0.26)"; g.lineWidth = 3; g.beginPath();
    for (let k = -40; k <= 40; k++) {
      let p = P(k * 140, -6000, 0, groundY), q = P(k * 140, 6000, 0, groundY); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
      p = P(-6000, k * 140, 0, groundY); q = P(6000, k * 140, 0, groundY); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
    }
    g.stroke();
  }
  // soft teal patch on the floor under something at half-side `half`
  function shadow(g, half, groundY = GROUND_Y, alpha = 0.12, cx = 0, cy = 0) {
    poly(g, [P(cx - half, cy - half, 0, groundY), P(cx + half, cy - half, 0, groundY), P(cx + half, cy + half, 0, groundY), P(cx - half, cy + half, 0, groundY)], css(COL.data, 1, alpha));
  }
  // The matrix as a tray of tiles. vals[col][row]. opts:
  //   oy        screen y of the tray centre (default TRAY_Y)
  //   scale     uniform scale about the tray centre (default 1)
  //   alpha     whole-tray opacity
  //   plate     false to draw tiles only
  //   color(c, r, v) -> RGB triple to override a tile's colour (return null for default)
  //   lift(c, r)     -> extra z for a tile (e.g. a column rising)
  //   show(c, r)     -> false to skip a tile
  function tray(g, vals, opts = {}) {
    const oy = opts.oy == null ? TRAY_Y : opts.oy, s = opts.scale == null ? 1 : opts.scale;
    const prevA = g.globalAlpha; if (opts.alpha != null) g.globalAlpha = prevA * opts.alpha;
    if (opts.plate !== false) box(g, -P2 * s, -P2 * s, P2 * s, P2 * s, 0, PLATE * s, oy, COL.plate, { shade: [1, 0.7, 0.5], edge: css(COL.muted) });
    const order = [];
    for (let c = 0; c < 3; c++) for (let r = 0; r < 3; r++) order.push([c, r]);
    order.sort((p, q) => (p[0] + p[1]) - (q[0] + q[1]) || p[1] - q[1]); // back to front
    order.forEach(([c, r]) => {
      if (opts.show && opts.show(c, r) === false) return;
      const v = vals[c][r], [x0, y0, x1, y1] = tileRect(c, r);
      const col = (opts.color && opts.color(c, r, v)) || tileColor(v, c);
      const z0 = PLATE + (opts.lift ? opts.lift(c, r) : 0);
      box(g, x0 * s, y0 * s, x1 * s, y1 * s, z0 * s, (z0 + tileHeight(v)) * s, oy, col);
    });
    g.globalAlpha = prevA;
  }
  // A square ring slab (a transformer block the tray can pass through), drawn
  // in two halves so the tray can be painted between them:
  //   slabBack(...); tray(...); slabFront(...);
  // half = outer half-side, hole = inner half-side, thick = thickness,
  // glow 0..1 mixes the slab toward magenta (the block at work).
  function slabBack(g, oy, o = {}) {
    const half = o.half || 250, hole = o.hole || 195, thick = o.thick || 40, glow = o.glow || 0;
    const top = css(mix(COL.slabTop, COL.hero, glow));
    g.beginPath();
    [[-half, -half], [half, -half], [half, half], [-half, half]].forEach(([x, y], i) => { const p = P(x, y, 0, oy); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); });
    g.closePath();
    [[-hole, -hole], [-hole, hole], [hole, hole], [hole, -hole]].forEach(([x, y], i) => { const p = P(x, y, 0, oy); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); });
    g.closePath(); g.fillStyle = top; g.fill("evenodd");
    poly(g, [P(-hole, -hole, 0, oy), P(-hole, hole, 0, oy), P(-hole, hole, -thick, oy), P(-hole, -hole, -thick, oy)], css(mix(COL.slabA, COL.hero, glow * 0.3), 0.8));
    poly(g, [P(-hole, -hole, 0, oy), P(hole, -hole, 0, oy), P(hole, -hole, -thick, oy), P(-hole, -hole, -thick, oy)], css(mix(COL.slabB, COL.hero, glow * 0.2), 0.8));
  }
  function slabFront(g, oy, o = {}) {
    const half = o.half || 250, hole = o.hole || 195, thick = o.thick || 40, glow = o.glow || 0;
    const top = css(mix(COL.slabTop, COL.hero, glow)), edge = css(mix(COL.slabEdge, COL.hero, glow));
    poly(g, [P(half, -half, 0, oy), P(half, half, 0, oy), P(half, half, -thick, oy), P(half, -half, -thick, oy)], css(mix(COL.slabA, COL.hero, glow * 0.35)));
    poly(g, [P(-half, half, 0, oy), P(half, half, 0, oy), P(half, half, -thick, oy), P(-half, half, -thick, oy)], css(mix(COL.slabB, COL.hero, glow * 0.25)));
    poly(g, [P(hole, -half, 0, oy), P(half, -half, 0, oy), P(half, half, 0, oy), P(-half, half, 0, oy), P(-half, hole, 0, oy), P(hole, hole, 0, oy)], top);
    // a light line on the outer top edges so the slab reads at phone size
    g.strokeStyle = edge; g.lineWidth = 3; g.beginPath();
    [[-half, -half], [half, -half], [half, half], [-half, half], [-half, -half]].forEach(([x, y], i) => { const p = P(x, y, 0, oy); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); });
    g.stroke();
  }

  // ---- flat DOM parts (HyperFrames' check audits DOM text) ----
  // The readout card: the words and the nine numbers, flat, top of the stage.
  // set(vals, opts): opts.flash 0..1 (all digits toward off-white),
  // opts.color(c, r, v) -> css colour string to override one digit.
  function makeCard(root, o = {}) {
    const el = document.createElement("div");
    const box = Object.assign({}, CARD, o);
    el.style.cssText = `position:absolute;left:${box.left}px;top:${box.top}px;width:${box.width}px;height:${box.height}px;` +
      `border-radius:20px;background:${css(COL.panel)};border:5px solid ${css(COL.dim)};padding:0 9px;transform-origin:50% 50%;`;
    const row = (cls) => { const r = document.createElement("div"); r.style.cssText = "display:flex;justify-content:space-between;height:62px;"; el.appendChild(r); return r; };
    const cell = (parent, size) => { const d = document.createElement("div"); d.style.cssText = `width:166px;text-align:center;font-size:${size}px;line-height:62px;letter-spacing:-1px;font-variant-numeric:tabular-nums;`; parent.appendChild(d); return d; };
    const wrow = row(), words = TOKENS.map((w) => { const d = cell(wrow, 60); d.textContent = w; d.style.color = css(COL.tokens[TOKENS.indexOf(w)]); return d; });
    const digits = [];
    for (let r = 0; r < 3; r++) { const rr = row(); for (let c = 0; c < 3; c++) digits.push({ el: cell(rr, 64), c, r }); }
    root.appendChild(el);
    return {
      el, words, digits,
      set(vals, opts = {}) {
        digits.forEach(({ el: d, c, r }) => {
          const v = round1(vals[c][r]);
          d.textContent = fmt(v);
          const base = digitColor(v, c);
          d.style.color = (opts.color && opts.color(c, r, v)) || css(mix(base, COL.text, opts.flash || 0));
        });
      },
    };
  }
  // A flat label. Position with left/top in px; the caller animates
  // el.style.transform / opacity / color inside render(t).
  function label(root, text, o = {}) {
    const el = document.createElement("div");
    const size = o.size || 64;
    el.textContent = text;
    el.style.cssText = `position:absolute;left:${o.left || 0}px;top:${o.top || 0}px;font-size:${size}px;line-height:${Math.round(size * 1.1)}px;` +
      `white-space:nowrap;color:${o.color || css(COL.text)};` + (o.width ? `width:${o.width}px;text-align:${o.align || "center"};` : "");
    root.appendChild(el);
    return el;
  }
  function guides(root) {
    if (!/[?&]guides/.test(location.search)) return;
    [[0, 0, 1080, 230], [0, 1536, 1080, 384], [950, 230, 130, 1306], [0, 230, 65, 1306]].forEach(([l, t, w, h]) => {
      const d = document.createElement("div");
      d.style.cssText = `position:absolute;left:${l}px;top:${t}px;width:${w}px;height:${h}px;background:rgba(255,60,60,0.18);pointer-events:none;`;
      root.appendChild(d);
    });
  }
  // Register the beat: one paused timeline whose only job is to be the clock.
  function start(seconds, render) {
    const clock = { p: 0 };
    const tl = gsap.timeline({ paused: true, onUpdate: () => render(tl.time()) });
    tl.to(clock, { p: 1, duration: seconds, ease: "none" }, 0);
    tl.set({}, {}, seconds);
    window.__timelines = window.__timelines || {};
    window.__timelines["main"] = tl;
    tl.seek(0); render(0);
    // Draw again once the fonts are in: a frame drawn before Inter loads measures
    // DOM text in the fallback face (a snapshot at t = 0 showed cards ~66 px off).
    // Renders seek every frame, so this only changes snapshots and previews.
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => render(tl.time()));
    return tl;
  }
  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });

  window.ISO = { W, H, SAFE, VIEW, setTheta, P, COL, TOKENS, TARGET, VALUES, ATTN_WEIGHTS, NEXT_TOKENS, lerpVals,
                 TILE, GAP, PITCH, PLATE, P2, TRAY_Y, GROUND_Y, CARD, tileRect, tileHeight, tileColor, digitColor, tokenPoint, tilePoint,
                 poly, box, ground, shadow, tray, slabBack, slabFront, makeCard, label, guides, start, E,
                 lerp, clamp01, seg, hash, round1, fmt, mix, css };
})();
