// wiki.js — the episode kit for 012 ep03 (LLM Wiki: the four layers).
// The building in cross-section: the human at the board upstairs, the glass
// case on the stairs, the janitor between floors, two agents writing pages in
// the basement. Draws only with CAST parts (videos/_shared/web/cast/cast.js)
// plus the building lines, the callout card, the link and the conflict marks,
// which the cast kit lacks (listed in the hand-off).
//
// Linked into a beat as `kit/` after vendor/, iso/ and cast/:
//   <script src="kit/wiki.js"></script>
// One call per frame: K.draw(S), where S is a full state object. Every beat
// opens on WIKI.SEAM[n-1] and ends on WIKI.SEAM[n], so cuts match by
// construction. Pure functions of S only: no clocks, no randomness.
(function () {
  const { PAL } = CAST;
  const lerp = (a, b, u) => a + (b - a) * u;
  const clamp01 = (u) => Math.max(0, Math.min(1, u));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const pulse = (u) => Math.sin(Math.PI * clamp01(u));            // 0 → 1 → 0

  // ---- the building (ledger, storyboard.md) ----
  const B = { left: 80, right: 930, roof: 262, slab: 700, open: 600, floor: 1310 };
  // Between the floors: a ladder down the hatch (rails x 600 and 648) and a
  // landing on the right (y 1000, x 652–930) that holds the case and the
  // janitor. A figure on the ladder stands at x LADDER.cx.
  const LADDER = { x0: 600, x1: 648, cx: 624, top: B.slab, bottom: B.floor, rung: 44 };
  const LANDING = { x0: 652, x1: B.right, y: 1000 };
  const POS = {
    human: [160, B.slab], board: [262, 396], vit: [806, 862],
    jan: [716, LANDING.y], agentA: [175, B.floor], agentB: [410, B.floor],
    pageA: [224, 1036], pageB: [459, 1036],
    wall: [96, 194, 292, 390, 488], wallY: 728, old: [[668, 1182], [726, 1184]],
  };
  const S_FIG = { human: 0.66, agent: 0.58, jan: 0.5 }, S_PAGE = { held: 0.5, wall: 0.36 };
  const BOARD = { w: 312, h: 270, cards: [2, 1, 3] };
  const CALLOUT = { left: 150, top: 712, width: 760, height: 296, lines: [["hash", "a3f9c2"], ["branch", "fix/auth"], ["commit", "9e1b04"]] };
  const HEROES = [null, "pages", "board", "case", "rules", "janitor", "broom", "callout"];

  // The state every beat fills. Numbers only (plus hero / face strings).
  const BASE = {
    hero: null,               // one of HEROES
    write: 1,                 // 0..1 amplitude of the agents' writing (0 = still)
    pen: 0,                   // writing phase in cycles (drive it from t; only matters while write > 0)
    fill: [0.55, 0.35],       // how much of each held page is written, 0..1 (A, B)
    wall: 3,                  // pinned pages on the basement wall, 3..5 (fractional fades the next one in)
    hand: 0,                  // 0..1 agent A passes a page to agent B (beat 2), back to 0 = done
    callout: 0, lines: 0,     // callout card grown 0..1; lines shown 0..3
    link: 0,                  // 0..1 the dashed link from the board's card to agent B's page
    kanban: 0,                // 0..1 one card slides from column 1 to column 2
    glint: 0,                 // 0..1 one glint across the glass case
    conflict: [0, 0],         // 0..1 the magenta conflicting line drawn on page B, then its copy on page A
    swept: 0,                 // 0..1 the conflict lines swept away
    old: 0,                   // 0..1 the two old pages swept off
    glow: null,               // [name, 0..1]: a short teal pulse on "pageA" | "pageB" | "board"
    human: { armL: 22, armR: 22, tilt: 0, lean: 0, face: "smile" },
    jan: { x: POS.jan[0], y: POS.jan[1], lean: 0, armR: 24, tilt: 0 },
  };
  const clone = (o) => JSON.parse(JSON.stringify(o));
  const merge = (a, b) => {
    const o = clone(a);
    Object.keys(b || {}).forEach((k) => {
      o[k] = (b[k] && typeof b[k] === "object" && !Array.isArray(b[k])) ? Object.assign({}, a[k], b[k]) : b[k];
    });
    return o;
  };
  // Where each beat starts and ends (SEAM[n] = end of beat n = start of beat n+1).
  const SEAM = [];
  SEAM[0] = merge(BASE, {});
  SEAM[1] = merge(BASE, { write: 0, pen: 0, fill: [0.7, 0.5] });
  SEAM[2] = merge(SEAM[1], { wall: 5, fill: [0.9, 0.75] });
  SEAM[3] = merge(SEAM[2], { hero: "board", link: 1, kanban: 1, human: { armR: 100, tilt: 6 } });
  SEAM[4] = merge(SEAM[3], { hero: "rules", link: 0, human: { armR: 22, tilt: 0 } });
  SEAM[5] = merge(SEAM[4], { hero: null, conflict: [1, 1], swept: 1, old: 1, jan: { x: 700, y: B.floor, lean: 0, armR: 24, tilt: 0 } });
  SEAM[6] = merge(SEAM[5], { jan: { x: POS.jan[0], y: POS.jan[1] } });

  // ---- mount: build every part once ----
  function mount(root) {
    const svg = CAST.layer(root);
    const L = (x1, y1, x2, y2, col, w, extra) => CAST.line(svg, x1, y1, x2, y2, Object.assign({ stroke: col, "stroke-width": w, "stroke-linecap": "round" }, extra || {}));
    // ground outside, walls, roof, slab, floor
    L(0, B.slab, B.left, B.slab, PAL.muted, 5); L(B.right, B.slab, 1080, B.slab, PAL.muted, 5);
    L(B.left, B.roof, B.right, B.roof, PAL.ink, 9);
    L(B.left, B.roof, B.left, B.floor, PAL.ink, 9); L(B.right, B.roof, B.right, B.floor, PAL.ink, 9);
    L(B.left, B.slab, B.open, B.slab, PAL.ink, 12);
    L(B.left, B.floor, B.right, B.floor, PAL.ink, 9);
    // the ladder down the hatch, and the landing between the floors
    L(LADDER.x0, LADDER.top, LADDER.x0, LADDER.bottom, PAL.ink, 7); L(LADDER.x1, LADDER.top, LADDER.x1, LADDER.bottom, PAL.ink, 7);
    for (let y = LADDER.top + LADDER.rung; y < LADDER.bottom - 10; y += LADDER.rung) L(LADDER.x0, y, LADDER.x1, y, PAL.ink, 5);
    L(LANDING.x0, LANDING.y, LANDING.x1, LANDING.y, PAL.ink, 10);

    // upstairs: the board and the human
    const board = CAST.board(svg, { x: POS.board[0], y: POS.board[1], w: BOARD.w, h: BOARD.h, cards: BOARD.cards });
    const cards = Array.from(board.el.querySelectorAll("rect")).slice(1);   // col0: 0,1 · col1: 2 · col2: 3,4,5
    const human = CAST.human(svg, { x: POS.human[0], y: POS.human[1], s: S_FIG.human });
    // the stairs: the case on the wall, the janitor on the flight
    const vit = CAST.vitrine(svg, { x: POS.vit[0], y: POS.vit[1], s: 0.38 });
    const vitFrame = vit.el.querySelector("rect");
    const glint = CAST.line(vit.el, 0, 0, 0, 0, { stroke: PAL.glass, "stroke-width": 10, "stroke-linecap": "round", opacity: 0 });
    const jan = CAST.janitor(svg, { x: POS.jan[0], y: POS.jan[1], s: S_FIG.jan });
    // basement: wall pages, the two old pages, agents and their held pages
    const wall = POS.wall.map((x, i) => CAST.page(svg, { x, y: POS.wallY, s: S_PAGE.wall, hash: ["a3f9c2", "7be014", "c51d9a", "04fe3b", "9e1b04"][i] }));
    const old = POS.old.map(([x, y], i) => {
      const p = CAST.page(svg, { x, y, s: S_PAGE.wall, hash: ["2d77e1", "b80c46"][i] });
      p.el.querySelectorAll("rect, line, text").forEach((el) => {
        if (el.getAttribute("stroke")) { el.setAttribute("stroke", PAL.muted); el.removeAttribute("data-tint"); }
      });
      p.el.querySelector("text").remove();                       // old: no hash left to read
      p.el.querySelector("rect").setAttribute("stroke-dasharray", "16 12");
      return p;
    });
    const agentA = CAST.agent(svg, { x: POS.agentA[0], y: POS.agentA[1], s: S_FIG.agent });
    const agentB = CAST.agent(svg, { x: POS.agentB[0], y: POS.agentB[1], s: S_FIG.agent });
    const pageA = CAST.page(svg, { x: POS.pageA[0], y: POS.pageA[1], s: S_PAGE.held, hash: "a3f9c2" });
    const pageB = CAST.page(svg, { x: POS.pageB[0], y: POS.pageB[1], s: S_PAGE.held, hash: "a3f9c2" });
    [pageA, pageB].forEach((p) => {
      p.lines = Array.from(p.el.querySelectorAll("line")).map((el) => ({ el, x1: +el.getAttribute("x1"), x2: +el.getAttribute("x2") }));
      // the conflicting rule: one magenta line over the page's 4th line
      const y = +p.lines[3].el.getAttribute("y1");
      p.mark = CAST.line(p.el, 24, y, 24, y, { stroke: PAL.hero, "stroke-width": 12, "stroke-linecap": "round", opacity: 0 });
      p.markW = p.lines[3].x2 - 24;
    });
    // the link: board card (column 2) down to page B
    const linkFrom = [POS.board[0] + BOARD.w / 3 * 1.5, POS.board[1] + 26 + 56];
    const linkTo = [POS.pageB[0] + 60, POS.pageB[1]];
    const link = CAST.line(svg, linkFrom[0], linkFrom[1], linkFrom[0], linkFrom[1], { stroke: PAL.hero, "stroke-width": 7, "stroke-linecap": "round", "stroke-dasharray": "18 16", opacity: 0 });
    // the dim behind the callout (above every part)
    const dim = CAST.node("rect", { x: 0, y: B.roof - 40, width: 1080, height: B.floor - B.roof + 80, fill: PAL.bg, opacity: 0 }, svg);

    // the callout card: DOM, so check sees its text
    const card = document.createElement("div");
    card.style.cssText = `position:absolute;left:${CALLOUT.left}px;top:${CALLOUT.top}px;width:${CALLOUT.width}px;height:${CALLOUT.height}px;` +
      `background:${PAL.panel};border:7px solid ${PAL.data};border-radius:18px;padding:30px 44px;opacity:0;transform-origin:50% 50%;`;
    const rows = CALLOUT.lines.map(([k, v]) => {
      const r = document.createElement("div");
      r.style.cssText = "font-size:60px;line-height:78px;white-space:nowrap;opacity:0;";
      const a = document.createElement("span"), b = document.createElement("span");
      a.textContent = k + " "; b.textContent = v;
      a.style.color = PAL.dim; b.style.color = PAL.data;
      [r, a, b].forEach((el) => { el.style.fontFamily = "monospace"; });   // set from script (beat-brief trap)
      r.appendChild(a); r.appendChild(b); card.appendChild(r);
      return r;
    });
    root.appendChild(card);
    const cardFrom = [POS.pageB[0] + 46 - (CALLOUT.left + CALLOUT.width / 2), POS.pageB[1] + 60 - (CALLOUT.top + CALLOUT.height / 2)];

    // ---- draw(S) ----
    const inkFig = (part, on, col = PAL.ink) => {
      part.el.querySelectorAll("line, circle, rect, path").forEach((el) => {
        if (part.broom && (el === part.broom.handle || el === part.broom.head)) return;
        const s = el.getAttribute("stroke");
        if (s === PAL.ink || s === PAL.hero) el.setAttribute("stroke", on ? PAL.hero : col);
      });
    };
    const heroPage = (p, on) => CAST.hero(p, on);
    function draw(S) {
      const h = S.hero;
      // heroes
      [pageA, pageB].concat(wall).forEach((p) => heroPage(p, h === "pages"));
      CAST.hero(board, h === "board");
      vitFrame.setAttribute("stroke", h === "case" ? PAL.hero : PAL.glass);
      vitFrame.setAttribute("stroke-opacity", h === "case" ? 1 : 0.6);
      vitFrame.setAttribute("stroke-width", h === "case" ? 16 : 6);       // thin glass reads faint at phone size when lit
      CAST.hero(vit.items.rules, h === "rules");
      inkFig(jan, h === "janitor");
      [jan.broom.handle, jan.broom.head].forEach((el) => el.setAttribute("stroke", h === "broom" ? PAL.hero : PAL.dim));
      card.style.borderColor = h === "callout" ? PAL.hero : PAL.data;

      // the agents write: right arm moves while write > 0
      const wob = Math.sin(2 * Math.PI * S.pen) * S.write;
      const wobB = Math.sin(2 * Math.PI * (S.pen + 0.37)) * S.write;
      const hand = pulse(S.hand);
      CAST.pose(agentA, { armR: 58 + 10 * wob + 30 * hand, armL: 22, tilt: 4 * wob });
      CAST.pose(agentB, { armR: 58 + 10 * wobB, armL: 22 + 40 * hand, tilt: 4 * wobB - 6 * hand });
      // page A slides toward B and back while it is handed over
      pageA.el.setAttribute("transform", `translate(${POS.pageA[0] + 120 * hand} ${POS.pageA[1] - 30 * hand}) scale(${S_PAGE.held})`);
      [[pageA, S.fill[0]], [pageB, S.fill[1]]].forEach(([p, f]) => {
        const k = f * p.lines.length;
        p.lines.forEach((l, i) => { const u = clamp01(k - i); l.el.setAttribute("x2", lerp(l.x1, l.x2, u)); l.el.setAttribute("opacity", u > 0 ? 1 : 0); });
      });
      // the wall pages: three always, the 4th and 5th fade in as wall goes 3 → 5
      wall.forEach((p, i) => CAST.show(p, i < 3 ? 1 : clamp01(S.wall - i)));
      // the old pages, swept right (away from the janitor and the ladder) and out
      old.forEach((p, i) => {
        const u = clamp01(S.old * 1.4 - (1 - i) * 0.4);
        p.el.setAttribute("transform", `translate(${POS.old[i][0] + 90 * u} ${POS.old[i][1] + 20 * u}) rotate(${18 * u}) scale(${S_PAGE.wall})`);
        CAST.show(p, 1 - u);
      });
      // the conflict: page B first, then its copy on page A; swept fades both
      [[pageB, S.conflict[0]], [pageA, S.conflict[1]]].forEach(([p, u]) => {
        p.mark.setAttribute("x2", 24 + p.markW * u);
        p.mark.setAttribute("opacity", u > 0 ? 1 - S.swept : 0);
      });
      // teal glow pulse on a named part
      [pageA, pageB].forEach((p) => p.el.querySelector("rect").setAttribute("stroke-width", 7));
      if (S.glow) {
        const [name, u] = S.glow, w = 7 + 9 * pulse(u);
        if (name === "pageA") pageA.el.querySelector("rect").setAttribute("stroke-width", w);
        if (name === "pageB") pageB.el.querySelector("rect").setAttribute("stroke-width", w);
        if (name === "board") board.el.querySelector("rect").setAttribute("stroke-width", w);
      } else board.el.querySelector("rect").setAttribute("stroke-width", 7);
      // kanban: column 1's second card slides into column 2
      cards[1].setAttribute("transform", `translate(${BOARD.w / 3 * S.kanban} 0)`);
      // the link draws down from the card
      link.setAttribute("x2", lerp(linkFrom[0], linkTo[0], S.link));
      link.setAttribute("y2", lerp(linkFrom[1], linkTo[1], S.link));
      link.setAttribute("opacity", S.link > 0 ? 1 : 0);
      link.setAttribute("stroke", h === "board" ? PAL.hero : PAL.dim);
      // glint: one line across the case glass
      const gu = S.glint, gx = lerp(-40, 330, gu);
      glint.setAttribute("x1", gx); glint.setAttribute("y1", 340); glint.setAttribute("x2", gx + 110); glint.setAttribute("y2", 20);
      glint.setAttribute("opacity", 0.9 * pulse(gu));
      // people
      const H = S.human;
      CAST.pose(human, { armL: H.armL, armR: H.armR, tilt: H.tilt, lean: H.lean });
      CAST.face(human, H.face);
      const J = S.jan;
      CAST.place(jan, J.x, J.y, S_FIG.jan);
      CAST.pose(jan, { armR: J.armR, lean: J.lean, tilt: J.tilt });
      // the callout card
      const c = S.callout;
      card.style.opacity = clamp01(c * 3);
      card.style.transform = `translate(${cardFrom[0] * (1 - c)}px, ${cardFrom[1] * (1 - c)}px) scale(${lerp(0.14, 1, c)})`;
      rows.forEach((r, i) => { r.style.opacity = clamp01(S.lines - i); });
      dim.setAttribute("opacity", 0.62 * c);
    }
    // the callout card covers the scene's texture text on purpose (beat 2)
    svg.querySelectorAll("text").forEach((el) => { el.setAttribute("data-layout-allow-occlusion", ""); el.setAttribute("data-layout-allow-overlap", ""); });
    return { svg, draw, parts: { human, board, cards, vit, jan, agentA, agentB, pageA, pageB, wall, old, link, card } };
  }

  // A state between two states (numbers lerp, strings and hero switch at u >= 0.5).
  function mix(a, b, u) {
    if (typeof a === "number") return lerp(a, b, u);
    if (Array.isArray(a)) return a.map((v, i) => mix(v, b[i], u));
    if (a && typeof a === "object") { const o = {}; Object.keys(a).forEach((k) => { o[k] = mix(a[k], b[k], u); }); return o; }
    return u < 0.5 ? a : b;
  }
  const E = () => ({ io: gsap.parseEase("power2.inOut"), out: gsap.parseEase("power2.out"), inn: gsap.parseEase("power2.in"),
                     back: gsap.parseEase("back.out(1.4)"), sine: gsap.parseEase("sine.inOut") });

  window.WIKI = { B, LADDER, LANDING, POS, CALLOUT, HEROES, BASE, SEAM, mount, merge, clone, mix, lerp, clamp01, seg, pulse, E };
})();
