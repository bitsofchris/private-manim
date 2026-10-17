// cast.js — the line-drawn cast for HyperFrames Shorts about agents and
// knowledge bases (the Harness Engineering look, 012; agents/style.md
// "Agents and knowledge bases"). Linked into a beat as `cast/`, after
// `iso/iso.js` (it borrows nothing from ISO but the clock and guides the
// beat already uses):
//   ln -s ../../../_shared/web/cast NN_beat/cast     (series episodes are one level deeper)
//
// One body, two heads. The human is the stick figure from
// prototypes/hyperframes/quiz (round head, dot eyes). The agent is the same
// body with a rectangle head and 1 and 0 for eyes, the only teal on it. The
// janitor is an agent with a broom, not a new character. Props are flat
// outlines: an agent's notes page, the human's board, the curated case, the
// map card, and the model as a blob with four pipes.
//
// Everything is SVG in one full-frame layer, so `hyperframes check` sees the
// geometry. Each part is a group placed at (x, y) with a scale; a figure's
// (x, y) is the point between its feet. Poses are plain numbers set from
// render(t): arm angles in degrees from straight down (positive swings out
// from the body), head tilt, a face. Pure functions only: no clocks, no
// randomness.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  // House palette (videos/_shared/style.py).
  const PAL = { bg: "#0B0B14", panel: "#14142B", ink: "#ECEBE4", dim: "#8A8FB0",
                data: "#2DD4BF", hero: "#C084FC", muted: "#4A5070", glass: "#67E8F9" };
  const STROKE = 9;                       // ink line at scale 1 (quiz figure)
  const BODY = { hip: -170, shoulder: -345, neck: -388, arm: 155, leg: 48 };
  const HEAD = { r: 64, cy: -452, rect: { w: 150, h: 124, rx: 26 } };

  // ---- SVG helpers ----
  function node(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach((k) => el.setAttribute(k, attrs[k]));
    if (parent) parent.appendChild(el);
    return el;
  }
  const line = (g, x1, y1, x2, y2, a = {}) => node("line", Object.assign({ x1, y1, x2, y2 }, a), g);
  const ink = (w = STROKE, col = PAL.ink) => ({ stroke: col, "stroke-width": w, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" });
  // A part's colourable strokes carry data-tint="base colour", so hero() can
  // swap them to magenta and back.
  function tint(el, col) { el.setAttribute("data-tint", col); return el; }
  function hero(part, on) {
    const g = part.el || part;
    const all = Array.from(g.querySelectorAll ? g.querySelectorAll("[data-tint]") : []);
    if (g.getAttribute && g.getAttribute("data-tint")) all.unshift(g);
    all.forEach((el) => {
      const c = on ? PAL.hero : el.getAttribute("data-tint");
      if (el.getAttribute("stroke") && el.getAttribute("stroke") !== "none") el.setAttribute("stroke", c);
      if (el.tagName === "text" || el.getAttribute("data-fill")) el.setAttribute("fill", c);
    });
  }
  function place(part, x, y, s = 1, rot = 0) {
    part.x = x; part.y = y; part.s = s;
    part.el.setAttribute("transform", `translate(${x} ${y}) rotate(${rot}) scale(${s})`);
  }
  function show(part, alpha) { part.el.setAttribute("opacity", Math.max(0, Math.min(1, alpha))); }

  // The full-frame layer every part draws into.
  function layer(root) {
    const svg = node("svg", { width: 1080, height: 1920, viewBox: "0 0 1080 1920" });
    svg.style.cssText = "position:absolute;left:0;top:0;overflow:visible;";
    svg.setAttribute("data-layout-allow-overflow", "");
    root.appendChild(svg);
    return svg;
  }

  // ---- figures ----
  // Where a limb ends: from (x, y), length len, angle deg from straight down,
  // side -1 (left) or +1 (right).
  function limb(x, y, len, deg, side) {
    const a = deg * Math.PI / 180;
    return [x + side * Math.sin(a) * len, y + Math.cos(a) * len];
  }
  function figure(svg, head, o = {}) {
    const g = node("g", {}, svg);
    const legL = line(g, 0, BODY.hip, -BODY.leg, 0, ink()), legR = line(g, 0, BODY.hip, BODY.leg, 0, ink());
    const upper = node("g", {}, g);
    line(upper, 0, BODY.hip, 0, BODY.neck, ink());
    const armL = line(upper, 0, BODY.shoulder, 0, 0, ink()), armR = line(upper, 0, BODY.shoulder, 0, 0, ink());
    const headG = node("g", {}, upper);
    const face = head(headG);
    const part = { el: g, upper, headG, armL, armR, legL, legR, face, kind: o.kind, pose: {} };
    pose(part, { armL: 22, armR: 22, lean: 0, tilt: 0 });
    place(part, o.x || 0, o.y || 0, o.s || 1);
    return part;
  }
  // Set any of { armL, armR (deg), lean (deg, whole upper body), tilt (deg, head) }.
  function pose(part, p) {
    Object.assign(part.pose, p);
    const q = part.pose;
    const l = limb(0, BODY.shoulder, BODY.arm, q.armL, -1), r = limb(0, BODY.shoulder, BODY.arm, q.armR, 1);
    part.armL.setAttribute("x2", l[0]); part.armL.setAttribute("y2", l[1]);
    part.armR.setAttribute("x2", r[0]); part.armR.setAttribute("y2", r[1]);
    part.upper.setAttribute("transform", `rotate(${q.lean} 0 ${BODY.hip})`);
    part.headG.setAttribute("transform", `rotate(${q.tilt} 0 ${BODY.neck})`);
    part.handL = l; part.handR = r;
    if (part.broom) broomTo(part);
  }
  // The hand in frame coordinates (for props held or pointed at).
  function hand(part, side = 1) {
    const h = side < 0 ? part.handL : part.handR;
    return [part.x + h[0] * part.s, part.y + h[1] * part.s];
  }

  function human(svg, o = {}) {
    return figure(svg, (g) => {
      node("circle", { cx: 0, cy: HEAD.cy, r: HEAD.r, fill: PAL.bg, stroke: PAL.ink, "stroke-width": STROKE }, g);
      const eyes = node("g", { fill: PAL.ink }, g);
      node("circle", { cx: -22, cy: HEAD.cy - 8, r: 8 }, eyes); node("circle", { cx: 22, cy: HEAD.cy - 8, r: 8 }, eyes);
      const mouth = node("path", Object.assign({ d: "" }, ink(7)), g);
      const f = { eyes, mouth };
      faceOf(f, o.face || "smile");
      return f;
    }, Object.assign({ kind: "human" }, o));
  }
  // smile | flat | frown
  function faceOf(f, kind) {
    const y = HEAD.cy + 26;
    const d = { smile: `M-20 ${y - 4} Q0 ${y + 16} 20 ${y - 4}`, flat: `M-18 ${y} L18 ${y}`, frown: `M-18 ${y + 8} Q0 ${y - 10} 18 ${y + 8}` }[kind];
    f.mouth.setAttribute("d", d);
  }
  function face(part, kind) { if (part.face.mouth) faceOf(part.face, kind); }

  function agent(svg, o = {}) {
    return figure(svg, (g) => {
      const R = HEAD.rect;
      node("rect", { x: -R.w / 2, y: BODY.neck - R.h, width: R.w, height: R.h, rx: R.rx, fill: PAL.bg, stroke: PAL.ink, "stroke-width": STROKE }, g);
      const eyes = [["1", -30], ["0", 30]].map(([c, dx]) => {
        const t = node("text", { x: dx, y: BODY.neck - R.h / 2 + 4, "text-anchor": "middle", "dominant-baseline": "middle",
                                 "font-size": 66, "font-weight": 800, fill: PAL.data }, g);
        t.textContent = c;
        t.style.fontFamily = "monospace";            // set from script: the HTML route renders in Inter (beat-brief trap)
        return t;
      });
      return { eyes };
    }, Object.assign({ kind: "agent" }, o));
  }
  // An agent's eyes: "10" by default; blink(part, u) closes them to dashes as u -> 1.
  function blink(part, u) {
    (part.face.eyes || []).forEach((t, i) => { t.textContent = u > 0.5 ? "-" : (i ? "0" : "1"); });
  }

  // The janitor: an agent holding a broom in its right hand. The handle runs
  // from just above the hand down through it to the floor.
  function janitor(svg, o = {}) {
    const a = agent(svg, Object.assign({ kind: "janitor" }, o));
    const b = node("g", {}, a.el);
    a.broom = { handle: line(b, 0, 0, 0, 0, ink(STROKE - 1, PAL.dim)),
                head: node("path", Object.assign({ d: "" }, ink(STROKE - 2, PAL.dim)), b) };
    a.el.insertBefore(b, a.el.firstChild);
    pose(a, { armR: 24 });
    return a;
  }
  function broomTo(part) {
    const [hx, hy] = part.handR;
    const dx = 0.42, top = [hx - dx * 70, hy - 70];                  // the handle leans out ~23°
    const foot = [hx + dx * (0 - hy), 0];
    part.broom.handle.setAttribute("x1", top[0]); part.broom.handle.setAttribute("y1", top[1]);
    part.broom.handle.setAttribute("x2", foot[0]); part.broom.handle.setAttribute("y2", foot[1] - 22);
    const [fx] = foot;
    part.broom.head.setAttribute("d", `M${fx - 38} ${-22} L${fx + 38} ${-22} L${fx + 52} 6 L${fx - 52} 6 Z`);
    part.broom.foot = [fx, 0];
  }

  // ---- props (origin top-left) ----
  // The agent layer: a dense page, written for agents. o.hash: the first line.
  function page(svg, o = {}) {
    const w = o.w || 260, h = o.h || 340, g = node("g", {}, svg);
    tint(node("rect", { x: 0, y: 0, width: w, height: h, rx: 10, fill: PAL.panel, stroke: PAL.data, "stroke-width": 7 }, g), PAL.data);
    const t = node("text", { x: 24, y: 78, "font-size": 60, "font-weight": 800, fill: PAL.data, "data-fill": 1 }, g);
    t.textContent = o.hash || "a3f9c2"; t.style.fontFamily = "monospace"; tint(t, PAL.data);
    const n = o.lines || 8;
    for (let i = 0; i < n; i++) {
      const lw = (w - 48) * (0.62 + 0.38 * ((i * 7) % 5) / 4);        // fixed ragged widths, no randomness
      line(g, 24, 118 + i * ((h - 150) / n), 24 + lw, 118 + i * ((h - 150) / n), { stroke: PAL.data, "stroke-width": 6, "stroke-linecap": "round", "stroke-opacity": 0.5 });
    }
    const part = { el: g, w, h, kind: "page" };
    place(part, o.x || 0, o.y || 0, o.s || 1);
    return part;
  }
  // The human layer: one board, columns of cards. o.cards: cards per column.
  function board(svg, o = {}) {
    const w = o.w || 320, h = o.h || 340, cols = o.cards || [2, 1, 3], g = node("g", {}, svg);
    tint(node("rect", { x: 0, y: 0, width: w, height: h, rx: 12, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7 }, g), PAL.ink);
    const cw = w / cols.length;
    cols.forEach((n, c) => {
      if (c) line(g, c * cw, 18, c * cw, h - 18, { stroke: PAL.muted, "stroke-width": 5 });
      for (let k = 0; k < n; k++)
        tint(node("rect", { x: c * cw + 14, y: 26 + k * 78, width: cw - 28, height: 56, rx: 8, fill: "none", stroke: PAL.ink, "stroke-width": 5 }, g), PAL.ink);
    });
    const part = { el: g, w, h, kind: "board" };
    place(part, o.x || 0, o.y || 0, o.s || 1);
    return part;
  }
  // The curated layer: a glass case holding rules, the map, and a goal.
  // part.items.{rules, map, goal} can each be made the hero.
  function vitrine(svg, o = {}) {
    const w = o.w || 290, h = o.h || 360, g = node("g", {}, svg);
    node("rect", { x: 0, y: 0, width: w, height: h, rx: 12, fill: PAL.panel, stroke: PAL.glass, "stroke-width": 6, "stroke-opacity": 0.6 }, g);
    node("rect", { x: 12, y: 12, width: w - 24, height: h - 24, rx: 8, fill: "none", stroke: PAL.glass, "stroke-width": 3, "stroke-opacity": 0.35 }, g);
    const rules = node("g", { transform: "translate(34 40)" }, g);
    tint(node("rect", { x: 0, y: 0, width: 92, height: 120, rx: 6, fill: "none", stroke: PAL.ink, "stroke-width": 6 }, rules), PAL.ink);
    [28, 54, 80].forEach((y, i) => tint(line(rules, 18, y, i === 2 ? 56 : 74, y, ink(5)), PAL.ink));
    const map = node("g", { transform: `translate(${w - 140} 44)` }, g);
    tint(node("path", Object.assign({ d: "M0 10 L36 28 L72 10 L108 28 L108 116 L72 98 L36 116 L0 98 Z" }, ink(6)), map), PAL.ink);
    const goal = node("g", { transform: `translate(${w / 2} ${h - 92})` }, g);
    [52, 30].forEach((r) => tint(node("circle", { cx: 0, cy: 0, r, fill: "none", stroke: PAL.ink, "stroke-width": 6 }, goal), PAL.ink));
    tint(node("circle", { cx: 0, cy: 0, r: 9, fill: PAL.ink, "data-fill": 1 }, goal), PAL.ink);
    const part = { el: g, w, h, kind: "vitrine", items: { rules: { el: rules }, map: { el: map }, goal: { el: goal } } };
    place(part, o.x || 0, o.y || 0, o.s || 1);
    return part;
  }
  // The map: a short index card whose arrows point to files. o.files: how
  // many it points to; o.ghost: files it does not point to (dashed).
  function mapCard(svg, o = {}) {
    const g = node("g", {}, svg), nf = o.files || 3, ng = o.ghost == null ? 1 : o.ghost;
    const card = node("g", {}, g);
    tint(node("rect", { x: 0, y: 0, width: 150, height: 110, rx: 10, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7 }, card), PAL.ink);
    [30, 55, 80].forEach((y, i) => tint(line(card, 22, y, i === 1 ? 104 : 126, y, ink(5)), PAL.ink));
    const files = [], ghosts = [];
    const fy = (i, n) => -40 + i * (190 / Math.max(1, n - 1 || 1));
    for (let i = 0; i < nf; i++) {
      const y = nf === 1 ? 40 : fy(i, nf);
      line(g, 150, 55, 236, y + 22, { stroke: PAL.dim, "stroke-width": 5, "stroke-linecap": "round" });
      files.push(tint(node("rect", { x: 240, y, width: 76, height: 46, rx: 6, fill: "none", stroke: PAL.data, "stroke-width": 6 }, g), PAL.data));
    }
    for (let i = 0; i < ng; i++)
      ghosts.push(node("rect", { x: 20 + i * 96, y: 170, width: 76, height: 46, rx: 6, fill: "none", stroke: PAL.muted, "stroke-width": 5, "stroke-dasharray": "10 10" }, g));
    const part = { el: g, kind: "map", card: { el: card }, files, ghosts };
    place(part, o.x || 0, o.y || 0, o.s || 1);
    return part;
  }
  // The model: a blob (origin at its centre) with four pipes out of it, in
  // PIPES order: up, right, down, left. part.pipes[i] can be made the hero.
  const PIPES = ["context", "tools", "memory", "loop"];
  function blob(svg, o = {}) {
    const g = node("g", {}, svg), L = o.pipe || 120;
    const dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]], R = [96, 116, 100, 112];
    const pipes = dirs.map(([dx, dy], i) => tint(line(g, dx * R[i] * 0.8, dy * R[i] * 0.8, dx * (R[i] + L), dy * (R[i] + L),
      { stroke: PAL.data, "stroke-width": 26, "stroke-linecap": "round" }), PAL.data));
    const D = "M-74 6 C-96 -66 -12 -112 34 -84 C96 -96 128 -20 98 22 C120 80 40 116 6 92 C-56 118 -104 62 -74 6 Z";
    node("path", { d: D, fill: PAL.bg }, g);                          // opaque underlay: the pipes stop at the edge
    const body = node("path", { d: D, fill: PAL.hero, "fill-opacity": 0.22, stroke: PAL.hero, "stroke-width": 8 }, g);
    const part = { el: g, kind: "blob", body, pipes, names: PIPES };
    place(part, o.x || 0, o.y || 0, o.s || 1);
    return part;
  }

  window.CAST = { PAL, STROKE, BODY, HEAD, PIPES, layer, node, line, ink, tint, hero, place, show,
                  limb, pose, hand, human, agent, janitor, face, blink, page, board, vitrine, mapCard, blob };
})();
