// jev.js — shared parts for 011-jev-decision-models-iso, loaded after iso.js
// (the isometric kit from 009). Three things keep their identity from beat to
// beat, so every beat draws them from here:
//   the probability pillars  one extruded column per choice; height = probability
//   the machine              a labelled slab (the Jev box, a model, a head)
//   flat cards and chips     the input ticket, the choices, tags
// Everything is a pure function of its arguments.
(function () {
  const { P, COL, mix, css, clamp01 } = ISO;

  // ---- the example, fixed for the whole Short (008's ledger) ----
  const CHOICES = ["bug", "query", "spam"];              // a support ticket, routed
  const TICKET = "I can't log in";                       // the input that is decided for good
  const CYCLE_INPUTS = ["order status?", "wrong size"];  // tickets that drop in under the hook question
  const CYCLE_PROBS = [[0.20, 0.05, 0.75], [0.10, 0.82, 0.08]];
  const FINAL_PROBS = [0.91, 0.06, 0.03];                // bug / query / spam for TICKET
  const STREAM = ['{"type": "bug",', '"why": "login"}']; // what the LLM types, 30 glyphs
  const CHOICE_COL = COL.tokens;                         // bug teal, query blue, spam gold

  // ---- a slab with a front face (machine, model, head) ----
  // o: x, y (world centre), z0, h, half (half-width), depth (half-depth), oy,
  //    col (front tint RGB, default panel), hero 0..1 (toward magenta), alpha
  function slab(g, o) {
    const x = o.x || 0, y = o.y || 0, z0 = o.z0 || 0, z1 = z0 + o.h, half = o.half, d = o.depth == null ? 30 : o.depth;
    const hero = o.hero || 0, prev = g.globalAlpha; g.globalAlpha = prev * (o.alpha == null ? 1 : o.alpha);
    const q = (px, py, pz) => P(px, py, pz, o.oy);
    const edge = css(mix(COL.slabEdge, COL.hero, hero)), front = o.col || COL.panel;
    ISO.poly(g, [q(x + half, y - d, z1), q(x + half, y + d, z1), q(x + half, y + d, z0), q(x + half, y - d, z0)], css(mix(COL.slabA, COL.hero, hero * 0.45), 0.85));
    ISO.poly(g, [q(x - half, y - d, z1), q(x + half, y - d, z1), q(x + half, y + d, z1), q(x - half, y + d, z1)], css(mix(COL.slabTop, COL.hero, hero * 0.75)));
    ISO.poly(g, [q(x - half, y + d, z1), q(x + half, y + d, z1), q(x + half, y + d, z0), q(x - half, y + d, z0)], css(mix(front, COL.hero, hero * 0.3), 1.2), edge);
    g.lineWidth = 4 + 3 * hero; g.strokeStyle = edge; g.lineJoin = "round"; g.beginPath();
    [[x - half, z1], [x + half, z1], [x + half, z0], [x - half, z0], [x - half, z1]].forEach(([px, pz], i) => { const p = q(px, y + d, pz); i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); });
    g.stroke(); g.globalAlpha = prev;
  }
  // screen point at the centre of a slab's front face (for its label)
  const slabFront = (o) => P(o.x || 0, (o.y || 0) + (o.depth == null ? 30 : o.depth), (o.z0 || 0) + o.h / 2, o.oy);
  // screen-space shear of an upright plane facing the viewer, for flat text laid on a front face
  const SHEAR = (P(100, 0, 0, 0)[1] - P(0, 0, 0, 0)[1]) / (P(100, 0, 0, 0)[0] - P(0, 0, 0, 0)[0]);
  // A flat label laid on a front face, centred on screen point c. Keep the
  // matrix when you scale it: matrix(s, SHEAR*s, 0, s, 0, 0).
  function planeLabel(root, text, c, o = {}) {
    const el = document.createElement("div"), size = o.size || 60, w = o.width || 520;
    el.textContent = text;
    el.style.cssText = `position:absolute;left:${(c[0] - w / 2).toFixed(1)}px;top:${(c[1] - size * 0.6).toFixed(1)}px;width:${w}px;height:${Math.round(size * 1.2)}px;` +
      `text-align:center;font-size:${size}px;line-height:${Math.round(size * 1.2)}px;white-space:nowrap;color:${o.color || css(COL.text)};` +
      `transform:matrix(1, ${SHEAR.toFixed(4)}, 0, 1, 0, 0);transform-origin:50% 50%;`;
    el.setAttribute("data-layout-allow-occlusion", ""); // it sits on a canvas-drawn face on purpose
    root.appendChild(el); return el;
  }

  // ---- the probability pillars ----
  // Geometry o: oy (screen y of the floor under them), x (world centre, default 0),
  // y (world depth, default 0), pitch (default 210), size (pillar side, default 120),
  // H (height of probability 1.0, default 300).
  const G = (o = {}) => ({ oy: o.oy, x: o.x || 0, y: o.y || 0, pitch: o.pitch || 210, size: o.size || 120, H: o.H || 300 });
  const pillarX = (i, o) => { const k = G(o); return k.x + (i - 1) * k.pitch; };
  // probs: three numbers 0..1. opts: alpha, hero [h0,h1,h2] (toward magenta), plate (false to hide the base)
  function pillars(g, probs, o = {}, opts = {}) {
    const k = G(o), s = k.size / 2, prev = g.globalAlpha; g.globalAlpha = prev * (opts.alpha == null ? 1 : opts.alpha);
    if (opts.plate !== false) ISO.box(g, k.x - k.pitch - s - 18, k.y - s - 18, k.x + k.pitch + s + 18, k.y + s + 18, 0, 8, k.oy, COL.plate, { shade: [1, 0.7, 0.5], edge: css(COL.muted) });
    for (let i = 0; i < 3; i++) {
      const cx = pillarX(i, o), h = 6 + clamp01(probs[i]) * k.H;
      const col = mix(CHOICE_COL[i], COL.hero, (opts.hero && opts.hero[i]) || 0);
      ISO.box(g, cx - s, k.y - s, cx + s, k.y + s, 8, 8 + h, k.oy, col);
    }
    g.globalAlpha = prev;
  }
  // screen anchors: above pillar i's top (for its value), and in front of its foot (for its name)
  const pillarTop = (i, p, o) => { const k = G(o); return P(pillarX(i, o), k.y, 8 + 6 + clamp01(p) * k.H, k.oy); };
  const pillarFoot = (i, o) => { const k = G(o); return P(pillarX(i, o), k.y + k.size / 2 + 18, 0, k.oy); };
  // DOM labels for the pillars: names (in the choice colours) under the feet and values above the tops.
  // Call set(probs, opts) every frame: it writes the values and moves them with the tops.
  // opts: alpha, valueAlpha, nameAlpha.
  function makePillarLabels(root, o = {}, lo = {}) {
    const nameSize = lo.nameSize || 60, valSize = lo.valueSize || 60;
    const mk = (size, color) => { const el = document.createElement("div"); el.style.cssText = `position:absolute;left:0;top:0;width:240px;height:${Math.round(size * 1.15)}px;text-align:center;font-size:${size}px;line-height:${Math.round(size * 1.15)}px;white-space:nowrap;color:${color};font-variant-numeric:tabular-nums;`; el.setAttribute("data-layout-allow-occlusion", ""); root.appendChild(el); return el; };
    const names = CHOICES.map((c, i) => { const el = mk(nameSize, css(CHOICE_COL[i])); el.textContent = c; return el; });
    const values = CHOICES.map(() => mk(valSize, css(COL.text)));
    return {
      names, values,
      set(probs, opts = {}) {
        const a = opts.alpha == null ? 1 : opts.alpha;
        for (let i = 0; i < 3; i++) {
          const f = pillarFoot(i, o), t = pillarTop(i, probs[i], o);
          names[i].style.transform = `translate(${(f[0] - 120).toFixed(1)}px, ${(f[1] + 10).toFixed(1)}px)`;
          names[i].style.opacity = (a * (opts.nameAlpha == null ? 1 : opts.nameAlpha)).toFixed(3);
          values[i].textContent = clamp01(probs[i]).toFixed(2);
          values[i].style.transform = `translate(${(t[0] - 120).toFixed(1)}px, ${(t[1] - valSize * 1.15 - 34).toFixed(1)}px)`;
          values[i].style.opacity = (a * (opts.valueAlpha == null ? 1 : opts.valueAlpha)).toFixed(3);
        }
      },
    };
  }

  // ---- flat cards and chips (DOM, screen space) ----
  // A rounded card: the input ticket, a choice chip, a tag. Position it in
  // render(t) with el.style.transform = translate(...) and opacity.
  // o: size (font px, default 60), color (text), border (css colour), mono (true for code)
  function card(root, text, o = {}) {
    const el = document.createElement("div"), size = o.size || 60;
    el.textContent = text;
    el.style.cssText = `position:absolute;left:0;top:0;padding:${Math.round(size * 0.18)}px ${Math.round(size * 0.42)}px;border-radius:${Math.round(size * 0.3)}px;` +
      `background:${css(COL.panel)};border:5px solid ${o.border || css(COL.dim)};font-size:${size}px;line-height:${Math.round(size * 1.15)}px;white-space:nowrap;` +
      `color:${o.color || css(COL.text)};` + (o.mono ? "font-family:monospace;font-weight:700;" : "");
    root.appendChild(el); return el;
  }

  window.JV = { CHOICES, TICKET, CYCLE_INPUTS, CYCLE_PROBS, FINAL_PROBS, STREAM, CHOICE_COL, SHEAR,
                slab, slabFront, planeLabel, pillars, pillarX, pillarTop, pillarFoot, makePillarLabels, card };
})();
