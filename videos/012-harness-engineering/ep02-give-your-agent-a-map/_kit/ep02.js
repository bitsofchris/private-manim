// ep02.js — the one world of Harness ep 2 ("Give your agent a map"), on top
// of the shared cast kit (CAST). Linked into a beat as `kit/` after `cast/`:
//   ln -s ../_kit NN_beat/kit        then  <script src="kit/ep02.js"></script>
//
// Every beat draws the same parts at the same pixels (storyboard ledger):
// the repo (a 4 x 4 grid of files, drawn as CAST.mapCard draws a file), the
// context window (bottom right) with its `context` label, the agent (left),
// the map card (a readable AGENTS.md map inside the window) with three arrows
// up the gaps of the grid to auth.md, api.md and deploy.md, the giant
// AGENTS.md page, the wander trail, and the human (beat 2 only).
//
// Use: const W = EP2.build(root); then in render(t) call W.set({...}) with a
// state object (W.MAP is the canonical frame). Anything not given takes the
// value in W.EMPTY, so a beat states only what it changes. Pure functions of
// the state: no clocks, no randomness.
(function () {
  const { PAL, node, line } = CAST;
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mixHex = (a, b, u) => { const p = hex(a), q = hex(b); return `rgb(${p.map((v, i) => Math.round(lerp(v, q[i], clamp01(u)))).join(",")})`; };

  // ---- geometry (px, 1080 x 1920 frame) ----
  const GRID = { x0: 150, y0: 255, w: 160, h: 62, px: 210, py: 95, cols: 4, rows: 4 };
  const cell = (c, r) => ({ x: GRID.x0 + c * GRID.px, y: GRID.y0 + r * GRID.py });
  const LANES = [335, 545, 755];                       // the gaps between columns
  const WIN = { x: 300, y: 650, w: 630, h: 430 };      // the context window
  const CARD = { x: 316, y: 668, w: 584, h: 310, pad: 18, lh: 70, size: 60 };
  const LABEL = { right: 910, top: 1002, size: 60 };
  const AGENT = { x: 175, y: 1080, s: 0.7 };
  const HUMAN = { x: 110, y: 1080, s: 0.7 };
  const AGENT_BESIDE = { x: 265, y: 1080 };            // where the agent stands in beat 2
  // The map: its lines, and the file each points to, by grid cell. One arrow
  // per line, up its lane, then a short turn into the file's side.
  const MAP_LINES = ["auth.md", "api.md", "deploy.md"];
  const TARGETS = [{ name: "auth.md", c: 0, r: 2, lane: 0 }, { name: "api.md", c: 1, r: 0, lane: 1 }, { name: "deploy.md", c: 3, r: 1, lane: 2 }];
  const fileIndex = (c, r) => r * GRID.cols + c;
  const AUTH = fileIndex(0, 2);                        // the file the agent drills into
  const TARGET_FILES = TARGETS.map((t) => fileIndex(t.c, t.r));
  // Where auth.md sits once retrieved into the window: lower right, beside the
  // card, which shrinks left to scale 0.72 to make room.
  const AUTH_IN_WIN = { x: 752, y: 880 };

  // ---- defaults: the empty world (beat 2's opening) ----
  const EMPTY = {
    files: "teal",            // "teal" | "ghost" (all but the targets dashed) | "muted"
    fileMode: null,           // optional array of 16 modes, overrides `files`
    fileAlpha: 1,
    fileXY: null,             // optional array of 16 [x, y] (top-left) overrides
    rot: 0,                   // 0..1: how far the files have gone teal -> muted
    authOpen: 0,              // 0..1: auth.md's lines draw in
    win: 1, winHero: 0,       // window opacity, outline teal->magenta
    label: "context", labelAlpha: 1, labelHero: 0,
    card: 0, cardScale: 1, cardHero: 0, cardLines: 4, underline: -1, underlineU: 0,
    arrows: [0, 0, 0], arrowHero: -1, arrowAlpha: 1,
    trail: 0, trailHero: 0, trailAlpha: 1,
    page: 0, pageTop: 250, pageLines: 0, pageHero: 0, pageMute: 0, scan: -1,
    agent: { x: AGENT.x, y: AGENT.y, armL: 22, armR: 22, lean: 0, tilt: 0, blink: 0 },
    human: { alpha: 0, armL: 22, armR: 22, lean: 0, tilt: 0, face: "smile" },
    point: 0,                 // the human's straight line to auth.md, 0..1
  };
  // The canonical frame: the map in the window, arrows out to its three files.
  const MAP = { files: "ghost", card: 1, arrows: [1, 1, 1] };

  // The stuffed window (beat 3): every file piled into the window, fixed
  // offsets. SPILL is the same pile after "backfire": it bulges past the
  // window's edges (still inside the safe area).
  const PILE = Array.from({ length: 16 }, (_, i) => [WIN.x + 20 + (i % 4) * 118 + ((i * 37) % 23), WIN.y + 30 + Math.floor(i / 4) * 78 + ((i * 53) % 29)]);
  const SPILL = PILE.map(([x, y], i) => {
    const c = i % 4, r = Math.floor(i / 4);
    return [x + (c - 1.5) * 34 + ((i * 29) % 17) - 8, y + (r - 1.5) * 40 - (r === 0 ? 40 : 0) + ((i * 41) % 13)];
  });

  // Seam states: SEAM[n] is the last frame of beat n and the first of beat
  // n + 1. Beats start from W.set(SEAM[n - 1]) and end on W.set(SEAM[n]).
  const SEAM = {
    1: Object.assign({}, MAP, { cardHero: 1 }),
    2: { win: 0.3, labelAlpha: 0.3, point: 1, trail: 1, trailHero: 1,
         agent: { x: AGENT_BESIDE.x }, human: { alpha: 1, armR: 140, tilt: -6 } },
    3: { fileXY: SPILL, winHero: 1, agent: { lean: -8, blink: 1 } },
    4: { fileXY: SPILL, rot: 1, label: "context rot", labelHero: 1, agent: { lean: -8, blink: 1 } },
    5: { files: "muted", page: 1, pageTop: 250, pageLines: 22, pageMute: 1, agent: { tilt: 10 } },
    6: Object.assign({}, MAP, { cardHero: 1 }),
    7: Object.assign({}, MAP, { cardHero: 1, agent: { armR: 115, tilt: -8 } }),
  };
  // Beat 8's end: the card shrinks left (scale 0.72, anchored top-left) and
  // auth.md sits at AUTH_IN_WIN, open, magenta, beside it.

  function build(root, o = {}) {
    const svg = CAST.layer(root);
    const W = { svg, root };

    // the window (under everything in it)
    W.win = node("rect", { x: WIN.x, y: WIN.y, width: WIN.w, height: WIN.h, rx: 18, fill: PAL.panel, stroke: PAL.dim, "stroke-width": 7 }, svg);

    // the human's pointing line and the agent's wander trail (under the files)
    W.pointLine = line(svg, 0, 0, 0, 0, { stroke: PAL.ink, "stroke-width": 6, "stroke-linecap": "round" });
    W.trail = node("path", { d: trailPath(), fill: "none", stroke: PAL.data, "stroke-width": 6, "stroke-linecap": "round", "stroke-linejoin": "round" }, svg);
    W.trailLen = 2600;

    // the 16 files
    W.files = [];
    for (let r = 0; r < GRID.rows; r++) for (let c = 0; c < GRID.cols; c++) {
      const g = node("g", {}, svg);
      const rect = node("rect", { x: 0, y: 0, width: GRID.w, height: GRID.h, rx: 6, fill: PAL.bg, stroke: PAL.data, "stroke-width": 6 }, g);
      const lines = [0, 1, 2].map((k) => line(g, 18, 0, 18, 0, { stroke: PAL.data, "stroke-width": 5, "stroke-linecap": "round", "stroke-opacity": 0.7 }));
      W.files.push({ g, rect, lines, c, r, home: cell(c, r) });
    }

    // the giant AGENTS.md page (beat 5): an SVG sheet + DOM title
    W.pageG = node("g", {}, svg);
    W.pageRect = node("rect", { x: CARD.x, y: 250, width: CARD.w, height: 800, rx: 14, fill: PAL.panel, stroke: PAL.ink, "stroke-width": 7 }, W.pageG);
    W.pageLines = [];
    for (let i = 0; i < 22; i++) {
      const lw = (CARD.w - 64) * (0.55 + 0.45 * ((i * 7) % 5) / 4);   // fixed ragged widths, as CAST.page
      W.pageLines.push(line(W.pageG, CARD.x + 32, 0, CARD.x + 32 + lw, 0, { stroke: PAL.ink, "stroke-width": 8, "stroke-linecap": "round" }));
    }
    W.scanBar = node("rect", { x: CARD.x + 12, y: 0, width: CARD.w - 24, height: 16, rx: 8, fill: PAL.glass, "fill-opacity": 0.35 }, W.pageG);
    W.pageTitle = text(root, "# AGENTS.md", { left: CARD.x + CARD.pad, top: 0, color: PAL.ink });
    W.pageTitle.style.fontFamily = "monospace";

    // the arrows (over the files), drawn with a dash offset
    W.arrows = TARGETS.map((t) => {
      const d = arrowPath(t), g = node("g", {}, svg);
      const p = node("path", { d, fill: "none", stroke: PAL.dim, "stroke-width": 6, "stroke-linecap": "round", "stroke-linejoin": "round" }, g);
      const head = node("path", { d: arrowHead(t), fill: PAL.dim }, g);
      return { g, p, head, len: arrowLen(t) };
    });

    // the map card: DOM, so `check` reads its text
    W.card = document.createElement("div");
    W.card.style.cssText = `position:absolute;left:${CARD.x}px;top:${CARD.y}px;width:${CARD.w}px;height:${CARD.h}px;` +
      `border-radius:14px;background:${PAL.panel};border:7px solid ${PAL.ink};padding:${CARD.pad - 7}px ${CARD.pad}px;transform-origin:0 0;`;
    root.appendChild(W.card);
    W.cardRows = ["# AGENTS.md"].concat(MAP_LINES).map((s, i) => {
      const d = document.createElement("div");
      d.textContent = s;
      d.style.cssText = `position:relative;font-size:${CARD.size}px;line-height:${CARD.lh}px;height:${CARD.lh}px;white-space:nowrap;color:${i ? PAL.ink : PAL.dim};`;
      d.style.fontFamily = "monospace";                // set from script (beat-brief trap)
      W.card.appendChild(d);
      return d;
    });
    W.underline = document.createElement("div");
    W.underline.style.cssText = `position:absolute;left:${CARD.pad}px;height:7px;border-radius:4px;background:${PAL.hero};transform-origin:0 50%;`;
    W.card.appendChild(W.underline);

    // the window's label (DOM, bottom right inside the window)
    W.label = text(root, "context", { left: LABEL.right - 520, top: LABEL.top, width: 520, align: "right", color: PAL.dim });

    // the cast
    W.agent = CAST.agent(svg, { x: AGENT.x, y: AGENT.y, s: AGENT.s });
    W.human = CAST.human(svg, { x: HUMAN.x, y: HUMAN.y, s: HUMAN.s });

    W.set = (st) => set(W, Object.assign({}, EMPTY, st, {
      agent: Object.assign({}, EMPTY.agent, st.agent || {}),
      human: Object.assign({}, EMPTY.human, st.human || {}),
    }));
    return W;
  }

  function text(root, s, o) {
    const el = document.createElement("div");
    el.textContent = s;
    el.style.cssText = `position:absolute;left:${o.left}px;top:${o.top}px;font-size:60px;line-height:66px;white-space:nowrap;color:${o.color};` +
      (o.width ? `width:${o.width}px;text-align:${o.align || "left"};` : "");
    root.appendChild(el);
    return el;
  }

  // ---- paths ----
  function arrowEnd(t) {
    const f = cell(t.c, t.r), x = LANES[t.lane], left = f.x + GRID.w < x;   // the file is left of its lane
    return { x, y: f.y + GRID.h / 2, ex: left ? f.x + GRID.w + 4 : f.x - 4, dir: left ? -1 : 1 };
  }
  const R = 16;
  function arrowPath(t) {
    const e = arrowEnd(t);
    return `M${e.x} ${CARD.y} L${e.x} ${e.y + R} Q${e.x} ${e.y} ${e.x + e.dir * R} ${e.y} L${e.ex - e.dir * 14} ${e.y}`;
  }
  function arrowLen(t) { const e = arrowEnd(t); return (CARD.y - e.y - R) + R * 1.57 + Math.abs(e.ex - e.dir * 14 - e.x - e.dir * R); }
  function arrowHead(t) {
    const e = arrowEnd(t), b = e.ex - e.dir * 28;
    return `M${e.ex} ${e.y} L${b} ${e.y - 17} L${b} ${e.y + 17} Z`;
  }
  // The wander: from the agent's head (beside the human) through file after
  // file in a fixed order, never the straight way.
  const WANDER = [[3, 3], [2, 2], [3, 1], [1, 1], [2, 0], [0, 0], [1, 2], [0, 3], [1, 3], [2, 3], [3, 2], [3, 0], [0, 1]];
  function trailPath() {
    let d = `M${AGENT_BESIDE.x + 70} 700`;
    WANDER.forEach(([c, r], i) => {
      const f = cell(c, r), x = f.x + GRID.w / 2, y = f.y + GRID.h / 2;
      const bx = x + (i % 2 ? -60 : 60), by = y + (i % 3 ? 70 : -60);
      d += ` Q${bx} ${by} ${x} ${y}`;
    });
    return d;
  }

  // ---- state -> drawing ----
  function fileColour(mode, rot) {
    if (mode === "hero") return PAL.hero;
    if (mode === "muted" || mode === "ghost") return PAL.muted;
    return mixHex(PAL.data, PAL.muted, rot);
  }
  function set(W, st) {
    // window
    W.win.setAttribute("opacity", st.win);
    W.win.setAttribute("stroke", st.winHero ? mixHex(PAL.dim, PAL.hero, st.winHero) : PAL.dim);
    // files
    W.files.forEach((f, i) => {
      let mode = st.fileMode ? st.fileMode[i] : st.files;
      if (mode === "ghost" && TARGET_FILES.includes(i)) mode = "teal";
      const xy = st.fileXY && st.fileXY[i] ? st.fileXY[i] : [f.home.x, f.home.y];
      f.g.setAttribute("transform", `translate(${xy[0]} ${xy[1]})`);
      f.g.setAttribute("opacity", Array.isArray(st.fileAlpha) ? st.fileAlpha[i] : st.fileAlpha);
      const col = fileColour(mode, st.rot);
      f.rect.setAttribute("stroke", col);
      f.rect.setAttribute("stroke-dasharray", mode === "ghost" ? "10 10" : "none");
      f.rect.setAttribute("stroke-width", mode === "ghost" ? 5 : 6);
      const open = i === AUTH ? st.authOpen : 0;
      f.lines.forEach((l, k) => {
        const y = 16 + k * 15, w = (GRID.w - 36) * (k === 1 ? 0.6 : 0.85) * clamp01(open * 3 - k);
        l.setAttribute("y1", y); l.setAttribute("y2", y); l.setAttribute("x2", 18 + w);
        l.setAttribute("stroke", col); l.setAttribute("opacity", w > 0 ? 1 : 0);
      });
    });
    CAST.place(W.human, HUMAN.x, HUMAN.y, HUMAN.s);
    CAST.pose(W.human, { armL: st.human.armL, armR: st.human.armR, lean: st.human.lean, tilt: st.human.tilt });
    // the human's straight line: from the hand to auth.md's bottom edge
    const hand = CAST.hand(W.human, 1);
    const a = cell(TARGETS[0].c, TARGETS[0].r), hx = hand[0], hy = hand[1], tx = a.x + GRID.w / 2, ty = a.y + GRID.h + 8;
    W.pointLine.setAttribute("x1", hx); W.pointLine.setAttribute("y1", hy);
    W.pointLine.setAttribute("x2", lerp(hx, tx, st.point)); W.pointLine.setAttribute("y2", lerp(hy, ty, st.point));
    W.pointLine.setAttribute("opacity", st.point > 0 ? st.human.alpha : 0);
    // trail
    W.trail.setAttribute("stroke-dasharray", `${W.trailLen} ${W.trailLen}`);
    W.trail.setAttribute("stroke-dashoffset", W.trailLen * (1 - st.trail));
    W.trail.setAttribute("stroke", st.trailHero ? mixHex(PAL.data, PAL.hero, st.trailHero) : PAL.data);
    W.trail.setAttribute("opacity", st.trail > 0 ? st.trailAlpha : 0);
    // page
    W.pageG.setAttribute("opacity", st.page);
    W.pageTitle.style.opacity = st.page;
    W.pageRect.setAttribute("y", st.pageTop); W.pageRect.setAttribute("height", 1060 - st.pageTop);
    W.pageTitle.style.top = `${st.pageTop + 14}px`;
    const lineCol = st.pageMute ? mixHex(st.pageHero ? PAL.hero : PAL.ink, PAL.muted, st.pageMute) : (st.pageHero ? mixHex(PAL.ink, PAL.hero, st.pageHero) : PAL.ink);
    W.pageLines.forEach((l, i) => {
      const y = st.pageTop + 112 + i * 31;
      l.setAttribute("y1", y); l.setAttribute("y2", y);
      l.setAttribute("stroke", lineCol);
      l.setAttribute("opacity", y < 1040 && i < st.pageLines ? 1 : 0);
    });
    W.scanBar.setAttribute("y", st.scan < 0 ? -100 : lerp(st.pageTop + 96, 1030, st.scan));
    W.scanBar.setAttribute("opacity", st.scan < 0 || st.scan >= 1 ? 0 : 1);
    // card
    W.card.style.opacity = st.card;
    W.card.style.transform = `scale(${st.cardScale})`;
    W.card.style.borderColor = st.cardHero ? mixHex(PAL.ink, PAL.hero, st.cardHero) : PAL.ink;
    W.cardRows.forEach((d, i) => { d.style.opacity = i < st.cardLines ? 1 : 0; });
    if (st.underline >= 0) {
      const chars = MAP_LINES[st.underline].length;
      W.underline.style.top = `${CARD.pad - 7 + (st.underline + 2) * CARD.lh - 8}px`;
      W.underline.style.width = `${chars * 36}px`;
      W.underline.style.transform = `scaleX(${st.underlineU})`;
      W.underline.style.opacity = st.underlineU > 0 ? 1 : 0;
    } else W.underline.style.opacity = 0;
    // arrows
    W.arrows.forEach((ar, i) => {
      const u = st.arrows[i], col = st.arrowHero === i ? PAL.hero : PAL.dim;
      ar.p.setAttribute("stroke-dasharray", `${ar.len + 2} ${ar.len + 2}`);
      ar.p.setAttribute("stroke-dashoffset", (ar.len + 2) * (1 - u));
      ar.p.setAttribute("stroke", col); ar.head.setAttribute("fill", col);
      ar.head.setAttribute("opacity", u >= 0.98 ? 1 : 0);
      ar.g.setAttribute("opacity", u > 0 ? st.arrowAlpha : 0);
    });
    // label
    W.label.textContent = st.label;
    W.label.style.opacity = st.labelAlpha * (1 - st.page);
    W.label.style.color = st.labelHero ? mixHex(PAL.dim, PAL.hero, st.labelHero) : PAL.dim;
    // cast
    const g = st.agent;
    CAST.place(W.agent, g.x, g.y, AGENT.s);
    CAST.pose(W.agent, { armL: g.armL, armR: g.armR, lean: g.lean, tilt: g.tilt });
    CAST.blink(W.agent, g.blink);
    const h = st.human;
    CAST.show(W.human, h.alpha);
    CAST.pose(W.human, { armL: h.armL, armR: h.armR, lean: h.lean, tilt: h.tilt });
    CAST.face(W.human, h.face);
  }

  window.EP2 = { GRID, cell, LANES, WIN, CARD, LABEL, AGENT, HUMAN, AGENT_BESIDE, MAP_LINES, TARGETS, AUTH, TARGET_FILES,
                 AUTH_IN_WIN, fileIndex, EMPTY, MAP, PILE, SPILL, SEAM, build, mixHex, lerp, clamp01 };
})();
