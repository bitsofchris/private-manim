// kitchen.js — the 015 kit, second pass (v1 is kitchen_v1.js) (Chris, 10/29: "build the scene
// sequentially, go back and forth with a Python view, make the knife crisp
// and have the cooks actually cut something"). Loaded by every beat of both
// episodes through its `kit` symlink, BEFORE cast/cast.js (it shims
// createElementNS for tools/hf_state_check.js, whose stub DOM lacks it).
//
// Two views on one frame, the kitchen above and the Python panel below:
//   kitchen   y 380–900   the box draws in, the cooks walk in, the knife lands,
//                         the oven and the appliance appear when named; at the
//                         close it shrinks to half size, left, and a second
//                         kitchen (S.twin, the same drawing) runs at right
//   panel     y 965–1300  `$ python main.py`, then one `Thread(...)` line per
//                         cook, then the same four rows as a thread timeline:
//                         magenta bars = running Python (the knife), dashed
//                         bars = waiting on I/O, teal = native code; at the
//                         close it splits into "process 1" / "process 2" halves
//   labels    y 235–367   "kitchen / process" top-left (stays), one slot
//                         top-right that shows the thing just named
//   chip      y 450       one line of code inside the kitchen (requests.get(url) …)
//   close     y 690/780   "waiting → threads", "running Python → processes"
//
// The knife: a chef's knife with the tip resting on the cutting board; the
// handle rocks in the holder's hand (S.chop), the carrot under the blade
// shortens and slices pile up left of the tip (cooks[i].cut). Pure
// functions of their arguments: no clocks, no randomness.
//   const k = SC.mount(root); k.draw(null, S)   // S = SC.state(SC.SEAM[n], patch)
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
  function merge(a, b) {
    const out = copy(a || {});
    Object.keys(b || {}).forEach((k) => {
      out[k] = b[k] && typeof b[k] === "object" && !Array.isArray(b[k]) && out[k] && typeof out[k] === "object" && !Array.isArray(out[k])
        ? merge(out[k], b[k]) : copy(b[k]);
    });
    return out;
  }
  // A chop phase that is 0 at t = 0 and at t = end (so seams are still): `rate` chops per second.
  const chopAt = (t, from, to, rate = 2) => { if (t <= from || t >= to) return 0; const n = Math.max(1, Math.round((to - from) * rate)); return ((t - from) * n / (to - from)) % 1; };

  // ---- geometry ----
  const BOX = { x: 80, y: 380, w: 870, h: 520, rx: 28 };
  const FEET = 880, FIG = 0.48;                       // cooks ~250 px tall
  const COUNTER = { x: 290, y: 800, w: 520, h: 25 };   // hip height (Chris, 10/29: higher looked like the knife at the neck)
  const BOARD = { x: 300, y: 782, w: 500, h: 18 };
  const SPOT = { counter: [370, 500, 630, 760], oven: 812, appl: 262, off: -140 };
  const TIP = -80;                                    // the cut point, left of the cook's centre
  const KNIFE_L = 150;                                // tip → end of the grip, at scale 1
  const OVEN = { x: 846, y: 660, w: 96, h: 180 };
  const APPL = { x: 96, y: 760, w: 110, h: 80 };
  const PANEL = { x: 80, y: 965, w: 870, h: 335, title: 975, row0: 1050, pitch: 64, barX: 400, barX1: 930, barH: 44 };
  const HALF = 0.48;                                  // the kitchens' scale at the close (two fit side by side with a gap)
  const TWIN = { x: 532, y: 380 };                    // where the second kitchen's top-left lands at the close
  const PANEL2 = { x: 525, w: 425, barX: 675 };        // the right half panel; the left half keeps PANEL.x with SPLIT bars
  const SPLIT = { w: 425, barX: 230, barX1: 485 };
  const CLOSE_Y = [690, 780];

  // ---- the state ----
  const REST = {
    K: { o: 0, draw: 1, lab: 0, half: 0 },            // draw: the outline drawn in 0..1; half: 1 = half size, left
    cooks: [0, 1, 2, 3].map(() => ({ in: 0, at: "counter", u: 1, wait: 0, cut: 0 })),   // in: walked in 0..1; u: walked to `at`
    veg: 0,                                           // the carrots on the board
    knife: { o: 0, holder: -1, hero: 1 },             // holder −1: on the board; fractional: between hands
    oven: { o: 0, ding: 0 }, appl: { o: 0 },         // ding: the oven flashes (the wait is over)
    slot: { o: 0, top: "", bottom: "", hero: 0 },     // the top-right label
    chip: { o: 0, text: "" },                         // the code line inside the kitchen
    panel: { o: 0, title: 0, code: 0, lanes: 0, rows: [[], [], [], []], pulse: { py: 0, io: 0 }, core: 0, split: 0 },
    //   code: how many Thread lines (0..4, fractional fades the last); lanes: code lines → timeline rows;
    //   rows[i]: [{ a, b, k }] bars from a to b (0..1 of the lane) of kind "py" | "io" | "nat"; core: the "= 1 core" tag on the title row
    //   split: 0 = one wide panel, 1 = two halves ("process 1" with `rows`, "process 2" with panel2.rows)
    panel2: { rows: [[], [], [], []] },
    twin: { o: 0, draw: 1, cooks: [0, 1, 2, 3].map(() => ({ in: 0, at: "counter", u: 1, wait: 0, cut: 0 })),   // the second kitchen
            veg: 0, knife: { o: 0, holder: -1, hero: 1 }, oven: { o: 0, ding: 0 }, appl: { o: 0 }, chop: 0 },
    close: { a: 0, b: 0 },
    chop: 0,
  };
  const state = (base, patch) => merge(merge(REST, base || {}), patch || {});
  function tween(A, B, u) {
    if (typeof A === "number" && typeof B === "number") return lerp(A, B, u);
    if (Array.isArray(B)) return B.map((b, i) => tween(A ? A[i] : undefined, b, u));
    if (B && typeof B === "object") { const o = {}; for (const k of Object.keys(B)) o[k] = tween(A ? A[k] : undefined, B[k], u); return o; }
    return B;
  }
  const cooksAt = (list) => list.map(([at, wait, cut, u]) => ({ in: 1, at, u: u === undefined ? 1 : u, wait, cut }));
  const SLOT = {
    cooks: { o: 1, top: "cooks", bottom: "threads", hero: 0 },
    counter: { o: 1, top: "counter", bottom: "shared memory", hero: 0 },
    knife: { o: 1, top: "knife", bottom: "GIL", hero: 1 },
    oven: { o: 1, top: "oven", bottom: "I/O", hero: 0 },
    appl: { o: 1, top: "appliance", bottom: "native code", hero: 0 },
    twin: { o: 1, top: "second kitchen", bottom: "another process", hero: 0 },
  };
  const STAIR = [[{ a: 0, b: 0.25, k: "py" }], [{ a: 0.25, b: 0.5, k: "py" }], [{ a: 0.5, b: 0.75, k: "py" }], [{ a: 0.75, b: 1, k: "py" }]];
  // Thread 2 waits (dashed), Thread 3 runs meanwhile, the oven dings and Thread 2 gets the knife back (magenta again).
  const OVEN_ROWS = [[], [{ a: 0, b: 0.55, k: "io" }, { a: 0.6, b: 0.64, k: "py" }], [{ a: 0.15, b: 0.55, k: "py" }], []];
  const APPL_ROWS = [[], [{ a: 0, b: 0.55, k: "io" }, { a: 0.6, b: 1, k: "py" }], [{ a: 0.15, b: 0.55, k: "py" }], [{ a: 0.7, b: 1, k: "nat" }]];
  // At the close the left half keeps those rows at half width and keeps growing while process 2's Thread 1 grows beside it.
  const CLOSE_ROWS = [[], [{ a: 0, b: 0.275, k: "io" }, { a: 0.3, b: 0.75, k: "py" }], [{ a: 0.075, b: 0.275, k: "py" }], [{ a: 0.35, b: 0.75, k: "nat" }]];
  const CLOSE_ROWS2 = [[{ a: 0.5, b: 0.75, k: "py" }], [], [], []];
  const TWIN_COOKS = cooksAt([["counter", 0, 0.3], ["counter", 1, 0], ["counter", 1, 0], ["counter", 1, 0]]);
  const KIT = { K: { o: 1, lab: 1 }, panel: { o: 1, title: 1, code: 4 } };
  // Episode 1 cuts (beat n ends / beat n+1 starts); SEAM1[0] is frame 0.
  const SEAM1 = {
    0: state({ panel: { o: 1, title: 1 } }),
    1: state(KIT, { cooks: cooksAt([["counter", 0, 0], ["counter", 0, 0], ["counter", 0, 0], ["counter", 0, 0]]), veg: 1, slot: SLOT.counter }),
    2: state(KIT, { cooks: cooksAt([["counter", 0, 0.5], ["counter", 1, 0], ["counter", 1, 0], ["counter", 1, 0]]), veg: 1, slot: SLOT.knife,
                    knife: { o: 1, holder: 0 }, panel: { lanes: 1, rows: [[{ a: 0, b: 0.5, k: "py" }], [], [], []] } }),
    3: state(KIT, { cooks: cooksAt([["counter", 1, 0.5], ["counter", 1, 0.5], ["counter", 1, 0.5], ["counter", 0, 0.5]]), veg: 1, slot: SLOT.knife,
                    knife: { o: 1, holder: 3 }, panel: { lanes: 1, rows: STAIR } }),
    4: state(KIT, { cooks: cooksAt([["counter", 1, 0.5], ["counter", 0, 0.5], ["counter", 1, 0.8], ["counter", 1, 0.5]]), veg: 1, slot: SLOT.oven,
                    knife: { o: 1, holder: 1 }, oven: { o: 1 }, panel: { lanes: 1, rows: OVEN_ROWS } }),
    5: state(KIT, { cooks: cooksAt([["counter", 1, 0.5], ["counter", 0, 0.8], ["counter", 1, 0.8], ["appl", 0, 0.5]]), veg: 1, slot: SLOT.appl,
                    knife: { o: 1, holder: 1 }, oven: { o: 1 }, appl: { o: 1 }, chip: { o: 1, text: "tokenizer(text)" }, panel: { lanes: 1, rows: APPL_ROWS } }),
    6: state(KIT, { K: { half: 1 }, cooks: cooksAt([["counter", 1, 0.5], ["counter", 0, 1], ["counter", 1, 0.8], ["appl", 0, 0.5]]), veg: 1, slot: SLOT.twin,
                    knife: { o: 1, holder: 1 }, oven: { o: 1 }, appl: { o: 1 }, panel: { lanes: 1, split: 1, rows: CLOSE_ROWS }, panel2: { rows: CLOSE_ROWS2 },
                    twin: { o: 1, draw: 1, cooks: TWIN_COOKS, veg: 1, knife: { o: 1, holder: 0 } }, close: { a: 1, b: 1 } }),
  };
  // Prototype frames (00_layout and the review sheet): the seam states plus the moments between them.
  const PROTO = [
    SEAM1[0],
    state({ K: { o: 1, lab: 1 }, panel: { o: 1, title: 1 } }),
    state(KIT, { cooks: [{ in: 1, at: "counter", u: 1, wait: 0, cut: 0 }, { in: 1, at: "counter", u: 1, wait: 0, cut: 0 }, { in: 0.6, at: "counter", u: 1, wait: 0, cut: 0 }, { in: 0.2, at: "counter", u: 1, wait: 0, cut: 0 }], slot: SLOT.cooks, panel: { code: 2.6 } }),
    SEAM1[1],
    state(KIT, { cooks: cooksAt([["counter", 0, 0], ["counter", 0, 0], ["counter", 0, 0], ["counter", 0, 0]]), veg: 1, slot: SLOT.knife, knife: { o: 1, holder: -1 }, panel: { lanes: 1 } }),
    state(KIT, { cooks: cooksAt([["counter", 0, 0.3], ["counter", 0.6, 0], ["counter", 0.6, 0], ["counter", 0.6, 0]]), veg: 1, slot: SLOT.knife, knife: { o: 1, holder: 0 }, panel: { lanes: 1, rows: [[{ a: 0, b: 0.3, k: "py" }], [], [], []] } }),
    state(KIT, { cooks: cooksAt([["counter", 1, 0.5], ["counter", 1, 0.5], ["counter", 0, 0.12], ["counter", 1, 0]]), veg: 1, slot: SLOT.knife, knife: { o: 1, holder: 2 },
                 panel: { lanes: 1, rows: [[{ a: 0, b: 0.25, k: "py" }], [{ a: 0.25, b: 0.5, k: "py" }], [{ a: 0.5, b: 0.62, k: "py" }], []] } }),
    SEAM1[3],
    state(KIT, { cooks: cooksAt([["counter", 1, 0.5], ["oven", 0, 0.5], ["counter", 1, 0.5], ["counter", 1, 0.5]]), veg: 1, slot: SLOT.oven, knife: { o: 1, holder: -1 }, oven: { o: 1 },
                 chip: { o: 1, text: "requests.get(url)" }, panel: { lanes: 1, rows: [[], [{ a: 0, b: 0.4, k: "io" }], [], []] } }),
    state(KIT, { cooks: cooksAt([["counter", 1, 0.5], ["oven", 0, 0.5, 0.5], ["counter", 0, 0.8], ["counter", 1, 0.5]]), veg: 1, slot: SLOT.oven, knife: { o: 1, holder: 2 }, oven: { o: 1, ding: 1 },
                 panel: { lanes: 1, rows: [[], [{ a: 0, b: 0.55, k: "io" }], [{ a: 0.15, b: 0.5, k: "py" }], []] } }),   // the oven dings, cook 2 walks back
    SEAM1[4],
    SEAM1[5],
    state(KIT, { K: { half: 1 }, cooks: cooksAt([["counter", 1, 0.5], ["counter", 0, 0.9], ["counter", 1, 0.8], ["appl", 0, 0.5]]), veg: 1, slot: SLOT.twin,
                 knife: { o: 1, holder: 1 }, oven: { o: 1 }, appl: { o: 1 }, panel: { lanes: 1, split: 1, rows: CLOSE_ROWS }, close: { a: 1, b: 1 },
                 twin: { o: 1, draw: 1, cooks: [{ in: 1, at: "counter", u: 1, wait: 0, cut: 0 }, { in: 0.7, at: "counter", u: 1, wait: 0, cut: 0 }, { in: 0.4, at: "counter", u: 1, wait: 0, cut: 0 }, { in: 0.1, at: "counter", u: 1, wait: 0, cut: 0 }], veg: 1 } }),   // the second kitchen fills
    SEAM1[6],
  ];

  // ---- drawing ----
  function mount(root) {
    const C = window.CAST, I = window.ISO;
    const svg = C.layer(root);
    const node = C.node, line = C.line;
    const opac = (el, a) => { el.setAttribute("opacity", clamp01(a)); el.setAttribute("visibility", a > 0.001 ? "visible" : "hidden"); };
    const domOpac = (el, a) => { el.style.opacity = clamp01(a); el.style.visibility = a > 0.001 ? "visible" : "hidden"; };
    const mono = (el) => { el.style.fontFamily = "monospace"; return el; };
    function pair(top, bottom, o) {
      const a = I.label(root, top, { size: 60, left: o.left, top: o.top, width: o.width, align: o.align || "center", color: o.color || PAL.ink });
      const b = I.label(root, bottom, { size: 60, left: o.left, top: o.top + 66, width: o.width, align: o.align || "center", color: o.color2 || PAL.dim });
      const set = (alpha, hero) => { [a, b].forEach((el) => domOpac(el, alpha)); if (hero !== undefined) { a.style.color = hero ? PAL.hero : (o.color || PAL.ink); b.style.color = hero ? PAL.hero : (o.color2 || PAL.dim); } };
      set(0);
      return { a, b, set };
    }

    // ---- one kitchen: box, counter, oven, appliance, carrots, four cooks, the knife (built twice: main and twin) ----
    function kitchen(id) {
      const g = node("g", {}, svg);
      // clipped at the box, so a cook walking in from off-left appears through the wall
      const clip = node("clipPath", { id }, g);
      node("rect", { x: BOX.x - 4, y: 0, width: 1080, height: 1920 }, clip);
      g.setAttribute("clip-path", `url(#${id})`);
      const boxEl = node("rect", { x: BOX.x, y: BOX.y, width: BOX.w, height: BOX.h, rx: BOX.rx, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7, pathLength: 1 }, g);
      const gCounter = node("g", {}, g);
      node("rect", { x: COUNTER.x, y: COUNTER.y, width: COUNTER.w, height: COUNTER.h, rx: 6, fill: PAL.muted }, gCounter);
      node("rect", { x: BOARD.x, y: BOARD.y, width: BOARD.w, height: BOARD.h, rx: 5, fill: PAL.bg, stroke: PAL.dim, "stroke-width": 4 }, gCounter);
      const gOven = node("g", {}, g);
      node("rect", { x: OVEN.x, y: OVEN.y, width: OVEN.w, height: OVEN.h, rx: 10, fill: PAL.bg, stroke: PAL.ink, "stroke-width": 7 }, gOven);
      node("rect", { x: OVEN.x + 16, y: OVEN.y + 60, width: OVEN.w - 32, height: OVEN.h - 76, rx: 6, fill: "none", stroke: PAL.dim, "stroke-width": 5 }, gOven);
      const ovenGlow = node("rect", { x: OVEN.x + 22, y: OVEN.y + 66, width: OVEN.w - 44, height: OVEN.h - 88, rx: 4, fill: PAL.data, "fill-opacity": 0.25 }, gOven);
      [0, 1, 2].forEach((i) => node("circle", { cx: OVEN.x + 24 + i * 24, cy: OVEN.y + 30, r: 8, fill: PAL.dim }, gOven));
      // the appliance: a food processor, a jar on a base
      const gAppl = node("g", {}, g);
      node("rect", { x: APPL.x, y: APPL.y + 40, width: APPL.w, height: APPL.h - 40, rx: 10, fill: PAL.bg, stroke: PAL.ink, "stroke-width": 7 }, gAppl);
      node("path", { d: `M${APPL.x + 24} ${APPL.y + 40} L${APPL.x + 18} ${APPL.y - 40} H${APPL.x + 102} L${APPL.x + 96} ${APPL.y + 40} Z`, fill: PAL.bg, stroke: PAL.ink, "stroke-width": 6, "stroke-linejoin": "round" }, gAppl);
      const applBlades = node("path", { d: `M${APPL.x + 36} ${APPL.y + 14} H${APPL.x + 84} M${APPL.x + 60} ${APPL.y - 10} V${APPL.y + 38}`, stroke: PAL.data, "stroke-width": 6, "stroke-linecap": "round" }, gAppl);
      node("circle", { cx: APPL.x + APPL.w - 24, cy: APPL.y + APPL.h - 20, r: 7, fill: PAL.dim }, gAppl);
      // the carrots and their slices, one set per cook, drawn before the cooks
      const gVeg = node("g", {}, g);
      const carrots = SPOT.counter.map((x) => node("rect", { x: x + TIP, y: BOARD.y - 20, width: 70, height: 20, rx: 10, fill: PAL.data }, gVeg));
      const slices = SPOT.counter.map((x) => [0, 1, 2, 3, 4, 5, 6, 7].map((k) => node("circle", { cx: x + TIP - 16 - 14 * (k % 4), cy: BOARD.y - 10 - 18 * Math.floor(k / 4), r: 9, fill: PAL.data }, gVeg)));
      // the cooks, toques on
      const toque = (p) => node("path", { d: "M-42 -500 H42 V-526 C62 -562 42 -594 0 -594 C-42 -594 -62 -562 -42 -526 Z",
        fill: PAL.bg, stroke: PAL.ink, "stroke-width": 8, "stroke-linejoin": "round" }, p.headG);
      const cooks = SPOT.counter.map((x) => { const p = C.human(g, { x, y: FEET, s: FIG }); toque(p); return p; });
      // the knife: tip at the origin, the blade along +x to the heel at 100, bolster, grip to 150
      const knife = node("g", {}, g);
      const blade = node("path", { d: "M0 0 C40 -4 72 -16 100 -34 L100 0 Z", fill: PAL.hero, stroke: PAL.hero, "stroke-width": 3, "stroke-linejoin": "round" }, knife);
      const bolster = node("rect", { x: 98, y: -38, width: 14, height: 42, rx: 3, fill: PAL.hero }, knife);
      const grip = node("rect", { x: 110, y: -28, width: 42, height: 22, rx: 7, fill: PAL.bg, stroke: PAL.hero, "stroke-width": 6 }, knife);
      const knifeColor = (c) => { blade.setAttribute("fill", c); blade.setAttribute("stroke", c); bolster.setAttribute("fill", c); grip.setAttribute("stroke", c); };

      // Sk: { o, draw, cooks, veg, knife, oven, appl, chop }; transform: the group's placement
      function drawK(Sk, transform) {
        const chop = Sk.chop || 0;
        g.setAttribute("transform", transform);
        opac(g, Sk.o);
        boxEl.setAttribute("stroke-dasharray", "1"); boxEl.setAttribute("stroke-dashoffset", 1 - clamp01(Sk.draw));
        boxEl.setAttribute("fill-opacity", clamp01(Sk.draw));
        opac(gCounter, Sk.draw >= 0.999 ? 1 : 0);
        opac(gOven, Sk.oven.o); opac(gAppl, Sk.appl.o);
        const atOven = Sk.cooks.some((c) => c.at === "oven" && c.u >= 0.999);
        ovenGlow.setAttribute("fill-opacity", lerp(atOven ? 0.4 : 0.12, 0.95, clamp01(Sk.oven.ding || 0)));
        applBlades.setAttribute("transform", `rotate(${Sk.cooks.some((c) => c.at === "appl" && c.u >= 0.999) ? 180 * chop : 0} ${APPL.x + 60} ${APPL.y + 14})`);
        opac(gVeg, Sk.veg);
        // the cooks
        let holderHand = null;
        cooks.forEach((p, i) => {
          const c = Sk.cooks[i], w = clamp01(c.wait || 0), inn = clamp01(c.in === undefined ? 1 : c.in), u = clamp01(c.u === undefined ? 1 : c.u);
          const target = c.at === "oven" ? SPOT.oven : c.at === "appl" ? SPOT.appl : SPOT.counter[i];
          const x = inn < 1 ? lerp(SPOT.off, SPOT.counter[i], io(inn)) : lerp(SPOT.counter[i], target, u);
          const bob = inn < 1 ? 6 * Math.abs(Math.sin(Math.PI * 4 * inn)) : 0;
          C.place(p, x, FEET - bob, FIG);
          C.show(p, 1);
          const h = Sk.knife.holder, holds = h >= 0 && Math.abs(h - i) < 0.5 && c.at === "counter";
          const there = u >= 0.999;
          const pose = { armL: 22, armR: 22, lean: 0, tilt: 0 };
          if (holds) { pose.armR = 24 + 22 * Math.sin(Math.PI * chop); pose.armL = 36; pose.lean = -3; }
          else if (c.at === "oven" && there) { pose.armR = 48; pose.lean = 4; }
          else if (c.at === "appl" && there) { pose.armL = 70 + 10 * Math.sin(Math.PI * chop); pose.lean = -4; }
          else if (inn < 1) { pose.armL = 30 + 14 * Math.sin(Math.PI * 4 * inn); pose.armR = 30 - 14 * Math.sin(Math.PI * 4 * inn); }
          else { pose.armL = lerp(22, -56, w); pose.armR = lerp(22, -56, w); pose.tilt = 9 * w; }   // waiting: arms folded, head tipped
          C.pose(p, pose);
          C.face(p, w >= 0.5 ? "flat" : "smile");
          const dim = !holds && c.at === "counter" ? w : 0;
          p.el.setAttribute("opacity", lerp(1, 0.4, dim));
          // the carrot and the slices
          const cut = clamp01(c.cut || 0);
          carrots[i].setAttribute("width", Math.max(0, 70 * (1 - cut)));
          carrots[i].setAttribute("opacity", cut >= 0.999 ? 0 : 1);
          slices[i].forEach((el, k) => el.setAttribute("opacity", k < Math.floor(cut * 7.999) ? 1 : 0));
          if (holds) holderHand = { i, hand: C.hand(p, 1) };
        });
        // the knife: between hands while the holder is fractional, else pivoting on the tip in the holder's hand
        const h = Sk.knife.holder;
        if (h >= 0 && Math.abs(h - Math.round(h)) > 0.001) {
          const a = Math.floor(h), b = Math.min(cooks.length - 1, Math.ceil(h)), v = h - a;
          const ha = C.hand(cooks[a], 1), hb = C.hand(cooks[b], 1), lift = 90 * Math.sin(Math.PI * v);
          const hx = lerp(ha[0], hb[0], io(v)), hy = lerp(ha[1], hb[1], io(v)) - lift;
          knife.setAttribute("transform", `translate(${hx - 120} ${hy + 10}) rotate(${-10 - 20 * Math.sin(Math.PI * v)}) scale(0.85)`);
        } else if (holderHand) {
          const tip = [SPOT.counter[holderHand.i] + TIP, BOARD.y], H = holderHand.hand;
          const dx = H[0] - tip[0], dy = H[1] - tip[1];
          const th = Math.atan2(dy, dx) * 180 / Math.PI, d = Math.hypot(dx, dy);
          knife.setAttribute("transform", `translate(${tip[0]} ${tip[1]}) rotate(${th}) scale(${d / KNIFE_L})`);
        } else knife.setAttribute("transform", `translate(${SPOT.counter[1] + TIP + 30} ${BOARD.y}) rotate(0) scale(0.85)`);   // on the board
        opac(knife, Sk.knife.o);
        knifeColor(Sk.knife.hero ? PAL.hero : PAL.ink);
      }
      return { g, cooks, knife, drawK };
    }
    const main = kitchen("kitClipMain");
    const twin = kitchen("kitClipTwin");

    // ---- labels ----
    const labK = pair("kitchen", "process", { left: BOX.x, top: 235, width: 420, align: "left" });
    const slot = pair("", "", { left: 440, top: 235, width: 510, align: "right" });
    const chip = mono(I.label(root, "", { size: 60, left: 100, top: 450, width: 830, align: "center", color: PAL.ink }));
    const closeA = I.label(root, "", { size: 60, left: 80, top: CLOSE_Y[0], width: 870, align: "center", color: PAL.ink });
    closeA.innerHTML = `<span style="color:${PAL.dim}">waiting</span> → threads`;
    const closeB = I.label(root, "", { size: 60, left: 80, top: CLOSE_Y[1], width: 870, align: "center", color: PAL.ink });
    closeB.innerHTML = `<span style="color:${PAL.hero}">running Python</span> → processes`;

    // ---- the Python panel (one wide panel that splits into two halves at the close) ----
    const gPanel = node("g", {}, svg);
    const panelBox = node("rect", { x: PANEL.x, y: PANEL.y, width: PANEL.w, height: PANEL.h, rx: 18, fill: PAL.panel, stroke: PAL.muted, "stroke-width": 5 }, gPanel);
    const title = mono(I.label(root, "$ python main.py", { size: 60, left: PANEL.x + 30, top: PANEL.title, width: 810, align: "left", color: PAL.ink }));
    const title1 = mono(I.label(root, "process 1", { size: 60, left: PANEL.x + 30, top: PANEL.title, width: SPLIT.w - 60, align: "left", color: PAL.ink }));
    const coreTag = I.label(root, "= 1 core", { size: 60, left: PANEL.x + 30, top: PANEL.title, width: 810, align: "right", color: PAL.hero });
    const rowY = (i) => PANEL.row0 + i * PANEL.pitch;
    const codeLines = [0, 1, 2, 3].map((i) => mono(I.label(root, "Thread(target=chop)", { size: 60, left: PANEL.x + 30, top: rowY(i), width: 810, align: "left", color: PAL.dim })));
    const laneLabs = [0, 1, 2, 3].map((i) => mono(I.label(root, `Thread ${i + 1}`, { size: 60, left: PANEL.x + 30, top: rowY(i), width: 300, align: "left", color: PAL.dim })));
    const shortLabs = [0, 1, 2, 3].map((i) => mono(I.label(root, `T${i + 1}`, { size: 60, left: PANEL.x + 30, top: rowY(i), width: 120, align: "left", color: PAL.dim })));
    const laneLines = [0, 1, 2, 3].map((i) => line(gPanel, PANEL.barX, rowY(i) + 36, PANEL.barX1, rowY(i) + 36, { stroke: PAL.muted, "stroke-width": 4, "stroke-dasharray": "6 10" }));
    const BARS = 4;
    const bars = [0, 1, 2, 3].map((i) => Array.from({ length: BARS }, () => node("rect", { x: 0, y: rowY(i) + 36 - PANEL.barH / 2, width: 0, height: PANEL.barH, rx: 8 }, gPanel)));
    // the right half: "process 2"
    const gPanel2 = node("g", {}, svg);
    node("rect", { x: PANEL2.x, y: PANEL.y, width: PANEL2.w, height: PANEL.h, rx: 18, fill: PAL.panel, stroke: PAL.muted, "stroke-width": 5 }, gPanel2);
    const title2 = mono(I.label(root, "process 2", { size: 60, left: PANEL2.x + 30, top: PANEL.title, width: PANEL2.w - 60, align: "left", color: PAL.ink }));
    const shortLabs2 = [0, 1, 2, 3].map((i) => mono(I.label(root, `T${i + 1}`, { size: 60, left: PANEL2.x + 30, top: rowY(i), width: 120, align: "left", color: PAL.dim })));
    [0, 1, 2, 3].forEach((i) => line(gPanel2, PANEL2.barX, rowY(i) + 36, PANEL.barX1, rowY(i) + 36, { stroke: PAL.muted, "stroke-width": 4, "stroke-dasharray": "6 10" }));
    const bars2 = [0, 1, 2, 3].map((i) => Array.from({ length: BARS }, () => node("rect", { x: 0, y: rowY(i) + 36 - PANEL.barH / 2, width: 0, height: PANEL.barH, rx: 8 }, gPanel2)));
    const barStyle = (el, k, pu) => {
      if (k === "py") { el.setAttribute("fill", PAL.hero); el.setAttribute("stroke", "none"); el.setAttribute("fill-opacity", lerp(0.9, 1, pu.py)); el.setAttribute("transform", ""); }
      else if (k === "io") { el.setAttribute("fill", PAL.bg); el.setAttribute("stroke", PAL.dim); el.setAttribute("stroke-width", lerp(5, 8, pu.io)); el.setAttribute("stroke-dasharray", "14 10"); el.setAttribute("fill-opacity", 1); }
      else { el.setAttribute("fill", PAL.data); el.setAttribute("stroke", "none"); el.setAttribute("fill-opacity", 0.9); }
    };
    const drawRows = (els, rows, x0, x1, pu, alpha) => els.forEach((row, i) => row.forEach((el, k) => {
      const sg = (rows[i] || [])[k];
      if (!sg || sg.b <= sg.a) { opac(el, 0); return; }
      const xa = lerp(x0, x1, clamp01(sg.a)), xb = lerp(x0, x1, clamp01(sg.b));
      el.setAttribute("x", xa); el.setAttribute("width", Math.max(2, xb - xa));
      barStyle(el, sg.k, pu);
      opac(el, alpha);
    }));

    function draw(g, S) {
      // the kitchens: the main one scales about its top-left at the close; the twin sits at TWIN, same scale
      const s = lerp(1, HALF, clamp01(S.K.half));
      main.drawK({ o: S.K.o, draw: S.K.draw, cooks: S.cooks, veg: S.veg, knife: S.knife, oven: S.oven, appl: S.appl, chop: S.chop || 0 },
                 `translate(${BOX.x} ${BOX.y}) scale(${s}) translate(${-BOX.x} ${-BOX.y})`);
      twin.drawK(S.twin, `translate(${TWIN.x} ${TWIN.y}) scale(${HALF}) translate(${-BOX.x} ${-BOX.y})`);
      labK.set(S.K.lab * S.K.o);
      // labels
      slot.a.textContent = S.slot.top; slot.b.textContent = S.slot.bottom;
      slot.set(S.slot.o, S.slot.hero);
      chip.textContent = S.chip.text; domOpac(chip, S.chip.o * S.K.o);
      domOpac(closeA, S.close.a); domOpac(closeB, S.close.b);
      // the panel
      const P = S.panel, split = clamp01(P.split || 0), lanes = clamp01(P.lanes);
      opac(gPanel, P.o);
      panelBox.setAttribute("width", lerp(PANEL.w, SPLIT.w, split));
      domOpac(title, P.title * P.o * (1 - seg(split, 0, 0.5))); domOpac(title1, P.o * seg(split, 0.5, 1));
      domOpac(coreTag, clamp01(P.core || 0) * P.o * (1 - split));
      codeLines.forEach((el, i) => domOpac(el, P.o * (1 - lanes) * clamp01(P.code - i)));
      laneLabs.forEach((el) => domOpac(el, P.o * lanes * (1 - seg(split, 0, 0.5))));
      shortLabs.forEach((el) => domOpac(el, P.o * lanes * seg(split, 0.5, 1)));
      const x0 = lerp(PANEL.barX, SPLIT.barX, split), x1 = lerp(PANEL.barX1, SPLIT.barX1, split);
      laneLines.forEach((el) => { el.setAttribute("x1", x0); el.setAttribute("x2", x1); opac(el, lanes); });
      const pu = { py: clamp01((P.pulse && P.pulse.py) || 0), io: clamp01((P.pulse && P.pulse.io) || 0) };
      drawRows(bars, P.rows, x0, x1, pu, lanes);
      // the right half
      const o2 = P.o * seg(split, 0.5, 1);            // the right half appears once the left has narrowed (no title overlap)
      opac(gPanel2, o2); domOpac(title2, o2); shortLabs2.forEach((el) => domOpac(el, o2));
      drawRows(bars2, (S.panel2 && S.panel2.rows) || [], PANEL2.barX, PANEL.barX1, { py: 0, io: 0 }, o2);
    }
    return { draw, svg, gKit: main.g, gTwin: twin.g, cooks: main.cooks, knife: main.knife, twin, labels: { labK, slot }, chip, title, closeA, closeB, bars, bars2, gPanel, gPanel2 };
  }

  window.SC = { PAL, BOX, FEET, FIG, SPOT, OVEN, APPL, PANEL, PANEL2, SPLIT, TWIN, HALF, CLOSE_Y, BOARD, TIP,
                REST, SEAM1, PROTO, SLOT, STAIR, OVEN_ROWS, APPL_ROWS, CLOSE_ROWS, CLOSE_ROWS2, TWIN_COOKS, KIT, cooksAt,
                state, tween, merge, mount, lerp, clamp01, seg, io, pulse, chopAt,
                SEAM: SEAM1 };
})();
