// score.js — the shared kit for 013 ep01 (the accuracy trap).
//
// Every beat loads this (through its `kit` symlink, after kit/dots.js) so the
// score line, the threshold, the tag, the counter, the code card and the 2×2
// box are identical from beat to beat, and each beat opens on the previous
// beat's last frame. Pure functions of their arguments: no clocks, no
// randomness (use SC.hash). Numbers come from the ledger (storyboard.md) and
// dots.js (generated from _data/scores.npz); never type a new one in a beat.
//
// Layout (px, 1080×1920; captions anchored bottom, so the stage runs to 1330):
//   tag            y 240–372   two lines, left at x 120
//   user pile      y 400–587   teal, above the axis
//   axis           y 590       score 0 at x 120, 1 at x 920; threshold 0.70 at x 680
//   attack pile    y 602–673   gold, below the axis
//   axis labels    y 690–756
//   middle         y 790–1320  counter, code card, or the box
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
  const LEDGER = { n: 10000, attacks: 50, users: 9950, tp: 40, fp: 60, fn: 10, tn: 9890, correct: 9930,
                   accNever: "99.5%", accA: "99.3%" };

  function ground(g) {
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.fillStyle = rgba(COL.bg); g.fillRect(0, 0, W, H);
  }

  function axis(g, o = {}) {
    const a = o.alpha == null ? 1 : o.alpha;
    g.strokeStyle = rgba(COL.muted, a); g.lineWidth = 4; g.lineCap = "round";
    g.beginPath(); g.moveTo(X0 - 14, AXIS_Y); g.lineTo(X1 + 14, AXIS_Y); g.stroke();
    g.lineWidth = 4;
    [0, 1].forEach((s) => { g.beginPath(); g.moveTo(X(s), AXIS_Y - 10); g.lineTo(X(s), AXIS_Y + 10); g.stroke(); });
  }

  // Draw every dot. o.place(kind, i, hx, hy) may return [x, y] (a dot in
  // flight or in a cell) or null (stay home). o.flag: 0..1, flagged dots
  // (score > 0.70) light up. o.userPulse / o.attackRing: 0..1 one-shot accents.
  // o.alpha(kind, i): optional per-dot opacity. o.ghost: 0..1, a placed dot
  // leaves a muted copy at home, so the score line keeps its shape.
  function dots(g, o = {}) {
    const flag = o.flag || 0, up = o.userPulse || 0, ring = o.attackRing || 0;
    const U = D.users, A = D.attacks;
    const ucol = mixc(COL.data, COL.text, 0.35 * up);
    for (let i = 0; i < U.x.length; i++) {
      let x = U.x[i], y = U.y[i];
      const p = o.place && o.place("user", i, x, y);
      if (p) {
        if (o.ghost) { g.fillStyle = rgba(COL.muted, o.ghost); g.fillRect(x - USER_R, y - USER_R, 2 * USER_R, 2 * USER_R); }
        x = p[0]; y = p[1];
      }
      const a = o.alpha ? o.alpha("user", i) : 1;
      if (a <= 0) continue;
      const lit = U.g[i] === "fp" ? flag : 0;
      g.fillStyle = rgba(lit ? mixc(ucol, COL.text, lit) : ucol, (0.8 + 0.2 * lit) * a);
      const r = USER_R + 1.6 * lit;
      g.fillRect(x - r, y - r, 2 * r, 2 * r);
    }
    for (let i = 0; i < A.x.length; i++) {
      let x = A.x[i], y = A.y[i];
      const p = o.place && o.place("attack", i, x, y);
      if (p) {
        if (o.ghost) { g.fillStyle = rgba(COL.muted, o.ghost); g.beginPath(); g.arc(x, y, ATK_R, 0, Math.PI * 2); g.fill(); }
        x = p[0]; y = p[1];
      }
      const a = o.alpha ? o.alpha("attack", i) : 1;
      if (a <= 0) continue;
      g.fillStyle = rgba(COL.attack, a);
      g.beginPath(); g.arc(x, y, ATK_R, 0, Math.PI * 2); g.fill();
      const lit = A.g[i] === "tp" ? flag : 0;
      const rr = Math.max(lit, ring);
      if (rr > 0) {
        g.strokeStyle = rgba(COL.text, rr * a); g.lineWidth = 2.5;
        g.beginPath(); g.arc(x, y, ATK_R + 3 + 4 * ring, 0, Math.PI * 2); g.stroke();
      }
    }
  }

  // The threshold: the series hero. u 0..1 drops it in from above.
  // o.color overrides magenta (a retired hero goes muted).
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
  function makeTag(root) {
    const l1 = el(root, `left:${X0}px;top:240px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`,
      "prompt-injection detector");
    const l2 = el(root, `left:${X0}px;top:306px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`,
      `10,000 requests · <span style="color:${rgba(COL.attack)}">50 attacks</span>`);
    return {
      l1, l2,
      set(o = {}) {
        const b = o.bright || 0;
        l1.style.color = rgba(mixc(COL.dim, COL.text, b));
        show(l2, o.opacity == null ? 1 : o.opacity);
        show(l1, o.opacity == null ? 1 : o.opacity);
      },
    };
  }

  function makeAxisLabels(root) {
    const c = `top:690px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`;
    const z = el(root, c + `left:${X0 - 18}px;`, "0");
    const one = el(root, c + `left:${X1 - 18}px;`, "1");
    const name = el(root, c + `left:${MID_X - 220}px;width:440px;text-align:center;`, "attack score");
    return { z, one, name };
  }

  // The counter. compact 0..1 (beat 2, with the code card): the label and the
  // caught line fade and the value shrinks to the top of the middle.
  function makeCounter(root) {
    const c = `left:${MID_X - 420}px;width:840px;text-align:center;`;
    const lab = el(root, c + `top:790px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`, "accuracy");
    const val = el(root, c + `top:868px;font-size:190px;line-height:200px;color:${rgba(COL.text)};transform-origin:50% 0;`, LEDGER.accNever);
    const sub = el(root, c + `top:1080px;font-size:60px;line-height:66px;color:${rgba(COL.dim)};`);
    return {
      lab, val, sub,
      set(o = {}) {
        const k = o.compact || 0, op = o.opacity == null ? 1 : o.opacity;
        show(lab, op * (1 - k));
        show(val, op);
        val.style.transform = `translateY(${-90 * k}px) scale(${lerp(1, 0.62, k)})`;
        if (o.value != null) val.textContent = o.value;
        val.style.color = rgba(o.valueColor || COL.text);
        const caught = o.caught == null ? 0 : o.caught, p = o.pulseCaught || 0;
        sub.innerHTML = `attacks caught <span style="color:${rgba(mixc(COL.attack, COL.text, p))}">${caught} / 50</span>`;
        sub.style.transform = `scale(${1 + 0.12 * p})`;
        show(sub, op * (1 - k) * (o.subOpacity == null ? 1 : o.subOpacity));
      },
    };
  }

  // The code card: the ledger's three lines of PyTorch (the first split in two
  // so it fits the safe width) and the output. active: line index lit, -1 none.
  const CODE = ["y = torch.zeros(10_000)", "y[:50] = 1", "pred = torch.zeros(10_000)", "(pred == y).float().mean()"];
  const CODE_OUT = "tensor(0.9950)";
  function makeCode(root) {
    const card = el(root, `left:70px;top:930px;width:878px;padding:18px 20px;border-radius:18px;` +
      `background:${rgba(COL.panel)};border:5px solid ${rgba(COL.muted)};font-size:52px;line-height:64px;color:${rgba(COL.text)};`);
    const rows = CODE.map((s) => el(card, "position:relative;padding:0 6px;border-radius:8px;", s.replace(/ /g, "&nbsp;")));
    const out = el(card, `position:relative;padding:0 6px;color:${rgba(COL.data)};`, CODE_OUT);
    rows.forEach((r) => (r.style.position = "relative"));
    out.style.position = "relative";
    [card, ...card.querySelectorAll("*")].forEach((e) => { e.style.fontFamily = "monospace"; e.style.fontWeight = "700"; });
    return {
      card, rows, out,
      set(o = {}) {
        show(card, o.opacity == null ? 1 : o.opacity);
        card.style.transform = `translateY(${(o.dy || 0)}px)`;
        rows.forEach((r, i) => {
          const on = o.lit ? o.lit[i] || 0 : 0;
          r.style.background = on ? rgba(COL.hero, 0.28 * on) : "transparent";
        });
        show(out, o.out == null ? 0 : o.out);
        out.style.color = rgba(mixc(COL.data, COL.hero, o.outHero || 0));
      },
    };
  }

  // ---- The box ----
  // Rows: flagged / not flagged. Columns: attack / real user.
  // tp top-left, fp top-right, fn bottom-left, tn bottom-right.
  // split.cx / split.cy: share of the cell width / height for column 1 / row 1
  // (0.5 at rest; beat 6 shrinks them so tn swells).
  const BOX = { left: 340, right: 945, top: 860, bottom: 1320, gap: 10, headY: 785, rowX: 80 };
  const CELLS = ["tp", "fp", "fn", "tn"];
  const TAGS = { tp: "TP", fp: "FP", fn: "FN", tn: "TN" };
  function geom(split = {}) {
    const cx = split.cx == null ? 0.5 : split.cx, cy = split.cy == null ? 0.5 : split.cy;
    const w = BOX.right - BOX.left - BOX.gap, h = BOX.bottom - BOX.top - BOX.gap;
    const xm = BOX.left + w * cx, ym = BOX.top + h * cy;
    const r = (x0, y0, x1, y1) => ({ x: x0, y: y0, w: x1 - x0, h: y1 - y0 });
    return {
      tp: r(BOX.left, BOX.top, xm, ym), fp: r(xm + BOX.gap, BOX.top, BOX.right, ym),
      fn: r(BOX.left, ym + BOX.gap, xm, BOX.bottom), tn: r(xm + BOX.gap, ym + BOX.gap, BOX.right, BOX.bottom),
    };
  }
  // Where dot `rank` of `group` sits in its cell: a grid in the cell's lower part.
  function slot(group, rank, G) {
    const c = G[group], n = LEDGER[group];
    const pad = 16, rx = c.x + pad, ry = c.y + 174, rw = c.w - 2 * pad, rh = Math.max(20, c.h - 174 - pad);
    const big = group === "tp" || group === "fn";
    const pitch = big ? 15 : Math.min(6, Math.sqrt((rw * rh) / n));
    const cols = Math.max(1, Math.floor(rw / pitch));
    const col = rank % cols, row = Math.floor(rank / cols);
    return [rx + pitch / 2 + col * pitch, ry + pitch / 2 + row * pitch];
  }
  function makeBox(root) {
    const head = (txt, col) => el(root, `top:${BOX.headY}px;font-size:60px;line-height:66px;text-align:center;width:300px;color:${rgba(col)};`, txt);
    const hA = head("attack", COL.attack), hU = head("real user", COL.data);
    const rowL = (txt, top) => el(root, `left:${BOX.rowX}px;top:${top}px;width:250px;font-size:60px;line-height:64px;color:${rgba(COL.dim)};white-space:normal;`, txt);
    const rF = rowL("flagged", 0), rN = rowL("not<br>flagged", 0);
    const cells = {};
    CELLS.forEach((k) => {
      const tag = el(root, `font-size:60px;line-height:66px;color:${rgba(COL.dim)};`, TAGS[k]);
      const num = el(root, `font-size:84px;line-height:92px;color:${rgba(COL.text)};`, LEDGER[k].toLocaleString("en-US"));
      cells[k] = { tag, num };
    });
    return {
      cells,
      // DOM part of the box. o.opacity (whole box), o.split, o.show[k] (tag+count), o.lit[k] (0..1 hero)
      // o.note[k] overrides a count's text (beat 6: "9,890 of 9,930").
      set(o = {}) {
        const G = geom(o.split), op = o.opacity == null ? 1 : o.opacity;
        const hc = (c) => c.x + c.w / 2 - 150;
        hA.style.left = hc(G.tp) + "px"; hU.style.left = hc(G.fp) + "px";
        show(hA, op); show(hU, op);
        rF.style.top = G.tp.y + G.tp.h / 2 - 33 + "px"; rN.style.top = G.fn.y + G.fn.h / 2 - 64 + "px";
        const ro = op * (o.rowOpacity == null ? 1 : o.rowOpacity); show(rF, ro); show(rN, ro);
        CELLS.forEach((k) => {
          const c = G[k], s = (o.show ? o.show[k] || 0 : 0) * op, lit = o.lit ? o.lit[k] || 0 : 0;
          const { tag, num } = cells[k];
          tag.style.left = c.x + 18 + "px"; tag.style.top = c.y + 12 + "px";
          num.style.left = c.x + 18 + "px"; num.style.top = c.y + 76 + "px";
          show(tag, s); show(num, s);
          tag.style.color = rgba(mixc(COL.dim, COL.hero, lit));
          num.textContent = o.note && o.note[k] ? o.note[k] : LEDGER[k].toLocaleString("en-US");
        });
      },
      // Canvas part: cell frames; a lit cell gets the magenta frame.
      draw(g, o = {}) {
        const G = geom(o.split), op = o.opacity == null ? 1 : o.opacity;
        if (op <= 0) return;
        CELLS.forEach((k) => {
          const c = G[k], lit = o.lit ? o.lit[k] || 0 : 0;
          g.fillStyle = rgba(COL.panel, op);
          g.strokeStyle = rgba(mixc(COL.muted, COL.hero, lit), op); g.lineWidth = 4 + 2 * lit;
          g.beginPath(); g.roundRect(c.x, c.y, c.w, c.h, 14); g.fill(); g.stroke();
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
    const d = document.createElement("div");   // the caption line (anchored bottom) stays clear of the stage
    d.style.cssText = "position:absolute;left:0;top:1330px;width:1080px;height:3px;background:rgba(255,200,60,0.6);";
    root.appendChild(d);
  }

  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });

  window.SC = { D, COL, LEDGER, W, H, X0, X1, X, TX, AXIS_Y, MID_X, BOX, CELLS, CODE, CODE_OUT,
                ground, axis, dots, threshold, makeTag, makeAxisLabels, makeCounter, makeCode, makeBox, geom, slot,
                guides, E, lerp, clamp01, seg, hash, pulse, rgba, mixc };
})();
