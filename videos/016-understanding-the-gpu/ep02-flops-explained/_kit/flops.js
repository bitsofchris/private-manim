// flops.js — ep 2's own parts, drawn over the series chip (../../_kit/chip.js).
// Linked into a beat as `ep/` (ln -s ../_kit NN_beat/ep), loaded after kit/code.js
// and before ep/seam.js. Not shared: other episodes never load it.
//
//   const kit = EP.mount(root);   // SC.mount + ep 2's parts
//   kit.draw(S);                  // S = the kit's fields + `card` + `float`
//
// kit.draw passes S to the chip as draw(S, S): tools/hf_state_check.js wraps
// draw(g, S) (the 013/014 kits' signature) and records its second argument.
//
// Parts (px, 1080×1920):
//   card     the top slot, x 65–950, y 245–435, in the CPU and queue's place
//            (they are off all episode: S.cpu 0, S.queueO 0). Two content
//            layers crossfade: card = {o, A, B, mix}; A at 1 − mix, B at mix.
//            Seam states use B: null, mix: 0. (card.y moves it; 00_layout's take B only.)
//   float    the zoom into one number, over the chip and the side slot (x 65–950,
//            y 450–1078), grown out of cell (row 5, col 5):
//            float = {o, grow, row1, row2, glide1, glide2, anat, anatO, lab: [s, d, e]}
//   core     the zoom into one core: the same panel and grow as float, showing the
//            arithmetic that core does. core = {o, grow, mode, ...}:
//              mode "op":  `1.5 × 2.0 = 3.0`, the 3.0 carried down, `3.0 + 0.5 = 3.5`;
//                          mul, carry, add 0..1 (each step's progress), n (the counter),
//                          lit "mul"|"add"|null (that sign teal)
//              mode "dot": one output of the tiny layer, x = [1.0 2.0 0.5], w = [0.5 1.5 2.0]:
//                          step 0..3 (pair i runs over [i, i+1): multiply at +0.25, add at +0.5);
//                          the counter (2 per pair, 6 in all) and y follow from step
//   acro     "FLOP" over the card, unpacking into FLOATING-POINT / OPERATION: acro = {o, u};
//            u 0 is "FLOP" alone, u 1 the two words; F L O P magenta on hero "acronym"
//   stream   numbers leaving GPU memory along the pipe into the chip: stream = {o, phase}
//            (phase: seconds; teal squares outlined in the background colour, 3 a pipe, 0.6 s apart)
//
// Card content {kind, ...} (every string is ep 2's ledger, storyboard.md):
//   op      `a × b + c` and a counter:  n (0|1|2), lit ("mul"|"add"|null: that sign teal)
//   name    "floating-point" / "operation", the fl and op letters magenta on hero "acronym"
//   word    one word: word ("weights" | "activations" | "gradients")
//   count   "FLOPs" (its s magenta on hero "s") / at o2: "720 trillion = 7.2 × 10¹⁴", or
//           while v < 1 the count rolling up to 720,000,000,000,000 (mono, so it doesn't jitter)
//   rate    "FLOPS" (its S magenta on hero "S") / "per second", and a 1 s clock at the
//           card's right: clockO its opacity, clock 0..1 its sweep (magenta on hero "clock")
//   matmul  `y = x @ W`
//   frac    "FLOPs ÷ FLOPS" / "= GPU-hours" (hero "hours") and " = $" at dollar (hero "bill")
//
// Hero names of ep 2's parts (S.hero, one at a time; the chip's own names still work):
//   count (the core's counter), acronym, sign, digits, exp, point, s, S, clock,
//   expr (the dot's running line), hours, bill
(function () {
  const SC = window.SC, PAL = SC.PAL, { clamp01, seg, lerp, show } = SC;
  const CARD = { x: 65, y: 245, w: 885, h: 190 };
  const PANEL = { x: 65, y: 450, w: 885, h: 628 };
  const c = SC.G.chip, CELL = { x: c.x + c.pad + 5 * c.pitch, y: c.y + c.pad + 5 * c.pitch, s: c.cell };
  const MONO = "monospace";

  // ---- card content → rows of spans {t, c, mono, size} ----
  const ink = PAL.ink, dim = PAL.dim, data = PAL.data, mag = PAL.hero;
  const h = (hero, name, base) => (hero === name ? mag : base);
  function rows(K, hero) {
    if (!K) return [];
    switch (K.kind) {
      case "word": return [[{ t: K.word, size: 84 }]];
      case "count": {
        const o2 = K.o2 == null ? 0 : K.o2;
        const row2 = K.v != null && K.v < 1
          ? [{ t: Math.round(720e12 * clamp01(K.v)).toLocaleString("en-US"), mono: 1, size: 60, c: data, o: o2 }]
          : [{ t: "720 trillion", size: 60, c: data, o: o2 }, { t: " = 7.2 × 10", size: 60, o: o2 },
             { t: "14", size: 40, sup: 1, o: o2 }];
        return [[{ t: "FLOP", size: 96 }, { t: "s", size: 96, c: h(hero, "s", ink) }], row2];
      }
      case "rate": return [[{ t: "FLOP", size: 96 }, { t: "S", size: 96, c: h(hero, "S", ink) }],
                           [{ t: "per second", size: 64, c: dim }]];
      case "matmul": return [[{ t: "y = x @ W", mono: 1, size: 84 }]];
      case "frac": return [
        [{ t: "FLOPs ÷ FLOPS", size: 84 }],
        [{ t: "= GPU-hours", size: 72, c: h(hero, "hours", ink) },
         { t: " = $", size: 72, c: h(hero, "bill", ink), o: K.dollar == null ? 0 : K.dollar }]];
    }
    return [];
  }

  function makeLayer(root) {
    const rowsEl = [0, 1].map(() => {
      const r = document.createElement("div");
      r.style.cssText = `position:absolute;left:${CARD.x}px;width:${CARD.w}px;text-align:center;white-space:pre;`;
      root.appendChild(r);
      const spans = [...Array(8)].map(() => { const s = document.createElement("span"); r.appendChild(s); return s; });
      return { r, spans };
    });
    function set(K, hero, o, top) {
      const R = rows(K, hero);
      const lh = R.map((row) => Math.round(Math.max(...row.map((s) => s.size)) * 1.12));
      let y = top + (CARD.h - lh.reduce((a, b) => a + b, 0)) / 2;
      rowsEl.forEach((el, i) => {
        const row = R[i];
        show(el.r, row ? o : 0);
        if (!row) return;
        el.r.style.top = `${Math.round(y)}px`; el.r.style.height = `${lh[i]}px`; el.r.style.lineHeight = `${lh[i]}px`;
        y += lh[i];
        el.spans.forEach((sp, k) => {
          const s = row[k];
          if (!s) { sp.textContent = ""; sp.style.display = "none"; return; }
          sp.style.display = "inline";
          sp.textContent = s.t;
          sp.style.fontSize = `${s.size}px`;
          sp.style.color = s.c || ink;
          sp.style.opacity = s.o == null ? 1 : s.o;
          sp.style.fontFamily = s.mono ? MONO : "";
          sp.style.fontWeight = s.mono ? "700" : "";
          sp.style.position = s.sup ? "relative" : ""; sp.style.top = s.sup ? `-${Math.round(s.size * 0.7)}px` : "";
        });
      });
    }
    return { set };
  }

  // ---- the float panel ----
  function el(root, css, text) {
    const d = document.createElement("div");
    d.style.cssText = "position:absolute;white-space:pre;" + css;
    if (text != null) d.textContent = text;
    root.appendChild(d);
    return d;
  }
  const CW = 40, GAP = 24, DIG = { x: 110, size: 60 };        // mono 60 px is 36 wide; GAP: the point's own slot
  const ROW_Y = [500, 605];
  const NUMS = [
    { digits: "00000001", from: 1, to: 8, sci: ["+1.0 × 10", "−7"], anat: ["+", "1.0", "−7"] },   // 0.0000001 → 1.
    { digits: "3000000", from: 7, to: 1, sci: ["+3.0 × 10", "6"], anat: ["+", "3.0", "6"] },       // 3000000. → 3.000000
  ];
  const BOX = [{ x: 140, w: 110 }, { x: 320, w: 170 }, { x: 700, w: 130 }], TIMES = { x: 505, w: 180 };
  const BOX_Y = 740, BOX_H = 120, LAB_Y = 885, LAB = ["sign", "digits", "exponent"], BOXNAME = ["sign", "digits", "exp"];

  function makeFloat(root) {
    const panel = el(root, `background:${PAL.panel};border:6px solid ${PAL.ink};border-radius:28px;`);
    // the panel covers the chip and GPU memory's labels on purpose (the zoom)
    ["data-layout-allow-overflow", "data-layout-allow-occlusion"].forEach((a) => panel.setAttribute(a, ""));
    const rowsF = NUMS.map((N, r) => {
      const digits = [...N.digits].map((ch, i) => el(root, `top:${ROW_Y[r]}px;left:${DIG.x + i * CW}px;width:${CW}px;text-align:center;` +
        `font-size:${DIG.size}px;line-height:70px;`, ch));
      const point = el(root, `top:${ROW_Y[r]}px;font-size:${DIG.size}px;line-height:70px;width:20px;text-align:center;`, ".");
      const arrow = el(root, `top:${ROW_Y[r]}px;left:470px;font-size:60px;line-height:70px;color:${PAL.dim};`, "→");
      const sci = el(root, `top:${ROW_Y[r]}px;left:560px;font-size:60px;line-height:70px;`);
      sci.textContent = N.sci[0];
      const sup = document.createElement("sup"); sup.textContent = N.sci[1]; sup.style.fontSize = "40px"; sci.appendChild(sup);
      [...digits, point].forEach((d) => { d.style.fontFamily = MONO; d.style.fontWeight = "700"; });
      ["data-layout-allow-overlap", "data-layout-allow-occlusion"].forEach((a) => point.setAttribute(a, ""));  // between two digits on purpose
      return { digits, point, arrow, sci };
    });
    const boxes = BOX.map((b) => {
      const d = el(root, `top:${BOX_Y}px;left:${b.x}px;width:${b.w}px;height:${BOX_H}px;border:6px solid ${PAL.ink};border-radius:18px;` +
        `text-align:center;font-size:72px;line-height:${BOX_H - 12}px;box-sizing:border-box;`);
      return d;
    });
    const times = el(root, `top:${BOX_Y}px;left:${TIMES.x}px;width:${TIMES.w}px;text-align:center;font-size:72px;line-height:${BOX_H}px;`, "× 10");
    const labs = LAB.map((t, i) => el(root, `top:${LAB_Y}px;left:${BOX[i].x + BOX[i].w / 2 - 160}px;width:320px;text-align:center;` +
      `font-size:60px;line-height:70px;color:${PAL.dim};`, t));

    function set(F, hero) {
      F = Object.assign({ o: 0, grow: 1, row1: 0, row2: 0, glide1: 0, glide2: 0, anat: 1, anatO: 0, lab: [0, 0, 0] }, F || {});
      const g = clamp01(F.grow), o = F.o;
      growBox(panel, o, g);
      const inner = o * seg(g, 0.7, 1);
      rowsF.forEach((R, r) => {
        const N = NUMS[r], ro = inner * (r ? F.row2 : F.row1), gl = clamp01(r ? F.glide2 : F.glide1);
        const k = lerp(N.from, N.to, gl);                        // the point sits before digit k
        R.digits.forEach((d, i) => {
          // zeros the point has passed fade back: leading zeros (row 1), trailing zeros (row 2)
          const passed = r === 0 ? i < Math.floor(k + 1e-6) - 1 && N.digits[i] === "0"
                                 : i > Math.ceil(k - 1e-6) && N.digits[i] === "0";
          show(d, ro * (passed ? 0.3 : 1));
          d.style.left = `${DIG.x + i * CW + GAP * clamp01(i + 1 - k)}px`;   // digits right of the point step over its slot
          d.style.color = ink;
        });
        R.point.style.left = `${DIG.x + k * CW + GAP / 2 - 10}px`;
        R.point.style.color = hero === "point" ? mag : ink;
        show(R.point, ro); show(R.arrow, ro); show(R.sci, ro);
      });
      const A = NUMS[F.anat === 2 ? 1 : 0].anat, ao = inner * F.anatO;
      boxes.forEach((b, i) => {
        const on = hero === BOXNAME[i];
        b.textContent = A[i];
        b.style.borderColor = on ? mag : PAL.ink; b.style.color = on ? mag : ink;
        show(b, ao);
        labs[i].style.color = on ? mag : PAL.dim;
        show(labs[i], ao * (F.lab[i] || 0));
      });
      show(times, ao);
    }
    return { set, panel, rows: rowsF, boxes, labs };
  }

  // ---- the panel both zooms grow (float and core): out of cell (row 5, col 5) ----
  function growBox(box, o, g) {
    show(box, o * (g > 0 ? 1 : 0));
    Object.assign(box.style, { left: `${lerp(CELL.x, PANEL.x, g)}px`, top: `${lerp(CELL.y, PANEL.y, g)}px`,
      width: `${lerp(CELL.s, PANEL.w, g)}px`, height: `${lerp(CELL.s, PANEL.h, g)}px`,
      borderWidth: `${lerp(2, 6, g)}px`, borderRadius: `${lerp(6, 28, g)}px` });
  }
  function tile(root, x, y, w, hh, text, size) {
    const d = el(root, `top:${y}px;left:${x}px;width:${w}px;height:${hh}px;border:6px solid ${PAL.ink};border-radius:18px;` +
      `text-align:center;font-size:${size}px;line-height:${hh - 12}px;box-sizing:border-box;font-family:${MONO};font-weight:700;`, text);
    return d;
  }
  const sign = (root, x, y, hh, text) => el(root, `top:${y}px;left:${x}px;width:90px;text-align:center;font-size:72px;` +
    `line-height:${hh}px;font-family:${MONO};font-weight:700;`, text);

  // ---- the core view ----
  const OP = { yA: 580, yB: 750, h: 110, w: 170, x: [130, 305, 400, 575, 670], yN: 905 };
  const DOT = { x: [1.0, 2.0, 0.5], w: [0.5, 1.5, 2.0], cols: [250, 460, 670], tw: 170, th: 100, yX: 570, yW: 690,
                yOp: 815, yY: 935 };
  const f1 = (v) => v.toFixed(1);
  function makeCore(root) {
    const box = el(root, `background:${PAL.panel};border:6px solid ${PAL.ink};border-radius:28px;`);
    ["data-layout-allow-overflow", "data-layout-allow-occlusion"].forEach((a) => box.setAttribute(a, ""));
    const head = el(root, `top:470px;left:${PANEL.x}px;width:${PANEL.w}px;text-align:center;font-size:60px;line-height:80px;color:${PAL.dim};`,
      "inside one core");
    // op
    const X = OP.x;
    const A = [tile(root, X[0], OP.yA, OP.w, OP.h, "1.5", 72), sign(root, X[1], OP.yA, OP.h, "×"),
               tile(root, X[2], OP.yA, OP.w, OP.h, "2.0", 72), sign(root, X[3], OP.yA, OP.h, "="),
               tile(root, X[4], OP.yA, OP.w, OP.h, "3.0", 72)];
    const B = [tile(root, X[0], OP.yB, OP.w, OP.h, "3.0", 72), sign(root, X[1], OP.yB, OP.h, "+"),
               tile(root, X[2], OP.yB, OP.w, OP.h, "0.5", 72), sign(root, X[3], OP.yB, OP.h, "="),
               tile(root, X[4], OP.yB, OP.w, OP.h, "3.5", 72)];
    const nRow = el(root, `top:${OP.yN}px;left:${PANEL.x}px;width:${PANEL.w}px;text-align:center;line-height:120px;`);
    const nNum = document.createElement("span"); nNum.style.fontSize = "96px"; nRow.appendChild(nNum);
    const nLab = document.createElement("span"); nLab.style.fontSize = "60px"; nLab.style.color = PAL.dim; nRow.appendChild(nLab);
    // dot
    const lx = sign(root, 110, DOT.yX, DOT.th, "x"), lw = sign(root, 110, DOT.yW, DOT.th, "w");
    const xs = DOT.x.map((v, i) => tile(root, DOT.cols[i], DOT.yX, DOT.tw, DOT.th, f1(v), 64));
    const ws = DOT.w.map((v, i) => tile(root, DOT.cols[i], DOT.yW, DOT.tw, DOT.th, f1(v), 64));
    const opLine = el(root, `top:${DOT.yOp}px;left:${PANEL.x}px;width:${PANEL.w}px;text-align:center;font-size:72px;line-height:100px;` +
      `font-family:${MONO};font-weight:700;`);
    const opSp = ["y += ", "1.0", " × ", "0.5"].map((t) => { const s = document.createElement("span"); s.textContent = t; opLine.appendChild(s); return s; });
    const yRow = el(root, `top:${DOT.yY}px;left:${PANEL.x}px;width:${PANEL.w}px;text-align:center;line-height:110px;`);
    const ySp = document.createElement("span"); ySp.style.cssText = `font-size:72px;font-family:${MONO};font-weight:700;`; yRow.appendChild(ySp);
    const yN = document.createElement("span"); yN.style.fontSize = "84px"; yRow.appendChild(yN);
    const yL = document.createElement("span"); yL.style.fontSize = "60px"; yL.style.color = PAL.dim; yRow.appendChild(yL);
    const opEls = [...A, ...B, nRow], dotEls = [lx, lw, ...xs, ...ws, opLine, yRow];

    function counter(numEl, labEl, n, hero) {
      numEl.textContent = String(n); numEl.style.color = hero === "count" ? mag : data;
      labEl.textContent = n === 1 ? " FLOP" : " FLOPs";
    }
    function set(K, hero) {
      K = Object.assign({ o: 0, grow: 1, mode: "op", mul: 0, carry: 0, add: 0, n: 0, lit: null, step: 0 }, K || {});
      const g = clamp01(K.grow), o = K.o;
      growBox(box, o, g);
      const inner = o * seg(g, 0.7, 1);
      show(head, inner);
      const isOp = K.mode === "op";
      opEls.forEach((e) => show(e, 0)); dotEls.forEach((e) => show(e, 0));
      if (isOp) {
        const step = (row, u, lit, io) => {              // one operation: operands, sign, "=", the result sliding out of the sign
          [row[0], row[2]].forEach((t) => (t.style.borderColor = u > 0 && u < 1 ? data : PAL.ink));
          row[1].style.color = K.lit === lit ? data : ink;
          show(row[3], io * seg(u, 0.2, 0.5));
          row[4].style.left = `${lerp(OP.x[3], OP.x[4], seg(u, 0.4, 0.8))}px`;
          show(row[4], io * seg(u, 0.4, 0.8));
        };
        [A[0], A[1], A[2]].forEach((e) => show(e, inner));
        step(A, K.mul, "mul", inner);
        // the carry: row A's result slides down into row B's first slot; row B's rest fades in behind it
        const c = clamp01(K.carry);
        B[0].style.left = `${lerp(OP.x[4], OP.x[0], c)}px`; B[0].style.top = `${lerp(OP.yA, OP.yB, c)}px`;
        show(B[0], inner * (c > 0 ? 1 : 0));
        step(B, K.add, "add", inner);
        show(B[1], inner * seg(c, 0.5, 1)); show(B[2], inner * seg(c, 0.5, 1));
        counter(nNum, nLab, K.n, hero); show(nRow, inner);
      } else {
        const s = Math.max(0, Math.min(3, K.step)), i = Math.min(2, Math.floor(s)), f = s >= 3 ? 1 : s - i;
        const cum = [0, 0.5, 3.5, 4.5];
        const muls = Math.floor(s) + (s < 3 && f >= 0.25 ? 1 : 0), adds = Math.floor(s) + (s < 3 && f >= 0.5 ? 1 : 0);
        [lx, lw].forEach((e) => show(e, inner));
        DOT.x.forEach((_, k) => {
          const on = s < 3 && k === i && s > 0;
          [xs[k], ws[k]].forEach((t) => { t.style.borderColor = on ? data : PAL.ink; show(t, inner); });
        });
        // the running line: the pair being done, the × teal while multiplying, the + while adding
        opSp[1].textContent = f1(DOT.x[i]); opSp[3].textContent = f1(DOT.w[i]);
        const lineC = hero === "expr" ? mag : ink;
        opSp[0].style.color = s > 0 && f >= 0.5 ? data : lineC; opSp[2].style.color = s > 0 && f >= 0.25 && f < 0.5 ? data : lineC;
        opSp[1].style.color = lineC; opSp[3].style.color = lineC;
        show(opLine, inner * (s > 0 && s < 3 ? 1 : 0));
        ySp.textContent = `y = ${f1(cum[adds])}`; ySp.style.color = ink;
        counter(yN, yL, muls + adds, hero); yN.textContent = "    " + (muls + adds);
        show(yRow, inner);
      }
    }
    return { set, box };
  }

  // ---- "FLOP" unpacking into FLOATING-POINT / OPERATION ----
  const ACRO = { rows: ["FLOATING-POINT", "OPERATION"], keep: [[0, 0], [0, 1], [1, 0], [1, 1]], size: 72, big: 120, pitch: 0.62 };
  function makeAcro(root) {
    const cx = CARD.x + CARD.w / 2;
    const end = [], letters = [];
    ACRO.rows.forEach((row, r) => [...row].forEach((ch, i) => {
      const p = ACRO.size * ACRO.pitch;
      end.push({ ch, r, i, x: cx - (row.length * p) / 2 + i * p, y: CARD.y + 15 + r * 80, p });
    }));
    end.forEach((E) => {
      const d = el(root, `text-align:center;font-family:${MONO};font-weight:700;`, E.ch);
      const k = ACRO.keep.findIndex(([r, i]) => r === E.r && i === E.i);
      letters.push({ d, E, k });
    });
    const order = letters.filter((L) => L.k < 0);
    function set(K, hero) {
      K = Object.assign({ o: 0, u: 0 }, K || {});
      const u = clamp01(K.u), mv = SC.clamp01(seg(u, 0, 0.6)), m = mv * mv * (3 - 2 * mv);
      const bp = ACRO.big * ACRO.pitch;
      letters.forEach((L) => {
        const { d, E, k } = L;
        let x = E.x, y = E.y, size = ACRO.size, lh = 80, o = K.o;
        if (k >= 0) {                                      // F L O P: from the big centred word to their places
          const sx = CARD.x + CARD.w / 2 - 2 * bp + k * bp, sy = CARD.y + (CARD.h - 140) / 2;
          x = lerp(sx, E.x, m); y = lerp(sy, E.y, m); size = lerp(ACRO.big, ACRO.size, m); lh = lerp(140, 80, m);
          d.style.color = hero === "acronym" ? mag : ink;
        } else {                                           // the rest types in, left to right, row by row
          const j = order.indexOf(L) / order.length;
          o *= seg(u, 0.45 + 0.45 * j, 0.5 + 0.45 * j);
          d.style.color = ink;
        }
        const w = size * ACRO.pitch;
        Object.assign(d.style, { left: `${x}px`, top: `${y}px`, width: `${w}px`, fontSize: `${size}px`, lineHeight: `${lh}px` });
        show(d, o);
      });
    }
    return { set };
  }

  // ---- numbers streaming from GPU memory into the chip ----
  function makeStream(svg) {
    const x0 = SC.G.side.x + 10, x1 = SC.G.chip.x + SC.G.chip.size - 110, span = x0 - x1, speed = 260, gap = 0.6;
    const dots = [];
    [0, 1, 2].forEach((p) => [0, 1, 2].forEach((q) => dots.push({ p, q, r: SC.node("rect", { width: 30, height: 30, rx: 6, fill: PAL.data, stroke: PAL.bg, "stroke-width": 4, y: 696 + p * 40 }, svg) })));
    function set(K) {
      K = Object.assign({ o: 0, phase: 0 }, K || {});
      dots.forEach(({ p, q, r }) => {
        const t = K.phase - q * gap - p * 0.2;
        const d = t < 0 ? -1 : (t * speed) % (3 * gap * speed);
        const on = d >= 0 && d <= span;
        const x = x0 - d - 15;
        r.setAttribute("x", x);
        const fade = on ? Math.min(1, d / 30, (span - d) / 50) : 0;
        r.setAttribute("opacity", K.o * Math.max(0, fade));
      });
    }
    return { set };
  }

  // ---- the 1 s clock on the rate card ----
  function makeClock(root) {
    const R = 75, cx = 860, cy = CARD.y + CARD.h / 2;
    const ring = el(root, `left:${cx - R}px;top:${cy - R}px;width:${2 * R}px;height:${2 * R}px;border-radius:50%;`);
    const hole = el(root, `left:${cx - R + 16}px;top:${cy - R + 16}px;width:${2 * R - 32}px;height:${2 * R - 32}px;border-radius:50%;` +
      `background:${PAL.panel};text-align:center;font-size:60px;line-height:${2 * R - 32}px;`, "1 s");
    function set(sweep, o, hero) {
      const col = hero === "clock" ? mag : data, deg = 360 * clamp01(sweep);
      ring.style.background = `conic-gradient(${col} 0deg ${deg}deg, ${PAL.off} ${deg}deg 360deg)`;
      show(ring, o); show(hole, o);
    }
    return { set };
  }

  function mount(root) {
    const k = SC.mount(root);
    const cardBg = el(root, `left:${CARD.x}px;top:${CARD.y}px;width:${CARD.w}px;height:${CARD.h}px;` +
      `background:${PAL.panel};border-radius:28px;`);
    const A = makeLayer(root), B = makeLayer(root);
    const float = makeFloat(root);
    const core = makeCore(root), acro = makeAcro(root), stream = makeStream(k.svg), clock = makeClock(root);
    function draw(S) {
      // GPU memory sits under the grown panel: drawn off so its labels aren't
      // "occluded" text. S itself (what hf_state_check records) is unchanged.
      const F = S.float || {}, K = S.core || {};
      const full = (P) => P.o > 0 && (P.grow == null ? 1 : P.grow) >= 0.999;
      const covered = full(F) || full(K);
      k.draw(covered ? Object.assign({}, S, { hbm: 0 }) : S, S);
      const C = Object.assign({ o: 0, A: null, B: null, mix: 0 }, S.card || {});
      const top = C.y == null ? CARD.y : C.y;          // C.y: only 00_layout's take B moves the card
      show(cardBg, C.o); cardBg.style.top = `${top}px`;
      A.set(C.A, S.hero, C.o * (1 - C.mix), top);
      B.set(C.B, S.hero, C.o * C.mix, top);
      float.set(S.float, S.hero);
      core.set(S.core, S.hero);
      acro.set(S.acro, S.hero);
      stream.set(S.stream);
      const ck = (L, w) => (L && L.kind === "rate" ? w * (L.clockO || 0) : 0);
      const cko = C.o * (ck(C.A, 1 - C.mix) + ck(C.B, C.mix));
      const cks = C.B && C.B.kind === "rate" && C.mix > 0.5 ? C.B.clock : (C.A && C.A.kind === "rate" ? C.A.clock : 0);
      clock.set(cks || 0, cko, S.hero);
    }
    return Object.assign({}, k, { draw, float, core, cardBg });
  }

  window.EP = { mount, CARD, PANEL, CELL, NUMS, OP, DOT };
})();
