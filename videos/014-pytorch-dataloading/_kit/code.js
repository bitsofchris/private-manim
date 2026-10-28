// code.js — the code card of the PyTorch Dataloading series (014). The
// machine flips to it (S.flip, machine.js) and it fills the stage; it types
// the ledger's real lines with a typist's uneven rhythm, and the line being
// typed is the hero. Loaded after kit/machine.js; machine.js picks it up
// through window.SC_makeCode and drives it from S.code.
//
// Card: x 65–950, centred on the stage (y 665), sized to its lines (3–8 rows
// at 68 px pitch; captions stay in the band). 52 px monospace (≈ 31 px a
// character: 28 characters a line, the limit kit/data.js keeps).
//
// S.code fields:
//   o 0..1          opacity (machine.js multiplies in S.flip)
//   lines [{t, lit}]  from kit/data.js (DL_DATA.code.*)
//   typed N         characters shown so far, over all lines in order; Infinity = all.
//                   Use SC_typedAt(lines, seconds) for the typing look.
//   lit NAME|null   the line whose `lit` equals NAME is drawn magenta (usually S.hero)
//   cursor 0|1      a block cursor after the last typed character
//   blink 0..       seconds, for the cursor's 0.5 s blink (pass the beat time)
(function () {
  const PAL = { bg: "#0B0B14", panel: "#14142B", ink: "#ECEBE4", dim: "#8A8FB0", data: "#2DD4BF", hero: "#C084FC", muted: "#4A5070" };
  const CARD = { x: 65, w: 885, pad: 34, pitch: 68, size: 52, rows: 8, cy: 665 };
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

  // How many characters a typist has landed `seconds` after starting, over
  // `lines` in order, at about `cps` characters a second: each character takes
  // 0.45–1.55× the mean (hashed by its index, so every frame agrees), a space
  // is quick, and a line break is a 2.5× pause before the next line starts.
  function typedAt(lines, seconds, cps = 22) {
    if (seconds <= 0) return 0;
    const mean = 1 / cps;
    let t = 0, n = 0;
    for (let li = 0; li < lines.length; li++) {
      const s = lines[li].t;
      if (li > 0) t += mean * 2.5;
      for (let i = 0; i < s.length; i++) {
        const c = s[i];
        t += c === " " ? mean * 0.5 : mean * (0.45 + 1.1 * hash(n * 7 + li * 131 + 1));
        if (t > seconds) return n;
        n++;
      }
    }
    return n;
  }
  // The seconds typedAt needs to finish `lines` (for a beat planning its cues).
  function typingSeconds(lines, cps = 22) {
    let lo = 0, hi = 60, total = lines.reduce((a, l) => a + l.t.length, 0);
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
      el.style.cssText = `position:absolute;left:${CARD.pad}px;top:${CARD.pad + i * CARD.pitch}px;height:${CARD.pitch}px;` +
        `font-size:${CARD.size}px;line-height:${CARD.pitch}px;white-space:pre;color:${PAL.ink};`;
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
      const nRows = Math.max(3, Math.min(CARD.rows, lines.length)), h = CARD.pad * 2 + nRows * CARD.pitch;
      card.style.height = `${h}px`; card.style.top = `${Math.round(CARD.cy - h / 2)}px`;
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
        const s = shown[first + r];
        if (!s) { el.textContent = ""; el.style.visibility = "hidden"; return; }
        el.style.visibility = "visible";
        const isComment = s.ln.t.trim().startsWith("#");
        el.textContent = s.ln.t.slice(0, s.n);
        el.style.color = s.ln.lit && C.lit && s.ln.lit === C.lit ? PAL.hero : isComment ? PAL.muted : PAL.ink;
        if (C.cursor && first + r === shown.length - 1 && blinkOn) el.appendChild(cursor);
      });
    }
    return { set, card, rows, CARD };
  }
  window.SC_makeCode = makeCode;
  window.SC_typedAt = typedAt;
  window.SC_typingSeconds = typingSeconds;
})();
