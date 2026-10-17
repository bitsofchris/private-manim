// score.js — the shared kit for 013 ep03 (the threshold and the ROC curve).
//
// Started from ep01's kit (score line, dots, tag, the box), with the
// threshold now a moving value and two new parts: the code line and the ROC
// plot. Every beat loads this (through its `kit` symlink, after kit/dots.js)
// and draws one state object per frame with K.draw(g, S), so each beat opens
// on the previous beat's last frame (SEAM). Pure functions of their
// arguments: no clocks, no randomness. Every count comes from the dots
// (`s > t` on the seed-13 scores), which reproduce the ledger stops exactly.
//
// Layout (px, 1080×1920; captions anchored bottom, so the stage runs to 1330):
//   tag            y 240–372   two lines, left at x 120
//   user pile      y 400–587   teal, above the axis
//   axis           y 590       score 0 at x 120, 1 at x 920
//   attack pile    y 602–673   gold, below the axis
//   axis labels    y 690–756
//   code line      y 772–848   `pred = scores > 0.70`, centred
//   box            x 70–500    headers y 862, cells y 936–1326
//   ROC plot       x 600–930, y 920–1250 (0,0 bottom-left); labels to y 1328
(function () {
  const D = window.SCORE_DOTS;
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const pulse = (t, at, w = 0.6) => { const u = (t - at) / w; return u < 0 || u > 1 ? 0 : Math.sin(Math.PI * u); };
  const rgba = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  // opacity, and hidden at 0 so `check` doesn't count invisible text as overlapping
  const show = (e, a) => { e.style.opacity = a; e.style.visibility = a > 0.001 ? "visible" : "hidden"; };
  const mixc = (p, q, u) => [0, 1, 2].map((k) => Math.round(lerp(p[k], q[k], u)));

  // House palette (videos/_shared/style.py). ATTACK = CONTENT_GOLD.
  const COL = {
    bg: [11, 11, 20], panel: [20, 20, 43], text: [236, 235, 228], dim: [138, 143, 176],
    data: [45, 212, 191], hero: [192, 132, 252], muted: [74, 80, 112], attack: [224, 176, 64],
  };
  const W = 1080, H = 1920;
  const X0 = D.x0, X1 = D.x1, AXIS_Y = D.axisY;
  const X = (s) => X0 + s * (X1 - X0);
  const MID_X = 507;                      // centre of the safe width (65–950)
  const USER_R = 1.7, ATK_R = 6.5;
  const N_ATK = 50, N_USR = 9950;

  // ---- counts at any threshold (sorted scores + binary search) ----
  const US = Float64Array.from(D.users.s).sort(), AS = Float64Array.from(D.attacks.s).sort();
  const above = (arr, t) => { let lo = 0, hi = arr.length; while (lo < hi) { const m = (lo + hi) >> 1; if (arr[m] > t) hi = m; else lo = m + 1; } return arr.length - lo; };
  function box(t) {
    const tp = above(AS, t), fp = above(US, t);
    return { t, tp, fp, fn: N_ATK - tp, tn: N_USR - fp, tpr: tp / N_ATK, fpr: fp / N_USR };
  }
  // The ROC curve: one point per distinct score, highest first, from (0,0) to (1,1).
  const ROC = (() => {
    const all = [];
    D.users.s.forEach((s) => all.push([s, 0])); D.attacks.s.forEach((s) => all.push([s, 1]));
    all.sort((a, b) => b[0] - a[0]);
    const pts = [[0, 0, 1.0001]]; let tp = 0, fp = 0;
    for (let i = 0; i < all.length; i++) {
      if (all[i][1]) tp++; else fp++;
      if (i + 1 < all.length && all[i + 1][0] === all[i][0]) continue;
      pts.push([fp / N_USR, tp / N_ATK, all[i][0]]);   // [fpr, tpr, the score where it changes]
    }
    return pts;
  })();
  const STOPS = [0.2, 0.4, 0.55, 0.7, 0.85];
  const T_BOX = 0.7;   // the ledger box
  const fmt = (n) => n.toLocaleString("en-US");
  const fmtT = (t) => t.toFixed(2);

  function ground(g) {
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.fillStyle = rgba(COL.bg); g.fillRect(0, 0, W, H);
  }

  function axis(g) {
    g.strokeStyle = rgba(COL.muted); g.lineWidth = 4; g.lineCap = "round";
    g.beginPath(); g.moveTo(X0 - 14, AXIS_Y); g.lineTo(X1 + 14, AXIS_Y); g.stroke();
    [0, 1].forEach((s) => { g.beginPath(); g.moveTo(X(s), AXIS_Y - 10); g.lineTo(X(s), AXIS_Y + 10); g.stroke(); });
  }

  // Every dot. Flagged (score > t) dots light up: users brighten, attacks get a
  // ring. o.userPulse 0..1 brightens the pile; o.missRing 0..1 rings the
  // unflagged attacks; o.attackRing 0..1 rings every attack.
  function dots(g, t, o = {}) {
    const up = o.userPulse || 0, miss = o.missRing || 0, ring = o.attackRing || 0;
    const U = D.users, A = D.attacks;
    const ucol = mixc(COL.data, COL.text, 0.35 * up);
    const lcol = mixc(ucol, COL.text, 1);
    for (let i = 0; i < U.x.length; i++) {
      const lit = U.s[i] > t;
      g.fillStyle = lit ? rgba(lcol, 1) : rgba(ucol, 0.8);
      const r = lit ? USER_R + 1.6 : USER_R;
      g.fillRect(U.x[i] - r, U.y[i] - r, 2 * r, 2 * r);
    }
    for (let i = 0; i < A.x.length; i++) {
      const x = A.x[i], y = A.y[i], lit = A.s[i] > t;
      g.fillStyle = rgba(COL.attack);
      g.beginPath(); g.arc(x, y, ATK_R, 0, Math.PI * 2); g.fill();
      const rr = Math.max(lit ? 1 : miss, ring);
      if (rr > 0) {
        g.strokeStyle = rgba(lit ? COL.text : mixc(COL.text, COL.attack, 0.0), rr); g.lineWidth = 2.5;
        g.beginPath(); g.arc(x, y, ATK_R + 3 + 4 * Math.max(ring, lit ? 0 : miss), 0, Math.PI * 2); g.stroke();
      }
    }
  }

  // The threshold at score t: the series hero. o.dim 0..1 sends it to rest.
  function threshold(g, t, o = {}) {
    const a = o.alpha == null ? 1 : o.alpha;
    if (a <= 0) return;
    const x = X(t), w = 8 + 4 * (o.pulse || 0);
    g.strokeStyle = rgba(mixc(COL.hero, COL.dim, o.dim || 0), a); g.lineWidth = w; g.lineCap = "round";
    g.beginPath(); g.moveTo(x, 392); g.lineTo(x, 676); g.stroke();
  }

  // ---- DOM text (everything a viewer reads is DOM, so `check` sees it) ----
  function el(root, css, html) {
    const e = document.createElement("div");
    e.style.cssText = "position:absolute;white-space:nowrap;font-weight:800;" + css;
    if (html != null) e.innerHTML = html;
    root.appendChild(e);
    return e;
  }

  // Frame-0 tag (SERIES.md "Context in every episode"), on from frame 0 to the end.
  function makeTag(root) {
    const l1 = el(root, `left:${X0}px;top:240px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`,
      "prompt-injection detector");
    const l2 = el(root, `left:${X0}px;top:306px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`,
      `10,000 requests · <span style="color:${rgba(COL.attack)}">50 attacks</span>`);
    return { set(o = {}) { l1.style.color = rgba(mixc(COL.dim, COL.text, o.bright || 0)); } };
  }

  function makeAxisLabels(root) {
    const c = `top:690px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`;
    el(root, c + `left:${X0 - 18}px;`, "0");
    el(root, c + `left:${X1 - 18}px;`, "1");
    el(root, c + `left:${MID_X - 220}px;width:440px;text-align:center;`, "attack score");
  }

  // The code line. o.hero 0..1 lights "> t" magenta (the line rests then).
  const CODE_W = 680;
  function makeCode(root) {
    const card = el(root, `left:${MID_X - CODE_W / 2}px;top:772px;width:${CODE_W}px;height:76px;padding:6px 0;border-radius:16px;` +
      `text-align:center;background:${rgba(COL.panel)};border:4px solid ${rgba(COL.muted)};font-size:52px;line-height:60px;color:${rgba(COL.text)};`);
    const pre = document.createElement("span"), op = document.createElement("span");
    card.appendChild(pre); card.appendChild(op);
    pre.innerHTML = "pred&nbsp;=&nbsp;scores&nbsp;";
    op.style.borderRadius = "8px"; op.style.padding = "0 6px";
    [card, pre, op].forEach((e) => { e.style.fontFamily = "monospace"; e.style.fontWeight = "700"; });
    return {
      set(o = {}) {
        show(card, o.opacity == null ? 1 : o.opacity);
        op.innerHTML = "&gt;&nbsp;" + fmtT(o.t);
        const h = o.hero || 0;
        op.style.background = h ? rgba(COL.hero, 0.28 * h) : "transparent";
      },
    };
  }

  // ---- The box (compact: headers + cell tags carry the meaning) ----
  const BOX = { left: 66, right: 512, top: 936, bottom: 1326, gap: 10, headY: 862 };
  const CELLS = ["tp", "fp", "fn", "tn"];
  const TAGS = { tp: "TP", fp: "FP", fn: "FN", tn: "TN" };
  function geom() {
    const w = (BOX.right - BOX.left - BOX.gap) / 2, h = (BOX.bottom - BOX.top - BOX.gap) / 2;
    const r = (i, j) => ({ x: BOX.left + i * (w + BOX.gap), y: BOX.top + j * (h + BOX.gap), w, h });
    return { tp: r(0, 0), fp: r(1, 0), fn: r(0, 1), tn: r(1, 1) };
  }
  function makeBox(root) {
    const G = geom();
    const head = (txt, col, c) => el(root, `top:${BOX.headY}px;left:${c.x + c.w / 2 - 120}px;width:240px;text-align:center;font-size:60px;line-height:66px;color:${rgba(col)};`, txt);
    head("attack", COL.attack, G.tp); head("user", COL.data, G.fp);
    const cells = {};
    CELLS.forEach((k) => {
      const c = G[k];
      const tag = el(root, `left:${c.x + 16}px;top:${c.y + 10}px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`, TAGS[k]);
      const num = el(root, `left:${c.x + 16}px;top:${c.y + 88}px;font-size:62px;line-height:72px;color:${rgba(COL.text)};transform-origin:0 50%;`, "");
      cells[k] = { tag, num };
    });
    return {
      // o.counts (from box(t)); o.hi[k] 0..1: a cell being named (white frame, number swells)
      set(o = {}) {
        CELLS.forEach((k) => {
          const h = o.hi ? o.hi[k] || 0 : 0;
          cells[k].num.textContent = fmt(o.counts[k]);
          cells[k].num.style.transform = `scale(${1 + 0.14 * h})`;
          cells[k].tag.style.color = rgba(mixc(COL.dim, COL.text, h));
        });
      },
      draw(g, o = {}) {
        CELLS.forEach((k) => {
          const c = G[k], h = o.hi ? o.hi[k] || 0 : 0;
          g.fillStyle = rgba(COL.panel);
          g.strokeStyle = rgba(mixc(COL.muted, COL.text, h)); g.lineWidth = 4 + 2 * h;
          g.beginPath(); g.roundRect(c.x, c.y, c.w, c.h, 14); g.fill(); g.stroke();
        });
      },
    };
  }

  // ---- The ROC plot ----
  const PLOT = { x0: 600, x1: 930, y0: 1250, y1: 920 };   // y0 is TPR 0 (bottom), y1 is TPR 1 (top)
  const PX = (fpr) => lerp(PLOT.x0, PLOT.x1, fpr), PY = (tpr) => lerp(PLOT.y0, PLOT.y1, tpr);
  function makeRocLabels(root) {
    const c = `font-size:60px;line-height:66px;color:${rgba(COL.dim)};`;
    const tpr = el(root, c + `left:${PLOT.x0 + 22}px;top:846px;`, "TPR");
    el(root, c + `left:${PLOT.x0 - 52}px;top:${PLOT.y1 - 30}px;`, "1");
    el(root, c + `left:${PLOT.x0 - 52}px;top:1262px;`, "0");
    const fpr = el(root, c + `left:${(PLOT.x0 + PLOT.x1) / 2 - 80}px;width:160px;text-align:center;top:1262px;`, "FPR");
    el(root, c + `left:${PLOT.x1 - 18}px;top:1262px;`, "1");
    return {
      set(o = {}) {
        const a = o.tpr || 0, b = o.fpr || 0;
        tpr.style.color = rgba(mixc(COL.dim, COL.text, a)); tpr.style.transform = `scale(${1 + 0.12 * a})`;
        fpr.style.color = rgba(mixc(COL.dim, COL.text, b)); fpr.style.transform = `scale(${1 + 0.12 * b})`;
      },
    };
  }
  // o.curve {alpha, dim, hero, trace}: trace 0..1 draws the curve from (0,0) up to that share of the scores
  //   (as the threshold falls from 1 to 0); o.t the current threshold (its dot); o.dot {alpha, dim};
  //   o.points [{t, a, dim}]; o.guide 0..1 (TPR / FPR guides from the dot); o.corner 0..1
  function roc(g, o = {}) {
    // corner glow, under everything
    const cg = o.corner || 0;
    if (cg > 0) {
      const gr = g.createRadialGradient(PX(0), PY(1), 0, PX(0), PY(1), 150);
      gr.addColorStop(0, rgba(COL.hero, 0.55 * cg)); gr.addColorStop(1, rgba(COL.hero, 0));
      g.fillStyle = gr; g.fillRect(PLOT.x0 - 10, PLOT.y1 - 10, 170, 170);
    }
    // axes and the dashed diagonal
    g.strokeStyle = rgba(COL.muted); g.lineWidth = 4; g.lineCap = "round"; g.setLineDash([]);
    g.beginPath(); g.moveTo(PLOT.x0, PLOT.y1 - 10); g.lineTo(PLOT.x0, PLOT.y0); g.lineTo(PLOT.x1 + 10, PLOT.y0); g.stroke();
    g.lineWidth = 3; g.setLineDash([12, 12]);
    g.beginPath(); g.moveTo(PX(0), PY(0)); g.lineTo(PX(1), PY(1)); g.stroke(); g.setLineDash([]);
    // corner ring
    if (cg > 0) { g.strokeStyle = rgba(COL.hero, cg); g.lineWidth = 6; g.beginPath(); g.arc(PX(0), PY(1), 18 + 6 * cg, 0, Math.PI * 2); g.stroke(); }
    // the curve
    const cv = Object.assign({ alpha: 1, dim: 0, hero: 0, trace: 1 }, o.curve || {});
    if (cv.alpha > 0 && cv.trace > 0) {
      const col = mixc(mixc(COL.data, COL.hero, cv.hero), COL.muted, cv.dim);
      g.strokeStyle = rgba(col, cv.alpha); g.lineWidth = 6; g.lineJoin = "round";
      g.beginPath(); g.moveTo(PX(0), PY(0));
      const tmin = 1 - cv.trace;                       // draw every point whose score is above tmin
      for (let i = 1; i < ROC.length; i++) {
        if (ROC[i][2] <= tmin) { const b = box(tmin); g.lineTo(PX(b.fpr), PY(b.tpr)); break; }
        g.lineTo(PX(ROC[i][0]), PY(ROC[i][1]));
      }
      g.stroke();
    }
    // guides from the current dot
    const b = box(o.t), gd = o.guide || 0;
    if (gd > 0) {
      g.strokeStyle = rgba(COL.text, 0.7 * gd); g.lineWidth = 3; g.setLineDash([8, 10]);
      g.beginPath(); g.moveTo(PX(b.fpr), PY(b.tpr)); g.lineTo(PLOT.x0, PY(b.tpr));
      g.moveTo(PX(b.fpr), PY(b.tpr)); g.lineTo(PX(b.fpr), PLOT.y0); g.stroke(); g.setLineDash([]);
    }
    // stop points
    (o.points || []).forEach((p) => {
      if (!(p.a > 0)) return;
      const q = box(p.t);
      g.fillStyle = rgba(mixc(COL.hero, COL.text, p.dim || 0), p.a);
      g.beginPath(); g.arc(PX(q.fpr), PY(q.tpr), 10, 0, Math.PI * 2); g.fill();
    });
    // the threshold's dot (one hero group with the line)
    const dt = Object.assign({ alpha: 1, dim: 0 }, o.dot || {});
    if (dt.alpha > 0) {
      g.fillStyle = rgba(mixc(COL.hero, COL.dim, dt.dim), dt.alpha);
      g.strokeStyle = rgba(COL.bg, dt.alpha); g.lineWidth = 4;
      g.beginPath(); g.arc(PX(b.fpr), PY(b.tpr), 15 + 5 * (dt.pulse || 0), 0, Math.PI * 2); g.fill(); g.stroke();
    }
  }

  // A small tag on one dot of the score line (beat 4): its own score, 2 dp.
  function makeScoreTag(root) {
    const e = el(root, `font-size:60px;line-height:66px;color:${rgba(COL.attack)};`, "");
    return {
      set(o) {
        if (!o || !(o.a > 0)) { show(e, 0); return; }
        const i = o.i, x = D.attacks.x[i];
        e.textContent = D.attacks.s[i].toFixed(2);
        e.style.left = x - 60 + "px"; e.style.top = "400px";
        show(e, o.a);
      },
      // the leader from the label to the dot (canvas)
      draw(g, o) {
        if (!o || !(o.a > 0)) return;
        const i = o.i, x = D.attacks.x[i], y = D.attacks.y[i];
        g.strokeStyle = rgba(COL.attack, o.a); g.lineWidth = 3;
        g.beginPath(); g.moveTo(x, 470); g.lineTo(x, y - ATK_R - 4); g.stroke();
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
    const d = document.createElement("div");   // the caption line (anchored bottom) stays clear of the stage
    d.style.cssText = "position:absolute;left:0;top:1330px;width:1080px;height:3px;background:rgba(255,200,60,0.6);";
    root.appendChild(d);
  }

  // ---- One state object -> one frame ----
  // S fields (all optional; defaults are the rest state at the ledger box):
  //   t                  the threshold's score (0.70)
  //   thr {alpha, dim, pulse}        the line
  //   dot {alpha, dim, pulse}        its ROC dot
  //   curve {alpha, dim, hero, trace}
  //   points [{t, a, dim}]           stop points on the plot (beat 7)
  //   guide 0..1, rocLabels {tpr, fpr} 0..1, corner 0..1
  //   code {opacity, hero}           the code line (its number is always t)
  //   boxHi {tp, fp, fn, tn} 0..1    a cell being named
  //   tagBright, userPulse, missRing, attackRing 0..1
  //   scoreTag {i, a}                attack i's own score above it
  function mount(root) {
    const tag = makeTag(root); makeAxisLabels(root);
    const code = makeCode(root), bx = makeBox(root), rl = makeRocLabels(root), st = makeScoreTag(root);
    guides(root);
    function draw(g, S) {
      const t = S.t == null ? T_BOX : S.t, counts = box(t);
      ground(g); axis(g);
      bx.draw(g, { hi: S.boxHi });
      dots(g, t, { userPulse: S.userPulse, missRing: S.missRing, attackRing: S.attackRing });
      st.draw(g, S.scoreTag);
      threshold(g, t, S.thr || {});
      roc(g, { t, curve: S.curve, dot: S.dot, points: S.points, guide: S.guide, corner: S.corner });
      tag.set({ bright: S.tagBright || 0 });
      code.set(Object.assign({ opacity: 0 }, S.code || {}, { t }));
      bx.set({ counts, hi: S.boxHi });
      rl.set(S.rocLabels || {});
      st.set(S.scoreTag);
    }
    return { draw };
  }

  // ---- Seams: beat n opens on SEAM[n-1] and ends on SEAM[n] ----
  const TAG_I = 16;   // beat 4's tagged attack: score 0.8374 ("0.84"), top row, right of 0.70
  const pts = (o = {}) => STOPS.map((t) => Object.assign({ t, a: 1 }, o));
  const SEAM = {
    // ends of beats 1–3: rest at the ledger box, no code line
    1: { t: T_BOX }, 2: { t: T_BOX }, 3: { t: T_BOX },
    // end of beat 4: the code line is on (it stays to the end)
    4: { t: T_BOX, code: { opacity: 1 } },
    // end of beat 5: slid left
    5: { t: 0.2, code: { opacity: 1 } },
    // end of beat 6: slid right
    6: { t: 0.85, code: { opacity: 1 } },
    // end of beat 7: the five stop points on the plot (magenta, with the line), curve back at rest
    7: { t: 0.85, code: { opacity: 1 }, points: pts() },
    // end of beat 8: the corner is the hero; line, dot and points at rest
    8: { t: 0.85, code: { opacity: 1 }, points: pts({ dim: 1 }), thr: { dim: 1 }, dot: { dim: 1 }, corner: 1 },
    // end of beat 9 (the last frame): back at the ledger box, points and corner gone
    9: { t: T_BOX, code: { opacity: 1 } },
  };

  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });

  window.SC = { D, COL, W, H, X0, X1, X, AXIS_Y, MID_X, BOX, PLOT, PX, PY, ROC, STOPS, T_BOX, CELLS,
                box, fmt, fmtT, SEAM, TAG_I, ground, axis, dots, threshold, roc, mount, E, lerp, clamp01, seg, hash, pulse, rgba, mixc, show };
})();
