// loop.js — ep 1's image: the training loop as a track the batch rides
// (Chris's diagram 1, redrawn in the series' card style). Episode-only
// helper of videos/014-pytorch-dataloading/ep01-training-loop; linked into a
// beat as `ep/` and loaded after kit/code.js:
//   ln -s ../_kit NN_beat/ep           (from the episode folder)
//   <script src="ep/loop.js"></script>
//
// It wraps SC.mount so the shared draw(g, S) also draws the loop from
// S.loop, and the state checker (tools/hf_state_check.js) sees one state.
// A loop beat turns the machine off with SC.LOOP_ONLY (its four opacities
// at 0) and the machine beats leave S.loop out (REST: { o: 0 }).
//
// Layout (take "ring", the approved one; "column" was the alternate):
//   DataLoader card  y 250–400  x 190–825   the slot (a batch glyph) at left, "DataLoader" at right
//   forward / loss / backward / update   x 480–840,  y 460, 610, 760, 910 (90 tall)
//   (stacked under the loader's right half; "column" centres them)
//   the track: out of the slot, down the right gutter (x 900) past the
//   four boxes, under update (y 1040), up the left gutter
//   (x 130), back into the slot. The glyph rides beside the boxes, never
//   over a label.
//
// S.loop fields (all optional):
//   o 0..1           opacity of the whole loop image (S.flip fades it like the machine)
//   take "ring"|"column"
//   u 0..1           where the riding batch is along the track (0 = in the slot; wraps)
//   batch 0..1       opacity of the riding batch glyph
//   slot 0..1        a second batch waiting in the slot (the next batch)
//   lit NAME|null    the magenta hero: batch, loader, forward, loss, backward, update,
//                    step (the four boxes together), track (the loop itself)
// LOOP.at(take, name) gives the u where the glyph sits beside a box
// ("forward", "loss", "backward", "update") or in the slot ("loader").
// LOOP.CODE is the code card's lines (SERIES.md ledger, "The training loop");
// LOOP.BODY its last four (the card before the `for` headers are typed), LOOP.STEP
// the four names to light together.
(function () {
  const SC = window.SC, PAL = SC.PAL, { node, label, show, lerp, seg, clamp01 } = SC;
  const BOXES = ["forward", "loss", "backward", "update"];
  const GLYPH = { w: 96, h: 56 };   // the batch glyph: a tiny readout, brackets and two rows of digits (machine.js tensorCard, small)
  const CODE = [
    { t: "for epoch in range(epochs):", lit: "outer" },
    { t: "  for batch in loader:", lit: "inner" },
    { t: "    out = model(batch)", lit: "forward" },
    { t: "    loss = loss_fn(out, y)", lit: "loss" },
    { t: "    loss.backward()", lit: "backward" },
    { t: "    optimizer.step()", lit: "update" },
  ];
  const BODY = CODE.slice(2);   // the four lines of the body, shown alone before the headers arrive (beats 4, 6)
  const TAKES = {
    ring: {
      loader: { x: 190, y: 250, w: 635, h: 150, slot: [305, 325], label: 400 },
      boxes: { forward: { x: 480, y: 460, w: 360, h: 90 }, loss: { x: 480, y: 610, w: 360, h: 90 },
               backward: { x: 480, y: 760, w: 360, h: 90 }, update: { x: 480, y: 910, w: 360, h: 90 } },
      track: [[305, 325], [305, 435], [900, 435], [900, 505], [900, 655], [900, 805], [900, 955], [900, 1040], [130, 1040], [130, 325], [305, 325]],
      beside: { loader: 0, forward: 3, loss: 4, backward: 5, update: 6 },
      dashedFrom: 7,
      arrows: [[900, 452, "down"], [148, 325, "right"]],
    },
    column: {
      loader: { x: 190, y: 250, w: 635, h: 150, slot: [305, 325], label: 400 },
      boxes: { forward: { x: 300, y: 460, w: 360, h: 90 }, loss: { x: 300, y: 610, w: 360, h: 90 },
               backward: { x: 300, y: 760, w: 360, h: 90 }, update: { x: 300, y: 910, w: 360, h: 90 } },
      track: [[305, 325], [305, 435], [725, 435], [725, 505], [725, 655], [725, 805], [725, 955], [725, 1040], [130, 1040], [130, 325], [305, 325]],
      beside: { loader: 0, forward: 3, loss: 4, backward: 5, update: 6 },
      dashedFrom: 7,
      arrows: [[725, 452, "down"], [148, 325, "right"]],
    },
  };
  // arc-length parametrisation of a track
  function measure(track) {
    const seglen = [], cum = [0];
    for (let i = 1; i < track.length; i++) {
      const d = Math.hypot(track[i][0] - track[i - 1][0], track[i][1] - track[i - 1][1]);
      seglen.push(d); cum.push(cum[i - 1] + d);
    }
    return { seglen, cum, total: cum[cum.length - 1] };
  }
  Object.keys(TAKES).forEach((k) => { TAKES[k].m = measure(TAKES[k].track); });
  function pointAt(take, u) {
    const T = TAKES[take], m = T.m;
    u = ((u % 1) + 1) % 1;
    const s = u * m.total;
    let i = 1;
    while (i < m.cum.length - 1 && m.cum[i] < s) i++;
    const a = T.track[i - 1], b = T.track[i], v = m.seglen[i - 1] ? (s - m.cum[i - 1]) / m.seglen[i - 1] : 0;
    return [lerp(a[0], b[0], v), lerp(a[1], b[1], v)];
  }
  const at = (take, name) => { const T = TAKES[take]; return T.m.cum[T.beside[name]] / T.m.total; };

  function mountLoop(root, svg) {
    const NS = "http://www.w3.org/2000/svg";
    const g = node("g", {}, svg);
    const dom = [];
    const built = {};
    function glyph(parent) {
      const gg = node("g", {}, parent);
      const r = node("rect", { x: -GLYPH.w / 2, y: -GLYPH.h / 2, width: GLYPH.w, height: GLYPH.h, rx: 12, fill: PAL.panel, stroke: PAL.data, "stroke-width": 5 }, gg);
      const rows = SC.D.series.readout.slice(0, 2);
      // the rounded card is the bracket here: two rows of the readout's digits inside it
      const ts = rows.map((row, j) => { const t = node("text", { x: 0, y: -4 + j * 20, "text-anchor": "middle", "font-size": 17, "font-weight": 700, "font-family": "monospace", fill: PAL.data }, gg); t.textContent = row.join(" "); return t; });
      return { g: gg, tint: (on) => { const c = on ? PAL.hero : PAL.data; r.setAttribute("stroke", c); ts.forEach((t) => t.setAttribute("fill", c)); } };
    }
    Object.keys(TAKES).forEach((take) => {
      const T = TAKES[take], tg = node("g", {}, g), B = {};
      // the track: solid out of the slot and past the boxes, dashed on the way back
      const pts = T.track;
      const solid = node("polyline", { points: pts.slice(0, T.dashedFrom + 1).map((p) => p.join(",")).join(" "), fill: "none", stroke: PAL.muted, "stroke-width": 5, "stroke-linejoin": "round" }, tg);
      const dashed = node("polyline", { points: pts.slice(T.dashedFrom).map((p) => p.join(",")).join(" "), fill: "none", stroke: PAL.muted, "stroke-width": 5, "stroke-dasharray": "18 14", "stroke-linejoin": "round" }, tg);
      const heads = T.arrows.map(([x, y, dir]) => node("polygon", {
        points: dir === "down" ? `${x - 14},${y - 24} ${x + 14},${y - 24} ${x},${y}` : `${x - 24},${y - 14} ${x - 24},${y + 14} ${x},${y}`, fill: PAL.muted }, tg));
      // the DataLoader card
      const L = T.loader;
      const lRect = node("rect", { x: L.x, y: L.y, width: L.w, height: L.h, rx: 22, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6 }, tg);
      const lLab = label(root, "DataLoader", { left: L.x + L.label - L.x, top: L.y + 40, size: 60 });
      lLab.style.left = `${L.label}px`;
      dom.push(lLab);
      const slotGlyph = glyph(tg); slotGlyph.g.setAttribute("transform", `translate(${L.slot[0]} ${L.slot[1]})`);
      // the four boxes
      BOXES.forEach((name) => {
        const b = T.boxes[name];
        const r = node("rect", { x: b.x, y: b.y, width: b.w, height: b.h, rx: 22, fill: PAL.panel, stroke: PAL.muted, "stroke-width": 5 }, tg);
        const lab = label(root, name, { left: b.x + 28, top: b.y + 11, size: 60 });
        dom.push(lab);
        B[name] = { r, lab };
      });
      const ride = glyph(tg);
      built[take] = { tg, solid, dashed, heads, lRect, lLab, slotGlyph, B, ride, labels: [lLab].concat(BOXES.map((n) => B[n].lab)) };
    });
    function draw(Lp, mOn) {
      Lp = Object.assign({ o: 0, take: "ring", u: 0, batch: 1, slot: 0, lit: null }, Lp || {});
      const o = clamp01(Lp.o) * mOn;
      Object.keys(built).forEach((take) => {
        const K = built[take], on = take === Lp.take ? o : 0;
        show(K.tg, on); K.labels.forEach((el) => show(el, on));
        if (on <= 0.001) return;
        const trackHot = Lp.lit === "track";
        [K.solid, K.dashed].forEach((el) => el.setAttribute("stroke", trackHot ? PAL.hero : PAL.muted));
        K.heads.forEach((el) => el.setAttribute("fill", trackHot ? PAL.hero : PAL.muted));
        const loaderHot = Lp.lit === "loader";
        K.lRect.setAttribute("stroke", loaderHot ? PAL.hero : PAL.ink);
        K.lLab.style.color = loaderHot ? PAL.hero : PAL.ink;
        BOXES.forEach((name) => {
          const hot = Lp.lit === name || Lp.lit === "step";
          K.B[name].r.setAttribute("stroke", hot ? PAL.hero : PAL.muted);
          K.B[name].lab.style.color = hot ? PAL.hero : PAL.ink;
        });
        const [x, y] = pointAt(take, Lp.u);
        K.ride.g.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
        show(K.ride.g, clamp01(Lp.batch));
        K.ride.tint(Lp.lit === "batch");
        show(K.slotGlyph.g, clamp01(Lp.slot));
        K.slotGlyph.tint(false);
      });
    }
    return { draw, built, pointAt };
  }

  const realMount = SC.mount;
  SC.mount = function (root) {
    const kit = realMount(root);
    const L = mountLoop(root, kit.svg);
    const machineDraw = kit.draw;
    kit.draw = (g, S) => {
      machineDraw(g, S);
      const flip = (S && S.flip) || 0, mOn = 1 - seg(flip, 0, 0.6);
      L.draw(S && S.loop, mOn);
    };
    kit.loop = L;
    return kit;
  };
  SC.REST.loop = { o: 0 };
  SC.LOOP_ONLY = { dataset: 0, loader: 0, batch: 0, model: 0, hero: null };
  const STEP = BOXES.slice();   // the four body lines lit together: code.lit = LOOP.STEP ("one training step")
  window.LOOP = { TAKES, CODE, BODY, STEP, at, pointAt, BOXES };
})();
