// code.js — the shared HyperFrames code card (promoted 2026-10-31 from 014's
// kit/code.js at its second use, 016's adapted copy). It types real lines with
// a typist's uneven rhythm, and the line being typed is the hero. A series
// links it as `_kit/code.js -> ../../_shared/web/code/code.js` and its kit
// (014 machine.js, 016 chip.js) mounts it with a preset:
//   CODE.make(root, CODE.STAGE)            014: fills the stage (y 665), Dark+ colours, gutter bar
//   CODE.make(root, CODE.DOCK)             016: docks in the bottom slot (y 1345), type shrinks to fit
//   CODE.make(root, Object.assign({}, CODE.STAGE, { cy: 900 }))   any other placement
//
// Options (a preset, or your own merged over one):
//   x, w, cy        the card's left, width and centre y (px, 1080×1920)
//   pad             inner padding; rows / minRows  the most rows shown, the fewest the card is sized for
//   size            monospace font size (px, weight 700)
//   pitch           row pitch in px; null = round(size × lead)
//   lead            pitch / size when pitch is null
//   fit             shrink the type for the whole card so the longest line fits w − 2·pad
//   fitChars        or: a line longer than this sets every row to size × fitChars / length,
//                   the pitch kept (014: 28 characters at 48 px; 30 characters → 44 px)
//   charW           a monospace character's width / size, for `fit` (0.6)
//   look "dark+"    VS Code Dark+ colours (tokenize), hero = magenta gutter bar + lighter row
//        "plain"    ink text, comments dim, hero line magenta (016's shipped look; new work uses dark+)
//
// set(C) fields:
//   o 0..1            opacity (the kit multiplies in its flip)
//   lines [{t, lit}]  the lines (each series' kit/data.js)
//   typed N           characters shown so far, over all lines in order; Infinity = all.
//                     Use CODE.typedAt(lines, seconds) for the typing look.
//   typedLines [N]    per-line counts instead of `typed` (lines typed out of order:
//                     014 ep01 types the two `for` headers above a body already there)
//   lit NAME|[NAME]   the line(s) whose `lit` matches are the hero
//   cursor 0|1        a block cursor after the last typed character (of the last line,
//                     or of line `cursorLine` when typing out of order)
//   blink 0..         seconds, for the cursor's 0.5 s blink (pass the beat time)
//   cy                the card's centre y for this frame (default the option's cy)
//
// Globals: window.CODE = { make, tokenize, typedAt, typingSeconds, STAGE, DOCK, SYN };
// SC_makeCode / SC_typedAt / SC_typingSeconds stay as aliases for the beats that use them.
(function () {
  const PAL = { panel: "#14142B", ink: "#ECEBE4", dim: "#8A8FB0", hero: "#C084FC" };
  const STAGE = { x: 65, w: 885, cy: 665, pad: 30, rows: 8, minRows: 3, size: 48, pitch: 64, lead: 1.4, fit: false, fitChars: 28, charW: 0.6, look: "dark+" };
  const DOCK = { x: 65, w: 885, cy: 1345, pad: 28, rows: 6, minRows: 2, size: 40, pitch: null, lead: 1.4, fit: true, charW: 0.6, look: "plain" };
  // VS Code Dark+ on the panel (every colour ≥ 5:1 on #14142B)
  const SYN = { kw: "#569CD6", call: "#DCDCAA", name: "#9CDCFE", num: "#B5CEA8", str: "#CE9178", comment: "#6A9955", punct: "#D4D4D4", cls: "#4EC9B0" };
  const KW = new Set(["for", "in", "def", "class", "return", "import", "from", "with", "as", "if", "else", "elif", "while", "yield", "True", "False", "None", "and", "or", "not", "is", "lambda", "pass", "break", "continue"]);
  const TOKEN = /#.*$|"[^"]*"|'[^']*'|\d+(?:\.\d+)?|[A-Za-z_]\w*|\s+|./g;
  // [{ s, c }]: the line split into runs with their colours (c null for whitespace)
  function tokenize(t) {
    const out = [];
    let m, prev = "";
    TOKEN.lastIndex = 0;
    while ((m = TOKEN.exec(t))) {
      const s = m[0];
      let c = SYN.punct;
      if (s[0] === "#") c = SYN.comment;
      else if (s[0] === '"' || s[0] === "'") c = SYN.str;
      else if (/^\d/.test(s)) c = SYN.num;
      else if (/^[A-Za-z_]/.test(s)) {
        const next = t.slice(TOKEN.lastIndex).match(/^\s*\(/);
        if (KW.has(s)) c = SYN.kw;
        else if (prev === "class" || /^[A-Z]/.test(s)) c = SYN.cls;
        else if (next) c = SYN.call;
        else c = SYN.name;
      } else if (/^\s+$/.test(s)) c = null;
      if (s.trim()) prev = s.trim();
      out.push({ s, c });
    }
    return out;
  }
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
        t += s[i] === " " ? mean * 0.5 : mean * (0.45 + 1.1 * hash(n * 7 + li * 131 + 1));
        if (t > seconds) return n;
        n++;
      }
    }
    return n;
  }
  // The seconds typedAt needs to finish `lines` (for a beat planning its cues).
  function typingSeconds(lines, cps = 22) {
    let lo = 0, hi = 60;
    const total = lines.reduce((a, l) => a + l.t.length, 0);
    for (let k = 0; k < 24; k++) { const m = (lo + hi) / 2; if (typedAt(lines, m, cps) >= total) hi = m; else lo = m; }
    return hi;
  }

  function make(root, opts) {
    const CARD = Object.assign({}, STAGE, opts || {});
    const darkPlus = CARD.look !== "plain", gutter = darkPlus ? 8 : 0;
    const card = document.createElement("div");
    card.style.cssText = `position:absolute;left:${CARD.x}px;top:0px;width:${CARD.w}px;height:100px;` +
      `border-radius:28px;background:${PAL.panel};overflow:hidden;`;
    card.setAttribute("data-layout-allow-overflow", "");
    card.setAttribute("data-layout-allow-occlusion", "");
    root.appendChild(card);
    const rows = [];
    for (let i = 0; i < CARD.rows; i++) {
      const el = document.createElement("div");
      el.style.cssText = `position:absolute;left:0px;width:${CARD.w}px;padding-left:${CARD.pad}px;` +
        `white-space:pre;color:${PAL.ink};border-left:${gutter}px solid transparent;`;
      el.style.fontFamily = "monospace"; el.style.fontWeight = "700";
      card.appendChild(el);
      rows.push(el);
    }
    // Row geometry is written only when it changes, so a beat may restyle
    // code.rows once (014 ep04 sets 46 px) and a fixed-size card keeps it.
    let laid = "";
    function lay(size, pitch) {
      if (laid === `${size}/${pitch}`) return;
      laid = `${size}/${pitch}`;
      rows.forEach((el, i) => {
        el.style.top = `${CARD.pad + i * pitch}px`; el.style.height = `${pitch}px`;
        el.style.fontSize = `${size}px`; el.style.lineHeight = `${pitch}px`;
      });
    }
    const metrics = (lines) => {
      let size = CARD.size;
      if (CARD.fit) {
        const longest = Math.max(1, ...lines.map((l) => l.t.length));
        size = Math.min(size, Math.floor((CARD.w - CARD.pad * 2) / (longest * CARD.charW)));
      } else if (CARD.fitChars) {
        const longest = Math.max(1, ...lines.map((l) => l.t.length));
        size = Math.min(size, Math.floor(CARD.size * CARD.fitChars / longest));
      }
      return { size, pitch: CARD.pitch == null || CARD.fit ? Math.round(size * CARD.lead) : CARD.pitch };
    };
    const m0 = metrics([]);
    lay(m0.size, m0.pitch);

    function fill(el, t, n, hero) {
      el.textContent = "";
      if (!darkPlus) {
        el.textContent = t.slice(0, n);
        el.style.color = hero ? PAL.hero : t.trim().startsWith("#") ? PAL.dim : PAL.ink;
        return;
      }
      // the hero row: a magenta bar in the gutter and a lighter row, the text keeps its colours
      let left = n;
      tokenize(t).forEach((tok) => {
        if (left <= 0) return;
        const span = document.createElement("span");
        span.textContent = tok.s.slice(0, left);
        if (tok.c) span.style.color = tok.c;
        el.appendChild(span);
        left -= tok.s.length;
      });
      el.style.borderLeftColor = hero ? PAL.hero : "transparent";
      el.style.background = hero ? "rgba(192,132,252,0.12)" : "transparent";
    }
    const cursor = document.createElement("span");
    cursor.textContent = "█";
    cursor.style.cssText = `color:${PAL.hero};`;
    function set(C) {
      const o = C.o == null ? 0 : C.o;
      card.style.opacity = o; card.style.visibility = o > 0.001 ? "visible" : "hidden";
      if (o <= 0.001) return;
      const lines = C.lines || [];
      const { size, pitch } = metrics(lines);
      lay(size, pitch);
      const nRows = Math.max(CARD.minRows, Math.min(CARD.rows, lines.length)), h = CARD.pad * 2 + nRows * pitch;
      const cy = C.cy == null ? CARD.cy : C.cy;
      card.style.height = `${h}px`; card.style.top = `${Math.round(cy - h / 2)}px`;
      let left = C.typed == null ? Infinity : Math.max(0, Math.floor(C.typed));
      const shown = [];
      if (C.typedLines) {
        lines.forEach((ln, i) => shown.push({ ln, n: Math.min(ln.t.length, Math.max(0, Math.floor(C.typedLines[i] == null ? Infinity : C.typedLines[i]))) }));
      } else lines.forEach((ln, i) => {
        const n = Math.min(ln.t.length, left);
        if (left > 0 || i === 0) shown.push({ ln, n });
        left -= ln.t.length;
      });
      const litSet = Array.isArray(C.lit) ? C.lit : C.lit ? [C.lit] : [];
      const first = Math.max(0, shown.length - CARD.rows);
      const blinkOn = C.blink == null ? true : Math.floor(C.blink / 0.5) % 2 === 0;
      const cursorRow = C.cursorLine == null ? shown.length - 1 : C.cursorLine;
      rows.forEach((el, r) => {
        const s = shown[first + r];
        if (!s) { el.textContent = ""; el.style.visibility = "hidden"; return; }
        el.style.visibility = "visible";
        fill(el, s.ln.t, s.n, !!(s.ln.lit && litSet.includes(s.ln.lit)));
        if (C.cursor && first + r === cursorRow && blinkOn) el.appendChild(cursor);
      });
    }
    return { set, card, rows, CARD };
  }

  window.CODE = { make, tokenize, typedAt, typingSeconds, STAGE, DOCK, SYN };
  window.SC_makeCode = make;
  window.SC_typedAt = typedAt;
  window.SC_typingSeconds = typingSeconds;
})();
