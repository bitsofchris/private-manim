// ep06.js — episode 6's numbers, layout and rest states (one matmul, whole batch).
// Linked into each beat as `ep/`, after vendor/gsap, iso/iso.js and vec/vec.js:
//   ln -s ../_ep NN_beat/ep
// Everything drawn comes from the shared plane kit (VEC); this file only holds
// the ledger (storyboard.md), where things sit, and the five states beats open
// and end on. Beats never edit it; they draw their changes on top of a state.
(function () {
  const { COL, css } = ISO;
  const { fmtv, vtxt, SLOT } = VEC;

  // ---- the ledger (storyboard.md; the (5, 3) @ (3, 2) example of episodes 3-6) ----
  const X = [[1, 2, -1], [0, -1, 3], [2, 0.5, 1], [-1, 1, 2], [3, -2, 0]];   // the batch, (5, 3)
  const W = [[2, -1], [0.5, 1], [-1, 2]];                                     // the map, (3, 2): row i = where input i lands
  const B = [0.1, -0.2];                                                      // the bias, (2,)
  const XW = X.map((x) => [0, 1].map((j) => x.reduce((s, v, i) => s + v * W[i][j], 0)));
  const Y = XW.map((r) => r.map((v, j) => Math.round((v + B[j]) * 100) / 100));
  // XW = [4, −1], [−3.5, 5], [3.25, 0.5], [−3.5, 6], [5, −5]
  // Y  = [4.1, −1.2], [−3.4, 4.8], [3.35, 0.3], [−3.4, 5.8], [5.1, −5.2]
  // Colour is the input direction: column i of X and row i of W are SLOT[i]
  // (teal, blue, gold). Y's digits are white. Magenta is the one hero.

  // ---- layout (px, 1080 x 1920; stage y 230-1100) ----
  const SIZE = 60, RH = 68;                               // digits and labels; row pitch
  const TOP_LABEL = 236, W_TOP = 312;                     // W's and b's labels; their first row
  const BOT_LABEL = 556, X_TOP = 632;                     // X's and Y's labels; their first row
  const CARD_TOP = 1012;                                  // the code card, centred, at the band top; it grows
                                                          // down to 1196 with its comment line (bottom <= 1330)
  const XM = { left: 100, cw: 100 };                      // X: 3 columns, x 100-400
  const WM = { left: 340, cw: 100 };                      // W: 2 columns, x 340-540 (above the gap)
  const YM = { left: 620, cw: 150 };                      // Y: 2 columns, x 620-920; b sits above it
  const ARROW_X = 510;                                    // the → per row, between X and Y
  const LABEL_GAP = 24;                                   // tag after a label

  const rowY = (top, r) => top + r * RH;
  const width = (M, cols) => M.cw * cols;

  // ---- DOM parts, made once per beat ----
  function cells(root, vals, M, top, colOf, txt = fmtv) {
    return vals.map((row, r) => row.map((v, c) => VEC.cell(root, txt(v, c, row.length), {
      left: M.left + c * M.cw, top: rowY(top, r), width: M.cw, height: RH, size: SIZE, col: colOf(r, c),
    })));
  }
  // the code card: VEC.codeCard with three rows (line 1, the shapes comment, the big comment);
  // show({ b, line2 }) picks what is visible: b adds " + b", line2 is null | "shapes" | "big".
  // Spans keep their colour until a beat sets it; state() resets them.
  function codeCard(root) {
    const c = VEC.codeCard(root, [
      [["Y = X @ W"], [" + b"]],
      [["# "], ["(5,"], ["3"], [")"], [" @ "], ["("], ["3"], [",2)"], [" → "], ["(5,2)"]],
      [["# ("], ["batch,"], ["seq"], [","], ["3"], [") @ (3,2)"]],
    ]);
    const card = { el: c.el, line1: c.spans[0], shapes: c.spans[1], big: c.spans[2], rows: [...c.el.children] };
    card.show = (o = {}) => {
      card.line1[1].style.display = o.b ? "" : "none";
      card.rows[1].style.display = o.line2 === "shapes" ? "" : "none";
      card.rows[2].style.display = o.line2 === "big" ? "" : "none";
    };
    card.at = (o = {}) => c.at(VEC.centreLeft(c.el), CARD_TOP, o);      // centred; call after show()
    return card;
  }
  // a matrix label: the name in --text, two spaces, the shape in --dim; dims are their own spans
  // ("X  (5, 3)": spans name, "  (", d0, ", ", d1, ")"); { el, name, dims[] }
  function nameTag(root, name, dims) {
    const el = document.createElement("div");
    el.style.cssText = `position:absolute;left:0;top:0;font-size:${SIZE}px;line-height:${Math.round(SIZE * 1.1)}px;` +
      `white-space:pre;color:${css(COL.dim)};font-variant-numeric:tabular-nums;`;
    const sp = (t, col) => { const s = document.createElement("span"); s.textContent = t; if (col) s.style.color = css(col); el.appendChild(s); return s; };
    const n = sp(name, COL.text); sp("  (");
    const ds = dims.map((d, i) => { const s = sp(String(d)); if (i < dims.length - 1) sp(", "); return s; });
    if (dims.length === 1) sp(",");
    sp(")");
    root.appendChild(el);
    return { el, name: n, dims: ds };
  }
  // P: card, the one code card (monospace), three rows, shown by card.show():
  //   card.line1: spans "Y = X @ W", " + b"
  //   card.shapes: spans "# ", "(5,", "3", ")", " @ ", "(", "3", ",2)", " → ", "(5,2)"
  //   card.big:    spans "# (", "batch,", "seq", ",", "3", ") @ (3,2)"   (beat 8 retypes "seq" from "5")
  //   (60 px monospace holds ~24 columns in the safe width, so the tuples have no space after the comma)
  // x[r][c] / w[r][c] / y[r][c] / b[0][c] cells, xB / wB / yB / bB brackets,
  // names {x, w, y, b} (nameTag), tags {data, map}, arrows[r] ("→"), hl / hl2 / hl3 highlight boxes.
  function parts(root) {
    const card = codeCard(root);
    const x = cells(root, X, XM, X_TOP, (r, c) => SLOT[c]);
    const w = cells(root, W, WM, W_TOP, (r) => SLOT[r]);
    const y = cells(root, XW, YM, X_TOP, () => COL.text);
    const b = cells(root, [B], YM, W_TOP, () => COL.text, vtxt);
    const xB = VEC.brackets(root, XM.left, X_TOP, XM.left + width(XM, 3), 5 * RH);
    const wB = VEC.brackets(root, WM.left, W_TOP, WM.left + width(WM, 2), 3 * RH);
    const yB = VEC.brackets(root, YM.left, X_TOP, YM.left + width(YM, 2), 5 * RH);
    const bB = VEC.brackets(root, YM.left, W_TOP, YM.left + width(YM, 2), RH);
    const names = { x: nameTag(root, "X", [5, 3]), w: nameTag(root, "W", [3, 2]), y: nameTag(root, "Y", [5, 2]), b: nameTag(root, "b", [2]) };
    const tag = (t, col) => ISO.label(root, t, { size: SIZE, color: css(col) });
    const tags = { data: tag("data", COL.data), map: tag("map", COL.hero) };
    const arrows = X.map(() => { const el = ISO.label(root, "→", { size: SIZE, color: css(COL.dim), width: 120, align: "center" }); el.style.lineHeight = `${RH - 8}px`; return el; });
    return { card, x, w, y, b, xB, wB, yB, bB, names, tags, arrows,
             hl: VEC.hbox(root), hl2: VEC.hbox(root), hl3: VEC.hbox(root) };
  }

  // ---- placement helpers ----
  const put = (el, left, top, alpha = 1, col) => {
    el.style.transform = `translate(${left.toFixed(1)}px, ${top.toFixed(1)}px)`;
    el.style.opacity = alpha.toFixed(3);
    if (col) el.style.color = css(col);
  };
  // where each label sits (left, top); W's is centred over W
  const LABEL = {
    x: () => [XM.left, BOT_LABEL],
    y: () => [YM.left, BOT_LABEL],
    w: (Pt) => [WM.left + width(WM, 2) / 2 - Pt.names.w.el.offsetWidth / 2, TOP_LABEL],
    b: () => [YM.left, TOP_LABEL],
  };
  // a tag right after a label (data after X's, map after W's)
  const tagAt = (Pt, key) => { const [l, t] = LABEL[key](Pt); return [l + Pt.names[key].el.offsetWidth + LABEL_GAP, t]; };
  const arrowAt = (r) => [ARROW_X - 60, rowY(X_TOP, r) + 4];
  // highlight-box rects ([left, top, w, h])
  const RECT = {
    xRow: (r) => [XM.left - 12, rowY(X_TOP, r) + 2, width(XM, 3) + 24, RH - 4],
    yRow: (r) => [YM.left - 12, rowY(X_TOP, r) + 2, width(YM, 2) + 24, RH - 4],
    x: () => [XM.left - 40, X_TOP - 12, width(XM, 3) + 80, 5 * RH + 24],
    w: () => [WM.left - 40, W_TOP - 12, width(WM, 2) + 80, 3 * RH + 24],
    wRow: (r) => [WM.left - 12, rowY(W_TOP, r) + 2, width(WM, 2) + 24, RH - 4],
    wCol: (c) => [WM.left + c * WM.cw - 4, W_TOP - 8, WM.cw + 8, 3 * RH + 16],
    b: () => [YM.left - 40, W_TOP - 12, width(YM, 2) + 80, RH + 24],
    span: (el, pad = 6) => {                                 // a box round a span of the code card
      const r = el.getBoundingClientRect(), root = el.closest("#root").getBoundingClientRect();
      return [r.left - root.left - pad, r.top - root.top - pad + 4, r.width + 2 * pad, r.height + 2 * pad - 8];
    },
  };

  function bg(g) { if (!g) return; g.clearRect(0, 0, ISO.W, ISO.H); g.fillStyle = css(COL.bg); g.fillRect(0, 0, ISO.W, ISO.H); }

  // ---- the rest states (storyboard.md "States") ----
  // INPUTS  : card "Y = X @ W"; W, X, the →s, Y's label and empty brackets. No b.
  // PRODUCT : INPUTS + Y's digits = X @ W.
  // SHAPES  : PRODUCT; the card gains "# (5,3) @ (3,2) → (5,2)", the inner 3s --dim.
  // CANON   : SHAPES with "Y = X @ W + b"; b above Y; Y's digits = X @ W + b (00_layout).
  // BIG     : CANON with the comment "# (batch,seq,3) @ (3,2)", its 3 magenta.
  function state(Pt, g, name) {
    const bias = name === "CANON" || name === "BIG";
    const C = Pt.card;
    C.show({ b: bias, line2: { SHAPES: "shapes", CANON: "shapes", BIG: "big" }[name] || null });
    C.line1.forEach((s) => { s.style.color = css(COL.text); s.style.opacity = "1"; });
    C.shapes.forEach((s, i) => { s.style.color = css(i === 0 ? COL.dim : i === 2 || i === 6 ? COL.dim : COL.text); s.style.opacity = "1"; });
    C.big.forEach((s, i) => { s.style.color = css(i === 0 ? COL.dim : i === 4 ? COL.hero : COL.text); s.style.opacity = "1"; });
    C.big[0].textContent = "# ("; C.big[1].textContent = "batch,"; C.big[2].textContent = "seq";
    C.at();
    // the matrices
    [Pt.x, Pt.w].forEach((m) => m.forEach((row) => row.forEach((c) => { c.home(); c.color(c.col0); c.border(COL.hero, 0); })));
    Pt.y.forEach((row, r) => row.forEach((c, k) => {
      c.set(fmtv((bias ? Y : XW)[r][k])); c.home({ alpha: name === "INPUTS" ? 0 : 1 }); c.color(COL.text); c.border(COL.hero, 0);
    }));
    Pt.b[0].forEach((c) => { c.home({ alpha: bias ? 1 : 0 }); c.color(COL.text); c.border(COL.hero, 0); });
    [Pt.xB, Pt.wB, Pt.yB].forEach((br) => { br.color(COL.dim); br.at(0, 0); });
    Pt.bB.color(COL.dim); Pt.bB.at(0, 0, { alpha: bias ? 1 : 0 });
    // labels, tags, arrows
    Object.entries(Pt.names).forEach(([k, n]) => {
      const [l, t] = LABEL[k](Pt);
      put(n.el, l, t, k === "b" && !bias ? 0 : 1);
      n.name.style.color = css(COL.text); n.dims.forEach((d) => { d.style.color = css(COL.dim); });
    });
    ["data", "map"].forEach((k) => { const [l, t] = tagAt(Pt, k === "data" ? "x" : "w"); put(Pt.tags[k], l, t, 0); });
    Pt.arrows.forEach((el, r) => { const [l, t] = arrowAt(r); put(el, l, t, 1, COL.dim); });
    [Pt.hl, Pt.hl2, Pt.hl3].forEach((h) => h.rect(RECT.x(), 0));
    bg(g);
  }

  window.EP = {
    X, W, B, XW, Y,
    CARD_TOP, SIZE, RH, TOP_LABEL, W_TOP, BOT_LABEL, X_TOP, XM, WM, YM, ARROW_X, LABEL, RECT,
    rowY, parts, put, tagAt, arrowAt, bg, state,
  };
})();
