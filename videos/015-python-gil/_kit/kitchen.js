// kitchen.js — the shared kit for 015 (the Python GIL series): one kitchen,
// one knife. Every beat of both episodes loads it (through its `kit` symlink,
// BEFORE cast/cast.js: it shims createElementNS for tools/hf_state_check.js,
// whose stub DOM lacks it) so the kitchen, the cooks, the knife, the oven, the
// appliance, the row of kitchens, the wall with its pipe and the fridge are
// identical from beat to beat, and each beat opens on the previous beat's last
// frame (SC.SEAM1 / SC.SEAM2, one state object per cut; SC.REST the defaults).
//
// Every label shows both names (Chris, 10/27): the kitchen word on the first
// line, the real term on the second. The analogy never floats free.
//
// Pure functions of their arguments: no clocks, no randomness. A beat calls
//   const k = SC.mount(root); k.draw(null, S)   // S: a state (SC.state(SEAM1[n], patch))
// with S.chop the knife's chop phase (0 at every seam, so the last frame is still).
//
// Layout (px, 1080×1920; captions anchored bottom, so the stage runs to y 1330):
//   label row     y 235–367   "kitchen / process" left, "knife / GIL" right
//   kitchen box   y 380–900   x 80–950; cooks' feet at y 880 (~250 px tall, toques on); counter y 740–765
//   bottom zone   y 980–1300  code card, timer bar, the ghost kitchen, the small row, the fridge
//   big row       y 380–900   the four kitchens, when the row is the subject (ep 2)
(function () {
  if (typeof document !== "undefined" && !document.createElementNS)
    document.createElementNS = (ns, tag) => document.createElement(tag);   // hf_state_check stub DOM

  const PAL = { bg: "#0B0B14", panel: "#14142B", ink: "#ECEBE4", dim: "#8A8FB0",
                data: "#2DD4BF", hero: "#C084FC", muted: "#4A5070" };
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const io = (u) => (u < 0.5 ? 2 * u * u : 1 - (-2 * u + 2) ** 2 / 2);
  const pulse = (t, at, w = 0.6) => { const u = (t - at) / w; return u < 0 || u > 1 ? 0 : Math.sin(Math.PI * u); };
  const copy = (v) => JSON.parse(JSON.stringify(v));
  // deep merge (arrays replaced whole)
  function merge(a, b) {
    const out = copy(a || {});
    Object.keys(b || {}).forEach((k) => {
      out[k] = b[k] && typeof b[k] === "object" && !Array.isArray(b[k]) && out[k] && typeof out[k] === "object" && !Array.isArray(out[k])
        ? merge(out[k], b[k]) : copy(b[k]);
    });
    return out;
  }

  // ---- geometry ----
  const BOX = { x: 80, y: 380, w: 870, h: 520, rx: 28 };
  const FEET = 880, FIG = 0.48;               // cooks ~260 px tall; the knife keeps its own size
  const COUNTER = { x: 290, y: 740, w: 520, h: 25 };
  const SPOT = { counter: [370, 500, 630, 760], oven: 860, appl: 170 };
  const OVEN = { x: 800, y: 660, w: 120, h: 180 };
  const APPL = { x: 110, y: 770, w: 120, h: 70 };
  const ZONE = { y: 980, h: 320 };                  // bottom zone
  const ROW = { n: 4, w: 200, gap: 23, x0: 80 };    // four kitchens across the safe width
  const rowX = (i) => ROW.x0 + i * (ROW.w + ROW.gap);
  // the row in its two homes: small (bottom zone) and big (the kitchen box's place)
  const ROW_SMALL = { y: 1050, h: 250, fig: 0.27, feet: 1278, counter: 1205 };
  const ROW_BIG = { y: 420, h: 440, fig: 0.44, feet: 830, counter: 720 };
  const WALL_I = 2;                                  // the wall stands before kitchen index 2
  const PIPE = { y: 600, h: 44, x0: 420, x1: 610 };  // crosses the wall between kitchens 1 and 2 (big row)
  const FRIDGE = { x: 80, y: 980, w: 870, h: 320, door: 420, shelves: [1050, 1130, 1210] };

  // ---- the state ----
  const REST = {
    K: { o: 1, lab: 1 },
    cooks: [{ at: "counter", wait: 0 }, { at: "counter", wait: 0 }, { at: "counter", wait: 0 }, { at: "counter", wait: 0 }],
    cooksLab: 0,
    knife: { holder: 0, lab: 0, hero: 1 },          // holder −1: on the counter
    oven: { o: 0, lab: 0 }, appl: { o: 0, lab: 0 },
    code: { o: 0, text: "" }, timer: { o: 0, fill: 0 },
    ghost: { o: 0 },
    row: { o: 0, big: 0, lab: 0, hero: 0, chop: 0 },
    tag: { o: 0 },
    wall: { o: 0, lab: 0, bowl: 0, boxed: 0, bowlO: 0 },
    fridge: { o: 0, lab: 0, bowl: 0, note: 0, noteO: 0, noteHero: 0 },
    close: { o: 0 },                                 // the final labels (ep 1: waiting → threads / running Python → processes)
    chop: 0,
  };
  const state = (base, patch) => merge(merge(REST, base || {}), patch || {});

  // Episode 1 cuts (beat n ends / beat n+1 starts); SEAM1[0] is frame 0.
  const SEAM1 = {
    0: state({}),
    1: state({ cooksLab: 1 }),
    2: state({ cooksLab: 1, knife: { lab: 1 }, cooks: [{ at: "counter", wait: 0 }, { at: "counter", wait: 1 }, { at: "counter", wait: 1 }, { at: "counter", wait: 1 }] }),
    3: state({ cooksLab: 1, knife: { lab: 1, holder: 3 }, cooks: [{ at: "counter", wait: 1 }, { at: "counter", wait: 1 }, { at: "counter", wait: 1 }, { at: "counter", wait: 0 }],
               code: { o: 1, text: "threads" }, timer: { o: 1, fill: 1 } }),
    4: state({ cooksLab: 1, knife: { lab: 1, holder: 2 }, oven: { o: 1, lab: 1 },
               cooks: [{ at: "counter", wait: 1 }, { at: "oven", wait: 1 }, { at: "counter", wait: 0 }, { at: "counter", wait: 1 }],
               timer: { o: 1, fill: 1 } }),
    5: state({ cooksLab: 1, knife: { lab: 1, holder: 2 }, oven: { o: 1, lab: 1 }, appl: { o: 1, lab: 1 },
               cooks: [{ at: "counter", wait: 1 }, { at: "oven", wait: 1 }, { at: "counter", wait: 0 }, { at: "appl", wait: 0 }],
               timer: { o: 1, fill: 1 } }),
    6: state({ cooksLab: 1, knife: { lab: 1, holder: 2 }, oven: { o: 1, lab: 1 }, appl: { o: 1, lab: 1 },
               cooks: [{ at: "counter", wait: 1 }, { at: "oven", wait: 1 }, { at: "counter", wait: 0 }, { at: "appl", wait: 0 }],
               ghost: { o: 1 }, close: { o: 1 } }),
  };
  // Episode 2 cuts. Frame 0 is ep 1's close with the row real instead of ghost.
  const EP2_KITCHEN = { cooksLab: 1, knife: { lab: 1, holder: 2 }, oven: { o: 1, lab: 1 }, appl: { o: 1, lab: 1 },
                        cooks: [{ at: "counter", wait: 1 }, { at: "oven", wait: 1 }, { at: "counter", wait: 0 }, { at: "appl", wait: 0 }] };
  const EP2_ROWBIG = { K: { o: 0, lab: 0 }, knife: { hero: 0, lab: 0 }, oven: { o: 0, lab: 0 }, appl: { o: 0, lab: 0 }, cooksLab: 0,
                       row: { o: 1, big: 1, lab: 1, hero: 1, chop: 1 } };
  const SEAM2 = {
    0: state(EP2_KITCHEN, { row: { o: 1, big: 0, lab: 0, hero: 0, chop: 1 }, close: { o: 1 } }),
    1: state(EP2_KITCHEN, { row: { o: 1, big: 0, lab: 0, hero: 0, chop: 1 }, close: { o: 1 } }),
    2: state(EP2_KITCHEN, { row: { o: 1, big: 0, lab: 0, hero: 0, chop: 1 }, close: { o: 1 }, tag: { o: 1 } }),
    3: state(EP2_ROWBIG, { code: { o: 1, text: "loader" } }),
    4: state(EP2_ROWBIG, { row: { chop: 0, hero: 0 }, wall: { o: 1, lab: 1, bowl: 1, boxed: 0, bowlO: 1 }, timer: { o: 1, fill: 0.55 } }),
    5: state(EP2_ROWBIG, { row: { chop: 0, hero: 0 }, wall: { o: 1, lab: 0 }, fridge: { o: 1, lab: 1, bowl: 1, note: 1, noteO: 1, noteHero: 1 } }),
    6: state(EP2_ROWBIG, { row: { chop: 1, hero: 1 }, wall: { o: 1, lab: 0 }, fridge: { o: 1, lab: 1, bowl: 1, note: 1, noteO: 1, noteHero: 0 }, close: { o: 1 } }),
  };

  // ---- drawing ----
  function mount(root) {
    const C = window.CAST, I = window.ISO;
    const svg = C.layer(root);
    const node = C.node, line = C.line, ink = C.ink;
    const opac = (el, a) => { el.setAttribute("opacity", clamp01(a)); el.setAttribute("visibility", a > 0.001 ? "visible" : "hidden"); };
    const domOpac = (el, a) => { el.style.opacity = clamp01(a); el.style.visibility = a > 0.001 ? "visible" : "hidden"; };
    // A two-line label: the kitchen word, then the real term. Both ≥ 60 px.
    function pair(top, bottom, o) {
      const a = I.label(root, top, { size: 60, left: o.left, top: o.top, width: o.width, align: o.align || "center", color: o.color || PAL.ink });
      const b = I.label(root, bottom, { size: 60, left: o.left, top: o.top + 66, width: o.width, align: o.align || "center", color: o.color2 || PAL.dim });
      const set = (alpha, hero) => { [a, b].forEach((el) => domOpac(el, alpha)); if (hero !== undefined) { a.style.color = hero ? PAL.hero : (o.color || PAL.ink); b.style.color = hero ? PAL.hero : (o.color2 || PAL.dim); } };
      set(0);
      return { a, b, set };
    }

    // the kitchen box, counter, oven, appliance
    const gK = node("g", {}, svg);
    node("rect", { x: BOX.x, y: BOX.y, width: BOX.w, height: BOX.h, rx: BOX.rx, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7 }, gK);
    node("rect", { x: COUNTER.x, y: COUNTER.y, width: COUNTER.w, height: COUNTER.h, rx: 6, fill: PAL.muted }, gK);
    const bowls = SPOT.counter.map((x) => node("ellipse", { cx: x + 46, cy: COUNTER.y - 6, rx: 30, ry: 12, fill: PAL.bg, stroke: PAL.data, "stroke-width": 5 }, gK));
    const gOven = node("g", {}, svg);
    node("rect", { x: OVEN.x, y: OVEN.y, width: OVEN.w, height: OVEN.h, rx: 10, fill: PAL.bg, stroke: PAL.ink, "stroke-width": 7 }, gOven);
    node("rect", { x: OVEN.x + 16, y: OVEN.y + 60, width: OVEN.w - 32, height: OVEN.h - 76, rx: 6, fill: "none", stroke: PAL.dim, "stroke-width": 5 }, gOven);
    const ovenGlow = node("rect", { x: OVEN.x + 22, y: OVEN.y + 66, width: OVEN.w - 44, height: OVEN.h - 88, rx: 4, fill: PAL.data, "fill-opacity": 0.25 }, gOven);
    [0, 1, 2].forEach((i) => node("circle", { cx: OVEN.x + 30 + i * 30, cy: OVEN.y + 30, r: 8, fill: PAL.dim }, gOven));
    const gAppl = node("g", {}, svg);
    node("rect", { x: APPL.x, y: APPL.y, width: APPL.w, height: APPL.h, rx: 10, fill: PAL.bg, stroke: PAL.ink, "stroke-width": 7 }, gAppl);
    node("rect", { x: APPL.x + 14, y: APPL.y + 14, width: APPL.w - 28, height: 24, rx: 4, fill: PAL.data, "fill-opacity": 0.6 }, gAppl);
    node("circle", { cx: APPL.x + APPL.w - 24, cy: APPL.y + APPL.h - 18, r: 7, fill: PAL.dim }, gAppl);

    // the cooks and their clocks
    // a toque on every cook, in the head group so it tilts with the head (head top sits at y −516 in figure space)
    const toque = (p) => node("path", { d: "M-42 -500 H42 V-526 C62 -562 42 -594 0 -594 C-42 -594 -62 -562 -42 -526 Z",
      fill: PAL.bg, stroke: PAL.ink, "stroke-width": 8, "stroke-linejoin": "round" }, p.headG);
    const cooks = SPOT.counter.map((x) => { const p = C.human(svg, { x, y: FEET, s: FIG }); toque(p); return p; });
    const clocks = cooks.map(() => {
      const g = node("g", {}, svg);
      node("circle", { cx: 0, cy: 0, r: 26, fill: PAL.bg, stroke: PAL.dim, "stroke-width": 5 }, g);
      line(g, 0, 0, 0, -16, ink(5, PAL.dim)); line(g, 0, 0, 11, 0, ink(5, PAL.dim));
      return g;
    });
    // the knife (origin at the grip)
    const knife = node("g", {}, svg);
    const blade = node("path", { d: "M0 0 L0 -34 Q0 -92 14 -108 L22 -108 Q22 -60 18 -34 L18 0 Z", fill: PAL.hero, stroke: PAL.hero, "stroke-width": 3, "stroke-linejoin": "round" }, knife);
    const grip = node("rect", { x: -5, y: 0, width: 28, height: 44, rx: 6, fill: PAL.bg, stroke: PAL.hero, "stroke-width": 6 }, knife);
    const knifeColor = (c) => { blade.setAttribute("fill", c); blade.setAttribute("stroke", c); grip.setAttribute("stroke", c); };

    // labels
    const labK = pair("kitchen", "process", { left: BOX.x, top: 235, width: 400, align: "left" });
    const labKnife = pair("knife", "GIL", { left: 550, top: 235, width: 400, align: "right", color: PAL.hero, color2: PAL.hero });
    const labCooks = pair("cooks", "threads", { left: 380, top: 440, width: 420 });
    const labOven = pair("oven", "I/O", { left: 760, top: 440, width: 190 });
    const labAppl = pair("appliance", "native code", { left: 70, top: 440, width: 340 });

    // bottom zone: code card, timer bar, ghost kitchen
    const code = document.createElement("div");
    code.style.cssText = `position:absolute;left:80px;top:${ZONE.y}px;width:870px;height:190px;border-radius:18px;background:${PAL.panel};` +
      `border:5px solid ${PAL.muted};padding:22px 34px;font-size:60px;line-height:66px;color:${PAL.ink};white-space:pre;`;
    code.style.fontFamily = "monospace";
    root.appendChild(code);
    const CODE = { threads: "for t in threads:\n    t.start()", loader: "DataLoader(ds,\n  num_workers=4)" };
    const timerG = node("g", {}, svg);
    node("rect", { x: 80, y: 1250, width: 870, height: 50, rx: 12, fill: PAL.bg, stroke: PAL.muted, "stroke-width": 5 }, timerG);
    const timerFill = node("rect", { x: 86, y: 1256, width: 0, height: 38, rx: 8, fill: PAL.data }, timerG);
    const timerLab = I.label(root, "work done", { size: 60, left: 80, top: 1178, width: 870, align: "left", color: PAL.dim });
    const ghostG = node("g", {}, svg);
    node("rect", { x: 80, y: 1050, width: 870, height: 250, rx: 28, fill: "none", stroke: PAL.dim, "stroke-width": 6, "stroke-dasharray": "22 18" }, ghostG);
    const labGhost = pair("second kitchen", "another process", { left: 80, top: 1108, width: 870 });

    // the row of kitchens (ep 2), drawn at a home h = ROW_SMALL | ROW_BIG, interpolated by row.big
    const rowG = node("g", {}, svg);
    const rowBoxes = [], rowCounters = [], rowCooks = [], rowKnives = [], rowBowls = [];
    for (let i = 0; i < ROW.n; i++) {
      rowBoxes.push(node("rect", { x: rowX(i), y: 0, width: ROW.w, height: 10, rx: 18, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 6 }, rowG));
      rowCounters.push(node("rect", { x: rowX(i) + 30, y: 0, width: ROW.w - 60, height: 16, rx: 4, fill: PAL.muted }, rowG));
      rowBowls.push(node("ellipse", { cx: rowX(i) + ROW.w / 2 + 26, cy: 0, rx: 18, ry: 8, fill: PAL.bg, stroke: PAL.data, "stroke-width": 4 }, rowG));
      const rc = C.human(rowG, { x: rowX(i) + ROW.w / 2 - 10, y: 0, s: 0.3 }); toque(rc); rowCooks.push(rc);
      const k = node("g", {}, rowG);
      node("path", { d: "M0 0 L0 -20 Q0 -54 8 -64 L13 -64 Q13 -36 11 -20 L11 0 Z", fill: PAL.ink, stroke: PAL.ink, "stroke-width": 2 }, k);
      node("rect", { x: -3, y: 0, width: 17, height: 26, rx: 4, fill: PAL.bg, stroke: PAL.ink, "stroke-width": 4 }, k);
      rowKnives.push(k);
    }
    const labRow = pair("kitchens", "processes", { left: BOX.x, top: 235, width: 500, align: "left" });
    const labRowSmall = pair("more kitchens", "processes", { left: 80, top: 235, width: 870 });   // unused home; kept for the close
    const tag = node("g", {}, svg);
    node("path", { d: "M0 0 L150 0 L190 40 L150 80 L0 80 Z", fill: PAL.bg, stroke: PAL.hero, "stroke-width": 6, "stroke-linejoin": "round" }, tag);
    const tagText = node("text", { x: 72, y: 56, "text-anchor": "middle", "font-size": 60, "font-weight": 800, fill: PAL.hero }, tag);
    tagText.textContent = "$"; tagText.style.fontFamily = "monospace";

    // the wall and the pipe (big row only), the bowl in flight
    const wallG = node("g", {}, svg);
    const wallRect = node("rect", { x: rowX(WALL_I) - ROW.gap - 4, y: ROW_BIG.y - 10, width: ROW.gap + 8, height: ROW_BIG.h + 20, fill: PAL.ink }, wallG);
    const pipeRect = node("rect", { x: PIPE.x0, y: PIPE.y - PIPE.h / 2, width: PIPE.x1 - PIPE.x0, height: PIPE.h, rx: PIPE.h / 2, fill: PAL.bg, stroke: PAL.dim, "stroke-width": 6 }, wallG);
    const labWall = pair("wall", "separate memory", { left: 80, top: ZONE.y + 20, width: 870 });
    const bowlG = node("g", {}, svg);
    const boxRect = node("rect", { x: -34, y: -34, width: 68, height: 68, rx: 8, fill: PAL.bg, stroke: PAL.dim, "stroke-width": 6 }, bowlG);
    node("ellipse", { cx: 0, cy: 0, rx: 26, ry: 11, fill: PAL.bg, stroke: PAL.data, "stroke-width": 5 }, bowlG);

    // the fridge (bottom zone), the note
    const frG = node("g", {}, svg);
    node("rect", { x: FRIDGE.x, y: FRIDGE.y, width: FRIDGE.w, height: FRIDGE.h, rx: 24, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7 }, frG);
    line(frG, FRIDGE.door, FRIDGE.y, FRIDGE.door, FRIDGE.y + FRIDGE.h, ink(6, PAL.dim));
    FRIDGE.shelves.forEach((y) => line(frG, FRIDGE.door + 30, y, FRIDGE.x + FRIDGE.w - 30, y, ink(5, PAL.dim)));
    const shelfNums = FRIDGE.shelves.map((y, i) => { const t = node("text", { x: FRIDGE.x + FRIDGE.w - 44, y: y - 10, "text-anchor": "end", "font-size": 60, "font-weight": 800, fill: PAL.dim }, frG); t.textContent = String(i + 1); t.style.fontFamily = "monospace"; return t; });
    const frBowl = node("ellipse", { cx: 600, cy: FRIDGE.shelves[2] - 10, rx: 28, ry: 12, fill: PAL.bg, stroke: PAL.data, "stroke-width": 5 }, frG);
    const labFridge = pair("fridge", "shared memory", { left: 95, top: FRIDGE.y + 90, width: 310 });
    const noteG = node("g", {}, svg);
    const noteRect = node("rect", { x: -120, y: -42, width: 240, height: 84, rx: 10, fill: PAL.bg, stroke: PAL.hero, "stroke-width": 6 }, noteG);
    const noteText = node("text", { x: 0, y: 20, "text-anchor": "middle", "font-size": 54, "font-weight": 800, fill: PAL.hero }, noteG);
    noteText.textContent = "shelf 3"; noteText.style.fontFamily = "monospace";

    // the close labels
    const labClose1 = pair("waiting", "→ threads", { left: 760, top: 580, width: 190 });   // unused by default; ep1 close uses the oven label
    const closeL = I.label(root, "waiting → threads", { size: 60, left: 80, top: 906, width: 870, align: "center", color: PAL.ink });
    const closeR = I.label(root, "running Python → processes", { size: 60, left: 80, top: 980, width: 870, align: "center", color: PAL.ink });

    // the bowl / note path between kitchen 1 and 2 of the big row: counter 1 → pipe → counter 2
    function pipePath(u) {
      const c1 = [rowX(1) + ROW.w / 2 + 26, ROW_BIG.counter - 14], c2 = [rowX(2) + ROW.w / 2 + 26, ROW_BIG.counter - 14];
      const p0 = [PIPE.x0 + 20, PIPE.y], p1 = [PIPE.x1 - 20, PIPE.y];
      if (u < 0.25) { const v = io(u / 0.25); return [lerp(c1[0], p0[0], v), lerp(c1[1], p0[1], v)]; }
      if (u < 0.75) { const v = (u - 0.25) / 0.5; return [lerp(p0[0], p1[0], v), PIPE.y]; }
      const v = io((u - 0.75) / 0.25); return [lerp(p1[0], c2[0], v), lerp(p1[1], c2[1], v)];
    }

    function draw(g, S) {
      const chop = S.chop || 0;
      // kitchen
      opac(gK, S.K.o); labK.set(S.K.lab * S.K.o);
      opac(gOven, S.oven.o * S.K.o); labOven.set(S.oven.lab * S.oven.o * S.K.o);
      opac(gAppl, S.appl.o * S.K.o); labAppl.set(S.appl.lab * S.appl.o * S.K.o);
      labCooks.set(S.cooksLab * S.K.o);
      labKnife.set(S.knife.lab * S.K.o, S.knife.hero);
      ovenGlow.setAttribute("fill-opacity", S.cooks.some((c) => c.at === "oven") ? 0.35 : 0.12);
      // cooks
      cooks.forEach((p, i) => {
        const c = S.cooks[i];
        const x = c.at === "oven" ? SPOT.oven : c.at === "appl" ? SPOT.appl : SPOT.counter[i];
        C.place(p, x, FEET, FIG);
        C.show(p, S.K.o);
        const holds = S.knife.holder === i;
        const pose = { armL: 22, armR: 22, lean: 0, tilt: 0 };
        if (holds) { pose.armR = 70 + 28 * Math.sin(Math.PI * chop); pose.lean = -3; }
        else if (c.at === "oven") { pose.armR = 48; pose.lean = 4; }
        else if (c.at === "appl") { pose.armL = 64 + 10 * Math.sin(Math.PI * chop); pose.lean = -4; }
        C.pose(p, pose);
        C.face(p, c.wait ? "flat" : "smile");
        p.el.setAttribute("stroke-opacity", 1);
        const dim = !holds && c.at === "counter" && c.wait;
        p.el.setAttribute("opacity", S.K.o * (dim ? 0.55 : 1));
        opac(clocks[i], c.wait * S.K.o);
        clocks[i].setAttribute("transform", `translate(${x + 70} ${FEET - 262})`);
        bowls[i].setAttribute("opacity", c.at === "counter" ? 1 : 0.25);
      });
      // knife
      if (S.knife.holder >= 0) {
        const h = C.hand(cooks[S.knife.holder], 1);
        knife.setAttribute("transform", `translate(${h[0]} ${h[1]}) rotate(${-20 + 35 * Math.sin(Math.PI * chop)}) scale(0.85)`);
      } else knife.setAttribute("transform", `translate(540 ${COUNTER.y - 8}) rotate(-90) scale(0.9)`);
      opac(knife, S.K.o);
      knifeColor(S.knife.hero ? PAL.hero : PAL.ink);
      // bottom zone
      code.textContent = CODE[S.code.text] || "";
      domOpac(code, S.code.o);
      opac(timerG, S.timer.o); domOpac(timerLab, S.timer.o);
      timerFill.setAttribute("width", Math.max(0, 858 * clamp01(S.timer.fill)));
      opac(ghostG, S.ghost.o); labGhost.set(S.ghost.o);
      // the row
      const R = S.row, home = { y: lerp(ROW_SMALL.y, ROW_BIG.y, R.big), h: lerp(ROW_SMALL.h, ROW_BIG.h, R.big),
                                fig: lerp(ROW_SMALL.fig, ROW_BIG.fig, R.big), feet: lerp(ROW_SMALL.feet, ROW_BIG.feet, R.big),
                                counter: lerp(ROW_SMALL.counter, ROW_BIG.counter, R.big) };
      opac(rowG, R.o);
      for (let i = 0; i < ROW.n; i++) {
        rowBoxes[i].setAttribute("y", home.y); rowBoxes[i].setAttribute("height", home.h);
        rowCounters[i].setAttribute("y", home.counter);
        rowBowls[i].setAttribute("cy", home.counter - 4);
        const p = rowCooks[i];
        C.place(p, rowX(i) + ROW.w / 2 - 10, home.feet, home.fig);
        C.pose(p, { armL: 22, armR: 70 + 28 * Math.sin(Math.PI * chop) * R.chop, lean: -3, tilt: 0 });
        const h = C.hand(p, 1);
        rowKnives[i].setAttribute("transform", `translate(${h[0]} ${h[1]}) rotate(${-20 + 35 * Math.sin(Math.PI * chop) * R.chop}) scale(${home.fig / 0.42})`);
        rowKnives[i].querySelectorAll && Array.from(rowKnives[i].querySelectorAll("*")).forEach((el, k) => {
          const c = R.hero ? PAL.hero : PAL.ink;
          if (k === 0) { el.setAttribute("fill", c); el.setAttribute("stroke", c); } else el.setAttribute("stroke", c);
        });
      }
      labRow.set(R.lab * R.o);
      opac(tag, S.tag.o); tag.setAttribute("transform", `translate(${rowX(3) + ROW.w - 196} ${ROW_SMALL.y + 12})`);
      // the wall, the pipe, the bowl
      opac(wallG, S.wall.o * R.o); labWall.set(S.wall.lab * S.wall.o);
      const bp = pipePath(S.wall.bowl);
      bowlG.setAttribute("transform", `translate(${bp[0]} ${bp[1]})`);
      opac(bowlG, S.wall.bowlO * S.wall.o);
      opac(boxRect, S.wall.boxed);
      // the fridge, the note
      opac(frG, S.fridge.o); labFridge.set(S.fridge.lab * S.fridge.o);
      opac(frBowl, S.fridge.bowl);
      shelfNums[2].setAttribute("fill", S.fridge.note > 0 ? PAL.hero : PAL.dim);
      const np = pipePath(S.fridge.note);
      noteG.setAttribute("transform", `translate(${np[0]} ${np[1] - 60}) scale(${S.fridge.noteHero ? 1 : 0.8})`);
      opac(noteG, S.fridge.noteO * S.fridge.o);
      const nc = S.fridge.noteHero ? PAL.hero : PAL.dim;
      noteRect.setAttribute("stroke", nc); noteText.setAttribute("fill", nc);
      // the close
      domOpac(closeL, S.close.o * S.K.o);
      domOpac(closeR, S.close.o * (S.ghost.o || (R.o && !R.big ? 1 : 0)));
      labClose1.set(0);
      labRowSmall.set(0);
    }
    return { draw, svg, cooks, knife, labels: { labK, labKnife, labCooks, labOven, labAppl, labRow, labWall, labFridge, labGhost }, code, timerFill, bowlG, noteG, rowCooks, rowKnives, tag };
  }

  window.SC = { PAL, BOX, FEET, FIG, SPOT, OVEN, APPL, ZONE, ROW, ROW_SMALL, ROW_BIG, PIPE, FRIDGE,
                REST, SEAM1, SEAM2, state, merge, mount, lerp, clamp01, seg, io, pulse,
                SEAM: SEAM1 };   // beats set SC.SEAM = SC.SEAM1 or SC.SEAM2 before mounting (hf_state_check reads SC.SEAM)
})();
