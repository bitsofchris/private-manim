// score.js — the shared kit for 013 ep02 (precision vs recall).
//
// Copied from ep01's kit (ep01-accuracy-trap/_kit/score.js at c05de17) and
// changed for this episode: the dots stay home on the score line (no flying
// into the box), the box is shorter and holds counts only, and two fraction
// rows (recall, precision) sit under it. Ep01's kit is not touched.
//
// Every beat loads this (through its `kit` symlink, after kit/dots.js) and
// draws one frame with K.draw(g, S), S a state object. A beat opens on
// SEAM[n-1] and ends on SEAM[n], the same objects, so cuts are exact.
// Pure functions of their arguments: no clocks, no randomness (use SC.hash).
// Numbers come from the ledger (storyboard.md) and dots.js (generated from
// _data/scores.npz); never type a new one in a beat.
//
// Layout (px, 1080×1920; captions anchored bottom, so the stage runs to 1330):
//   tag            y 240–372   two lines, left at x 120
//   user pile      y 400–587   teal, above the axis
//   axis           y 590       score 0 at x 120, 1 at x 920; threshold 0.70 at x 680
//   attack pile    y 602–673   gold, below the axis
//   axis labels    y 690–756
//   box headers    y 785–851   "attack" / "real user"
//   box cells      y 858–1170  two rows of 151 px, tag over count
//   fraction rows  y 1196–1330 "recall 40 / 50 80%", "precision 40 / 100 40%"
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
  const X0 = D.x0, X1 = D.x1, AXIS_Y = D.axisY, T = D.threshold;
  const X = (s) => X0 + s * (X1 - X0);
  const TX = X(T);
  const MID_X = 507;                      // centre of the safe width (65–950)
  const USER_R = 1.7, ATK_R = 6.5;
  const TAG_X = 80;   // the tag's second line runs ~850 px; at x 120 (ep 1) it crossed the right safe edge, 950
  const LEDGER = { n: 10000, attacks: 50, users: 9950, tp: 40, fp: 60, fn: 10, tn: 9890, flagged: 100,
                   recall: "80%", precision: "40%" };

  function ground(g) {
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.fillStyle = rgba(COL.bg); g.fillRect(0, 0, W, H);
  }

  function axis(g) {
    g.strokeStyle = rgba(COL.muted); g.lineWidth = 4; g.lineCap = "round";
    g.beginPath(); g.moveTo(X0 - 14, AXIS_Y); g.lineTo(X1 + 14, AXIS_Y); g.stroke();
    [0, 1].forEach((s) => { g.beginPath(); g.moveTo(X(s), AXIS_Y - 10); g.lineTo(X(s), AXIS_Y + 10); g.stroke(); });
  }

  // Every dot, at home on the score line. o.flag 0..1: flagged dots (score > 0.70)
  // light up. o.ring {tp, fp, fn}: 0..1, ring that group's dots (attacks get a
  // ring, users brighten and grow). o.userPulse / o.attackRing: one-shot accents
  // (attackRing rings all 50). o.dimUsers 0..1: unflagged users fade back.
  function dots(g, o = {}) {
    const flag = o.flag || 0, up = o.userPulse || 0, ringAll = o.attackRing || 0, R = o.ring || {};
    const U = D.users, A = D.attacks;
    const ucol = mixc(COL.data, COL.text, 0.35 * up);
    for (let i = 0; i < U.x.length; i++) {
      const k = U.g[i], lit = k === "fp" ? Math.max(flag, R.fp || 0) : 0, rg = k === "fp" ? R.fp || 0 : 0;
      g.fillStyle = rgba(lit ? mixc(ucol, COL.text, lit) : ucol, 0.8 + 0.2 * lit);
      const r = USER_R + 1.6 * lit + 1.4 * rg;
      g.fillRect(U.x[i] - r, U.y[i] - r, 2 * r, 2 * r);
      if (rg > 0) {   // a ringed user (fp) gets a teal halo, so the 60 read as a group
        g.strokeStyle = rgba(COL.data, rg); g.lineWidth = 2.5;
        g.beginPath(); g.arc(U.x[i], U.y[i], r + 4 * rg, 0, Math.PI * 2); g.stroke();
      }
    }
    for (let i = 0; i < A.x.length; i++) {
      const x = A.x[i], y = A.y[i], k = A.g[i];
      g.fillStyle = rgba(COL.attack);
      g.beginPath(); g.arc(x, y, ATK_R, 0, Math.PI * 2); g.fill();
      const lit = k === "tp" ? flag : 0, rg = Math.max(R[k] || 0, ringAll);
      const rr = Math.max(lit, rg);
      if (rr > 0) {
        g.strokeStyle = rgba(COL.text, rr); g.lineWidth = 2.5 + 1.5 * rg;
        g.beginPath(); g.arc(x, y, ATK_R + 3 + 4 * rg, 0, Math.PI * 2); g.stroke();
      }
    }
  }

  // The threshold: the series hero in ep 1; here it rests dimmed (thrDim 1).
  function threshold(g, u, o = {}) {
    if (u <= 0) return;
    const top = 392, bot = 676, y0 = lerp(top - 140, top, u);
    g.strokeStyle = rgba(o.color || COL.hero, clamp01(u * 1.5)); g.lineWidth = 8; g.lineCap = "round";
    g.beginPath(); g.moveTo(TX, y0); g.lineTo(TX, lerp(y0 + 30, bot, u)); g.stroke();
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
  // o.bright 0..1 lights line 1; o.atk 0..1 lights "50 attacks".
  function makeTag(root) {
    const l1 = el(root, `left:${TAG_X}px;top:240px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`,
      "prompt-injection detector");
    const l2 = el(root, `left:${TAG_X}px;top:306px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`,
      `10,000 requests · <span style="color:${rgba(COL.attack)}">50 attacks</span>`);
    const n = l2.querySelector("span");
    return {
      l1, l2,
      set(o = {}) {
        l1.style.color = rgba(mixc(COL.dim, COL.text, o.bright || 0));
        l2.style.color = rgba(mixc(COL.dim, COL.text, o.bright2 || 0));
        n.style.color = rgba(mixc(COL.attack, COL.text, 0.5 * (o.atk || 0)));
        show(l1, 1); show(l2, 1);
      },
    };
  }

  function makeAxisLabels(root) {
    const c = `top:690px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`;
    el(root, c + `left:${X0 - 18}px;`, "0");
    el(root, c + `left:${X1 - 18}px;`, "1");
    el(root, c + `left:${MID_X - 220}px;width:440px;text-align:center;`, "attack score");
  }

  // ---- The box ----
  // Rows: flagged / not flagged. Columns: attack / real user.
  // tp top-left, fp top-right, fn bottom-left, tn bottom-right.
  const BOX = { left: 340, right: 945, top: 858, bottom: 1170, gap: 10, headY: 785, rowX: 80 };
  const CELLS = ["tp", "fp", "fn", "tn"];
  const TAGS = { tp: "TP", fp: "FP", fn: "FN", tn: "TN" };
  // ep 2's words for the two mistakes (beats 7–8): the tag swaps to them
  const ALT = { fn: ["missed", COL.attack], fp: ["wasted", COL.data] };
  function geom() {
    const w = BOX.right - BOX.left - BOX.gap, h = BOX.bottom - BOX.top - BOX.gap;
    const xm = BOX.left + w / 2, ym = BOX.top + h / 2;
    const r = (x0, y0, x1, y1) => ({ x: x0, y: y0, w: x1 - x0, h: y1 - y0 });
    return {
      tp: r(BOX.left, BOX.top, xm, ym), fp: r(xm + BOX.gap, BOX.top, BOX.right, ym),
      fn: r(BOX.left, ym + BOX.gap, xm, BOX.bottom), tn: r(xm + BOX.gap, ym + BOX.gap, BOX.right, BOX.bottom),
    };
  }
  // the attack column (recall's denominator) and the flagged row (precision's)
  function groupRect(kind) {
    const G = geom();
    return kind === "col" ? { x: G.tp.x, y: G.tp.y, w: G.tp.w, h: G.fn.y + G.fn.h - G.tp.y }
                          : { x: G.tp.x, y: G.tp.y, w: G.fp.x + G.fp.w - G.tp.x, h: G.tp.h };
  }
  function makeBox(root) {
    const head = (txt, col) => el(root, `top:${BOX.headY}px;font-size:60px;line-height:66px;text-align:center;width:300px;color:${rgba(col)};`, txt);
    const hA = head("attack", COL.attack), hU = head("real user", COL.data);
    const rowL = (txt) => el(root, `left:${BOX.rowX}px;top:0;width:250px;font-size:60px;line-height:64px;color:${rgba(COL.dim)};white-space:normal;`, txt);
    const rF = rowL("flagged"), rN = rowL("not<br>flagged");
    const cells = {};
    CELLS.forEach((k) => {
      const tag = el(root, `font-size:60px;line-height:60px;color:${rgba(COL.dim)};`, TAGS[k]);
      const alt = ALT[k] ? el(root, `font-size:60px;line-height:60px;color:${rgba(ALT[k][1])};`, ALT[k][0]) : null;
      const num = el(root, `font-size:84px;line-height:76px;color:${rgba(COL.text)};`, LEDGER[k].toLocaleString("en-US"));
      cells[k] = { tag, alt, num };
    });
    const G = geom();
    hA.style.left = G.tp.x + G.tp.w / 2 - 150 + "px"; hU.style.left = G.fp.x + G.fp.w / 2 - 150 + "px";
    rF.style.top = G.tp.y + G.tp.h / 2 - 33 + "px"; rN.style.top = G.fn.y + G.fn.h / 2 - 64 + "px";
    CELLS.forEach((k) => {
      const c = G[k], { tag, alt, num } = cells[k];
      tag.style.left = c.x + 18 + "px"; tag.style.top = c.y + 6 + "px";
      if (alt) { alt.style.left = c.x + 18 + "px"; alt.style.top = c.y + 6 + "px"; }
      num.style.left = c.x + 18 + "px"; num.style.top = c.y + 72 + "px";
    });
    return {
      cells,
      // o.lit[k] 0..1 (magenta frame + tag), o.bright[k] 0..1 (count pulses white→bigger),
      // o.ghost[k] 0..1 (the cell fades to muted, a strike runs through it),
      // o.alt[k] 0..1 (fn / fp: the tag crossfades to "missed" / "wasted")
      set(o = {}) {
        show(hA, 1); show(hU, 1); show(rF, 1); show(rN, 1);
        CELLS.forEach((k) => {
          const lit = o.lit ? o.lit[k] || 0 : 0, gh = o.ghost ? o.ghost[k] || 0 : 0;
          const al = o.alt ? o.alt[k] || 0 : 0, br = o.bright ? o.bright[k] || 0 : 0;
          const { tag, alt, num } = cells[k], fade = 1 - 0.7 * gh;
          tag.style.color = rgba(mixc(COL.dim, COL.hero, lit));
          show(tag, fade * (1 - al));
          if (alt) { show(alt, al); alt.style.color = rgba(mixc(ALT[k][1], COL.hero, lit)); }
          show(num, fade);
          num.style.transformOrigin = "0 0";   // grows down, away from the tag above it
          num.style.transform = `scale(${1 + 0.1 * br})`;
        });
      },
      // Canvas part: cell frames; a lit cell gets the magenta frame; a ghosted one a strike.
      draw(g, o = {}) {
        const G = geom();
        CELLS.forEach((k) => {
          const c = G[k], lit = o.lit ? o.lit[k] || 0 : 0, gh = o.ghost ? o.ghost[k] || 0 : 0;
          g.fillStyle = rgba(mixc(COL.panel, COL.bg, gh));
          g.strokeStyle = rgba(mixc(mixc(COL.muted, COL.hero, lit), COL.panel, 0.5 * gh)); g.lineWidth = 4 + 2 * lit;
          g.beginPath(); g.roundRect(c.x, c.y, c.w, c.h, 14); g.fill(); g.stroke();
          const st = o.strike ? o.strike[k] || 0 : 0;
          if (st > 0) {
            g.strokeStyle = rgba(COL.dim); g.lineWidth = 6; g.lineCap = "round";
            const x0 = c.x + 18, y0 = c.y + c.h - 22, x1 = c.x + c.w - 18, y1 = c.y + 22;
            g.beginPath(); g.moveTo(x0, y0); g.lineTo(lerp(x0, x1, st), lerp(y0, y1, st)); g.stroke();
          }
        });
      },
    };
  }

  // ---- The fraction rows ----
  // Two rows under the box: label | numerator / denominator | percentage.
  //   recall     40 / 50    80%
  //   precision  40 / 100   40%
  // The numerator is gold (attacks caught). Per row: lit 0..1 (label magenta: the
  // row is the hero), num / den / pct 0..1 (each fades and drops in 16 px),
  // pctHero 0..1 (the percentage is magenta as it lands).
  const ROWS = { r: { y: 1196, label: "recall", den: LEDGER.attacks, pct: LEDGER.recall },
                 p: { y: 1264, label: "precision", den: LEDGER.flagged, pct: LEDGER.precision } };
  const FR = { labelX: 80, numR: 556, slashX: 574, denX: 624, pctR: 945 };
  // where a lifted group lands: the denominator's slot
  const denRect = (k) => ({ x: FR.denX - 14, y: ROWS[k].y - 4, w: k === "p" ? 148 : 110, h: 74 });
  const numPos = (k) => ({ x: FR.numR - 76, y: ROWS[k].y });   // left edge of "40" at 60 px
  function makeBars(root) {
    const rows = {};
    Object.keys(ROWS).forEach((k) => {
      const R = ROWS[k], c = `top:${R.y}px;font-size:60px;line-height:66px;`;
      rows[k] = {
        label: el(root, c + `left:${FR.labelX}px;color:${rgba(COL.dim)};`, R.label),
        num: el(root, c + `left:${FR.numR - 200}px;width:200px;text-align:right;color:${rgba(COL.attack)};`, String(LEDGER.tp)),
        slash: el(root, c + `left:${FR.slashX}px;color:${rgba(COL.dim)};`, "/"),
        den: el(root, c + `left:${FR.denX}px;color:${rgba(COL.text)};`, String(R.den)),
        pct: el(root, c + `left:${FR.pctR - 220}px;width:220px;text-align:right;color:${rgba(COL.text)};`, R.pct),
      };
    });
    // the numerator in flight: a copy of TP's 40 that travels from the cell to the row
    const fly = el(root, `left:0;top:0;font-size:84px;line-height:76px;color:${rgba(COL.text)};transform-origin:0 0;`, String(LEDGER.tp));
    fly.setAttribute("data-layout-allow-overlap", "");   // passes over the cells on its way down, on purpose
    return {
      rows, fly,
      set(o = {}) {
        Object.keys(ROWS).forEach((k) => {
          const s = o[k] || {}, e = rows[k];
          e.label.style.color = rgba(mixc(COL.dim, COL.hero, s.lit || 0));
          show(e.label, 1);
          [["num", s.num], ["den", s.den], ["pct", s.pct]].forEach(([n, u]) => {
            u = u || 0; show(e[n], u); e[n].style.transform = `translateY(${-16 * (1 - u)}px)`;
          });
          show(e.slash, Math.max(s.num || 0, s.den || 0));
          e.pct.style.color = rgba(mixc(COL.text, COL.hero, s.pctHero || 0));
          e.den.style.color = rgba(mixc(COL.text, COL.hero, s.denHero || 0));
        });
        // o.flyNum = { row: "r" | "p", u: 0..1 }: the 40 from the TP cell to the row's numerator
        const f = o.flyNum;
        if (f && f.u > 0 && f.u < 1) {
          const c = geom().tp, ease = gsap.parseEase("power2.inOut")(f.u), to = numPos(f.row);
          const x = lerp(c.x + 18, to.x, ease), y = lerp(c.y + 72, to.y, ease), sc = lerp(1, 60 / 84, ease);
          fly.style.transform = `translate(${x}px, ${y}px) scale(${sc})`;
          fly.style.color = rgba(mixc(COL.text, COL.attack, ease));
          show(fly, 1);
        } else show(fly, 0);
      },
    };
  }

  // The lift: a magenta frame that leaves the box around the attack column
  // (kind "col", recall) or the flagged row (kind "row", precision) and shrinks
  // onto that row's denominator. o = { kind, u 0..1, a 0..1 }.
  function lift(g, o) {
    if (!o || !(o.a > 0)) return;
    const from = groupRect(o.kind), to = denRect(o.kind === "col" ? "r" : "p");
    const e = gsap.parseEase("power2.inOut")(clamp01(o.u || 0));
    const r = { x: lerp(from.x, to.x, e), y: lerp(from.y, to.y, e), w: lerp(from.w, to.w, e), h: lerp(from.h, to.h, e) };
    g.strokeStyle = rgba(COL.hero, o.a); g.lineWidth = 7;
    g.beginPath(); g.roundRect(r.x, r.y, r.w, r.h, lerp(16, 12, e)); g.stroke();
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
  // S fields (all optional; defaults are the rest state):
  //   flag 0..1                  flagged dots lit (1 at rest)
  //   ring {tp, fp, fn} 0..1     ring a group's dots on the score line
  //   userPulse, attackRing 0..1 one-shot accents
  //   tag {bright, bright2, atk} 0..1
  //   box {lit, bright, ghost, strike, alt}: per-cell maps, 0..1
  //   lift {kind: "col"|"row", u, a}
  //   bars {r: {lit, num, den, pct, pctHero, denHero}, p: {...}, flyNum: {row, u}}
  function mount(root) {
    const tag = makeTag(root); makeAxisLabels(root);
    const box = makeBox(root), bars = makeBars(root);
    guides(root);
    function draw(g, S) {
      ground(g); axis(g);
      box.draw(g, S.box || {});
      dots(g, { flag: S.flag == null ? 1 : S.flag, ring: S.ring, userPulse: S.userPulse, attackRing: S.attackRing });
      threshold(g, 1, { color: mixc(COL.hero, COL.dim, 1) });
      lift(g, S.lift);
      tag.set(S.tag || {});
      box.set(S.box || {});
      bars.set(S.bars || {});
    }
    return { draw, tag, box, bars };
  }

  const FULL = { num: 1, den: 1, pct: 1 };
  const SEAM = {
    // frame 0 of the Short: score line, box counted, both rows labelled and empty
    0: {},
    // end of beat 1: the attack column lit, its dots ringed, "recall" lit
    1: { ring: { tp: 1, fn: 1 }, box: { lit: { tp: 1, fn: 1 } }, bars: { r: { lit: 1 } } },
    // end of beat 2: back at rest
    2: {},
    // end of beat 3: recall row filled, 40 / 50 80%, at rest
    3: { bars: { r: FULL } },
    // end of beat 4: the flagged row lit, its 100 dots ringed, "precision" lit
    4: { ring: { tp: 1, fp: 1 }, box: { lit: { tp: 1, fp: 1 } }, bars: { r: FULL, p: { lit: 1 } } },
    // end of beat 5: both rows filled, at rest
    5: { bars: { r: FULL, p: FULL } },
    // end of beat 6: TN ghosted and struck through
    6: { box: { ghost: { tn: 1 }, strike: { tn: 1 } }, bars: { r: FULL, p: FULL } },
    // end of beat 7: FN lit and renamed "missed", its 10 dots ringed
    7: { ring: { fn: 1 }, box: { ghost: { tn: 1 }, strike: { tn: 1 }, lit: { fn: 1 }, alt: { fn: 1 } },
         bars: { r: FULL, p: FULL } },
    // end of beat 8 (the last frame, still): "missed" and "wasted" in place, nothing lit
    8: { box: { ghost: { tn: 1 }, strike: { tn: 1 }, alt: { fn: 1, fp: 1 } }, bars: { r: FULL, p: FULL } },
  };

  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });

  window.SC = { D, COL, LEDGER, W, H, X0, X1, X, TX, AXIS_Y, MID_X, BOX, CELLS, ROWS, FR,
                ground, axis, dots, threshold, makeTag, makeAxisLabels, makeBox, makeBars, lift, geom, groupRect,
                guides, mount, SEAM, E, lerp, clamp01, seg, hash, pulse, rgba, mixc };
})();
