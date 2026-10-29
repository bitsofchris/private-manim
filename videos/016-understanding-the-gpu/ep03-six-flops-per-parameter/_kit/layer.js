// layer.js — ep 3's tiny layer (3 inputs, 2 outputs, 6 weights), its matrix W, the FLOP bar
// and readout, on top of the series chip. Linked into a beat as `ep/` (ln -s ../_kit NN_beat/ep),
// loaded after kit/code.js and ep/ep.js, before ep/seam.js.
//
// It wraps SC.mount: SC.mount(root) mounts the chip and the layer and returns
// { draw(S), chip, parts }. One state S per frame: the chip's fields (../_kit/chip.js header)
// plus S.ly for this file. One S.hero for both, so there is one magenta hero:
//   chip's names (cpu, queue, chip, ...) or this file's:
//   readout   the readout text           lines    the six weight lines
//   matrix    the 2 × 3 matrix cells      fwd / back / grad   that pass: its lines, its bar
//                                                      segment (and for grad the dW cells)
//
// S.ly fields (SC.REST.ly is the rest state):
//   o 0..1          the layer, matrix and formula (one group)
//   shrink 0..1     the group shrinks into one core cell of the chip (L.cell) and fades at the end
//   run 0|1         a value pulse runs forward along every line (reads SC.clock; frame 0 "working")
//   inLab "x"|"dx"  input labels;  outLab "y"|"dy"  output labels
//   pass null|"fwd"|"back"|"grad", prog 0..6   a pass over the lines in order w11 w12 w13 w21 w22 w23;
//                   line k is done when prog ≥ k + 1; the one in progress carries a dot and a
//                   rider glyph, × for its first half, + for its second (fwd: in → out; back:
//                   out → in; grad: at the line's middle, and the cell fills)
//   flash -1|k      line k and its cell drawn as the hero (beat 02's "six weights")
//   bumpIn, bumpOut 0..1   the input / output dots swell (a pulse; 0 at rest)
//   mat {o, name "W"|"dW", fill 0..6}   the matrix; dW cells fill one by one (fill), W cells are full
//   eq {o, text}    the formula left of the matrix (EP.eq.*)
//   bar {o, f [a, b, c], split 0..1}   the FLOP bar: three segments (forward, back to the input,
//                   back to the weights), each 0..1 full; split 0 labels them → 2 | ← 4, 1 → 2 | ← 2 | ← 2
//   rd {o, text}    the readout above the bar
//   bump 0..2 + barBump [0..1 ×3]   (optional) segment pulses for the hook
//
// The checker hook: tools/hf_state_check.js wraps the chip's mount and records the second
// argument of its draw; this file calls chip.draw(chipState, S) so the full S is what it records.
(function () {
  const SC = window.SC, EP = window.EP, PAL = SC.PAL;
  const { node, label, show, clamp01, lerp } = SC;
  const L = {
    inX: 230, outX: 780, inY: [600, 800, 1000], outY: [700, 900], r: 40,
    rdY: 244, barY: 362, barH: 50, labY: 428, x0: 65, x1: 950, gap: 16,
    mat: { x: 752, y: 1110, cell: 56, pitch: 66 }, eqY: 1135,
    centre: { x: 500, y: 860 },
  };
  L.segW = (L.x1 - L.x0 - 2 * L.gap) / 3;
  // w11 w12 w13 w21 w22 w23: line k joins input i to output j, cell (row j, column i) of W.
  const LINES = [];
  for (let j = 0; j < 2; j++) for (let i = 0; i < 3; i++) LINES.push({ i, j });
  // The core cell the layer shrinks into: the lowest-ranked (lit at rest) cell near the chip's middle.
  L.cell = (() => {
    let best = -1;
    for (let r = 4; r < 8; r++) for (let k = 4; k < 8; k++) {
      const c = r * SC.N + k; if (best < 0 || SC.RANK[c] < SC.RANK[best]) best = c;
    }
    const r = Math.floor(best / SC.N), k = best % SC.N, g = SC.G.chip;
    return { index: best, x: g.x + g.pad + k * g.pitch + g.cell / 2, y: g.y + g.pad + r * g.pitch + g.cell / 2 };
  })();

  const LREST = { o: 0, shrink: 0, run: 0, inLab: EP.inName, outLab: EP.outName, pass: null, prog: 0, flash: -1,
                  bumpIn: 0, bumpOut: 0, mat: { o: 0, name: "W", fill: 0 }, eq: { o: 0, text: "" },
                  bar: { o: 0, f: [0, 0, 0], split: 0 }, rd: { o: 0, text: "" }, barBump: [0, 0, 0] };
  const frac = (u) => u - Math.floor(u);

  function mountLayer(root) {
    // the shrinking group: one full-frame div holding the layer's SVG and its DOM labels
    const grp = document.createElement("div");
    grp.style.cssText = "position:absolute;left:0;top:0;width:1080px;height:1920px;";
    grp.style.transformOrigin = `${L.centre.x}px ${L.centre.y}px`;
    root.appendChild(grp);
    const svg = node("svg", { width: 1080, height: 1920, viewBox: "0 0 1080 1920" });
    svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    svg.setAttribute("data-layout-allow-overflow", "");
    grp.appendChild(svg);
    const lines = LINES.map(({ i, j }) => node("line", { x1: L.inX, y1: L.inY[i], x2: L.outX, y2: L.outY[j],
      stroke: PAL.data, "stroke-width": 8, "stroke-linecap": "round" }, svg));
    const runDots = LINES.map(() => node("circle", { r: 11, fill: PAL.ink }, svg));
    const dot = node("circle", { r: 16, fill: PAL.ink }, svg);
    const dotsIn = L.inY.map((y) => node("circle", { cx: L.inX, cy: y, r: L.r, fill: PAL.panel, stroke: PAL.data, "stroke-width": 8 }, svg));
    const dotsOut = L.outY.map((y) => node("circle", { cx: L.outX, cy: y, r: L.r, fill: PAL.panel, stroke: PAL.data, "stroke-width": 8 }, svg));
    const labIn = L.inY.map((y) => label(grp, "", { left: 65, top: y - 35, width: L.inX - L.r - 14 - 65, align: "right" }));
    const labOut = L.outY.map((y) => label(grp, "", { left: L.outX + L.r + 14, top: y - 35, width: 950 - L.outX - L.r - 14, align: "left" }));
    const rider = label(grp, "", { size: 60, width: 60, color: PAL.ink });
    const m = L.mat;
    const cells = LINES.map(({ i, j }) => node("rect", { x: m.x + i * m.pitch, y: m.y + j * m.pitch, width: m.cell, height: m.cell, rx: 8,
      fill: PAL.data, stroke: PAL.data, "stroke-width": 4 }, svg));
    const eq = label(grp, "", { left: 65, top: L.eqY, width: m.x - 40 - 65, align: "left" });

    // the top: readout and bar (not part of the shrinking group)
    const top = document.createElement("div");
    top.style.cssText = "position:absolute;left:0;top:0;width:1080px;height:1920px;";
    root.appendChild(top);
    const tsvg = node("svg", { width: 1080, height: 1920, viewBox: "0 0 1080 1920" });
    tsvg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    tsvg.setAttribute("data-layout-allow-overflow", "");
    top.appendChild(tsvg);
    const rd = label(top, "", { left: L.x0, top: L.rdY, size: 72, width: L.x1 - L.x0 });
    const barG = node("g", {}, tsvg);
    const segX = (s) => L.x0 + s * (L.segW + L.gap);
    const segs = [0, 1, 2].map((s) => {
      const g = node("g", {}, barG);
      const box = node("rect", { x: segX(s), y: L.barY, width: L.segW, height: L.barH, rx: 10, fill: PAL.bg, stroke: PAL.muted, "stroke-width": 4 }, g);
      const fill = node("rect", { x: segX(s), y: L.barY, width: 0, height: L.barH, rx: 10, fill: PAL.data }, g);
      return { g, box, fill, cx: segX(s) + L.segW / 2 };
    });
    const segLab = (text, cx, w) => label(top, text, { left: cx - w / 2, top: L.labY, size: 60, width: w, color: PAL.dim });
    const labF = segLab(EP.bar.fwd, segs[0].cx, L.segW);
    const lab4 = segLab(EP.bar.back4, (segs[1].cx + segs[2].cx) / 2, L.segW * 2);
    const lab2 = [segLab(EP.bar.back2, segs[1].cx, L.segW), segLab(EP.bar.back2, segs[2].cx, L.segW)];

    function draw(Y, hero) {
      Y = Object.assign({}, LREST, Y || {});
      const mat = Object.assign({}, LREST.mat, Y.mat), bar = Object.assign({}, LREST.bar, Y.bar);
      const eqS = Object.assign({}, LREST.eq, Y.eq), rdS = Object.assign({}, LREST.rd, Y.rd);
      const clock = SC.clock || 0;

      // the group: shrink into the core cell, fading over the last 40 %
      const e = Y.shrink * Y.shrink * (3 - 2 * Y.shrink);
      const s = lerp(1, SC.G.chip.cell / 520, e);
      const tx = lerp(0, L.cell.x - L.centre.x, e), ty = lerp(0, L.cell.y - L.centre.y, e);
      grp.style.transform = `translate(${tx.toFixed(2)}px, ${ty.toFixed(2)}px) scale(${s.toFixed(4)})`;
      show(grp, Y.o * (1 - clamp01((Y.shrink - 0.6) / 0.4)));

      // the pass
      const passCol = Y.pass && hero === Y.pass ? PAL.hero : PAL.data;
      const k = Math.floor(Y.prog), u = Y.prog - k, active = Y.pass && k < 6 && u > 0;
      lines.forEach((ln, i) => {
        let c = PAL.data, w = 8;
        if (Y.pass) c = i < k || (i === k && active) || Y.prog >= 6 ? passCol : PAL.muted;
        if (hero === "lines") c = PAL.hero;
        if (Y.flash === i) { c = PAL.hero; w = 14; } else if (Y.flash >= 0 && hero === "lines") c = PAL.data;
        ln.setAttribute("stroke", c); ln.setAttribute("stroke-width", w);
      });
      // the dot and its rider
      if (active) {
        const { i, j } = LINES[k];
        const from = Y.pass === "back" ? [L.outX, L.outY[j]] : [L.inX, L.inY[i]];
        const to = Y.pass === "back" ? [L.inX, L.inY[i]] : [L.outX, L.outY[j]];
        const v = Y.pass === "grad" ? 0.5 : u;
        const x = lerp(from[0], to[0], v), y = lerp(from[1], to[1], v);
        dot.setAttribute("cx", x.toFixed(1)); dot.setAttribute("cy", y.toFixed(1));
        dot.setAttribute("fill", passCol === PAL.hero ? PAL.hero : PAL.ink);
        rider.textContent = u < 0.5 ? EP.times : EP.plus;
        rider.style.left = `${(x - 30).toFixed(1)}px`; rider.style.top = `${(y - 112).toFixed(1)}px`;
        rider.style.color = passCol === PAL.hero ? PAL.hero : PAL.ink;
      }
      show(dot, active ? 1 : 0); show(rider, active ? 1 : 0);
      runDots.forEach((d, i) => {
        const { i: a, j: b } = LINES[i], v = frac(clock * 0.7 + i / 6);
        d.setAttribute("cx", lerp(L.inX, L.outX, v).toFixed(1)); d.setAttribute("cy", lerp(L.inY[a], L.outY[b], v).toFixed(1));
        show(d, Y.run ? Math.sin(Math.PI * v) : 0);
      });

      // dots and labels
      const bi = 1 + 0.3 * Y.bumpIn, bo = 1 + 0.3 * Y.bumpOut;
      dotsIn.forEach((d) => d.setAttribute("r", (L.r * bi).toFixed(1)));
      dotsOut.forEach((d) => d.setAttribute("r", (L.r * bo).toFixed(1)));
      labIn.forEach((el, i) => (el.textContent = `${Y.inLab}${i + 1}`));
      labOut.forEach((el, j) => (el.textContent = `${Y.outLab}${j + 1}`));

      // the matrix: W full; dW fills cell by cell
      cells.forEach((c, i) => {
        let a = mat.name === "W" ? 1 : clamp01(mat.fill - i);
        const isHero = hero === "matrix" || (hero === "grad" && mat.name !== "W") || (hero === "lines" && Y.flash === i);
        const col = isHero ? PAL.hero : PAL.data;
        c.setAttribute("stroke", a > 0 ? col : PAL.muted);
        c.setAttribute("fill", a > 0 ? col : PAL.off);
        c.setAttribute("fill-opacity", (a > 0 ? 0.25 + 0.75 * a : 1).toFixed(3));
        show(c, mat.o);
      });
      eq.textContent = eqS.text; show(eq, eqS.o);

      // readout and bar
      rd.textContent = rdS.text; show(rd, rdS.o);
      rd.style.color = hero === "readout" ? PAL.hero : PAL.ink;
      show(barG, bar.o);
      const segHero = [hero === "fwd", hero === "back", hero === "grad"];
      segs.forEach((sg, i) => {
        const f = clamp01(bar.f[i]), b = (Y.barBump && Y.barBump[i]) || 0;
        sg.fill.setAttribute("width", (L.segW * f).toFixed(1));
        sg.fill.setAttribute("fill", segHero[i] ? PAL.hero : PAL.data);
        sg.g.setAttribute("transform", b ? `translate(${sg.cx} ${L.barY + L.barH / 2}) scale(${1 + 0.12 * b}) translate(${-sg.cx} ${-(L.barY + L.barH / 2)})` : "");
      });
      show(labF, bar.o); show(lab4, bar.o * (1 - bar.split)); lab2.forEach((l) => show(l, bar.o * bar.split));
    }
    return { draw, grp, top, lines, dot, runDots, dotsIn, dotsOut, labIn, labOut, rider, cells, eq, rd, segs, labF, lab4, lab2 };
  }

  // Wrap the chip's mount: one draw for the chip and the layer.
  const chipMount = SC.mount;
  SC.mount = function (root) {
    const chip = chipMount(root);
    const ly = mountLayer(root);
    function draw(a, b) {
      const S = b !== undefined ? b : a;
      const C = Object.assign({}, S); delete C.ly;
      chip.draw(C, S);              // see the header: the checker records the second argument
      ly.draw(S.ly, S.hero);
    }
    return { draw, chip, parts: ly, code: chip.code, cells: chip.cells };
  };
  // REST for both, as the checker merges it: chip.js's REST plus this file's under ly.
  SC.REST = Object.assign({}, SC.REST, { ly: LREST });
  SC.LAYER = { L, LINES, LREST };
})();
