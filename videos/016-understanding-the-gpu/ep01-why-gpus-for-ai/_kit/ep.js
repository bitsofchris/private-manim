// ep.js — ep 1's own parts on the series chip (../../_kit/chip.js). Linked into
// a beat as `ep/` (ln -s ../_kit NN_beat/ep), loaded after kit/code.js and
// before ep/seam.js. Beats call EP.mount(root) instead of SC.mount(root): it
// mounts the series chip and adds, over it,
//
//   the CPU     a box of 4 big cores. Small in the top slot (x 65–632,
//               y 250–380: "CPU" and the cores in a row); `big` grows it into
//               the chip's place (x 65–693, y 450–1078: 2 × 2 cores, each with
//               a cache block and a branch fork). The series' own CPU box
//               ("CPU / Python", ep 6's) stays hidden all episode.
//   y = x @ W   three 4 × 4 matrices in the bottom slot (y 1197–1313), in the
//               code's order. `fill` says which y cells are done.
//   wave        a bright band that sweeps the lit grid cells once (0 → 1).
//   the network a tiny neural network, 4-4-4-2 nodes left to right, in the top
//               slot (x 114–836, y 246–428) while the CPU is away (beats 1–2).
//               Its first layer (column 0 → column 1, 16 edges) is W: the
//               edges into node j are column j of W, node j's output is y's column j.
//
// Ep 1 fields of S (defaults merged into SC.REST, so tools/hf_state_check.js sees them):
//   net 0..1         the network's opacity
//   focus 0..1       beats 1–2's layout (1): the network on top, y = x @ W right under it at 1.3×
//                    (centre y 540), and the whole series chip (grid, memory, title) at 0.8×
//                    below them (centre y 925); 0 = the series layout, matrices in the bottom slot
//   flow 0|1         activity: one layer's edges at a time light teal, left to right, on SC.clock
//                    (like the chip's shimmer; must be 0 in a beat's still end)
//   cpu4 0..1        the CPU's opacity
//   big 0..1         small (top slot) → big (the chip's place); fade chip/hbm yourself
//   cores "1111"     which of the 4 cores are lit teal
//   cache, branch    0..1, the cache blocks and branch forks (drawn only as the CPU grows)
//   mat 0..1         the matrices' opacity
//   fill "0…"        16 chars, row-major: 1 = that y cell is done (teal)
//   pick -1|k        with hero "ycell": x row k/4, W column k%4 and y cell k go magenta
//   wave 0..1        the sweep's position; 0 and 1 are off
// Hero names added: "cpu" (this CPU), "net" (every node of the network),
// "layer" (the first layer's 16 edges and its 4 output nodes),
// "ycell" (row, column and the one y cell, plus output node k%4 and its 4 incoming edges),
// "y" (every y cell, plus the first layer's 4 output nodes). The chip's own (chip, tc, ...) are unchanged.
(function () {
  const SC = window.SC, { PAL, lerp, node, label, show, clamp01 } = SC;
  const LIGHT = "#8FF0E2";                       // the wave's band: teal lifted toward ink

  Object.assign(SC.REST, {
    cpu: 0, queueO: 0, strip: 0,                 // the series CPU, queue and time strip: not in ep 1
    cpu4: 1, big: 0, cores: "1111", cache: 0, branch: 0,
    mat: 1, fill: "0".repeat(16), pick: -1, wave: 0, net: 0, flow: 0, focus: 0,
  });

  // The network: 4 columns of nodes; column c's nodes centred on y 337, pitch 50.
  const NET = { xs: [130, 360, 590, 820], n: [4, 4, 4, 2], cy: 337, pitch: 50, r: 16, step: 0.35 };
  const nodeY = (c, i) => NET.cy + (i - (NET.n[c] - 1) / 2) * NET.pitch;

  // Small and big CPU geometry; cores lerp between the two.
  const SMALL = { x: 65, y: 250, w: 567, h: 130, lab: { x: 89, y: 280 },
                  core: (i) => ({ x: 240 + i * 96, y: 275, w: 80, h: 80 }) };
  const BIG = { x: 65, y: 450, w: 628, h: 628, lab: { x: 65 + 314 - 60, y: 474 },
                core: (i) => ({ x: 89 + (i % 2) * 300, y: 565 + Math.floor(i / 2) * 255, w: 280, h: 235 }) };
  // The matrices: "y ▦ = x ▦ @ W ▦", 672 px wide, centred in the safe width.
  const M = { x0: 171, top: 1197, cell: 26, pitch: 30, size: 116, ty: 1220 };
  // focus: where the matrices row and the series chip go (centre, scale) when focus = 1
  const FOCUS = { mat: { c: [507, 1255], to: [507, 540], s: 1.3 }, gpu: { c: [507.5, 805], to: [507.5, 925], s: 0.8 } };
  const ROW = [["y", 0], ["▦y", 52], ["=", 192], ["x", 252], ["▦x", 304], ["@", 444], ["W", 504], ["▦W", 556]];

  function mount(root) {
    // the series chip mounts in its own layer, so `focus` can scale all of it at once
    const layer = (parent) => {
      const d = document.createElement("div");
      d.style.cssText = `position:absolute;left:0;top:0;width:${SC.W}px;height:${SC.H}px;transform-origin:0 0;`;
      parent.appendChild(d);
      return d;
    };
    const kitDiv = layer(root);
    const kit = SC.mount(kitDiv);
    const svg = node("svg", { width: SC.W, height: SC.H, viewBox: `0 0 ${SC.W} ${SC.H}` });
    svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    svg.setAttribute("data-layout-allow-overflow", "");
    root.appendChild(svg);
    const matDiv = layer(root);                  // the matrix letters, moved with the matrices

    // the network: edges first, nodes over them
    const netG = node("g", {}, svg);
    const edges = [];                            // edges[c] = [{i, j, el}] from column c to c + 1
    for (let c = 0; c < 3; c++) {
      edges.push([]);
      for (let i = 0; i < NET.n[c]; i++) for (let j = 0; j < NET.n[c + 1]; j++) {
        const el = node("line", { x1: NET.xs[c], y1: nodeY(c, i), x2: NET.xs[c + 1], y2: nodeY(c + 1, j),
                                  "stroke-width": 4, "stroke-linecap": "round" }, netG);
        edges[c].push({ i, j, el });
      }
    }
    const nodes = NET.n.map((n, c) => [...Array(n)].map((_, i) =>
      node("circle", { cx: NET.xs[c], cy: nodeY(c, i), r: NET.r, "stroke-width": 4 }, netG)));

    // the CPU
    const cpuG = node("g", {}, svg);
    const box = node("rect", { fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6, rx: 22 }, cpuG);
    const cores = [0, 1, 2, 3].map(() => {
      const g = node("g", {}, cpuG);
      const body = node("rect", { rx: 10 }, g);
      const cache = [0, 1, 2].map(() => node("rect", { fill: PAL.panel, rx: 4 }, g));
      const fork = node("path", { fill: "none", stroke: PAL.panel, "stroke-width": 10, "stroke-linecap": "round",
                                  "stroke-linejoin": "round" }, g);
      return { body, cache, fork };
    });
    const cpuLab = label(root, "CPU", { size: 60 });

    // the matrices
    const matG = node("g", {}, svg);
    const mats = {};
    const letters = [];
    ROW.forEach(([name, dx]) => {
      if (name[0] !== "▦") {
        const el = label(matDiv, name, { left: M.x0 + dx, top: M.ty, size: 60, width: 36 });
        el.style.fontFamily = "monospace"; el.style.fontWeight = "700";
        letters.push(el);
        return;
      }
      const key = name[1];
      mats[key] = [...Array(16)].map((_, k) => node("rect", {
        x: M.x0 + dx + (k % 4) * M.pitch, y: M.top + Math.floor(k / 4) * M.pitch,
        width: M.cell, height: M.cell, rx: 5, fill: PAL.off }, matG));
    });

    function drawCpu(S) {
      const u = S.big, o = S.cpu4;
      show(cpuG, o); show(cpuLab, o);
      const bx = lerp(SMALL.x, BIG.x, u), by = lerp(SMALL.y, BIG.y, u);
      const bw = lerp(SMALL.w, BIG.w, u), bh = lerp(SMALL.h, BIG.h, u);
      Object.entries({ x: bx, y: by, width: bw, height: bh }).forEach(([k, v]) => box.setAttribute(k, v.toFixed(1)));
      const hot = S.hero === "cpu";
      box.setAttribute("stroke", hot ? PAL.hero : PAL.ink);
      cpuLab.style.color = hot ? PAL.hero : PAL.ink;
      cpuLab.style.left = `${lerp(SMALL.lab.x, BIG.lab.x, u).toFixed(1)}px`;
      cpuLab.style.top = `${lerp(SMALL.lab.y, BIG.lab.y, u).toFixed(1)}px`;
      cores.forEach((c, i) => {
        const a = SMALL.core(i), b = BIG.core(i);
        const x = lerp(a.x, b.x, u), y = lerp(a.y, b.y, u), w = lerp(a.w, b.w, u), h = lerp(a.h, b.h, u);
        const on = (S.cores || "")[i] === "1";
        Object.entries({ x, y, width: w, height: h }).forEach(([k, v]) => c.body.setAttribute(k, v.toFixed(1)));
        c.body.setAttribute("fill", on ? PAL.data : PAL.off);
        // cache: three stacked bars across the top third; branch: a fork in the lower half
        const co = clamp01(S.cache) * u, fo = clamp01(S.branch) * u;
        c.cache.forEach((r, k) => {
          r.setAttribute("x", (x + w * 0.1).toFixed(1)); r.setAttribute("y", (y + h * (0.1 + k * 0.1)).toFixed(1));
          r.setAttribute("width", (w * 0.8).toFixed(1)); r.setAttribute("height", (h * 0.06).toFixed(1));
          r.setAttribute("fill", on ? PAL.dataDeep : PAL.grid); show(r, co);
        });
        const fx = x + w * 0.5, f0 = y + h * 0.5, f1 = y + h * 0.66, f2 = y + h * 0.88;
        c.fork.setAttribute("d", `M${fx} ${f0}V${f1}M${fx} ${f1}L${fx - w * 0.2} ${f2}M${fx} ${f1}L${fx + w * 0.2} ${f2}`);
        c.fork.setAttribute("stroke", on ? PAL.dataDeep : PAL.grid); show(c.fork, fo);
      });
    }

    // translate(t) scale(s) that maps centre c to centre `to` as focus runs 0 → 1
    const fit = (F, f) => {
      const s = lerp(1, F.s, f), cx = lerp(F.c[0], F.to[0], f), cy = lerp(F.c[1], F.to[1], f);
      return [cx - s * F.c[0], cy - s * F.c[1], s];
    };
    function drawFocus(S) {
      const f = clamp01(S.focus);
      const [mx, my, ms] = fit(FOCUS.mat, f), [gx, gy, gs] = fit(FOCUS.gpu, f);
      matG.setAttribute("transform", `translate(${mx.toFixed(2)} ${my.toFixed(2)}) scale(${ms.toFixed(4)})`);
      matDiv.style.transform = `translate(${mx.toFixed(2)}px, ${my.toFixed(2)}px) scale(${ms.toFixed(4)})`;
      kitDiv.style.transform = `translate(${gx.toFixed(2)}px, ${gy.toFixed(2)}px) scale(${gs.toFixed(4)})`;
    }

    function drawMats(S) {
      show(matG, S.mat); letters.forEach((el) => show(el, S.mat));
      const k = S.pick, i = Math.floor(k / 4), j = k % 4, row = S.hero === "ycell" && k >= 0;
      const fill = S.fill || "";
      mats.x.forEach((r, n) => r.setAttribute("fill", row && Math.floor(n / 4) === i ? PAL.hero : PAL.muted));
      mats.W.forEach((r, n) => r.setAttribute("fill", row && n % 4 === j ? PAL.hero : PAL.muted));
      mats.y.forEach((r, n) => {
        const hero = (row && n === k) || (S.hero === "y" && fill[n] === "1");
        r.setAttribute("fill", hero ? PAL.hero : fill[n] === "1" ? PAL.data : PAL.off);
      });
    }

    function drawNet(S) {
      show(netG, S.net);
      if (!(S.net > 0)) return;
      const h = S.hero, j0 = S.pick % 4;
      const live = S.flow ? Math.floor((SC.clock || 0) / NET.step) % 3 : -1;   // the layer the activity is in
      edges.forEach((row, c) => row.forEach((e) => {
        const hot = (h === "layer" && c === 0) || (h === "ycell" && S.pick >= 0 && c === 0 && e.j === j0);
        e.el.setAttribute("stroke", hot ? PAL.hero : c === live ? PAL.data : PAL.muted);
      }));
      nodes.forEach((col, c) => col.forEach((el, i) => {
        const hot = h === "net" || ((h === "layer" || h === "y") && c === 1) ||
                    (h === "ycell" && S.pick >= 0 && c === 1 && i === j0);
        const on = c === live + 1 || (!S.flow && c === 0);
        el.setAttribute("stroke", hot ? PAL.hero : on ? PAL.data : PAL.dim);
        el.setAttribute("fill", hot ? PAL.hero : on ? PAL.data : PAL.panel);
      }));
    }

    // A diagonal band of lit cells turns light as `wave` runs 0 → 1.
    function drawWave(S) {
      if (!(S.wave > 0 && S.wave < 1) || !(S.chip > 0)) return;
      const front = lerp(-3, 25, S.wave);
      kit.cells.forEach((cl, n) => {
        const d = Math.abs(Math.floor(n / SC.N) + (n % SC.N) - front);
        if (d < 2.5 && cl.body.getAttribute("fill") === PAL.data) cl.body.setAttribute("fill", LIGHT);
      });
    }

    function draw(S) {
      S = Object.assign({}, SC.REST, S);
      kit.draw(S);
      drawFocus(S); drawNet(S); drawCpu(S); drawMats(S); drawWave(S);
    }
    return Object.assign({}, kit, { draw, cpu: { box, cores, label: cpuLab }, mats, letters, net: { g: netG, edges, nodes }, layers: { kit: kitDiv, mat: matDiv } });
  }

  // A beat's state at master time: blend two seam states field by field (numbers lerp, the rest switch at u ≥ 0.5).
  function mix(a, b, u) {
    const out = {};
    new Set([...Object.keys(a), ...Object.keys(b)]).forEach((k) => {
      const x = a[k] !== undefined ? a[k] : SC.REST[k], y = b[k] !== undefined ? b[k] : SC.REST[k];
      out[k] = typeof x === "number" && typeof y === "number" ? lerp(x, y, u) : u < 0.5 ? x : y;
    });
    return out;
  }

  window.EP = { mount, mix, M, SMALL, BIG, NET, FOCUS };
})();
