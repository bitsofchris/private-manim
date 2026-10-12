// ep08.js — episode 8's numbers, layout and rest states (the dot product).
// Linked into each beat as `ep/`, after vendor/gsap, iso/iso.js and vec/vec.js:
//   ln -s ../_ep NN_beat/ep
// Everything drawn comes from the shared plane kit (VEC); this file holds the
// ledger (storyboard.md), where things sit, and the states beats open and end
// on. Beats never edit it; they draw their changes on top of a state.
//
// Revision 2 (Chris, after the first cut): the 3-D pairwise example
// ([1, 2, 3] · [4, −1, 0]) and its readout are gone. The math is shown on the
// turning pair itself: a = [ 1, 1 ], b's numbers, and the pairwise sum
// "1 × 2 + 1 × 2" live under the readout, so 4, 0 and −4 are visibly computed.
(function () {
  const { COL, css, mix, lerp, clamp01 } = ISO;
  const { fmtv, SLOT } = VEC;

  // ---- the ledger (storyboard.md) ----
  // The turning pair (2-D, on the plane): a fixed, b turns about the origin, |b| = 2|a|.
  // th = the angle from a to b in degrees (counter-clockwise); a · b = 1·bx + 1·by = 4 cos th.
  // Landmarks on grid points: th 0 -> b [2, 2], 4; th 90 -> b [−2, 2], 0; th 180 -> b [−2, −2], −4.
  const A2 = [1, 1];
  const RB = 2 * Math.SQRT2, A_DEG = 45;
  const bAt = (th) => { const r = (A_DEG + th) * Math.PI / 180; return [RB * Math.cos(r), RB * Math.sin(r)]; };
  const dotAt = (th) => { const b = bAt(th); return A2[0] * b[0] + A2[1] * b[1]; };
  const TH = { CANON: 60, ALIGNED: 0, PERP: 90, OPPOSITE: 180 };
  const CODE = ["torch.dot(a, b)", "# 1·2 + 1·2 = 4"];
  // The embedding payoff: three words as 2-D vectors (a toy; real embeddings have hundreds of numbers).
  const WORDS = { king: [2, 1], queen: [1.5, 2], banana: [-1, 2] };
  const KQ = 5, KB = 0;                                  // king · queen, king · banana
  // A value shows to one decimal while it moves and exactly at the landmarks:
  // 2.8, 4, 0, −4 (never "4.0", never "−0").
  const fmtd = (v) => { const r = Math.round(v * 10) / 10; return Math.abs(r) < 0.05 ? "0" : fmtv(r); };

  // ---- layout (px, 1080 x 1920; stage y 230-1100) ----
  // The plane: 145 px a step. b's whole sweep (45° to 225°) stays between y 395
  // (straight up) and 1095 (th 180), under the two readout rows and above the band.
  const PLANE = { step: 145, ox: 507, oy: 805, ax: { w: -2.6, e: 2.6, s: -2.0, n: 2.6 } };
  // Readouts: the lead text right-aligned to leadR, the number left-aligned at numL,
  // so the number never pushes the words around while it ticks. Two rows.
  const RO = { size: 64, leadR: 700, numL: 724, top: [250, 326] };
  // The pairwise sum under the readout (row 2): 1 × bx + 1 × by, fixed slots so it never jitters.
  // Slots: a0 × b0 + a1 × b1 (a's numbers teal, b's blue, operators dim).
  const FORM = { size: 60, top: 326, cx: 507, w: [50, 56, 130, 64, 50, 56, 130] };
  // The tip labels: a's beside its tip; b's only near a landmark (its text and offset per landmark).
  const TIP = {
    a: { dx: 150, dy: 30 },
    b: [{ th: 0, text: "[ 2, 2 ]", dx: -110, dy: -50 },
        { th: 90, text: "[ −2, 2 ]", dx: 110, dy: -50 },
        { th: 180, text: "[ −2, −2 ]", dx: 240, dy: -40 }],
  };
  const CODE_TOP = 1115;                                 // the code card, centred, at the band top (captions sit at the band bottom)

  // ---- DOM parts, made once per beat ----
  function readout(root) {
    const lead = ISO.label(root, "", { size: RO.size, color: css(COL.dim), width: 640, align: "right" });
    const num = ISO.label(root, "", { size: RO.size, color: css(COL.hero), width: 240, align: "left" });
    num.style.fontVariantNumeric = "tabular-nums"; num.style.transformOrigin = "20% 50%";
    return {
      lead, num,
      // set(text, value | string, { row, alpha, scale (number only), col (number), leadCol })
      set(text, v, o = {}) {
        const top = RO.top[o.row || 0], a = o.alpha == null ? 1 : o.alpha, s = o.scale == null ? 1 : o.scale;
        if (lead.textContent !== text) lead.textContent = text;
        const nt = typeof v === "number" ? fmtd(v) : v;
        if (num.textContent !== nt) num.textContent = nt;
        lead.style.transform = `translate(${(RO.leadR - 640).toFixed(1)}px, ${top}px)`;
        num.style.transform = `translate(${RO.numL}px, ${top}px) scale(${s.toFixed(4)})`;
        lead.style.opacity = num.style.opacity = a.toFixed(3);
        lead.style.color = css(o.leadCol || COL.dim); num.style.color = css(o.col || COL.hero);
      },
    };
  }
  // the pairwise sum: 7 fixed slots. .set(th, { alpha, k: [7 alphas] (build in slot by slot) })
  function formula(root) {
    const cols = [SLOT[0], COL.dim, SLOT[1], COL.dim, SLOT[0], COL.dim, SLOT[1]];
    const total = FORM.w.reduce((s, v) => s + v, 0);
    let x = FORM.cx - total / 2;
    const slots = FORM.w.map((wd, i) => {
      const el = ISO.label(root, "", { size: FORM.size, color: css(cols[i]), width: wd, align: "center" });
      el.style.fontVariantNumeric = "tabular-nums"; el.dataset.left = String(x); x += wd; return el;
    });
    const txt = ["1", "×", "", "+", "1", "×", ""];
    return {
      slots,
      set(th, o = {}) {
        const b = bAt(th), a = o.alpha == null ? 1 : o.alpha, k = o.k || [1, 1, 1, 1, 1, 1, 1];
        txt[2] = fmtd(b[0]); txt[6] = fmtd(b[1]);
        slots.forEach((el, i) => {
          if (el.textContent !== txt[i]) el.textContent = txt[i];
          el.style.transform = `translate(${el.dataset.left}px, ${FORM.top}px)`;
          el.style.opacity = clamp01(a * k[i]).toFixed(3);
        });
      },
    };
  }
  // P: ro[0], ro[1] readouts; form (the pairwise sum); tipA, tipB (vector labels at the tips);
  // code (codeCard; spans[0] = torch. / dot / (a, b), spans[1] = # / 1·2 / + 1·2 / = 4);
  // words {king, queen, banana} labels.
  function parts(root) {
    const tipA = VEC.label(root, "[ 1, 1 ]", { color: css(SLOT[0]), width: 300, size: 60 });
    const tipB = VEC.label(root, "", { color: css(SLOT[1]), width: 300, size: 60 });
    const code = VEC.codeCard(root, [
      [["torch."], ["dot"], ["(a, b)"]],
      [["# ", COL.dim], ["1·2", COL.dim], [" + 1·2", COL.dim], [" = 4", COL.dim]],
    ]);
    const words = {};
    Object.keys(WORDS).forEach((w, i) => { words[w] = VEC.label(root, w, { color: css(SLOT[i]), width: 260 }); });
    return { ro: [readout(root), readout(root)], form: formula(root), tipA, tipB, code, words };
  }

  // ---- placement ----
  const put = (el, left, top, alpha = 1, scale = 1) => {
    el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${scale.toFixed(4)})`;
    el.style.opacity = clamp01(alpha).toFixed(3);
  };
  // The numbers on the turning pair: the pairwise sum (row 2), a's tip label, and b's tip label
  // near a landmark (full within 3°, gone by 12°). o: alpha (all), formA, aA, bA, k (formula slots).
  function nums(Pt, th, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    Pt.form.set(th, { alpha: al * (o.formA == null ? 1 : o.formA), k: o.k });
    VEC.place(Pt.tipA, A2[0], A2[1], { dx: TIP.a.dx, dy: TIP.a.dy, alpha: al * (o.aA == null ? 1 : o.aA) });
    let best = TIP.b[0];
    TIP.b.forEach((L) => { if (Math.abs(th - L.th) < Math.abs(th - best.th)) best = L; });
    const near = 1 - clamp01((Math.abs(th - best.th) - 3) / 9), b = bAt(best.th);
    if (Pt.tipB.textContent !== best.text) Pt.tipB.textContent = best.text;
    VEC.place(Pt.tipB, b[0], b[1], { dx: best.dx, dy: best.dy, alpha: al * near * (o.bA == null ? 1 : o.bA) });
  }
  // the code card at the band top: line 2's spans shown up to `n` (0..4), alpha a
  function placeCode(Pt, a = 1, n = 4, o = {}) {
    Pt.code.spans[1].forEach((s, i) => { s.style.opacity = i < n ? "1" : "0"; });
    Pt.code.at(VEC.centreLeft(Pt.code.el), CODE_TOP + (o.dy || 0), { alpha: a, scale: o.scale });
  }

  // ---- canvas ----
  function bg(g) { g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }
  // the plane alone (o: alpha). It clears the canvas: draw it first.
  function plane(g, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    VEC.view(PLANE);
    if (al <= 0.001) { bg(g); return; }
    VEC.floor(g, { alpha: 0.42 * al });
    VEC.axes(g, { alpha: al });
  }
  // the arc from angle d0 to d1 (degrees, screen-space CCW in grid terms) at radius r steps
  function arc(g, d0, d1, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001 || Math.abs(d1 - d0) < 0.5) return;
    const [cx, cy] = VEC.at(0, 0), r = (o.r || 0.7) * VEC.step();
    g.save(); g.strokeStyle = css(o.col || COL.dim, 1, al); g.lineWidth = o.width || 6; g.lineCap = "round";
    g.beginPath(); g.arc(cx, cy, r, -d0 * Math.PI / 180, -d1 * Math.PI / 180, d1 > d0); g.stroke(); g.restore();
  }
  // the right-angle mark between directions d0 and d0 + 90 (o: alpha, col, s side in steps)
  function rightMark(g, d0, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha;
    if (al <= 0.001) return;
    const s = o.s || 0.32, r0 = d0 * Math.PI / 180, r1 = (d0 + 90) * Math.PI / 180;
    const u = [Math.cos(r0) * s, Math.sin(r0) * s], v = [Math.cos(r1) * s, Math.sin(r1) * s];
    const p = [VEC.at(u[0], u[1]), VEC.at(u[0] + v[0], u[1] + v[1]), VEC.at(v[0], v[1])];
    g.save(); g.strokeStyle = css(o.col || COL.text, 1, al); g.lineWidth = 6; g.lineJoin = "round";
    g.beginPath(); g.moveTo(p[0][0], p[0][1]); g.lineTo(p[1][0], p[1][1]); g.lineTo(p[2][0], p[2][1]); g.stroke(); g.restore();
  }
  // a (fixed, teal) and b (at angle th, blue), with the angle arc between them.
  // o: alpha, aA, bA (per-arrow alpha), arcA (default 0.8), right (0..1 right-angle mark),
  // bCol (default blue), bU (b's draw progress). a is drawn over b so it shows when aligned.
  function pair(g, th, o = {}) {
    const al = o.alpha == null ? 1 : o.alpha, b = bAt(th);
    arc(g, A_DEG, A_DEG + th, { alpha: al * (o.arcA == null ? 0.8 : o.arcA), col: COL.muted });
    rightMark(g, A_DEG, { alpha: al * (o.right || 0) });
    VEC.arrow(g, [0, 0], b, { col: o.bCol || SLOT[1], alpha: al * (o.bA == null ? 1 : o.bA), u: o.bU, width: 40 });
    VEC.arrow(g, [0, 0], A2, { col: SLOT[0], alpha: al * (o.aA == null ? 1 : o.aA), width: 40 });
    VEC.puck(g, 0, 0, { alpha: al });
  }
  // label offsets beside each word's tip (px); "query" (king's label in ATTN) sits 20 px further left
  const WORD_OFF = { king: { dx: 60, dy: 90 }, queen: { dx: 110, dy: -30 }, banana: { dx: -110, dy: -40 } };
  const QUERY_DX = -20;
  // the three word arrows with their labels. o: alpha {king, queen, banana}, u (draw progress, same keys),
  // ddx {word: extra px}
  function words(g, Pt, o = {}) {
    const A = o.alpha || {}, U = o.u || {}, X = o.ddx || {};
    Object.keys(WORDS).forEach((w, i) => {
      const a = A[w] == null ? 1 : A[w], p = WORDS[w];
      VEC.arrow(g, [0, 0], p, { col: SLOT[i], alpha: a, u: U[w], width: 40 });
      const k = U[w] == null ? 1 : clamp01(U[w]);
      VEC.place(Pt.words[w], p[0] * k, p[1] * k, { dx: WORD_OFF[w].dx + (X[w] || 0), dy: WORD_OFF[w].dy, alpha: a * k });
    });
    VEC.puck(g, 0, 0);
  }

  // ---- the rest states (storyboard.md "States") ----
  // CANON      : the plane, a and b at th 60, the arc, readout "dot product = 2". (00_layout; the look)
  // ALIGNED    : the same at th 0: b [2, 2] under a [1, 1], "dot product = 4". (end of beat 1)
  // MATH       : ALIGNED + the numbers (tip labels, "1 × 2 + 1 × 2") + the code card. (end of beat 2)
  // ALIGNED_N  : ALIGNED + the numbers, no code card. (end of beat 3)
  // OPPOSITE_N : th 180: b [−2, −2], "1 × −2 + 1 × −2", "dot product = −4", arc a half turn. (end of beat 4)
  // WORDS      : the plane, king, queen, banana, the muted king-queen arc; "king · queen = 5", "king · banana = 0". (end of beat 5)
  // ATTN       : king -> "query", queen -> "key", banana gone; "query · key = 5", "attention score". (end of beat 6)
  function state(Pt, g, name) {
    // reset every DOM part to hidden / rest colours, then show this state's
    Pt.ro.forEach((r) => r.set("", "", { alpha: 0 }));
    Pt.form.set(0, { alpha: 0 }); put(Pt.tipA, 0, 0, 0); put(Pt.tipB, 0, 0, 0);
    Pt.code.at(0, 0, { alpha: 0 }); Pt.code.spans[0][1].style.color = css(COL.text);
    Object.values(Pt.words).forEach((el) => { el.style.opacity = "0"; });
    Pt.words.king.textContent = "king"; Pt.words.queen.textContent = "queen";
    if (!g) return;
    plane(g);
    const th = { CANON: TH.CANON, ALIGNED: 0, MATH: 0, ALIGNED_N: 0, OPPOSITE_N: 180 }[name];
    if (th != null) {
      pair(g, th);
      Pt.ro[0].set("dot product = ", dotAt(th));
      if (name !== "CANON" && name !== "ALIGNED") nums(Pt, th);
      if (name === "MATH") placeCode(Pt);
    }
    if (name === "WORDS") {
      words(g, Pt);
      arc(g, 26.57, 53.13, { r: 0.9, col: COL.muted });
      Pt.ro[0].set("king · queen = ", KQ);
      Pt.ro[1].set("king · banana = ", KB, { row: 1, col: COL.text });
    }
    if (name === "ATTN") {
      Pt.words.king.textContent = "query"; Pt.words.queen.textContent = "key";
      words(g, Pt, { alpha: { banana: 0 }, ddx: { king: QUERY_DX } });
      Pt.ro[0].set("query · key = ", KQ);
      Pt.ro[1].set("attention score", "", { row: 1, leadCol: COL.dim });
    }
  }

  window.EP = {
    A2, RB, A_DEG, bAt, dotAt, TH, CODE, WORDS, KQ, KB, fmtd,
    PLANE, RO, FORM, TIP, CODE_TOP, WORD_OFF, QUERY_DX,
    parts, put, nums, placeCode, bg, plane, arc, rightMark, pair, words, state, mix,
  };
})();
