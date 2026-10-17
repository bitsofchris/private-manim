// score.js — the shared kit for 013 ep04 (ROC AUC vs PR AUC).
//
// Every beat loads this (through its `kit` symlink, after kit/dots.js) and
// draws every frame with one call, K.draw(g, S), where S is a state object.
// Each beat opens on SEAM[n-1] and ends on SEAM[n], so cuts are exact.
// Pure functions of their arguments: no clocks, no randomness. Numbers come
// from the ledger (storyboard.md) and dots.js (generated from
// _data/scores.npz); never type a new one in a beat.
//
// The score line, tag, dots and threshold are ep01's kit (ep01-accuracy-trap/
// _kit/score.js), copied and made shorter; the plot is new.
//
// Layout (px, 1080×1920; captions anchored bottom, so the stage runs to 1330):
//   tag            y 240–372   two lines, left at x 120
//   user pile      y 405–527   teal, above the axis
//   axis           y 530       score 0 at x 120, 1 at x 920
//   attack pile    y 542–614   gold, below the axis
//   axis labels    y 622–688   0 · attack score · 1
//   y-axis name    y 700–766   left at x 150 (ROC: true positive rate)
//   plot           y 790–1196, x 150–930 (0..1 × 0..1)
//   x-axis row     y 1210–1276 0 · x-axis name · 1
//   code card      y 250–620   beat 8 only, in the score line's place
(function () {
  const D = window.SCORE_DOTS;
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const pulse = (t, at, w = 0.6) => { const u = (t - at) / w; return u < 0 || u > 1 ? 0 : Math.sin(Math.PI * u); };
  const rgba = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
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
  const USER_R = 1.7, ATK_R = 6.5;
  const LEDGER = {
    n: 10000, attacks: 50, users: 9950, rocAuc: "0.985", prAuc: "0.556", pairs: "98.5%",
    tA: 0.70, tP: 0.55, fprP: "2.3%", blockedP: 233, caughtP: 44, rate: "0.005", times: "111×",
  };

  // ---- the plot ----
  const PL = 150, PR = 930, PT = 790, PB = 1196;
  const PX = (u) => PL + u * (PR - PL), PY = (v) => PB - v * (PB - PT);
  // A point's position: m 0 = ROC (fpr, tpr), m 1 = PR (recall, precision).
  const at = (fpr, tpr, prec, m) => [PX(lerp(fpr, tpr, m)), PY(lerp(tpr, prec, m))];

  // tp / fp at threshold t, counted from the dots (a dot is flagged when its score > t)
  function counts(t) {
    let tp = 0, fp = 0;
    D.attacks.s.forEach((s) => { if (s > t) tp++; });
    D.users.s.forEach((s) => { if (s > t) fp++; });
    return { tp, fp, fpr: fp / LEDGER.users, tpr: tp / LEDGER.attacks, prec: tp + fp ? tp / (tp + fp) : 1 };
  }

  function ground(g) {
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.fillStyle = rgba(COL.bg); g.fillRect(0, 0, W, H);
  }

  // ---- score line (ep01) ----
  function axis(g, a = 1) {
    g.strokeStyle = rgba(COL.muted, a); g.lineWidth = 4; g.lineCap = "round";
    g.beginPath(); g.moveTo(X0 - 14, AXIS_Y); g.lineTo(X1 + 14, AXIS_Y); g.stroke();
    [0, 1].forEach((s) => { g.beginPath(); g.moveTo(X(s), AXIS_Y - 10); g.lineTo(X(s), AXIS_Y + 10); g.stroke(); });
  }

  // o.t: threshold value; o.flag 0..1 rings flagged attacks; o.fpLit 0..1
  // brightens flagged users; o.tnDim 0..1 mutes unflagged users;
  // o.userPulse / o.attackRing 0..1 accents; o.pair 0..1 rings PAIR's two dots;
  // o.alpha: whole score line.
  const PAIR = { attack: 0, user: 0 };
  (function pickPair() {   // a fixed attack near 0.8 and a fixed user near 0.25
    let ba = 1e9, bu = 1e9;
    D.attacks.s.forEach((s, i) => { if (Math.abs(s - 0.8) < ba) { ba = Math.abs(s - 0.8); PAIR.attack = i; } });
    D.users.s.forEach((s, i) => { const d = Math.abs(s - 0.25) + (D.users.y[i] < AXIS_Y - 60 ? 1 : 0); if (d < bu) { bu = d; PAIR.user = i; } });
  })();
  function dots(g, o = {}) {
    const t = o.t, flag = o.flag || 0, fpLit = o.fpLit || 0, tnDim = o.tnDim || 0, A0 = o.alpha == null ? 1 : o.alpha;
    const up = o.userPulse || 0, ring = o.attackRing || 0, pair = o.pair || 0;
    if (A0 <= 0) return;
    const U = D.users, A = D.attacks;
    const ucol = mixc(COL.data, COL.text, 0.35 * up);
    for (let i = 0; i < U.x.length; i++) {
      const x = U.x[i], y = U.y[i], on = U.s[i] > t;
      const lit = on ? fpLit : 0;
      const c = on ? mixc(ucol, COL.text, lit) : mixc(ucol, COL.muted, tnDim);
      g.fillStyle = rgba(c, (0.8 + 0.2 * lit) * A0);
      const r = USER_R + 1.6 * lit;
      g.fillRect(x - r, y - r, 2 * r, 2 * r);
    }
    for (let i = 0; i < A.x.length; i++) {
      const x = A.x[i], y = A.y[i];
      g.fillStyle = rgba(COL.attack, A0);
      g.beginPath(); g.arc(x, y, ATK_R, 0, Math.PI * 2); g.fill();
      const rr = Math.max(A.s[i] > t ? flag : 0, ring);
      if (rr > 0) {
        g.strokeStyle = rgba(COL.text, rr * A0); g.lineWidth = 2.5;
        g.beginPath(); g.arc(x, y, ATK_R + 3 + 4 * ring, 0, Math.PI * 2); g.stroke();
      }
    }
    if (pair > 0) {   // the random pair: a white ring round each, the user dot drawn big
      const ux = U.x[PAIR.user], uy = U.y[PAIR.user], ax = A.x[PAIR.attack], ay = A.y[PAIR.attack];
      g.fillStyle = rgba(COL.data, pair * A0); g.beginPath(); g.arc(ux, uy, ATK_R, 0, Math.PI * 2); g.fill();
      g.strokeStyle = rgba(COL.text, pair * A0); g.lineWidth = 4;
      [[ux, uy], [ax, ay]].forEach(([x, y]) => { g.beginPath(); g.arc(x, y, 16, 0, Math.PI * 2); g.stroke(); });
    }
  }

  // The threshold at score t. u 0..1 drops it in; o.dim 0..1 retires it to --dim.
  function threshold(g, t, u, o = {}) {
    if (u <= 0) return;
    const top = 398, bot = 622, y0 = lerp(top - 140, top, u), x = X(t);
    g.strokeStyle = rgba(mixc(COL.hero, COL.dim, o.dim || 0), clamp01(u * 1.5) * (o.alpha == null ? 1 : o.alpha));
    g.lineWidth = 8; g.lineCap = "round";
    g.beginPath(); g.moveTo(x, y0); g.lineTo(x, lerp(y0 + 30, bot, u)); g.stroke();
  }

  // ---- plot (canvas) ----
  function frame(g, a = 1) {
    g.strokeStyle = rgba(COL.muted, a); g.lineWidth = 4; g.lineCap = "round";
    g.beginPath(); g.moveTo(PL, PT - 6); g.lineTo(PL, PB); g.lineTo(PR + 6, PB); g.stroke();
    g.lineWidth = 2; g.setLineDash([6, 10]);
    g.beginPath(); g.moveTo(PL, PT); g.lineTo(PR, PT); g.lineTo(PR, PB); g.stroke();
    g.setLineDash([]);
  }
  // the good corner: m 0 top-left (ROC), 1 top-right (PR); glow 0..1
  function corner(g, m, glow) {
    if (glow <= 0) return;
    const x = lerp(PL, PR, m), y = PT;
    const gr = g.createRadialGradient(x, y, 0, x, y, 150);
    gr.addColorStop(0, rgba(COL.text, 0.45 * glow)); gr.addColorStop(1, rgba(COL.text, 0));
    g.fillStyle = gr; g.beginPath(); g.arc(x, y, 150, 0, Math.PI * 2); g.fill();
  }
  function curvePath(g, m) {
    const P = D.curve;
    g.beginPath();
    P.forEach(([f, r, p], i) => { const [x, y] = at(f, r, p, m); i ? g.lineTo(x, y) : g.moveTo(x, y); });
  }
  // o.m morph; o.hero 0..1 (teal -> magenta); o.alpha
  function curveLine(g, o = {}) {
    const a = o.alpha == null ? 1 : o.alpha;
    if (a <= 0) return;
    g.strokeStyle = rgba(mixc(COL.data, COL.hero, o.hero || 0), a); g.lineWidth = 7; g.lineJoin = "round";
    curvePath(g, o.m || 0); g.stroke();
  }
  // Area under the ROC curve (polygon) or the PR curve (AP steps, one per attack).
  function rocArea(g, o) {
    if (!o || !(o.o > 0)) return;
    g.fillStyle = rgba(mixc(COL.data, COL.hero, o.hero || 0), 0.26 * o.o);
    curvePath(g, 0); g.lineTo(PX(1), PY(0)); g.lineTo(PX(0), PY(0)); g.closePath(); g.fill();
  }
  function prArea(g, o) {
    if (!o || !(o.o > 0)) return;
    const S = D.apSteps, n = S.length, w = (PR - PL) / n, rev = o.reveal == null ? 1 : o.reveal;
    g.fillStyle = rgba(mixc(COL.data, COL.hero, o.hero || 0), 0.3 * o.o);
    S.forEach((p, j) => {
      const u = clamp01(rev * n - j); if (u <= 0) return;   // reveal sweeps left to right
      g.fillRect(PX(j / n), PY(p * u), w + 0.5, PB - PY(p * u));
    });
  }
  // ROC coin flip: the dashed diagonal, drawn in by u
  function diag(g, u, a = 1) {
    if (u <= 0) return;
    g.strokeStyle = rgba(COL.dim, a); g.lineWidth = 4; g.setLineDash([16, 14]);
    g.beginPath(); g.moveTo(PX(0), PY(0)); g.lineTo(PX(u), PY(u)); g.stroke(); g.setLineDash([]);
  }
  // PR coin flip: a dashed level line at precision v; o.hero 0..1
  function baseLine(g, b) {
    if (!b || !(b.o > 0)) return;
    g.strokeStyle = rgba(mixc(COL.dim, COL.hero, b.hero || 0), b.o); g.lineWidth = 5; g.setLineDash([16, 14]);
    const y = PY(b.v);
    g.beginPath(); g.moveTo(PL, y); g.lineTo(PR, y); g.stroke(); g.setLineDash([]);
  }
  // The point for threshold t on the curve; o.hero 0..1, o.ring 0..1 (a halo)
  function point(g, t, m, o) {
    if (!o || !(o.o > 0)) return;
    const c = counts(t), [x, y] = at(c.fpr, c.tpr, c.prec, m);
    if (o.ring > 0) {
      g.strokeStyle = rgba(COL.hero, o.ring * o.o); g.lineWidth = 4;
      g.beginPath(); g.arc(x, y, 20 + 10 * o.ring, 0, Math.PI * 2); g.stroke();
    }
    g.fillStyle = rgba(mixc(COL.text, COL.hero, o.hero || 0), o.o);
    g.beginPath(); g.arc(x, y, 13, 0, Math.PI * 2); g.fill();
    return [x, y];
  }

  // ---- DOM text (everything a viewer reads is DOM, so `check` sees it) ----
  function el(root, css, html) {
    const e = document.createElement("div");
    e.style.cssText = "position:absolute;white-space:nowrap;font-weight:800;" + css;
    if (html != null) e.innerHTML = html;
    root.appendChild(e);
    return e;
  }
  const F60 = "font-size:60px;line-height:66px;";

  function makeTag(root) {
    const l1 = el(root, `left:${X0}px;top:240px;${F60}color:${rgba(COL.dim)};`, "prompt-injection detector");
    const l2 = el(root, `left:${X0}px;top:306px;${F60}color:${rgba(COL.dim)};`,
      `10,000 requests · <span style="color:${rgba(COL.attack)}">50 attacks</span>`);
    return { set(o = {}) {
      l1.style.color = rgba(mixc(COL.dim, COL.text, o.bright || 0));
      const a = o.opacity == null ? 1 : o.opacity; show(l1, a); show(l2, a);
    } };
  }
  function makeAxisLabels(root) {
    const c = `top:622px;${F60}color:${rgba(COL.dim)};`;
    const e = [el(root, c + `left:${X0 - 18}px;`, "0"), el(root, c + `left:${X1 - 18}px;`, "1"),
               el(root, c + `left:${(X0 + X1) / 2 - 220}px;width:440px;text-align:center;`, "attack score")];
    return { set(a = 1) { e.forEach((x) => show(x, a)); } };
  }

  // Axis names. Slot Y is above the plot at the left; slot X is centred under it.
  // A starts as "true positive rate" in slot Y and becomes "recall" in slot X;
  // B starts as "false positive rate" in slot X and becomes "precision" in slot Y.
  // o.aText / o.bText 0..1 cross-fade the words; o.aMove / o.bMove 0..1 move them.
  // o.aLit / o.bLit 0..1 brighten a name to white while the VO names it.
  // Every word is left-aligned in its box; a slot is an anchor (Y: left edge,
  // X: centre), and the box's left edge is interpolated so nothing jumps.
  const SLOT = { y: { x: PL, y: 700, centre: false }, x: { x: (PL + PR) / 2, y: 1210, centre: true } };
  function makeAxisNames(root) {
    const word = (a, b) => {
      const box = el(root, `${F60}color:${rgba(COL.dim)};height:66px;`);
      const s0 = el(box, "left:0;top:0;", a), s1 = el(box, "left:0;top:0;", b);
      return { box, s0, s1 };
    };
    const A = word("true positive rate", "recall"), B = word("false positive rate", "precision");
    const ticks = [el(root, `top:1210px;${F60}left:${PL - 18}px;color:${rgba(COL.dim)};`, "0"),
                   el(root, `top:1210px;${F60}left:${PR - 18}px;color:${rgba(COL.dim)};`, "1"),
                   el(root, `top:${PT - 33}px;${F60}left:${PL - 62}px;color:${rgba(COL.dim)};`, "1")];
    function place(w, from, to, u, xt, lit) {
      const p = SLOT[from], q = SLOT[to];
      const wd = lerp(w.s0.offsetWidth, w.s1.offsetWidth, xt);
      const left = (s) => (s.centre ? s.x - wd / 2 : s.x);
      // a gentle arc, opposite for the two names, so they pass without touching
      const x = lerp(left(p), left(q), u), y = lerp(p.y, q.y, u) + (from === "y" ? 90 : -90) * Math.sin(Math.PI * u);
      w.box.style.left = x + "px"; w.box.style.top = y + "px";
      show(w.s0, 1 - xt); show(w.s1, xt);
      const c = rgba(mixc(COL.dim, COL.text, lit || 0));
      w.s0.style.color = c; w.s1.style.color = c;
    }
    return { set(o = {}) {
      place(A, "y", "x", o.aMove || 0, o.aText || 0, o.aLit);
      place(B, "x", "y", o.bMove || 0, o.bText || 0, o.bLit);
    } };
  }

  // Notes on the plot. ROC readout bottom right; PR readout top right; two
  // sub lines (right-aligned, upper middle, ROC only); the point's label;
  // the PR baseline's label (follows the line); the PR sub (lower left).
  function makeNotes(root) {
    const R = 915;
    const big = (head, val, top) => {
      const h = el(root, `${F60}color:${rgba(COL.dim)};text-align:right;width:400px;`, head);
      const v = el(root, `font-size:120px;line-height:124px;color:${rgba(COL.text)};text-align:right;width:400px;`, val);
      return { h, v, top };
    };
    // ROC: "ROC AUC" + 0.985 on one row, bottom right. PR: "PR AUC" over 0.556, top right.
    const roc = big("ROC AUC", LEDGER.rocAuc), pr = big("PR AUC", LEDGER.prAuc);
    roc.h.style.left = R - 400 - 370 + "px"; roc.h.style.top = 1136 + "px";
    roc.v.style.left = R - 400 + "px"; roc.v.style.top = 1078 + "px";
    pr.h.style.left = R - 400 + "px"; pr.h.style.top = 800 + "px";
    pr.v.style.left = R - 400 + "px"; pr.v.style.top = 868 + "px";
    const sub = [0, 1].map((i) => el(root, `${F60}color:${rgba(COL.text)};text-align:right;width:780px;left:${R - 780}px;top:${944 + 66 * i}px;`));
    const ptLab = el(root, `${F60}color:${rgba(COL.text)};`, `FPR ${LEDGER.fprP}`);
    const baseLab = [el(root, `${F60}color:${rgba(COL.dim)};left:${PL + 20}px;`, "0.5"),
                     el(root, `${F60}color:${rgba(COL.dim)};left:${PL + 20}px;`, `${LEDGER.rate} · attack rate`)];
    const prSub = el(root, `${F60}color:${rgba(COL.text)};left:${PL + 20}px;top:1050px;`, `${LEDGER.times} a coin flip`);
    return {
      // o.roc / o.pr: {o, hero} readouts; o.sub: [[text, o], [text, o]];
      // o.ptLab: {o, x, y} (x, y from point()); o.base: {o, v, hero}; o.prSub: o
      set(o = {}) {
        const r = o.roc || {}, p = o.pr || {};
        show(roc.h, r.o || 0); show(roc.v, r.o || 0); roc.v.style.color = rgba(mixc(COL.text, COL.hero, r.hero || 0));
        show(pr.h, p.o || 0); show(pr.v, p.o || 0); pr.v.style.color = rgba(mixc(COL.text, COL.hero, p.hero || 0));
        sub.forEach((e, i) => {
          const s = o.sub && o.sub[i];
          if (s) e.textContent = s[0];
          show(e, s ? s[1] : 0);
          e.style.color = rgba(s && s[2] ? COL.attack : COL.text);
        });
        const pl = o.ptLab || {};
        show(ptLab, pl.o || 0);
        if (pl.x != null) { ptLab.style.left = pl.x + 34 + "px"; ptLab.style.top = pl.y - 4 + "px"; }
        const b = o.base || {}, bo = b.o || 0, y = PY(b.v == null ? 0.5 : b.v);
        const k = seg(b.v == null ? 0.5 : b.v, 0.3, 0.05);   // 0 at 0.5, 1 at the floor
        baseLab.forEach((e) => { e.style.top = y - 76 + "px"; e.style.color = rgba(mixc(COL.dim, COL.hero, b.hero || 0)); });
        show(baseLab[0], bo * (1 - k)); show(baseLab[1], bo * k);
        show(prSub, o.prSub || 0);
      },
    };
  }

  // The code card (beat 8), in the score line's place.
  const CODE = ["roc_auc_score(y, s)", "average_precision_score(y, s)"];
  const CODE_OUT = [LEDGER.rocAuc, LEDGER.prAuc];
  function makeCode(root) {
    const card = el(root, `left:65px;top:260px;width:885px;padding:18px 10px;border-radius:18px;` +
      `background:${rgba(COL.panel)};border:5px solid ${rgba(COL.muted)};font-size:48px;line-height:60px;color:${rgba(COL.text)};`);
    const rows = [], outs = [];
    CODE.forEach((s, i) => {
      rows.push(el(card, "position:relative;padding:0 6px;border-radius:8px;", s.replace(/ /g, "&nbsp;")));
      outs.push(el(card, `position:relative;padding:0 6px 10px;color:${rgba(COL.data)};`, CODE_OUT[i]));
    });
    [card, ...card.querySelectorAll("*")].forEach((e) => { e.style.fontFamily = "monospace"; e.style.fontWeight = "700"; });
    return { set(o = {}) {
      show(card, o.o || 0);
      rows.forEach((r, i) => { const on = o.lit ? o.lit[i] || 0 : 0; r.style.background = on ? rgba(COL.hero, 0.28 * on) : "transparent"; });
      outs.forEach((e, i) => show(e, o.out ? o.out[i] || 0 : 0));
    } };
  }

  function guides(root) {
    if (!/[?&]guides/.test(location.search)) return;
    [[0, 0, 1080, 230], [0, 1536, 1080, 384], [950, 230, 130, 1306], [0, 230, 65, 1306]].forEach(([l, t, w, h]) => {
      const d = document.createElement("div");
      d.style.cssText = `position:absolute;left:${l}px;top:${t}px;width:${w}px;height:${h}px;background:rgba(255,60,60,0.18);pointer-events:none;`;
      root.appendChild(d);
    });
    const d = document.createElement("div");
    d.style.cssText = "position:absolute;left:0;top:1330px;width:1080px;height:3px;background:rgba(255,200,60,0.6);";
    root.appendChild(d);
  }

  // ---- One state object -> one frame ----
  // S fields (all optional; defaults in REST):
  //   t                 threshold value (0.70 → 0.55 in beat 4)
  //   thr {u, dim}      threshold drop-in 0..1, retired 0..1 (dim 0 = the hero)
  //   flag, fpLit, tnDim, userPulse, attackRing, pair    score-line accents (0..1)
  //   tag {bright, opacity}, line 0..1 (score line + tag + labels; 0 for the code card)
  //   m 0..1            ROC → PR morph (points, curve, point, corner)
  //   curve {hero, alpha}, rocArea {o, hero}, prArea {o, hero, reveal}
  //   diag 0..1, base {o, v, hero}, point {o, hero, ring}, corner 0..1
  //   names {aText, aMove, bText, bMove, aLit, bLit}
  //   notes {roc, pr, sub, ptLab:{o}, prSub}    (ptLab's x, y come from the point)
  //   code {o, lit:[2], out:[2]}
  const REST = { t: LEDGER.tA, thr: { u: 1, dim: 1 }, flag: 1, line: 1, m: 0, curve: {}, names: {}, notes: {} };
  function mount(root) {
    const tag = makeTag(root), ax = makeAxisLabels(root), names = makeAxisNames(root);
    const notes = makeNotes(root), code = makeCode(root);
    guides(root);
    function draw(g, S0) {
      const S = Object.assign({}, REST, S0), L = S.line, m = S.m;
      ground(g);
      axis(g, L);
      dots(g, { t: S.t, flag: S.flag, fpLit: S.fpLit, tnDim: S.tnDim, userPulse: S.userPulse,
                attackRing: S.attackRing, pair: S.pair, alpha: L });
      threshold(g, S.t, S.thr.u, { dim: S.thr.dim, alpha: L });
      frame(g);
      corner(g, m, S.corner || 0);
      rocArea(g, S.rocArea); prArea(g, S.prArea);
      diag(g, S.diag || 0); baseLine(g, S.base);
      curveLine(g, Object.assign({ m }, S.curve));
      const p = point(g, S.t, m, S.point);
      tag.set(Object.assign({ opacity: L }, S.tag || {}));
      ax.set(L);
      names.set(S.names);
      const n = Object.assign({}, S.notes);
      if (n.ptLab && p) n.ptLab = Object.assign({ x: p[0], y: p[1] }, n.ptLab);
      notes.set(n);
      code.set(S.code || {});
    }
    return { draw };
  }

  // Seam states: SEAM[n] = the last frame of beat n = the first frame of beat n+1.
  // Hero per seam in the comment.
  const ROC1 = { roc: { o: 1 } };
  const PRN = { aText: 1, aMove: 1, bText: 1, bMove: 1 };   // the axis names after the swap
  const SEAM = {
    // 1 hook: threshold 0.70 the hero, its 60 users lit; ROC area at rest; "60 of 100 flags / are real users"
    1: { thr: { u: 1, dim: 0 }, fpLit: 1, rocArea: { o: 1 },
         notes: { roc: { o: 1 }, sub: [["60 of 100 flags", 1], ["are real users", 1]] } },
    // 2 context: the same, tag back at rest (beat 2 only brightens it and lets it go)
    2: { thr: { u: 1, dim: 0 }, fpLit: 1, rocArea: { o: 1 },
         notes: { roc: { o: 1 }, sub: [["60 of 100 flags", 1], ["are real users", 1]] } },
    // 3 what AUC is: area the hero; diagonal drawn; subs "98.5% of pairs" / "coin flip 0.5"; pair ringed
    3: { rocArea: { o: 1, hero: 1 }, diag: 1, pair: 1,
         notes: { roc: { o: 1 }, sub: [["98.5% of pairs", 1], ["coin flip 0.5", 1]] } },
    // 4 the point: threshold at 0.55 (hero) and its point ringed; 233 users lit; "233 blocked / 44 caught"
    4: { t: LEDGER.tP, thr: { u: 1, dim: 0 }, fpLit: 1, rocArea: { o: 0.5 },
         point: { o: 1, hero: 1, ring: 1 },
         notes: { roc: { o: 0 }, ptLab: { o: 1 }, sub: [["233 users blocked", 1], ["44 attacks caught", 1, "attack"]] } },
    // 5 swap: PR view, curve the hero, good corner top right lit, unflagged users dimmed
    5: { t: LEDGER.tP, thr: { u: 1, dim: 1 }, fpLit: 1, tnDim: 1, m: 1, curve: { hero: 1 },
         point: { o: 1 }, corner: 1, names: PRN },
    // 6 baseline: the dashed line at 0.005 (hero), labelled
    6: { t: LEDGER.tP, thr: { u: 1, dim: 1 }, fpLit: 1, tnDim: 1, m: 1, point: { o: 1 }, names: PRN,
         base: { o: 1, v: 0.005, hero: 1 } },
    // 7 PR AUC: area filled (hero), readout 0.556, "111× a coin flip"; baseline at rest
    7: { t: LEDGER.tP, thr: { u: 1, dim: 1 }, fpLit: 1, tnDim: 1, m: 1, point: { o: 1 }, names: PRN,
         base: { o: 1, v: 0.005 }, prArea: { o: 1, hero: 1 },
         notes: { pr: { o: 1 }, prSub: 1 } },
    // 8 takeaway (the last frame): code card in the score line's place, line 2 lit; PR plot at rest
    8: { t: LEDGER.tP, thr: { u: 1, dim: 1 }, line: 0, m: 1, point: { o: 1 }, names: PRN,
         base: { o: 1, v: 0.005 }, prArea: { o: 1 },
         notes: { pr: { o: 1 }, prSub: 1 }, code: { o: 1, lit: [0, 1], out: [1, 1] } },
  };
  // Frame 0 of the Short (beat 1 opens here): the area is the hero, threshold retired.
  SEAM[0] = { rocArea: { o: 1, hero: 1 }, notes: ROC1 };

  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });

  window.SC = { D, COL, LEDGER, W, H, X0, X1, X, AXIS_Y, PL, PR, PT, PB, PX, PY, CODE, CODE_OUT, PAIR,
                counts, ground, axis, dots, threshold, frame, corner, curveLine, rocArea, prArea, diag, baseLine, point,
                makeTag, makeAxisLabels, makeAxisNames, makeNotes, makeCode, guides, mount, SEAM, REST, E,
                lerp, clamp01, seg, hash, pulse, rgba, mixc };
})();
