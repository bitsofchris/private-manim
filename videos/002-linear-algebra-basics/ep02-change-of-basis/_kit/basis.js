// basis.js — the shared kit for ep02 (change of basis).
//
// Every beat links this folder as `kit` (ln -s ../_kit NN_beat/kit) and
// loads <script src="kit/basis.js">, so the world, the lattice, the arrows,
// the address readout and the camera drift are identical from beat to beat
// and each beat opens on the previous beat's last frame.
//
// World: x, y on the floor, z up (right-handed). The view is an orthographic
// camera with a fixed elevation and a slow yaw drift that is a function of
// MASTER time (BK.setMaster(start) once, then everything takes beat-local t),
// so the drift is continuous across cuts. Everything is a pure function of
// its arguments: no clocks, no randomness.
(function () {
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const add = (p, q) => [p[0] + q[0], p[1] + q[1], p[2] + q[2]];
  const scale = (p, k) => [p[0] * k, p[1] * k, p[2] * k];
  const lerp3 = (p, q, u) => [lerp(p[0], q[0], u), lerp(p[1], q[1], u), lerp(p[2], q[2], u)];
  const rgba = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const mixc = (p, q, u) => [0, 1, 2].map((i) => Math.round(lerp(p[i], q[i], u)));

  // ---- palette (videos/_shared/style.py; blue is the iso kit's 2nd token colour) ----
  const COL = {
    bg: [11, 11, 20], panel: [20, 20, 43], text: [236, 235, 228], dim: [138, 143, 176],
    grid: [74, 80, 112], hero: [192, 132, 252],
    slots: [[45, 212, 191], [96, 165, 250], [224, 176, 64]], // teal, blue, gold: e1/v1, e2/v2, e3/v3
  };

  // ---- the ledger (storyboard.md) ----
  const E = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
  const V = [[1, 0, 0], [1, 1, 0], [1, 1, 1]];
  const P = [3, 5, 2];
  const ADDR_E = [3, 5, 2];
  const ADDR_V = [-2, 3, 2];
  const NAMES_E = ["x", "y", "z"];
  const NAMES_V = ["v1", "v2", "v3"];
  // 2D (beat 7)
  const U2 = [1, 1], D2 = [[1, 1], [-1, 1]], ADDR_U_E = [1, 1], ADDR_U_D = [1, 0];

  // basis part-way from standard (u=0) to new (u=1); each vector morphs to its partner
  const basisAt = (u) => [0, 1, 2].map((i) => lerp3(E[i], V[i], u));
  const combo = (B, c) => add(add(scale(B[0], c[0]), scale(B[1], c[1])), scale(B[2], c[2]));

  // ---- the view ----
  const W = 1080, H = 1920;
  const SAFE = { x0: 65, x1: 950, y0: 230, y1: 1536, stageBottom: 1100 };
  const BOX = { lo: [-2.5, -0.5, 0], hi: [4.5, 5.5, 2.5] };     // the lattice lives in here
  const VIEW = {
    cx: 507, cy: 760,          // screen point of the box centre
    centre: [1, 2.5, 1.25],
    s: 92,                     // px per world unit
    elev: 34 * Math.PI / 180,  // camera elevation
    yaw0: -32 * Math.PI / 180, // yaw at master t = 0
    drift: 7 * Math.PI / 180,  // +/- yaw drift amplitude
    period: 30,                // seconds per drift cycle
  };
  let master0 = 0, yaw = VIEW.yaw0;
  const setMaster = (start) => { master0 = start; };
  const yawAt = (t) => VIEW.yaw0 + VIEW.drift * Math.sin(2 * Math.PI * (master0 + t) / VIEW.period);
  const setTime = (t) => { yaw = yawAt(t); };
  // world -> screen
  const S = (p) => {
    const x = p[0] - VIEW.centre[0], y = p[1] - VIEW.centre[1], z = p[2] - VIEW.centre[2];
    const c = Math.cos(yaw), s = Math.sin(yaw);
    const X = x * c - y * s, D = x * s + y * c;   // D: depth, away from the viewer
    const ce = Math.cos(VIEW.elev), se = Math.sin(VIEW.elev);
    return [VIEW.cx + VIEW.s * X, VIEW.cy - VIEW.s * (z * ce + D * se)];
  };

  // ---- drawing (canvas) ----
  function clear(g) { g.fillStyle = rgba(COL.bg); g.fillRect(0, 0, W, H); }
  function line(g, a, b, color, width) {
    const p = S(a), q = S(b);
    g.strokeStyle = color; g.lineWidth = width; g.lineCap = "round";
    g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke();
  }
  // clip the line o + t*d to BOX; returns [t0, t1] or null (Liang-Barsky)
  function clipBox(o, d) {
    let t0 = -1e9, t1 = 1e9;
    for (let i = 0; i < 3; i++) {
      if (Math.abs(d[i]) < 1e-9) { if (o[i] < BOX.lo[i] - 1e-9 || o[i] > BOX.hi[i] + 1e-9) return null; continue; }
      let a = (BOX.lo[i] - o[i]) / d[i], b = (BOX.hi[i] - o[i]) / d[i];
      if (a > b) [a, b] = [b, a];
      t0 = Math.max(t0, a); t1 = Math.min(t1, b);
    }
    return t1 - t0 > 1e-6 ? [t0, t1] : null;
  }
  // The lattice of basis B: every line along one basis vector through an
  // integer combination of the other two, clipped to BOX.
  //   o.alpha (default 0.5), o.color (RGB, default COL.grid), o.width (default 2),
  //   o.grow 0..1 (lines reveal outward from the origin by their offset), o.families [0,1,2]
  function lattice(g, B, o = {}) {
    const alpha = o.alpha == null ? 0.5 : o.alpha, col = o.color || COL.grid, w = o.width || 2;
    const grow = o.grow == null ? 1 : o.grow, fams = o.families || [0, 1, 2];
    if (alpha <= 0) return;
    g.strokeStyle = rgba(col, alpha); g.lineWidth = w; g.lineCap = "round";
    g.beginPath();
    fams.forEach((a) => {
      const b = (a + 1) % 3, c = (a + 2) % 3;
      for (let m = -12; m <= 12; m++) for (let n = -12; n <= 12; n++) {
        if (grow < 1 && Math.max(Math.abs(m), Math.abs(n)) > grow * 9) continue;
        const off = add(scale(B[b], m), scale(B[c], n));
        const r = clipBox(off, B[a]);
        if (!r) continue;
        let [t0, t1] = r;
        if (grow < 1) { const reach = grow * 9; t0 = Math.max(t0, -reach); t1 = Math.min(t1, reach); if (t1 <= t0) continue; }
        const p = S(add(off, scale(B[a], t0))), q = S(add(off, scale(B[a], t1)));
        g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]);
      }
    });
    g.stroke();
  }
  // an arrow from world a to world b, drawn to fraction `progress`; head in px
  function arrow(g, a, b, color, o = {}) {
    const prog = o.progress == null ? 1 : o.progress, w = o.width || 9, head = o.head || 34;
    if (prog <= 0) return;
    const tip = lerp3(a, b, prog), p = S(a), q = S(tip);
    const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy);
    if (L < 1) return;
    const ux = dx / L, uy = dy / L, h = Math.min(head, L * 0.6);
    g.globalAlpha = o.alpha == null ? 1 : o.alpha;
    g.strokeStyle = color; g.fillStyle = color; g.lineWidth = w; g.lineCap = "round";
    g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0] - ux * h * 0.8, q[1] - uy * h * 0.8); g.stroke();
    g.beginPath(); g.moveTo(q[0], q[1]);
    g.lineTo(q[0] - ux * h - uy * h * 0.5, q[1] - uy * h + ux * h * 0.5);
    g.lineTo(q[0] - ux * h + uy * h * 0.5, q[1] - uy * h - ux * h * 0.5);
    g.closePath(); g.fill();
    g.globalAlpha = 1;
  }
  function dot(g, p, r, color, alpha = 1) {
    const q = S(p); g.globalAlpha = alpha; g.fillStyle = color;
    g.beginPath(); g.arc(q[0], q[1], r, 0, 2 * Math.PI); g.fill(); g.globalAlpha = 1;
  }
  function ring(g, p, r, color, alpha = 1, width = 6) {
    const q = S(p); g.globalAlpha = alpha; g.strokeStyle = color; g.lineWidth = width;
    g.beginPath(); g.arc(q[0], q[1], r, 0, 2 * Math.PI); g.stroke(); g.globalAlpha = 1;
  }
  // the flat plane through two basis vectors (the "independent" check), as a filled parallelogram
  function plane(g, b1, b2, color, alpha, ext = 2.2) {
    const pts = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([i, j]) => S(add(scale(b1, i * ext), scale(b2, j * ext))));
    g.globalAlpha = alpha; g.fillStyle = color;
    g.beginPath(); pts.forEach((p, i) => (i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]))); g.closePath(); g.fill();
    g.globalAlpha = 1;
  }

  // ---- the canonical frame ----
  // The world every 3D beat opens and closes on, at basis morph u (0 = x y z,
  // 1 = v1 v2 v3). o.lattice / o.basis / o.hero: alphas (default 1).
  // o.ghost: alpha of the standard lattice drawn faint underneath (default 0).
  const ARROW_W = { basis: 12, hero: 12 };
  function world(g, t, u, o = {}) {
    setTime(t); clear(g);
    const B = basisAt(u), a = (k, d = 1) => (o[k] == null ? d : o[k]);
    if (a("ghost", 0) > 0) lattice(g, E, { alpha: 0.25 * a("ghost", 0) });
    lattice(g, B, { alpha: 0.6 * a("lattice"), grow: o.grow });
    if (a("hero") > 0) {
      arrow(g, [0, 0, 0], P, rgba(COL.hero), { width: ARROW_W.hero, head: 40, alpha: a("hero"), progress: a("heroDraw") });
      if (a("heroDraw") >= 1) dot(g, P, 14, rgba(COL.hero), a("hero"));
    }
    // basis arrows over the hero: near the origin they share its first stretch
    if (a("basis") > 0) B.forEach((b, i) => arrow(g, [0, 0, 0], b, rgba(COL.slots[i]), { width: ARROW_W.basis, head: 30, alpha: a("basis") }));
    return B;
  }

  // ---- DOM parts (check audits DOM text) ----
  // The address readout: "(a, b, c)", each number in its slot colour.
  //   set(vals, o): vals may be fractional (they tick: shown rounded);
  //   o.alpha (whole readout), o.pulse [k0,k1,k2] (per-number scale 1..1.3),
  //   o.lit [..] per-number 0..1 (1 = full colour, 0 = dim), o.colors override.
  const MINUS = "−";
  function makeReadout(root, o = {}) {
    const n = o.n || 3, size = o.size || 110, top = o.top == null ? 262 : o.top;
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:65px;top:${top}px;width:885px;text-align:center;font-size:${size}px;` +
      `line-height:${Math.round(size * 1.15)}px;white-space:nowrap;color:${rgba(COL.text)};font-variant-numeric:tabular-nums;`;
    const nums = [];
    const span = (txt) => { const s = document.createElement("span"); s.textContent = txt; el.appendChild(s); return s; };
    span("(");
    for (let k = 0; k < n; k++) {
      const s = span("0"); s.style.display = "inline-block"; s.style.transformOrigin = "50% 60%"; nums.push(s);
      if (k < n - 1) span(", ");
    }
    span(")");
    root.appendChild(el);
    return {
      el, nums,
      set(vals, so = {}) {
        el.style.opacity = so.alpha == null ? 1 : so.alpha;
        nums.forEach((s, k) => {
          const v = Math.round(vals[k]);
          s.textContent = (v < 0 ? MINUS : "") + Math.abs(v);
          const base = (so.colors && so.colors[k]) || COL.slots[k];
          const lit = so.lit ? so.lit[k] : 1;
          s.style.color = rgba(mixc(COL.dim, base, lit));
          s.style.transform = `scale(${so.pulse ? so.pulse[k] : 1})`;
        });
      },
    };
  }
  // A world-anchored label (x, y, z, v1, ...): place(p3, dx, dy) each frame.
  function makeLabel(root, text, color, size = 64) {
    const el = document.createElement("div");
    el.textContent = text;
    el.style.cssText = `position:absolute;left:0;top:0;font-size:${size}px;line-height:${Math.round(size * 1.1)}px;` +
      `white-space:nowrap;color:${rgba(color)};`;
    root.appendChild(el);
    return {
      el,
      set text(v) { el.textContent = v; },
      place(p3, dx = 0, dy = 0, alpha = 1) {
        const q = S(p3), w = el.offsetWidth, h = el.offsetHeight;
        el.style.transform = `translate(${Math.round(q[0] + dx - w / 2)}px, ${Math.round(q[1] + dy - h / 2)}px)`;
        el.style.opacity = alpha;
      },
    };
  }
  // The three basis labels at the arrow tips, offset outward. place(B, u, alpha)
  // re-texts x/y/z -> v1/v2/v3 when the morph passes u = 0.5.
  const LABEL_OFF = [[14, 52], [58, 34], [-46, -14]]; // px offsets from each tip
  function makeBasisLabels(root) {
    const ls = [0, 1, 2].map((i) => makeLabel(root, NAMES_E[i], COL.slots[i]));
    return {
      ls,
      place(B, u, alpha = 1) {
        ls.forEach((l, i) => {
          l.el.textContent = u < 0.5 ? NAMES_E[i] : NAMES_V[i];
          const tip = scale(B[i], 1.0);
          l.place(tip, LABEL_OFF[i][0], LABEL_OFF[i][1], alpha);
        });
      },
    };
  }
  function guides(root) {
    if (!/[?&]guides/.test(location.search)) return;
    [[0, 0, 1080, 230], [0, 1536, 1080, 384], [950, 230, 130, 1306], [0, 230, 65, 1306]].forEach(([l, t, w, h]) => {
      const d = document.createElement("div");
      d.style.cssText = `position:absolute;left:${l}px;top:${t}px;width:${w}px;height:${h}px;background:rgba(255,60,60,0.18);pointer-events:none;`;
      root.appendChild(d);
    });
  }
  const ease = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"),
                        back: gsap.parseEase("back.out(1.6)"), sine: gsap.parseEase("sine.inOut") });
  // a 0 -> 1 -> 0 bump over [a, a + d] (for pulses)
  const bump = (t, a, d) => { const u = seg(t, a, a + d); return Math.sin(Math.PI * u); };

  window.BK = { W, H, SAFE, BOX, VIEW, COL, E, V, P, ADDR_E, ADDR_V, NAMES_E, NAMES_V, U2, D2, ADDR_U_E, ADDR_U_D,
                basisAt, combo, setMaster, setTime, yawAt, S, clear, line, lattice, arrow, dot, ring, plane, world, ARROW_W,
                makeReadout, makeLabel, makeBasisLabels, guides, ease, bump,
                lerp, lerp3, clamp01, seg, add, scale, rgba, mixc };
})();
