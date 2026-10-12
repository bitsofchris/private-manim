// ep08.js — episode 8's numbers, layout and rest states (the dot product).
// Linked into each beat as `ep/`, after vendor/gsap, iso/iso.js and vec/vec.js:
//   ln -s ../_ep NN_beat/ep
// Everything drawn comes from the shared plane kit (VEC); this file holds the
// ledger (storyboard.md), where things sit, and the states beats open and end
// on. Beats never edit it; they draw their changes on top of a state.
(function () {
  const { COL, css, mix, lerp, clamp01 } = ISO;
  const { fmtv, SLOT } = VEC;

  // ---- the ledger (storyboard.md) ----
  // The pairwise example (Unit 4 notebook, problem 1): 3-D, numbers only, never on the plane.
  const A3 = [1, 2, 3], B3 = [4, -1, 0], PROD = [4, -2, 0], SUM = 2;
  const CODE = ["torch.dot(a, b)", "# 4 − 2 + 0 = 2"];
  // The turning arrow (2-D, on the plane): a fixed, b turns about the origin, |b| = 2|a|.
  // th = the angle from a to b in degrees (counter-clockwise); a · b = 4 cos th.
  // Landmarks on grid points: th 0 -> b (2, 2), 4; th 90 -> b (−2, 2), 0; th 180 -> b (−2, −2), −4.
  const A2 = [1, 1];
  const RB = 2 * Math.SQRT2, A_DEG = 45;
  const bAt = (th) => { const r = (A_DEG + th) * Math.PI / 180; return [RB * Math.cos(r), RB * Math.sin(r)]; };
  const dotAt = (th) => 4 * Math.cos(th * Math.PI / 180);
  const TH = { CANON: 60, ALIGNED: 0, PERP: 90, OPPOSITE: 180 };
  // The embedding payoff: three words as 2-D vectors (a toy; real embeddings have hundreds of numbers).
  const WORDS = { king: [2, 1], queen: [1.5, 2], banana: [-1, 2] };
  const KQ = 5, KB = 0;                                  // king · queen, king · banana
  // A readout shows a value to one decimal while it moves and exactly at the landmarks:
  // 2.8, 4, 0, −4 (never "4.0", never "−0").
  const fmtd = (v) => { const r = Math.round(v * 10) / 10; return Math.abs(r) < 0.05 ? "0" : fmtv(r); };

  // ---- layout (px, 1080 x 1920; stage y 230-1100, band empty) ----
  // The plane: 140 px a step, origin left of centre so the readout and b's sweep both fit.
  const PLANE = { step: 150, ox: 507, oy: 775, ax: { w: -2.6, e: 2.6, s: -2.2, n: 2.6 } };
  // Readouts: the lead text right-aligned to LEAD_R, the number left-aligned at NUM_L,
  // so the number never pushes the words around while it ticks. Two rows.
  const RO = { size: 64, leadR: 700, numL: 724, top: [250, 330] };
  // The pairwise numbers (beats 2-3): rows a, b, products (a * b), then "sum = 2" under them.
  // Numbers are right-aligned on colX (as PyTorch prints a tensor), each comma right after its number.
  const NUM = { size: 72, colX: [470, 640, 810], nameR: 320, brL: 385, brR: 860,
                rowY: { a: 300, b: 410, p: 580, sum: 700 }, ruleY: 530, cellW: 150, cellH: 90,
                sumX: 640 };                             // the sum's centre ("sum =" sits left of it)
  const CODE_TOP = 850;                                  // the code card, centred, under the numbers

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
  // P: ro[0], ro[1] readouts; names {a, b}; cells {a[i], b[i], p[i]}; br {a, b, p} ([ and ] labels);
  // commas {a[i], b[i], p[i]} (p's turn into "+" on "sum"); eq, sum (the "=" and the "2");
  // code (codeCard; spans[0] = torch. / dot / (a, b), spans[1] = # / 4 / − 2 / + 0 / = 2);
  // words {king, queen, banana} labels; hl highlight box.
  function parts(root) {
    const lab = (t, o = {}) => ISO.label(root, t, Object.assign({ size: NUM.size, color: css(COL.dim), width: NUM.cellW, align: "center" }, o));
  const right = (el) => { el.style.textAlign = "right"; return el; };
    const names = { a: lab("a =", { width: 160, align: "right" }), b: lab("b =", { width: 160, align: "right" }) };
    const cells = {}, br = {}, commas = {};
    [["a", A3, SLOT[0]], ["b", B3, SLOT[1]], ["p", PROD, COL.text]].forEach(([k, vals, col]) => {
      cells[k] = vals.map((v) => { const el = right(lab(fmtv(v), { color: css(col) })); el.style.fontVariantNumeric = "tabular-nums"; return el; });
      br[k] = [lab("[", { width: 40 }), lab("]", { width: 40 })];
      commas[k] = vals.slice(0, -1).map(() => lab(",", { width: 40 }));
    });
    const eq = right(lab("sum =", { width: 240 })), sum = lab(fmtv(SUM), { color: css(COL.hero), width: 120 });
    sum.style.transformOrigin = "50% 50%";
    const code = VEC.codeCard(root, [
      [["torch."], ["dot"], ["(a, b)"]],
      [["# ", COL.dim], ["4", COL.dim], [" − 2", COL.dim], [" + 0", COL.dim], [" = 2", COL.dim]],
    ]);
    const words = {};
    Object.keys(WORDS).forEach((w, i) => { words[w] = VEC.label(root, w, { color: css(SLOT[i]), width: 260 }); });
    return { ro: [readout(root), readout(root)], names, cells, br, commas, eq, sum, code, words, hl: VEC.hbox(root) };
  }

  // ---- placement ----
  const put = (el, left, top, alpha = 1, scale = 1) => {
    el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px) scale(${scale.toFixed(4)})`;
    el.style.opacity = clamp01(alpha).toFixed(3);
  };
  // one row of the pairwise numbers, right edges on colX. o: alpha (whole row), cell [i] alpha,
  // br (brackets' alpha), commaA, dy px. Row p has no name; its brackets and commas are dim like a and b's.
  function placeRow(Pt, k, o = {}) {
    const a = o.alpha == null ? 1 : o.alpha, y = NUM.rowY[k] + (o.dy || 0), cA = o.cell || [1, 1, 1];
    NUM.colX.forEach((x, i) => put(Pt.cells[k][i], x - NUM.cellW, y, a * cA[i]));
    put(Pt.br[k][0], NUM.brL - 20, y, a * (o.br == null ? 1 : o.br));
    put(Pt.br[k][1], NUM.brR - 20, y, a * (o.br == null ? 1 : o.br));
    Pt.commas[k].forEach((el, i) => put(el, NUM.colX[i] - 12, y, a * (o.commaA == null ? 1 : o.commaA)));
    if (k !== "p") put(Pt.names[k], NUM.nameR - 160, y, a);
  }
  // the sum line: "sum =" then the magenta 2 at NUM.sumX (o: alpha of each, scale of the 2)
  function placeSum(Pt, o = {}) {
    const y = NUM.rowY.sum;
    put(Pt.eq, NUM.sumX - 60 - 240, y, o.eqA == null ? 1 : o.eqA);
    put(Pt.sum, NUM.sumX - 60, y, o.alpha == null ? 1 : o.alpha, o.scale == null ? 1 : o.scale);
  }
  // a cell's screen centre (to fly a number from one place to another): row k, column i
  const cellCentre = (k, i) => [NUM.colX[i] - 30, NUM.rowY[k] + NUM.cellH / 2];
  // highlight-box rect around column i of a and b
  const colRect = (i) => [NUM.colX[i] - 104, NUM.rowY.a - 8, 128, NUM.rowY.b - NUM.rowY.a + NUM.cellH + 4];
  // the code card: line 2's spans shown up to `n` (0..5), alpha a
  function placeCode(Pt, a = 1, n = 5, o = {}) {
    Pt.code.spans[1].forEach((s, i) => { s.style.opacity = i < n ? "1" : "0"; });
    Pt.code.at(VEC.centreLeft(Pt.code.el), CODE_TOP + (o.dy || 0), { alpha: a, scale: o.scale });
  }

  // ---- canvas ----
  function bg(g) { g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }
  // the plane alone (o: alpha)
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
  // label offsets beside each word's tip (px)
  const WORD_OFF = { king: { dx: 60, dy: 90 }, queen: { dx: 110, dy: -30 }, banana: { dx: -110, dy: -40 } };
  // the three word arrows with their labels. o: alpha {king, queen, banana}, u (draw progress, same keys)
  function words(g, Pt, o = {}) {
    const A = o.alpha || {}, U = o.u || {};
    Object.keys(WORDS).forEach((w, i) => {
      const a = A[w] == null ? 1 : A[w], p = WORDS[w];
      VEC.arrow(g, [0, 0], p, { col: SLOT[i], alpha: a, u: U[w], width: 40 });
      const k = U[w] == null ? 1 : clamp01(U[w]);
      VEC.place(Pt.words[w], p[0] * k, p[1] * k, { dx: WORD_OFF[w].dx, dy: WORD_OFF[w].dy, alpha: a * k });
    });
    VEC.puck(g, 0, 0);
  }

  // ---- the rest states (storyboard.md "States") ----
  // CANON    : the plane, a and b at th 60, the arc, readout "dot product = 2". (00_layout; the look)
  // ALIGNED  : the same at th 0: b (2, 2) under a (1, 1), "dot product = 4".  (end of beats 1 and 4)
  // NUMS     : no plane; rows a = [ 1, 2, 3 ], b = [ 4, −1, 0 ]; code card line 1 only. (end of beat 2)
  // SUM      : NUMS + the rule, products [ 4, −2, 0 ], "sum = 2" (2 magenta), code line 2 full. (end of beat 3)
  // OPPOSITE : the plane at th 180: b (−2, −2), "dot product = −4", arc a half turn.  (end of beat 5)
  // WORDS    : the plane, king, queen, banana; "king · queen = 5" (5 magenta), "king · banana = 0". (end of beat 6)
  // ATTN     : king -> "query", queen -> "key", banana gone; "query · key = 5", "attention score" under it. (end of beat 7)
  function state(Pt, g, name) {
    const plane_ = ["CANON", "ALIGNED", "OPPOSITE", "WORDS", "ATTN"].includes(name);
    const nums = name === "NUMS" || name === "SUM", sum = name === "SUM";
    // reset every DOM part to hidden / rest colours, then show this state's
    Pt.ro.forEach((r) => r.set("", "", { alpha: 0 }));
    ["a", "b", "p"].forEach((k) => placeRow(Pt, k, { alpha: 0 }));
    put(Pt.eq, 0, 0, 0); put(Pt.sum, 0, 0, 0); Pt.code.at(0, 0, { alpha: 0 }); Pt.hl.rect(colRect(0), 0);
    Pt.code.spans[0][1].style.color = css(COL.text);
    Object.values(Pt.words).forEach((el) => { el.style.opacity = "0"; });
    Pt.words.king.textContent = "king"; Pt.words.queen.textContent = "queen";
    if (!g) return;
    bg(g);
    if (plane_) plane(g);
    if (name === "CANON" || name === "ALIGNED" || name === "OPPOSITE") {
      const th = TH[name];
      pair(g, th, { right: 0 });
      Pt.ro[0].set("dot product = ", dotAt(th));
    }
    if (nums) {
      placeRow(Pt, "a"); placeRow(Pt, "b");
      placeCode(Pt, 1, sum ? 5 : 0);
      if (sum) {
        rule(g, 1);
        placeRow(Pt, "p");
        placeSum(Pt);
      }
    }
    if (name === "WORDS") {
      words(g, Pt);
      Pt.ro[0].set("king · queen = ", KQ);
      Pt.ro[1].set("king · banana = ", KB, { row: 1, col: COL.text });
    }
    if (name === "ATTN") {
      Pt.words.king.textContent = "query"; Pt.words.queen.textContent = "key";
      words(g, Pt, { alpha: { banana: 0 } });
      Pt.ro[0].set("query · key = ", KQ);
      Pt.ro[1].set("attention score", "", { row: 1, leadCol: COL.dim });
    }
  }
  // the rule under rows a and b (u: draw progress)
  function rule(g, u = 1, al = 1) {
    if (u <= 0.001 || al <= 0.001) return;
    const x0 = NUM.brL - 10, x1 = lerp(x0, NUM.brR + 30, clamp01(u));
    g.save(); g.strokeStyle = css(COL.dim, 1, 0.8 * al); g.lineWidth = 5; g.lineCap = "round";
    g.beginPath(); g.moveTo(x0, NUM.ruleY); g.lineTo(x1, NUM.ruleY); g.stroke(); g.restore();
  }

  window.EP = {
    A3, B3, PROD, SUM, CODE, A2, RB, A_DEG, bAt, dotAt, TH, WORDS, KQ, KB, fmtd,
    PLANE, RO, NUM, CODE_TOP, WORD_OFF,
    parts, put, placeRow, placeSum, cellCentre, colRect, placeCode, bg, plane, arc, rightMark, pair, words, rule, state, mix,
  };
})();
