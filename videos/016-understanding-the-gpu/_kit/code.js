// code.js — the code card of the Understanding the GPU series (016), adapted
// from 014's kit/code.js (same typist, same API). Here the card docks in the
// bottom slot under the chip (the storyboards' "code card bottom-middle")
// instead of replacing the stage, and its type shrinks to fit the longest line.
// Loaded after kit/chip.js; chip.js picks it up through window.SC_makeCode and
// drives it from S.code.
//
// Card: x 65–950, centred on y = cy (default 1335: the bottom slot, y 1110–1536,
// which the time strip uses when the card is off). 40 px monospace fits 36
// characters; a longer line shrinks the type for the whole card.
//
// S.code fields:
//   o 0..1            opacity
//   lines [{t, lit}]  from kit/data.js (GPU_DATA.code.*)
//   typed N           characters shown so far, over all lines in order; Infinity = all.
//                     Use SC_typedAt(lines, seconds) for the typing look.
//   lit NAME|null     the line whose `lit` equals NAME is drawn magenta
//   cursor 0|1        a block cursor after the last typed character
//   blink 0..         seconds, for the cursor's 0.5 s blink (pass the beat time)
//   cy                the card's centre y (default CARD.cy)
(function () {
  const PAL = { panel: "#14142B", ink: "#ECEBE4", hero: "#C084FC", dim: "#8A8FB0" };
  const CARD = { x: 65, w: 885, pad: 28, size: 40, rows: 6, cy: 1335, charW: 0.6 };
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

  // How many characters a typist has landed `seconds` after starting (014's typist).
  function typedAt(lines, seconds, cps = 22) {
    if (seconds <= 0) return 0;
    const mean = 1 / cps;
    let t = 0, n = 0;
    for (let li = 0; li < lines.length; li++) {
      const s = lines[li].t;
      if (li > 0) t += mean * 2.5;
      for (let i = 0; i < s.length; i++) {
        t += s[i] === " " ? mean * 0.5 : mean * (0.45 + 1.1 * hash(n * 7 + li * 131 + 1));
        if (t > seconds) return n;
        n++;
      }
    }
    return n;
  }
  function typingSeconds(lines, cps = 22) {
    let lo = 0, hi = 60;
    const total = lines.reduce((a, l) => a + l.t.length, 0);
    for (let k = 0; k < 24; k++) { const m = (lo + hi) / 2; if (typedAt(lines, m, cps) >= total) hi = m; else lo = m; }
    return hi;
  }

  function makeCode(root) {
    const card = document.createElement("div");
    card.style.cssText = `position:absolute;left:${CARD.x}px;top:0px;width:${CARD.w}px;height:100px;` +
      `border-radius:28px;background:${PAL.panel};overflow:hidden;`;
    card.setAttribute("data-layout-allow-overflow", "");
    card.setAttribute("data-layout-allow-occlusion", "");
    root.appendChild(card);
    const rows = [];
    for (let i = 0; i < CARD.rows; i++) {
      const el = document.createElement("div");
      el.style.cssText = `position:absolute;left:${CARD.pad}px;white-space:pre;color:${PAL.ink};`;
      el.style.fontFamily = "monospace"; el.style.fontWeight = "700";
      card.appendChild(el);
      rows.push(el);
    }
    const cursor = document.createElement("span");
    cursor.textContent = "█";
    cursor.style.cssText = `color:${PAL.hero};`;
    function set(C) {
      const o = C.o == null ? 0 : C.o;
      card.style.opacity = o; card.style.visibility = o > 0.001 ? "visible" : "hidden";
      if (o <= 0.001) return;
      const lines = C.lines || [];
      const longest = Math.max(1, ...lines.map((l) => l.t.length));
      const size = Math.min(CARD.size, Math.floor((CARD.w - CARD.pad * 2) / (longest * CARD.charW)));
      const pitch = Math.round(size * 1.4);
      const nRows = Math.max(2, Math.min(CARD.rows, lines.length)), h = CARD.pad * 2 + nRows * pitch;
      const cy = C.cy == null ? CARD.cy : C.cy;
      card.style.height = `${h}px`; card.style.top = `${Math.round(cy - h / 2)}px`;
      let left = C.typed == null ? Infinity : Math.max(0, Math.floor(C.typed));
      const shown = [];
      lines.forEach((ln, i) => {
        const n = Math.min(ln.t.length, left);
        if (left > 0 || i === 0) shown.push({ ln, n });
        left -= ln.t.length;
      });
      const first = Math.max(0, shown.length - CARD.rows);
      const blinkOn = C.blink == null ? true : Math.floor(C.blink / 0.5) % 2 === 0;
      rows.forEach((el, r) => {
        el.style.top = `${CARD.pad + r * pitch}px`;
        el.style.fontSize = `${size}px`; el.style.lineHeight = `${pitch}px`; el.style.height = `${pitch}px`;
        const s = shown[first + r];
        if (!s) { el.textContent = ""; el.style.visibility = "hidden"; return; }
        el.style.visibility = "visible";
        el.textContent = s.ln.t.slice(0, s.n);
        const isComment = s.ln.t.trim().startsWith("#");
        el.style.color = s.ln.lit && C.lit && s.ln.lit === C.lit ? PAL.hero : isComment ? PAL.dim : PAL.ink;
        if (C.cursor && first + r === shown.length - 1 && blinkOn) el.appendChild(cursor);
      });
    }
    return { set, card, rows, CARD };
  }
  window.SC_makeCode = makeCode;
  window.SC_typedAt = typedAt;
  window.SC_typingSeconds = typingSeconds;
})();
