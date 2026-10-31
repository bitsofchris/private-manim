// ep.js — ep 4's own parts on the series chip (../../_kit/chip.js). Linked into
// a beat as `ep/` (ln -s ../_kit NN_beat/ep), loaded after kit/code.js and
// before ep/seam.js. Beats call EP.mount(root) instead of SC.mount(root): it
// mounts the series chip in its own layer (so the episode can fade it or lift
// it) and adds, around it,
//
//   bit rows   fp32 / fp16 / bf16 / fp8, one box per bit, to scale (ledger:
//              1|8|23, 1|5|10, 1|8|7, 1|4|3). Fields: sign --muted, exponent
//              teal, mantissa --dim. Two layouts, lerped by `view`:
//                view 0 (chip view)  four small rows, y 240–436
//                view 1 (bits view)  big rows over the whole stage, y 240–1042:
//                                    label above each row, field counts under
//                                    it ("8 exponent · 23 mantissa")
//              `close` lifts bf16 into the first small slot (the end frame).
//   split      each core cell divided into 1, 2 or 4 numbers (0, 1, 2).
//   ladder     the dense peak ladder in the bottom slot, chip view only:
//              TF32 1,125 / bf16 2,250 / fp8 4,500 TFLOPS, bars to scale.
//   values     bits view: what two real numbers become in each format, on each
//              row's label line. 1/3 (precision): 0.33333334 / 0.33325195 /
//              0.33398438 / 0.34375, the digits still right in teal. 70,000
//              (range): 70,000 / inf / 70,144 / "max 448". Computed (round to
//              nearest even); see storyboard "Facts".
//   scale tag  bits view: "× scale" clipped onto the fp8 row, "Transformer
//              Engine" under it.
//
// Ep 4 fields of S (defaults merged into SC.REST, so tools/hf_state_check.js sees them):
//   view 0..1        chip view → bits view (the chip layer fades out as rows grow)
//   close 0..1       the end layout: chip layer lifted 120 px, bf16 in the top slot
//   o32 o16 ob16 o8  each row's opacity
//   split 0..2       numbers per cell: 0 = 1, 1 = 2, 2 = 4 (dividers fade in)
//   ladder 0..1      the ladder's opacity; rungs 0..3 how many bars have grown
//   colA 0..1        the 1/3 column (header and all four cells)
//   big 0..1         the 70,000 column's header and fp32's cell
//   inf 0..1         fp16's 70,000 cell, "inf"
//   bigb 0..1        bf16's 70,000 cell, "70,144"
//   big8 0..1        fp8's 70,000 cell, "max 448"
//   same 0..1        outlines on fp32's and bf16's exponent fields
//   scale 0..1       the fp8 scale tag
// Hero names added (the chip's own still work: tc, pipe, chip, ...):
//   "row:F"  a whole bit row      "exp:F"  its exponent field (+ fp32's when `same`, + its 70,000 cell)
//   "man:F"  its mantissa field (+ its 1/3 cell)                 "inf"  fp16's 70,000 cell
//   "rung:F" a ladder rung (+ row F's label)
//   "scale"  the fp8 scale tag    "code"   nothing here: the code card's own `lit` line is the hero
(function () {
  const SC = window.SC, { PAL, lerp, node, label, show, clamp01 } = SC;

  Object.assign(SC.REST, {
    cpu: 0, queueO: 0, strip: 0,                  // the series CPU, queue and time strip: not in ep 4
    view: 0, close: 0, o32: 1, o16: 1, ob16: 1, o8: 1, split: 0,
    ladder: 0, rungs: 0, colA: 0, big: 0, inf: 0, bigb: 0, big8: 0, same: 0, scale: 0,
  });

  const FMT = {                                   // ledger bit layouts: sign | exponent | mantissa
    // small/big: the boxes' top in each view. a/b: the 1/3 and 70,000 cells as [right digits, the rest].
    fp32: { f: [1, 8, 23], o: "o32", small: 240, big: 360, a: ["0.3333333", "4"], b: ["70,000", ""], ob: "big" },
    fp16: { f: [1, 5, 10], o: "o16", small: 292, big: 550, a: ["0.333", "25195"], b: ["", "inf"], ob: "inf" },
    bf16: { f: [1, 8, 7], o: "ob16", small: 344, big: 740, a: ["0.33", "398438"], b: ["70,", "144"], ob: "bigb" },
    fp8: { f: [1, 4, 3], o: "o8", small: 396, big: 930, a: ["0.3", "4375"], b: ["", "max 448"], ob: "big8" },
  };
  const NAMES = Object.keys(FMT);
  const SMALL = { x0: 215, pitch: 23, w: 19, h: 40, lab: 44 };
  const BIG = { x0: 65, pitch: 27.5, w: 23, h: 56, lab: 48, spec: 40, val: 44 };
  const COL = { a: 440, b: 760, head: 240 };     // value columns (bits view): x of each, header top
  const CLOSE_Y = 250;                            // bf16's small slot in the end frame
  const LIFT = 120;                               // the chip layer's lift in the end frame
  const FIELD = [PAL.muted, PAL.data, PAL.dim];   // sign, exponent, mantissa
  const FIELD_NAME = ["", "exponent", "mantissa"];
  // Ladder (chip view, bottom slot): bars to scale, 4,500 = 400 px.
  const LAD = { x: 210, max: 400, top: 1170, pitch: 55, h: 40,
                rungs: [["TF32", 1125, "1,125"], ["bf16", 2250, "2,250"], ["fp8", 4500, "4,500"]] };

  function mount(root) {
    // the chip in its own layer: faded by `view`, lifted by `close`
    const layer = document.createElement("div");
    layer.style.cssText = "position:absolute;left:0;top:0;width:1080px;height:1920px;";
    layer.setAttribute("data-layout-allow-overflow", "");
    root.appendChild(layer);
    const kit = SC.mount(layer);
    const over = node("svg", { width: SC.W, height: SC.H, viewBox: `0 0 ${SC.W} ${SC.H}` });
    over.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    over.setAttribute("data-layout-allow-overflow", "");
    layer.insertBefore(over, kit.code ? kit.code.card : null);
    // dividers: one middle line and two quarter lines per cell, in the chip's panel colour
    const half = node("g", {}, over), quarter = node("g", {}, over);
    kit.cells.forEach((cl) => {
      const v = (g, dx) => node("rect", { x: cl.x + dx - 1.5, y: cl.y, width: 3, height: SC.G.chip.cell, fill: PAL.panel }, g);
      v(half, 21); v(quarter, 10.5); v(quarter, 31.5);
    });

    const svg = node("svg", { width: SC.W, height: SC.H, viewBox: `0 0 ${SC.W} ${SC.H}` });
    svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    svg.setAttribute("data-layout-allow-overflow", "");
    root.appendChild(svg);

    // bit rows
    const rows = {};
    NAMES.forEach((name) => {
      const g = node("g", {}, svg);
      const [s, e, m] = FMT[name].f, n = s + e + m;
      const boxes = [...Array(n)].map((_, i) => node("rect", { rx: 4, fill: FIELD[i < s ? 0 : i < s + e ? 1 : 2] }, g));
      const field = (i) => (i < s ? 0 : i < s + e ? 1 : 2);
      const lab = label(root, name, { size: SMALL.lab });
      const spec = document.createElement("div");
      spec.style.cssText = `position:absolute;left:${BIG.x0}px;white-space:nowrap;` +
        `font-size:${BIG.spec}px;line-height:${Math.round(BIG.spec * 1.15)}px;`;
      const specE = document.createElement("span"), dot = document.createElement("span"), specM = document.createElement("span");
      specE.textContent = `${e} ${FIELD_NAME[1]}`; dot.textContent = " · "; specM.textContent = `${m} ${FIELD_NAME[2]}`;
      dot.style.color = PAL.dim;
      spec.appendChild(specE); spec.appendChild(dot); spec.appendChild(specM);
      root.appendChild(spec);
      const outline = node("rect", { rx: 8, fill: "none", "stroke-width": 5 }, svg);
      const cell = (x, [ok, rest]) => {             // monospace from the script (the CSS-class trap)
        const el = label(root, "", { left: x, size: BIG.val });
        const a = document.createElement("span"), b = document.createElement("span");
        a.textContent = ok; b.textContent = rest; el.appendChild(a); el.appendChild(b);
        [el, a, b].forEach((n) => { n.style.fontFamily = "monospace"; n.style.fontWeight = "700"; });
        return { el, ok: a, rest: b };
      };
      const ca = cell(COL.a, FMT[name].a), cb = cell(COL.b, FMT[name].b);
      rows[name] = { g, boxes, field, lab, spec, specE, specM, outline, n, s, e, ca, cb };
    });

    // ladder
    const ladG = node("g", {}, svg);
    const rungs = LAD.rungs.map(([name, v, text], i) => {
      const y = LAD.top + i * LAD.pitch;
      const bar = node("rect", { x: LAD.x, y, width: 0, height: LAD.h, rx: 8, fill: PAL.data }, ladG);
      const lab = label(root, name, { left: 65, top: y - 5, size: 44 });
      const num = label(root, `${text} TFLOPS`, { top: y - 2, size: 40 });
      return { bar, lab, num, w: (LAD.max * v) / 4500 };
    });

    // value column headers
    const headA = label(root, "1/3", { left: COL.a, top: COL.head, size: BIG.val, color: PAL.dim });
    const headB = label(root, "70,000", { left: COL.b, top: COL.head, size: BIG.val, color: PAL.dim });
    [headA, headB].forEach((n) => { n.style.fontFamily = "monospace"; n.style.fontWeight = "700"; });

    // fp8 scale tag
    const tagG = node("g", {}, svg);
    const fp8End = BIG.x0 + 7 * BIG.pitch + BIG.w;
    const tagBox = node("rect", { x: fp8End + 30, y: FMT.fp8.big - 2, width: 210, height: BIG.h + 4, rx: 30, fill: PAL.panel, "stroke-width": 5 }, tagG);
    const tagLab = label(root, "× scale", { left: fp8End + 30, top: FMT.fp8.big + 2, size: 44, width: 210 });
    const teLab = label(root, "Transformer Engine", { left: BIG.x0, top: FMT.fp8.big + BIG.h + 70, size: 44 });

    function drawRows(S) {
      const v = clamp01(S.view), c = clamp01(S.close), hero = S.hero || "";
      NAMES.forEach((name) => {
        const r = rows[name], o = clamp01(S[FMT[name].o]);
        const smallY = name === "bf16" ? lerp(FMT.bf16.small, CLOSE_Y, c) : FMT[name].small;
        const y = lerp(smallY, FMT[name].big, v), h = lerp(SMALL.h, BIG.h, v);
        const x0 = lerp(SMALL.x0, BIG.x0, v), p = lerp(SMALL.pitch, BIG.pitch, v), w = lerp(SMALL.w, BIG.w, v);
        const heroRow = hero === `row:${name}`, heroE = hero === `exp:${name}` || (hero === "exp:bf16" && name === "fp32" && S.same > 0.5);
        const heroM = hero === `man:${name}`, heroL = heroRow || hero === `rung:${name}`;
        show(r.g, o);
        r.boxes.forEach((b, i) => {
          b.setAttribute("x", (x0 + i * p).toFixed(1)); b.setAttribute("y", y.toFixed(1));
          b.setAttribute("width", w.toFixed(1)); b.setAttribute("height", h.toFixed(1));
          const f = r.field(i);
          b.setAttribute("fill", heroRow || (heroE && f === 1) || (heroM && f === 2) ? PAL.hero : FIELD[f]);
        });
        // label: left of the row (small) → above it (big)
        const ls = lerp(SMALL.lab, BIG.lab, v);
        r.lab.style.fontSize = `${ls.toFixed(1)}px`; r.lab.style.lineHeight = `${Math.round(ls * 1.15)}px`;
        r.lab.style.left = "65px";
        r.lab.style.top = `${lerp(y - 5, y - 60, v).toFixed(1)}px`;
        r.lab.style.color = heroL ? PAL.hero : PAL.ink;
        show(r.lab, o);
        r.spec.style.top = `${(y + BIG.h + 8).toFixed(1)}px`;
        show(r.spec, o * clamp01((v - 0.5) * 2));
        r.specE.style.color = heroE ? PAL.hero : PAL.data;
        r.specM.style.color = heroM ? PAL.hero : PAL.dim;
        // "same range": an outline round the exponent field
        const so = name === "fp32" || name === "bf16" ? clamp01(S.same) * o * v : 0;
        r.outline.setAttribute("x", (x0 + r.s * p - 7).toFixed(1)); r.outline.setAttribute("y", (y - 7).toFixed(1));
        r.outline.setAttribute("width", ((r.e - 1) * p + w + 14).toFixed(1)); r.outline.setAttribute("height", (h + 14).toFixed(1));
        r.outline.setAttribute("stroke", heroE ? PAL.hero : PAL.data);
        show(r.outline, so);
        // value cells, on the label line (bits view only)
        const top = `${(y - 60 + 2).toFixed(1)}px`;
        r.ca.el.style.top = r.cb.el.style.top = top;
        show(r.ca.el, o * v * clamp01(S.colA));
        show(r.cb.el, o * v * clamp01(S[FMT[name].ob]));
        const hotA = heroM, hotB = (name === "fp16" && hero === "inf") || heroE && name !== "fp32";
        r.ca.ok.style.color = hotA ? PAL.hero : PAL.data; r.ca.rest.style.color = hotA ? PAL.hero : PAL.dim;
        r.cb.ok.style.color = hotB ? PAL.hero : PAL.data;
        r.cb.rest.style.color = hotB ? PAL.hero : name === "fp16" ? PAL.ink : PAL.dim;
        if (name === "fp32") r.cb.ok.style.color = PAL.ink;
      });
      show(headA, v * clamp01(S.colA)); show(headB, v * clamp01(S.big));
    }

    function drawLadder(S) {
      const o = clamp01(S.ladder) * (1 - clamp01(S.view)), hero = S.hero || "";
      show(ladG, o);
      rungs.forEach((r, i) => {
        const u = clamp01(S.rungs - i), w = r.w * u, hot = hero === `rung:${LAD.rungs[i][0]}`;
        r.bar.setAttribute("width", w.toFixed(1));
        r.bar.setAttribute("fill", hot ? PAL.hero : PAL.data);
        r.lab.style.color = r.num.style.color = hot ? PAL.hero : PAL.ink;
        r.num.style.left = `${(LAD.x + w + 16).toFixed(1)}px`;
        show(r.lab, o * clamp01(u * 4)); show(r.num, o * clamp01((u - 0.6) * 2.5));
      });
    }

    function drawTag(S) {
      const o = clamp01(S.scale) * clamp01(S.view) * clamp01(S.o8), hot = S.hero === "scale";
      show(tagG, o); show(tagLab, o); show(teLab, o);
      tagBox.setAttribute("stroke", hot ? PAL.hero : PAL.data);
      tagLab.style.color = hot ? PAL.hero : PAL.ink;
    }

    function draw(S) {
      S = Object.assign({}, SC.REST, S);
      const v = clamp01(S.view), c = clamp01(S.close);
      // The chip ignores ep 4's hero names ("row:bf16", ...); it sees only its own.
      const chipS = Object.assign({}, S, { hero: S.hero && S.hero.indexOf(":") < 0 && S.hero !== "inf" &&
                                                  S.hero !== "scale" && S.hero !== "code" ? S.hero : null });
      // (S, S): tools/hf_state_check.js wraps SC.mount's draw as (g, S) and records the second argument.
      kit.draw(chipS, S);
      layer.style.opacity = (1 - v).toFixed(3);
      layer.style.visibility = v < 0.999 ? "visible" : "hidden";
      layer.style.transform = `translateY(${(-LIFT * c).toFixed(1)}px)`;
      show(half, clamp01(S.split)); show(quarter, clamp01(S.split - 1));
      drawRows(S); drawLadder(S); drawTag(S);
    }
    return Object.assign({}, kit, { draw, rows, rungs, layer, headA, headB, tagLab, teLab, FMT, BIG, SMALL, COL, LAD });
  }

  // A beat's state between two seam states: numbers lerp, the rest switch at u ≥ 0.5 (ep 1's mix).
  function mix(a, b, u) {
    const out = {};
    new Set([...Object.keys(a), ...Object.keys(b)]).forEach((k) => {
      const x = a[k] !== undefined ? a[k] : SC.REST[k], y = b[k] !== undefined ? b[k] : SC.REST[k];
      out[k] = typeof x === "number" && typeof y === "number" ? lerp(x, y, u) : u < 0.5 ? x : y;
    });
    return out;
  }

  window.EP = { mount, mix, FMT, SMALL, BIG, COL, LAD, LIFT };
})();
