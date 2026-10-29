// machine.js — the shared kit for the PyTorch Dataloading series (014): the
// machine every episode opens on. Linked into a beat as `kit/` after
// kit/data.js, before kit/code.js:
//   ln -s ../../_kit NN_beat/kit        (from the episode folder)
//
// One state object S -> one frame, drawn by SC.mount(root).draw(g, S) (g is
// unused: the machine is SVG plus DOM labels, so `hyperframes check` sees the
// geometry). A beat opens on SC.SEAM[n-1] and ends on SC.SEAM[n]; the episode's
// own kit/seam.js fills SC.SEAM. Pure functions of S: no clocks, no randomness.
// The sample flow (frame 0 "already running") is the one thing not in S: a
// beat sets SC.clock = master seconds before each draw, so the flow is
// continuous across cuts and tools/hf_state_check.js ignores it.
//
// Layout (px, 1080×1920; captions anchored bottom, so the code card can sit
// at y 1105–1330 and captions below it):
//   dataset card   y 250–400    x 190–825    "Dataset" + its methods
//   samples        y 400–500    hop from the dataset card into the loader box (SC.clock drives them)
//   loader box     y 500–970    x 65–950     dashed; "DataLoader"; four stations
//     stations     y 580+       x 95–920     sampler, fetch, batching, collate; 86 tall, 12 apart
//   batch row      y 1000–1090  the batch tensor (x 190–600) -> the model chip (x 700–920)
//                              a tensor is rows of numbers in brackets (data.js `readout`) with its shape beside it;
//                              a sample in flight is one row of it in brackets; the batching station stacks three rows ×32
//   code card      y 330–1010   kit/code.js, shown instead of the machine (S.flip)
//
// S fields (all optional; SC.REST is the rest state, ep 2's frame 0):
//   mode "map"|"iterable"      methods on the dataset card; "iterable" strikes the sampler
//   workers 0|1|2              photocopies of the dataset in the fetch station
//   hero NAME|null             the one magenta part: dataset, len, getitem, iter, sampler,
//                              fetch, batching, collate, batch, model, twins
//   strike 0..1                the sampler's strike-through (1 in SEAM states of ep 4–5)
//   twins 0..1                 a second, identical batch beside the first (ep 5); the True/False is on the code card
//   shape "[32, 512]"          the batch card's label (ep 5: "[4, 512]")
//   loader 0..1, batch 0..1, model 0..1, dataset 0..1   opacities
//   flip 0..1                  0 = the machine, 1 = the code card; never both (a 0.4 s crossfade)
//   code {o, lines, typed, lit, cursor, blink}   the code card (kit/code.js)
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const D = window.DL_DATA;
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const pulse = (t, at, w = 0.6) => { const u = (t - at) / w; return u < 0 || u > 1 ? 0 : Math.sin(Math.PI * u); };
  const PAL = { bg: "#0B0B14", panel: "#14142B", ink: "#ECEBE4", dim: "#8A8FB0",
                data: "#2DD4BF", hero: "#C084FC", muted: "#4A5070", grid: "#1F2440" };
  const W = 1080, H = 1920;
  const SAFE = { x0: 65, x1: 950, y0: 230, y1: 1536, stageBottom: 1100 };
  const MID = 507;
  const G = {
    dataset: { x: 190, y: 250, w: 635, h: 150 },
    loader: { x: 65, y: 500, w: 885, h: 470 },
    station: { x: 95, w: 825, h: 86, gap: 12, y0: 580 },
    batch: { x: 190, y: 1000, w: 410, h: 90 },
    model: { x: 700, y: 1000, w: 220, h: 90 },
  };
  const STATIONS = ["sampler", "fetch", "batching", "collate"];
  const stationY = (i) => G.station.y0 + i * (G.station.h + G.station.gap);

  // ---- helpers ----
  function node(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach((k) => el.setAttribute(k, attrs[k]));
    if (parent) parent.appendChild(el);
    return el;
  }
  const rect = (g, x, y, w, h, a) => node("rect", Object.assign({ x, y, width: w, height: h, rx: 22 }, a), g);
  const line = (g, x1, y1, x2, y2, a) => node("line", Object.assign({ x1, y1, x2, y2, "stroke-linecap": "round" }, a), g);
  const show = (el, a) => { el.style.opacity = a; el.style.visibility = a > 0.001 ? "visible" : "hidden"; };
  function label(root, text, o = {}) {
    const el = document.createElement("div");
    const size = o.size || 60;
    el.textContent = text;
    el.style.cssText = `position:absolute;left:${o.left || 0}px;top:${o.top || 0}px;font-size:${size}px;line-height:${Math.round(size * 1.15)}px;` +
      `white-space:nowrap;color:${o.color || PAL.ink};` + (o.width ? `width:${o.width}px;text-align:${o.align || "left"};` : "");
    if (o.mono) { el.style.fontFamily = "monospace"; el.style.fontWeight = "700"; }
    root.appendChild(el);
    return el;
  }
  function guides(root) {
    if (!/[?&]guides/.test(location.search)) return;
    [[0, 0, 1080, 230], [0, 1536, 1080, 384], [950, 230, 130, 1306], [0, 230, 65, 1306]].forEach(([l, t, w, h]) => {
      const d = document.createElement("div");
      d.style.cssText = `position:absolute;left:${l}px;top:${t}px;width:${w}px;height:${h}px;background:rgba(255,60,60,0.18);pointer-events:none;`;
      root.appendChild(d);
    });
  }
  function layer(root) {
    const svg = node("svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}` });
    svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    svg.setAttribute("data-layout-allow-overflow", "");
    root.appendChild(svg);
    return svg;
  }
  // A short time series: the ledger's sample, as a polyline of n points.
  function squiggle(g, x, y, w, h, k, a) {
    const n = 14, pts = [];
    for (let i = 0; i < n; i++) {
      const u = i / (n - 1);
      pts.push(`${(x + u * w).toFixed(1)},${(y + h / 2 - Math.sin(u * 6.28 * (1.5 + k)) * h * 0.42 - (u - 0.5) * h * 0.2).toFixed(1)}`);
    }
    return node("polyline", Object.assign({ points: pts.join(" "), fill: "none", stroke: PAL.data, "stroke-width": 5,
                                            "stroke-linecap": "round", "stroke-linejoin": "round" }, a), g);
  }
  // A tensor readout: `rows` of numbers (data.js `readout`) in one tall pair of brackets, each row ending in ⋯
  // (the style guide's matrix notation). DOM rows (the layout check sees the text) between two SVG bracket paths.
  // Returns { move(x) } so a card can slide (twins) and keep its digits; the rows join part p for hero tinting.
  function readout(root, g, p, x, y, h, rows, o = {}) {
    const size = o.size || 24, pitch = o.pitch || Math.round(size * 1.12), pad = Math.max(0, (h - rows.length * pitch) / 2);
    const cw = size * 0.6, text = rows.map((r) => r.join(" ") + " \u22EF");
    const w = Math.max(...text.map((t) => t.length)) * cw;
    const bl = node("path", { d: `M${x + 18},${y + 8} h-10 v${h - 16} h10`, fill: "none", stroke: PAL.dim, "stroke-width": 4, "stroke-linecap": "round" }, g);
    const br = node("path", { d: `M${x + 26 + w},${y + 8} h10 v${h - 16} h-10`, fill: "none", stroke: PAL.dim, "stroke-width": 4, "stroke-linecap": "round" }, g);
    p.svg.push(tintable(bl, PAL.dim)); p.svg.push(tintable(br, PAL.dim));
    const els = text.map((t, i) => domTint(p, label(root, t, { left: x + 26, top: y + pad + i * pitch, size, mono: true }), PAL.data));
    els.forEach((el) => { el.style.lineHeight = `${pitch}px`; });
    const end = x + 44 + w;   // where the readout ends (the shape label goes after it)
    return { els, end, move: (nx) => els.forEach((el) => { el.style.left = `${nx + 26}px`; }) };
  }
  // One sample as a vector: a row of numbers in brackets, SVG text so it can ride (centred on x = MID, y = 0).
  function sampleGlyph(g, row) {
    const gg = node("g", {}, g), size = 22, text = row.join(" ") + " \u22EF", w = text.length * size * 0.6;
    const t = node("text", { x: MID, y: 8, "text-anchor": "middle", "font-size": size, "font-weight": 700, "font-family": "monospace", fill: PAL.data }, gg);
    t.textContent = text;
    // brackets: the bar at x, the arms pointing in toward the digits
    [[-1, MID - w / 2 - 8], [1, MID + w / 2 + 8]].forEach(([s, x]) => node("path", { d: `M${x - 7 * s},-14 h${7 * s} v28 h${-7 * s}`, fill: "none", stroke: PAL.dim, "stroke-width": 3, "stroke-linecap": "round" }, gg));
    return gg;
  }
  // Hero tinting: every stroke/fill with data-tint goes magenta when its part is the hero.
  function tintable(el, col) { el.setAttribute("data-tint", col); return el; }
  function tint(part, on) {
    part.svg.forEach((el) => {
      const c = on ? PAL.hero : el.getAttribute("data-tint");
      if (el.getAttribute("stroke") && el.getAttribute("stroke") !== "none") el.setAttribute("stroke", c);
      if (el.getAttribute("data-fill")) el.setAttribute("fill", c);
    });
    part.dom.forEach((el) => { el.style.color = on ? PAL.hero : el.getAttribute("data-color"); });
  }
  const part = () => ({ svg: [], dom: [] });
  const domTint = (p, el, col) => { el.setAttribute("data-color", col); el.style.color = col; p.dom.push(el); return el; };

  // ---- mount ----
  function mount(root) {
    const svg = layer(root);
    const parts = {};
    STATIONS.concat(["dataset", "len", "getitem", "iter", "batch", "model", "twins"]).forEach((k) => (parts[k] = part()));

    // dataset card
    const ds = G.dataset;
    const dsG = node("g", {}, svg);
    parts.dataset.svg.push(tintable(rect(dsG, ds.x, ds.y, ds.w, ds.h, { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6 }), PAL.ink));
    const dsLabel = domTint(parts.dataset, label(root, "Dataset", { left: ds.x + 34, top: ds.y + 40, size: 60 }), PAL.ink);
    const mLen = domTint(parts.len, label(root, D.methods.map[0], { left: ds.x + 330, top: ds.y + 18, size: 44, mono: true }), PAL.data);
    const mGet = domTint(parts.getitem, label(root, D.methods.map[1], { left: ds.x + 330, top: ds.y + 78, size: 44, mono: true }), PAL.data);
    const mIter = domTint(parts.iter, label(root, D.methods.iterable[0], { left: ds.x + 330, top: ds.y + 48, size: 44, mono: true }), PAL.data);

    // samples in flight: dataset -> the loader box (three, phased by SC.clock). A sample is a [512]
    // tensor: one row of the readout in brackets (the style guide's vector), the row it becomes in the batch.
    const flow = [0, 1].map((k) => sampleGlyph(svg, D.series.readout[k]));

    // loader box
    const lo = G.loader;
    const loG = node("g", {}, svg);
    const loRect = rect(loG, lo.x, lo.y, lo.w, lo.h, { fill: "none", stroke: PAL.muted, "stroke-width": 5, "stroke-dasharray": "22 16", rx: 34 });
    const loLabel = label(root, "DataLoader", { left: lo.x + 30, top: lo.y + 14, size: 60 });

    // stations
    const st = {};
    STATIONS.forEach((name, i) => {
      const y = stationY(i), p = parts[name];
      const g = node("g", {}, svg);
      p.svg.push(tintable(rect(g, G.station.x, y, G.station.w, G.station.h, { fill: PAL.panel, stroke: PAL.muted, "stroke-width": 5 }), PAL.muted));
      const lab = domTint(p, label(root, name, { left: G.station.x + 30, top: y + 9, size: 60 }), PAL.ink);
      st[name] = { g, y, lab, glyph: node("g", {}, g) };
    });
    // sampler glyph: shuffled indices; and its strike line
    const idx = domTint(parts.sampler, label(root, D.indices.join(" "), { left: 560, top: st.sampler.y + 16, size: 48, mono: true }), PAL.data);
    const strike = line(svg, G.station.x + 20, st.sampler.y + G.station.h / 2, G.station.x + 20, st.sampler.y + G.station.h / 2,
                        { stroke: PAL.dim, "stroke-width": 8 });
    // fetch glyph: worker photocopies of the dataset card
    const workers = [0, 1].map((k) => {
      const g = node("g", {}, st.fetch.glyph);
      const r = tintable(rect(g, 0, 0, 150, 56, { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 4, rx: 12 }), PAL.ink);
      parts.fetch.svg.push(r);
      [0, 1].forEach((j) => parts.fetch.svg.push(tintable(line(g, 18, 19 + j * 18, 132, 19 + j * 18, { stroke: PAL.data, "stroke-width": 4 }), PAL.data)));
      return g;
    });
    const nWorkers = domTint(parts.fetch, label(root, "", { left: 820, top: st.fetch.y + 16, size: 48, mono: true }), PAL.data);
    // batching glyph: the samples as rows of numbers in brackets, and how many of them (×32)
    const stackRO = readout(root, st.batching.glyph, parts.batching, 560, st.batching.y + 4, G.station.h - 8, D.series.readout, { size: 22 });
    const nBatch = domTint(parts.batching, label(root, "\u00D7" + D.series.batch, { left: stackRO.end + 16, top: st.batching.y + 16, size: 48, mono: true }), PAL.data);
    // collate glyph: the stack becoming one block
    const colStack = [0, 1, 2].map((j) => line(st.collate.glyph, 580 + j * 6, st.collate.y + 20 + j * 20, 690 + j * 6, st.collate.y + 20 + j * 20, { stroke: PAL.data, "stroke-width": 5 }));
    line(st.collate.glyph, 720, st.collate.y + 43, 770, st.collate.y + 43, { stroke: PAL.dim, "stroke-width": 5 });
    node("polygon", { points: `770,${st.collate.y + 31} 790,${st.collate.y + 43} 770,${st.collate.y + 55}`, fill: PAL.dim }, st.collate.glyph);
    parts.collate.svg.push(tintable(rect(st.collate.glyph, 810, st.collate.y + 15, 90, 56, { fill: "none", stroke: PAL.data, "stroke-width": 5, rx: 8 }), PAL.data));

    // batch row: the tensor (rows of numbers in brackets, its shape beside), the twin, the model chip
    const bt = G.batch;
    function tensorCard(p, x) {
      const g = node("g", {}, svg);
      p.svg.push(tintable(rect(g, x, bt.y, bt.w, bt.h, { fill: PAL.panel, stroke: PAL.data, "stroke-width": 6 }), PAL.data));
      const ro = readout(root, g, p, x, bt.y + 4, bt.h - 8, D.series.readout, { size: 26, pitch: 27 });
      const labDx = ro.end + 12 - x;
      const lab = domTint(p, label(root, D.series.shape, { left: x + labDx, top: bt.y + 25, size: 34, mono: true }), PAL.ink);
      const move = (nx) => { g.setAttribute("transform", `translate(${(nx - x).toFixed(1)} 0)`); lab.style.left = `${nx + labDx}px`; ro.move(nx); };
      return { g, lab, x, move, els: ro.els };
    }
    const batch = tensorCard(parts.batch, bt.x);
    const twin = tensorCard(parts.twins, bt.x);
    const md = G.model;
    const modelG = node("g", {}, svg);
    parts.model.svg.push(tintable(rect(modelG, md.x, md.y, md.w, md.h, { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6 }), PAL.ink));
    const modelLab = domTint(parts.model, label(root, "model", { left: md.x, top: md.y + 14, size: 60, width: md.w, align: "center" }), PAL.ink);
    const arrow = node("g", {}, svg);
    line(arrow, bt.x + bt.w + 20, bt.y + bt.h / 2, md.x - 36, bt.y + bt.h / 2, { stroke: PAL.dim, "stroke-width": 6 });
    node("polygon", { points: `${md.x - 36},${bt.y + 28} ${md.x - 8},${bt.y + bt.h / 2} ${md.x - 36},${bt.y + bt.h - 28}`, fill: PAL.dim }, arrow);
    // the batch leaving the loader
    const outArrow = node("g", {}, svg);
    line(outArrow, MID, lo.y + lo.h, MID, bt.y - 30, { stroke: PAL.dim, "stroke-width": 6 });
    node("polygon", { points: `${MID - 16},${bt.y - 30} ${MID},${bt.y - 6} ${MID + 16},${bt.y - 30}`, fill: PAL.dim }, outArrow);

    const code = window.SC_makeCode ? window.SC_makeCode(root) : null;
    guides(root);

    function draw(g, S) {
      S = Object.assign({}, REST, S);
      const clock = SC.clock || 0;
      // the flip: the machine fades over the first 60 % of it, the code card comes in over the last 60 %
      const flip = S.flip || 0, mOn = 1 - seg(flip, 0, 0.6), cOn = seg(flip, 0.4, 1);
      S = Object.assign({}, S, { dataset: S.dataset * mOn, loader: S.loader * mOn, batch: S.batch * mOn, model: S.model * mOn });
      // dataset
      const dsO = S.dataset;
      show(dsG, dsO); show(dsLabel, dsO);
      const isMap = S.mode === "map";
      show(mLen, dsO * (isMap ? 1 : 0)); show(mGet, dsO * (isMap ? 1 : 0)); show(mIter, dsO * (isMap ? 0 : 1));
      // samples in flight: one every 0.9 s, hopping from the dataset card into the loader box
      flow.forEach((el, k) => {
        const u = ((clock / 1.8 + k / 2) % 1 + 1) % 1;
        const y = lerp(ds.y + ds.h + 6, lo.y - 18, u);
        el.setAttribute("transform", `translate(0 ${y.toFixed(1)})`);
        show(el, S.dataset * S.loader * (u < 0.15 ? u / 0.15 : u > 0.8 ? (1 - u) / 0.2 : 1));
      });
      // loader box and stations
      show(loG, S.loader); show(loLabel, S.loader);
      STATIONS.forEach((name) => { show(st[name].g, S.loader); show(st[name].lab, S.loader); });
      show(idx, S.loader * (1 - 0.7 * S.strike));
      st.sampler.lab.style.opacity = S.loader * (1 - 0.5 * S.strike);
      strike.setAttribute("x2", G.station.x + 20 + S.strike * (G.station.w - 40));
      show(strike, S.strike > 0.001 ? S.loader : 0);
      workers.forEach((w, k) => {
        const on = S.workers > k ? 1 : (k === 0 ? 0.5 : 0);
        w.setAttribute("transform", `translate(${580 + k * 26} ${st.fetch.y + 12 + k * 8})`);
        show(w, S.loader * on);
      });
      nWorkers.textContent = S.workers >= 2 ? "×" + S.workers : "";
      show(nWorkers, S.loader * (S.workers >= 2 ? 1 : 0));
      show(nBatch, S.loader); stackRO.els.forEach((el) => show(el, S.loader));
      // batch row
      const tw = S.twins;
      batch.lab.textContent = S.shape; twin.lab.textContent = S.shape;
      // with twins the first card slides to the safe left edge and the twin lands beside it (x 65–475, 540–950)
      const bX = lerp(bt.x, SAFE.x0, tw), twX = lerp(bt.x, SAFE.x1 - bt.w, tw);
      batch.move(bX); twin.move(twX);
      show(batch.g, S.batch); show(batch.lab, S.batch); batch.els.forEach((el) => show(el, S.batch));
      show(twin.g, S.batch * tw); show(twin.lab, S.batch * tw); twin.els.forEach((el) => show(el, S.batch * tw));
      // with twins on screen the model chip and arrow step aside
      show(modelG, S.model * (1 - tw)); show(modelLab, S.model * (1 - tw)); show(arrow, S.model * S.batch * (1 - tw));
      show(outArrow, S.loader * S.batch);
      // hero
      Object.keys(parts).forEach((k) => tint(parts[k], S.hero === k));
      if (code) { const c = Object.assign({ o: 1 }, S.code || {}); c.o *= cOn; code.set(c); }
    }
    return { draw, parts, stations: st, code, svg };
  }

  const REST = { mode: "map", workers: 0, hero: null, strike: 0, twins: 0, shape: D.series.shape, flip: 0,
                 loader: 1, batch: 1, model: 1, dataset: 1, code: { o: 0 } };
  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });
  // Register the beat: one paused timeline whose only job is to be the clock.
  function start(seconds, render) {
    const tl = gsap.timeline({ paused: true, onUpdate: () => render(tl.time()) });
    tl.to({ p: 0 }, { p: 1, duration: seconds, ease: "none" }, 0);
    tl.set({}, {}, seconds);
    window.__timelines = window.__timelines || {};
    window.__timelines["main"] = tl;
    tl.seek(0); render(0);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => render(tl.time()));
    return tl;
  }

  window.SC = { D, PAL, W, H, SAFE, MID, G, STATIONS, stationY, mount, REST, SEAM: {}, clock: 0,
                start, E, lerp, clamp01, seg, hash, pulse, label, guides, show, node, squiggle, readout };
})();
