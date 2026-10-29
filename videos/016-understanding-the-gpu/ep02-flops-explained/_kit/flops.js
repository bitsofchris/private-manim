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
//
// Card content {kind, ...} (every string is ep 2's ledger, storyboard.md):
//   op      `a × b + c` and a counter:  n (0|1|2), lit ("mul"|"add"|null: that sign teal)
//   name    "floating-point" / "operation", the fl and op letters magenta on hero "acronym"
//   word    one word: word ("weights" | "activations" | "gradients")
//   count   "FLOPs" (its s magenta on hero "s") / "720 trillion" at o2
//   rate    step 0: "FLOPS" (its S magenta on hero "S") / "per second"
//           step 1: "2,250 TFLOPS" (magenta on hero "spec") / "bf16"
//           step 2: "2,250 TFLOPS" (its T magenta on hero "tera") / "tera = a trillion"
//   matmul  step 0: `y = x @ W`; step 1 adds `x1*w1 + x2*w2 + x3*w3` (magenta on hero "expr")
//   frac    "FLOPs ÷ FLOPS" / "= GPU-hours" (hero "hours") and " = $" at dollar (hero "bill")
//
// Hero names of ep 2's parts (S.hero, one at a time; the chip's own names still work):
//   count, acronym, sign, digits, exp, point, s, S, spec, tera, expr, hours, bill
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
      case "op": return [[
        { t: "a ", mono: 1, size: 76 }, { t: "×", mono: 1, size: 76, c: K.lit === "mul" ? data : ink },
        { t: " b ", mono: 1, size: 76 }, { t: "+", mono: 1, size: 76, c: K.lit === "add" ? data : ink },
        { t: " c", mono: 1, size: 76 }, { t: "    " + (K.n || 0), size: 96, c: h(hero, "count", data) },
        { t: " FLOPs", size: 60, c: dim }]];
      case "name": return [
        [{ t: "fl", size: 72, c: h(hero, "acronym", ink) }, { t: "oating-point", size: 72 }],
        [{ t: "op", size: 72, c: h(hero, "acronym", ink) }, { t: "eration", size: 72 }]];
      case "word": return [[{ t: K.word, size: 84 }]];
      case "count": return [
        [{ t: "FLOP", size: 96 }, { t: "s", size: 96, c: h(hero, "s", ink) }],
        [{ t: "720 trillion", size: 64, c: data, o: K.o2 == null ? 0 : K.o2 }]];
      case "rate": {
        if (!K.step) return [[{ t: "FLOP", size: 96 }, { t: "S", size: 96, c: h(hero, "S", ink) }],
                             [{ t: "per second", size: 64, c: dim }]];
        const spec = h(hero, "spec", ink);
        return [[{ t: "2,250 ", size: 96, c: spec }, { t: "T", size: 96, c: h(hero, "tera", spec) }, { t: "FLOPS", size: 96, c: spec }],
                [{ t: K.step === 1 ? "bf16" : "tera = a trillion", size: 64, c: dim }]];
      }
      case "matmul": return [
        [{ t: "y = x @ W", mono: 1, size: 72 }],
        [{ t: "x1*w1 + x2*w2 + x3*w3", mono: 1, size: 60, c: h(hero, "expr", data), o: K.step ? 1 : 0 }]];
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
      show(panel, o * (g > 0 ? 1 : 0));
      const x = lerp(CELL.x, PANEL.x, g), y = lerp(CELL.y, PANEL.y, g);
      const w = lerp(CELL.s, PANEL.w, g), hh = lerp(CELL.s, PANEL.h, g);
      Object.assign(panel.style, { left: `${x}px`, top: `${y}px`, width: `${w}px`, height: `${hh}px`,
                                   borderWidth: `${lerp(2, 6, g)}px`, borderRadius: `${lerp(6, 28, g)}px` });
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

  function mount(root) {
    const k = SC.mount(root);
    const cardBg = el(root, `left:${CARD.x}px;top:${CARD.y}px;width:${CARD.w}px;height:${CARD.h}px;` +
      `background:${PAL.panel};border-radius:28px;`);
    const A = makeLayer(root), B = makeLayer(root);
    const float = makeFloat(root);
    function draw(S) {
      // GPU memory sits under the grown panel: drawn off so its labels aren't
      // "occluded" text. S itself (what hf_state_check records) is unchanged.
      const F = S.float || {};
      const covered = F.o > 0 && (F.grow == null ? 1 : F.grow) >= 0.999;
      k.draw(covered ? Object.assign({}, S, { hbm: 0 }) : S, S);
      const C = Object.assign({ o: 0, A: null, B: null, mix: 0 }, S.card || {});
      const top = C.y == null ? CARD.y : C.y;          // C.y: only 00_layout's take B moves the card
      show(cardBg, C.o); cardBg.style.top = `${top}px`;
      A.set(C.A, S.hero, C.o * (1 - C.mix), top);
      B.set(C.B, S.hero, C.o * C.mix, top);
      float.set(S.float, S.hero);
    }
    return Object.assign({}, k, { draw, float, cardBg });
  }

  window.EP = { mount, CARD, PANEL, CELL, NUMS };
})();
