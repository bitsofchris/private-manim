// chip.js — the shared kit for Understanding the GPU (016): the one chip every
// episode draws (SERIES.md "The series image", take A, approved by Chris
// 2026-10-29). Linked into a beat as `kit/` after kit/data.js, before
// kit/code.js:
//   ln -s ../../_kit NN_beat/kit        (from the episode folder)
//
// One state object S -> one frame, drawn by SC.mount(root).draw(S). SVG plus
// DOM labels, so `hyperframes check` sees the geometry. A beat opens on
// SC.SEAM[n-1] and ends on SC.SEAM[n]; the episode's own kit/seam.js fills
// SC.SEAM. Pure functions of S: no clocks, no randomness. The one exception is
// the shimmer of lit cells (S.shimmer), which reads SC.clock (master seconds,
// set by the beat before each draw) so it runs on across cuts;
// tools/hf_state_check.js ignores it.
//
// Layout (px, 1080×1920; the safe area is x 65–950, y 230–1536):
//   top slot     y 250–380    the CPU box (x 65–295) and its kernel queue (x 325–950),
//                             or the data loader box in the CPU's place
//   chip         y 450–1078   x 65–693: 12 × 12 cells, pitch 50; each cell is a core
//                             with its tensor core in the bottom-right corner
//   side slot    y 470–1060   x 790–950: the HBM slab (and the pipe to it, x 693–790),
//                             or the MFU meter; one at a time
//   title        y 1090       "GPU", bold and centred under the chip, the CPU label's size
//   bottom slot  y 1180–1536  the time strip (slots 1200–1260; the readout left and
//                             "time →" right at 1285), or the code card (kit/code.js);
//                             one at a time
//
// S fields (all optional; SC.REST is the rest state):
//   lit 0..1          share of cells lit teal (the same cells in every episode: ranked by hash)
//   shimmer 0|1       the lit cells trade places over time (frame 0 "already working")
//   one -1|i          a single cell lit alone (ep 7's "one tiny kernel"); its own hero name "cell"
//   tc 0..1           tensor cores emphasised (ep 5): the corners grow and brighten
//   hero NAME|null    the one magenta part: cpu, queue, chip, cell, tc, hbm, pipe, meter,
//                     loader, strip, util
//   queue [labels]    the kernel tiles, front first (default GPU_DATA.queue)
//   drain 0..1        the queue's front tile drops into the chip and the rest step forward
//   cpuWait 0..1      the CPU greys and says "waiting" (ep 6's loss.item())
//   slots "1101…"     the time strip, 24 slots: 1 = a kernel ran, 0 = idle (grey)
//   util "…"          the strip's readout (default GPU_DATA.run.util)
//   mfu 0..1          the meter's fill; mfuText its readout
//   bw 0|1            "8 TB/s" in the HBM slab
//   title "…"         the label under the chip (default "GPU"; a beat may rename it, e.g. "tensor cores";
//                     it goes magenta with the chip, or with tc when tc is the hero)
//   cpu, queueO, loader, chip, hbm, meter, strip   opacities (queueO: the queue's)
//   code {o, lines, typed, lit, cursor, blink, cy}   the code card (kit/code.js, a link to videos/_shared/web/code/code.js, preset CODE.DOCK)
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const D = window.GPU_DATA;
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const PAL = { bg: "#0B0B14", panel: "#14142B", ink: "#ECEBE4", dim: "#8A8FB0", data: "#2DD4BF",
                dataDeep: "#0F766E", hero: "#C084FC", muted: "#4A5070", grid: "#1F2440", off: "#262B4A" };
  const W = 1080, H = 1920;
  const SAFE = { x0: 65, x1: 950, y0: 230, y1: 1536 };
  const N = D.chip.n;
  const G = {
    cpu: { x: 65, y: 250, w: 230, h: 130 },
    queue: { x: 325, y: 280, w: 115, h: 70, pitch: 127, max: 5 },
    chip: { x: 65, y: 450, pitch: 50, cell: 42, pad: 18 },
    side: { x: 790, y: 470, w: 160, h: 590 },
    title: { y: 1090 },
    strip: { x: 65, y: 1200, h: 60, n: 24, w: 31, pitch: 37, readout: 1285 },
  };
  G.chip.size = N * G.chip.pitch + G.chip.pad * 2 - 8;                // 628
  G.queue.frontX = G.queue.x + G.queue.w / 2;                         // the arrow into the chip
  // Every episode lights the same cells: rank them once by a fixed hash.
  const RANK = (() => {
    const order = [...Array(N * N).keys()].sort((a, b) => hash(a * 3.7 + 1) - hash(b * 3.7 + 1));
    const r = new Array(N * N); order.forEach((c, i) => (r[c] = i)); return r;
  })();

  // ---- helpers ----
  function node(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach((k) => el.setAttribute(k, attrs[k]));
    if (parent) parent.appendChild(el);
    return el;
  }
  const rect = (g, x, y, w, h, a) => node("rect", Object.assign({ x, y, width: w, height: h, rx: 22 }, a), g);
  const show = (el, a) => { el.style.opacity = a; el.style.visibility = a > 0.001 ? "visible" : "hidden"; };
  function label(root, text, o = {}) {
    const el = document.createElement("div");
    const size = o.size || 60;
    el.textContent = text;
    el.style.cssText = `position:absolute;left:${o.left || 0}px;top:${o.top || 0}px;font-size:${size}px;` +
      `line-height:${Math.round(size * 1.15)}px;white-space:nowrap;color:${o.color || PAL.ink};` +
      (o.width ? `width:${o.width}px;text-align:${o.align || "center"};` : "");
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
  const arrowDown = (g, x, y0, y1) => {
    node("line", { x1: x, y1: y0, x2: x, y2: y1 - 22, stroke: PAL.dim, "stroke-width": 6, "stroke-linecap": "round" }, g);
    node("polygon", { points: `${x - 16},${y1 - 24} ${x},${y1} ${x + 16},${y1 - 24}`, fill: PAL.dim }, g);
  };

  // ---- mount ----
  function mount(root) {
    const svg = node("svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}` });
    svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    svg.setAttribute("data-layout-allow-overflow", "");
    root.appendChild(svg);

    // top slot: the CPU, its queue, the loader
    const cpuG = node("g", {}, svg);
    const cpuBox = rect(cpuG, G.cpu.x, G.cpu.y, G.cpu.w, G.cpu.h, { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6 });
    const cpuLab = label(root, "CPU", { left: G.cpu.x, top: G.cpu.y + 12, size: 60, width: G.cpu.w });
    const cpuSub = label(root, "Python", { left: G.cpu.x, top: G.cpu.y + 80, size: 36, width: G.cpu.w, color: PAL.dim });
    const waitLab = label(root, "waiting", { left: G.cpu.x, top: G.cpu.y + 80, size: 36, width: G.cpu.w, color: PAL.dim });
    const qG = node("g", {}, svg);
    const tiles = [...Array(G.queue.max + 1)].map(() => {
      const g = node("g", {}, qG);
      const r = rect(g, 0, G.queue.y, G.queue.w, G.queue.h, { fill: PAL.panel, stroke: PAL.data, "stroke-width": 4, rx: 12 });
      const lab = label(root, "", { top: G.queue.y + 17, size: 26, width: G.queue.w, mono: true, color: PAL.data });
      return { g, r, lab };
    });
    const qArrow = node("g", {}, svg);
    arrowDown(qArrow, G.queue.frontX, G.queue.y + G.queue.h + 10, G.chip.y - 6);
    const loaderG = node("g", {}, svg);
    const loaderBox = rect(loaderG, G.cpu.x, G.cpu.y, G.cpu.w, G.cpu.h, { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6, "stroke-dasharray": "18 12" });
    const loaderLab = label(root, "data", { left: G.cpu.x, top: G.cpu.y + 12, size: 52, width: G.cpu.w });
    const loaderSub = label(root, "loader", { left: G.cpu.x, top: G.cpu.y + 70, size: 44, width: G.cpu.w, color: PAL.dim });

    // the chip
    const c = G.chip;
    const chipG = node("g", {}, svg);
    const chipBox = rect(chipG, c.x, c.y, c.size, c.size, { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6, rx: 28 });
    const cells = [];
    for (let r = 0; r < N; r++) for (let k = 0; k < N; k++) {
      const x = c.x + c.pad + k * c.pitch, y = c.y + c.pad + r * c.pitch;
      const body = rect(chipG, x, y, c.cell, c.cell, { fill: PAL.off, rx: 6 });
      const tc = rect(chipG, x + 24, y + 24, 14, 14, { fill: PAL.grid, rx: 3 });
      cells.push({ body, tc, x, y });
    }
    const title = label(root, "", { left: c.x, top: G.title.y, size: 60, width: c.size });

    // side slot: HBM and its pipe, or the MFU meter
    const s = G.side;
    const hbmG = node("g", {}, svg);
    const hbmBox = rect(hbmG, s.x, s.y, s.w, s.h, { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6 });
    const pipe = [0, 1, 2].map((k) => rect(hbmG, c.x + c.size, 700 + k * 40, s.x - c.x - c.size, 22, { fill: PAL.dim, rx: 6, opacity: 0.8 }));
    const hbmLab = label(root, D.hbm.name[0], { left: s.x, top: 685, size: 40, width: s.w });
    const hbmLab2 = label(root, D.hbm.name[1], { left: s.x, top: 735, size: 32, width: s.w });
    const hbmAka = label(root, D.hbm.aka, { left: s.x, top: 775, size: 30, width: s.w, color: PAL.dim });
    const hbmSize = label(root, D.hbm.size, { left: s.x, top: 840, size: 34, width: s.w, color: PAL.dim });
    const hbmBw = label(root, D.hbm.bw, { left: s.x, top: 888, size: 34, width: s.w, color: PAL.dim });
    const meterG = node("g", {}, svg);
    const gauge = { x: s.x + 30, y: s.y + 150, w: s.w - 60, h: s.h - 170 };
    const meterBox = rect(meterG, gauge.x, gauge.y, gauge.w, gauge.h, { fill: PAL.bg, stroke: PAL.ink, "stroke-width": 6, rx: 16 });
    const meterFill = rect(meterG, gauge.x + 10, gauge.y + gauge.h - 10, gauge.w - 20, 0, { fill: PAL.data, rx: 8 });
    const meterLab = label(root, "MFU", { left: s.x, top: s.y, size: 52, width: s.w });
    const meterVal = label(root, "", { left: s.x, top: s.y + 66, size: 52, width: s.w, color: PAL.data });

    // bottom slot: the time strip
    const st = G.strip;
    const stripG = node("g", {}, svg);
    const stripLab = label(root, "time →", { left: st.x, top: st.readout + 8, size: 36, color: PAL.dim,
                                              width: st.n * st.pitch - (st.pitch - st.w), align: "right" });
    const slots = [...Array(st.n)].map((_, i) => rect(stripG, st.x + i * st.pitch, st.y, st.w, st.h, { fill: PAL.data, rx: 6 }));
    const utilLab = label(root, "", { left: st.x, top: st.readout, size: 48 });

    const code = window.CODE ? window.CODE.make(root, window.CODE.DOCK) : null;
    guides(root);

    function draw(S) {
      S = Object.assign({}, REST, S);
      const hero = S.hero, clock = SC.clock || 0;
      const col = (name, base) => (hero === name ? PAL.hero : base);

      // CPU, queue, loader
      show(cpuG, S.cpu); show(cpuLab, S.cpu);
      const wait = S.cpuWait;
      cpuBox.setAttribute("stroke", col("cpu", wait > 0.5 ? PAL.muted : PAL.ink));
      cpuLab.style.color = col("cpu", wait > 0.5 ? PAL.dim : PAL.ink);
      show(cpuSub, S.cpu * (1 - wait)); show(waitLab, S.cpu * wait);
      const q = S.queue || D.queue, dr = S.drain;
      tiles.forEach((t, i) => {
        const has = i < q.length;
        // tile i sits at slot i - drain; the front tile drops down the arrow as it leaves
        const slot = i - dr, x = G.queue.x + Math.max(0, slot) * G.queue.pitch;
        const drop = slot < 0 ? -slot : 0;
        t.g.setAttribute("transform", `translate(${x.toFixed(1)} ${(drop * 120).toFixed(1)})`);
        t.lab.style.left = `${x}px`; t.lab.style.top = `${G.queue.y + 17 + drop * 120}px`;
        t.lab.textContent = has ? q[i] : "";
        // the tile behind the last slot fades in as the queue steps forward
        const o = has ? S.queueO * (1 - drop) * clamp01(G.queue.max - slot) : 0;
        show(t.g, o); show(t.lab, o);
        const c2 = col("queue", PAL.data);
        t.r.setAttribute("stroke", c2); t.lab.style.color = c2;
      });
      show(qArrow, S.queueO * Math.max(S.cpu, S.loader));
      show(loaderG, S.loader); show(loaderLab, S.loader); show(loaderSub, S.loader);
      loaderBox.setAttribute("stroke", col("loader", PAL.ink)); loaderLab.style.color = col("loader", PAL.ink);

      // chip
      show(chipG, S.chip);
      chipBox.setAttribute("stroke", col("chip", PAL.ink));
      const nLit = Math.round(S.lit * N * N);
      const shift = S.shimmer ? Math.floor(clock / 0.25) * 37 : 0;
      cells.forEach((cl, i) => {
        const on = S.one >= 0 ? i === S.one : (RANK[i] + shift) % (N * N) < nLit;
        const isOne = S.one >= 0 && i === S.one;
        cl.body.setAttribute("fill", isOne && hero === "cell" ? PAL.hero : on ? PAL.data : PAL.off);
        const g = S.tc * 6;
        cl.tc.setAttribute("x", cl.x + 24 - g); cl.tc.setAttribute("y", cl.y + 24 - g);
        cl.tc.setAttribute("width", 14 + g); cl.tc.setAttribute("height", 14 + g);
        cl.tc.setAttribute("fill", hero === "tc" ? (on ? PAL.hero : "#4B2E6B") : on ? PAL.dataDeep : S.tc > 0.5 ? PAL.muted : PAL.grid);
      });
      title.textContent = S.title; show(title, S.chip * (S.title ? 1 : 0));
      title.style.color = hero === "chip" || hero === "tc" ? PAL.hero : PAL.ink;

      // side slot
      show(hbmG, S.hbm); show(hbmLab, S.hbm); show(hbmLab2, S.hbm); show(hbmAka, S.hbm); show(hbmSize, S.hbm); show(hbmBw, S.hbm * S.bw);
      hbmBox.setAttribute("stroke", col("hbm", PAL.ink)); hbmLab.style.color = hbmLab2.style.color = col("hbm", PAL.ink);
      pipe.forEach((p) => p.setAttribute("fill", col("pipe", PAL.dim)));
      show(meterG, S.meter); show(meterLab, S.meter); show(meterVal, S.meter);
      const fh = (gauge.h - 20) * clamp01(S.mfu);
      meterFill.setAttribute("y", gauge.y + gauge.h - 10 - fh); meterFill.setAttribute("height", fh);
      meterFill.setAttribute("fill", col("meter", PAL.data)); meterVal.style.color = col("meter", PAL.data);
      meterVal.textContent = S.mfuText != null ? S.mfuText : Math.round(S.mfu * 100) + "%";

      // bottom slot
      show(stripG, S.strip); show(stripLab, S.strip); show(utilLab, S.strip);
      const pat = S.slots || "1".repeat(st.n);
      slots.forEach((el, i) => el.setAttribute("fill", pat[i] === "1" ? col("strip", PAL.data) : PAL.muted));
      utilLab.textContent = S.util != null ? S.util : D.run.util;
      utilLab.style.color = col("util", PAL.ink);
      if (code) code.set(Object.assign({ o: 0 }, S.code || {}));
    }
    return { draw, cells, tiles, code, svg, gauge };
  }

  const REST = { lit: D.run.mfu, shimmer: 0, one: -1, tc: 0, hero: null, queue: null, drain: 0, cpuWait: 0,
                 slots: null, util: null, mfu: D.run.mfu, mfuText: null, bw: 0, title: D.chip.title,
                 cpu: 1, queueO: 1, loader: 0, chip: 1, hbm: 1, meter: 0, strip: 1, code: { o: 0 } };
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

  window.SC = { D, PAL, W, H, SAFE, G, N, RANK, mount, REST, SEAM: {}, clock: 0,
                start, lerp, clamp01, seg, hash, label, guides, show, node };
})();
