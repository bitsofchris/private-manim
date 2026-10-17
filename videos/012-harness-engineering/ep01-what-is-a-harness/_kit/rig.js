// rig.js — ep 1's rig: the model (CAST.blob) with its four pipes, the four
// pipe labels, the pipe states, and the two verdicts (✓, ↻). Every beat of
// ep 1 draws the rig from here so the cuts match (storyboard.md, "Ledger").
// Linked into a beat as `kit/` (ln -s ../_kit NN_beat/kit), after cast/cast.js.
//
// Local to this episode; not a kit change. The blob body is drawn dim here
// (this Short is about everything except the model), so magenta only ever
// goes to the pipe being named.
(function () {
  const { PAL } = CAST;
  const R = [96, 116, 100, 112];              // CAST.blob's pipe roots, PIPES order
  const DIRS = [[0, -1], [1, 0], [0, 1], [-1, 0]];
  const NAMES = CAST.PIPES;                   // context, tools, memory, loop
  const HOME = { x: 480, y: 640, s: 0.95, pipe: 150 };
  const HUMAN = { x: 140, y: 1090, s: 0.6 };
  const LABEL = 60;

  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mixHex = (a, b, u) => { const p = hex(a), q = hex(b);
    return `rgb(${p.map((v, i) => Math.round(v + (q[i] - v) * Math.max(0, Math.min(1, u)))).join(",")})`; };

  // The end of pipe i at (x, y, s), and where its label sits.
  function pipeEnd(i, x, y, s, L = HOME.pipe) {
    const d = (R[i] + L) * s;
    return [x + DIRS[i][0] * d, y + DIRS[i][1] * d];
  }
  function labelBox(i, x, y, s) {
    const [ex, ey] = pipeEnd(i, x, y, s), h = Math.round(LABEL * 1.1), gap = 22 * s + 8;
    if (i === 0) return { left: ex - 160, top: ey - gap - h, width: 320, align: "center" };
    if (i === 1) return { left: ex + gap, top: ey - h / 2, width: 220, align: "left" };
    if (i === 2) return { left: ex - 160, top: ey + gap, width: 320, align: "center" };
    return { left: ex - gap - 180, top: ey - h / 2, width: 180, align: "right" };
  }

  // make(svg, root, o): o.x, o.y, o.s (default HOME), o.missing: pipe indexes
  // drawn dashed and muted (beat 6's second rig), o.labels (default true).
  function make(svg, root, o = {}) {
    const x = o.x != null ? o.x : HOME.x, y = o.y != null ? o.y : HOME.y, s = o.s || HOME.s;
    const g = CAST.node("g", {}, svg);
    const blob = CAST.blob(g, { x: 0, y: 0, s: 1, pipe: HOME.pipe });
    blob.body.setAttribute("stroke", PAL.dim);
    blob.body.setAttribute("fill", PAL.dim);
    blob.body.setAttribute("fill-opacity", 0.12);
    const missing = o.missing || [];
    missing.forEach((i) => {
      const p = blob.pipes[i];
      p.setAttribute("stroke", PAL.muted); p.setAttribute("stroke-width", 14);
      p.setAttribute("stroke-dasharray", "26 22"); p.setAttribute("stroke-linecap", "butt");
      p.setAttribute("data-tint", PAL.muted);
    });
    // Flow: three bg-coloured ticks per pipe sliding toward the blob.
    const ticks = blob.pipes.map((p, i) => missing.includes(i) ? [] : [0, 1, 2].map(() =>
      CAST.node("circle", { r: 6, fill: PAL.bg, "fill-opacity": 0.7 }, blob.el)));
    const labels = NAMES.map((n, i) => {
      const el = ISO.label(root, n, Object.assign({ size: LABEL }, labelBox(i, x, y, s)));
      el.style.transformOrigin = "50% 50%";
      return el;
    });
    const rig = { g, blob, labels, ticks, missing, x, y, s, state: [0, 0, 0, 0] };
    place(rig, x, y, s);
    labels.forEach((el) => { el.style.opacity = o.labels === false ? 0 : 1; });
    return rig;
  }

  // Move and scale the whole rig; labels follow. a: label opacity.
  function place(rig, x, y, s, a) {
    rig.x = x; rig.y = y; rig.s = s;
    rig.g.setAttribute("transform", `translate(${x} ${y}) scale(${s})`);
    rig.labels.forEach((el, i) => {
      const b = labelBox(i, x, y, s);
      el.style.left = b.left + "px"; el.style.top = b.top + "px";
      if (a != null) el.style.opacity = a;
    });
  }

  // Pipe i's hero amount u: 0 = rest (teal), 1 = named (magenta). The label
  // goes magenta with it. pop (0..1) swells the label briefly.
  function pipe(rig, i, u, pop = 0) {
    rig.state[i] = u;
    if (rig.missing.includes(i)) {
      rig.blob.pipes[i].setAttribute("stroke", mixHex(PAL.muted, PAL.hero, u));
    } else {
      rig.blob.pipes[i].setAttribute("stroke", mixHex(PAL.data, PAL.hero, u));
    }
    rig.labels[i].style.color = mixHex(PAL.ink, PAL.hero, u);
    rig.labels[i].style.transform = `scale(${1 + 0.18 * Math.sin(Math.PI * Math.max(0, Math.min(1, pop)))})`;
  }
  // Set all four at once: us = [u0, u1, u2, u3].
  function pipes(rig, us) { us.forEach((u, i) => pipe(rig, i, u)); }

  // Flow along the pipes at phase f (seconds of flow; freeze it for the hold).
  function flow(rig, f) {
    rig.ticks.forEach((ts, i) => ts.forEach((c, k) => {
      const u = ((f * 0.45 + k / 3) % 1);                  // outer end -> blob
      const d = R[i] * 0.95 + (1 - u) * (HOME.pipe - 6);
      c.setAttribute("cx", DIRS[i][0] * d); c.setAttribute("cy", DIRS[i][1] * d);
      c.setAttribute("fill-opacity", 0.7 * Math.sin(Math.PI * u));
    }));
  }

  // A point along pipe i in frame coordinates: u 0 = at the blob's edge, 1 = the end.
  function along(rig, i, u) {
    const d = (R[i] * 0.8 + u * (R[i] + HOME.pipe - R[i] * 0.8)) * rig.s;
    return [rig.x + DIRS[i][0] * d, rig.y + DIRS[i][1] * d];
  }

  // The human, at its ledger place.
  function human(svg, o = {}) {
    return CAST.human(svg, Object.assign({}, HUMAN, o));
  }

  // The verdicts: a teal check, and a dim circling arrow (spin it with rot).
  function check(svg, x, y, s = 1) {
    const g = CAST.node("g", {}, svg);
    CAST.node("path", Object.assign({ d: "M-38 0 L-10 28 L42 -30" }, CAST.ink(14, PAL.data)), g);
    const part = { el: g }; CAST.place(part, x, y, s); return part;
  }
  function circling(svg, x, y, s = 1) {
    const g = CAST.node("g", {}, svg), inner = CAST.node("g", {}, g);
    CAST.node("path", Object.assign({ d: "M 40 0 A 40 40 0 1 1 28 -28.6" }, CAST.ink(12, PAL.dim)), inner);
    CAST.node("path", Object.assign({ d: "M 10 -34 L 30 -30 L 30 -52" }, CAST.ink(12, PAL.dim)), inner);
    const part = { el: g, inner };
    CAST.place(part, x, y, s);
    return part;
  }
  function spin(part, deg) { part.inner.setAttribute("transform", `rotate(${deg})`); }

  window.RIG = { HOME, HUMAN, NAMES, LABEL, R, DIRS, make, place, pipe, pipes, flow, along, pipeEnd, human, check, circling, spin, mixHex };
})();
