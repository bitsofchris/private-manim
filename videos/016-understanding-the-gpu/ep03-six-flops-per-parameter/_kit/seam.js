// seam.js — ep 3's seam states: SC.SEAM[n] is the state at cut n (the end of beat n and the start of
// beat n+1); SEAM[0] is frame 0. Loaded after ep/layer.js. tools/hf_state_check.js compares a beat's
// S(0) and S(end) with these, merged over SC.REST. The storyboard's seam-states table is the prose
// version of this file.
//
// Two images:
//   layer(hero, ly)     beats 01–06: the tiny layer, no chip parts
//   chip(hero, extra)   beats 07–08: the series chip at rest (CPU, queue, GPU memory), the code card
//                       docked at the band top (cy 1246: bottom edge 1330, captions anchored bottom)
(function () {
  const SC = window.SC, EP = window.EP, SIX = SC.D.code.sixN;
  const NO_CHIP = { cpu: 0, queueO: 0, chip: 0, hbm: 0, strip: 0, meter: 0, shimmer: 0, code: { o: 0 } };
  const layer = (hero, ly) => Object.assign({ hero }, NO_CHIP, { ly: Object.assign({ o: 1 }, ly) });
  const chip = (hero, extra) => Object.assign({ hero, cpu: 1, queueO: 1, chip: 1, hbm: 1, strip: 0, meter: 0,
    lit: SC.D.run.mfu, shimmer: 1, ly: { o: 0 } }, extra);
  const W = { o: 1, name: "W", fill: 0 }, dW = { o: 1, name: "dW", fill: 6 };
  const eq = (k) => ({ o: 1, text: EP.eq[k] });
  const bar = (f, split) => ({ o: 1, f, split });
  const rd = (text) => ({ o: 1, text });
  const LINE1 = SIX[0].t.length;
  SC.SEAM = {
    0: layer("readout", { run: 1, bar: bar([1, 1, 1], 0), rd: rd(EP.hook) }),           // frame 0: working
    1: layer("readout", { bar: bar([1, 1, 1], 0), rd: rd(EP.hook) }),                   // "…on the backward pass."
    2: layer(null, { mat: W, eq: eq("fwd") }),                                         // "…six weights."
    3: layer("readout", { pass: "fwd", prog: 6, mat: W, eq: eq("fwd"),
                          bar: bar([1, 0, 0], 1), rd: rd(EP.count(12)) }),                // "…this entire layer."
    4: layer("back", { pass: "back", prog: 6, inLab: EP.errIn, outLab: EP.errOut, mat: W, eq: eq("back"),
                       bar: bar([1, 1, 0], 1), rd: rd(EP.count(24)) }),                   // "…multiply and add each."
    5: layer("grad", { pass: "grad", prog: 6, outLab: EP.errOut, mat: dW, eq: eq("grad"),
                       bar: bar([1, 1, 1], 1), rd: rd(EP.count(36)) }),                   // "…is two more."
    6: layer("readout", { pass: "grad", prog: 6, outLab: EP.errOut, mat: dW, eq: eq("grad"),
                          bar: bar([1, 1, 1], 0), rd: rd(EP.total) }),                    // "…per weight per token."
    7: chip(null, { code: { o: 1, lines: SIX, typed: LINE1, lit: "sixN", cursor: 0, cy: 1246 } }),  // "…times tokens."
    8: chip("chip", { shimmer: 0, title: EP.run,
                      code: { o: 1, lines: SIX, typed: Infinity, lit: null, cursor: 0, cy: 1246 } }),  // the end: "720 teraflops."
  };
})();
