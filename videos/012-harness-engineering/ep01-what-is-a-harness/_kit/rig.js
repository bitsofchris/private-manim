// rig.js — ep 1's rig: the agent wears the harness (look C, Chris 2026-10-17).
// The agent's head is the model (outline drawn dim); the four parts of the
// harness are what it carries: pages above its head (context), a terminal in
// its right hand (tools), a drawer in its left hand (memory), an arrow
// circling its feet (loop). Every beat of ep 1 draws the rig from here so the
// cuts match (storyboard.md, "Ledger").
// Linked into a beat as `kit/` (ln -s ../_kit NN_beat/kit), after cast/cast.js.
// Local to this episode; not a cast-kit change.
//
// Coordinates: rig-local units are frame pixels at the home place, origin at
// the agent's feet. place(rig, x, y, s) moves and scales the whole rig.
(function () {
  const { PAL, node, line, ink } = CAST;
  const NAMES = ["context", "tools", "memory", "loop"];   // CAST.PIPES order
  const HOME = { x: 500, y: 1040, s: 1 };
  const AGENT_S = 1.1;                                     // the agent inside the rig
  const LABEL = 60;
  // Rig-local anchors (home: frame = HOME + local).
  const AT = {
    head: [0, -(388 + 62) * AGENT_S],                      // centre of the rectangle head
    headTop: [0, -(388 + 124) * AGENT_S],
    context: [0, -700], tools: [205, -280], memory: [-205, -280], loop: [0, 0],
  };
  // Label centres (x) and tops (y), rig-local.
  const LAB = { context: [-280, -740], tools: [205, -215], memory: [-185, -215], loop: [350, -95], model: [260, -537] };
  const ELL = { rx: 260, ry: 58 };                         // the loop on the floor

  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mixHex = (a, b, u) => { const p = hex(a), q = hex(b), k = Math.max(0, Math.min(1, u));
    return `rgb(${p.map((v, i) => Math.round(v + (q[i] - v) * k)).join(",")})`; };

  // A part's strokes carry data-base (their resting colour) so part() can
  // blend them toward magenta.
  const tag = (el, base) => { el.setAttribute("data-base", base); return el; };

  function cards(g, col) {                                 // context: a stack of three pages
    [[-24, -24], [-12, -12], [0, 0]].forEach(([dx, dy]) =>
      tag(node("rect", { x: dx - 60, y: dy - 75, width: 120, height: 150, rx: 10, fill: PAL.panel, stroke: col, "stroke-width": 7 }, g), col));
    [-35, -12, 11, 34].forEach((yy, i) => tag(line(g, -36, yy, i % 2 ? 22 : 36, yy, ink(6, col)), col));
  }
  function term(g, col) {                                  // tools: a terminal card
    tag(node("rect", { x: -80, y: -58, width: 160, height: 116, rx: 12, fill: PAL.panel, stroke: col, "stroke-width": 7 }, g), col);
    tag(line(g, -80, -26, 80, -26, ink(5, col)), col);
    const t = tag(node("text", { x: -50, y: 34, "font-size": 56, "font-weight": 800, fill: col, "data-fill": 1 }, g), col);
    t.textContent = ">_"; t.style.fontFamily = "monospace";
  }
  function drawer(g, col) {                                // memory: a two-drawer cabinet
    tag(node("rect", { x: -75, y: -65, width: 150, height: 130, rx: 10, fill: PAL.panel, stroke: col, "stroke-width": 7 }, g), col);
    tag(line(g, -75, 0, 75, 0, ink(6, col)), col);
    tag(line(g, -20, -32, 20, -32, ink(7, col)), col); tag(line(g, -20, 33, 20, 33, ink(7, col)), col);
  }
  function floorLoop(g, col) {                             // loop: an arrow circling the feet
    const A0 = 200 * Math.PI / 180, A1 = 520 * Math.PI / 180;
    const ep = (a) => [ELL.rx * Math.cos(a), ELL.ry * Math.sin(a)];
    const [s0x, s0y] = ep(A0), [s1x, s1y] = ep(A1);
    tag(node("path", Object.assign({ d: `M ${s0x} ${s0y} A ${ELL.rx} ${ELL.ry} 0 1 1 ${s1x} ${s1y}` }, ink(12, col)), g), col);
    const dx = -ELL.rx * Math.sin(A1), dy = ELL.ry * Math.cos(A1), n = Math.hypot(dx, dy), ux = dx / n, uy = dy / n, h = 32;
    tag(node("path", Object.assign({ d: `M ${s1x - h * ux - 0.6 * h * uy} ${s1y - h * uy + 0.6 * h * ux} L ${s1x} ${s1y} L ${s1x - h * ux + 0.6 * h * uy} ${s1y - h * uy - 0.6 * h * ux}` }, ink(12, col)), g), col);
  }
  const DRAW = { context: [cards, 0.62], tools: [term, 0.8], memory: [drawer, 0.75], loop: [floorLoop, 1] };

  // make(svg, root, o): o.x, o.y, o.s (default HOME); o.missing: part indexes
  // drawn as dashed muted outlines (beat 6's second agent); o.labels (default true).
  function make(svg, root, o = {}) {
    const g = node("g", {}, svg);
    const missing = o.missing || [];
    // Parts drawn first sit behind the agent; the floor loop goes under the feet.
    const parts = NAMES.map((name, i) => {
      const [draw, sc] = DRAW[name], miss = missing.includes(i);
      const pg = node("g", {}, g), inner = node("g", { transform: `scale(${sc})` }, pg);
      draw(inner, miss ? PAL.muted : PAL.data);
      if (miss) inner.querySelectorAll("[data-base]").forEach((el) => {
        el.setAttribute("stroke-dasharray", "14 12"); if (el.getAttribute("fill") === PAL.panel) el.setAttribute("fill", "none");
        if (el.tagName === "text") el.setAttribute("opacity", 0);
      });
      return { name, el: pg, inner, miss, u: 0 };
    });
    // context's feed line into the head
    const feed = tag(line(g, AT.context[0], AT.context[1] + 70, AT.headTop[0], AT.headTop[1] - 6,
      { stroke: missing.includes(0) ? PAL.muted : PAL.data, "stroke-width": 8, "stroke-linecap": "round" }), missing.includes(0) ? PAL.muted : PAL.data);
    if (missing.includes(0)) feed.setAttribute("stroke-dasharray", "14 12");
    parts[0].feed = feed;
    const agent = CAST.agent(g, { x: 0, y: 0, s: AGENT_S });
    agent.headG.querySelector("rect").setAttribute("stroke", PAL.dim);    // the model, at rest
    CAST.pose(agent, { armL: 58, armR: 58 });
    g.insertBefore(parts[3].el, g.firstChild);                            // loop under the feet
    const labels = NAMES.map((n) => ISO.label(root, n, { size: LABEL, width: 320 }));
    const model = ISO.label(root, "model", { size: LABEL, width: 320, color: PAL.dim });
    labels.concat([model]).forEach((el) => { el.style.transformOrigin = "50% 50%"; });
    const rig = { g, agent, parts, labels, model, missing, x: 0, y: 0, s: 1, labelAlpha: o.labels === false ? 0 : 1 };
    place(rig, o.x != null ? o.x : HOME.x, o.y != null ? o.y : HOME.y, o.s || HOME.s);
    NAMES.forEach((_, i) => part(rig, i, 0));
    return rig;
  }

  // Frame point of a rig-local point.
  const at = (rig, p) => [rig.x + p[0] * rig.s, rig.y + p[1] * rig.s];

  // Move and scale the whole rig; a: label opacity (default: keep).
  function place(rig, x, y, s, a) {
    rig.x = x; rig.y = y; rig.s = s;
    if (a != null) rig.labelAlpha = a;
    rig.g.setAttribute("transform", `translate(${x} ${y}) scale(${s})`);
    follow(rig);
    const h = Math.round(LABEL * 1.1);
    NAMES.concat(["model"]).forEach((n, i) => {
      const el = i < 4 ? rig.labels[i] : rig.model;
      const [lx, ly] = at(rig, LAB[n]);
      el.style.left = (lx - 160) + "px"; el.style.top = ly + "px";
      el.style.opacity = rig.labelAlpha * (i < 4 && rig.missing.includes(i) ? 0 : 1);
    });
  }
  // Keep the hand-held parts in the agent's hands (after CAST.pose on rig.agent).
  function follow(rig) {
    const hs = AGENT_S, a = rig.agent;
    const handR = [a.handR[0] * hs, a.handR[1] * hs], handL = [a.handL[0] * hs, a.handL[1] * hs];
    const off = (p, base, hand) => [hand[0] + (base[0] - (base === AT.tools ? 145 : -145)), hand[1] + (base[1] + 290)];
    rig.parts.forEach((p) => {
      let pos = AT[p.name];
      if (p.name === "tools") pos = off(p, AT.tools, handR);
      if (p.name === "memory") pos = off(p, AT.memory, handL);
      p.pos = pos;
      p.el.setAttribute("transform", `translate(${pos[0]} ${pos[1]})`);
    });
  }

  // Part i's hero amount u: 0 = rest (teal), 1 = named (magenta); its label
  // goes magenta with it. pop (0..1) swells the label once.
  function part(rig, i, u, pop = 0) {
    const p = rig.parts[i]; p.u = u;
    const els = Array.from(p.inner.querySelectorAll("[data-base]"));
    if (p.feed) els.push(p.feed);
    els.forEach((el) => {
      const c = mixHex(el.getAttribute("data-base"), PAL.hero, u);
      if (el.getAttribute("stroke")) el.setAttribute("stroke", c);
      if (el.getAttribute("data-fill")) el.setAttribute("fill", c);
    });
    rig.labels[i].style.color = mixHex(PAL.ink, PAL.hero, u);
    rig.labels[i].style.transform = `scale(${1 + 0.18 * Math.sin(Math.PI * Math.max(0, Math.min(1, pop)))})`;
  }
  function parts(rig, us) { us.forEach((u, i) => part(rig, i, u)); }

  // Frame point of a part's centre, of the head, of a point on the floor loop (u 0..1 round).
  const partAt = (rig, i) => at(rig, rig.parts[i].pos);
  const headAt = (rig) => at(rig, AT.head);
  const loopAt = (rig, u) => { const a = (200 + 320 * u) * Math.PI / 180; return at(rig, [ELL.rx * Math.cos(a), ELL.ry * Math.sin(a)]); };

  // The verdicts: a teal check, and a dim circling arrow (turn it with spin).
  function check(svg, x, y, s = 1) {
    const g = node("g", {}, svg);
    node("path", Object.assign({ d: "M-38 0 L-10 28 L42 -30" }, ink(14, PAL.data)), g);
    const p = { el: g }; CAST.place(p, x, y, s); return p;
  }
  function circling(svg, x, y, s = 1) {
    const g = node("g", {}, svg), inner = node("g", {}, g);
    node("path", Object.assign({ d: "M 40 0 A 40 40 0 1 1 28 -28.6" }, ink(12, PAL.dim)), inner);
    node("path", Object.assign({ d: "M 10 -34 L 30 -30 L 30 -52" }, ink(12, PAL.dim)), inner);
    const p = { el: g, inner }; CAST.place(p, x, y, s); return p;
  }
  function spin(p, deg) { p.inner.setAttribute("transform", `rotate(${deg})`); }

  window.RIG = { HOME, NAMES, LABEL, AT, LAB, ELL, AGENT_S, make, place, follow, part, parts, at, partAt, headAt, loopAt,
                 check, circling, spin, mixHex };
})();
