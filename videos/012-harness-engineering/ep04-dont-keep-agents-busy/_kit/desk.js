// desk.js — the one scene of Harness ep 4 ("Stop Keeping Agents Busy"),
// built on the shared cast kit (videos/_shared/web/cast/cast.js). Local to
// this episode: the desk, the pile of finished pages, the human's own sheet,
// the code card and the day strip are not in the kit (hand-off lists them).
// Linked into every beat as `kit/`, after cast/cast.js:
//   ln -s ../_kit NN_beat/kit
//
// One state object -> one frame. Every beat builds S(t) and calls
// scene.draw(S, t). A beat opens on DESK.SEAM[n-1] and ends on DESK.SEAM[n],
// so cuts are exact. S fields (all optional; defaults are the hook's rest):
//   flow            global count of pages thrown (float). Page j flies from
//                   agent A (even j) or B (odd j) to the pile for TRAVEL s of
//                   flow, then lands. Keep it continuous across cuts.
//   stream 0..1     how visible the flying pages and tossing arms are
//   pile0           slabs on the desk before page 0 landed
//   pileOut 0..1    the pile slides off the desk to the right and fades
//   pileHero 0..1   the pile turns magenta (the bottleneck)
//   sheet {hero, dim, ink}  the human's own sheet: magenta / muted; ink 0..5
//                   handwritten lines drawn so far
//   human {armR, armL, tilt, lean, face}, write 0..1 (arm to the sheet, pencil
//                   shown), wiggle 0..1 (the pencil moving; 0 at every seam)
//   agents {rest 0..1}  1: arms down, no tossing
//   code {a, plumb 0..1, variant, core 0..1, coreHero 0..1, under 0..1, pulse 0..1}
//   day {a, slot 0..1}
(function () {
  const { PAL } = CAST;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const lerp = (a, b, u) => a + (b - a) * u;
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mixc = (a, b, u) => { const p = hex(a), q = hex(b);                 // "#rrggbb" in and out, so mixes nest
    return "#" + p.map((v, i) => Math.round(lerp(v, q[i], clamp01(u))).toString(16).padStart(2, "0")).join(""); };
  const pulse = (t, a, b) => Math.sin(Math.PI * seg(t, a, b));

  // ---- the ledger: places shared by every beat ----
  const FLOOR = 1010;
  const HUMAN = { x: 215, s: 0.9 };
  const AG = [{ x: 790, s: 0.62 }, { x: 900, s: 0.62 }];
  const DESK = { x0: 268, x1: 682, top: 822, legs: [298, 652] };
  const SHEET = { x: 300, y: 566, w: 166, h: 248 };
  const PILE = { cx: 575, w: 150, slab: 14, pitch: 18, max: 28 };
  const TRAVEL = 1.6;                          // flow units a page spends in the air
  const CODE = { left: 72, top: 252, width: 872, plumb: ["train(model, data)", "dl = DataLoader(ds)", "log(step, loss)"],
                 core: "softmax(q @ k.T)" };
  const DAY = { x: 700, y: 336, w: 230, slots: 5, slotH: 56, gap: 6, pick: 1 };
  const HUMAN_REST = { armR: 22, armL: 22, tilt: 0, lean: 0, face: "smile" };
  const WRITE_ARM = 50;                        // 00_layout's fixed writing angle (beats use writeArm)

  // The writing arm aims the hand at the line being written: while line n
  // writes (ink n..n+1) the hand sits on line n, gliding there from line
  // n-1 over the first tenth; at rest (ink an integer) it is on the last line
  // written. Continuous in ink, so seams stay exact.
  const lineY = (i) => SHEET.y + 46 + Math.max(0, Math.min(4, i)) * 42;
  function writeArm(sh) {
    const ink = sh && sh.ink != null ? sh.ink : 1, n = Math.floor(ink), f = ink - n;
    const y = lerp(lineY(n - 1), lineY(n), Math.min(1, f / 0.1)) + 8;   // hand just under the line
    const sy = FLOOR + CAST.BODY.shoulder * HUMAN.s, len = CAST.BODY.arm * HUMAN.s;
    return Math.acos(Math.max(-1, Math.min(1, (y - sy) / len))) * 180 / Math.PI;
  }
  function mount(root) {
    const svg = CAST.layer(root);
    const N = CAST.node, L = CAST.line;
    // floor and desk (ink is structure)
    L(svg, 80, FLOOR + 6, 940, FLOOR + 6, { stroke: PAL.muted, "stroke-width": 5, "stroke-linecap": "round" });
    const human = CAST.human(svg, { x: HUMAN.x, y: FLOOR, s: HUMAN.s });
    const agents = AG.map((a) => CAST.agent(svg, { x: a.x, y: FLOOR, s: a.s }));
    const deskG = N("g", {}, svg);
    DESK.legs.forEach((x) => L(deskG, x, DESK.top, x, FLOOR, CAST.ink()));
    L(deskG, DESK.x0, DESK.top, DESK.x1, DESK.top, CAST.ink(12));
    // the human's own sheet, propped on the desk, with handwritten lines
    const sheetG = N("g", {}, svg);
    const sheetBox = N("rect", { x: SHEET.x, y: SHEET.y, width: SHEET.w, height: SHEET.h, rx: 8, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7 }, sheetG);
    const hand = [];
    for (let i = 0; i < 5; i++) {
      const y = SHEET.y + 46 + i * 42, x0 = SHEET.x + 22, x1 = SHEET.x + SHEET.w - 22 - (i % 3) * 18;
      let d = `M${x0} ${y}`;
      for (let x = x0 + 12, k = 0; x <= x1; x += 12, k++) d += ` Q${x - 6} ${y + (k % 2 ? 9 : -9)} ${x} ${y}`;
      hand.push(N("path", { d, fill: "none", stroke: PAL.ink, "stroke-width": 5, "stroke-linecap": "round", pathLength: 1, "stroke-dasharray": "1 1", "stroke-dashoffset": 1 }, sheetG));
    }
    const pencil = L(svg, 0, 0, 0, 0, { stroke: PAL.dim, "stroke-width": 7, "stroke-linecap": "round" });
    // the pile: side-on slabs on the desk, pre-made
    const pileG = N("g", {}, svg);
    const slabs = [];
    for (let i = 0; i < PILE.max; i++)
      slabs.push(N("rect", { x: PILE.cx - PILE.w / 2 + (hash(i) * 18 - 9), y: DESK.top - 6 - (i + 1) * PILE.pitch, width: PILE.w, height: PILE.slab,
                             rx: 4, fill: PAL.panel, stroke: PAL.data, "stroke-width": 5 }, pileG));
    // pages in the air: a small pool of agent pages
    const flyers = [0, 1, 2].map(() => CAST.page(svg, { s: 0.24, lines: 5 }));
    // pages fly past the agents' eyes on purpose: waive the overlap on both texts
    flyers.concat(agents).forEach((p) => p.el.querySelectorAll("text").forEach((el) => el.setAttribute("data-layout-allow-overlap", "")));
    // the code card (DOM text, so check sees it)
    const card = document.createElement("div");
    card.style.cssText = `position:absolute;left:${CODE.left}px;top:${CODE.top}px;width:${CODE.width}px;height:214px;border-radius:20px;` +
      `background:${PAL.panel};border:5px solid ${PAL.muted};padding:22px 34px;`;
    const row = (col) => { const d = document.createElement("div"); d.style.cssText = `font-size:60px;line-height:80px;white-space:nowrap;color:${col};`; d.style.fontFamily = "monospace"; card.appendChild(d); return d; };
    const plumb = row(PAL.data), core = row(PAL.ink);
    const under = document.createElement("div");
    under.style.cssText = `position:absolute;left:34px;top:178px;height:6px;width:${CODE.core.length * 36}px;background:${PAL.hero};border-radius:3px;transform-origin:0 50%;`;
    card.appendChild(under);
    root.appendChild(card);
    // the day strip: "today" and five slots; one gets blocked
    const dayLab = document.createElement("div");
    dayLab.textContent = "today";
    dayLab.style.cssText = `position:absolute;left:${DAY.x}px;top:${DAY.y - 92}px;width:${DAY.w}px;text-align:center;font-size:60px;line-height:70px;color:${PAL.ink};`;
    root.appendChild(dayLab);
    const dayG = N("g", {}, svg);
    const dayH = DAY.slots * (DAY.slotH + DAY.gap) + DAY.gap;
    N("rect", { x: DAY.x, y: DAY.y, width: DAY.w, height: dayH, rx: 14, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7 }, dayG);
    const slotEls = [];
    for (let i = 0; i < DAY.slots; i++)
      slotEls.push(N("rect", { x: DAY.x + 14, y: DAY.y + DAY.gap + 4 + i * (DAY.slotH + DAY.gap), width: DAY.w - 28, height: DAY.slotH - 8, rx: 8,
                              fill: PAL.hero, "fill-opacity": 0, stroke: PAL.muted, "stroke-width": 5 }, dayG));

    function draw(S, t) {
      const st = S.stream || 0, flow = S.flow || 0, rest = (S.agents && S.agents.rest) || 0;
      // ---- pile ----
      const landed = Math.max(0, Math.floor(flow - TRAVEL) + 1);
      const n = Math.min(PILE.max, Math.round((S.pile0 == null ? 6 : S.pile0)) + landed);
      const out = S.pileOut || 0, pc = mixc(PAL.data, PAL.hero, S.pileHero || 0);
      pileG.setAttribute("transform", `translate(${420 * out * out} 0)`);
      pileG.setAttribute("opacity", 1 - out);
      slabs.forEach((el, i) => { el.setAttribute("opacity", i < n ? 1 : 0); el.setAttribute("stroke", pc); });
      const topY = DESK.top - 6 - n * PILE.pitch;
      // ---- flyers: page j in the air while 0 <= flow - j < TRAVEL ----
      const toss = [0, 0];
      flyers.forEach((f, k) => {
        const j = Math.floor(flow) - k, u = (flow - j) / TRAVEL;
        if (j < 0 || u < 0 || u >= 1 || st <= 0) { CAST.show(f, 0); return; }
        const a = agents[j % 2], [hx, hy] = CAST.hand(a, -1);
        const v = E.io(u), x = lerp(hx, PILE.cx, v) - 31, y = lerp(hy, topY - 30, v) - 220 * Math.sin(Math.PI * v) - 40;
        CAST.place(f, x, y, 0.24, lerp(-25, 8, v) + (j % 2 ? 10 : 0));
        CAST.show(f, st * Math.min(1, (1 - u) * 6));
        toss[j % 2] = Math.max(toss[j % 2], 1 - u / 0.35);
      });
      agents.forEach((a, i) => {
        const up = clamp01(toss[i]) * st * (1 - rest);
        CAST.pose(a, { armL: 24 + 92 * E.io(up), armR: 24, lean: -4 * up });
        CAST.blink(a, S.agents && S.agents.blink && S.agents.blink[i] ? 1 : 0);
      });
      // ---- the human ----
      const H = Object.assign({}, HUMAN_REST, S.human || {});
      const w = S.write || 0;
      const armR = H.armR + w * (writeArm(S.sheet) - H.armR) + (S.wiggle || 0) * 4 * Math.sin(t * 13);
      CAST.pose(human, { armR, armL: H.armL, tilt: H.tilt, lean: H.lean });
      CAST.face(human, H.face);
      const [px, py] = CAST.hand(human, 1);
      pencil.setAttribute("x1", px - 4); pencil.setAttribute("y1", py + 6);
      pencil.setAttribute("x2", px + 30); pencil.setAttribute("y2", py - 30);
      pencil.setAttribute("opacity", w > 0.02 ? Math.min(1, w * 3) : 0);
      // ---- the sheet ----
      const sh = S.sheet || {}, sc = mixc(mixc(PAL.ink, PAL.muted, sh.dim || 0), PAL.hero, sh.hero || 0);
      sheetBox.setAttribute("stroke", sc);
      const ink = sh.ink == null ? 1 : sh.ink;
      hand.forEach((p, i) => { p.setAttribute("stroke", sc); p.setAttribute("stroke-dashoffset", 1 - clamp01(ink - i)); });
      // ---- code card ----
      const c = Object.assign({ a: 0, plumb: 0, variant: 0, core: 0, coreHero: 0, under: 0, pulse: 0 }, S.code || {});
      card.style.opacity = c.a;
      card.style.transform = `translateY(${(1 - c.a) * -24}px)`;
      const ptxt = CODE.plumb[c.variant % CODE.plumb.length];
      plumb.textContent = ptxt.slice(0, Math.round(ptxt.length * clamp01(c.plumb)));
      core.textContent = CODE.core;
      core.style.color = mixc(PAL.ink, PAL.hero, c.coreHero);
      core.style.clipPath = `inset(0 ${100 * (1 - clamp01(c.core))}% 0 0)`;
      core.style.transform = `scale(${1 + 0.06 * c.pulse})`;
      core.style.transformOrigin = "0 50%";
      under.style.transform = `scaleX(${clamp01(c.under)})`;
      // ---- day strip ----
      const d = Object.assign({ a: 0, slot: 0 }, S.day || {});
      dayG.setAttribute("opacity", d.a); dayLab.style.opacity = d.a;
      dayG.setAttribute("transform", `translate(${(1 - d.a) * 60} 0)`);
      slotEls.forEach((el, i) => {
        const on = i === DAY.pick ? d.slot : 0;
        el.setAttribute("stroke", mixc(PAL.muted, PAL.hero, on)); el.setAttribute("fill-opacity", 0.55 * on);
      });
    }
    return { draw, human, agents, svg };
  }

  const E = { io: (u) => (u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2), out: (u) => 1 - (1 - u) * (1 - u) };

  // Seam states: SEAM[n] is the last frame of beat n and the first of beat
  // n+1 (SEAM[0] is frame 0 of the hook). Pass MASTER time to draw (beat
  // start + t). wiggle is 0 in every seam, so the hold is still and the
  // cut matches; a beat ramps it up while the human writes.
  // Beat starts (master s): START[n] for beat n.
  const START = { 1: 0, 2: 5.50, 3: 10.00, 4: 13.10, 5: 18.85, 6: 26.75, 7: 32.20, 8: 37.05, 9: 41.80, end: 47.486 };
  const SEAM = {
    0: { flow: 2.0, stream: 1, pile0: 4, sheet: { ink: 1 }, write: 1 },
    1: { flow: 7.8, stream: 1, pile0: 4, sheet: { ink: 2, hero: 1 }, write: 0 },
    2: { flow: 16.8, stream: 1, pile0: 4, sheet: { ink: 2 }, human: { tilt: 8, face: "flat" } },
    3: { flow: 24.8, stream: 1, pile0: 4, pileHero: 1, sheet: { ink: 2, dim: 1 }, human: { lean: -8, tilt: -6, face: "frown" } },
    4: { flow: 26.5, stream: 0, pile0: 4, pileOut: 1, agents: { rest: 1 }, sheet: { ink: 3, hero: 1 }, write: 1 },
    5: { flow: 26.5, stream: 0, pile0: 4, pileOut: 1, agents: { rest: 1 }, sheet: { ink: 3 }, write: 1,
         code: { a: 1, plumb: 1, variant: 0, core: 1, coreHero: 1 } },
    6: { flow: 26.5, stream: 0, pile0: 4, pileOut: 1, agents: { rest: 1 }, sheet: { ink: 3 }, write: 0,
         human: { armL: 150, tilt: 10, face: "flat" }, code: { a: 1, plumb: 1, variant: 2, core: 1, coreHero: 1, under: 1 } },
    7: { flow: 26.5, stream: 0, pile0: 4, pileOut: 1, agents: { rest: 1 }, sheet: { ink: 4, hero: 1 }, write: 1 },
    8: { flow: 26.5, stream: 0, pile0: 4, pileOut: 1, agents: { rest: 1 }, sheet: { ink: 4 }, write: 1, day: { a: 1, slot: 1 } },
    9: { flow: 26.5, stream: 0, pile0: 4, pileOut: 1, agents: { rest: 1 }, sheet: { ink: 5 }, write: 0, day: { a: 1, slot: 1 } },
  };

  window.DESK = { FLOOR, HUMAN, AG, DESK, SHEET, PILE, TRAVEL, CODE, DAY, HUMAN_REST, WRITE_ARM, SEAM, START,
                  mount, E, clamp01, seg, lerp, hash, mixc, pulse };
})();
