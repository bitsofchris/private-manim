// score.js — the kit for 013 ep05 (F1 and the threshold).
//
// Built from ep01's kit (`../ep01-accuracy-trap/_kit/score.js` at bc1b4b3);
// dots.js and make_dots.py are copied unchanged, so the score line is the
// series' own. Every beat loads this (through its `kit` symlink, after
// kit/dots.js) and draws one state object per frame: `K.draw(g, S)`.
// Each beat opens on SEAM[n-1] and ends on SEAM[n], so cuts are exact.
// Pure functions of their arguments: no clocks, no randomness (SC.hash).
// Numbers come from the ledger (storyboard.md) or are counted from the dots;
// never type a new one in a beat.
//
// Layout (px, 1080×1920; captions anchored bottom, so the stage runs to 1330):
//   tag            y 240–372   two lines, left at x 120
//   user pile      y 400–587   teal, above the axis
//   axis           y 590       score 0 at x 120, 1 at x 920
//   attack pile    y 602–673   gold, below the axis
//   axis labels    y 690–756
//   middle         y 790–1320  bars (beats 1–3), formula (2b), cost cards (4), target + readout (5–7)
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
  const MID_X = 507;                      // centre of the safe width (65–950)
  const USER_R = 1.7, ATK_R = 6.5;
  // Thresholds. A dot is flagged when its score > the threshold.
  // T_A: Model A (ledger 0.70: 40 attacks, 60 users). T_END: as far down as
  // "at least 1 flag in 3 is real" allows (ledger 0.66; scores ≥ 0.656:
  // 41 attacks, 82 users, 123 flags).
  const T_A = 0.70, T_END = 0.6559;
  const LEDGER = { n: 10000, attacks: 50, users: 9950,
                   ex: { p: 0.9, r: 0.1, mean: 0.5, f1: 0.18 },
                   a: { p: 0.40, r: 0.80, f1: 0.53 } };

  // Flag counts for a threshold, counted from the dots (they are the data).
  function counts(thrS) {
    let tp = 0, fp = 0;
    for (const s of D.attacks.s) if (s > thrS) tp++;
    for (const s of D.users.s) if (s > thrS) fp++;
    return { tp, fp, flags: tp + fp };
  }

  function ground(g) {
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.fillStyle = rgba(COL.bg); g.fillRect(0, 0, W, H);
  }

  function axis(g) {
    g.strokeStyle = rgba(COL.muted); g.lineWidth = 4; g.lineCap = "round";
    g.beginPath(); g.moveTo(X0 - 14, AXIS_Y); g.lineTo(X1 + 14, AXIS_Y); g.stroke();
    [0, 1].forEach((s) => { g.beginPath(); g.moveTo(X(s), AXIS_Y - 10); g.lineTo(X(s), AXIS_Y + 10); g.stroke(); });
  }

  // Every dot. o.thrS: threshold score; o.flag 0..1: dots right of it light up
  // (users brighten, attacks get a white ring). One-shot accents, 0..1:
  // o.userPulse (whole pile), o.attackRing (all 50), o.fpRing (flagged users),
  // o.fnRing (attacks left of the line).
  function dots(g, o = {}) {
    const thrS = o.thrS == null ? T_A : o.thrS, flag = o.flag || 0;
    const up = o.userPulse || 0, ring = o.attackRing || 0, fpR = o.fpRing || 0, fnR = o.fnRing || 0;
    const U = D.users, A = D.attacks;
    const ucol = mixc(COL.data, COL.text, 0.35 * up);
    for (let i = 0; i < U.x.length; i++) {
      const x = U.x[i], y = U.y[i];
      const lit = U.s[i] > thrS ? Math.max(flag, fpR) : 0;
      g.fillStyle = rgba(lit ? mixc(ucol, COL.text, lit) : ucol, 0.8 + 0.2 * lit);
      const r = USER_R + 1.6 * lit + 2.4 * (U.s[i] > thrS ? fpR : 0);
      g.fillRect(x - r, y - r, 2 * r, 2 * r);
    }
    for (let i = 0; i < A.x.length; i++) {
      const x = A.x[i], y = A.y[i], on = A.s[i] > thrS;
      g.fillStyle = rgba(COL.attack);
      g.beginPath(); g.arc(x, y, ATK_R, 0, Math.PI * 2); g.fill();
      const acc = Math.max(ring, on ? 0 : fnR);
      const rr = Math.max(on ? flag : 0, acc);
      if (rr > 0) {
        g.strokeStyle = rgba(COL.text, rr); g.lineWidth = 2.5;
        g.beginPath(); g.arc(x, y, ATK_R + 3 + 4 * acc, 0, Math.PI * 2); g.stroke();
      }
    }
  }

  // The threshold at score thrS. u 0..1 drops it in from above; hero 0..1
  // mixes dim (at rest) to magenta (the hero); o.pulse 0..1 a one-shot swell.
  function threshold(g, u, thrS, hero, p = 0) {
    if (u <= 0) return;
    const tx = X(thrS), top = 392, bot = 676, y0 = lerp(top - 140, top, u);
    g.strokeStyle = rgba(mixc(COL.dim, COL.hero, hero), clamp01(u * 1.5)); g.lineWidth = 8 + 6 * p; g.lineCap = "round";
    g.beginPath(); g.moveTo(tx, y0); g.lineTo(tx, lerp(y0 + 30, bot, u)); g.stroke();
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
    const c = `left:${X0}px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`;
    const l1 = el(root, c + "top:240px;", "prompt-injection detector");
    const l2 = el(root, c + "top:306px;", `10,000 requests · <span style="color:${rgba(COL.attack)}">50 attacks</span>`);
    return { set(o = {}) { l1.style.color = rgba(mixc(COL.dim, COL.text, o.bright || 0)); } };
  }

  function makeAxisLabels(root) {
    const c = `top:690px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`;
    el(root, c + `left:${X0 - 18}px;`, "0");
    el(root, c + `left:${X1 - 18}px;`, "1");
    el(root, c + `left:${MID_X - 220}px;width:440px;text-align:center;`, "attack score");
  }

  // ---- Bars: precision and recall on 0..1, the mean line and the F1 line ----
  const BARS = { base: 1170, top: 850, w: 150, pX: 230, rX: 520, lx0: 110, lx1: 640, labX: 665 };
  const BY = (v) => lerp(BARS.base, BARS.top, v);
  function makeBars(root) {
    const name = (txt, cx) => el(root, `left:${cx - 180}px;width:360px;text-align:center;top:1186px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`, txt);
    const val = (cx) => el(root, `left:${cx - 180}px;width:360px;text-align:center;top:1254px;font-size:60px;line-height:66px;color:${rgba(COL.data)};`);
    const nP = name("precision", BARS.pX), nR = name("recall", BARS.rX);
    const vP = val(BARS.pX), vR = val(BARS.rX);
    const lab = (col) => el(root, `left:${BARS.labX}px;font-size:60px;line-height:66px;color:${rgba(col)};`);
    const mL = lab(COL.dim), fL = lab(COL.hero);
    return {
      // o: {opacity, p, r, f1, pText, rText, f1Text, mean (opacity), pulseP, pulseR, f1Pulse}
      set(o = {}) {
        const op = o.opacity == null ? 1 : o.opacity;
        [nP, nR].forEach((e) => show(e, op));
        vP.textContent = o.pText; vR.textContent = o.rText;
        show(vP, op); show(vR, op);
        vP.style.color = rgba(mixc(COL.data, COL.text, o.pulseP || 0));
        vR.style.color = rgba(mixc(COL.data, COL.text, o.pulseR || 0));
        mL.textContent = `mean ${LEDGER.ex.mean}`;
        mL.style.top = BY(LEDGER.ex.mean) - 33 + "px"; show(mL, op * (o.mean || 0));
        fL.textContent = o.f1Text;
        fL.style.top = BY(o.f1) - 33 + "px"; show(fL, op);
        fL.style.transform = `scale(${1 + 0.12 * (o.f1Pulse || 0)})`; fL.style.transformOrigin = "0 50%";
      },
      draw(g, o = {}) {
        const op = o.opacity == null ? 1 : o.opacity;
        if (op <= 0) return;
        g.strokeStyle = rgba(COL.muted, op); g.lineWidth = 4; g.lineCap = "round";
        g.beginPath(); g.moveTo(BARS.lx0, BARS.base); g.lineTo(BARS.lx1, BARS.base); g.stroke();
        const bar = (cx, v, pl) => {
          const y = BY(v);
          g.fillStyle = rgba(mixc(COL.data, COL.text, 0.45 * pl), op * (0.75 + 0.25 * pl));
          g.beginPath(); g.roundRect(cx - BARS.w / 2 - 6 * pl, y, BARS.w + 12 * pl, BARS.base - y - 2, [10, 10, 0, 0]); g.fill();
        };
        bar(BARS.pX, o.p, o.pulseP || 0); bar(BARS.rX, o.r, o.pulseR || 0);
        const m = o.mean || 0;
        if (m > 0) {
          g.strokeStyle = rgba(COL.dim, op * m); g.lineWidth = 5; g.setLineDash([18, 14]);
          const y = BY(LEDGER.ex.mean), x1 = lerp(BARS.lx0, BARS.lx1, clamp01(m * 1.4));
          g.beginPath(); g.moveTo(BARS.lx0, y); g.lineTo(x1, y); g.stroke(); g.setLineDash([]);
        }
        const fy = BY(o.f1), fp = o.f1Pulse || 0;
        g.strokeStyle = rgba(COL.hero, op); g.lineWidth = 8 + 5 * fp;
        g.beginPath(); g.moveTo(BARS.lx0, fy); g.lineTo(BARS.lx1, fy); g.stroke();
      },
    };
  }

  // ---- Cost cards: the two mistakes, stacked full width ----
  const CARDS = { x: 70, w: 875, h: 240, fpY: 800, fnY: 1075 };
  function makeCards(root) {
    const card = (y, head, headCol, line, sub) => {
      const c = `left:${CARDS.x + 34}px;font-size:60px;line-height:66px;`;
      return [el(root, c + `top:${y + 21}px;color:${rgba(headCol)};`, head),
              el(root, c + `top:${y + 87}px;color:${rgba(COL.text)};`, line),
              el(root, c + `top:${y + 153}px;color:${rgba(COL.dim)};`, sub)];
    };
    const fp = card(CARDS.fpY, "false positive", COL.data, "real user blocked", "can try again");
    const fn = card(CARDS.fnY, "false negative", COL.attack, "agent hijacked", "data leaked");
    return {
      // o: {opacity, lit: {fp, fn}}
      set(o = {}) {
        const op = o.opacity == null ? 1 : o.opacity;
        [...fp, ...fn].forEach((e) => show(e, op));
      },
      draw(g, o = {}) {
        const op = o.opacity == null ? 1 : o.opacity;
        if (op <= 0) return;
        [["fp", CARDS.fpY], ["fn", CARDS.fnY]].forEach(([k, y]) => {
          const lit = o.lit ? o.lit[k] || 0 : 0;
          g.fillStyle = rgba(COL.panel, op);
          g.strokeStyle = rgba(mixc(COL.muted, COL.hero, lit), op); g.lineWidth = 4 + 3 * lit;
          g.beginPath(); g.roundRect(CARDS.x, y, CARDS.w, CARDS.h, 18); g.fill(); g.stroke();
        });
      },
    };
  }

  // ---- Target (2 blocked : 1 stopped → at least 1 flag in 3 is real) and the readout ----
  const TGT = { tokY: 835, tokR: 28, tokX: [MID_X - 130, MID_X - 45, MID_X + 110], rateY: 895, l1Y: 975, l2Y: 1041,
                caughtY: 1140, flagsY: 1246 };
  function makeTarget(root) {
    const c = `left:${MID_X - 440}px;width:880px;text-align:center;font-size:60px;line-height:66px;`;
    const rate = el(root, c + `top:${TGT.rateY}px;color:${rgba(COL.dim)};`,
      `<span style="color:${rgba(COL.data)}">2 blocked</span> : <span style="color:${rgba(COL.attack)}">1 stopped</span>`);
    const l1 = el(root, c + `top:${TGT.l1Y}px;`, "at least 1 flag in 3");
    const l2 = el(root, c + `top:${TGT.l2Y}px;color:${rgba(COL.text)};`, "is a real attack");
    const caught = el(root, `left:${MID_X - 440}px;width:880px;text-align:center;top:${TGT.caughtY}px;font-size:84px;line-height:92px;color:${rgba(COL.text)};`);
    const flags = el(root, c + `top:${TGT.flagsY}px;color:${rgba(COL.dim)};`);
    return {
      // o: {opacity, tokens 0..1, rate 0..1, rule 0..1, ruleHero 0..1, rulePulse, readout 0..1, caughtPulse, thrS}
      set(o = {}) {
        const op = o.opacity == null ? 1 : o.opacity;
        show(rate, op * (o.rate || 0));
        const h = o.ruleHero || 0, pl = o.rulePulse || 0;
        l1.style.color = rgba(mixc(COL.text, COL.hero, h));
        l1.style.transform = `scale(${1 + 0.08 * pl})`;
        show(l1, op * (o.rule || 0)); show(l2, op * (o.rule || 0));
        const k = counts(o.thrS == null ? T_A : o.thrS), cp = o.caughtPulse || 0;
        caught.innerHTML = `caught <span style="color:${rgba(mixc(COL.attack, COL.text, cp))}">${k.tp} / 50</span>`;
        caught.style.transform = `scale(${1 + 0.1 * cp})`;
        flags.textContent = `${k.flags} flags, ${k.tp} real`;
        show(caught, op * (o.readout || 0)); show(flags, op * (o.readout || 0));
      },
      draw(g, o = {}) {
        const op = (o.opacity == null ? 1 : o.opacity) * (o.tokens || 0);
        if (op <= 0) return;
        const cols = [COL.data, COL.data, COL.attack];
        TGT.tokX.forEach((x, i) => {
          g.fillStyle = rgba(cols[i], op);
          g.beginPath(); g.arc(x, TGT.tokY, TGT.tokR, 0, Math.PI * 2); g.fill();
        });
        const b = (o.rule || 0) * op;   // the "1 in 3" outline around all three
        if (b > 0) {
          g.strokeStyle = rgba(mixc(COL.muted, COL.hero, o.ruleHero || 0), b); g.lineWidth = 5;
          const x0 = TGT.tokX[0] - TGT.tokR - 22, x1 = TGT.tokX[2] + TGT.tokR + 22;
          g.beginPath(); g.roundRect(x0, TGT.tokY - TGT.tokR - 16, x1 - x0, 2 * TGT.tokR + 32, 40); g.stroke();
        }
      },
    };
  }

  // ---- The formula (beat 2b): F1 = 2·P·R / (P + R), then the example plugged in ----
  // Two stacked fractions centred at FORM.cx; "F1 =" left of the first, "= 0.18" right of the second.
  const FORM = { cx: 470, labY: 800, aY: 975, bY: 1205, ruleW: 330 };
  function makeFormula(root) {
    const t = (css, html) => el(root, `text-align:center;color:${rgba(COL.text)};` + css, html);
    const frac = (y, num, den, fs, w) => {
      const lh = Math.round(fs * 1.1);
      return [t(`left:${FORM.cx - 300}px;width:600px;top:${y - lh - 8}px;font-size:${fs}px;line-height:${lh}px;`, num),
              el(root, `left:${FORM.cx - w / 2}px;top:${y - 3}px;width:${w}px;height:6px;border-radius:3px;background:${rgba(COL.text)};`),
              t(`left:${FORM.cx - 300}px;width:600px;top:${y + 10}px;font-size:${fs}px;line-height:${lh}px;`, den)];
    };
    const lab = t(`left:${MID_X - 440}px;width:880px;top:${FORM.labY}px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`, "harmonic mean");
    const f1 = el(root, `left:65px;width:215px;text-align:right;top:${FORM.aY - 40}px;font-size:72px;line-height:80px;`, "F1 =");
    const A = frac(FORM.aY, "2 · P · R", "P + R", 72, FORM.ruleW);
    const B = frac(FORM.bY, "2 · 0.9 · 0.1", "0.9 + 0.1", 64, 440);
    const res = el(root, `left:${FORM.cx + 235}px;top:${FORM.bY - 36}px;font-size:64px;line-height:72px;`, "= 0.18");
    return {
      // o: {opacity, plug 0..1 (the example row; the hero passes from "F1" to its 0.18)}
      set(o = {}) {
        const op = o.opacity == null ? 0 : o.opacity, pl = o.plug || 0;
        [lab, ...A].forEach((e) => show(e, op));
        show(f1, op); f1.style.color = rgba(mixc(COL.hero, COL.text, pl));
        B.forEach((e) => show(e, op * pl));
        show(res, op * pl); res.style.color = rgba(COL.hero);
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
    const d = document.createElement("div");
    d.style.cssText = "position:absolute;left:0;top:1330px;width:1080px;height:3px;background:rgba(255,200,60,0.6);";
    root.appendChild(d);
  }

  // ---- One state object -> one frame ----
  // S fields (all optional; defaults are the hook at rest):
  //   thr 0..1 (dropped in), thrS (score, default T_A), thrHero 0..1, thrPulse 0..1
  //   flag 0..1, userPulse, attackRing, fpRing, fnRing 0..1   (dots)
  //   tagBright 0..1
  //   bars {opacity, p, r, f1, pText, rText, f1Text, mean, pulseP, pulseR, f1Pulse}
  //   cards {opacity, lit:{fp, fn}}
  //   target {opacity, tokens, rate, rule, ruleHero, rulePulse, readout, caughtPulse}
  //   formula {opacity, plug}   (beat 2b only; off everywhere else)
  const BARS_EX = { opacity: 1, p: LEDGER.ex.p, r: LEDGER.ex.r, f1: LEDGER.ex.f1,
                    pText: "0.9", rText: "0.1", f1Text: "F1 0.18", mean: 0 };
  const BARS_A = { opacity: 1, p: LEDGER.a.p, r: LEDGER.a.r, f1: LEDGER.a.f1,
                   pText: "40%", rText: "80%", f1Text: "F1 0.53", mean: 0 };
  function mount(root) {
    const tag = makeTag(root); makeAxisLabels(root);
    const bars = makeBars(root), cards = makeCards(root), target = makeTarget(root), formula = makeFormula(root);
    guides(root);
    function draw(g, S) {
      const thrS = S.thrS == null ? T_A : S.thrS;
      const B = Object.assign({}, BARS_EX, S.bars || {});
      const C = Object.assign({ opacity: 0 }, S.cards || {});
      const T = Object.assign({ opacity: 0 }, S.target || {}, { thrS });
      ground(g); axis(g);
      bars.draw(g, B); cards.draw(g, C); target.draw(g, T);
      dots(g, { thrS, flag: (S.flag || 0) * (S.thr || 0), userPulse: S.userPulse, attackRing: S.attackRing,
                fpRing: S.fpRing, fnRing: S.fnRing });
      threshold(g, S.thr || 0, thrS, S.thrHero || 0, S.thrPulse || 0);
      tag.set({ bright: S.tagBright || 0 });
      bars.set(B); cards.set(C); target.set(T); formula.set(S.formula || {});
    }
    return { draw, tag, bars, cards, target, formula };
  }

  const TARGET_ON = { opacity: 1, tokens: 1, rate: 1, rule: 1, ruleHero: 1, readout: 1 };
  const SEAM = {
    // end of beat 1: the hook at rest (bars at 0.9 / 0.1, F1 0.18, no mean, no threshold)
    1: { bars: BARS_EX },
    // end of beat 2: + the dashed mean at 0.5
    2: { bars: Object.assign({}, BARS_EX, { mean: 1 }) },
    // end of beat 3: Model A — threshold in at 0.70 (dim), flagged lit; bars 40% / 80%, F1 0.53
    3: { thr: 1, flag: 1, bars: BARS_A },
    // end of beat 4: the cost cards, fn lit; bars gone
    4: { thr: 1, flag: 1, bars: Object.assign({}, BARS_A, { opacity: 0 }), cards: { opacity: 1, lit: { fn: 1 } } },
    // end of beat 5: the target and the readout at Model A's line; "1 in 3" is the hero
    5: { thr: 1, flag: 1, bars: Object.assign({}, BARS_A, { opacity: 0 }), target: TARGET_ON },
    // end of beat 6: the line moved down to T_END, magenta; the rule back to rest
    6: { thr: 1, flag: 1, thrS: T_END, thrHero: 1, bars: Object.assign({}, BARS_A, { opacity: 0 }),
         target: Object.assign({}, TARGET_ON, { ruleHero: 0 }) },
    // end of beat 7 (the last frame): the same, still
    7: { thr: 1, flag: 1, thrS: T_END, thrHero: 1, bars: Object.assign({}, BARS_A, { opacity: 0 }),
         target: Object.assign({}, TARGET_ON, { ruleHero: 0 }) },
  };

  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });

  window.SC = { D, COL, LEDGER, W, H, X0, X1, X, AXIS_Y, MID_X, T_A, T_END, BARS, BY, CARDS, TGT, BARS_EX, BARS_A,
                counts, ground, axis, dots, threshold, makeTag, makeAxisLabels, makeBars, makeCards, makeTarget, makeFormula, FORM,
                guides, mount, SEAM, E, lerp, clamp01, seg, hash, pulse, rgba, mixc };
})();
