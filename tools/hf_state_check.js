#!/usr/bin/env node
// Check a seam-state HyperFrames beat against its kit's SEAM table, without rendering.
//
// Usage (from anywhere):
//   node tools/hf_state_check.js BEAT_DIR FROM TO [--tol 1e-6] [--still 0.3]
//   e.g. node ../../../tools/hf_state_check.js 05_swap 4 5
//
// For a beat built on a seam-state kit (one state object per frame, drawn by
// `SC.mount(root).draw(g, S)`, with `SC.SEAM[n]` the state at cut n and an
// optional `SC.REST` of defaults; see agents/beat-brief-hyperframes.md), it
// loads the beat's index.html in Node with a stub DOM and a stub GSAP, seeks
// the registered timeline, records the state each draw receives, and compares:
//   S(0)               with SEAM[FROM]   (the cut into this beat)
//   S(end)             with SEAM[TO]     (the cut out of it)
//   S(end - still)     with SEAM[TO]     (the last `still` seconds hold)
// States are compared as flat dotted fields after merging REST; a missing
// field equals 0 / false / "", and a part at opacity 0 (`o` / `opacity`
// 0, or a [text, 0] pair) is compared as hidden, whatever it holds.
// Numbers match within --tol. Neighbouring beats
// can then be checked before either is rendered; tools/seam_check.py diffs
// pixels once both renders exist. Exit code = number of failing checks.
// Tested in tests/test_hf_state_check.py.
"use strict";
const fs = require("fs"), path = require("path"), vm = require("vm");

// Hidden: an object whose own `o` / `opacity` is 0 (or missing), or a
// [text, opacity] pair at opacity 0. What it holds isn't on screen.
const OPACITY = ["o", "opacity"];
function hidden(v) {
  if (Array.isArray(v)) return v.length >= 2 && typeof v[0] === "string" && typeof v[1] === "number" && v[1] <= 0;
  if (!v || typeof v !== "object") return false;
  const k = OPACITY.find((x) => x in v);
  return k !== undefined && !(v[k] > 0);
}

function flatten(v, pre = "", out = {}) {
  if (hidden(v)) { out[pre] = "(hidden)"; return out; }
  if (v && typeof v === "object") {
    for (const k of Object.keys(v)) flatten(v[k], pre ? `${pre}.${k}` : k, out);
  } else if (v !== undefined && v !== null) out[pre] = v;
  return out;
}

const empty = (v) => v === undefined || v === 0 || v === false || v === "" || v === "(hidden)";

// Fields that differ between two states: [key, a, b].
function diff(a, b, tol) {
  const A = flatten(a), B = flatten(b), bad = [];
  for (const k of new Set([...Object.keys(A), ...Object.keys(B)])) {
    const x = A[k], y = B[k];
    if (empty(x) && empty(y)) continue;
    const same = typeof x === "number" && typeof y === "number" ? Math.abs(x - y) <= tol : x === y;
    if (!same) bad.push([k, x, y]);
  }
  return bad;
}

// A DOM just deep enough for the kits: elements with style, children, text.
function stubDom() {
  const ctx2d = () => new Proxy({}, {
    get: (o, k) => (k in o ? o[k] : k === "createRadialGradient" || k === "createLinearGradient" ? () => ({ addColorStop() {} })
      : k === "measureText" ? () => ({ width: 0 }) : () => {}),
    set: (o, k, v) => ((o[k] = v), true),
  });
  const make = (tag) => {
    const e = { tagName: tag, style: {}, children: [], textContent: "", innerHTML: "", offsetWidth: 0, offsetHeight: 0,
      appendChild(c) { this.children.push(c); c.parentNode = this; return c; },
      get firstChild() { return this.children[0] || null; },
      querySelectorAll() { const all = []; const walk = (n) => n.children.forEach((c) => { all.push(c); walk(c); }); walk(this); return all; },
      getContext: ctx2d, setAttribute() {}, getAttribute() { return null; } };
    return e;
  };
  const byId = {};
  return { createElement: make, createElementNS: (ns, tag) => make(tag), getElementById: (id) => (byId[id] = byId[id] || make("div")), fonts: null,
           querySelectorAll: () => [], body: make("body") };
}

function stubGsap(ctx) {
  return {
    parseEase: (name) => {
      const p = /power(\d)\.(inOut|in|out)/.exec(name || "");
      if (!p) return (u) => u;   // a beat's state must not depend on the exact curve at the ends
      const n = +p[1] + 1, f = { in: (u) => u ** n, out: (u) => 1 - (1 - u) ** n,
        inOut: (u) => (u < 0.5 ? 2 ** (n - 1) * u ** n : 1 - (-2 * u + 2) ** n / 2) }[p[2]];
      return f;
    },
    timeline(opts = {}) {
      let time = 0;
      const tl = { to() { return tl; }, set() { return tl; }, fromTo() { return tl; }, from() { return tl; },
        add() { return tl; }, call() { return tl; },
        time() { return time; },
        seek(t) { time = t; if (opts.onUpdate) opts.onUpdate(); return tl; } };
      return tl;
    },
    to() {}, set() {}, registerPlugin() {},
  };
}

function load(beatDir) {
  const html = fs.readFileSync(path.join(beatDir, "index.html"), "utf8");
  const dur = /data-duration="([0-9.]+)"/.exec(html);
  if (!dur) throw new Error("no data-duration in index.html");
  const ctx = { Math, Object, Array, JSON, Number, String, Set, Map, Proxy, console, location: { search: "" } };
  ctx.window = ctx; ctx.globalThis = ctx;
  ctx.document = stubDom();
  ctx.gsap = stubGsap(ctx);
  vm.createContext(ctx);
  let last = null, wrapped = false;
  const wrapMount = () => {
    if (wrapped || !ctx.SC || !ctx.SC.mount) return;
    const real = ctx.SC.mount;
    ctx.SC.mount = (root) => { const k = real(root); return Object.assign({}, k, { draw: (g, S) => { last = S; k.draw(g, S); } }); };
    wrapped = true;
  };
  const tags = [...html.matchAll(/<script(?:\s+src="([^"]+)")?\s*>([\s\S]*?)<\/script>/g)];
  for (const [, src, body] of tags) {
    if (src && /gsap/.test(src)) continue;
    const code = src ? fs.readFileSync(path.join(beatDir, src), "utf8") : body;
    vm.runInContext(code, ctx, { filename: src || "index.html" });
    wrapMount();
  }
  if (!wrapped) throw new Error("no SC.mount: not a seam-state kit beat");
  const tl = ctx.__timelines && ctx.__timelines.main;
  if (!tl) throw new Error('no window.__timelines["main"]');
  return { SC: ctx.SC, seconds: +dur[1], stateAt: (t) => { last = null; tl.seek(t); return last; } };
}

function check(beatDir, from, to, tol = 1e-6, still = 0.3) {
  const b = load(beatDir), SEAM = b.SC.SEAM, REST = b.SC.REST || {};
  if (!SEAM || !(from in SEAM) || !(to in SEAM)) throw new Error(`SEAM[${from}] or SEAM[${to}] missing`);
  const merged = (s) => Object.assign({}, REST, s);
  const rows = [[`S(0) = SEAM[${from}]`, 0, from], [`S(end) = SEAM[${to}]`, b.seconds, to],
                [`S(end - ${still}) = SEAM[${to}]`, b.seconds - still, to]];
  return rows.map(([name, t, n]) => {
    const s = b.stateAt(t);
    if (!s) return { name, bad: [["(no draw at this time)", "", ""]] };
    return { name, bad: diff(merged(s), merged(SEAM[n]), tol) };
  });
}

if (require.main === module) {
  const args = process.argv.slice(2), opt = (k, d) => { const i = args.indexOf(k); return i < 0 ? d : +args.splice(i, 2)[1]; };
  const tol = opt("--tol", 1e-6), still = opt("--still", 0.3);
  if (args.length !== 3) { console.error("usage: hf_state_check.js BEAT_DIR FROM TO [--tol T] [--still S]"); process.exit(2); }
  const res = check(args[0], args[1], args[2], tol, still);
  let fails = 0;
  for (const r of res) {
    if (!r.bad.length) { console.log(`ok    ${r.name}`); continue; }
    fails++;
    console.log(`FAIL  ${r.name}`);
    r.bad.forEach(([k, x, y]) => console.log(`        ${k}: beat ${JSON.stringify(x)} vs seam ${JSON.stringify(y)}`));
  }
  process.exit(fails);
}

module.exports = { flatten, diff, check };
