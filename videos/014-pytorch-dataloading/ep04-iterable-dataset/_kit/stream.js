// stream.js — ep 4's third image, the stream (Chris, 10/29: "show what
// streaming means"). Loaded after ep/ep4.js; EP4.mount draws it from S.stream.
// Shown instead of the machine and instead of the code card: never two images
// at once (ep4.js fades the machine by S.stream.o; S.flip fades the stream).
//
// Top to bottom, centred on x 507 (the machine's MID), stage y 250–1090:
//   shards     y 260–380   three file cards; the one being read has a read head
//                          that steps down its rows, one row per sample out
//   memory     y 420–540   where a loaded shard sits (beat 6); its rows leave in a
//                          shuffled order
//   __iter__   y 590–664   the gate every sample passes through
//   lane       y 664–950   samples, one at a time, down into the loader; `next()`
//                          rides up the right side on each call
//   DataLoader y 960–1090  dashed bar; samples drop into it
// Samples are the machine's glyph (one readout row in brackets, teal). The flow
// is SC.clock-driven like the machine's: one sample every PERIOD seconds.
//
// S.stream fields (all optional):
//   o 0..1          opacity of the whole image
//   order [a,b,c]   which shard sits in slot 0, 1, 2; `pos` overrides (fractional, while moving)
//   pos, lift       as ep4.js's shards (slot of card k; px up, replaces the hop)
//   read k|null     the shard being read (default: whichever sits in slot 0)
//   load 0..1       shard `read` drops from its slot into memory (1 = in memory)
//   lanes 0..1      the stream forks under the shards into two workers' __iter__ (beat 7); 1 = forked
//   ask 0..1        the `next()` call arrow's opacity
//   src 0..1        the shards' opacity; they drop in from 60 px above as it rises (beat 3)
//   flow 0..1       how far down the lane the samples have filled (0 = none yet, 1 = all of it)
//   nosampler 0..1  a struck `sampler` tag left of the gate (beat 5: nothing hands out an i)
//   hero NAME|null  shards, memory, iter, next, loader, sampler, split (the "?" between workers)
(function () {
  const SC = window.SC, D = SC.D, PAL = SC.PAL, MID = SC.MID;
  const PERIOD = 0.6;
  const SH = { w: 250, h: 120, y: 260, x: (s) => MID - 125 + (s - 1) * 280 };
  const MEM = { w: 300, h: 120, x: MID - 150, y: 420 };
  const GATE = { w: 300, h: 74, x: MID - 150, y: 590 };
  const LO = { x: 65, y: 960, w: 885, h: 130 };
  const WK = [MID - 230, MID + 230];   // worker gates' centres when forked
  const ROWS = [[0.85, 0.55, 0.7, 0.6], [0.6, 0.9, 0.45, 0.75], [0.75, 0.4, 0.8, 0.5]];
  const SHUF = [2, 0, 3, 1];          // the order a loaded shard's rows leave in

  function glyph(g, row, size) {
    const gg = SC.node("g", {}, g), text = row.join(" ") + " ⋯", w = text.length * size * 0.6;
    const t = SC.node("text", { x: 0, y: size * 0.36, "text-anchor": "middle", "font-size": size, "font-weight": 700, "font-family": "monospace", fill: PAL.data }, gg);
    t.textContent = text;
    [[-1, -w / 2 - 8], [1, w / 2 + 8]].forEach(([s, x]) => SC.node("path", { d: `M${x - 7 * s},-16 h${7 * s} v32 h${-7 * s}`, fill: "none", stroke: PAL.dim, "stroke-width": 3, "stroke-linecap": "round" }, gg));
    return gg;
  }
  function card(g, w, h, rows) {
    const cg = SC.node("g", {}, g);
    const r = SC.node("rect", { x: 0, y: 0, width: w, height: h, rx: 14, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 5 }, cg);
    const ls = rows.map((f, j) => SC.node("line", { x1: 26, y1: 24 + j * 24, x2: 26 + f * (w - 70), y2: 24 + j * 24, stroke: PAL.data, "stroke-width": 7, "stroke-linecap": "round" }, cg));
    const head = SC.node("path", { d: "M0,0 l-14,-10 v20 z", fill: PAL.ink }, cg);   // the read head, left of the row being read
    return { cg, r, ls, head };
  }

  function mount(root, svg) {   // svg: the machine's layer (ep4.js passes kit.svg)
    const g = SC.node("g", {}, svg);
    const lane = SC.node("line", { x1: MID, y1: SH.y + SH.h, x2: MID, y2: LO.y, stroke: PAL.grid, "stroke-width": 200, "stroke-linecap": "butt" }, g);
    const forks = WK.map((x) => SC.node("path", { d: "", fill: "none", stroke: PAL.grid, "stroke-width": 180, "stroke-linecap": "butt" }, g));
    const shards = [0, 1, 2].map((k) => card(g, SH.w, SH.h, ROWS[k]));
    const memRect = SC.node("rect", { x: MEM.x - 14, y: MEM.y - 14, width: MEM.w + 28, height: MEM.h + 28, rx: 20, fill: "none", stroke: PAL.muted, "stroke-width": 4, "stroke-dasharray": "14 12" }, g);
    const memLab = SC.label(root, "memory", { left: MEM.x + MEM.w + 30, top: MEM.y + 34, size: 40, color: PAL.dim });
    const flow = [0, 1, 2, 3, 4, 5].map((k) => glyph(g, D.series.readout[k % 4], 30));
    const gates = [0, 1, 2].map(() => {
      const gg = SC.node("g", {}, g);
      const r = SC.node("rect", { x: -GATE.w / 2, y: 0, width: GATE.w, height: GATE.h, rx: 37, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6 }, gg);
      return { gg, r, lab: SC.label(root, "__iter__", { size: 44, mono: true, color: PAL.ink }) };
    });
    const ask = SC.node("g", {}, g);
    const askPath = SC.node("path", { d: `M${MID + 120},930 C${MID + 230},860 ${MID + 230},720 ${MID + 170},676`, fill: "none", stroke: PAL.dim, "stroke-width": 5, "stroke-dasharray": "10 10", "stroke-linecap": "round" }, ask);
    const askHead = SC.node("path", { d: `M${MID + 170},676 l22,4 l-12,18 z`, fill: PAL.dim }, ask);
    const askLab = SC.label(root, "next()", { left: MID + 228, top: 770, size: 44, mono: true, color: PAL.dim });
    const split = SC.label(root, "?", { left: MID - 31, top: GATE.y - 32, size: 110, color: PAL.hero });
    const smpLab = SC.label(root, "sampler", { left: 60, top: GATE.y + 12, size: 44, mono: true, color: PAL.dim });
    const smpStrike = SC.node("line", { x1: 50, y1: GATE.y + 38, x2: 300, y2: GATE.y + 38, stroke: PAL.dim, "stroke-width": 6, "stroke-linecap": "round" }, g);
    const loG = SC.node("g", {}, g);
    const loRect = SC.node("rect", { x: LO.x, y: LO.y, width: LO.w, height: LO.h, rx: 34, fill: "none", stroke: PAL.muted, "stroke-width": 5, "stroke-dasharray": "22 16" }, loG);
    const loLab = SC.label(root, "DataLoader", { left: LO.x + 40, top: LO.y + 34, size: 56 });

    function draw(S) {
      const st = Object.assign({ o: 0, order: [0, 1, 2], load: 0, lanes: 0, ask: 0, src: 1, flow: 1, nosampler: 0, hero: null }, S.stream || {});
      // o 1 → 0 is a crossfade to the machine shaped like the flip: the stream is gone by o 0.4, the machine in from o 0.6 (ep4.js)
      const O = (1 - SC.seg(1 - st.o, 0, 0.6)) * (1 - SC.seg(S.flip || 0, 0, 0.6));
      const hero = (n) => (st.hero === n ? PAL.hero : null);
      const pos = st.pos || [0, 1, 2].map((k) => st.order.indexOf(k));
      const read = st.read == null ? st.order[0] : st.read;
      const clock = SC.clock || 0, step = Math.floor(clock / PERIOD), ph = clock / PERIOD - step;
      // shards and the read head
      shards.forEach((c, k) => {
        const p = pos[k], lo = Math.floor(p), hi = Math.min(2, lo + 1), f = p - lo;
        let x = SC.lerp(SH.x(lo), SH.x(hi), f), y = SH.y - (st.lift ? st.lift[k] : Math.sin(Math.PI * f) * 40) - (1 - st.src) * 60;
        let w = SH.w;
        if (k === read && st.load > 0) {
          const u = st.load;
          x = SC.lerp(x, MEM.x, u); y = SC.lerp(y, MEM.y, u); w = SC.lerp(SH.w, MEM.w, u);
        }
        c.cg.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
        c.r.setAttribute("width", w.toFixed(1));
        c.r.setAttribute("stroke", (k === read && st.load > 0.5 ? hero("memory") : hero("shards")) || PAL.ink);
        const reading = k === read && st.lanes < 0.5 && st.flow > 0;
        const row = st.load > 0.5 ? SHUF[step % 4] : step % 4;
        c.ls.forEach((l, j) => { l.style.opacity = reading && j === row ? 1 : 0.55; });
        c.head.setAttribute("transform", `translate(14 ${24 + row * 24})`);
        SC.show(c.head, reading ? 1 : 0);
        SC.show(c.cg, O * st.src);
      });
      SC.show(memRect, O * SC.seg(st.load, 0, 0.3)); SC.show(memLab, O * SC.seg(st.load, 0, 0.3));
      // the gate(s): one in the lane, or two workers' gates when forked (each reads the shards itself)
      const L = st.lanes;
      SC.show(lane, O * (L > 0 ? 0 : 1));
      forks.forEach((pth, i) => {
        const wx = SC.lerp(MID, WK[i], L);
        pth.setAttribute("d", `M${MID},${SH.y + SH.h} C${MID},${GATE.y - 80} ${wx},${GATE.y - 140} ${wx},${GATE.y} L${wx},${LO.y}`);
        SC.show(pth, O * (L > 0 ? 1 : 0));
      });
      gates.forEach((gt, i) => {
        // the workers' gates slide out of the one gate as the pipe forks
        const cx = i === 0 ? MID : SC.lerp(MID, WK[i - 1], L), cy = GATE.y;
        const a = i === 0 ? (L > 0 ? 0 : 1) : (L > 0 ? 1 : 0);
        gt.gg.setAttribute("transform", `translate(${cx} ${cy})`);
        gt.lab.style.left = `${cx - 106}px`; gt.lab.style.top = `${cy + 12}px`;
        const col = hero("iter") || PAL.ink;
        gt.r.setAttribute("stroke", col); gt.lab.style.color = col;
        SC.show(gt.gg, O * a); SC.show(gt.lab, O * a);
      });
      // samples: out of the shard (or memory), through the gate, down into the loader
      const y0 = SC.lerp(SH.y + SH.h, MEM.y + MEM.h, st.load), y1 = LO.y + 30;
      flow.forEach((el, k) => {
        const u = ((clock / PERIOD - k) / flow.length % 1 + 1) % 1;     // 0..1 along the lane, spaced 1/6 apart
        const y = SC.lerp(y0, y1, u);
        const side = k % 2;   // round robin: each sample keeps one worker the whole way (six slots, so k and k+1 alternate)
        const x = SC.lerp(MID, SC.lerp(MID, WK[side], L), SC.E().sine(SC.seg(y, SH.y + SH.h + 40, GATE.y)));
        el.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
        const inGate = y > GATE.y - 22 && y < GATE.y + GATE.h + 22;
        SC.show(el, O * (inGate ? 0 : 1) * (u <= st.flow ? 1 : 0) * SC.seg(u, 0, 0.06) * (1 - SC.seg(u, 0.92, 1)));
      });
      // next(): the loader asking, a dashed arrow up to the gate
      const askO = O * st.ask * (1 - L);
      const ac = hero("next") || PAL.dim;
      askPath.setAttribute("stroke", ac); askHead.setAttribute("fill", ac); askLab.style.color = ac;
      SC.show(ask, askO); SC.show(askLab, askO);
      SC.show(split, O * L * (st.hero === "split" ? 1 : 0));
      const sc = hero("sampler") || PAL.dim;
      smpLab.style.color = sc; smpStrike.setAttribute("stroke", sc);
      SC.show(smpLab, O * st.nosampler); SC.show(smpStrike, O * st.nosampler);
      loLab.style.color = hero("loader") || PAL.ink;
      loRect.setAttribute("stroke", hero("loader") || PAL.muted);
      SC.show(loG, O); SC.show(loLab, O);
    }
    return { draw };
  }
  window.EP4_STREAM = { mount, PERIOD };
})();
