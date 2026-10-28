// code.js — the typed code card in the band for the PyTorch Dataloading series
// (014), after prototypes/hyperframes/kb-code/: the editor types the ledger's
// real lines, and the line being typed is the hero (its station lights through
// S.hero in machine.js). Loaded after kit/machine.js; machine.js picks it up
// through window.SC_makeCode and drives it from S.code.
//
// Card: x 65–950, y 1105–1330 (captions anchored bottom sit under it; every
// caption must fit one line). Four lines at 48 px pitch, 44 px monospace
// (≈ 26.5 px a character: 33 characters a line). A fifth line scrolls the first
// one out.
//
// S.code fields:
//   o 0..1          opacity
//   lines [{t, lit}]  from kit/data.js (DL_DATA.code.*)
//   typed N         characters shown so far, over all lines in order; Infinity = all
//   lit NAME|null   the line whose `lit` equals NAME is drawn magenta (usually S.hero)
//   cursor 0|1      a block cursor after the last typed character
(function () {
  const PAL = { bg: "#0B0B14", panel: "#14142B", ink: "#ECEBE4", dim: "#8A8FB0", data: "#2DD4BF", hero: "#C084FC", muted: "#4A5070" };
  const CARD = { x: 65, y: 1105, w: 885, h: 225, pad: 16, pitch: 48, size: 44, rows: 4 };

  function makeCode(root) {
    const card = document.createElement("div");
    card.style.cssText = `position:absolute;left:${CARD.x}px;top:${CARD.y}px;width:${CARD.w}px;height:${CARD.h}px;` +
      `border-radius:24px;background:${PAL.panel};overflow:hidden;`;
    card.setAttribute("data-layout-allow-overflow", "");
    card.setAttribute("data-layout-allow-occlusion", "");
    root.appendChild(card);
    const rows = [];
    for (let i = 0; i < CARD.rows + 1; i++) {
      const el = document.createElement("div");
      el.style.cssText = `position:absolute;left:${CARD.pad}px;top:${CARD.pad + i * CARD.pitch}px;height:${CARD.pitch}px;` +
        `font-size:${CARD.size}px;line-height:${CARD.pitch}px;white-space:pre;color:${PAL.ink};`;
      el.style.fontFamily = "monospace"; el.style.fontWeight = "700";
      card.appendChild(el);
      rows.push(el);
    }
    const cursor = document.createElement("span");
    cursor.textContent = "█";
    cursor.style.cssText = `color:${PAL.hero};`;
    let last = "";
    function set(C) {
      const o = C.o == null ? 0 : C.o;
      card.style.opacity = o; card.style.visibility = o > 0.001 ? "visible" : "hidden";
      if (o <= 0.001) return;
      const lines = C.lines || [];
      let left = C.typed == null ? Infinity : Math.max(0, Math.floor(C.typed));
      // which lines are visible: the last CARD.rows that have started typing
      const shown = [];
      lines.forEach((ln, i) => {
        const n = Math.min(ln.t.length, left);
        if (left > 0 || i === 0) shown.push({ ln, n, i });
        left -= ln.t.length;
      });
      const first = Math.max(0, shown.length - CARD.rows);
      rows.forEach((el, r) => {
        const s = shown[first + r];
        if (!s) { el.textContent = ""; el.style.visibility = "hidden"; return; }
        el.style.visibility = "visible";
        const text = s.ln.t.slice(0, s.n);
        const isComment = s.ln.t.trim().startsWith("#");
        el.textContent = text;
        el.style.color = s.ln.lit && C.lit && s.ln.lit === C.lit ? PAL.hero : isComment ? PAL.muted : PAL.ink;
        if (C.cursor && first + r === shown.length - 1 && s.n < s.ln.t.length + 1) el.appendChild(cursor);
      });
    }
    return { set, card, rows };
  }
  window.SC_makeCode = makeCode;
})();
